"""Stage 4b — 순수 상향식 GWA 도출 (ONET-유사 형태 목표).

별도 실험: 기존 Stage 4(트랙1 ONET 채택; gwa/iwa_to_gwa)는 건드리지 않는다.
우리가 도출한 TASK→DWA→IWA에서 출발해, ONET 41 GWA와 '닮은 형태'가 나오도록
명시적 기준을 적용해 상향식으로 KR-GWA를 자생시킨다.

── ONET-유사 형태를 만드는 기준 ──────────────────────────────────────
 (1) 군집 단위 = IWA 대표벡터(178). GWA는 IWA 한 단계 위이므로 TASK 트리가 아니라
     IWA 단위를 군집한다(이전 트랙2 실패 원인=16k TASK 트리 상위 거대가지 지배).
 (2) Ward(분산최소) 연결 — average linkage의 사슬효과(한 덩어리 흡수)를 제거해
     ONET처럼 균형 잡힌 일반 범주를 만든다. L2정규화 벡터의 유클리드 Ward = 코사인 정합.
 (3) 추상 입도 = ONET 비율 정합. ONET IWA:GWA ≈ 332:41 ≈ 8.1:1 → 178/8.1 ≈ 22 GWA(기본).
     ONET '개수' 정합(k=41) 변형도 병기 비교.
 (4) 2계층 = 도메인 4 → GWA. 같은 Ward 트리의 4-절단(도메인)과 K-절단(GWA)은 nested →
     각 GWA ⊂ 정확히 1 도메인(ONET의 4대 영역 형태 재현).
 (5) 균형 모니터 — 최대 군집 비율을 보고(과대군집 점검).
 (6) ONET 정합도 검증 — 각 KR-GWA 중심 ↔ ONET 41 최근접 cosine, 매칭 개수·평균·도메인 일치.

흐름:
    diagnose      IWA Ward 트리 → k 스윕(균형·ONET정합) → 권장 k
    cluster --k K 도메인4 + GWA K 절단(nested) → 명명배치 → cache/s4b_*
    (Opus 명명: 도메인 4 + KR-GWA K)
    persist       DB(kr_gwa_bottomup·iwa_to_kr_gwa, CREATE IF NOT EXISTS) + Excel + 비교

PYTHONUTF8=1 권장. 입력 캐시: s4_iwa_centroids.npy(Stage4 prep), s4_gwa_emb.npy(Stage4 map).
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import numpy as np

TEST1_DIR = Path(__file__).resolve().parents[1]
CACHE = TEST1_DIR / "cache"
PROMPTS = TEST1_DIR / "prompts"

IWA_CENT = CACHE / "s4_iwa_centroids.npy"
IWA_IDS = CACHE / "s4_iwa_ids.json"
GWA_EMB = CACHE / "s4_gwa_emb.npy"
GWA_ORDER = CACHE / "s4_gwa_order.json"
TRANSLATION = CACHE / "s4_translation.json"

S4B_LINK = CACHE / "s4b_linkage.npy"
S4B_CLUSTERS = CACHE / "s4b_clusters.json"
S4B_GWA_BATCH = CACHE / "s4b_gwa_batch.json"
S4B_DOMAIN_BATCH = CACHE / "s4b_domain_batch.json"
S4B_SUMMARY = CACHE / "s4b_summary.json"

ONET_RATIO = 8.1          # ONET IWA:GWA = 332:41
N_DOMAIN = 4              # ONET 4대 영역
N_REP_IWA = 12           # 명명용 대표 IWA 라벨 수
DOMAIN_OF = {"4.A.1": "정보 입력", "4.A.2": "정신 과정",
             "4.A.3": "작업 산출", "4.A.4": "타인과의 상호작용"}


def _domain(onet_gwa_id: str) -> str:
    for pre, name in DOMAIN_OF.items():
        if onet_gwa_id.startswith(pre):
            return name
    return "기타"


def _load():
    if not IWA_CENT.exists():
        raise SystemExit("s4_iwa_centroids.npy 없음 — Stage4 prep 먼저")
    if not GWA_EMB.exists():
        raise SystemExit("s4_gwa_emb.npy 없음 — Stage4 map 먼저")
    iwa_emb = np.load(IWA_CENT)
    iwa_ids = json.loads(IWA_IDS.read_text(encoding="utf-8"))
    gwa_emb = np.load(GWA_EMB)
    gwa_order = json.loads(GWA_ORDER.read_text(encoding="utf-8"))
    trans = {t["onet_gwa_id"]: t for t in
             json.loads(TRANSLATION.read_text(encoding="utf-8"))}
    return iwa_emb, iwa_ids, gwa_emb, gwa_order, trans


def _load_iwa_meta() -> dict[str, dict]:
    from pipeline import db
    con = db.get_con(read_only=True)
    rows = con.execute(
        "SELECT iwa_id, label, definition, n_dwa, n_task, n_jobs FROM iwa").fetchall()
    con.close()
    return {r[0]: {"label": r[1], "definition": r[2], "n_dwa": r[3],
                   "n_task": r[4], "n_jobs": r[5]} for r in rows}


def _build_link(iwa_emb):
    """Ward 트리(캐시). L2정규화 벡터 → 유클리드 Ward = 코사인 정합."""
    from scipy.cluster.hierarchy import linkage
    if S4B_LINK.exists():
        Z = np.load(S4B_LINK)
        if Z.shape[0] == iwa_emb.shape[0] - 1:
            return Z
    Z = linkage(iwa_emb, method="ward", metric="euclidean")
    np.save(S4B_LINK, Z)
    return Z


def _nearest_onet(cent, gwa_emb, gwa_order, trans):
    sims = gwa_emb @ cent
    j = int(np.argmax(sims))
    gid = gwa_order[j]
    return gid, trans[gid]["label_kr"], trans[gid]["domain"], float(sims[j])


def _cluster_centroids(labels, iwa_emb):
    out = {}
    for c in sorted(set(labels.tolist())):
        rows = np.where(labels == c)[0]
        v = iwa_emb[rows].mean(axis=0)
        out[c] = v / (np.linalg.norm(v) or 1.0)
    return out


def diagnose():
    from scipy.cluster.hierarchy import fcluster
    iwa_emb, iwa_ids, gwa_emb, gwa_order, trans = _load()
    n = len(iwa_ids)
    Z = _build_link(iwa_emb)
    print(f"[diagnose] IWA {n}개 Ward 트리 · ONET 비율정합 k≈{round(n/ONET_RATIO)} "
          f"(IWA:GWA {ONET_RATIO}:1) · 개수정합 k=41")
    print("  k   n_eff  최대군집  균형(최대%)  ONET매칭/41  평균최근접cos  평균응집")
    for k in [12, 18, round(n/ONET_RATIO), 25, 30, 35, 41, 50]:
        labels = fcluster(Z, t=k, criterion="maxclust")
        sizes = Counter(labels.tolist())
        n_eff = len(sizes)
        mx = max(sizes.values())
        cents = _cluster_centroids(labels, iwa_emb)
        # ONET 매칭
        matched, coss = set(), []
        for c, cent in cents.items():
            gid, _, _, cos = _nearest_onet(cent, gwa_emb, gwa_order, trans)
            matched.add(gid); coss.append(cos)
        # 응집(군집 내 멤버-중심 평균 코사인)
        coh = []
        for c in cents:
            rows = np.where(labels == c)[0]
            coh.append(float((iwa_emb[rows] @ cents[c]).mean()))
        print(f"  {k:<4d}{n_eff:<7d}{mx:<10d}{mx/n*100:>6.1f}%     "
              f"{len(matched):>2d}/41        {np.mean(coss):.3f}         {np.mean(coh):.3f}")
    print("\n  권장: ONET 비율정합 k≈22(같은 추상수준) / ONET 개수정합 k=41(개수 맞춤).")


def run_cluster(k: int):
    from scipy.cluster.hierarchy import fcluster
    iwa_emb, iwa_ids, gwa_emb, gwa_order, trans = _load()
    n = len(iwa_ids)
    meta = _load_iwa_meta()
    Z = _build_link(iwa_emb)

    labels_g = fcluster(Z, t=k, criterion="maxclust")          # GWA
    labels_d = fcluster(Z, t=N_DOMAIN, criterion="maxclust")   # 도메인(같은 트리 nested)
    k_eff = len(set(labels_g.tolist()))

    # GWA → 도메인 nesting(같은 트리이므로 1:1)
    g2d = {}
    for i in range(n):
        g2d.setdefault(int(labels_g[i]), set()).add(int(labels_d[i]))
    g2d = {g: (next(iter(s)) if len(s) == 1 else Counter(
        int(labels_d[i]) for i in range(n) if labels_g[i] == g).most_common(1)[0][0])
        for g, s in g2d.items()}

    cents_g = _cluster_centroids(labels_g, iwa_emb)
    cents_d = _cluster_centroids(labels_d, iwa_emb)

    # 도메인 메타 + 명명배치(소속 GWA가 아니라 대표 IWA로)
    dom_members = defaultdict(list)
    for i in range(n):
        dom_members[int(labels_d[i])].append(i)
    domains, dom_batch, dom_id_map = [], [], {}
    for j, (d, rows) in enumerate(sorted(dom_members.items(),
                                         key=lambda kv: -len(kv[1])), 1):
        did = f"D_{j}"
        dom_id_map[d] = did
        ranked = sorted(rows, key=lambda i: -float(iwa_emb[i] @ cents_d[d]))
        reps = [meta[iwa_ids[i]]["label"] for i in ranked[:N_REP_IWA]]
        gid, glbl, gdom, cos = _nearest_onet(cents_d[d], gwa_emb, gwa_order, trans)
        domains.append({"domain_id": did, "n_iwa": len(rows),
                        "nearest_onet_domain": gdom, "nearest_onet_label": glbl,
                        "nearest_cosine": round(cos, 4), "rep_iwa_labels": reps})
        dom_batch.append({"domain_id": did, "n_iwa": len(rows),
                          "member_iwa_labels": reps})

    # GWA 메타 + 명명배치
    g_members = defaultdict(list)
    for i in range(n):
        g_members[int(labels_g[i])].append(i)
    gwas, gwa_batch, gid_map = [], [], {}
    for j, (g, rows) in enumerate(sorted(g_members.items(),
                                         key=lambda kv: -len(kv[1])), 1):
        kid = f"KG_{j:02d}"
        gid_map[g] = kid
        ranked = sorted(rows, key=lambda i: -float(iwa_emb[i] @ cents_g[g]))
        reps = [meta[iwa_ids[i]]["label"] for i in ranked[:N_REP_IWA]]
        on_id, on_lbl, on_dom, cos = _nearest_onet(cents_g[g], gwa_emb, gwa_order, trans)
        coh = float((iwa_emb[rows] @ cents_g[g]).mean())
        gwas.append({
            "kr_gwa_id": kid, "domain_id": dom_id_map[g2d[g]],
            "n_iwa": len(rows), "cohesion": round(coh, 4),
            "member_iwa_ids": [iwa_ids[i] for i in rows],
            "nearest_onet": on_id, "nearest_onet_label": on_lbl,
            "nearest_onet_domain": on_dom, "nearest_cosine": round(cos, 4),
            "rep_iwa_labels": reps})
        gwa_batch.append({"kr_gwa_id": kid, "n_iwa": len(rows),
                          "domain_id": dom_id_map[g2d[g]],
                          "member_iwa_labels": reps})

    CACHE.mkdir(parents=True, exist_ok=True)
    S4B_CLUSTERS.write_text(json.dumps(
        {"k": k, "k_eff": k_eff, "domains": domains, "gwas": gwas},
        ensure_ascii=False, indent=2), encoding="utf-8")
    sys_g = (PROMPTS / "gwa_bottomup_system.md").read_text(encoding="utf-8")
    S4B_GWA_BATCH.write_text(json.dumps(
        {"system": sys_g, "items": gwa_batch}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    sys_d = (PROMPTS / "gwa_domain_system.md").read_text(encoding="utf-8")
    S4B_DOMAIN_BATCH.write_text(json.dumps(
        {"system": sys_d, "items": dom_batch}, ensure_ascii=False, indent=2),
        encoding="utf-8")

    # ONET 정합 요약
    matched = {x["nearest_onet"] for x in gwas}
    matched_strong = {x["nearest_onet"] for x in gwas if x["nearest_cosine"] >= 0.55}
    coss = [x["nearest_cosine"] for x in gwas]
    sizes = [x["n_iwa"] for x in gwas]
    dom_match = sum(1 for x in gwas
                    if x["nearest_onet_domain"] == next(
                        d["nearest_onet_domain"] for d in domains
                        if d["domain_id"] == x["domain_id"]))
    summary = {
        "k_requested": k, "k_effective": k_eff, "n_iwa": n,
        "iwa_per_gwa": round(n / k_eff, 2), "onet_ratio_ref": ONET_RATIO,
        "max_cluster": max(sizes), "max_cluster_pct": round(max(sizes) / n * 100, 1),
        "min_cluster": min(sizes), "singletons": sum(1 for s in sizes if s == 1),
        "onet_distinct_matched": len(matched),
        "onet_distinct_matched_strong(cos>=.55)": len(matched_strong),
        "onet_coverage_41": round(len(matched) / 41, 3),
        "mean_nearest_cosine": round(float(np.mean(coss)), 4),
        "domain_self_consistency": round(dom_match / k_eff, 3),
    }
    S4B_SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2),
                           encoding="utf-8")
    print(f"[cluster] 도메인 {len(domains)} · KR-GWA {k_eff}개(요청 k={k}) · "
          f"IWA/GWA {summary['iwa_per_gwa']} (ONET {ONET_RATIO})")
    print(f"  균형: 최대군집 {summary['max_cluster']}({summary['max_cluster_pct']}%) · "
          f"최소 {summary['min_cluster']} · 단일 {summary['singletons']}")
    print(f"  ONET 정합: 매칭 {len(matched)}/41 (강매칭 {len(matched_strong)}) · "
          f"평균 최근접 cos {summary['mean_nearest_cosine']} · "
          f"도메인 자기정합 {summary['domain_self_consistency']}")
    print(f"  ▶ 명명: Opus가 {S4B_DOMAIN_BATCH.name}(도메인4) + {S4B_GWA_BATCH.name}(GWA{k_eff}) "
          f"→ s4b_domain_result.json · s4b_gwa_result.json")
    return summary


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["diagnose", "cluster"])
    ap.add_argument("--k", type=int, default=22)
    a = ap.parse_args()
    if a.cmd == "diagnose":
        diagnose()
    else:
        run_cluster(a.k)
