"""Stage 1 — TASK 추출 입출력 스캐폴딩 (무-API · Opus 서브에이전트 방식).

설계: stages/Stage1_TASK_도출_설계.md · 핸드오프: stages/07_Stage1_TASK추출_핸드오프.md

흐름(LLM 호출은 API가 아니라 Claude Code Opus 서브에이전트가 담당):
    build_requests(scope)  ─▶ S0 build_record로 코드별 입력 렌더 → cache/s1_requests/{code}.json
    [Opus 서브에이전트 2회 독립 추출]      → cache/s1_results/{code}_run{n}.json
    load_results + union_runs(scope)       → 2회 합집합(둘다출현→confidence↑, jaccard 기록)
    (이후 s1_persist 가 dedup·개수가드·DB적재)

본 모듈은 순수 IO·집합연산만. 임베딩·DB적재는 dedup.py·s1_persist.py 가 담당.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Iterable

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

TEST1_DIR = Path(__file__).resolve().parents[1]
PROMPTS = TEST1_DIR / "prompts"
CACHE = TEST1_DIR / "cache"
REQ_DIR = CACHE / "s1_requests"
RES_DIR = CACHE / "s1_results"

CONF_BOTH = 0.95   # 2회 모두 출현
CONF_ONE = 0.80    # 1회만 출현


# ── 프롬프트 렌더 ────────────────────────────────────────────────────
def load_system_prompt() -> str:
    return (PROMPTS / "extract_tasks_system.md").read_text(encoding="utf-8")


def _user_template() -> str:
    return (PROMPTS / "extract_tasks_user.template.md").read_text(encoding="utf-8")


def render_user_prompt(rec: dict) -> str:
    """S0 build_record 한 건 → 사용자 프롬프트 문자열."""
    main_tasks_text = "\n".join(f"- {t}" for t in rec.get("main_tasks", [])) or "(없음)"
    examples_text = "\n".join(f"- {e}" for e in rec.get("examples", [])) or "(없음)"
    return _user_template().format(
        ksco_code=rec["ksco_code"], name=rec["name"],
        major_code=rec["major_code"], major_name=rec["major_name"],
        mid_code=rec["mid_code"], mid_name=rec["mid_name"],
        minor_code=rec["minor_code"], minor_name=rec["minor_name"],
        broad_code=rec["broad_code"], broad_name=rec["broad_name"],
        layer=rec.get("layer", "L0"), source=rec.get("source", "KSCO_해설서"),
        source_subject=rec.get("source_subject") or "(없음)",
        low_signal=rec.get("low_signal", False),
        main_tasks_source=rec.get("main_tasks_source", ""),
        extraction_context=rec.get("extraction_context", ""),
        main_tasks_text=main_tasks_text, examples_text=examples_text,
    )


# ── 체크포인트 ───────────────────────────────────────────────────────
def done_codes(con) -> set[str]:
    """이미 task 적재된 세세분류(재개 시 skip)."""
    return {r[0] for r in con.execute("SELECT DISTINCT ksco_code FROM task").fetchall()}


# ── build_requests ───────────────────────────────────────────────────
def build_requests(scope: Iterable[str] | None = None, *, force: bool = False) -> list[str]:
    """scope 코드별 추출 요청(JSON) 생성. 반환: 생성된 코드 리스트."""
    from pipeline import db, s0_preprocess as s0
    REQ_DIR.mkdir(parents=True, exist_ok=True)
    con = db.get_con(read_only=True)
    cache = s0._load_caches(con)
    codes = list(s0.iter_codes(con, scope))
    skip = set() if force else done_codes(con)

    system = load_system_prompt()
    written = []
    for code in codes:
        if code in skip:
            continue
        rec = s0.build_record(con, code, cache)
        payload = {
            "ksco_code": code,
            "name": rec["name"],
            "parent_code": rec["broad_code"],
            "main_tasks_source": rec["main_tasks_source"],
            "low_signal": rec["low_signal"],
            "valid": rec["valid"],
            "source": rec.get("source", "KSCO_해설서"),
            "source_subject": rec.get("source_subject"),
            "system": system,
            "user": render_user_prompt(rec),
        }
        (REQ_DIR / f"{code}.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        written.append(code)
    con.close()
    print(f"[build-requests] {len(written)}건 생성 → {REQ_DIR.relative_to(TEST1_DIR)} "
          f"(skip {len(codes) - len(written)})")
    return written


def read_request(code: str) -> dict:
    return json.loads((REQ_DIR / f"{code}.json").read_text(encoding="utf-8"))


# ── 결과 수합 + 합집합 ───────────────────────────────────────────────
def _norm(s) -> str:
    return " ".join(str(s).split()) if s is not None else ""


def task_key(t: dict) -> tuple[str, str]:
    return (_norm(t.get("verb")), _norm(t.get("object")))


def jaccard(s1: set, s2: set) -> float:
    if not s1 and not s2:
        return 1.0
    u = s1 | s2
    return len(s1 & s2) / len(u) if u else 1.0


def load_results(code: str, runs: int = 2) -> list[dict]:
    """{code}_run{n}.json 들을 읽어 반환(존재하는 것만)."""
    outs = []
    for n in range(1, runs + 1):
        p = RES_DIR / f"{code}_run{n}.json"
        if p.exists():
            outs.append(json.loads(p.read_text(encoding="utf-8")))
    return outs


def union_runs(outs: list[dict], code: str) -> dict:
    """2회(이상) 합집합. (verb,object)로 dedup, 둘다출현→conf↑. jaccard 기록."""
    sets = [{task_key(t) for t in (o.get("tasks") or [])} for o in outs]
    cross = jaccard(sets[0], sets[1]) if len(sets) >= 2 else (1.0 if outs else 0.0)

    merged: dict[tuple, dict] = {}
    counts: dict[tuple, int] = {}
    for o in outs:
        seen = set()
        for t in o.get("tasks") or []:
            k = task_key(t)
            if k == ("", "") or k in seen:
                continue
            seen.add(k)
            counts[k] = counts.get(k, 0) + 1
            merged.setdefault(k, t)
    tasks = []
    for k, t in merged.items():
        t = {**t, "confidence": CONF_BOTH if counts[k] >= 2 else CONF_ONE,
             "run_votes": counts[k]}
        tasks.append(t)

    tools = _union_by(outs, "tools", lambda x: _norm(x.get("name")))
    work = _union_by(outs, "work_context",
                     lambda x: (_norm(x.get("category")), _norm(x.get("value"))))
    return {
        "ksco_code": code, "tasks": tasks, "tools": tools, "work_context": work,
        "extraction_runs": len(outs), "cross_consistency": round(cross, 4),
    }


def _union_by(outs: list[dict], field: str, keyf) -> list[dict]:
    seen, result = set(), []
    for o in outs:
        for x in o.get(field) or []:
            k = keyf(x)
            if k and k not in seen:
                seen.add(k)
                result.append(x)
    return result


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["build-requests"])
    ap.add_argument("--scope", default=None, help="콤마구분 코드/접두(예: 28 또는 28,22)")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    scope = a.scope.split(",") if a.scope else None
    if a.cmd == "build-requests":
        build_requests(scope, force=a.force)
