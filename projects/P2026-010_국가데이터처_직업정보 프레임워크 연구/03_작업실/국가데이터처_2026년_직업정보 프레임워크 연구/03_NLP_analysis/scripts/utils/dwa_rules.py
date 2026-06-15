"""DWA 8조항 Writing Standards 자동검증 (설계서 Stage2 §⑨와 1:1 대응).

출처: O*NET Work Activities Project 보고서 p.24 / Appendix B "DWA Writing Standards".
본 모듈은 그 8조항의 한국어판(설계서 §⑨)을 규칙으로 구현한다.

설계 원칙
- 형태소 분석기 의존 없이 표준 ``re``만 사용(경량·재현성·Windows footgun 회피).
- 조항 1·2·3·4·6·7·8 = 자동검증 대상(7개). 조항 5(명료화 형용사)는 정성 기준이라
  자동검증에서 제외하고 QC 육안 판정에 맡긴다.
- ``eight_rules_passed`` = 자동검증 대상 7개 조항을 모두 통과하면 True
  (DB ``dwa.eight_rules_passed`` 컬럼과 대응).
- 조항 8(가독성)의 한국어 지표(KOR-DALE 등)는 시범 28 단계에서 확정 예정.
  확정 전까지 어절수 상한 + 음절 휴리스틱으로 잠정 운용한다.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

# ── 조항별 검증 파라미터(설계서 §⑨ 부속 규정; 시범 28 실측으로 캘리브레이션) ──
MAX_EOJEOL = 14          # 조항8: 라벨 어절수 상한(잠정)
MAX_SYLLABLE = 45        # 조항8: 한글 음절수 상한(잠정)
MAX_LIST_ITEMS = 3       # 조항3: 가운뎃점/쉼표 나열 허용 상한

# 조항1: 활동 결합을 나타내는 연결어미(2개 이상이면 복합서술 의심)
_CONNECTIVE = re.compile(r"(하고|되고|하며|되며|하거나|되거나|한\s|하여|해서)")

# 조항2: 현재 평서형 종결 '~다'. 아래는 위반(명사형·명사화·과거·높임)
_BAD_ENDINGS = re.compile(r"(함|하기|했다|하였다|되었다|합니다|됩니다|하였음|임)$")
_PROPER_ENDING = re.compile(r"다$")

# 조항4: 금지 일반어(광의어). 문장 맨 앞 또는 나열기호 뒤에 '수식 없이' 단독 등장할
# 때만 위반으로 본다. 앞에 수식어(공백 뒤)가 붙은 "통계 자료"·"의료 장비"는 면제.
_GENERIC = re.compile(
    r"(^|[·,、])\s*(장비|자료|업무|기타|각종|여러|관련)(을|를|의|에|와|과|이|가|나)?(\s|$|[·,、])"
)

# 조항6: 예시·열거구
_EXEMPLAR = re.compile(r"(등을|등의|등에|등과|등\s|등$|와 같은|과 같은|예를 들어|가령|이를테면)")

# 조항7: 목적·결과절
_PURPOSE = re.compile(r"(하기 위하여|하기 위해|위하여|위해서|함으로써|하도록|하기 위한)")


@dataclass
class RuleCheck:
    rule: int
    name: str
    passed: bool
    detail: str


@dataclass
class DwaRuleResult:
    label: str
    checks: list[RuleCheck] = field(default_factory=list)
    eight_rules_passed: bool = False
    n_auto: int = 0          # 자동검증 대상 조항 수(=7)
    n_passed: int = 0
    pass_rate: float = 0.0

    def violations(self) -> list[RuleCheck]:
        return [c for c in self.checks if not c.passed]


def _syllables(text: str) -> int:
    return len(re.findall(r"[가-힣]", text))


def check_dwa(label: str) -> DwaRuleResult:
    """DWA 라벨 1건을 8조항으로 검증. 조항5는 자동검증 제외(정성)."""
    label = (label or "").strip()
    checks: list[RuleCheck] = []

    # 조항1 — 단일 핵심 서술어(연결어미 2개 이상이면 복합서술 경고)
    n_conn = len(_CONNECTIVE.findall(label))
    checks.append(RuleCheck(
        1, "단일 서술어", n_conn <= 1,
        f"연결어미 {n_conn}개" if n_conn <= 1 else f"연결어미 {n_conn}개(복합서술 의심)"))

    # 조항2 — 현재 평서형 종결 '~한다'
    proper = bool(_PROPER_ENDING.search(label)) and not _BAD_ENDINGS.search(label)
    checks.append(RuleCheck(
        2, "현재평서 종결", proper,
        "정상('~다' 종결)" if proper else "명사형/과거/높임 종결 위반"))

    # 조항3 — 다중객체 '및/또는', 과도 나열 금지
    n_list = label.count("·") + label.count(",") + label.count("、")
    checks.append(RuleCheck(
        3, "객체 절제", n_list < MAX_LIST_ITEMS,
        f"나열기호 {n_list}개" if n_list < MAX_LIST_ITEMS
        else f"나열기호 {n_list}개(과도 나열, '및/또는' 권장)"))

    # 조항4 — 중간 추상도 명사(금지 일반어 차단)
    m_generic = _GENERIC.search(label)
    checks.append(RuleCheck(
        4, "중간 추상도", m_generic is None,
        "정상" if m_generic is None else f"금지 일반어 '{m_generic.group(2)}'"))

    # 조항6 — 예시·열거구 금지
    m_ex = _EXEMPLAR.search(label)
    checks.append(RuleCheck(
        6, "예시구 금지", m_ex is None,
        "정상" if m_ex is None else f"예시구 '{m_ex.group(1).strip()}'"))

    # 조항7 — 목적·결과절 최소화(1개 초과 경고)
    n_purpose = len(_PURPOSE.findall(label))
    checks.append(RuleCheck(
        7, "목적절 최소", n_purpose <= 1,
        f"목적절 {n_purpose}개" if n_purpose <= 1 else f"목적절 {n_purpose}개(남용)"))

    # 조항8 — 가독성(어절수·음절수 상한; 한국어 지표는 시범 28서 확정)
    n_eojeol = len(label.split())
    n_syl = _syllables(label)
    readable = n_eojeol <= MAX_EOJEOL and n_syl <= MAX_SYLLABLE
    checks.append(RuleCheck(
        8, "가독성", readable,
        f"{n_eojeol}어절/{n_syl}음절"
        + ("" if readable else f"(상한 {MAX_EOJEOL}어절/{MAX_SYLLABLE}음절 초과)")))

    n_passed = sum(1 for c in checks if c.passed)
    n_auto = len(checks)
    return DwaRuleResult(
        label=label, checks=checks,
        eight_rules_passed=(n_passed == n_auto),
        n_auto=n_auto, n_passed=n_passed,
        pass_rate=round(n_passed / n_auto, 4) if n_auto else 0.0,
    )


def check_batch(labels: list[str]) -> tuple[list[DwaRuleResult], float]:
    """라벨 다수 검증 → (결과 리스트, 전체 준수율). 준수율 기준 §⑦: ≥0.90."""
    results = [check_dwa(x) for x in labels]
    if not results:
        return results, 0.0
    rate = sum(r.eight_rules_passed for r in results) / len(results)
    return results, round(rate, 4)


if __name__ == "__main__":
    import sys
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # Windows cp949 콘솔 대응
    except Exception:
        pass
    # 간이 자기검증(설계서 §⑨ 예시 기반)
    samples = [
        "재무 기록을 조사하여 재무제표를 작성한다",          # 적합
        "통계 자료를 분석하여 위험과 확률을 산정한다",        # 적합
        "장비를 점검한다",                                  # 조항4 위반(일반어 '장비')
        "고객 요구를 파악하고 설계하며 시공하고 검수한다",     # 조항1 위반(복합서술)
        "보고서 작성 및 제출",                              # 조항2 위반(명사형 종결)
        "효율을 높이기 위하여 비용을 절감하기 위해 공정을 개선한다",  # 조항7 위반
        "자료, 장비, 인력 등을 관리한다",                    # 조항3·4·6 위반
    ]
    for r in check_batch(samples)[0]:
        flag = "OK " if r.eight_rules_passed else "FAIL"
        print(f"[{flag}] {r.pass_rate:.2f}  {r.label}")
        for c in r.violations():
            print(f"        x 조항{c.rule}({c.name}): {c.detail}")
    print(f"\n전체 준수율: {check_batch(samples)[1]:.2%} (기준 ≥90%)")
