"""Stage 1 단위 테스트 — LLM·임베딩 모델 없이 주입 fixture로 검증.

검증: 프롬프트 렌더 · 합집합(union) · near-dup 병합 · 개수가드 · persist 멱등/스키마.
"""
import sys
from pathlib import Path

import duckdb
import numpy as np
import pytest

TEST1 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TEST1))

from pipeline import db as DB
from pipeline import dedup as D
from pipeline import s1_extract as X
from pipeline import s1_persist as P


# ── fake 임베딩: alias 로 동의 텍스트를 같은 컬럼에 매핑 → cos=1.0 ──
def make_embed(alias=None):
    alias = alias or {}

    def embed(texts):
        keys = [alias.get(t, t) for t in texts]
        uniq = {k: i for i, k in enumerate(dict.fromkeys(keys))}
        M = np.zeros((len(texts), max(len(uniq), 1)), dtype="float32")
        for r, k in enumerate(keys):
            M[r, uniq[k]] = 1.0
        return M
    return embed


# ── 프롬프트 렌더 ────────────────────────────────────────────────────
def _rec(**kw):
    base = dict(
        ksco_code="28120", name="회계사", major_code="2", major_name="전문가",
        mid_code="28", mid_name="경영·금융", minor_code="281", minor_name="회계",
        broad_code="2812", broad_name="회계사", layer="L0", source="KSCO_해설서",
        source_subject=None, low_signal=False, main_tasks_source="세분류 상속",
        extraction_context="[세세분류 28120 회계사] 회계 업무를 수행한다.",
        main_tasks=["재무제표를 작성한다"], examples=["공인회계사"])
    base.update(kw)
    return base


def test_render_user_prompt_fills_fields():
    out = X.render_user_prompt(_rec())
    assert "28120" in out and "회계사" in out
    assert "회계 업무를 수행한다" in out          # extraction_context 투입
    assert "재무제표를 작성한다" in out            # 상속 주요업무
    assert "세분류 상속" in out                    # 출처분기 노출


def test_render_handles_none_source_subject_and_empty_lists():
    out = X.render_user_prompt(_rec(source_subject=None, main_tasks=[], examples=[]))
    assert "(없음)" in out


# ── 합집합(union) ────────────────────────────────────────────────────
def _t(verb, obj, stmt=None):
    return {"verb": verb, "object": obj,
            "full_statement": stmt or f"{obj}를 {verb}", "source_sentence": "원문",
            "derived_from": "세세분류 정의"}


def test_union_runs_is_union_not_intersection():
    out1 = {"tasks": [_t("작성", "재무제표"), _t("분석", "재무제표")]}
    out2 = {"tasks": [_t("작성", "재무제표"), _t("감사", "재무회계")]}
    merged = X.union_runs([out1, out2], "28120")
    keys = {(t["verb"], t["object"]) for t in merged["tasks"]}
    assert keys == {("작성", "재무제표"), ("분석", "재무제표"), ("감사", "재무회계")}  # 합집합 3개


def test_union_confidence_and_jaccard():
    out1 = {"tasks": [_t("작성", "재무제표"), _t("분석", "재무제표")]}
    out2 = {"tasks": [_t("작성", "재무제표")]}
    merged = X.union_runs([out1, out2], "28120")
    conf = {(t["verb"], t["object"]): t["confidence"] for t in merged["tasks"]}
    assert conf[("작성", "재무제표")] == X.CONF_BOTH      # 둘다 출현 → 높은 conf
    assert conf[("분석", "재무제표")] == X.CONF_ONE       # 1회만 → 낮은 conf
    assert merged["cross_consistency"] == pytest.approx(1 / 2)  # jaccard 1/2
    assert merged["extraction_runs"] == 2


def test_union_dedups_tools_and_context():
    out1 = {"tasks": [], "tools": [{"name": "전산회계시스템"}],
            "work_context": [{"category": "장소", "value": "사무실"}]}
    out2 = {"tasks": [], "tools": [{"name": "전산회계시스템"}, {"name": "ERP"}],
            "work_context": [{"category": "장소", "value": "사무실"}]}
    merged = X.union_runs([out1, out2], "28120")
    assert {t["name"] for t in merged["tools"]} == {"전산회계시스템", "ERP"}
    assert len(merged["work_context"]) == 1


