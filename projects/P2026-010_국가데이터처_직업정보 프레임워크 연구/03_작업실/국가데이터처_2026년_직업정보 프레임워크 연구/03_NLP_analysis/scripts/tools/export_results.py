"""DuckDB 결과 → 엑셀(.xlsx) 내보내기. 비개발자가 더블클릭으로 확인.

사용: python tools/export_results.py
출력: 03_NLP_analysis/results/추출결과_확인_<날짜>.xlsx
"""
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, ".")
import duckdb
import pandas as pd

RESULTS = Path(__file__).resolve().parents[1].parent / "results"
DB = RESULTS / "pipeline.duckdb"
KST = timezone(timedelta(hours=9))
OUT = RESULTS / f"추출결과_확인_{datetime.now(KST).strftime('%Y%m%d_%H%M')}.xlsx"


def q(con, sql):
    return con.execute(sql).fetchdf()


def main():
    con = duckdb.connect(str(DB), read_only=True)
    sheets = {}

    sheets["추출_TASK"] = q(con, """
        SELECT t.ksco_code AS 세세분류코드, o.name AS 직업명, t.parent_code AS 부모세분류,
               t.verb AS 동사, t.object AS 목적어, t.full_statement AS 작업진술,
               t.confidence AS 신뢰도, t.cross_consistency AS 일관성,
               CASE WHEN t.low_signal THEN '정의빈약(상속의존·주의)' ELSE '정의충분' END AS 정의상태
        FROM task t LEFT JOIN ksco_occupation o ON t.ksco_code=o.ksco_code
        ORDER BY t.ksco_code, t.task_id""")

    sheets["추출_도구"] = q(con, """
        SELECT ti.ksco_code AS 세세분류코드, o.name AS 직업명,
               ti.name AS 도구명, ti.category AS 분류, ti.evidence_span AS 근거
        FROM tool_inventory ti LEFT JOIN ksco_occupation o ON ti.ksco_code=o.ksco_code
        ORDER BY ti.ksco_code, ti.tool_id""")

    sheets["추출_환경"] = q(con, """
        SELECT wc.ksco_code AS 세세분류코드, o.name AS 직업명,
               wc.category AS 분류, wc.value AS 환경요소, wc.evidence_span AS 근거
        FROM work_context wc LEFT JOIN ksco_occupation o ON wc.ksco_code=o.ksco_code
        ORDER BY wc.ksco_code, wc.context_id""")

    # 직업별 요약 (도구 대비)
    sheets["요약_직업별"] = q(con, """
        SELECT o.ksco_code AS 코드, o.name AS 직업명,
               (SELECT count(*) FROM task t WHERE t.ksco_code=o.ksco_code) AS TASK수,
               (SELECT count(*) FROM tool_inventory ti WHERE ti.ksco_code=o.ksco_code) AS 도구수,
               (SELECT count(*) FROM work_context wc WHERE wc.ksco_code=o.ksco_code) AS 환경수
        FROM ksco_occupation o
        WHERE o.ksco_code IN (SELECT DISTINCT ksco_code FROM task)
        ORDER BY o.ksco_code""")

    def onet(tbl):
        try:
            return q(con, f"SELECT * FROM external_ref.{tbl}")
        except Exception:
            return q(con, f"SELECT * FROM {tbl}")

    sheets["ONET_GWA(41)"] = onet("onet_gwa")
    sheets["ONET_IWA(332)"] = onet("onet_iwa")
    sheets["ONET_DWA(2087)"] = onet("onet_dwa")

    sheets["LLM호출로그"] = q(con, """
        SELECT model AS 모델, seed, cached AS 캐시적중,
               input_tokens AS 입력토큰, output_tokens AS 출력토큰, called_at AS 호출시각
        FROM llm_call_log ORDER BY called_at""")
    con.close()

    with pd.ExcelWriter(OUT, engine="openpyxl") as xw:
        for name, df in sheets.items():
            df.to_excel(xw, sheet_name=name[:31], index=False)

    print(f"저장 완료: {OUT}")
    for name, df in sheets.items():
        print(f"  [{name}] {len(df)} 행")


if __name__ == "__main__":
    main()
