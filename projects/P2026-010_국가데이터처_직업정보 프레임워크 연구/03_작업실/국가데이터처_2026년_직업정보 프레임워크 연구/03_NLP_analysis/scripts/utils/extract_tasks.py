"""TASK 3차원 추출 오케스트레이션 (사양서 §1, 설계서 §4 ②). Sprint 2 코어.

    fetch_for_extraction(세세분류) ─▶ 2회 독립 호출(seed 0·1)
       ─▶ self_consistency ─┬─ 일치 ─▶ 채택
                            └─ 불일치 ─▶ GPT-5 cross ─▶ 다수결
       ─▶ persist: task / tool_inventory / work_context 적재

LLM 호출은 llm_client.call_llm 경유(캐시·로그). provider 주입으로 오프라인 테스트 가능.
"""
from __future__ import annotations

from typing import Any, Callable

from . import consistency as C
from . import ksco_fetch as F
from .llm_client import call_llm

MODEL_PRIMARY = "claude-opus-4"
MODEL_CROSS = "gpt-5"


def _dedup_tools(*outs: dict) -> list[dict]:
    """tools 합집합(name 기준 dedup, 첫 등장 우선)."""
    seen, result = set(), []
    for out in outs:
        for t in out.get("tools") or []:
            key = (t.get("name") or "").strip()
            if key and key not in seen:
                seen.add(key)
                result.append(t)
    return result


def _dedup_context(*outs: dict) -> list[dict]:
    """work_context 합집합((category,value) 기준 dedup)."""
    seen, result = set(), []
    for out in outs:
        for w in out.get("work_context") or []:
            key = ((w.get("category") or "").strip(), (w.get("value") or "").strip())
            if key != ("", "") and key not in seen:
                seen.add(key)
                result.append(w)
    return result


def extract_one(
    ctx: dict,
    *,
    model_primary: str = MODEL_PRIMARY,
    model_cross: str = MODEL_CROSS,
    provider: Callable[..., tuple[str, int, int]] | None = None,
    con: Any = None,
    use_cache: bool = True,
) -> dict:
    """세세분류 1건 추출 + self-consistency 판정. DB 적재는 하지 않는다(persist 분리).

    Args:
        ctx: ksco_fetch.fetch_for_extraction 결과(상속 컨텍스트).
        provider: 테스트용 LLM 주입. None이면 실제 호출(키 필요).
        con: llm_call_log 적재용(선택).

    Returns:
        {ksco_code, parent_code, tasks, tools, work_context,
         cross_consistency, extraction_runs, status, low_signal}
    """
    system = F.load_system_prompt()
    user = F.render_user_prompt(ctx)

    out1 = call_llm(model_primary, system, user, seed=0, con=con,
                    use_cache=use_cache, _provider=provider)
    out2 = call_llm(model_primary, system, user, seed=1, con=con,
                    use_cache=use_cache, _provider=provider)

    accepted, jac, status = C.self_consistency(out1, out2)
    runs = 2
    pool = [out1, out2]

    if status == "cross_check_required":
        out3 = call_llm(model_cross, system, user, seed=0, con=con,
                        use_cache=use_cache, _provider=provider)
        accepted, status = C.cross_model_vote(out1, out2, out3)
        runs = 3
        pool = [out1, out2, out3]

    return {
        "ksco_code": ctx["ksco_code"],
        "parent_code": ctx["parent_code"],
        "tasks": accepted,
        "tools": _dedup_tools(*pool),
        "work_context": _dedup_context(*pool),
        "cross_consistency": jac,
        "extraction_runs": runs,
        "status": status,
        "low_signal": ctx.get("low_signal", False),
    }


def persist(con: Any, result: dict) -> dict:
    """추출 결과를 task / tool_inventory / work_context 에 적재(트랜잭션).

    id 규약(사양서 §1.5): task → T_{code}_{seq:04d}, tool → TL_{code}_{seq}, ctx → WC_{code}_{seq}.
    반복 적재 안전: 같은 ksco_code 기존 행 삭제 후 재적재(idempotent).

    Returns: {"tasks": n, "tools": n, "work_context": n}
    """
    code = result["ksco_code"]
    parent = result.get("parent_code")
    low = bool(result.get("low_signal", False))
    runs = result.get("extraction_runs", 2)
    cross = result.get("cross_consistency")

    con.execute("BEGIN")
    try:
        con.execute("DELETE FROM task WHERE ksco_code = ?", [code])
        con.execute("DELETE FROM tool_inventory WHERE ksco_code = ?", [code])
        con.execute("DELETE FROM work_context WHERE ksco_code = ?", [code])

        for i, t in enumerate(result["tasks"], 1):
            con.execute(
                """INSERT INTO task
                   (task_id, ksco_code, parent_code, verb, object, full_statement,
                    source_sentence, layer, source, source_subject,
                    primary_gwa_id, confidence, extraction_runs, cross_consistency, low_signal)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                [f"T_{code}_{i:04d}", code, parent, t.get("verb"), t.get("object"),
                 t.get("full_statement"), t.get("source_sentence"), "L0", "KSCO_HS", None,
                 None, t.get("confidence"), runs, cross, low],
            )
        for i, tl in enumerate(result["tools"], 1):
            con.execute(
                """INSERT INTO tool_inventory
                   (tool_id, ksco_code, name, canonical_name, category,
                    evidence_span, extraction_runs, confidence)
                   VALUES (?,?,?,?,?,?,?,?)""",
                [f"TL_{code}_{i:04d}", code, tl.get("name"), None, tl.get("category"),
                 tl.get("evidence_span"), runs, None],
            )
        for i, w in enumerate(result["work_context"], 1):
            con.execute(
                """INSERT INTO work_context
                   (context_id, ksco_code, category, value, standardized, evidence_span, confidence)
                   VALUES (?,?,?,?,?,?,?)""",
                [f"WC_{code}_{i:04d}", code, w.get("category"), w.get("value"),
                 None, w.get("evidence_span"), None],
            )
        con.execute("COMMIT")
    except Exception:
        con.execute("ROLLBACK")
        raise

    return {"tasks": len(result["tasks"]),
            "tools": len(result["tools"]),
            "work_context": len(result["work_context"])}
