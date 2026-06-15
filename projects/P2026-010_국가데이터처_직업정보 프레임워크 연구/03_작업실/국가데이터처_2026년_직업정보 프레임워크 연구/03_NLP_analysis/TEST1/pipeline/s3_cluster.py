"""Stage 3 — IWA 군집(결정론적·무LLM 부분).

설계: stages/Stage3_IWA_도출_설계.md §④·⑥·⑦ · 방법 A(같은 트리 상위 절단).
흐름:
    cluster   캐시 Z(S2와 동일 응집트리) → IWA밴드(DWA÷8~5) 자연절단 → labels_iwa
              → DWA→IWA 매핑(각 DWA의 1차 TASK 다수결, 만장일치율=strict-nesting 지표)
              → IWA 메타(n_dwa·n_task·n_jobs·cohesion) + dwa_to_iwa
              → 명명배치 cache/s3_batch_inputs/b{NN}.json (소속 DWA 라벨)
    diagnose  IWA 절단 곡선만 출력(절단점 확정용)

IWA id 규약: I_{idx:04d}. 명명은 Opus 서브에이전트가 cache/s3_results/b{NN}.json 에 기록.
이후 s3_persist 가 검증·DB적재. PYTHONUTF8=1 권장.
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
LINKS_JSON = CACHE / "s2_links.json"            # task_to_dwa (S2 결과)
EMB_IDS = CACHE / "embedding_ids.json"

S3_CLUSTERS_JSON = CACHE / "s3_clusters.json"   # IWA 메타(명명 입력)
S3_MAP_JSON = CACHE / "s3_dwa_to_iwa.json"      # dwa_id → iwa_id
S3_BATCHES = CACHE / "s3_batches.json"
S3_BATCH_DIR = CACHE / "s3_batch_inputs"
S3_RES_DIR = CACHE / "s3_results"
S3_SUMMARY = CACHE / "s3_summary.json"

# ── 설계 상수 ────────────────────────────────────────────────────────
IWA_BAND_LO_DIV = 8        # band_k = [n_dwa/8, n_dwa/5] (ONET DWA:IWA≈6.3:1)
IWA_BAND_HI_DIV = 5
COHESION_REPORT = 0.55     # 참고치(게이트 아님, 설계 §⑦)
N_REP_DWA = 8              # 명명용 대표 DWA 라벨 수
BATCH_SIZE = 30            # 명명 배치 크기(S2와 동일)


# ── 공용 로더(S2 캐시 재사용) ────────────────────────────────────────
def _load_emb_and_link():
    """S2가 만든 embeddings.npy / linkage.npy / embedding_ids.json 로드(재계산 없음)."""
    from pipeline.s2_cluster import EMB_PATH, LINK_PATH
    if not (EMB_PATH.exists() and LINK_PATH.exists() and EMB_IDS.exists()):
        raise SystemExit("S2 캐시(embeddings/linkage/ids) 없음 — Stage 2 먼저 실행 필요")
    emb = np.load(EMB_PATH)
    Z = np.load(LINK_PATH)
    ids = json.loads(EMB_IDS.read_text(encoding="utf-8"))
    assert emb.shape[0] == len(ids) == Z.shape[0] + 1, "캐시 크기 불일치"
    return emb, Z, ids


def _load_dwa_from_db() -> dict[str, dict]:
    """DB dwa 테이블: dwa_id → {label, definition, cluster_size, n_jobs, mean_cosine}."""
    from pipeline import db
    con = db.get_con(read_only=True)
    rows = con.execute(
        "SELECT dwa_id,label,definition,cluster_size,n_jobs,mean_cosine FROM dwa"
    ).fetchall()
    con.close()
    return {r[0]: {"dwa_id": r[0], "label": r[1], "definition": r[2],
                   "cluster_size": r[3], "n_jobs": r[4], "mean_cosine": r[5]}
            for r in rows}


def _job_of(ids: list[str]) -> dict[str, str]:
    from pipeline import db
    con = db.get_con(read_only=True)
    rows = con.execute("SELECT task_id, ksco_code FROM task").fetchall()
    con.close()
    return {r[0]: r[1] for r in rows}


# ── 자연절단(IWA 밴드 = DWA÷8~5, k on TASK tree) ─────────────────────
def natural_cut_iwa(Z: np.ndarray, n: int, n_dwa: int,
                    k_override: int | None = None) -> tuple[int, list[dict]]:
    heights = Z[:, 2]
    lo = max(2, n_dwa // IWA_BAND_LO_DIV)
    hi = max(lo, n_dwa // IWA_BAND_HI_DIV)
    best_k, best_gap, curve = None, -1.0, []
    for k in range(lo, hi + 1):
        i = n - 1 - k
        if i < 0 or i + 1 > len(heights) - 1:
            continue
        cut_h = float(heights[i])
        gap = float(heights[i + 1] - heights[i])
        curve.append({"k": k, "cut_height": round(cut_h, 5), "gap": round(gap, 6)})
        if gap > best_gap:
            best_gap, best_k = gap, k
    if best_k is None:
        best_k = (lo + hi) // 2
    return (k_override or best_k), curve


# ── DWA 대표벡터(1차 TASK 평균, 정규화) ──────────────────────────────
def _dwa_centroids(emb, idx_of, primary_tasks_of):
    cents, order = {}, []
    for dwa_id, tids in primary_tasks_of.items():
        rows = [idx_of[t] for t in tids if t in idx_of]
        if not rows:
            continue
        c = emb[rows].mean(axis=0)
        nrm = np.linalg.norm(c) or 1.0
        cents[dwa_id] = c / nrm
        order.append(dwa_id)
    return cents, order


def run_cluster(k_override: int | None = None) -> dict:
    from scipy.cluster.hierarchy import fcluster

    emb, Z, ids = _load_emb_and_link()
    n = len(ids)
    idx_of = {t: i for i, t in enumerate(ids)}
    dwa = _load_dwa_from_db()
    n_dwa = len(dwa)

    # 1차 링크(link_order=1) task → dwa
    links = json.loads(LINKS_JSON.read_text(encoding="utf-8"))
    primary_tasks_of: dict[str, list[str]] = defaultdict(list)
    for l in links:
        if l.get("link_order") == 1 and l["dwa_id"] in dwa:
            primary_tasks_of[l["dwa_id"]].append(l["task_id"])

    job_of = _job_of(ids)

    # 1) IWA 절단 + S2 DWA 절단(트리 노드 정의용) — 같은 트리(방법 A)
    k_iwa, curve = natural_cut_iwa(Z, n, n_dwa, k_override)
    labels_iwa = fcluster(Z, t=k_iwa, criterion="maxclust")   # 1..k_iwa (task별)
    k_dwa_s2 = json.loads((CACHE / "s2_summary.json").read_text(encoding="utf-8"))["k_cut"]
    labels_dwa_raw = fcluster(Z, t=k_dwa_s2, criterion="maxclust")  # S2 raw 트리노드
    print(f"[cut] IWA k={k_iwa} (band {n_dwa//IWA_BAND_LO_DIV}~{n_dwa//IWA_BAND_HI_DIV}) "
          f"→ 트리군집 {labels_iwa.max()}개 · S2 raw k={k_dwa_s2}")

    # raw 트리노드 → IWA 조상(같은 트리·finer cut이므로 1:1 nesting, 수학 보장)
    raw2iwa: dict[int, int] = {}
    _tmp: dict[int, set] = defaultdict(set)
    for i in range(n):
        _tmp[int(labels_dwa_raw[i])].add(int(labels_iwa[i]))
    impure = 0
    for r, s in _tmp.items():
        raw2iwa[r] = next(iter(s)) if len(s) == 1 else Counter(
            int(labels_iwa[i]) for i in range(n) if labels_dwa_raw[i] == r).most_common(1)[0][0]
        if len(s) > 1:
            impure += 1
    if impure:
        print(f"[nest][warn] raw→IWA 비순수 {impure}건(이론상 0, 동률절단 영향)")

    # 2) DWA→IWA(방법 A): 각 DWA의 지배적 raw 트리노드 → 그 IWA 조상(strict)
    #    + 트리순도(purity)=1차 TASK 중 같은 IWA 조상에 떨어지는 비율(품질 지표)
    dwa_to_rawiwa: dict[str, int] = {}
    fully_nested = 0          # purity==1.0 (완전 트리 nesting)
    purities, split_report = [], []
    for dwa_id, tids in primary_tasks_of.items():
        raws = [int(labels_dwa_raw[idx_of[t]]) for t in tids if t in idx_of]
        if not raws:
            continue
        dom_raw, _ = Counter(raws).most_common(1)[0]
        iwa_raw = raw2iwa[dom_raw]
        dwa_to_rawiwa[dwa_id] = iwa_raw
        same = sum(1 for r in raws if raw2iwa[r] == iwa_raw)
        pur = same / len(raws)
        purities.append(pur)
        if pur >= 0.999:
            fully_nested += 1
        else:
            split_report.append({"dwa_id": dwa_id, "n_task": len(raws),
                                  "purity": round(pur, 3)})
    n_mapped = len(dwa_to_rawiwa)
    uni_rate = fully_nested / n_mapped if n_mapped else 0.0
    mean_pur = float(np.mean(purities)) if purities else 0.0
    print(f"[nest] DWA→IWA(방법A·트리노드) {n_mapped}/{n_dwa} · "
          f"완전nesting {fully_nested} ({uni_rate:.1%}) · 평균순도 {mean_pur:.3f} · "
          f"부분분할 {len(split_report)}")
    unanimous = fully_nested

    # 3) IWA 재번호(DWA 보유 군집만, 소속 DWA수 내림차순) → I_0001..
    raw_members: dict[int, list[str]] = defaultdict(list)
    for dwa_id, raw in dwa_to_rawiwa.items():
        raw_members[raw].append(dwa_id)
    raw_sorted = sorted(raw_members.items(), key=lambda kv: (-len(kv[1]), kv[0]))

    # DWA centroid(대표 선정·cohesion용)
    cents, _ = _dwa_centroids(emb, idx_of, primary_tasks_of)

    iwa_clusters, dwa_to_iwa = [], {}
    for j, (raw, members) in enumerate(raw_sorted, 1):
        iwa_id = f"I_{j:04d}"
        for d in members:
            dwa_to_iwa[d] = iwa_id
        # IWA centroid = 소속 DWA centroid 평균(정규화)
        mvec = np.vstack([cents[d] for d in members if d in cents])
        ic = mvec.mean(axis=0)
        ic = ic / (np.linalg.norm(ic) or 1.0)
        coss = mvec @ ic
        mean_cos = float(coss.mean())
        # 대표 DWA(centroid 근접순) 라벨
        ranked = sorted([d for d in members if d in cents],
                        key=lambda d: -float(cents[d] @ ic))
        rep = ranked[:N_REP_DWA] if ranked else members[:N_REP_DWA]
        # n_task·n_jobs(소속 DWA의 1차 TASK 합/직업)
        member_tids = [t for d in members for t in primary_tasks_of.get(d, [])]
        n_task = len(member_tids)
        n_jobs = len(set(job_of.get(t, "") for t in member_tids) - {""})
        iwa_clusters.append({
            "iwa_id": iwa_id,
            "n_dwa": len(members),
            "n_task": n_task,
            "n_jobs": n_jobs,
            "mean_cosine": round(mean_cos, 4),
            "cohesion_ok": bool(mean_cos >= COHESION_REPORT),
            "member_dwa_ids": members,
            "rep_dwa_ids": rep,
            "rep_dwa_labels": [dwa[d]["label"] for d in rep],
        })

    n_iwa = len(iwa_clusters)
    print(f"[iwa] IWA {n_iwa}개 · DWA:IWA = {n_dwa/n_iwa:.2f}:1 (ONET 6.3:1)")

    # 4) 저장 + 명명배치
    CACHE.mkdir(parents=True, exist_ok=True)
    S3_CLUSTERS_JSON.write_text(json.dumps(iwa_clusters, ensure_ascii=False, indent=2),
                                encoding="utf-8")
    S3_MAP_JSON.write_text(json.dumps(dwa_to_iwa, ensure_ascii=False), encoding="utf-8")
    _write_batches(iwa_clusters)

    cohs = np.array([c["mean_cosine"] for c in iwa_clusters])
    summary = {
        "n_dwa": n_dwa, "k_iwa_cut": int(k_iwa), "n_iwa": n_iwa,
        "band_k": [n_dwa // IWA_BAND_LO_DIV, n_dwa // IWA_BAND_HI_DIV],
        "ratio_dwa_per_iwa": round(n_dwa / n_iwa, 2),
        "nesting_method": "A_tree_node",
        "nesting_fully_nested": unanimous, "nesting_fully_rate": round(uni_rate, 4),
        "nesting_mean_purity": round(mean_pur, 4),
        "nesting_split": len(split_report),
        "cohesion_median": round(float(np.median(cohs)), 4),
        "cohesion_ge_055": int((cohs >= COHESION_REPORT).sum()),
        "n_batches": (n_iwa + BATCH_SIZE - 1) // BATCH_SIZE,
        "cut_curve_head": curve[:5],
        "split_examples": split_report[:10],
    }
    S3_SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2),
                          encoding="utf-8")
    print("\n── Stage3 IWA 군집 요약 ──")
    for kx, vx in summary.items():
        if kx not in ("cut_curve_head", "split_examples"):
            print(f"  {kx}: {vx}")
    print(f"  명명배치 {summary['n_batches']}개 → {S3_BATCH_DIR.relative_to(TEST1_DIR)}")
    return summary


def _write_batches(clusters: list[dict]) -> None:
    """IWA 명명 배치 생성(소속 DWA 라벨 입력). b{NN}.json + s3_batches.json."""
    S3_BATCH_DIR.mkdir(parents=True, exist_ok=True)
    batches, batch_ids = [], []
    for s0 in range(0, len(clusters), BATCH_SIZE):
        chunk = clusters[s0:s0 + BATCH_SIZE]
        items = [{
            "iwa_id": c["iwa_id"],
            "n_dwa": c["n_dwa"], "n_task": c["n_task"], "n_jobs": c["n_jobs"],
            "mean_cosine": c["mean_cosine"],
            "member_dwa_labels": c["rep_dwa_labels"],
        } for c in chunk]
        bi = len(batches)
        (S3_BATCH_DIR / f"b{bi:02d}.json").write_text(
            json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
        batches.append([c["iwa_id"] for c in chunk])
        batch_ids.append(f"b{bi:02d}")
    S3_BATCHES.write_text(json.dumps(batches, ensure_ascii=False), encoding="utf-8")


def diagnose(k_override: int | None = None) -> None:
    emb, Z, ids = _load_emb_and_link()
    n = len(ids)
    dwa = _load_dwa_from_db()
    k, curve = natural_cut_iwa(Z, n, len(dwa), k_override)
    print(f"[diagnose] DWA={len(dwa)} · IWA band k=[{len(dwa)//IWA_BAND_LO_DIV},"
          f"{len(dwa)//IWA_BAND_HI_DIV}] · 권장 절단 k={k}")
    print("  상위 gap 15 (k, cut_height, gap):")
    for r in sorted(curve, key=lambda x: -x["gap"])[:15]:
        print(f"    k={r['k']:5d}  h={r['cut_height']:.4f}  gap={r['gap']:.6f}")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["cluster", "diagnose"])
    ap.add_argument("--k", type=int, default=None, help="IWA 절단 k 강제")
    a = ap.parse_args()
    if a.cmd == "cluster":
        run_cluster(k_override=a.k)
    else:
        diagnose(k_override=a.k)
