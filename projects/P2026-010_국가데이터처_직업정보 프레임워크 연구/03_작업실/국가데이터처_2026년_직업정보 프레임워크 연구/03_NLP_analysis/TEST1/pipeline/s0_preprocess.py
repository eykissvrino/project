"""Stage 0 — 입력·전처리 (KSCO 권위 원천 → 추출가능 입력 레코드).

설계: stages/Stage0_입력_전처리_설계.md
입력원: HWPX 권위 파싱으로 적재된 ksco_node + ksco_main_task/example/exclusion (db.py).

본 단계 책임:
- 세세분류(1,270) 단위로 **완전한 위계(대>중>소>세>세세 코드·명칭)** 부착
- 정의 정제 + 부모 세분류 주요업무 상속(D0)
- 메타·플래그: low_signal / has_tasks / valid / remarks + 커버리지 리포트
행동진술(TASK) 판정은 Stage 1.
"""
from __future__ import annotations

import re
from typing import Iterable, Iterator

# ── 정제 ─────────────────────────────────────────────────────────────
def normalize_ws(s: str | None) -> str:
    if not s:
        return ""
    return " ".join(str(s).split())


def clean_text(s: str | None) -> str:
    """공백 정규화(HWPX 권위 파싱이라 페이지헤더 노이즈는 거의 없음)."""
    return normalize_ws(s)


def ascii_ratio(s: str) -> float:
    if not s:
        return 0.0
    ascii_n = sum(1 for ch in s if ord(ch) < 128 and not ch.isspace())
    total = sum(1 for ch in s if not ch.isspace())
    return ascii_n / total if total else 0.0


def is_low_signal(definition: str) -> bool:
    """정의<50자 또는 ASCII비율>0.45 → 정의 빈약."""
    d = definition or ""
    return len(d) < 50 or ascii_ratio(d) > 0.45


# ── 캐시 로드 ────────────────────────────────────────────────────────
def _load_caches(con) -> dict:
    nodes = con.execute(
        """SELECT ksco_code, level, name, parent_code, major_code, major_name,
                  definition, has_own_tasks FROM ksco_node""").fetchall()
    name = {r[0]: r[2] for r in nodes}
    node = {r[0]: {"level": r[1], "name": r[2], "parent_code": r[3],
                   "major_code": r[4], "major_name": r[5],
                   "definition": r[6] or "", "has_own_tasks": bool(r[7])} for r in nodes}
    tasks: dict[str, list[str]] = {}
    for code, item in con.execute(
            "SELECT ksco_code, item FROM ksco_main_task ORDER BY ksco_code, seq").fetchall():
        tasks.setdefault(code, []).append(item)
    exs: dict[str, list[str]] = {}
    for code, ex in con.execute(
            "SELECT ksco_code, example FROM ksco_example ORDER BY ksco_code, seq").fetchall():
        exs.setdefault(code, []).append(ex)
    return {"name": name, "node": node, "tasks": tasks, "examples": exs}


# 주요업무 출처 한글 라벨
SRC_SELF, SRC_PARENT, SRC_NONE = "세세분류 자체보유", "세분류 상속", "없음"


def _def_of(node: dict, code: str) -> str:
    return clean_text(node.get(code, {}).get("definition", ""))


def build_extraction_context(rec: dict) -> str:
    """빈약한 세세 정의를 보완하기 위해 세세+조상 정의를 결합(구체→일반)."""
    parts = [f"[세세분류 {rec['ksco_code']} {rec['name']}] {rec['definition'] or '(정의 없음)'}"]
    for lvl, c, nm, d in [
        ("세분류", rec["broad_code"], rec["broad_name"], rec["broad_def"]),
        ("소분류", rec["minor_code"], rec["minor_name"], rec["minor_def"]),
        ("중분류", rec["mid_code"], rec["mid_name"], rec["mid_def"]),
        ("대분류", rec["major_code"], rec["major_name"], rec["major_def"]),
    ]:
        if d:
            parts.append(f"[{lvl} {c} {nm}] {d}")
    return "\n".join(parts)


