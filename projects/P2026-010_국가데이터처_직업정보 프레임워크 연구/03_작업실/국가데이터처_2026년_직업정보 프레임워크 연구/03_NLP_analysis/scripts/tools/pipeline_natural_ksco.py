"""전체 KSCO 상향식 4계층 — 목표 없는 '자연 절단점' + 전 계층 추적(이름 포함).

방법:
  1) 정제 TASK(행동진술) 임베딩(bge-m3)
  2) 계층군집 1회(평균연결, 코사인) → linkage Z
  3) 절단높이별 군집수 곡선 → '안정구간(plateau)'이 넓은 = 자연스러운 군집수
     (목표값 없이) 가장 안정적인 3개 수준을 DWA/IWA/GWA로 채택
  4) 각 군집 이름 = 대표(medoid) TASK (잠정)
  5) 한국 GWA ↔ ONET 41 유사도 비교(가설)
출력: results/전체KSCO_자연절단_추적_<날짜>.xlsx (직업→TASK→DWA→IWA→GWA 전 계층 이름 추적)
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
from scipy.cluster.hierarchy import fcluster, linkage

from utils import clustering as CL

RESULTS = Path(__file__).resolve().parents[1].parent / "results"
DB = str(RESULTS / "pipeline.duckdb")
KST = timezone(timedelta(hours=9))
OUT = RESULTS / f"전체KSCO_자연절단_추적_{datetime.now(KST).strftime('%Y%m%d_%H%M')}.xlsx"
NOISE = re.compile(r"(대분류|한국표준직업분류)")


def parse_tasks(mt):
    out = []
    for piece in (mt or "").split("·"):
        s = " ".join(piece.split())
        s = re.sub(r"\s*\d+┃한국표준직업분류.*$", "", s)
        s = re.sub(r"대분류\s*\d+", "", s)
        core = re.sub(r"[\s.·∙)]+$", "", s).strip()
        if len(core) < 8 or NOISE.search(core) or not core.endswith("다"):
            continue
        out.append(core)
    return out


def cluster_count_curve(Z, n, grid=400):
    """절단높이 t별 군집수. 반환 [(t, k)]."""
    hmax = float(Z[:, 2].max())
    out = []
    for t in np.linspace(0.02, hmax, grid):
        k = int(fcluster(Z, t=t, criterion="distance").max())
        out.append((float(t), k))
    return out


def natural_plateaus(curve, kmin=4, kmax=900):
    """군집수가 일정하게 유지되는 구간(plateau)의 폭을 계산.
    폭이 넓을수록 '자연스러운/안정적인' 군집수. (목표값 없음)
    반환 [(k, width, t_mid)] width 내림차순."""
    plats = {}
    i = 0
    while i < len(curve):
        k = curve[i][1]
        t0 = curve[i][0]
        j = i
        while j + 1 < len(curve) and curve[j + 1][1] == k:
            j += 1
        t1 = curve[j][0]
        if kmin <= k <= kmax:
            w = t1 - t0
            if k not in plats or w > plats[k][0]:
                plats[k] = (w, (t0 + t1) / 2)
        i = j + 1
    res = [(k, w, tm) for k, (w, tm) in plats.items()]
    res.sort(key=lambda x: -x[1])
    return res


def label_clusters(labels, emb, statements):
    """군집별 medoid(대표) 이름·크기. 반환 dict id -> {name, size, medoid_idx}."""
    info = {}
    for c in np.unique(labels):
        idx = np.where(labels == c)[0]
        me = emb[idx]
        medoid = idx[(me @ me.T).sum(1).argmax()]
        info[int(c)] = {"name": statements[medoid][:46], "size": int(len(idx)), "medoid": int(medoid)}
    return info


def main():
    con = duckdb.connect(DB, read_only=True)
    rows = con.execute("""
        SELECT ksco_code, name, main_tasks_text FROM ksco_occupation
        WHERE length(ksco_code)=4 AND main_tasks_text IS NOT NULL AND length(main_tasks_text)>10
        ORDER BY ksco_code""").fetchall()
    recs = [{"sub_code": c, "sub_name": n, "statement": s}
            for c, n, mt in rows for s in parse_tasks(mt)]
    df = pd.DataFrame(recs).drop_duplicates("statement").reset_index(drop=True)
    stmts = df["statement"].tolist()
    print(f"정제 TASK {len(df)}건 (세분류 {df['sub_code'].nunique()})")
    gwa_ref = con.execute("SELECT onet_gwa_id,label FROM external_ref.onet_gwa ORDER BY onet_gwa_id").fetchdf()
    con.close()

    cache = RESULTS / "_ksco_task_emb_clean.npy"
    if cache.exists() and np.load(cache).shape[0] == len(stmts):
        emb = np.load(cache); print("임베딩 캐시 로드")
    else:
        print("임베딩(bge-m3)..."); emb = CL.embed(stmts, batch_size=64); np.save(cache, emb)

    print("계층군집...")
    Z = linkage(emb, method="average", metric="cosine")
    curve = cluster_count_curve(Z, len(df))
    plats = natural_plateaus(curve)
    print("자연 안정구간 top10 (군집수, 구간폭):")
    for k, w, tm in plats[:10]:
        print(f"   k={k:>4}  폭={w:.3f}  (절단≈{tm:.3f})")

    # 목표 없이: 가장 안정적(폭 넓은) 3개 수준을 granularity 순으로 GWA<IWA<DWA
    top = sorted(plats[:12], key=lambda x: x[0])  # 군집수 오름차순
    # 3개를 고르게: 가장 작은 k(=GWA), 가장 큰 k(=DWA), 중간(=IWA)
    cand = [p for p in top]
    gwa_p = min(cand, key=lambda x: x[0])
    dwa_p = max(cand, key=lambda x: x[0])
    mid_target = (gwa_p[0] + dwa_p[0]) / 2
    iwa_p = min(cand, key=lambda x: abs(x[0] - mid_target))
    levels = {"GWA": gwa_p, "IWA": iwa_p, "DWA": dwa_p}
    print(f"채택: GWA k={gwa_p[0]}, IWA k={iwa_p[0]}, DWA k={dwa_p[0]} (모두 자연 안정구간)")

    df["GWA"] = fcluster(Z, t=gwa_p[2], criterion="distance")
    df["IWA"] = fcluster(Z, t=iwa_p[2], criterion="distance")
    df["DWA"] = fcluster(Z, t=dwa_p[2], criterion="distance")

    gwa_lab = label_clusters(df["GWA"].values, emb, stmts)
    iwa_lab = label_clusters(df["IWA"].values, emb, stmts)
    dwa_lab = label_clusters(df["DWA"].values, emb, stmts)
    df["GWA명"] = df["GWA"].map(lambda c: gwa_lab[c]["name"])
    df["IWA명"] = df["IWA"].map(lambda c: iwa_lab[c]["name"])
    df["DWA명"] = df["DWA"].map(lambda c: dwa_lab[c]["name"])

    # 한국 GWA ↔ ONET 비교
    gwa_emb = CL.embed(gwa_ref["label"].tolist())
    cmp_rows = []
    for c in sorted(df["GWA"].unique()):
        idx = df.index[df["GWA"] == c].to_numpy()
        cen = emb[idx].mean(0); cen /= (np.linalg.norm(cen) + 1e-9)
        sims = gwa_emb @ cen; j = int(sims.argmax())
        cmp_rows.append({"한국GWA": int(c), "GWA명(대표TASK)": gwa_lab[c]["name"],
                         "TASK수": int(len(idx)), "IWA수": int(df.loc[idx, "IWA"].nunique()),
                         "DWA수": int(df.loc[idx, "DWA"].nunique()),
                         "최근접_ONET_GWA": gwa_ref["label"].iloc[j], "유사도": round(float(sims[j]), 3)})
    gwa_df = pd.DataFrame(cmp_rows).sort_values("TASK수", ascending=False)
    matched = gwa_df["최근접_ONET_GWA"].nunique()
    print(f"한국GWA {len(gwa_df)} ↔ ONET 매칭 {matched}/41, 평균유사도 {gwa_df['유사도'].mean():.3f}")

    # IWA·DWA 목록(상위 계층명 포함)
    def parent_name(level_col, lab, child_ids_col):
        rows = []
        for c in sorted(df[level_col].unique()):
            sub = df[df[level_col] == c]
            rows.append({f"{level_col}": int(c), f"{level_col}명": lab[c]["name"],
                         "상위GWA명": sub["GWA명"].iloc[0],
                         **({"상위IWA명": sub["IWA명"].iloc[0]} if level_col == "DWA" else {}),
                         "하위수": int(sub[child_ids_col].nunique()) if child_ids_col else 0,
                         "TASK수": int(len(sub))})
        return pd.DataFrame(rows).sort_values("TASK수", ascending=False)

    iwa_df = parent_name("IWA", iwa_lab, "DWA")
    dwa_df = parent_name("DWA", dwa_lab, None)

    plat_df = pd.DataFrame([{"군집수": k, "안정구간폭": round(w, 3), "절단거리": round(tm, 3)}
                            for k, w, tm in plats[:20]])
    summary = pd.DataFrame([
        {"계층": "TASK(정제)", "개수": len(df)},
        {"계층": "DWA(자연절단)", "개수": dwa_p[0]},
        {"계층": "IWA(자연절단)", "개수": iwa_p[0]},
        {"계층": "GWA(자연절단)", "개수": gwa_p[0]},
        {"계층": "ONET GWA(비교)", "개수": 41},
        {"계층": "ONET 매칭수", "개수": matched},
        {"계층": "평균 유사도(×1000)", "개수": int(gwa_df["유사도"].mean() * 1000)},
    ])

    chain = df.rename(columns={"sub_code": "세분류", "sub_name": "직업명", "statement": "TASK"})[
        ["세분류", "직업명", "TASK", "DWA명", "IWA명", "GWA명"]]
    byjob = (df.groupby(["sub_code", "sub_name"])["statement"]
             .apply(lambda s: " ▸ ".join(s)).reset_index()
             .rename(columns={"sub_code": "세분류", "sub_name": "직업명", "statement": "도출된 TASK들"}))

    with pd.ExcelWriter(OUT, engine="openpyxl") as xw:
        pd.DataFrame([
            ["방법", "상향식 계층군집(평균연결·코사인), 목표값 없이 자연 안정구간으로 절단"],
            ["군집 이름", "각 군집 대표(medoid) TASK — 잠정(정식 LLM 라벨은 다음 단계)"],
            ["ONET", "입력 아님 — 도출된 한국 GWA와의 유사도 '비교'에만 사용(가설 검증)"],
            ["추출", "전수는 규칙추출(행동진술만). 직업별 LLM 특화는 별도(API/시범)"],
        ], columns=["항목", "설명"]).to_excel(xw, sheet_name="00_안내", index=False)
        summary.to_excel(xw, sheet_name="1_요약", index=False)
        plat_df.to_excel(xw, sheet_name="2_자연절단_안정구간", index=False)
        gwa_df.to_excel(xw, sheet_name="3_GWA목록_ONET비교", index=False)
        iwa_df.to_excel(xw, sheet_name="4_IWA목록", index=False)
        dwa_df.to_excel(xw, sheet_name="5_DWA목록", index=False)
        chain.to_excel(xw, sheet_name="6_전체체인_TASK→GWA", index=False)
        byjob.to_excel(xw, sheet_name="7_직업별_TASK", index=False)

    print(f"\n저장: {OUT}")
    print(f"위계(자연절단): TASK {len(df)} > DWA {dwa_p[0]} > IWA {iwa_p[0]} > GWA {gwa_p[0]}")


if __name__ == "__main__":
    main()
