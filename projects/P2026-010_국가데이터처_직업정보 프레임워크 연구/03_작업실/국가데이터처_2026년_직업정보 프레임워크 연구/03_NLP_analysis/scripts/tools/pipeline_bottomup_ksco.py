"""전체 KSCO 상향식(bottom-up) 4계층 도출 — 연구 가설대로.

  TASK ─(군집)→ DWA ─(군집)→ IWA ─(추상화)→ GWA   ※ ONET을 입력 버킷으로 쓰지 않음
  마지막에 한국형 GWA ↔ ONET 41 GWA 유사도 비교(가설: 비슷하게 나온다).

방법: 정제 TASK 임베딩(bge-m3) → scipy 계층군집(평균연결, 코사인) 1회 →
      3개 높이에서 절단(cut)하여 DWA/IWA/GWA 도출(노이즈 없음, 모든 TASK 배정).
TASK 정제: '~다'로 끝나는 행동진술만(직업명·소제목 제외, §1.2 기준).
출력: results/전체KSCO_상향식_4계층_<날짜>.xlsx
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
OUT = RESULTS / f"전체KSCO_상향식_4계층_{datetime.now(KST).strftime('%Y%m%d_%H%M')}.xlsx"
NOISE = re.compile(r"(대분류|한국표준직업분류)")
# TASK 도출 목표 군집수(상향식이 자연스럽게 만드는 수에 가까운 절단점 자동선택)
TARGET = {"DWA": 350, "IWA": 130, "GWA": 41}


def parse_tasks(mt):
    """주요업무 → 행동진술(TASK)만. '~다'로 끝나야 함(직업명·소제목 제외)."""
    out = []
    for piece in (mt or "").split("·"):
        s = " ".join(piece.split())
        s = re.sub(r"\s*\d+┃한국표준직업분류.*$", "", s)
        s = re.sub(r"대분류\s*\d+", "", s)
        core = re.sub(r"[\s.·∙)]+$", "", s).strip()
        if len(core) < 8 or NOISE.search(core):
            continue
        if not core.endswith("다"):          # 행동진술만(고위공무원·보험 관리자 등 제외)
            continue
        out.append(core)
    return out


def pick_threshold(Z, target):
    """병합 거리 범위를 훑어 군집수가 target에 가장 가까운 절단 거리를 고른다."""
    best_t, best_n, best_gap = None, None, 1e9
    for t in np.linspace(0.05, 1.2, 120):
        n = int(fcluster(Z, t=t, criterion="distance").max())
        if abs(n - target) < best_gap:
            best_gap, best_t, best_n = abs(n - target), t, n
    return best_t, best_n


def main():
    con = duckdb.connect(DB, read_only=True)
    rows = con.execute("""
        SELECT ksco_code, name, main_tasks_text FROM ksco_occupation
        WHERE length(ksco_code)=4 AND main_tasks_text IS NOT NULL AND length(main_tasks_text)>10
        ORDER BY ksco_code""").fetchall()
    recs = []
    for code, name, mt in rows:
        for s in parse_tasks(mt):
            recs.append({"sub_code": code, "sub_name": name, "statement": s})
    df = pd.DataFrame(recs).drop_duplicates("statement").reset_index(drop=True)
    print(f"정제 TASK {len(df)}건 (세분류 {df['sub_code'].nunique()})")

    gwa_ref = con.execute("SELECT onet_gwa_id,label FROM external_ref.onet_gwa ORDER BY onet_gwa_id").fetchdf() \
        if con.execute("SELECT count(*) FROM information_schema.tables WHERE table_name='onet_gwa'").fetchone()[0] else None
    con.close()

    # 임베딩(정제본 캐시는 별도)
    cache = RESULTS / "_ksco_task_emb_clean.npy"
    stmts = df["statement"].tolist()
    if cache.exists() and np.load(cache).shape[0] == len(stmts):
        emb = np.load(cache); print("임베딩 캐시 로드")
    else:
        print("임베딩(bge-m3)..."); emb = CL.embed(stmts, batch_size=64); np.save(cache, emb)

    # ── 상향식 계층 군집 (1회 linkage, 3 높이 절단) ──
    print("계층 군집(평균연결, 코사인)...")
    Z = linkage(emb, method="average", metric="cosine")
    levels = {}
    for name, tgt in TARGET.items():
        t, n = pick_threshold(Z, tgt)
        levels[name] = (t, n, fcluster(Z, t=t, criterion="distance"))
        print(f"  {name}: 절단거리 {t:.3f} → {n}개 (목표 {tgt})")
    df["DWA"] = levels["DWA"][2]
    df["IWA"] = levels["IWA"][2]
    df["GWA"] = levels["GWA"][2]

    # ── 한국형 GWA ↔ ONET 41 비교 (가설 검증) ──
    onet_cmp = None
    if gwa_ref is not None:
        gwa_emb = CL.embed(gwa_ref["label"].tolist())
        cmp_rows = []
        for g in sorted(df["GWA"].unique()):
            cen = emb[df.index[df["GWA"] == g].to_numpy()].mean(0)
            cen = cen / (np.linalg.norm(cen) + 1e-9)
            sims = gwa_emb @ cen
            j = int(sims.argmax())
            # 대표 TASK(센트로이드 최근접)
            members = df.index[df["GWA"] == g].to_numpy()
            me = emb[members]
            rep = df.loc[members[(me @ cen).argmax()], "statement"]
            cmp_rows.append({"한국GWA번호": int(g), "TASK수": int((df["GWA"] == g).sum()),
                             "대표TASK": rep[:40], "최근접_ONET_GWA": gwa_ref["label"].iloc[j],
                             "유사도": round(float(sims[j]), 3)})
        onet_cmp = pd.DataFrame(cmp_rows).sort_values("TASK수", ascending=False)
        matched = onet_cmp["최근접_ONET_GWA"].nunique()
        meancos = onet_cmp["유사도"].mean()
        print(f"한국GWA {len(onet_cmp)}개 ↔ ONET: 매칭된 ONET GWA {matched}/41, 평균유사도 {meancos:.3f}")

    # 위계 표 (GWA→IWA→DWA 개수)
    hier = (df.groupby("GWA").agg(IWA수=("IWA", "nunique"), DWA수=("DWA", "nunique"),
            TASK수=("statement", "count")).reset_index().sort_values("TASK수", ascending=False))

    summary = pd.DataFrame([
        {"계층": "TASK(정제·행동진술)", "개수": len(df), "비고": "직업명·소제목 제외"},
        {"계층": "DWA(상향식 도출)", "개수": levels["DWA"][1], "비고": f"절단 {levels['DWA'][0]:.2f}"},
        {"계층": "IWA(상향식 도출)", "개수": levels["IWA"][1], "비고": f"절단 {levels['IWA'][0]:.2f}"},
        {"계층": "GWA(상향식 도출)", "개수": levels["GWA"][1], "비고": "ONET 미사용·데이터에서 emergent"},
        {"계층": "ONET GWA(비교기준)", "개수": 41, "비고": "가설: 한국GWA가 이와 유사"},
    ])

    with pd.ExcelWriter(OUT, engine="openpyxl") as xw:
        summary.to_excel(xw, sheet_name="00_요약", index=False)
        if onet_cmp is not None:
            onet_cmp.to_excel(xw, sheet_name="1_한국GWA_ONET비교", index=False)
        hier.to_excel(xw, sheet_name="2_위계_GWA별_IWA_DWA수", index=False)
        df.rename(columns={"sub_code": "세분류", "statement": "TASK"})[
            ["세분류", "sub_name", "TASK", "GWA", "IWA", "DWA"]].to_excel(
            xw, sheet_name="3_TASK전체", index=False)

    print(f"\n저장: {OUT}")
    print(f"위계: TASK {len(df)} > DWA {levels['DWA'][1]} > IWA {levels['IWA'][1]} > GWA {levels['GWA'][1]}")


if __name__ == "__main__":
    main()
