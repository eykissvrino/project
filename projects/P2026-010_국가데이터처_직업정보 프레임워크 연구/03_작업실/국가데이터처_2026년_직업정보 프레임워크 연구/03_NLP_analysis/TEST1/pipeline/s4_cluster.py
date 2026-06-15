"""Stage 4 — GWA 도출(결정론적·무LLM 부분).

설계: stages/Stage4_GWA_도출_설계.md §④·⑥·⑦ · 2트랙.
  트랙1(주) 하이브리드 = ONET 41 GWA 한국어 채택 → 각 IWA를 최근접 GWA에 매핑(임베딩+애매건 Opus).
  트랙2(탐색) 순수 상향식 = 같은 응집트리 최상위 절단 → 한국형 GWA 자생 → ONET 41 일치도 비교.

흐름(서브커맨드):
    prep       IWA 대표벡터 재구성(S2/S3 캐시) → cache/s4_iwa_centroids.npy
               + ONET 41 GWA 번역요청 cache/s4_translate_request.json (Opus가 번역 → s4_translation.json)
    map        (번역 후) ONET41 한국어 임베딩 → IWA 최근접 매핑 → cache/s4_iwa_to_gwa.json
               + 애매건 배치 cache/s4_ambiguous.json (Opus zero-shot 재판정) + gwa_emb 캐시
    bottomup   (트랙2) 같은 트리 최상위 절단(자연·k=41) → 한국형 GWA 군집 → ONET 비교
               + 명명배치 cache/s4_bottomup_batch.json (Opus 명명)
    diagnose   상향식 절단 곡선 출력

이후 s4_persist 가 검증·DB적재(gwa·iwa_to_gwa·gwa_bottomup). PYTHONUTF8=1 권장.
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
EMB_IDS = CACHE / "embedding_ids.json"
LINKS_JSON = CACHE / "s2_links.json"            # task_to_dwa (S2 결과)

# 산출 캐시
S4_IWA_CENT = CACHE / "s4_iwa_centroids.npy"     # IWA 대표벡터(178×1024)
S4_IWA_IDS = CACHE / "s4_iwa_ids.json"           # 행 순서 iwa_id
S4_TRANSLATE_REQ = CACHE / "s4_translate_request.json"
S4_TRANSLATION = CACHE / "s4_translation.json"   # Opus 번역결과(41)
S4_GWA_EMB = CACHE / "s4_gwa_emb.npy"            # ONET41 한국어 임베딩
S4_GWA_ORDER = CACHE / "s4_gwa_order.json"       # gwa_emb 행 순서(onet_gwa_id)
S4_MAP_JSON = CACHE / "s4_iwa_to_gwa.json"       # iwa_id → 임베딩 prior 매핑
S4_COS_LOOKUP = CACHE / "s4_iwa_gwa_cos.json"    # iwa_id → {gwa_id: cosine}(전 41)
S4_MAP_BATCH = CACHE / "s4_map_batch.json"       # 전수 IWA→GWA Opus 분류 배치
S4_MAP_RES = CACHE / "s4_map_result.json"        # Opus 분류 결과(있으면 적용)
S4_BOTTOMUP = CACHE / "s4_bottomup.json"         # 트랙2 군집 메타
S4_BU_BATCH = CACHE / "s4_bottomup_batch.json"   # 트랙2 명명 배치(Opus)
S4_BU_SUMMARY = CACHE / "s4_bottomup_summary.json"
S4_SUMMARY = CACHE / "s4_summary.json"

# ── 설계 상수 ────────────────────────────────────────────────────────
AMBIG_COS = 0.50        # top1 cosine 이 이 미만이면 애매(Opus 재판정)
AMBIG_MARGIN = 0.03     # top1-top2 격차가 이 미만이면 애매
KR_UNIQUE_COS = 0.55    # 최근접 cosine 이 이 미만이면 한국 특이활동 후보(보고)
N_REP_IWA = 10          # 상향식 명명용 대표 IWA 라벨 수
# ONET GWA 4대 영역(onet_gwa_id 접두)
DOMAIN_OF = {"4.A.1": "정보 입력", "4.A.2": "정신 과정",
             "4.A.3": "작업 산출", "4.A.4": "타인과의 상호작용"}


def _domain(onet_gwa_id: str) -> str:
    for pre, name in DOMAIN_OF.items():
        if onet_gwa_id.startswith(pre):
            return name
    return "기타"


# ── 공용 로더 ────────────────────────────────────────────────────────
def _load_emb_and_link():
    from pipeline.s2_cluster import EMB_PATH, LINK_PATH
    if not (EMB_PATH.exists() and LINK_PATH.exists() and EMB_IDS.exists()):
        raise SystemExit("S2 캐시(embeddings/linkage/ids) 없음 — Stage 2 먼저 실행 필요")
    emb = np.load(EMB_PATH)
    Z = np.load(LINK_PATH)
    ids = json.loads(EMB_IDS.read_text(encoding="utf-8"))
    assert emb.shape[0] == len(ids) == Z.shape[0] + 1, "캐시 크기 불일치"
    return emb, Z, ids


def _load_dwa_to_iwa() -> dict[str, str]:
    """DB dwa_to_iwa: dwa_id → iwa_id (strict 1:1)."""
    from pipeline import db
    con = db.get_con(read_only=True)
    rows = con.execute("SELECT dwa_id, iwa_id FROM dwa_to_iwa").fetchall()
    con.close()
    if not rows:
        raise SystemExit("dwa_to_iwa 비어있음 — Stage 3 먼저 완료 필요")
    return {r[0]: r[1] for r in rows}


def _load_iwa_meta() -> dict[str, dict]:
    from pipeline import db
    con = db.get_con(read_only=True)
    rows = con.execute(
        "SELECT iwa_id, label, definition, n_dwa, n_task, n_jobs FROM iwa").fetchall()
    con.close()
    return {r[0]: {"iwa_id": r[0], "label": r[1], "definition": r[2],
                   "n_dwa": r[3], "n_task": r[4], "n_jobs": r[5]} for r in rows}


def _load_onet_gwa() -> list[dict]:
    from pipeline import db
    con = db.get_con(read_only=True)
    rows = con.execute(
        "SELECT onet_gwa_id, label, description FROM external_ref.onet_gwa "
        "ORDER BY onet_gwa_id").fetchall()
    con.close()
    return [{"onet_gwa_id": r[0], "onet_label_en": r[1], "description_en": r[2],
             "domain": _domain(r[0])} for r in rows]


def _primary_tasks_of() -> dict[str, list[str]]:
    """s2_links.json 의 link_order==1 (각 DWA 1차 TASK)."""
    links = json.loads(LINKS_JSON.read_text(encoding="utf-8"))
    out: dict[str, list[str]] = defaultdict(list)
    for l in links:
        if l.get("link_order") == 1:
            out[l["dwa_id"]].append(l["task_id"])
    return out


# ── IWA 대표벡터 재구성(S3와 동일 산식: DWA centroid 평균) ─────────────
def _build_iwa_centroids(emb, ids) -> tuple[np.ndarray, list[str]]:
    idx_of = {t: i for i, t in enumerate(ids)}
    dwa_to_iwa = _load_dwa_to_iwa()
    primary = _primary_tasks_of()

    # DWA centroid = 1차 TASK 임베딩 평균(정규화)
    dwa_cent: dict[str, np.ndarray] = {}
    for dwa_id, tids in primary.items():
        rows = [idx_of[t] for t in tids if t in idx_of]
        if not rows:
            continue
        c = emb[rows].mean(axis=0)
        dwa_cent[dwa_id] = c / (np.linalg.norm(c) or 1.0)

    # IWA centroid = 소속 DWA centroid 평균(정규화)
    members: dict[str, list[str]] = defaultdict(list)
    for dwa_id, iwa_id in dwa_to_iwa.items():
        members[iwa_id].append(dwa_id)
    iwa_ids = sorted(members.keys())
    vecs = []
    for iwa_id in iwa_ids:
        mvec = np.vstack([dwa_cent[d] for d in members[iwa_id] if d in dwa_cent])
        ic = mvec.mean(axis=0)
        vecs.append(ic / (np.linalg.norm(ic) or 1.0))
    return np.vstack(vecs).astype("float32"), iwa_ids


def run_prep() -> dict:
    """IWA 대표벡터 재구성 + ONET 41 번역요청 생성."""
    emb, Z, ids = _load_emb_and_link()
    iwa_emb, iwa_ids = _build_iwa_centroids(emb, ids)
    CACHE.mkdir(parents=True, exist_ok=True)
    np.save(S4_IWA_CENT, iwa_emb)
    S4_IWA_IDS.write_text(json.dumps(iwa_ids, ensure_ascii=False), encoding="utf-8")

    onet = _load_onet_gwa()
    system = (PROMPTS / "gwa_translate_system.md").read_text(encoding="utf-8")
    S4_TRANSLATE_REQ.write_text(json.dumps(
        {"system": system, "items": onet}, ensure_ascii=False, indent=2),
        encoding="utf-8")

    dom_counts = Counter(o["domain"] for o in onet)
    print(f"[prep] IWA 대표벡터 {iwa_emb.shape} → {S4_IWA_CENT.relative_to(TEST1_DIR)}")
    print(f"[prep] ONET GWA {len(onet)}개 번역요청 → {S4_TRANSLATE_REQ.relative_to(TEST1_DIR)}")
    print(f"       영역분포: {dict(dom_counts)}")
    print(f"  ▶ 다음: Opus 서브에이전트가 system+items 로 번역 → {S4_TRANSLATION.name} "
          f"([{{onet_gwa_id,onet_label_en,label_kr,definition_kr,domain}}] 배열)")
    return {"n_iwa": len(iwa_ids), "n_onet_gwa": len(onet)}


# ── ONET41 한국어 임베딩 ─────────────────────────────────────────────
def _embed_onet_kr(translation: list[dict]) -> tuple[np.ndarray, list[str]]:
    from pipeline.dedup import bge_m3_embed
    order = [t["onet_gwa_id"] for t in translation]
    texts = [f"{t['label_kr']} : {t.get('definition_kr','')}".strip() for t in translation]
    e = np.asarray(bge_m3_embed(texts), dtype="float32")
    n = np.linalg.norm(e, axis=1, keepdims=True); n[n == 0] = 1.0
    return e / n, order


def run_map() -> dict:
    """ONET41 한국어 임베딩 → IWA 최근접 매핑 + 애매건 배치."""
    if not S4_TRANSLATION.exists():
        raise SystemExit(f"번역결과 없음: {S4_TRANSLATION} — Opus 번역 먼저(run_prep 참조)")
    if not S4_IWA_CENT.exists():
        raise SystemExit("IWA 대표벡터 없음 — prep 먼저 실행")
    translation = json.loads(S4_TRANSLATION.read_text(encoding="utf-8"))
    if len(translation) != 41:
        print(f"[map][warn] 번역 {len(translation)}건(기대 41) — 진행하되 확인 요")
    by_gwa = {t["onet_gwa_id"]: t for t in translation}

    iwa_emb = np.load(S4_IWA_CENT)
    iwa_ids = json.loads(S4_IWA_IDS.read_text(encoding="utf-8"))
    iwa_meta = _load_iwa_meta()

    gwa_emb, gwa_order = _embed_onet_kr(translation)
    np.save(S4_GWA_EMB, gwa_emb)
    S4_GWA_ORDER.write_text(json.dumps(gwa_order, ensure_ascii=False), encoding="utf-8")

    sim = iwa_emb @ gwa_emb.T                       # (178 × 41)
    mapping, batch_items, cos_lookup = {}, [], {}
    n_weak, n_ambig = 0, 0
    for i, iwa_id in enumerate(iwa_ids):
        row = sim[i]
        order = np.argsort(-row)
        top1, top2 = int(order[0]), int(order[1])
        cos1, cos2 = float(row[top1]), float(row[top2])
        margin = cos1 - cos2
        is_ambig = (cos1 < AMBIG_COS) or (margin < AMBIG_MARGIN)
        is_weak = cos1 < KR_UNIQUE_COS
        n_weak += int(is_weak); n_ambig += int(is_ambig)
        top3 = [{"gwa_id": gwa_order[int(j)],
                 "label_kr": by_gwa[gwa_order[int(j)]]["label_kr"],
                 "cosine": round(float(row[int(j)]), 4)} for j in order[:3]]
        # 임베딩 prior(폴백). GWA 추상수준은 임베딩 변별력 낮아 Opus가 정본 분류.
        mapping[iwa_id] = {
            "gwa_id": gwa_order[top1], "cosine": round(cos1, 4),
            "method": "mapped", "margin": round(margin, 4),
            "ambiguous": bool(is_ambig), "weak": bool(is_weak), "top3": top3}
        cos_lookup[iwa_id] = {gwa_order[j]: round(float(row[j]), 4)
                              for j in range(len(gwa_order))}
        m = iwa_meta.get(iwa_id, {})
        batch_items.append({
            "iwa_id": iwa_id, "iwa_label": m.get("label", ""),
            "iwa_definition": m.get("definition", ""),
            "top_candidates": top3})

    S4_MAP_JSON.write_text(json.dumps(mapping, ensure_ascii=False, indent=2),
                           encoding="utf-8")
    S4_COS_LOOKUP.write_text(json.dumps(cos_lookup, ensure_ascii=False),
                             encoding="utf-8")
    # 전수 분류 배치(Opus): system + 41 후보(in-context) + 전 IWA(임베딩 top3 힌트)
    system = (PROMPTS / "gwa_map_system.md").read_text(encoding="utf-8")
    candidates = [{"gwa_id": t["onet_gwa_id"], "label_kr": t["label_kr"],
                   "definition_kr": t.get("definition_kr", ""),
                   "domain": t.get("domain", "")} for t in translation]
    S4_MAP_BATCH.write_text(json.dumps(
        {"system": system, "gwa_candidates": candidates, "items": batch_items},
        ensure_ascii=False, indent=2), encoding="utf-8")

    # 분포 요약(임베딩 prior 기준 — 정본은 Opus 분류 후)
    dist = Counter(v["gwa_id"] for v in mapping.values())
    used = len(dist)
    print(f"[map] IWA {len(iwa_ids)} → GWA(임베딩 prior) · 사용 GWA {used}/41 · "
          f"임베딩 애매 {n_ambig} · weak(<{KR_UNIQUE_COS}) {n_weak}")
    coss = np.array([v["cosine"] for v in mapping.values()])
    summary = {
        "n_iwa": len(iwa_ids), "n_onet_gwa": len(translation),
        "used_gwa_embed_prior": used, "n_embed_ambiguous": n_ambig, "n_weak": n_weak,
        "embed_cosine_median": round(float(np.median(coss)), 4),
        "embed_cosine_min": round(float(coss.min()), 4),
        "top_gwa_embed_prior": [{"gwa_id": g, "label_kr": by_gwa[g]["label_kr"], "n_iwa": c}
                                for g, c in dist.most_common(10)],
    }
    S4_SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2),
                          encoding="utf-8")
    print(f"  임베딩 cosine 중앙값 {summary['embed_cosine_median']} · "
          f"최소 {summary['embed_cosine_min']}")
    print(f"  ▶ 전수 {len(iwa_ids)}건 Opus zero-shot 분류 → {S4_MAP_RES.name} "
          f"(임베딩 변별력 낮음 {n_ambig}/{len(iwa_ids)} 애매 → Opus 정본)")
    return summary


# ── 트랙2: 상향식 최상위 절단 ────────────────────────────────────────
def _natural_cut(Z, n, lo, hi, k_override=None):
    heights = Z[:, 2]
    best_k, best_gap, curve = None, -1.0, []
    for k in range(lo, hi + 1):
        i = n - 1 - k
        if i < 0 or i + 1 > len(heights) - 1:
            continue
        cut_h = float(heights[i]); gap = float(heights[i + 1] - heights[i])
        curve.append({"k": k, "cut_height": round(cut_h, 5), "gap": round(gap, 6)})
        if gap > best_gap:
            best_gap, best_k = gap, k
    if best_k is None:
        best_k = (lo + hi) // 2
    return (k_override or best_k), curve


def _assign_iwa_to_clusters(labels, ids, primary, dwa_to_iwa):
    """각 IWA → 소속 1차 TASK 다수결 트리군집. returns iwa_id→cluster_label."""
    idx_of = {t: i for i, t in enumerate(ids)}
    iwa_members: dict[str, list[str]] = defaultdict(list)  # iwa → primary task ids
    for dwa_id, iwa_id in dwa_to_iwa.items():
        iwa_members[iwa_id].extend(primary.get(dwa_id, []))
    out = {}
    for iwa_id, tids in iwa_members.items():
        labs = [int(labels[idx_of[t]]) for t in tids if t in idx_of]
        if not labs:
            continue
        out[iwa_id] = Counter(labs).most_common(1)[0][0]
    return out


def run_bottomup(k_override=None) -> dict:
    """트랙2: 같은 트리 최상위 절단 → 한국형 GWA 군집 → ONET 비교 + 명명배치."""
    from scipy.cluster.hierarchy import fcluster
    if not S4_GWA_EMB.exists():
        raise SystemExit("gwa_emb 없음 — map 먼저 실행(ONET 비교에 필요)")

    emb, Z, ids = _load_emb_and_link()
    n = len(ids)
    primary = _primary_tasks_of()
    dwa_to_iwa = _load_dwa_to_iwa()
    iwa_emb = np.load(S4_IWA_CENT)
    iwa_ids = json.loads(S4_IWA_IDS.read_text(encoding="utf-8"))
    iwa_meta = _load_iwa_meta()
    iwa_row = {iid: i for i, iid in enumerate(iwa_ids)}
    gwa_emb = np.load(S4_GWA_EMB)
    gwa_order = json.loads(S4_GWA_ORDER.read_text(encoding="utf-8"))
    translation = {t["onet_gwa_id"]: t for t in
                   json.loads(S4_TRANSLATION.read_text(encoding="utf-8"))}

    n_iwa = len(iwa_ids)
    # 자연 최상위 절단(band 2~60) + ONET 비교용 k=41
    k_nat, curve = _natural_cut(Z, n, 2, 60, k_override)

    def _clusters_at(k):
        labels = fcluster(Z, t=k, criterion="maxclust")
        iwa2c = _assign_iwa_to_clusters(labels, ids, primary, dwa_to_iwa)
        groups: dict[int, list[str]] = defaultdict(list)
        for iid, c in iwa2c.items():
            groups[c].append(iid)
        out = []
        for c, members in groups.items():
            mvec = np.vstack([iwa_emb[iwa_row[m]] for m in members if m in iwa_row])
            cent = mvec.mean(axis=0); cent = cent / (np.linalg.norm(cent) or 1.0)
            sims = gwa_emb @ cent
            j = int(np.argmax(sims))
            out.append({"cluster": int(c), "n_iwa": len(members),
                        "member_iwa_ids": members,
                        "nearest_onet": gwa_order[j],
                        "nearest_onet_label": translation[gwa_order[j]]["label_kr"],
                        "nearest_cosine": round(float(sims[j]), 4),
                        "centroid": cent})
        out.sort(key=lambda d: -d["n_iwa"])
        return out

    nat = _clusters_at(k_nat)
    k41 = _clusters_at(41)

    def _onet_match_stats(clusters):
        matched = {c["nearest_onet"] for c in clusters if c["nearest_cosine"] >= KR_UNIQUE_COS}
        coss = [c["nearest_cosine"] for c in clusters]
        return {"n_clusters": len(clusters),
                "onet_distinct_matched": len(matched),
                "onet_coverage_41": round(len(matched) / 41, 3),
                "mean_nearest_cosine": round(float(np.mean(coss)), 4) if coss else 0.0,
                "kr_unique_candidates": sum(1 for c in clusters
                                            if c["nearest_cosine"] < KR_UNIQUE_COS)}

    stats_nat = _onet_match_stats(nat)
    stats_41 = _onet_match_stats(k41)

    # 자연 절단 군집을 정본으로 id 부여 + 명명배치
    bottomup = []
    batch_items = []
    for j, c in enumerate(nat, 1):
        kr_id = f"KG_{j:02d}"
        ranked = sorted(c["member_iwa_ids"],
                        key=lambda m: -float(iwa_emb[iwa_row[m]] @ c["centroid"])
                        if m in iwa_row else 0.0)
        rep_labels = [iwa_meta[m]["label"] for m in ranked[:N_REP_IWA]
                      if m in iwa_meta]
        bottomup.append({
            "kr_gwa_id": kr_id, "n_iwa": c["n_iwa"],
            "member_iwa_ids": c["member_iwa_ids"],
            "nearest_onet": c["nearest_onet"],
            "nearest_onet_label": c["nearest_onet_label"],
            "nearest_cosine": c["nearest_cosine"],
            "rep_iwa_labels": rep_labels})
        batch_items.append({"kr_gwa_id": kr_id, "n_iwa": c["n_iwa"],
                            "member_iwa_labels": rep_labels})

    S4_BOTTOMUP.write_text(json.dumps(bottomup, ensure_ascii=False, indent=2),
                           encoding="utf-8")
    system = (PROMPTS / "gwa_bottomup_system.md").read_text(encoding="utf-8")
    S4_BU_BATCH.write_text(json.dumps(
        {"system": system, "items": batch_items}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    bu_summary = {
        "k_natural": int(k_nat), "n_kr_gwa_natural": len(nat),
        "natural_vs_onet": stats_nat, "k41_vs_onet": stats_41,
        "cut_curve_head": sorted(curve, key=lambda x: -x["gap"])[:8],
    }
    S4_BU_SUMMARY.write_text(json.dumps(bu_summary, ensure_ascii=False, indent=2),
                             encoding="utf-8")
    print(f"[bottomup] 자연절단 k={k_nat} → 한국형 GWA {len(nat)}개")
    print(f"  자연 vs ONET: 군집 {stats_nat['n_clusters']} · ONET매칭 "
          f"{stats_nat['onet_distinct_matched']}/41(coverage {stats_nat['onet_coverage_41']}) · "
          f"평균 최근접 cos {stats_nat['mean_nearest_cosine']} · "
          f"한국특이후보 {stats_nat['kr_unique_candidates']}")
    print(f"  k=41 vs ONET: 군집 {stats_41['n_clusters']} · ONET매칭 "
          f"{stats_41['onet_distinct_matched']}/41 · 평균 cos {stats_41['mean_nearest_cosine']}")
    print(f"  ▶ 명명: Opus 서브에이전트가 {S4_BU_BATCH.name} → {CACHE.name}/s4_bottomup_result.json")
    return bu_summary


def diagnose() -> None:
    emb, Z, ids = _load_emb_and_link()
    n = len(ids)
    k, curve = _natural_cut(Z, n, 2, 60)
    print(f"[diagnose] 상향식 GWA 권장 자연절단 k={k}  (band 2~60)")
    print("  상위 gap 15 (k, cut_height, gap):")
    for r in sorted(curve, key=lambda x: -x["gap"])[:15]:
        print(f"    k={r['k']:4d}  h={r['cut_height']:.4f}  gap={r['gap']:.6f}")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["prep", "map", "bottomup", "diagnose"])
    ap.add_argument("--k", type=int, default=None, help="상향식 절단 k 강제")
    a = ap.parse_args()
    if a.cmd == "prep":
        run_prep()
    elif a.cmd == "map":
        run_map()
    elif a.cmd == "bottomup":
        run_bottomup(k_override=a.k)
    else:
        diagnose()
