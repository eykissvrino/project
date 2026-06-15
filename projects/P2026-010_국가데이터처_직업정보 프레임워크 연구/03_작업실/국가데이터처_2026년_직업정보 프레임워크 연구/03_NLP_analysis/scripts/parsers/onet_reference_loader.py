"""O*NET 29.3 Work Activities 위계 → external_ref.onet_gwa/iwa/dwa 적재 (사양서 §2.2).

입력(텍스트 탭구분, parsers/download_onet.py 로 받음):
  - Content Model Reference.txt → GWA 41 (Element ID 4.A.x.x.x)
  - IWA Reference.txt           → IWA 332 (Element ID=GWA, IWA ID, IWA Title)
  - DWA Reference.txt           → DWA 2,087 (Element ID=GWA, IWA ID, DWA ID, DWA Title)

검증: onet_gwa = 41. 트랜잭션 + idempotent(전체 삭제 후 재적재).
사용: python parsers/onet_reference_loader.py
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

import duckdb

_HERE = Path(__file__).resolve().parent
ROOT = _HERE.parents[2]  # 프로젝트 루트
DB = _HERE.parent.parent / "results" / "pipeline.duckdb"
DATA = (ROOT / "01_data_collection" / "00_external_references"
        / "직업정보 관련 참고자료_해외" / "02_ONET_WorkActivities_DWA" / "onet_data")

GWA_RE = re.compile(r"^4\.A\.\d+\.[a-z]\.\d+$")  # GWA leaf element id


def _read(fname: str) -> list[list[str]]:
    with (DATA / fname).open(encoding="utf-8") as fh:
        return list(csv.reader(fh, delimiter="\t"))


def _qualified(con, table: str) -> str:
    """information_schema 에서 onet_* 테이블의 스키마.테이블 형태를 찾는다."""
    row = con.execute(
        "SELECT table_schema FROM information_schema.tables WHERE table_name = ?",
        [table],
    ).fetchone()
    if row is None:
        raise RuntimeError(f"테이블 {table} 없음 — kfw init 으로 DDL 먼저 적용 필요")
    return f"{row[0]}.{table}"


def load(db_path: Path = DB) -> dict:
    cm = _read("Content Model Reference.txt")[1:]
    iwa = _read("IWA Reference.txt")[1:]
    dwa = _read("DWA Reference.txt")[1:]

    gwa_rows = [(r[0], r[1], r[2] if len(r) > 2 else None)
                for r in cm if GWA_RE.match(r[0])]
    iwa_rows = [(r[1], r[2], r[0]) for r in iwa if len(r) >= 3]          # (iwa_id, title, gwa_id)
    dwa_rows = [(r[2], r[3], r[1]) for r in dwa if len(r) >= 4]          # (dwa_id, title, iwa_id)

    con = duckdb.connect(str(db_path))
    t_gwa = _qualified(con, "onet_gwa")
    t_iwa = _qualified(con, "onet_iwa")
    t_dwa = _qualified(con, "onet_dwa")
    try:
        con.execute("BEGIN")
        # 자식부터 삭제(FK 안전)
        con.execute(f"DELETE FROM {t_dwa}")
        con.execute(f"DELETE FROM {t_iwa}")
        con.execute(f"DELETE FROM {t_gwa}")
        con.executemany(
            f"INSERT INTO {t_gwa} (onet_gwa_id, label, description) VALUES (?,?,?)", gwa_rows)
        con.executemany(
            f"INSERT INTO {t_iwa} (onet_iwa_id, label, onet_gwa_id) VALUES (?,?,?)", iwa_rows)
        con.executemany(
            f"INSERT INTO {t_dwa} (onet_dwa_id, label, onet_iwa_id) VALUES (?,?,?)", dwa_rows)
        con.execute("COMMIT")
    except Exception:
        con.execute("ROLLBACK")
        raise

    counts = {
        "onet_gwa": con.execute(f"SELECT count(*) FROM {t_gwa}").fetchone()[0],
        "onet_iwa": con.execute(f"SELECT count(*) FROM {t_iwa}").fetchone()[0],
        "onet_dwa": con.execute(f"SELECT count(*) FROM {t_dwa}").fetchone()[0],
    }
    con.execute("CHECKPOINT")
    con.close()
    return counts


if __name__ == "__main__":
    if not DATA.exists():
        print(f"ONET 데이터 폴더 없음: {DATA}\n먼저 parsers/download_onet.py 실행", file=sys.stderr)
        sys.exit(1)
    counts = load()
    print("적재 완료:", counts)
    ok = counts["onet_gwa"] == 41
    print("GWA 41 검증:", "OK" if ok else f"FAIL ({counts['onet_gwa']})")
    sys.exit(0 if ok else 1)
