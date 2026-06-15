"""ksco_fetch.py 통합테스트 — 실제 pipeline.duckdb(read-only)로 D0 상속 검증.

이게 키 없이 D0 설계(세세분류 + 부모 세분류 주요업무 상속)가 실데이터에서
도는지 증명하는 핵심 테스트다.
"""
from pathlib import Path

import duckdb
import pytest

from utils import ksco_fetch as F

_DB = Path(__file__).resolve().parent.parent.parent / "results" / "pipeline.duckdb"


@pytest.fixture(scope="module")
def con():
    if not _DB.exists():
        pytest.skip(f"pipeline.duckdb 없음: {_DB}")
    c = duckdb.connect(str(_DB), read_only=True)
    yield c
    c.close()


# ── 상속: 정의 풍부한 세세분류 (28431 자동차부품) ──────────────────────────────
def test_fetch_inherits_parent_main_tasks(con):
    ctx = F.fetch_for_extraction(con, "28431")
    assert ctx["ksco_code"] == "28431"
    assert "자동차" in ctx["name"]
    assert ctx["parent_code"] == "2843"
    assert ctx["parent_name"] == "기술 영업원"
    # 부모 주요업무가 상속됨(세세분류엔 주요업무 0)
    assert ctx["parent_main_tasks_text"] not in ("", "(없음 — 직업사전 보강 후순위)")
    assert len(ctx["parent_main_tasks_text"]) > 50
    # 자기 정의는 직무특성 포함 → 저신뢰 아님
    assert ctx["low_signal"] is False


# ── 저신뢰: 이름+영문만 세세분류 (28433 의료장비) ───────────────────────────────
def test_fetch_low_signal_name_plus_english(con):
    ctx = F.fetch_for_extraction(con, "28433")
    assert "의료장비" in ctx["name"]
    # 이름+영문 정의(ASCII 과다) → 저신뢰 플래그, 상속 골격으로 동작
    assert ctx["low_signal"] is True
    # 그래도 부모 주요업무는 상속되어 빈손 아님
    assert len(ctx["parent_main_tasks_text"]) > 50


# ── 모든 세세분류는 부모 주요업무를 상속받을 수 있어야(설계 전제) ──────────────
def test_every_child_has_inheritable_parent(con):
    # 시범 도메인 28의 세세분류 일부 표본
    codes = [c for (c,) in con.execute(
        "SELECT ksco_code FROM ksco_occupation WHERE ksco_code LIKE '284%' "
        "AND length(ksco_code)=5 ORDER BY ksco_code").fetchall()]
    assert len(codes) >= 5
    for code in codes:
        ctx = F.fetch_for_extraction(con, code)
        assert ctx["parent_code"] == code[:4]
        # 부모가 존재(시범 도메인은 정의·주요업무 완비)
        assert ctx["parent_name"] != ""


# ── 없는 코드 방어 ────────────────────────────────────────────────────────────
def test_fetch_unknown_code_raises(con):
    # 'ZZZZZ'는 DB에 없는 5자리 코드(99999는 실제 KSCO 코드라 사용 불가)
    with pytest.raises(ValueError):
        F.fetch_for_extraction(con, "ZZZZZ")


def test_fetch_rejects_4digit(con):
    # 세분류(4자리)는 도출 단위가 아님
    with pytest.raises(ValueError):
        F.fetch_for_extraction(con, "2843")


# ── render_user_prompt: 상속 필드 인터폴레이션 ───────────────────────────────
def test_render_user_prompt_fills_inheritance(con):
    ctx = F.fetch_for_extraction(con, "28431")
    rendered = F.render_user_prompt(ctx)
    assert "28431" in rendered
    assert "[부모 세분류 주요 업무]" in rendered
    assert ctx["parent_main_tasks_text"][:20] in rendered
    assert "[세세분류 정의]" in rendered
    # 누락 키가 있어도 KeyError 안 남(format_map 기본값)
    assert "{" not in rendered.replace("{없음}", "")


def test_system_prompt_loads(con):
    sysp = F.load_system_prompt()
    assert "직무활동(Tasks)" in sysp
    assert "JSON 외 어떤 문자도 출력하지 않는다" in sysp


# ── iter_scope: 중분류/세분류/세세분류 ──────────────────────────────────────
def test_iter_scope_midclass_28(con):
    codes = list(F.iter_scope(con, "28"))
    assert len(codes) >= 50  # 중분류 28은 세세분류 다수
    assert all(len(c) == 5 and c.startswith("28") for c in codes)


def test_iter_scope_subclass_children(con):
    codes = list(F.iter_scope(con, "2843"))
    assert set(codes) >= {"28431", "28432", "28433"}
    assert all(c.startswith("2843") for c in codes)


def test_iter_scope_single_세세분류(con):
    assert list(F.iter_scope(con, "28120")) == ["28120"]


def test_iter_scope_dedup_multi(con):
    codes = list(F.iter_scope(con, "2843,28431"))  # 2843이 28431 포함
    assert codes.count("28431") == 1  # 중복 제거
