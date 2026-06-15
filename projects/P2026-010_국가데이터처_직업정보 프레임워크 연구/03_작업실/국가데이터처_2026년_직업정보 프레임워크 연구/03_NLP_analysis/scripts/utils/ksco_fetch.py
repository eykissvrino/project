"""KSCO 세세분류 + 부모 세분류 주요업무 상속 조회 (설계서 D0, 사양서 §1.3 v1.1).

TASK 도출 단위는 세세분류(5자리)다. 그러나 주요업무(가장 풍부한 TASK 재료)는
세분류(4자리)에만 존재(0/1,270)하므로, 부모 세분류의 정의·주요업무를 상속해
입력 컨텍스트를 구성한다(2-pass: 상속 골격 + 세세분류 특화).

    세세분류 28431 ──(parent = 앞 4자리)──▶ 세분류 2843
       │ 정의·예시 (특화 신호)                  │ 정의·주요업무 (상속 골격)
       └──────────────┬───────────────────────┘
                      ▼
          extract_tasks_user.template.md 채움

설계: 12_도출방법론_설계서.md §1·§4 ②
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Iterator

# 저신뢰 플래그 임계 (설계서 §4 ② 게이트)
# 빈약한 세세분류 정의는 두 형태로 나타난다:
#   (1) 너무 짧음 (예: 22231 "범용 소프트웨어 개발자" 40자)
#   (2) 이름+영문만 (예: 28433 "의료장비 기술 영업원 Medical and Dental ...") 72자지만 실질 정의 없음
# 길이만으로는 (2)를 못 잡으므로 ASCII(영문) 비율도 본다.
LOW_SIGNAL_DEF_LEN = 50          # (1) 길이 임계
LOW_SIGNAL_ASCII_RATIO = 0.45    # (2) 영문 과다 임계(실정의는 ASCII 거의 0)


def _ascii_ratio(text: str) -> float:
    """문자 중 ASCII 비율. 한글 정의는 ~0, 이름+영문 항목은 높음."""
    if not text:
        return 0.0
    ascii_n = sum(1 for c in text if ord(c) < 128 and not c.isspace())
    non_space = sum(1 for c in text if not c.isspace())
    return ascii_n / non_space if non_space else 0.0


def is_low_signal(definition_text: str | None) -> bool:
    """정의가 빈약(이름만/영문만)해 상속 골격에 의존해야 하는지 판정."""
    d = definition_text or ""
    if len(d) < LOW_SIGNAL_DEF_LEN:
        return True
    return _ascii_ratio(d) > LOW_SIGNAL_ASCII_RATIO

_PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"
_USER_TEMPLATE = _PROMPTS_DIR / "extract_tasks_user.template.md"
_SYSTEM_PROMPT = _PROMPTS_DIR / "extract_tasks_system.md"


def parent_code_of(ksco_code: str) -> str:
    """세세분류(5자리) → 부모 세분류(앞 4자리)."""
    return ksco_code[:4]


def fetch_for_extraction(con: Any, ksco_code: str) -> dict:
    """세세분류 1건의 추출 입력 컨텍스트(부모 상속 포함)를 구성한다.

    Args:
        con: duckdb 연결(read_only 가능)
        ksco_code: 세세분류 5자리 코드

    Returns:
        템플릿 인터폴레이션용 dict. 부모 미존재·필드 None도 방어(빈 문자열).
        low_signal=True 면 정의가 빈약(이름만)해 상속 골격 의존 + 저신뢰.

    Raises:
        ValueError: 세세분류 코드가 DB에 없을 때.
    """
    row = con.execute(
        """SELECT name, definition_text, examples_text, major_class, mid_class
           FROM ksco_occupation
           WHERE ksco_code = ? AND length(ksco_code) = 5""",
        [ksco_code],
    ).fetchone()
    if row is None:
        raise ValueError(f"세세분류 코드 없음(또는 5자리 아님): {ksco_code}")
    name, definition_text, examples_text, major_class, mid_class = row

    pcode = parent_code_of(ksco_code)
    prow = con.execute(
        """SELECT name, definition_text, main_tasks_text
           FROM ksco_occupation WHERE ksco_code = ?""",
        [pcode],
    ).fetchone()
    parent_name, parent_def, parent_main = (prow or (None, None, None))

    def_len = len(definition_text or "")
    low = is_low_signal(definition_text)
    return {
        "ksco_code": ksco_code,
        "name": name or "",
        "parent_code": pcode,
        "parent_name": parent_name or "",
        "layer": "L0",
        "source": "KSCO_HS",
        "source_subject_or_null": "null",
        "parent_definition_text": parent_def or "(없음)",
        "parent_main_tasks_text": parent_main or "(없음 — 직업사전 보강 후순위)",
        "definition_text": definition_text or "(없음)",
        "examples_text": examples_text or "(없음)",
        "major_class": major_class,
        "mid_class": mid_class,
        "low_signal": low,
        "def_len": def_len,
    }


def load_system_prompt() -> str:
    return _SYSTEM_PROMPT.read_text(encoding="utf-8")


def render_user_prompt(ctx: dict, template: str | None = None) -> str:
    """사용자 템플릿(§1.3)을 컨텍스트로 채운다. 템플릿에 없는 키는 무시.

    str.format_map + 기본값 dict로 누락 키 방어.
    """
    if template is None:
        template = _USER_TEMPLATE.read_text(encoding="utf-8")

    class _Default(dict):
        def __missing__(self, key):  # 템플릿에 있으나 ctx에 없는 키 → 빈칸
            return "(없음)"

    return template.format_map(_Default(ctx))


def iter_scope(con: Any, scope: str) -> Iterator[str]:
    """scope 문자열 → 세세분류(5자리) 코드 이터레이터.

    scope 형식 (콤마 구분 다중 허용):
      - 2자리(중분류 '28')      → 해당 중분류 하위 모든 세세분류
      - 4자리(세분류 '2843')    → 해당 세분류의 자식 세세분류
      - 5자리(세세분류 '28120') → 그 코드 1건
    """
    seen: set[str] = set()
    for token in (s.strip() for s in scope.split(",") if s.strip()):
        n = len(token)
        if n == 5:
            q = "SELECT ksco_code FROM ksco_occupation WHERE ksco_code = ? AND length(ksco_code)=5"
        elif n in (2, 4):
            q = ("SELECT ksco_code FROM ksco_occupation "
                 "WHERE ksco_code LIKE ? AND length(ksco_code)=5 ORDER BY ksco_code")
            token = token + "%"
        else:
            raise ValueError(f"scope 토큰 길이 오류(2/4/5 자리만): {token!r}")
        for (code,) in con.execute(q, [token]).fetchall():
            if code not in seen:
                seen.add(code)
                yield code
