"""중분류 28 전수 — Opus 4.8(Claude Code) 직업별 특화 추출 → 적재 → 4계층 → 엑셀.

data/extractions_28.json (Claude Code가 직업별로 특화 작성한 추출)을
production 경로(extract_one self-consistency → persist)로 전수 적재한 뒤,
실제 추출 TASK로 GWA→DWA→IWA→GWA 군집까지 돌리고 엑셀로 내보낸다. API 0원.

실행: python tools/run_28_llm.py
"""
import io
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, ".")
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import duckdb
import numpy as np
import pandas as pd

from utils import clustering as CL
from utils import ksco_fetch as F
from utils.extract_tasks import extract_one, persist

RESULTS = Path(__file__).resolve().parents[1].parent / "results"
DB = str(RESULTS / "pipeline.duckdb")
DATA = Path("data/extractions_28.json")
KST = timezone(timedelta(hours=9))
OUT = RESULTS / f"전수_중분류28_LLM_4계층_{datetime.now(KST).strftime('%Y%m%d_%H%M')}.xlsx"


def make_provider(payload):
    def prov(model, system, user, temperature, seed):
        return json.dumps(payload, ensure_ascii=False), 1200, 600
    return prov


def expand(code, e):
    return {
        "ksco_code": code,
        "tasks": [{"verb": t[0], "object": t[1], "full_statement": t[2],
                   "source_sentence": "", "confidence": 0.9} for t in e.get("t", [])],
        "tools": [{"name": x[0], "category": x[1], "evidence_span": ""} for x in e.get("tools", [])],
        "work_context": [{"category": x[0], "value": x[1], "evidence_span": ""} for x in e.get("wc", [])],
    }


def main():
    extractions = json.loads(DATA.read_text(encoding="utf-8"))
    con = duckdb.connect(DB)

    # ── 1) 전수 적재 (직업별 특화 추출) ──
    tot = {"tasks": 0, "tools": 0, "work_context": 0}
    for code, e in extractions.items():
        ctx = F.fetch_for_extraction(con, code)
        res = extract_one(ctx, con=con, provider=make_provider(expand(code, e)), use_cache=True)
        c = persist(con, res)
        for k in tot:
            tot[k] += c[k]
    print(f"적재: {len(extractions)}개 직업 | task {tot['tasks']} · tool {tot['tools']} · ctx {tot['work_context']}")

    # ── 2) 군집: 중분류 28 task 전체 ──
    tdf = con.execute("""
        SELECT t.task_id, t.ksco_code, o.name, t.full_statement
        FROM task t LEFT JOIN ksco_occupation o ON t.ksco_code=o.ksco_code
        WHERE t.ksco_code LIKE '28%' ORDER BY t.ksco_code""").fetchdf()
    tdf.columns = ["task_id", "ksco_code", "직업명", "full_statement"]
    try:
        gwa = con.execute("SELECT onet_gwa_id,label FROM external_ref.onet_gwa ORDER BY onet_gwa_id").fetchdf()
    except Exception:
        gwa = con.execute("SELECT onet_gwa_id,label FROM onet_gwa ORDER BY onet_gwa_id").fetchdf()

    print(f"군집 대상 TASK {len(tdf)}건 (고유 {tdf['full_statement'].nunique()})")
    emb = CL.embed(tdf["full_statement"].tolist())
    gwa_emb = CL.embed(gwa["label"].tolist())
    gi, gs = CL.assign_nearest(emb, gwa_emb)
    tdf["GWA"] = gwa["label"].values[gi]

    tdf["DWA군집"] = -1
    tdf["DWA(잠정)"] = ""
    clusters = {}
    cid = 0
    for gl, grp in tdf.groupby("GWA"):
        if len(grp) < 4:
            continue
        ge = emb[grp.index.to_numpy()]
        labs = CL.hdbscan_cluster(ge, min_cluster_size=4, min_samples=1)
        for lab in sorted(set(labs)):
            if lab == -1:
                continue
            members = grp.index.to_numpy()[labs == lab]
            me = emb[members]
            medoid = members[(me @ me.T).sum(1).argmax()]
            label = "(잠정) " + tdf.loc[medoid, "full_statement"][:34]
            tdf.loc[members, "DWA군집"] = cid
            tdf.loc[members, "DWA(잠정)"] = label
            clusters[cid] = {"gwa": gl, "size": int(len(members)),
                             "cos": round(CL.mean_cosine(me), 3), "label": label,
                             "jobs": tdf.loc[members, "ksco_code"].nunique()}
            cid += 1
    con.execute("CHECKPOINT")
    con.close()

    placed = (tdf["DWA군집"] >= 0).sum()
    # 4계층 위계 (IWA = GWA 버킷 잠정)
    hier = pd.DataFrame([
        {"GWA(ONET)": c["gwa"], "DWA(잠정)": c["label"], "TASK수": c["size"],
         "직업수": c["jobs"], "응집도": c["cos"]}
        for c in sorted(clusters.values(), key=lambda x: (x["gwa"], -x["size"]))])

    summary = pd.DataFrame([
        {"항목": "추출 직업(세세분류)", "값": len(extractions)},
        {"항목": "총 TASK", "값": int(tot["tasks"])},
        {"항목": "군집 대상 TASK", "값": len(tdf)},
        {"항목": "DWA 군집(잠정)", "값": len(clusters)},
        {"항목": "군집 배치 TASK", "값": int(placed)},
        {"항목": "GWA 버킷 사용", "값": tdf["GWA"].nunique()},
        {"항목": "평균 응집도", "값": round(float(np.mean([c["cos"] for c in clusters.values()])), 3) if clusters else 0},
    ])

    with pd.ExcelWriter(OUT, engine="openpyxl") as xw:
        summary.to_excel(xw, sheet_name="00_요약", index=False)
        hier.to_excel(xw, sheet_name="1_4계층_위계", index=False)
        tdf[["ksco_code", "직업명", "full_statement", "GWA", "DWA(잠정)"]].rename(
            columns={"ksco_code": "코드", "full_statement": "TASK"}).to_excel(
            xw, sheet_name="2_직업별_TASK(전수)", index=False)
    print(f"\n저장: {OUT}")
    print(f"4계층: TASK {len(tdf)} → DWA {len(clusters)} → GWA {tdf['GWA'].nunique()} | "
          f"배치 {placed}/{len(tdf)} ({placed/len(tdf)*100:.0f}%) | "
          f"응집도 {summary[summary['항목']=='평균 응집도']['값'].iloc[0]}")


if __name__ == "__main__":
    main()