def build_record(con, code: str, cache: dict | None = None) -> dict:
    """세세분류 1건 → 완전 위계 + 전수준 정의 + 상속 주요업무 + 추출컨텍스트 + 플래그."""
    cache = cache or _load_caches(con)
    name, node, tasks, exs = cache["name"], cache["node"], cache["tasks"], cache["examples"]
    if code not in node or node[code]["level"] != 5:
        raise KeyError(f"세세분류 아님/없음: {code}")

    c2, c3, c4 = code[:2], code[:3], code[:4]
    clean_def = clean_text(node[code]["definition"])

    own_tasks = tasks.get(code, [])
    parent_tasks = tasks.get(c4, [])
    main_tasks = own_tasks or parent_tasks
    tasks_source = SRC_SELF if own_tasks else (SRC_PARENT if parent_tasks else SRC_NONE)

    low_signal = is_low_signal(clean_def)
    has_tasks = bool(main_tasks)
    # 추출가능: 주요업무가 있거나, (세세+조상) 정의가 충분
    ancestor_def = any(_def_of(node, c) for c in (c4, c3, c2, code[0]))
    valid = has_tasks or bool(clean_def) or ancestor_def

    rec = {
        # 완전 위계 (대>중>소>세>세세 코드·명칭)
        "major_code": code[0], "major_name": node[code]["major_name"],
        "mid_code": c2, "mid_name": name.get(c2, ""),
        "minor_code": c3, "minor_name": name.get(c3, ""),
        "broad_code": c4, "broad_name": name.get(c4, ""),
        "ksco_code": code, "name": node[code]["name"],
        # 전수준 정의 (대>중>소>세>세세) — 조상 설명 노출
        "major_def": _def_of(node, code[0]),
        "mid_def": _def_of(node, c2),
        "minor_def": _def_of(node, c3),
        "broad_def": _def_of(node, c4),
        "definition": clean_def,
        # 주요업무 (상속) · 예시
        "main_tasks": main_tasks,
        "main_tasks_source": tasks_source,
        "own_task_count": len(own_tasks),
        "examples": exs.get(code, []),
        # 메타
        "layer": "L0", "source": "KSCO_해설서",
        "low_signal": low_signal, "has_tasks": has_tasks, "valid": valid,
    }
    rec["extraction_context"] = build_extraction_context(rec)

    remarks = []
    if tasks_source == SRC_NONE:
        remarks.append("주요업무 없음 → 정의·조상정의로 추출")
    elif tasks_source == SRC_PARENT:
        remarks.append("세분류 주요업무 상속")
    if low_signal:
        remarks.append("세세정의 빈약 → 조상정의 보강")
    if not valid:
        remarks.append("추출 불가")
    rec["remarks"] = "; ".join(remarks)
    return rec


def iter_codes(con, scope: Iterable[str] | None = None) -> Iterator[str]:
    codes = [r[0] for r in con.execute(
        "SELECT ksco_code FROM ksco_node WHERE level=5 ORDER BY ksco_code").fetchall()]
    if scope:
        prefixes = tuple(str(s) for s in scope)
        codes = [c for c in codes if c.startswith(prefixes)]
    yield from codes


def build_all(con, scope: Iterable[str] | None = None) -> list[dict]:
    cache = _load_caches(con)
    return [build_record(con, c, cache) for c in iter_codes(con, scope)]


def coverage_report(records: list[dict]) -> dict:
    n = len(records)
    valid_n = sum(1 for r in records if r["valid"])
    low_n = sum(1 for r in records if r["low_signal"])
    tasks_n = sum(1 for r in records if r["has_tasks"])
    self_n = sum(1 for r in records if r["main_tasks_source"] == SRC_SELF)
    parent_n = sum(1 for r in records if r["main_tasks_source"] == SRC_PARENT)
    none_n = sum(1 for r in records if r["main_tasks_source"] == SRC_NONE)

    by_major: dict[str, dict] = {}
    for r in records:
        key = r["major_code"]
        d = by_major.setdefault(key, {"대분류": f"{key} {r['major_name']}", "직업수": 0,
                                      "valid": 0, "low_signal": 0, "주요업무보유": 0})
        d["직업수"] += 1
        d["valid"] += int(r["valid"])
        d["low_signal"] += int(r["low_signal"])
        d["주요업무보유"] += int(r["has_tasks"])

    return {
        "총_세세분류": n, "valid": valid_n, "valid율": round(valid_n / n, 4) if n else 0,
        "low_signal": low_n, "주요업무보유": tasks_n,
        "주요업무보유율": round(tasks_n / n, 4) if n else 0,
        "주요업무_self": self_n, "주요업무_parent": parent_n, "주요업무_none": none_n,
        "by_major": sorted(by_major.values(), key=lambda x: x["대분류"]),
    }
