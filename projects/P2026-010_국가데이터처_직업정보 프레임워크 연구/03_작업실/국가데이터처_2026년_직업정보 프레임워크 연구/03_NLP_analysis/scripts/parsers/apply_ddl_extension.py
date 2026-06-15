"""ddl_extension.sql 을 pipeline.duckdb 에 적용한다 (Sprint 1 Step 2).

사용: python parsers/apply_ddl_extension.py [db_path]
트랜잭션 + idempotent. 적용 후 신설 테이블 존재를 검증해 출력한다.
"""
from __future__ import annotations

import sys
from pathlib import Path

import duckdb

_HERE = Path(__file__).resolve().parent
DDL_FILE = _HERE / "ddl_extension.sql"
DEFAULT_DB = _HERE.parent.parent / "results" / "pipeline.duckdb"


def apply(db_path: Path) -> None:
    sql = DDL_FILE.read_text(encoding="utf-8")
    con = duckdb.connect(str(db_path))
    try:
        con.execute("BEGIN")
        con.execute(sql)
        con.execute("COMMIT")
    except Exception:
        con.execute("ROLLBACK")
        raise
    # 검증
    tables = {r[1] for r in con.execute(
        "select table_schema, table_name from information_schema.tables").fetchall()}
    gwa_cols = {r[0] for r in con.execute(
        "select column_name from information_schema.columns where table_name='gwa'").fetchall()}
    task_cols = {r[0] for r in con.execute(
        "select column_name from information_schema.columns where table_name='task'").fetchall()}
    con.close()

    print("tool_inventory:", "OK" if "tool_inventory" in tables else "MISSING")
    print("work_context  :", "OK" if "work_context" in tables else "MISSING")
    print("gwa.kr_label  :", "OK" if "kr_label" in gwa_cols else "MISSING")
    print("task.parent_code:", "OK" if "parent_code" in task_cols else "MISSING")
    print("task.low_signal :", "OK" if "low_signal" in task_cols else "MISSING")


if __name__ == "__main__":
    db = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_DB
    print(f"applying DDL extension to: {db}")
    apply(db)
