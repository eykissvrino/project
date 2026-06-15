"""전체 KSCO 4계층 — 절차대로 TASK → DWA → IWA → GWA (전 중분류).

전수 규칙추출(주요업무 글머리) → bge-m3 임베딩 → ONET 41 GWA 할당
 → [GWA 버킷 내] HDBSCAN: TASK→DWA  → [GWA 버킷 내] DWA medoid 재군집: DWA→IWA
 → 위계: GWA ⊃ IWA ⊃ DWA ⊃ TASK (ONET식 nesting, 올바른 비율).

※ 전체 스케일(1,270 직업)은 규칙추출(자동). 직업별 LLM 특화는 별도(API/시범).
출력: results/전체KSCO_4계층_<날짜>.xlsx
"""
import io
import re
import sys
from collections import Counter
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
DB = str(RESULTS / "pipeline.duckdb")
KST = timezone(timedelta(hours=9))
OUT = RESULTS / f"전체KSCO_4계층_{datetime.now(KST).strftime('%Y%m%d_%H%M')}.xlsx"
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
    con = duckdb.connect(DB, read_only=True)
    rows = con.execute("""
        SELECT ksco_code, name, mid_class, main_tasks_text FROM ksco_occupation
        WHERE length(ksco_code)=4 AND main_tasks_text IS NOT NULL AND length(main_tasks_text)>10
        ORDER BY ksco_code""").fetchall()

    recs = []
    for code, name, mid, mt in rows:
        for b in parse_bullets(mt):
            recs.append({"sub_code": code, "sub_name": name, "mid": code[:2], "statement": b})
    df = pd.DataFrame(recs).drop_duplicates("statement").reset_index(drop=True)
    print(f"전 세분류 {len(rows)}개 → 고유 TASK {len(df)}건 (중분류 {df['mid'].nunique()}개)")

    try:
        gwa = con.execute("SELECT onet_gwa_id,label FROM external_ref.onet_gwa ORDER BY onet_gwa_id").fetchdf()
    except Exception:
        gwa = con.execute("SELECT onet_gwa_id,label FROM onet_gwa ORDER BY onet_gwa_id").fetchdf()
    con.close()

    stmts = df["statement"].tolist()
    emb_cache = RESULTS / "_ksco_task_emb.npy"
    if emb_cache.exists() and np.load(emb_cache).shape[0] == len(stmts):
        print("임베딩 캐시 로드")
        emb = np.load(emb_cache)
    else:
        print("임베딩(bge-m3, 수천 건)...")
        emb = CL.embed(stmts, batch_size=64)
        np.save(emb_cache, emb)
    gwa_emb = CL.embed(gwa["label"].tolist())
    gi, gs = CL.assign_nearest(emb, gwa_emb)
    df["gwa_id"] = gwa["onet_gwa_id"].values[gi]
    df["gwa_label"] = gwa["label"].values[gi]

    # GWA 버킷 내: TASK→DWA, 그 다음 DWA medoid→IWA
    df["dwa"] = -1
    df["iwa"] = -1
    dwa_info, iwa_info = {}, {}
    dwa_id = iwa_id = 0
    for gid, grp in df.groupby("gwa_id"):
        idx = grp.index.to_numpy()
        ge = emb[idx]
        if len(idx) < 4:
            continue
        labs = CL.hdbscan_cluster(ge, min_cluster_size=3, min_samples=1, method="leaf")
        local_dwa = {}
        dwa_medoids = []
        for lab in sorted(set(labs)):
            if lab == -1:
                continue
            members = idx[labs == lab]
            me = emb[members]
            medoid_local = members[(me @ me.T).sum(1).argmax()]
            df.loc[members, "dwa"] = dwa_id
            dwa_info[dwa_id] = {"gwa": grp["gwa_label"].iloc[0], "size": int(len(members)),
                                "cos": round(CL.mean_cosine(me), 3),
                                "label": df.loc[medoid_local, "statement"][:40]}
            local_dwa[dwa_id] = members
            dwa_medoids.append((dwa_id, emb[medoid_local]))
            dwa_id += 1
        # DWA medoid 재군집 → IWA (같은 GWA 내). DWA 2개 미만이면 IWA=DWA 승격
        if len(dwa_medoids) >= 3:
            mvecs = np.vstack([m for _, m in dwa_medoids])
            ilabs = CL.hdbscan_cluster(mvecs, min_cluster_size=2, min_samples=1)
        else:
            ilabs = np.array([-1] * len(dwa_medoids))
        # IWA 배정 (노이즈 DWA는 단독 IWA)
        local_iwa = {}
        for k, (did, _) in enumerate(dwa_medoids):
            il = ilabs[k]
            key = (gid, int(il)) if il != -1 else (gid, f"solo{did}")
            if key not in local_iwa:
                local_iwa[key] = iwa_id
                iwa_info[iwa_id] = {"gwa": grp["gwa_label"].iloc[0], "dwa_ids": []}
                iwa_id += 1
            iid = local_iwa[key]
            iwa_info[iid]["dwa_ids"].append(did)
            df.loc[local_dwa[did], "iwa"] = iid

    placed = (df["dwa"] >= 0).sum()
    summary = pd.DataFrame([
        {"계층": "TASK (고유, 규칙추출)", "개수": len(df)},
        {"계층": "DWA (도출)", "개수": len(dwa_info)},
        {"계층": "IWA (도출)", "개수": len(iwa_info)},
        {"계층": "GWA (ONET 사용)", "개수": int(df["gwa_id"].nunique())},
        {"계층": "군집배치 TASK", "개수": int(placed)},
        {"계층": "평균 DWA 응집도", "개수": round(float(np.mean([d["cos"] for d in dwa_info.values()])), 3) if dwa_info else 0},
    ])

    # 위계 표 (GWA → IWA → DWA)
    hier = []
    for iid, info in iwa_info.items():
        for did in info["dwa_ids"]:
            d = dwa_info[did]
            hier.append({"GWA(ONET)": d["gwa"], "IWA번호": iid, "DWA(잠정)": d["label"],
                         "DWA_TASK수": d["size"], "응집도": d["cos"]})
    hdf = pd.DataFrame(hier)
    # GWA별 IWA·DWA 개수 (비율 확인용)
    gstat = (hdf.groupby("GWA(ONET)").agg(IWA수=("IWA번호", "nunique"),
             DWA수=("DWA(잠정)", "count"), TASK수=("DWA_TASK수", "sum"))
             .reset_index().sort_values("TASK수", ascending=False))

    with pd.ExcelWriter(OUT, engine="openpyxl") as xw:
        summary.to_excel(xw, sheet_name="00_요약", index=False)
        gstat.to_excel(xw, sheet_name="1_GWA별_IWA_DWA수", index=False)
        hdf.to_excel(xw, sheet_name="2_위계_GWA_IWA_DWA", index=False)
        df.rename(columns={"sub_code": "세분류", "statement": "TASK", "gwa_label": "GWA",
                           "dwa": "DWA번호", "iwa": "IWA번호"})[
            ["세분류", "sub_name", "TASK", "GWA", "IWA번호", "DWA번호"]].to_excel(
            xw, sheet_name="3_TASK전체", index=False)

    print(f"\n저장: {OUT}")
    print(f"4계층: TASK {len(df)} → DWA {len(dwa_info)} → IWA {len(iwa_info)} → GWA {df['gwa_id'].nunique()}")
    print(f"배치 {placed}/{len(df)} ({placed/len(df)*100:.0f}%) | "
          f"비율 점검: DWA>{len(iwa_info)}(IWA)>{df['gwa_id'].nunique()}(GWA) "
          f"{'정상' if len(dwa_info)>len(iwa_info)>=df['gwa_id'].nunique()*0.5 else '확인필요'}")


if __name__ == "__main__":
    main()
