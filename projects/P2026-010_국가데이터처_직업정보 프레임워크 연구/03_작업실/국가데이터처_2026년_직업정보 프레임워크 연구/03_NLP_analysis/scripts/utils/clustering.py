"""임베딩 + 밀도군집 (사양서 §3.2). bge-m3 + sklearn HDBSCAN.

설계서 §4 ④-a. hdbscan 패키지 대신 scikit-learn 내장 HDBSCAN 사용
([Layer 1] Windows 빌드 footgun 회피, 동일 알고리즘).
첫 호출 시 bge-m3 모델(~2GB) 자동 다운로드.
"""
from __future__ import annotations

import os

import numpy as np

_model_cache: dict = {}
DEFAULT_MODEL = os.environ.get("EMBED_MODEL", "BAAI/bge-m3")


def get_model(name: str = DEFAULT_MODEL):
    from sentence_transformers import SentenceTransformer
    if name not in _model_cache:
        _model_cache[name] = SentenceTransformer(name)
    return _model_cache[name]


def embed(texts: list[str], model_name: str = DEFAULT_MODEL, batch_size: int = 16) -> np.ndarray:
    """L2 정규화 임베딩 (N, dim). 정규화 → 코사인=내적."""
    model = get_model(model_name)
    return model.encode(texts, normalize_embeddings=True, batch_size=batch_size,
                        show_progress_bar=False)


def hdbscan_cluster(emb: np.ndarray, min_cluster_size: int = 4, min_samples: int = 2,
                    method: str = "eom") -> np.ndarray:
    """HDBSCAN 군집 라벨. -1 = 노이즈(미배치).

    method='eom'  → 큰 안정 군집 선호(거칠게, IWA용)
    method='leaf' → 잎 노드까지 세분(세밀하게, DWA용 — ONET식 다수 DWA)
    """
    from sklearn.cluster import HDBSCAN
    cl = HDBSCAN(min_cluster_size=min_cluster_size, min_samples=min_samples,
                 metric="euclidean", cluster_selection_method=method)
    return cl.fit_predict(emb)


def assign_nearest(task_emb: np.ndarray, ref_emb: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """각 task를 가장 가까운 참조(예: ONET 41 GWA 라벨)에 할당.

    정규화 임베딩 가정 → 코사인 = 내적. 반환 (argmax_idx, cos_score).
    """
    sims = task_emb @ ref_emb.T           # (N_task, N_ref)
    idx = sims.argmax(axis=1)
    score = sims.max(axis=1)
    return idx, score


def mean_cosine(emb: np.ndarray) -> float:
    """군집 내 평균 쌍별 코사인(응집도, 사양서 §4-b 기준 ≥0.70). 정규화 가정."""
    if len(emb) < 2:
        return 1.0
    sims = emb @ emb.T
    n = len(emb)
    off = (sims.sum() - n) / (n * (n - 1))  # 대각(자기자신=1) 제외 평균
    return float(off)
