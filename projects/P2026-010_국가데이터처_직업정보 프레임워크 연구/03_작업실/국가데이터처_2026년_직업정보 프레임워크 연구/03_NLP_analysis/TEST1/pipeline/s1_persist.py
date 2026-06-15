"""Stage 1 — 적재: union → bge-m3 near-dup → 개수가드 → DB(트랜잭션·멱등).

설계 §4-6, ⑦·⑧-2. id 규약: task T_{code}_{seq:04d} · tool TL_{code}_{seq:04d} · wc WC_{code}_{seq:04d}.
개수 기준: 8~30 목표, 상한 40. (<8 부족 / >40 과추출 → note 기록, 적재는 유지)
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from typing import Any, Iterable

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from pipeline import s1_extract as X
from pipeline import dedup as D

MODEL = "claude-opus-4.8"
TARGET_LO, TARGET_HI, CAP = 8, 30, 40


def count_status(n: int) -> str:
    if n < TARGET_LO:
        return f"부족({n}<{TARGET_LO}) 정보부족"
    if n > CAP:
        return f"과추출({n}>{CAP}) 점검"
    if n > TARGET_HI:
        return f"상한근접({n})"
    return f"적정({n})"


def persist_one(con, code: str, result: dict, meta: dict, *, embed_fn=None) -> dict:
    """union 결과 한 건 → near-dup 병합 → task/tool_inventory/work_context 적재(멱등)."""
    deduped, _log = D.dedup_result(result, embed_fn=embed_fn)
    parent = meta.get("parent_code") or code[:4]
    low = bool(meta.get("low_signal", False))
    source = meta.get("source", "KSCO_해설서")
    source_subject = meta.get("source_subject")
    runs = deduped.get("extraction_runs", 2)
    cross = deduped.get("cross_consistency")
    tasks = deduped.get("tasks", [])
    tools = deduped.get("tools", [])
    work = deduped.get("work_context", [])
    status = count_status(len(tasks))

    con.execute("BEGIN")
    try:
        con.execute("DELETE FROM task WHERE ksco_code = ?", [code])
        con.execute("DELETE FROM tool_inventory WHERE ksco_code = ?", [code])
        con.execute("DELETE FROM work_context WHERE ksco_code = ?", [code])
        for i, t in enumerate(tasks, 1):
            con.execute(
                """INSERT INTO task
                   (task_id, ksco_code, parent_code, verb, object, full_statement,
                    source_sentence, derived_from, layer, source, source_subject,
                    confidence, extraction_runs, cross_consistency, low_signal)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                [f"T_{code}_{i:04d}", code, parent, t.get("verb"), t.get("object"),
                 t.get("full_statement"), t.get("source_sentence"), t.get("derived_from"),
                 "L0", source, source_subject,
                 t.get("confidence"), runs, cross, low])
        for i, tl in enumerate(tools, 1):
            con.execute(
                """INSERT INTO tool_inventory
                   (tool_id, ksco_code, name, canonical_name, category, evidence_span, confidence)
                   VALUES (?,?,?,?,?,?,?)""",
                [f"TL_{code}_{i:04d}", code, tl.get("name"), None, tl.get("category"),
                 tl.get("evidence_span"), tl.get("confidence")])
        for i, w in enumerate(work, 1):
            con.execute(
                """INSERT INTO work_context
                   (context_id, ksco_code, category, value, standardized, evidence_span, confidence)
                   VALUES (?,?,?,?,?,?,?)""",
                [f"WC_{code}_{i:04d}", code, w.get("category"), w.get("value"),
                 None, w.get("evidence_span"), w.get("confidence")])
        phash = hashlib.sha1((meta.get("user") or code).encode("utf-8")).hexdigest()[:12]
        con.execute(
            """INSERT INTO llm_call_log
               (call_id, model, seed, prompt_hash, cached, input_tokens, output_tokens, note)
               VALUES (?,?,?,?,?,?,?,?)""",
            [code, MODEL, None, phash, False, None, None,
             f"runs={runs} jaccard={cross} tasks={len(tasks)} {status} "
             f"tools={len(tools)} wc={len(work)}"])
        con.execute("COMMIT")
    except Exception:
        con.execute("ROLLBACK")
        raise
    return {"tasks": len(tasks), "tools": len(tools), "work_context": len(work),
            "status": status, "jaccard": cross}


def run(scope: Iterable[str] | None = None, *, runs: int = 2,
        force: bool = False, embed_fn=None) -> dict:
    """결과가 있는 scope 코드들을 적재. 반환: 요약 dict."""
    from pipeline import db, s0_preprocess as s0
    con = db.get_con()
    cache = s0._load_caches(con)
    codes = list(s0.iter_codes(con, scope))
    skip = set() if force else X.done_codes(con)

    summary = {"persisted": 0, "skipped": 0, "no_result": 0, "rows": []}
    for code in codes:
        if code in skip:
            summary["skipped"] += 1
            continue
        outs = X.load_results(code, runs=runs)
        if not outs:
            summary["no_result"] += 1
            continue
        merged = X.union_runs(outs, code)
        try:
            meta = X.read_request(code)
        except FileNotFoundError:
            rec = s0.build_record(con, code, cache)
            meta = {"parent_code": rec["broad_code"], "low_signal": rec["low_signal"],
                    "source": rec.get("source", "KSCO_해설서"), "source_subject": None}
        r = persist_one(con, code, merged, meta, embed_fn=embed_fn)
        summary["persisted"] += 1
        summary["rows"].append({"code": code, **r})
        print(f"  {code} {meta.get('name','')}: task {r['tasks']} tool {r['tools']} "
              f"wc {r['work_context']} | {r['status']} jac={r['jaccard']}")
    con.close()
    print(f"[persist] 적재 {summary['persisted']} · skip {summary['skipped']} · "
          f"결과없음 {summary['no_result']}")
    return summary


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--scope", default=None)
    ap.add_argument("--runs", type=int, default=2)
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    run(a.scope.split(",") if a.scope else None, runs=a.runs, force=a.force)
