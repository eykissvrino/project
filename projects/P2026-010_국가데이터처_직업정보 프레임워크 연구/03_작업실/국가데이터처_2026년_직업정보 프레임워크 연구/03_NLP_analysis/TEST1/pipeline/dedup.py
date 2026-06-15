"""의미중복(near-dup) 병합 — bge-m3 임베딩 코사인 ≥ 임계 통합.

설계 §4-6(C3): 2회 합집합은 의역 중복을 늘려 Stage 2 군집을 오염시키므로,
임베딩 near-dup 병합을 TASK 단계에서 선행한다(임베딩은 어차피 Stage 2 입력).

본 단계 책임 = **직업 내부** 의역중복 통합(같은 ksco_code의 task/도구/환경 리스트).
직업 *간* 의미통합은 Stage 2(군집)가 담당 — 여기서 하지 않는다.

Stage 2 재사용 가능하게 임베딩 함수와 병합 로직을 분리했다(embed_fn 주입 → 테스트는 LLM·모델 없이).
"""
from __future__ import annotations

from typing import Callable, Iterable

NEAR_DUP_COS = 0.90

_MODEL = None


def _get_model():
    """bge-m3 모델 지연 로드(싱글턴). 최초 1회만 가중치 로드."""
    global _MODEL
    if _MODEL is None:
        from FlagEmbedding import BGEM3FlagModel
        _MODEL = BGEM3FlagModel("BAAI/bge-m3", use_fp16=True)
    return _MODEL


def bge_m3_embed(texts: list[str]):
    """문장 리스트 → dense 임베딩(numpy 2D). 빈 입력 방어."""
    if not texts:
        import numpy as np
        return np.zeros((0, 1024), dtype="float32")
    model = _get_model()
    return model.encode(texts, batch_size=12, max_length=256)["dense_vecs"]


def _cosine_matrix(vecs):
    import numpy as np
    v = np.asarray(vecs, dtype="float32")
    n = np.linalg.norm(v, axis=1, keepdims=True)
    n[n == 0] = 1.0
    u = v / n
    return u @ u.T


def merge_near_dup(
    items: list[dict],
    text_key: str,
    *,
    threshold: float = NEAR_DUP_COS,
    embed_fn: Callable[[list[str]], "object"] | None = None,
    conf_key: str = "confidence",
) -> tuple[list[dict], list[dict]]:
    """items 를 text_key 임베딩 코사인 ≥ threshold 로 군집·통합.

    대표 선택: confidence 최고 → 동률이면 먼저 등장(원래 순서).
    Returns: (deduped_items, merge_log[{kept, dropped, cosine}]).
    """
    if len(items) <= 1:
        return list(items), []
    texts = [str(it.get(text_key) or "") for it in items]
    embed = embed_fn or bge_m3_embed
    sim = _cosine_matrix(embed(texts))

    n = len(items)
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)

    log = []
    for i in range(n):
        for j in range(i + 1, n):
            if float(sim[i][j]) >= threshold:
                union(i, j)

    clusters: dict[int, list[int]] = {}
    for i in range(n):
        clusters.setdefault(find(i), []).append(i)

    kept_items, seen_root = [], set()
    for i in range(n):  # 원래 순서 보존
        root = find(i)
        if root in seen_root:
            continue
        seen_root.add(root)
        members = clusters[root]
        rep = max(members, key=lambda m: (float(items[m].get(conf_key) or 0), -m))
        kept = {**items[rep]}
        if len(members) > 1:
            kept["merged_count"] = len(members)
            for m in members:
                if m == rep:
                    continue
                log.append({"kept": texts[rep], "dropped": texts[m],
                            "cosine": round(float(sim[rep][m]), 4)})
        kept_items.append(kept)
    return kept_items, log


def dedup_result(result: dict, *, threshold: float = NEAR_DUP_COS,
                 embed_fn=None) -> tuple[dict, dict]:
    """union_runs 결과 한 건의 task/tools/work_context 를 각각 near-dup 병합.

    Returns: (deduped_result, log{tasks,tools,work_context}).
    """
    tasks, lt = merge_near_dup(result.get("tasks", []), "full_statement",
                               threshold=threshold, embed_fn=embed_fn)
    tools, lo = merge_near_dup(result.get("tools", []), "name",
                               threshold=threshold, embed_fn=embed_fn)
    work, lw = merge_near_dup(result.get("work_context", []), "value",
                              threshold=threshold, embed_fn=embed_fn)
    out = {**result, "tasks": tasks, "tools": tools, "work_context": work}
    return out, {"tasks": lt, "tools": lo, "work_context": lw}
