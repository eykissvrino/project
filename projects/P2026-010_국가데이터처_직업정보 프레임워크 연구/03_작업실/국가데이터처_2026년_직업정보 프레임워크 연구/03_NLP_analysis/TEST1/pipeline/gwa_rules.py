"""Stage 4 — GWA 명사형 검증.

GWA는 직업·산업 무관 최상위 일반 작업활동 '범주'이며, ONET이 명사구로 표기한다
(예: "정보 입수", "데이터·정보 분석", "의사결정 및 문제해결"). 따라서 DWA/IWA와 달리
**명사형**이 정상이고 '~한다' 동사종결이 오히려 위반이다(검증 방향이 반대).

게이트(하드): G1 명사형(동사종결 아님)·G2 빈 라벨 아님·G3 예시·열거구 없음.
경고(소프트): G4 길이(명사구 권고 어절)·G5 높임/과거 종결 흔적.

사용:
    from pipeline.gwa_rules import check_gwa, check_batch_gwa
    r = check_gwa("데이터·정보 분석")     # passed=True
    r = check_gwa("정보를 분석한다")        # G1 위반(동사종결)
"""
from __future__ import annotations

import re

from pipeline import dwa_rules

PASS_RATE_GATE = dwa_rules.PASS_RATE_GATE
EXAMPLE_PATTERNS = dwa_rules.EXAMPLE_PATTERNS

# 동사 평서 종결(GWA에선 위반) — '~한다/된다/하다/짓다' 등 용언 종지형
VERB_END = [r"한다$", r"된다$", r"는다$", r"진다$", r"받는다$",
            r"하다$", r"되다$"]
HONORIFIC = [r"합니다$", r"습니다$", r"입니다$"]
PAST = [r"하였다$", r"했다$", r"되었다$", r"였다$"]
MAX_EOJEOL_GWA = 12        # 명사구 권고 어절 상한


def _eojeol(s: str) -> int:
    return len([w for w in re.split(r"\s+", s.strip()) if w])


def normalize_label(label: str) -> str:
    """말미 마침표·공백 제거. GWA는 명사형이라 종지부 없이 저장."""
    return (label or "").strip().rstrip(" .。·")


def check_gwa(label: str) -> dict:
    """GWA label 1건 검증. passed = G1·G2·G3(하드) 통과."""
    s = normalize_label(label)
    v: list[str] = []
    w: list[str] = []
    rules: dict[str, bool] = {}

    n_eoj = _eojeol(s)

    # G2: 빈 라벨 아님
    g2 = n_eoj > 0
    if not g2:
        v.append("G2: 빈 라벨")
    rules["G2_비어있지않음"] = g2

    # G1: 명사형(동사 평서종결이면 위반)
    verb_hit = any(re.search(p, s) for p in VERB_END)
    g1 = not verb_hit
    if not g1:
        v.append("G1: 동사종결('~한다')—GWA는 명사형이어야 함")
    rules["G1_명사형"] = g1

    # G3: 예시·열거구 없음
    hit3 = [p for p in EXAMPLE_PATTERNS if re.search(p, s)]
    g3 = not hit3
    if not g3:
        v.append("G3: 예시·열거구('~등/~와 같은')")
    rules["G3_예시금지"] = g3

    # G4: 길이(경고)
    g4 = 0 < n_eoj <= MAX_EOJEOL_GWA
    if n_eoj > MAX_EOJEOL_GWA:
        w.append(f"G4: {n_eoj}어절(명사구 권고 {MAX_EOJEOL_GWA} 초과)")
    rules["G4_가독성"] = g4

    # G5: 높임/과거 종결 흔적(경고)
    if any(re.search(p, s) for p in HONORIFIC + PAST):
        w.append("G5: 높임/과거 종결 흔적")

    hard_ok = g1 and g2 and g3
    return {"label": s, "passed": hard_ok, "violations": v,
            "warnings": w, "rules": rules, "eojeol": n_eoj}


def check_batch_gwa(labels: list[str]) -> dict:
    results = [check_gwa(x) for x in labels]
    n = len(results)
    n_pass = sum(1 for r in results if r["passed"])
    rate = (n_pass / n) if n else 0.0
    return {"n": n, "n_pass": n_pass, "pass_rate": round(rate, 4),
            "gate_passed": rate >= PASS_RATE_GATE, "results": results}


if __name__ == "__main__":
    samples = [
        "정보 입수",                       # OK 명사형
        "데이터·정보 분석",                # OK
        "의사결정 및 문제해결",            # OK
        "정보를 분석한다",                 # G1 동사종결
        "각종 기계 등을 조작",             # G3 예시구
        "",                                # G2 빈
    ]
    out = check_batch_gwa(samples)
    print(f"준수율 {out['pass_rate']:.2%} (게이트 {out['gate_passed']})")
    for r in out["results"]:
        flag = "✓" if r["passed"] else "✗"
        print(f"  {flag} '{r['label']}'  위반={r['violations']} 경고={r['warnings']}")
