"""중분류 28 4계층 파이프라인 테스트 (규칙추출 → 임베딩 → GWA → DWA → IWA → GWA매핑).

스케일 테스트: 주요업무 글머리(·)를 규칙기반 1차 추출(사양서 §1.2 step1)로 코퍼스 구성 →
군집 기계(bge-m3 + HDBSCAN)가 중분류 스케일에서 DWA/IWA/GWA를 도출하는지 검증.
※ 추출은 규칙기반(LLM 아님). 군집 파이프라인 메커니즘 테스트가 목적.

1단계 산출(이 스크립트): results/pipeline_test_28/ 에
  tasks.parquet, gwa_assign, dwa_clusters.json, embeddings.npy
"""
import io
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, ".")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

import duckdb
import numpy as np
import pandas as pd

from utils import clustering as CL

OUT = Path("../results/pipeline_test_28")
OUT.mkdir(parents=True, exist_ok=True)
DB = "../results/pipeline.duckdb"

NOISE = re.compile(r"(대분류|한국표준직업분류|^\d+$|^\s*\d+\s*$)")


def parse_bullets(mt: str) -> list[str]:
    """main_tasks_text → 글머리(·) 단위 진술 리스트. 노이즈·페이지헤더 제거."""
    out = []
    for piece in mt.split("·"):
        s = " ".join(piece.split())               # 줄바꿈·중복공백 정리
        s = re.sub(r"\s*\d+┃한국표준직업분류.*$", "", s)
        s = re.sub(r"대분류\s*\d+", "", s).strip()
        if len(s) >= 6 and not NOISE.fullmatch(s):
            out.append(s)
    return out


def main():
    con = duckdb.connect(DB, read_only=True)
    rows = con.execute("""
        SELECT ksco_code, name, main_tasks_text FROM ksco_occupation
        WHERE ksco_code LIKE '28%' AND length(ksco_code)=4
              AND main_tasks_text IS NOT NULL AND length(main_tasks_text)>10
        ORDER BY ksco_code""").fetchall()

    tasks = []
    for code, name, mt in rows:
        for stmt in parse_bullets(mt):
            tasks.append({"sub_code": code, "sub_name": name, "statement": stmt})
    df = pd.DataFrame(tasks)
    print(f"규칙추출 TASK: {len(df)}건 (세분류 {df['sub_code'].nunique()}개)")

    # ONET 41 GWA 라벨 로드
    try:
        gwa = con.execute("SELECT onet_gwa_id, label FROM external_ref.onet_gwa ORDER BY onet_gwa_id").fetchdf()
    except Exception:
        gwa = con.execute("SELECT onet_gwa_id, label FROM onet_gwa ORDER BY onet_gwa_id").fetchdf()
    con.close()

    print("임베딩 중(bge-m3, 첫 실행은 모델 다운로드)...")
    task_emb = CL.embed(df["statement"].tolist())
    gwa_emb = CL.embed(gwa["label"].tolist())
    np.save(OUT / "task_emb.npy", task_emb)

    # GWA 할당 (임베딩 최근접, zero-shot 프록시)
    idx, score = CL.assign_nearest(task_emb, gwa_emb)
    df["gwa_id"] = gwa["onet_gwa_id"].values[idx]
    df["gwa_label"] = gwa["label"].values[idx]
    df["gwa_cos"] = score
    print(f"GWA 버킷 사용: {df['gwa_id'].nunique()}/41개")

    # GWA 버킷 단위 HDBSCAN → DWA 군집
    df["dwa_cluster"] = -1
    clusters = []
    cid = 0
    for gid, grp in df.groupby("gwa_id"):
        if len(grp) < 3:
            continue
        emb = task_emb[grp.index.to_numpy()]
        labels = CL.hdbscan_cluster(emb, min_cluster_size=3, min_samples=1)
        for lab in sorted(set(labels)):
            if lab == -1:
                continue
            members = grp.index.to_numpy()[labels == lab]
            cohesion = CL.mean_cosine(task_emb[members])
            df.loc[members, "dwa_cluster"] = cid
            clusters.append({
                "dwa_cluster": cid, "gwa_id": gid,
                "gwa_label": grp["gwa_label"].iloc[0],
                "size": int(len(members)), "mean_cosine": round(cohesion, 3),
                "members": df.loc[members, "statement"].tolist(),
                "member_idx": [int(x) for x in members],
            })
            cid += 1

    df.to_parquet(OUT / "tasks.parquet")
    (OUT / "dwa_clusters.json").write_text(
        json.dumps(clusters, ensure_ascii=False, indent=2), encoding="utf-8")

    placed = (df["dwa_cluster"] >= 0).sum()
    print(f"DWA 군집 후보: {len(clusters)}개 | 군집배치 task {placed}/{len(df)} "
          f"({placed/len(df)*100:.0f}%)")
    print(f"평균 응집도: {np.mean([c['mean_cosine'] for c in clusters]):.3f} "
          f"(≥0.70 목표)" if clusters else "")
    print("\n[상위 군집 미리보기]")
    for c in sorted(clusters, key=lambda x: -x["size"])[:8]:
        print(f"  #{c['dwa_cluster']} [{c['gwa_label'][:30]}] size={c['size']} cos={c['mean_cosine']}")
        for m in c["members"][:3]:
            print(f"      - {m[:55]}")
    print(f"\n저장: {OUT}/  (tasks.parquet, dwa_clusters.json, task_emb.npy)")


if __name__ == "__main__":
    main()
