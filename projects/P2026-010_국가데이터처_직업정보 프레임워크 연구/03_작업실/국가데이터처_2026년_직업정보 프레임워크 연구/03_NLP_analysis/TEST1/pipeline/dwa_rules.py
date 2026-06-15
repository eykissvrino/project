"""Stage 2 — DWA 8조항 자동검증 (설계 §⑨와 1:1 대응).

O*NET DWA Writing Standards 8조항의 한국어판을 형태소/정규식 휴리스틱으로 검사한다.
정성 조항(5: 변별 한정수식)은 자동검증에서 제외(QC 육안).

사용:
    from pipeline.dwa_rules import check_dwa, check_batch
    r = check_dwa("재무기록을 조사하여 재무제표를 작성한다")
    # r = {"passed": bool, "violations": [...], "rules": {r1:bool, ...}}
"""
from __future__ import annotations

import re

# ── 조항 4: 금지 일반어(중간 추상도 위반 = 광의 일반어) ──────────────
# 맨(수식·복합어 없는) 일반명사만 위반. 복합어(운송장비·기계장비·검사자료)나
# 수식된 머리명사(분무 장비·시장 자료)는 통과 — 단어경계로 판별.
BROAD_NOUNS = ["장비", "자료", "업무", "기타", "각종", "제반", "전반", "여러 가지"]
# 항상 위반(맥락 무관 광의어)
BROAD_ALWAYS = ["각종", "제반", "전반", "여러 가지", "기타", "일반적인",
                "관련 일", "관련 업무", "해당 업무"]
_PARTICLE = "을를이가은는에의로"           # 목적/주격 조사 → 바로 앞이 머리명사
_CONJ = ("및", "또는", "그리고")            # 등위접속 → 뒤 명사는 맨명사로 간주


def _r4_violations(s: str) -> list[str]:
    """광의 일반어를 '맨 머리명사'로 쓴 경우만 위반(복합어·수식어 통과)."""
    import re as _re
    hits = []
    for noun in BROAD_ALWAYS:
        if noun in s:
            hits.append(noun)
    for noun in ["장비", "자료", "업무"]:
        for m in _re.finditer(_re.escape(noun), s):
            i, j = m.start(), m.end()
            # 1) 바로 앞이 한글 → 복합어 일부(운송장비·검사자료) → 통과
            if i > 0 and "가" <= s[i - 1] <= "힣":
                continue
            # 2) 바로 뒤가 조사가 아니면 머리명사 아님(업무 기록=수식어) → 통과
            if j >= len(s) or s[j] not in _PARTICLE:
                continue
            # 3) 앞에 수식 명사가 있으면(분무 장비·시장 자료) 통과 — 단 '및/또는' 등위는 맨명사
            prev = s[:i].rstrip()
            if prev and "가" <= prev[-1] <= "힣" and not prev.endswith(_CONJ):
                continue
            hits.append(noun)
            break
    return sorted(set(hits))
# ── 조항 6: 예시·열거구 ──────────────────────────────────────────────
EXAMPLE_PATTERNS = [
    r"등을", r"등의", r"등에", r"등\s*$", r"등\)", r"와 같은", r"과 같은",
    r"예를\s*들어", r"가령", r"및\s*기타", r"따위",
]
# ── 조항 7: 목적·결과절 ──────────────────────────────────────────────
PURPOSE_PATTERNS = [r"하기\s*위하여", r"하기\s*위해", r"위하여", r"위해서",
                    r"함으로써", r"하도록", r"하기\s*위한"]
# ── 조항 2: 금지 종결/형태 ───────────────────────────────────────────
HONORIFIC = [r"합니다$", r"습니다$", r"입니다$"]
PAST = [r"하였다$", r"했다$", r"되었다$", r"였다$"]
NOMINAL_END = [r"하기$", r"함$", r"임$", r"기$"]
# ── 조항 1: 연결어미(활동 2개 이상 잇기) ─────────────────────────────
CONJ_ENDINGS = [r"하고\s", r"하며\s", r"하거나\s", r"한\s*뒤\s", r"한\s*후\s",
                r"하여\s+.*하여\s"]

# ── 길이(조항 8) ─────────────────────────────────────────────────────
MAX_EOJEOL = 25            # 권고 어절 상한
MULTI_OBJ_COMMA = 3        # 조항 3: 쉼표 나열 경고 임계

PASS_RATE_GATE = 0.90      # §⑦ 준수율 기준


def _eojeol(s: str) -> int:
    return len([w for w in re.split(r"\s+", s.strip()) if w])


def normalize_label(label: str) -> str:
    """말미 마침표·공백 제거(종결 '~한다' 일관화). DWA 라벨은 종지부 없이 저장."""
    return (label or "").strip().rstrip(" .。·")


