"""Stage 2 — DWA 군집(결정론적·무LLM 부분).

설계: stages/Stage2_DWA_도출_설계.md §④·⑥·⑧.
흐름:
    embed     전수 TASK full_statement → bge-m3 임베딩 → cache/embeddings.npy (재사용: S3/S4)
    cluster   응집트리(평균연결·코사인) → ONET밴드 자연절단 → 채택임계(한국형 3/2)
              → Multiple Linkage(≤3, τ 캘리브레이션 avg~1.3) → DWA 메타 + task_to_dwa
              → 명명요청 cache/s2_requests/{dwa_id}.json (대표 TASK 5건)
    diagnose  절단 곡선만 출력(명명 전 점검)

DWA id 규약: D_{idx:04d}. 명명은 Opus 서브에이전트가 cache/s2_results/{dwa_id}.json 에 기록.
이후 s2_persist 가 검증·DB적재. PYTHONUTF8=1 권장.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import numpy as np

TEST1_DIR = Path(__file__).resolve().parents[1]
CACHE = TEST1_DIR / "cache"
EMB_PATH = CACHE / "embeddings.npy"
EMB_IDS = CACHE / "embedding_ids.json"
LINK_PATH = CACHE / "linkage.npy"
CLUSTERS_JSON = CACHE / "s2_clusters.json"      # 채택 DWA 메타(명명 입력)
LINKS_JSON = CACHE / "s2_links.json"            # task_to_dwa (Multiple Linkage)
REQ_DIR = CACHE / "s2_requests"
RES_DIR = CACHE / "s2_results"

# ── 설계 상수 ────────────────────────────────────────────────────────
ONET_BAND_LO_DIV = 12      # band = [N/12, N/6]  (TASK:DWA ≈ 9:1 broad)
ONET_BAND_HI_DIV = 6
ADOPT_MIN_TASK = 3         # 한국형 3/2: size>=3 OR n_jobs>=2 → 채택
ADOPT_MIN_JOBS = 2
MAX_LINKS = 3              # Multiple Linkage 상한(ONET 준거)
TARGET_AVG_LINKS = 1.3    # ONET 실측 1.26
COHESION_GATE = 0.70      # §⑦ 군집 응집도(평균 코사인) 기준
N_REP = 5                 # 명명용 대표 TASK 수


# ── 데이터 로드 ──────────────────────────────────────────────────────
def load_tasks(con) -> list[dict]:
    rows = con.execute(
        "SELECT task_id, ksco_code, full_statement FROM task "
        "WHERE full_statement IS NOT NULL AND full_statement<>'' "
        "ORDER BY task_id").fetchall()
    return [{"task_id": r[0], "ksco_code": r[1], "full_statement": r[2]} for r in rows]


# ── 임베딩(캐시) ─────────────────────────────────────────────────────
def build_embeddings(force: bool = False) -> tuple[np.ndarray, list[str]]:
    """전수 TASK 임베딩 → L2정규화 → cache. 재실행 시 캐시 로드."""
    from pipeline import db
    con = db.get_con(read_only=True)
    tasks = load_tasks(con)
    con.close()
    ids = [t["task_id"] for t in tasks]

    if EMB_PATH.exists() and EMB_IDS.exists() and not force:
        cached_ids = json.loads(EMB_IDS.read_text(encoding="utf-8"))
        if cached_ids == ids:
            emb = np.load(EMB_PATH)
            print(f"[embed] 캐시 사용: {emb.shape}")
            return emb, ids
        print("[embed] 캐시 불일치 → 재생성")

    from pipeline.dedup import bge_m3_embed
    texts = [t["full_statement"] for t in tasks]
    print(f"[embed] {len(texts)}건 bge-m3 인코딩 시작…")
    emb = np.asarray(bge_m3_embed(texts), dtype="float32")
    # L2 정규화(코사인 = 내적)
    norm = np.linalg.norm(emb, axis=1, keepdims=True)
    norm[norm == 0] = 1.0
    emb = emb / norm
    CACHE.mkdir(parents=True, exist_ok=True)
    np.save(EMB_PATH, emb)
    EMB_IDS.write_text(json.dumps(ids, ensure_ascii=False), encoding="utf-8")
    print(f"[embed] 저장: {emb.shape} → {EMB_PATH.relative_to(TEST1_DIR)}")
    return emb, ids


# ── 응집트리(캐시) ───────────────────────────────────────────────────
def build_linkage(emb: np.ndarray, force: bool = False) -> np.ndarray:
    """평균연결·코사인 단일 응집트리. condensed 거리행렬 직접(설계 §⑧-1)."""
    from scipy.cluster.hierarchy import linkage
    from scipy.spatial.distance import pdist

    if LINK_PATH.exists() and not force:
        Z = np.load(LINK_PATH)
        if Z.shape[0] == emb.shape[0] - 1:
            print(f"[linkage] 캐시 사용: {Z.shape}")
            return Z
        print("[linkage] 캐시 크기 불일치 → 재생성")

    n = emb.shape[0]
    print(f"[linkage] pdist(cosine) {n}×{n} → condensed {n*(n-1)//2:,}쌍 …")
    d = pdist(emb, metric="cosine")            # float64 condensed (~1GB @16k)
    print(f"[linkage] average linkage 계산 중…")
    Z = linkage(d, method="average")
    del d
    np.save(LINK_PATH, Z)
    print(f"[linkage] 저장: {Z.shape} → {LINK_PATH.relative_to(TEST1_DIR)}")
    return Z


# ── 절단점 선택(자연 plateau ∩ ONET band) ────────────────────────────
def natural_cut_in_band(Z: np.ndarray, n: int) -> tuple[int, list[dict]]:
    """band=[N/12,N/6] 안에서 병합높이 gap 최대(가장 자연스러운) k 선택.

    k 클러스터 형성 절단높이 = heights[n-1-k], gap = heights[n-k]-heights[n-1-k].
    """
    heights = Z[:, 2]                      # 오름차순, 길이 n-1
    lo = max(2, n // ONET_BAND_HI_DIV * 0 + n // ONET_BAND_LO_DIV)  # N/12
    hi = n // ONET_BAND_HI_DIV                                       # N/6
    lo, hi = min(lo, hi), max(lo, hi)
    best_k, best_gap = None, -1.0
    curve = []
    for k in range(lo, hi + 1):
        i = n - 1 - k                     # heights index, 이 병합 직후 k 클러스터
        if i < 0 or i + 1 > len(heights) - 1:
            continue
        cut_h = float(heights[i])
        gap = float(heights[i + 1] - heights[i])
        curve.append({"k": k, "cut_height": round(cut_h, 5), "gap": round(gap, 6)})
        if gap > best_gap:
            best_gap, best_k = gap, k
    if best_k is None:                    # band 비었으면 중앙
        best_k = (lo + hi) // 2
    return best_k, curve


# ── 군집 응집도 ──────────────────────────────────────────────────────
def cluster_cohesion(emb: np.ndarray, member_idx: list[int]) -> tuple[np.ndarray, float]:
    """centroid(정규화) + 평균 멤버-centroid 코사인(응집도)."""
    sub = emb[member_idx]
    c = sub.mean(axis=0)
    cn = np.linalg.norm(c)
    if cn == 0:
        cn = 1.0
    c = c / cn
    cos = sub @ c
    return c, float(cos.mean())


# ── Multiple Linkage τ 캘리브레이션 ──────────────────────────────────
def calibrate_tau(sim_to_centroids: np.ndarray, primary_idx: np.ndarray,
                  target: float = TARGET_AVG_LINKS) -> float:
    """avg links/task ≈ target 되도록 보조연결 코사인 임계 τ 탐색.

    sim_to_centroids: (n_task, n_dwa) 각 task→채택DWA centroid 코사인.
    primary_idx: 각 task의 1차 DWA 인덱스(항상 1 연결).
    보조연결 후보 = primary 제외 centroid 중 cos>=τ, task당 최대 MAX_LINKS-1.
    """
    n = sim_to_centroids.shape[0]
    s = sim_to_centroids.copy()
    s[np.arange(n), primary_idx] = -1.0     # 1차 제외
    # τ 후보를 분위수로 스윕
    best_tau, best_diff = 0.9, 1e9
    for tau in np.linspace(0.95, 0.55, 41):
        over = s >= tau
        extra = np.minimum(over.sum(axis=1), MAX_LINKS - 1)
        avg = 1.0 + extra.mean()
        diff = abs(avg - target)
        if diff < best_diff:
            best_diff, best_tau = diff, float(tau)
        if avg >= target:                   # 충분히 올라가면 그 부근이 최적
            best_tau = float(tau)
            best_diff = diff
            break
    return round(best_tau, 4)


# ── 메인: cluster ────────────────────────────────────────────────────
def run_cluster(force_emb: bool = False, force_link: bool = False,
                k_override: int | None = None) -> dict:
    from scipy.cluster.hierarchy import fcluster
    from pipeline import db

    emb, ids = build_embeddings(force=force_emb)
    Z = build_linkage(emb, force=force_link)
    n = emb.shape[0]

    con = db.get_con(read_only=True)
    tasks = load_tasks(con)
    con.close()
    assert [t["task_id"] for t in tasks] == ids, "task 순서/임베딩 id 불일치"
    job_of = np.array([t["ksco_code"] for t in tasks])

    # 1) 절단점
    k, curve = natural_cut_in_band(Z, n)
    if k_override:
        k = k_override
    labels = fcluster(Z, t=k, criterion="maxclust")    # 1..k
    print(f"[cut] k={k} (band {n//ONET_BAND_LO_DIV}~{n//ONET_BAND_HI_DIV}) → 실제 군집 {labels.max()}개")

    # 2) 군집별 멤버 + 채택임계(한국형 3/2)
    from collections import defaultdict
    members = defaultdict(list)
    for i, lab in enumerate(labels):
        members[int(lab)].append(i)

    adopted = []        # [{dwa_id, member_idx, n_jobs, mean_cosine, centroid}]
    rejected_idx = []   # 미채택 군집의 task 인덱스(→ 최근접 채택DWA로 1차 연결)
    for lab, idx in sorted(members.items()):
        njobs = len(set(job_of[idx]))
        if len(idx) >= ADOPT_MIN_TASK or njobs >= ADOPT_MIN_JOBS:
            c, coh = cluster_cohesion(emb, idx)
            adopted.append({"raw_label": lab, "member_idx": idx,
                            "n_jobs": njobs, "mean_cosine": coh, "centroid": c})
        else:
            rejected_idx.extend(idx)
    # dwa_id 부여(크기 내림차순 안정 정렬)
    adopted.sort(key=lambda d: (-len(d["member_idx"]), d["raw_label"]))
    for j, d in enumerate(adopted, 1):
        d["dwa_id"] = f"D_{j:04d}"
    print(f"[adopt] 채택 DWA {len(adopted)} · 미채택군집 task {len(rejected_idx)} "
          f"(최근접 채택DWA로 재배정)")

    centroids = np.vstack([d["centroid"] for d in adopted])        # (n_dwa, dim)
    n_dwa = centroids.shape[0]

    # 3) 각 task → 채택 DWA centroid 코사인 (블록 처리: 메모리 절약)
    primary = np.empty(n, dtype=np.int32)
    # 1차 = 자기 군집(채택)이면 그 dwa, 아니면 최근접 centroid
    raw_to_dwa = {d["raw_label"]: di for di, d in enumerate(adopted)}
    sim = np.empty((n, n_dwa), dtype="float32")
    BLK = 2000
    for s0 in range(0, n, BLK):
        s1 = min(s0 + BLK, n)
        sim[s0:s1] = emb[s0:s1] @ centroids.T
    for i in range(n):
        own = raw_to_dwa.get(int(labels[i]))
        primary[i] = own if own is not None else int(sim[i].argmax())

    # 4) Multiple Linkage τ 캘리브레이션 + 보조연결
    tau = calibrate_tau(sim, primary)
    s_aux = sim.copy()
    s_aux[np.arange(n), primary] = -1.0
    links = []          # {task_id, dwa_id, link_order}
    extra_counts = []
    for i in range(n):
        links.append({"task_id": ids[i], "dwa_id": adopted[primary[i]]["dwa_id"],
                      "link_order": 1, "cosine": round(float(sim[i, primary[i]]), 4)})
        cand = np.where(s_aux[i] >= tau)[0]
        if len(cand):
            cand = cand[np.argsort(-s_aux[i, cand])][:MAX_LINKS - 1]
        extra_counts.append(len(cand))
        for o, di in enumerate(cand, start=2):
            links.append({"task_id": ids[i], "dwa_id": adopted[di]["dwa_id"],
                          "link_order": o, "cosine": round(float(sim[i, di]), 4)})
    avg_links = 1.0 + (np.mean(extra_counts) if extra_counts else 0.0)
    print(f"[mlink] τ={tau} → 평균 연결 {avg_links:.3f}/task (목표 {TARGET_AVG_LINKS}, ONET 1.26)")

    # 5) DWA 메타 집계 + 대표 TASK(centroid 최근접 N_REP)
    by_dwa_members = defaultdict(list)        # dwa_id → primary task idx
    for i in range(n):
        by_dwa_members[adopted[primary[i]]["dwa_id"]].append(i)
    clusters_out = []
    stmt = [t["full_statement"] for t in tasks]
    cohesions = []
    for di, d in enumerate(adopted):
        prim_members = by_dwa_members.get(d["dwa_id"], [])
        # 대표: 1차 멤버 중 centroid 코사인 상위 — 단, 동일 문장은 1회만(고유 신호 확보)
        pool = prim_members if prim_members else d["member_idx"]
        order = sorted(pool, key=lambda i: -float(sim[i, di]))
        rep, seen_txt = [], set()
        for i in order:
            key = " ".join(stmt[i].split())
            if key in seen_txt:
                continue
            seen_txt.add(key)
            rep.append(i)
            if len(rep) >= N_REP:
                break
        njobs_prim = len(set(job_of[prim_members])) if prim_members else d["n_jobs"]
        cohesions.append(d["mean_cosine"])
        clusters_out.append({
            "dwa_id": d["dwa_id"],
            "cluster_size": len(prim_members),       # 1차연결 기준 크기
            "tree_size": len(d["member_idx"]),       # 트리 군집 원크기
            "n_jobs": int(njobs_prim),
            "mean_cosine": round(float(d["mean_cosine"]), 4),
            "cohesion_ok": bool(d["mean_cosine"] >= COHESION_GATE),
            "n_unique_stmt": len(set(" ".join(stmt[i].split()) for i in pool)),
            "rep_task_ids": [ids[i] for i in rep],
            "rep_statements": [stmt[i] for i in rep],
            "rep_jobs": [job_of[i] for i in rep],
        })

    # cross-family(다른 대분류 묶임) 플래그
    major_of = {t["task_id"]: t["ksco_code"][0] for t in tasks}
    for c in clusters_out:
        members_tids = [l["task_id"] for l in links
                        if l["dwa_id"] == c["dwa_id"] and l["link_order"] == 1]
        majors = set(major_of[tid] for tid in members_tids)
        c["is_cross_family"] = len(majors) >= 2

    # 6) 저장(명명 입력) + 요청 파일
    CACHE.mkdir(parents=True, exist_ok=True)
    CLUSTERS_JSON.write_text(json.dumps(clusters_out, ensure_ascii=False, indent=2),
                             encoding="utf-8")
    LINKS_JSON.write_text(json.dumps(links, ensure_ascii=False), encoding="utf-8")
    _write_requests(clusters_out)

    coh_arr = np.array(cohesions)
    summary = {
        "n_task": n, "k_cut": int(k), "n_dwa": len(adopted),
        "band": [n // ONET_BAND_LO_DIV, n // ONET_BAND_HI_DIV],
        "tau": tau, "avg_links": round(float(avg_links), 3),
        "cohesion_median": round(float(np.median(coh_arr)), 4),
        "cohesion_ge_070": int((coh_arr >= COHESION_GATE).sum()),
        "cross_family": sum(1 for c in clusters_out if c["is_cross_family"]),
        "cross_family_pct": round(
            sum(1 for c in clusters_out if c["is_cross_family"]) / len(clusters_out), 4),
        "ratio_task_per_dwa": round(n / len(adopted), 2),
        "cut_curve_head": curve[:5],
    }
    (CACHE / "s2_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n── Stage2 군집 요약 ──")
    for kx, vx in summary.items():
        if kx != "cut_curve_head":
            print(f"  {kx}: {vx}")
    print(f"  명명요청 {len(clusters_out)}건 → {REQ_DIR.relative_to(TEST1_DIR)}")
    return summary


def _write_requests(clusters: list[dict]) -> None:
    """DWA별 Opus 명명 요청 JSON 생성(system + 대표 TASK 5건)."""
    REQ_DIR.mkdir(parents=True, exist_ok=True)
    system = (TEST1_DIR / "prompts" / "dwa_write_system.md").read_text(encoding="utf-8")
    for c in clusters:
        reps = "\n".join(f"  {i}. {s}" for i, s in enumerate(c["rep_statements"], 1))
        user = (
            f"[DWA 군집 정보]\n"
            f"- dwa_id: {c['dwa_id']}\n"
            f"- 군집 크기(소속 TASK): {c['cluster_size']} (고유 진술문 {c['n_unique_stmt']}종)\n"
            f"- 소속 직업 수: {c['n_jobs']}\n"
            f"- 군집 응집도(평균 코사인): {c['mean_cosine']}\n\n"
            f"[대표 TASK 진술문 {len(c['rep_statements'])}건 — 중심 근접순·중복제거]\n{reps}\n\n"
            f"위 TASK들을 포괄하는 한 단계 위 작업활동(DWA)의 label과 definition을 "
            f"8조항에 맞춰 작성하고, 반드시 dwa_id=\"{c['dwa_id']}\"로 JSON만 출력하라."
        )
        (REQ_DIR / f"{c['dwa_id']}.json").write_text(
            json.dumps({"dwa_id": c["dwa_id"], "system": system, "user": user},
                       ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["embed", "cluster", "diagnose"])
    ap.add_argument("--force-emb", action="store_true")
    ap.add_argument("--force-link", action="store_true")
    ap.add_argument("--k", type=int, default=None, help="절단 k 강제(시범/대조)")
    a = ap.parse_args()
    if a.cmd == "embed":
        build_embeddings(force=a.force_emb)
    elif a.cmd == "cluster":
        run_cluster(force_emb=a.force_emb, force_link=a.force_link, k_override=a.k)
    elif a.cmd == "diagnose":
        emb, _ = build_embeddings(force=a.force_emb)
        Z = build_linkage(emb, force=a.force_link)
        k, curve = natural_cut_in_band(Z, emb.shape[0])
        print(f"[diagnose] 권장 절단 k={k}")
        print("  k, cut_height, gap (상위 gap 15):")
        for r in sorted(curve, key=lambda x: -x["gap"])[:15]:
            print(f"    k={r['k']:5d}  h={r['cut_height']:.4f}  gap={r['gap']:.5f}")