# ── near-dup 병합 ────────────────────────────────────────────────────
def test_merge_near_dup_merges_paraphrases_keeps_high_conf():
    items = [
        {"full_statement": "재무제표를 작성한다", "confidence": 0.8},
        {"full_statement": "재무제표 및 보고서를 작성한다", "confidence": 0.95},  # 의역
        {"full_statement": "세무조정 계산서를 작성한다", "confidence": 0.9},      # 별개
    ]
    alias = {"재무제표 및 보고서를 작성한다": "재무제표를 작성한다"}  # 두 의역을 같은 군집으로
    kept, log = D.merge_near_dup(items, "full_statement", embed_fn=make_embed(alias))
    stmts = [k["full_statement"] for k in kept]
    assert len(kept) == 2
    assert "세무조정 계산서를 작성한다" in stmts
    # 대표는 confidence 높은 의역본
    assert "재무제표 및 보고서를 작성한다" in stmts
    assert len(log) == 1 and log[0]["cosine"] == pytest.approx(1.0)


def test_merge_near_dup_singleton_noop():
    items = [{"full_statement": "혼자", "confidence": 0.9}]
    kept, log = D.merge_near_dup(items, "full_statement", embed_fn=make_embed())
    assert kept == items and log == []


# ── 개수가드 ─────────────────────────────────────────────────────────
@pytest.mark.parametrize("n,expect", [
    (3, "부족"), (8, "적정"), (20, "적정"), (30, "적정"), (35, "상한근접"), (45, "과추출")])
def test_count_status(n, expect):
    assert P.count_status(n).startswith(expect)


# ── persist 멱등 + 스키마 ────────────────────────────────────────────
@pytest.fixture
def con():
    c = duckdb.connect(":memory:")
    c.execute(DB.KSCO_SCHEMA_SQL)
    c.execute(DB.SCHEMA_SQL)
    yield c
    c.close()


def _result():
    return {
        "ksco_code": "28120",
        "tasks": [_t("작성", "재무제표", "재무제표를 작성한다"),
                  _t("분석", "재무제표", "재무제표를 분석한다")],
        "tools": [{"name": "전산회계시스템", "category": "시스템", "evidence_span": "근거"}],
        "work_context": [{"category": "장소", "value": "사무실", "evidence_span": "근거"}],
        "extraction_runs": 2, "cross_consistency": 1.0,
    }


def _meta():
    return {"parent_code": "2812", "low_signal": False,
            "source": "KSCO_해설서", "source_subject": None, "user": "프롬프트"}


def test_persist_one_inserts_rows(con):
    r = P.persist_one(con, "28120", _result(), _meta(), embed_fn=make_embed())
    assert r["tasks"] == 2 and r["tools"] == 1 and r["work_context"] == 1
    assert con.execute("SELECT COUNT(*) FROM task WHERE ksco_code='28120'").fetchone()[0] == 2
    row = con.execute(
        "SELECT verb, object, source_sentence, derived_from, source, extraction_runs, "
        "cross_consistency FROM task WHERE task_id='T_28120_0001'").fetchone()
    assert row[0] == "작성" and row[2] == "원문" and row[3] == "세세분류 정의"
    assert row[4] == "KSCO_해설서" and row[5] == 2 and row[6] == 1.0
    # llm_call_log 기록
    assert con.execute("SELECT COUNT(*) FROM llm_call_log WHERE call_id='28120'").fetchone()[0] == 1


def test_persist_one_is_idempotent(con):
    P.persist_one(con, "28120", _result(), _meta(), embed_fn=make_embed())
    P.persist_one(con, "28120", _result(), _meta(), embed_fn=make_embed())  # 재적재
    assert con.execute("SELECT COUNT(*) FROM task WHERE ksco_code='28120'").fetchone()[0] == 2


def test_persist_applies_near_dup(con):
    res = _result()
    res["tasks"].append(_t("작성", "재무제표및보고서", "재무제표 및 보고서를 작성한다"))
    alias = {"재무제표 및 보고서를 작성한다": "재무제표를 작성한다"}
    r = P.persist_one(con, "28120", res, _meta(), embed_fn=make_embed(alias))
    assert r["tasks"] == 2  # 3 → near-dup 병합 → 2
