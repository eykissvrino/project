"""Stage 4c — 연역적 한국형 GWA 도출 (ONET '방법'을 복제, ONET '41목록'은 미사용).

기존 Stage4(트랙1 ONET채택)·4b(순수상향식)와 별개. ONET이 GWA를 만든 방식 그대로:
이론 프레임 고정 → KSCO IWA 인벤토리를 근거로 → worker-oriented 일반범주를 연역 설계 → 데이터로 검증.

── 방법(ONET 재현) ──────────────────────────────────────────────────
 (1) 정보처리 4영역(입력·처리·산출·상호작용)을 천장으로 고정(이론, ONET-41 아님).
 (2) Opus(I/O 전문가 패널 대리)가 178 IWA 인벤토리를 근거로 GWA 분류체계를 연역 설계
     — 데이터 군집을 읽는 게 아니라 이론 우선·데이터 근거. 이론상 필요하나 데이터 얇은
     범주(의사결정·전략수립 등)는 basis='theory'로 포함(완결성). prompts/gwa_deductive_design_system.md.
 (3) 우리 178 IWA를 설계된 KR-GWA에 매핑(strict 1:1). 빈 GWA=추출로는 안 잡히는 이론범주(측정 필요).
 (4) 검증: 커버리지·basis 분포·ONET 41 정합(구성타당도).

흐름:
    prep     설계입력 cache/s4c_design_input.json (4영역 정의 + 178 IWA + 영역힌트)
    (Opus 설계 → cache/s4c_gwa_design.json: {domains, gwa[]})
    map      설계 KR-GWA 임베딩 → IWA 매핑배치 cache/s4c_map_b*.json + cos룩업
    (Opus 매핑 → s4c_map_res*.json)
    persist  DB(kr_gwa_deductive·iwa_to_kr_gwa_deductive) + Excel + 해설서

입력 캐시: s4_iwa_centroids.npy(prep), s4_gwa_emb.npy·s4_gwa_order.json·s4_translation.json(ONET 비교).
PYTHONUTF8=1 권장.
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
OUTPUTS = TEST1_DIR / "outputs"
RESULTS = (TEST1_DIR / ".." / ".." / "04_framework_design" / "docs"
           / "stages" / "results").resolve()

IWA_CENT = CACHE / "s4_iwa_centroids.npy"
IWA_IDS = CACHE / "s4_iwa_ids.json"
GWA_EMB = CACHE / "s4_gwa_emb.npy"
GWA_ORDER = CACHE / "s4_gwa_order.json"
TRANSLATION = CACHE / "s4_translation.json"

DESIGN_INPUT = CACHE / "s4c_design_input.json"
DESIGN = CACHE / "s4c_gwa_design.json"        # Opus 설계 결과
KR_EMB = CACHE / "s4c_kr_emb.npy"
KR_ORDER = CACHE / "s4c_kr_order.json"
MAP_JSON = CACHE / "s4c_iwa_to_kr.json"        # 임베딩 prior
COS_LOOKUP = CACHE / "s4c_cos.json"
MAP_RESULT = CACHE / "s4c_map_result.json"     # Opus 매핑 병합
SUMMARY = CACHE / "s4c_summary.json"

# 정보처리 4영역(이론 프레임 — ONET 41 아님)
DOMAINS = [
    {"domain_id": "ID1", "label": "정보 입력",
     "definition": "업무 수행에 필요한 정보·자료·신호를 감지·수집·확인·평가하는 활동. 관찰·점검·식별·검사·측정·추정 등 외부로부터 정보를 받아들이는 모든 작업활동을 포함한다."},
    {"domain_id": "ID2", "label": "정신 과정",
     "definition": "수집된 정보를 처리·분석·판단하여 의사결정·계획·창안·문제해결을 수행하는 인지 활동. 분석·평가·추론·기획·설계·창작 등 머리로 수행하는 작업활동을 포함한다."},
    {"domain_id": "ID3", "label": "작업 산출",
     "definition": "신체·도구·기계·장비를 사용해 대상을 다루거나 변형·이동·제작·조작하여 물리적 결과를 만들어내는 활동. 운전·조작·제작·시공·정비·취급 등 물리적 산출을 포함한다."},
    {"domain_id": "ID4", "label": "타인과의 상호작용",
     "definition": "타인과 소통·조정·지원·지도·관리·설득하여 협업하거나 서비스를 제공하는 활동. 의사소통·응대·돌봄·교육·지휘·협상·판매 등 사람을 대상으로 하는 작업활동을 포함한다."},
]


def _load_iwa_meta() -> list[dict]:
    from pipeline import db
    con = db.get_con(read_only=True)
    rows = con.execute(
        "SELECT iwa_id, label, definition, n_dwa, n_jobs FROM iwa ORDER BY iwa_id").fetchall()
    con.close()
    return [{"iwa_id": r[0], "label": r[1], "definition": r[2],
             "n_dwa": r[3], "n_jobs": r[4]} for r in rows]


def _embed(texts):
    from pipeline.dedup import bge_m3_embed
    e = np.asarray(bge_m3_embed(texts), dtype="float32")
    n = np.linalg.norm(e, axis=1, keepdims=True); n[n == 0] = 1.0
    return e / n


def run_prep() -> dict:
    """설계 입력 조립: 4영역 정의 + 178 IWA(+임베딩 영역힌트)."""
    if not IWA_CENT.exists():
        raise SystemExit("s4_iwa_centroids.npy 없음 — Stage4 prep 먼저")
    meta = _load_iwa_meta()
    iwa_emb = np.load(IWA_CENT)
    iwa_ids = json.loads(IWA_IDS.read_text(encoding="utf-8"))
    row = {i: k for k, i in enumerate(iwa_ids)}

    # 영역 힌트(영역 정의 임베딩과 최근접) — ONET 41 미사용, 4영역 정의만 사용
    dom_emb = _embed([d["definition"] for d in DOMAINS])
    inv = []
    for m in meta:
        if m["iwa_id"] not in row:
            continue
        sims = dom_emb @ iwa_emb[row[m["iwa_id"]]]
        hint = DOMAINS[int(np.argmax(sims))]["label"]
        inv.append({"iwa_id": m["iwa_id"], "label": m["label"],
                    "domain_hint": hint, "n_dwa": m["n_dwa"], "n_jobs": m["n_jobs"]})

    system = (PROMPTS / "gwa_deductive_design_system.md").read_text(encoding="utf-8")
    DESIGN_INPUT.write_text(json.dumps({
        "domains": [{"domain_id": d["domain_id"], "label": d["label"],
                     "definition": d["definition"]} for d in DOMAINS],
        "iwa_inventory": inv,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    (CACHE / "s4c_design_system.md").write_text(system, encoding="utf-8")

    hint_dist = Counter(x["domain_hint"] for x in inv)
    print(f"[prep] 설계입력 작성: 4영역 + IWA {len(inv)}건 → {DESIGN_INPUT.relative_to(TEST1_DIR)}")
    print(f"       영역힌트 분포(참고): {dict(hint_dist)}")
    print(f"  ▶ Opus(전문가 패널)가 system(gwa_deductive_design_system.md)+design_input 으로")
    print(f"     KR-GWA 분류체계 연역 설계 → {DESIGN.name} ({{domains, gwa[]}})")
    return {"n_iwa": len(inv), "hint_dist": dict(hint_dist)}


def run_map() -> dict:
    """설계된 KR-GWA 임베딩 → IWA 최근접 prior + 전수 매핑배치."""
    if not DESIGN.exists():
        raise SystemExit(f"설계 결과 없음: {DESIGN} — Opus 설계 먼저(run_prep 참조)")
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    gwa = design["gwa"]
    by_dom = {d["domain_id"]: d.get("label_kr", d.get("label", d["domain_id"]))
              for d in design["domains"]}
    meta = {m["iwa_id"]: m for m in _load_iwa_meta()}
    iwa_emb = np.load(IWA_CENT)
    iwa_ids = json.loads(IWA_IDS.read_text(encoding="utf-8"))

    kr_text = [f"{g['label_kr']} : {g.get('definition_kr','')}".strip() for g in gwa]
    kr_emb = _embed(kr_text)
    kr_order = [g["gwa_id"] for g in gwa]
    np.save(KR_EMB, kr_emb)
    KR_ORDER.write_text(json.dumps(kr_order, ensure_ascii=False), encoding="utf-8")

    sim = iwa_emb @ kr_emb.T                     # (178 × N)
    by_gwa = {g["gwa_id"]: g for g in gwa}
    mapping, cos_lookup, batch_items = {}, {}, []
    for i, iwa_id in enumerate(iwa_ids):
        rowv = sim[i]; order = np.argsort(-rowv)
        top3 = [{"gwa_id": kr_order[int(j)], "label_kr": by_gwa[kr_order[int(j)]]["label_kr"],
                 "domain": by_dom.get(by_gwa[kr_order[int(j)]]["domain_id"], ""),
                 "cosine": round(float(rowv[int(j)]), 4)} for j in order[:3]]
        mapping[iwa_id] = {"gwa_id": kr_order[int(order[0])],
                           "cosine": round(float(rowv[int(order[0])]), 4), "method": "mapped"}
        cos_lookup[iwa_id] = {kr_order[j]: round(float(rowv[j]), 4) for j in range(len(kr_order))}
        m = meta.get(iwa_id, {})
        batch_items.append({"iwa_id": iwa_id, "iwa_label": m.get("label", ""),
                            "iwa_definition": m.get("definition", ""), "top_candidates": top3})

    MAP_JSON.write_text(json.dumps(mapping, ensure_ascii=False, indent=2), encoding="utf-8")
    COS_LOOKUP.write_text(json.dumps(cos_lookup, ensure_ascii=False), encoding="utf-8")

    candidates = [{"gwa_id": g["gwa_id"], "label_kr": g["label_kr"],
                   "definition_kr": g.get("definition_kr", ""),
                   "domain": by_dom.get(g["domain_id"], "")} for g in gwa]
    system = (PROMPTS / "gwa_map_system.md").read_text(encoding="utf-8")
    size = 30
    nb = 0
    for s0 in range(0, len(batch_items), size):
        chunk = batch_items[s0:s0 + size]
        (CACHE / f"s4c_map_b{nb}.json").write_text(json.dumps(
            {"system": system, "gwa_candidates": candidates, "items": chunk},
            ensure_ascii=False, indent=2), encoding="utf-8")
        nb += 1
    print(f"[map] KR-GWA {len(gwa)}개 임베딩 · IWA {len(iwa_ids)} 매핑배치 {nb}개(30씩)")
    print(f"  ▶ Opus가 s4c_map_b0..{nb-1}.json → s4c_map_res0..{nb-1}.json (각 IWA→KR-GWA 1개)")
    print(f"     병합 → {MAP_RESULT.name}")
    return {"n_gwa": len(gwa), "n_batches": nb}


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["prep", "map"])
    a = ap.parse_args()
    if a.cmd == "prep":
        run_prep()
    else:
        run_map()