def check_dwa(label: str) -> dict:
    """DWA label 1건 8조항 검사. passed = 모든 '하드' 조항 통과."""
    s = normalize_label(label)
    v: list[str] = []          # 위반(하드)
    w: list[str] = []          # 경고(소프트)
    rules: dict[str, bool] = {}

    # 조항 2: 현재 평서형 '~다' 종결
    r2 = s.endswith("다")
    if not r2:
        v.append("R2: '~다' 종결 아님")
    for pat in HONORIFIC:
        if re.search(pat, s):
            r2 = False; v.append("R2: 높임형 종결('~합니다')")
            break
    for pat in PAST:
        if re.search(pat, s):
            r2 = False; v.append("R2: 과거형 종결('~했다/하였다')")
            break
    for pat in NOMINAL_END:
        if re.search(pat, s):
            r2 = False; v.append("R2: 명사형 종결('~하기/함')")
            break
    rules["R2_종결어미"] = r2

    # 조항 1: 단일 핵심 서술어 — 종결 '~다' 1개 + 연결어미 과다 금지
    conj = sum(1 for pat in CONJ_ENDINGS if re.search(pat, s))
    # '~하여/~하고'가 2회 이상이면 활동 다중 결합 의심
    link_count = len(re.findall(r"(하여|하고|하며|하거나)", s))
    r1 = link_count < 2
    if not r1:
        v.append(f"R1: 연결어미 {link_count}개(활동 다중 결합 의심)")
    rules["R1_단일서술어"] = r1

    # 조항 3: 다중객체 쉼표 나열 경고
    commas = s.count(",") + s.count("、") + s.count("·")
    r3 = commas < MULTI_OBJ_COMMA
    if not r3:
        w.append(f"R3: 쉼표/나열 {commas}개(병렬객체는 '및/또는' 권장)")
    rules["R3_객체절제"] = r3

    # 조항 4: 금지 일반어(맨 머리명사만 — 복합어·수식어 통과)
    hit4 = _r4_violations(s)
    r4 = not hit4
    if not r4:
        v.append(f"R4: 광의 일반어 {hit4}")
    rules["R4_중간추상도"] = r4

    # 조항 6: 예시·열거구
    hit6 = [p for p in EXAMPLE_PATTERNS if re.search(p, s)]
    r6 = not hit6
    if not r6:
        v.append("R6: 예시·열거구('~등/~와 같은')")
    rules["R6_예시금지"] = r6

    # 조항 7: 목적·결과절 1개 초과 경고
    p7 = sum(1 for p in PURPOSE_PATTERNS if re.search(p, s))
    r7 = p7 <= 1
    if not r7:
        w.append(f"R7: 목적절 {p7}개(최소화 권장)")
    rules["R7_목적절최소"] = r7

    # 조항 8: 가독성(어절 상한 휴리스틱)
    n_eoj = _eojeol(s)
    r8 = 0 < n_eoj <= MAX_EOJEOL
    if n_eoj == 0:
        v.append("R8: 빈 라벨")
    elif n_eoj > MAX_EOJEOL:
        w.append(f"R8: {n_eoj}어절(권고 {MAX_EOJEOL} 초과)")
    rules["R8_가독성"] = r8

    # 하드 조항(재작성 트리거): R1·R2·R4·R6·R8(빈/0어절). 소프트(R3·R7·R8길이)는 경고만.
    hard_ok = r1 and r2 and r4 and r6 and (n_eoj > 0)
    return {
        "label": s,
        "passed": hard_ok,
        "violations": v,
        "warnings": w,
        "rules": rules,
        "eojeol": n_eoj,
    }


def check_batch(labels: list[str]) -> dict:
    """라벨 리스트 일괄 검사 + 준수율(§⑦ ≥0.90 게이트)."""
    results = [check_dwa(x) for x in labels]
    n = len(results)
    n_pass = sum(1 for r in results if r["passed"])
    rate = (n_pass / n) if n else 0.0
    return {
        "n": n, "n_pass": n_pass, "pass_rate": round(rate, 4),
        "gate_passed": rate >= PASS_RATE_GATE,
        "results": results,
    }


if __name__ == "__main__":
    samples = [
        "재무기록을 조사하여 재무제표를 작성한다",          # OK
        "고객을 응대하고 상품을 판매하며 재고를 관리한다",   # R1 다중
        "각종 장비를 점검한다",                              # R4 일반어
        "환자에게 투약하기 위해 처방전을 확인한다",          # R7 목적
        "보고서 작성",                                       # R2 명사형
        "기계 등을 정비한다",                                # R6 예시구
    ]
    out = check_batch(samples)
    print(f"준수율 {out['pass_rate']:.2%} (게이트 {out['gate_passed']})")
    for r in out["results"]:
        flag = "✓" if r["passed"] else "✗"
        print(f"  {flag} {r['label']}  위반={r['violations']} 경고={r['warnings']}")
