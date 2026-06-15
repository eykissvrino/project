"""LLM 통합 호출 + 캐시 + llm_call_log (사양서 §0.3, §1.1, Sprint1 Step3).

재현성 계약(설계서 D5): 모든 호출은 temperature=0, seed 고정, 캐시·로그된다.

    call_llm(model, system, user, seed) ─┬─ 캐시 적중 ─▶ 캐시 JSON 반환 (호출 0회)
                                         └─ 미적중 ─▶ _provider_call ─▶ JSON 파싱(재시도 3회)
                                                       ─▶ 캐시 저장 + llm_call_log 적재

실 API 호출은 `_provider_call` 한 곳에 격리 → 키 없이 단위테스트 시 monkeypatch 가능.
캐시 경로: 03_NLP_analysis/results/cache/{model}_{prompt_hash}.json
"""
from __future__ import annotations

import hashlib
import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

# 경로: utils/ → scripts/ → 03_NLP_analysis/ → results/cache
_SCRIPTS_DIR = Path(__file__).resolve().parent.parent
CACHE_DIR = _SCRIPTS_DIR.parent / "results" / "cache"

try:
    from dotenv import load_dotenv

    # 실행 위치(cwd)와 무관하게 scripts/.env 를 명시적으로 로드
    load_dotenv(_SCRIPTS_DIR / ".env")
except Exception:  # dotenv 미설치 환경도 동작
    pass

MAX_JSON_RETRIES = 3


class LLMError(RuntimeError):
    """LLM 호출/파싱 실패. 휴리스틱 수정 금지(사양서 작업원칙 4) → 호출자에 raise."""


# ── 해시·캐시 ────────────────────────────────────────────────────────────────
def prompt_hash(system: str, user: str, seed: int) -> str:
    """SHA256(system + user + seed) (사양서 §0.3). temperature는 항상 0 전제."""
    h = hashlib.sha256()
    h.update(system.encode("utf-8"))
    h.update(b"\x00")
    h.update(user.encode("utf-8"))
    h.update(b"\x00")
    h.update(str(seed).encode("utf-8"))
    return h.hexdigest()


def _safe_model_name(model: str) -> str:
    """파일명 안전화 (슬래시·콜론 제거)."""
    return "".join(c if c.isalnum() or c in "-_." else "_" for c in model)


def cache_path(model: str, system: str, user: str, seed: int) -> Path:
    return CACHE_DIR / f"{_safe_model_name(model)}_{prompt_hash(system, user, seed)}.json"


# ── JSON 파싱 ────────────────────────────────────────────────────────────────
def parse_json(text: str) -> Any:
    """LLM 텍스트 → JSON. 코드펜스(```json ... ```) 제거 후 파싱. 실패 시 LLMError."""
    if text is None:
        raise LLMError("LLM 응답이 None")
    t = text.strip()
    if t.startswith("```"):
        # ```json 또는 ``` 펜스 제거
        t = t.split("\n", 1)[1] if "\n" in t else t
        if t.rstrip().endswith("```"):
            t = t.rstrip()[:-3]
    t = t.strip()
    try:
        return json.loads(t)
    except json.JSONDecodeError as e:
        raise LLMError(f"JSON 파싱 실패: {e}") from e


# ── 제공자 호출 (격리: 테스트 시 monkeypatch) ───────────────────────────────────
def _provider_call(
    model: str, system: str, user: str, temperature: float, seed: int
) -> tuple[str, int, int]:
    """실제 API 호출. 반환 (text, input_tokens, output_tokens).

    model 명에 'gpt'가 포함되면 OpenAI, 아니면 Anthropic으로 라우팅.
    이 함수는 키가 필요하므로 단위테스트에서는 monkeypatch 한다.
    """
    is_openai = "gpt" in model.lower()
    if is_openai:
        from openai import OpenAI

        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        resp = client.chat.completions.create(
            model=os.environ.get("OPENAI_MODEL", model),
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=temperature,
            seed=seed,
            response_format={"type": "json_object"},
        )
        text = resp.choices[0].message.content
        usage = resp.usage
        return text, getattr(usage, "prompt_tokens", 0), getattr(usage, "completion_tokens", 0)

    from anthropic import Anthropic

    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    resp = client.messages.create(
        model=os.environ.get("ANTHROPIC_MODEL", model),
        max_tokens=4096,
        temperature=temperature,
        system=system + "\n\n반드시 JSON만 출력한다. 코드펜스·설명 금지.",
        messages=[{"role": "user", "content": user}],
    )
    text = "".join(block.text for block in resp.content if getattr(block, "type", "") == "text")
    usage = resp.usage
    return text, getattr(usage, "input_tokens", 0), getattr(usage, "output_tokens", 0)


# ── llm_call_log ────────────────────────────────────────────────────────────
def _log_call(con, *, call_id, model, p_hash, in_tok, out_tok, temperature, seed, cached):
    if con is None:
        return
    con.execute(
        """INSERT INTO llm_call_log
           (call_id, model, prompt_hash, input_tokens, output_tokens,
            temperature, seed, called_at, cached)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        [call_id, model, p_hash, in_tok, out_tok, temperature, seed,
         datetime.now(timezone.utc), cached],
    )


# ── 공개 API ─────────────────────────────────────────────────────────────────
def call_llm(
    model: str,
    system: str,
    user: str,
    temperature: float = 0.0,
    seed: int = 0,
    con: Any = None,
    use_cache: bool = True,
    _provider: Callable[..., tuple[str, int, int]] | None = None,
) -> dict:
    """LLM 1회 호출. 캐시 우선, JSON 강제(재시도 3회), llm_call_log 적재.

    Args:
        model: 'claude-opus-4' / 'gpt-5' 등 (provider는 'gpt' 포함 여부로 판정)
        con: duckdb 연결(있으면 호출 로그 적재). None이면 로그 생략.
        _provider: 테스트용 주입. None이면 _provider_call 사용.

    Returns:
        파싱된 JSON dict.

    Raises:
        LLMError: 3회 재시도 후에도 JSON 파싱 실패(휴리스틱 수정 금지).
    """
    provider = _provider or _provider_call
    p_hash = prompt_hash(system, user, seed)
    cpath = cache_path(model, system, user, seed)

    # 1) 캐시 적중
    if use_cache and cpath.exists():
        data = json.loads(cpath.read_text(encoding="utf-8"))
        _log_call(con, call_id=f"{p_hash[:16]}_{seed}_c_{uuid.uuid4().hex[:8]}", model=model,
                  p_hash=p_hash, in_tok=0, out_tok=0, temperature=temperature, seed=seed, cached=True)
        return data

    # 2) 실호출 + JSON 파싱 재시도
    last_err: Exception | None = None
    for attempt in range(MAX_JSON_RETRIES):
        text, in_tok, out_tok = provider(model, system, user, temperature, seed)
        try:
            data = parse_json(text)
            break
        except LLMError as e:
            last_err = e
            continue
    else:
        raise LLMError(
            f"{model} JSON 파싱 {MAX_JSON_RETRIES}회 실패: {last_err}"
        )

    # 3) 캐시 저장 + 로그
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cpath.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    _log_call(con, call_id=f"{p_hash[:16]}_{seed}_{uuid.uuid4().hex[:8]}", model=model,
              p_hash=p_hash, in_tok=in_tok, out_tok=out_tok, temperature=temperature,
              seed=seed, cached=False)
    return data
