"""Self-Consistency + Cross-Model 다수결 (사양서 §1.4).

TASK 추출의 재현성·신뢰도 판정을 담당한다. LLM 호출은 하지 않는다(순수 함수).
판정 단위는 (verb, object) 튜플 집합의 Jaccard 일치율.

    TASK 2회 독립 실행 ─┬─ Jaccard ≥ 0.85 ─▶ 교집합 채택 (auto_accept, conf 0.95)
                        └─ < 0.85 ─▶ GPT-5 추가 3-set 다수결 (review_required, conf 0.75)

설계 근거: 12_도출방법론_설계서.md §4 ②, 사양서 §1.4
"""
from __future__ import annotations

from collections import Counter
from typing import Iterable

# 채택 임계 (사양서 §1.1, §1.4)
JACCARD_THRESHOLD = 0.85
CONF_AUTO_ACCEPT = 0.95
CONF_REVIEW = 0.75

TaskKey = tuple[str, str]  # (verb, object)


def _norm(s: str | None) -> str:
    """비교용 정규화: None 방어 + 공백 제거 + 소문자화는 하지 않음(한국어).

    한국어는 대소문자 개념이 없으므로 strip만. 앞뒤 공백·중복 공백만 제거한다.
    """
    if s is None:
        return ""
    return " ".join(str(s).split())


def task_key(task: dict) -> TaskKey:
    """task dict → (verb, object) 비교 키. 누락 필드는 빈 문자열로 방어."""
    return (_norm(task.get("verb")), _norm(task.get("object")))


def task_set(tasks: Iterable[dict] | None) -> set[TaskKey]:
    """task 리스트 → (verb, object) 집합. None/빈 입력은 빈 집합."""
    if not tasks:
        return set()
    return {task_key(t) for t in tasks}


def jaccard(set1: set[TaskKey], set2: set[TaskKey]) -> float:
    """Jaccard 일치율. 양쪽 모두 비면 1.0(완전 일치로 간주, 사양서 §1.4)."""
    if not set1 and not set2:
        return 1.0
    union = set1 | set2
    if not union:
        return 1.0
    return len(set1 & set2) / len(union)


def self_consistency(
    out1: dict,
    out2: dict,
    threshold: float = JACCARD_THRESHOLD,
) -> tuple[list[dict], float, str]:
    """동일 입력 2회(seed 0·1) 결과의 self-consistency 판정 (사양서 §1.4).

    Args:
        out1, out2: LLM 출력 dict. 최소 'tasks': list[dict] 키를 가진다.
        threshold: 채택 임계 Jaccard.

    Returns:
        (accepted_tasks, jaccard, status)
        - status == 'auto_accept': 교집합 task만 채택, confidence 0.95 부여
        - status == 'cross_check_required': 임계 미달 → cross_model_vote 호출 필요
          (이 경우 accepted_tasks는 out1·out2 합집합의 교집합 후보를 임시 반환)
    """
    tasks1 = out1.get("tasks") or []
    tasks2 = out2.get("tasks") or []
    s1, s2 = task_set(tasks1), task_set(tasks2)
    jac = jaccard(s1, s2)

    if jac >= threshold:
        inter = s1 & s2
        accepted = []
        for t in tasks1:
            if task_key(t) in inter:
                t = {**t, "confidence": CONF_AUTO_ACCEPT}
                accepted.append(t)
        return accepted, jac, "auto_accept"

    # 임계 미달 → 호출자가 GPT-5 결과로 cross_model_vote를 돌려야 한다.
    return [], jac, "cross_check_required"


def cross_model_vote(
    out1: dict,
    out2: dict,
    out3: dict,
    min_votes: int = 2,
) -> tuple[list[dict], str]:
    """3-set 다수결 (사양서 §1.4). 2개 이상 출력에 나타난 task만 채택.

    Args:
        out1, out2: 1차 모델(예: Claude) seed 0·1
        out3: cross-check 모델(예: GPT-5) seed 0
        min_votes: 채택 최소 득표(기본 2/3)

    Returns:
        (accepted_tasks, status='cross_model_vote'). confidence 0.75 부여.
        대표 진술은 가장 먼저 등장한 출력의 full_statement를 사용한다.
    """
    outs = [out1, out2, out3]
    votes: Counter[TaskKey] = Counter()
    representative: dict[TaskKey, dict] = {}
    for out in outs:
        seen_this_out: set[TaskKey] = set()
        for t in out.get("tasks") or []:
            k = task_key(t)
            if k in seen_this_out:
                continue  # 같은 출력 내 중복은 1표
            seen_this_out.add(k)
            votes[k] += 1
            representative.setdefault(k, t)

    accepted = []
    for k, n in votes.items():
        if n >= min_votes:
            t = {**representative[k], "confidence": CONF_REVIEW, "votes": n}
            accepted.append(t)
    return accepted, "cross_model_vote"


def responsibility_consistency(
    out1: dict, out2: dict
) -> tuple[dict, float, str]:
    """Responsibility 3축 2회 일관성 (사양서 §6.4).

    점수차 합 == 0 → consistent(1.0) / ≤ 2 → averaged(0.85) / > 2 → review_required(0.65).
    """
    axes = ["mgmt_score", "supervisory_score", "safety_score"]
    diff = sum(abs(int(out1.get(a, 0)) - int(out2.get(a, 0))) for a in axes)
    if diff == 0:
        return out1, 1.0, "consistent"
    if diff <= 2:
        avg = {a: round((int(out1.get(a, 0)) + int(out2.get(a, 0))) / 2) for a in axes}
        avg["total_score"] = sum(avg.values())
        return avg, 0.85, "averaged"
    return {}, 0.65, "review_required"
