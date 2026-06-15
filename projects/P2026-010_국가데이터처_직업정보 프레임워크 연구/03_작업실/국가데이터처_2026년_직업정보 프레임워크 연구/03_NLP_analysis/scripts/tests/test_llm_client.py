"""llm_client.py 단위테스트. 실 API 호출 없음 — _provider 주입(monkeypatch).

캐시 디렉터리는 tmp_path 로 격리해 results/cache 오염 방지.
"""
import json

import pytest

from utils import llm_client as L


@pytest.fixture(autouse=True)
def _isolate_cache(tmp_path, monkeypatch):
    monkeypatch.setattr(L, "CACHE_DIR", tmp_path / "cache")


# ── prompt_hash / cache_path ─────────────────────────────────────────────────
def test_prompt_hash_deterministic():
    h1 = L.prompt_hash("sys", "user", 0)
    h2 = L.prompt_hash("sys", "user", 0)
    assert h1 == h2 and len(h1) == 64


def test_prompt_hash_varies_by_seed():
    assert L.prompt_hash("sys", "user", 0) != L.prompt_hash("sys", "user", 1)


def test_prompt_hash_varies_by_content():
    assert L.prompt_hash("sys", "a", 0) != L.prompt_hash("sys", "b", 0)


# ── parse_json ───────────────────────────────────────────────────────────────
def test_parse_plain_json():
    assert L.parse_json('{"a": 1}') == {"a": 1}


def test_parse_json_with_code_fence():
    assert L.parse_json('```json\n{"a": 1}\n```') == {"a": 1}


def test_parse_json_with_bare_fence():
    assert L.parse_json('```\n{"a": 2}\n```') == {"a": 2}


def test_parse_json_invalid_raises():
    with pytest.raises(L.LLMError):
        L.parse_json("not json at all")


# ── call_llm: provider 주입 ──────────────────────────────────────────────────
def test_call_llm_uses_provider_and_caches():
    calls = {"n": 0}

    def fake_provider(model, system, user, temperature, seed):
        calls["n"] += 1
        return '{"tasks": [{"verb":"작성하다","object":"재무제표"}]}', 100, 50

    out = L.call_llm("claude-opus-4", "S", "U", seed=0, _provider=fake_provider)
    assert out["tasks"][0]["verb"] == "작성하다"
    assert calls["n"] == 1
    # 캐시 파일 생성됨
    assert L.cache_path("claude-opus-4", "S", "U", 0).exists()


def test_call_llm_cache_hit_skips_provider():
    def fake_provider(model, system, user, temperature, seed):
        return '{"x": 1}', 10, 5

    # 1차: 실호출 → 캐시 저장
    L.call_llm("gpt-5", "S", "U", seed=0, _provider=fake_provider)

    # 2차: provider가 호출되면 실패하도록 설정 → 캐시로만 반환되어야 함
    def boom(*a, **k):
        raise AssertionError("provider 호출되면 안 됨(캐시 적중 기대)")

    out = L.call_llm("gpt-5", "S", "U", seed=0, _provider=boom)
    assert out == {"x": 1}


def test_call_llm_retries_then_raises_on_bad_json():
    attempts = {"n": 0}

    def bad_provider(model, system, user, temperature, seed):
        attempts["n"] += 1
        return "이건 JSON 아님", 1, 1

    with pytest.raises(L.LLMError):
        L.call_llm("claude-opus-4", "S", "U", seed=0, _provider=bad_provider, use_cache=False)
    assert attempts["n"] == L.MAX_JSON_RETRIES  # 3회 재시도


def test_call_llm_recovers_on_second_attempt():
    seq = iter(["엉터리", '{"ok": true}'])

    def flaky(model, system, user, temperature, seed):
        return next(seq), 1, 1

    out = L.call_llm("claude-opus-4", "S", "U", seed=0, _provider=flaky, use_cache=False)
    assert out == {"ok": True}


# ── llm_call_log 적재 (in-memory duckdb) ─────────────────────────────────────
def test_call_llm_logs_to_duckdb():
    duckdb = pytest.importorskip("duckdb")
    con = duckdb.connect(":memory:")
    con.execute("""CREATE TABLE llm_call_log (
        call_id VARCHAR PRIMARY KEY, model VARCHAR, prompt_hash VARCHAR,
        input_tokens INTEGER, output_tokens INTEGER, temperature DOUBLE,
        seed INTEGER, called_at TIMESTAMP, cached BOOLEAN)""")

    def fake_provider(model, system, user, temperature, seed):
        return '{"ok": 1}', 123, 45

    L.call_llm("claude-opus-4", "S", "U", seed=0, con=con, _provider=fake_provider)
    rows = con.execute("SELECT model, input_tokens, output_tokens, cached FROM llm_call_log").fetchall()
    assert len(rows) == 1
    assert rows[0][0] == "claude-opus-4"
    assert rows[0][1] == 123 and rows[0][2] == 45
    assert rows[0][3] is False
