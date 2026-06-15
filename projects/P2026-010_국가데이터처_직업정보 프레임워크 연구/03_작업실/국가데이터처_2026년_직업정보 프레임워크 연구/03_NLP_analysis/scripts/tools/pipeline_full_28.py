"""중분류 28 전수 4계층 (51 세세분류 전부). 규칙추출+상속 → 임베딩 → GWA → DWA → IWA → GWA.

전수 커버리지: 51개 세세분류 모두에 부모 세분류 주요업무를 상속해 TASK 부여.
※ 한계: 규칙추출(LLM 아님) + 형제 세세분류는 상속분 동일(특화는 LLM/API 필요).
DWA 라벨은 군집 대표문장 기반 '잠정' (8조항 LLM 라벨링은 다음 단계).

출력: results/전수_중분류28_4계층_<날짜>.xlsx
"""
import io
import re
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

RESULTS = Path(__file__).resolve().parents[1].parent / "results"
DB = RESULTS / "pipeline.duckdb"
KST = timezone(timedelta(hours=9))
OUT = RESULTS / f"전수_중분류28_4계층_{datetime.now(KST).strftime('%Y%m%d_%H%M')}.xlsx"
NOISE = re.compile(r"(대분류|한국표준직업분류)")


def parse_bullets(mt):
    out = []
    for piece in (mt or "").split("·"):
        s = " ".join(piece.split())
        s = re.sub(r"\s*\d+┃한국표준직업분류.*$", "", s)
        s = re.sub(r"대분류\s*\d+", "", s).strip()
        if len(s) >= 6 and not NOISE.search(s):
            out.append(s)
    return out


def main():
    con = duckdb.connect(str(DB), read_only=True)
    # 51 세세분류 + 부모 주요업무
    occs = con.execute("""
        SELECT c.ksco_code, c.name, p.ksco_code AS pcode, p.name AS pname, p.main_tasks_text
        FROM ksco_occupation c
        LEFT JOIN ksco_occupation p ON p.ksco_code = substr(c.ksco_code,1,4)
        WHERE c.ksco_code LIKE '28%' AND length(c.ksco_code)=5
        ORDER BY c.ksco_code""").fetchall()

    task_rows = []          # 직업별 TASK (상속)
    for code, name, pcode, pname, pmt in occs:
        bullets = parse_bullets(pmt)
        for b in bullets:
            task_rows.append({"세세분류": code, "직업명": name, "부모세분류": pcode,
                              "TASK진술(상속)": b})
    tdf = pd.DataFrame(task_rows)
    covered = tdf["세세분류"].nunique()
    no_task = [c for c, *_ in occs if c not in set(tdf["세세분류"])]

    # 고유 진술만 임베딩(중복 형제 제거)
    distinct = tdf["TASK진술(상속)"].drop_duplicates().tolist()
    print(f"세세분류 51 중 TASK 부여 {covered}개 / 무부여 {len(no_task)}개(부모 주요업무 없음): {no_task}")
    print(f"총 TASK행 {len(tdf)} (고유 진술 {len(distinct)})")

    # GWA 라벨
    try:
        gwa = con.execute("SELECT onet_gwa_id,label FROM external_ref.onet_gwa ORDER BY onet_gwa_id").fetchdf()
    except Exception:
        gwa = con.execute("SELECT onet_gwa_id,label FROM onet_gwa ORDER BY onet_gwa_id").fetchdf()
    con.close()

    print("임베딩(bge-m3)...")
    emb = CL.embed(distinct)
    gwa_emb = CL.embed(gwa["label"].tolist())
    gi, gs = CL.assign_nearest(emb, gwa_emb)

    sdf = pd.DataFrame({"TASK진술(상속)": distinct,
                        "할당GWA": gwa["label"].values[gi],
                        "GWA유사도": gs.round(3)})
    sdf["DWA군집"] = -1
    sdf["DWA(잠정)"] = ""
    # GWA 버킷별 HDBSCAN
    cid = 0
    cluster_info = {}
    for gl, grp in sdf.groupby("할당GWA"):
        if len(grp) < 3:
            continue
        ge = emb[grp.index.to_numpy()]
        labs = CL.hdbscan_cluster(ge, min_cluster_size=3, min_samples=1)
        for lab in sorted(set(labs)):
            if lab == -1:
                continue
            members = grp.index.to_numpy()[labs == lab]
            me = emb[members]
            medoid = members[(me @ me.T).sum(1).argmax()]
            label = "(잠정) " + sdf.loc[medoid, "TASK진술(상속)"][:36]
            sdf.loc[members, "DWA군집"] = cid
            sdf.loc[members, "DWA(잠정)"] = label
            cluster_info[cid] = {"gwa": gl, "size": int(len(members)),
                                 "cos": round(CL.mean_cosine(me), 3), "label": label}
            cid += 1

    # 직업별 TASK에 DWA/GWA 붙이기
    tdf = tdf.merge(sdf, on="TASK진술(상속)", how="left")

    # 4계층 위계 (GWA→IWA(=GWA버킷 잠정)→DWA)
    hier = []
    for c, info in sorted(cluster_info.items(), key=lambda x: (x[1]["gwa"], -x[1]["size"])):
        hier.append({"GWA(ONET)": info["gwa"], "IWA(잠정=GWA버킷)": info["gwa"],
                     "DWA(잠정)": info["label"], "TASK수": info["size"], "응집도": info["cos"]})
    hdf = pd.DataFrame(hier)

    summary = pd.DataFrame([
        {"항목": "세세분류 전수", "값": 51},
        {"항목": "TASK 부여된 세세분류", "값": covered},
        {"항목": "TASK 무부여(부모 주요업무 없음)", "값": len(no_task)},
        {"항목": "총 TASK행(상속 포함)", "값": len(tdf)},
        {"항목": "고유 TASK 진술", "값": len(distinct)},
        {"항목": "DWA 군집(잠정)", "값": len(cluster_info)},
        {"항목": "GWA 버킷 사용", "값": hdf["GWA(ONET)"].nunique()},
    ])

    with pd.ExcelWriter(OUT, engine="openpyxl") as xw:
        summary.to_excel(xw, sheet_name="00_요약", index=False)
        pd.DataFrame([
            ["전수 방식", "규칙추출 + 부모 세분류 주요업무 상속 (LLM 아님)"],
            ["한계", "형제 세세분류는 상속분 동일 → 직업별 특화 없음(LLM/API 필요)"],
            ["DWA 라벨", "군집 대표문장 기반 '잠정' (8조항 LLM 라벨링은 다음 단계)"],
        ], columns=["항목", "설명"]).to_excel(xw, sheet_name="00_안내", index=False)
        hdf.to_excel(xw, sheet_name="1_4계층_위계", index=False)
        tdf.to_excel(xw, sheet_name="2_직업별_TASK(전수)", index=False)
        if no_task:
            pd.DataFrame({"TASK무부여_세세분류": no_task}).to_excel(xw, sheet_name="3_보강필요(직업사전)", index=False)

    print(f"\n저장: {OUT}")
    print(f"4계층: 고유TASK {len(distinct)} → DWA(잠정) {len(cluster_info)} → GWA {hdf['GWA(ONET)'].nunique()}")


if __name__ == "__main__":
    main()
