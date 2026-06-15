"""extract_tasks.py 오프라인 테스트 — 가짜 provider + in-memory DuckDB. 키 불필요."""
import json

import duckdb
import pytest

from utils import extract_tasks as E


def _ctx(code="28431"):
    return {
        "ksco_code": code, "name": "자동차 부품 기술 영업원",
        "parent_code": code[:4], "parent_name": "기술 영업원",
        "parent_definition_text": "부모 정의", "parent_main_tasks_text": "·판매한다",
        "definition_text": "자동차 부품을 판매한다", "examples_text": "예시",
        "low_signal": False,
    }


def _payload(tasks, tools=None, ctxs=None):
    return json.dumps({
        "tasks": [{"verb": v, "object": o, "full_statement": f"{o} {v}",
                   "source_sentence": "원문"} for v, o in tasks],
        "tools": tools or [],
        "work_context": ctxs or [],
    }, ensure_ascii=False)


# ── auto_accept 경로 (seed0 == seed1) ────────────────────────────────────────
def test_extract_one_auto_accept():
    base = [("설명하다", "사양"), ("추천하다", "부품"), ("작성하다", "계약서")]

    def provider(model, system, user, temperature, seed):
        return _payload(base, tools=[{"name": "진단기", "category": "장비",
                                       "evidence_span": "진단기 사용"}],
                        ctxs=[{"category": "사회적", "value": "고객 응대",
                               "evidence_span": "고객"}]), 100, 50

    res = E.extract_one(_ctx(), provider=provider, use_cache=False)
    assert res["status"] == "auto_accept"
    assert res["extraction_runs"] == 2
    assert len(res["tasks"]) == 3
    assert res["cross_consistency"] == 1.0
    assert all(t["confidence"] == 0.95 for t in res["tasks"])
    assert len(res["tools"]) == 1 and len(res["work_context"]) == 1


# ── cross-check 경로 (seed0 != seed1 → GPT 다수결) ───────────────────────────
def test_extract_one_cross_model_vote():
    set0 = [("a", "1"), ("b", "2"), ("c", "3"), ("d", "4")]
    set1 = [("a", "1"), ("b", "2"), ("c", "3"), ("e", "5")]  # jaccard 0.6
    cross = [("a", "1"), ("b", "2"), ("c", "3"), ("d", "4")]

    def provider(model, system, user, temperature, seed):
        if "gpt" in model.lower():
            return _payload(cross), 1, 1
        return _payload(set0 if seed == 0 else set1), 1, 1

    res = E.extract_one(_ctx(), provider=provider, use_cache=False)
    assert res["status"] == "cross_model_vote"
    assert res["extraction_runs"] == 3
    keys = {(t["verb"], t["object"]) for t in res["tasks"]}
    assert {("a", "1"), ("b", "2"), ("c", "3"), ("d", "4")} == keys  # d 2표 채택, e 1표 탈락
    assert all(t["confidence"] == 0.75 for t in res["tasks"])


def test_extract_one_dedup_tools_across_runs():
    base = [("설명하다", "사양")]

    def provider(model, system, user, temperature, seed):
        # 두 run 모두 같은 도구 → dedup 후 1개
        return _payload(base, tools=[{"name": "진단기", "category": "장비"}]), 1, 1

    res = E.extract_one(_ctx(), provider=provider, use_cache=False)
    assert len(res["tools"]) == 1


# ── persist: in-memory DuckDB ────────────────────────────────────────────────
def _mem_db():
    con = duckdb.connect(":memory:")
    con.execute("""CREATE TABLE task(
        task_id VARCHAR PRIMARY KEY, ksco_code VARCHAR, parent_code VARCHAR,
        verb VARCHAR, object VARCHAR, full_statement VARCHAR, source_sentence VARCHAR,
        layer VARCHAR, source VARCHAR, source_subject VARCHAR, primary_gwa_id VARCHAR,
        confidence DOUBLE, extraction_runs INTEGER, cross_consistency DOUBLE, low_signal BOOLEAN)""")
    con.execute("""CREATE TABLE tool_inventory(
        tool_id VARCHAR PRIMARY KEY, ksco_code VARCHAR, name VARCHAR, canonical_name VARCHAR,
        category VARCHAR, evidence_span VARCHAR, extraction_runs INTEGER, confidence DOUBLE)""")
    con.execute("""CREATE TABLE work_context(
        context_id VARCHAR PRIMARY KEY, ksco_code VARCHAR, category VARCHAR, value VARCHAR,
        standardized VARCHAR, evidence_span VARCHAR, confidence DOUBLE)""")
    return con


def test_persist_inserts_rows():
    con = _mem_db()
    result = {
        "ksco_code": "28431", "parent_code": "2843", "low_signal": False,
        "extraction_runs": 2, "cross_consistency": 1.0,
        "tasks": [{"verb": "설명하다", "object": "사양", "full_statement": "사양 설명",
                   "source_sentence": "원문", "confidence": 0.95}],
        "tools": [{"name": "진단기", "category": "장비", "evidence_span": "진단기"}],
        "work_context": [{"category": "사회적", "value": "고객 응대", "evidence_span": "고객"}],
    }
    counts = E.persist(con, result)
    assert counts == {"tasks": 1, "tools": 1, "work_context": 1}
    assert con.execute("SELECT count(*) FROM task").fetchone()[0] == 1
    row = con.execute("SELECT parent_code, low_signal, extraction_runs FROM task").fetchone()
    assert row[0] == "2843" and row[1] is False and row[2] == 2
    assert con.execute("SELECT task_id FROM task").fetchone()[0] == "T_28431_0001"


def test_persist_is_idempotent():
    con = _mem_db()
    result = {
        "ksco_code": "28431", "parent_code": "2843", "low_signal": False,
        "extraction_runs": 2, "cross_consistency": 1.0,
        "tasks": [{"verb": "설명하다", "object": "사양", "full_statement": "사양 설명",
                   "source_sentence": "원문", "confidence": 0.95}],
        "tools": [], "work_context": [],
    }
    E.persist(con, result)
    E.persist(con, result)  # 재적재
    assert con.execute("SELECT count(*) FROM task").fetchone()[0] == 1  # 중복 안 됨
