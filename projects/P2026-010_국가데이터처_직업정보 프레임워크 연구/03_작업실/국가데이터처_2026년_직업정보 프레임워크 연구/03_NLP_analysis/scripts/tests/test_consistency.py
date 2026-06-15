"""consistency.py 단위테스트 (사양서 §1.4). 순수 함수 — 키·DB 불필요."""
from utils import consistency as C


def _t(verb, obj, stmt=None):
    return {"verb": verb, "object": obj, "full_statement": stmt or f"{obj}을 {verb}"}


# ── jaccard ──────────────────────────────────────────────────────────────────
def test_jaccard_both_empty_is_one():
    assert C.jaccard(set(), set()) == 1.0


def test_jaccard_identical():
    s = {("검토하다", "도면")}
    assert C.jaccard(s, s) == 1.0


def test_jaccard_disjoint_is_zero():
    assert C.jaccard({("a", "b")}, {("c", "d")}) == 0.0


def test_jaccard_half():
    s1 = {("a", "b"), ("c", "d")}
    s2 = {("a", "b"), ("e", "f")}
    assert C.jaccard(s1, s2) == 1 / 3  # 교집합1 / 합집합3


# ── self_consistency ─────────────────────────────────────────────────────────
def test_self_consistency_auto_accept_keeps_intersection():
    tasks = [_t("작성하다", "재무제표"), _t("조사하다", "회계기록"), _t("수행하다", "감사")]
    out1 = {"tasks": tasks}
    out2 = {"tasks": tasks}  # 완전 일치
    accepted, jac, status = C.self_consistency(out1, out2)
    assert status == "auto_accept"
    assert jac == 1.0
    assert len(accepted) == 3
    assert all(a["confidence"] == C.CONF_AUTO_ACCEPT for a in accepted)


def test_self_consistency_drops_non_intersection():
    out1 = {"tasks": [_t("작성하다", "재무제표"), _t("조사하다", "회계기록"),
                       _t("수행하다", "감사"), _t("제공하다", "자문")]}
    out2 = {"tasks": [_t("작성하다", "재무제표"), _t("조사하다", "회계기록"),
                       _t("수행하다", "감사"), _t("정리하다", "자료")]}
    # 합집합5, 교집합3 → jaccard 0.6 < 0.85 → cross_check_required
    accepted, jac, status = C.self_consistency(out1, out2)
    assert status == "cross_check_required"
    assert abs(jac - 0.6) < 1e-9
    assert accepted == []


def test_self_consistency_high_overlap_accepts():
    common = [_t(f"v{i}", f"o{i}") for i in range(9)]
    out1 = {"tasks": common + [_t("x", "y")]}
    out2 = {"tasks": common + [_t("x", "y")]}
    accepted, jac, status = C.self_consistency(out1, out2)
    assert status == "auto_accept" and jac == 1.0 and len(accepted) == 10


def test_self_consistency_empty_both():
    accepted, jac, status = C.self_consistency({"tasks": []}, {"tasks": []})
    assert status == "auto_accept" and jac == 1.0 and accepted == []


# ── cross_model_vote ─────────────────────────────────────────────────────────
def test_cross_model_majority_2_of_3():
    a = _t("작성하다", "재무제표")
    b = _t("조사하다", "회계기록")
    c = _t("제공하다", "자문")
    out1 = {"tasks": [a, b]}
    out2 = {"tasks": [a, c]}
    out3 = {"tasks": [a, b]}
    accepted, status = C.cross_model_vote(out1, out2, out3)
    keys = {(x["verb"], x["object"]) for x in accepted}
    assert status == "cross_model_vote"
    assert ("작성하다", "재무제표") in keys   # 3표
    assert ("조사하다", "회계기록") in keys   # 2표
    assert ("제공하다", "자문") not in keys   # 1표 탈락
    assert all(x["confidence"] == C.CONF_REVIEW for x in accepted)


def test_cross_model_dup_within_one_output_counts_once():
    a = _t("작성하다", "재무제표")
    out1 = {"tasks": [a, a, a]}  # 같은 출력 내 3개 = 1표
    out2 = {"tasks": []}
    out3 = {"tasks": []}
    accepted, _ = C.cross_model_vote(out1, out2, out3)
    assert accepted == []  # 1표뿐 → 탈락


# ── responsibility_consistency ───────────────────────────────────────────────
def test_resp_consistent():
    o = {"mgmt_score": 2, "supervisory_score": 1, "safety_score": 0}
    res, conf, status = C.responsibility_consistency(o, dict(o))
    assert status == "consistent" and conf == 1.0


def test_resp_averaged_small_diff():
    o1 = {"mgmt_score": 2, "supervisory_score": 1, "safety_score": 0}
    o2 = {"mgmt_score": 3, "supervisory_score": 1, "safety_score": 0}  # diff 1
    res, conf, status = C.responsibility_consistency(o1, o2)
    assert status == "averaged" and conf == 0.85
    assert res["mgmt_score"] in (2, 3) and res["total_score"] == sum(
        res[k] for k in ["mgmt_score", "supervisory_score", "safety_score"])


def test_resp_review_required_large_diff():
    o1 = {"mgmt_score": 0, "supervisory_score": 0, "safety_score": 0}
    o2 = {"mgmt_score": 3, "supervisory_score": 0, "safety_score": 0}  # diff 3 > 2
    res, conf, status = C.responsibility_consistency(o1, o2)
    assert status == "review_required" and conf == 0.65
