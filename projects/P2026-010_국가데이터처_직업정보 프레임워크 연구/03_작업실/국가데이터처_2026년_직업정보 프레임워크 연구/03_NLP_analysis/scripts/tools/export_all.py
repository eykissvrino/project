"""전체 결과 통합 엑셀 — 검토용. DB + 중분류28 4계층 + ONET + 안내.

사용: python tools/export_all.py
출력: 03_NLP_analysis/results/전체결과_검토용_<날짜>.xlsx
"""
import io
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, ".")
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import duckdb
import pandas as pd

RESULTS = Path(__file__).resolve().parents[1].parent / "results"
DB = RESULTS / "pipeline.duckdb"
P28 = RESULTS / "pipeline_test_28"
KST = timezone(timedelta(hours=9))
OUT = RESULTS / f"전체결과_검토용_{datetime.now(KST).strftime('%Y%m%d_%H%M')}.xlsx"

# DWA/IWA 라벨 (stage2 와 동일 — import 시 stdout 재래핑 문제 피하려 인라인)
DWA_LABELS = {
    0: "통계 자료를 분석하여 위험과 확률을 산정한다",
    1: "재무·인사 자료를 조사하고 분석하여 의사결정 정보를 제공한다",
    2: "조직 체계와 업무 절차를 진단하여 개선안을 제안한다",
    3: "자산 포트폴리오를 운용하고 투자 전략을 수립한다",
    4: "전문 분야의 정책과 규정을 해석하여 자문한다",
    5: "고객의 요구를 파악하여 적합한 상품이나 서비스를 추천한다",
}
IWA_DEF = {
    "IWA_KR_28_01": ("자료를 분석하여 정보·판단을 산출한다", [0, 1], "Analyzing Data or Information"),
    "IWA_KR_28_02": ("조직·자산의 전략과 체계를 설계한다", [2, 3], "Developing Objectives and Strategies"),
    "IWA_KR_28_03": ("전문 자문과 고객 상담을 제공한다", [4, 5], "Providing Consultation and Advice to Others"),
}


def q(con, sql):
    return con.execute(sql).fetchdf()


def main():
    con = duckdb.connect(str(DB), read_only=True)
    sheets = {}

    # ── 안내(목차) ──
    guide = [
        ("00_안내", "이 시트 — 각 시트 설명"),
        ("1_요약_직업별", "LLM 추출한 직업별 TASK·도구·환경 개수 (회계사 vs 용접원 대비)"),
        ("2_추출_TASK", "직업별 도출된 작업진술 + 신뢰도·일관성·정의상태"),
        ("3_추출_도구", "직업별 사용 도구 (직업군 따라 풍부도 다름)"),
        ("4_추출_환경", "직업별 작업 환경 (근거 스팬 포함)"),
        ("5_중분류28_4계층", "★ TASK→DWA→IWA→GWA 4계층 위계 (중분류 28 테스트)"),
        ("6_중분류28_DWA군집", "DWA 군집별 멤버 TASK + 응집도"),
        ("7_중분류28_TASK상세", "규칙추출 137 TASK + GWA 할당 + 소속 DWA"),
        ("8_ONET_GWA41", "ONET 41 일반작업활동(기준)"),
        ("9_ONET_IWA332", "ONET 332 중간작업활동"),
        ("10_ONET_DWA2087", "ONET 2,087 상세작업활동"),
        ("11_LLM호출로그", "LLM 호출·캐시 기록 (재현성)"),
    ]
    sheets["00_안내"] = pd.DataFrame(guide, columns=["시트", "설명"])

    sheets["1_요약_직업별"] = q(con, """
        SELECT o.ksco_code AS 코드, o.name AS 직업명,
               (SELECT count(*) FROM task t WHERE t.ksco_code=o.ksco_code) AS TASK수,
               (SELECT count(*) FROM tool_inventory ti WHERE ti.ksco_code=o.ksco_code) AS 도구수,
               (SELECT count(*) FROM work_context wc WHERE wc.ksco_code=o.ksco_code) AS 환경수
        FROM ksco_occupation o WHERE o.ksco_code IN (SELECT DISTINCT ksco_code FROM task)
        ORDER BY o.ksco_code""")

    sheets["2_추출_TASK"] = q(con, """
        SELECT t.ksco_code AS 코드, o.name AS 직업명, t.verb AS 동사, t.object AS 목적어,
               t.full_statement AS 작업진술, t.confidence AS 신뢰도, t.cross_consistency AS 일관성,
               CASE WHEN t.low_signal THEN '정의빈약(상속의존)' ELSE '정의충분' END AS 정의상태
        FROM task t LEFT JOIN ksco_occupation o ON t.ksco_code=o.ksco_code ORDER BY t.ksco_code, t.task_id""")
    sheets["3_추출_도구"] = q(con, """
        SELECT ti.ksco_code AS 코드, o.name AS 직업명, ti.name AS 도구명, ti.category AS 분류, ti.evidence_span AS 근거
        FROM tool_inventory ti LEFT JOIN ksco_occupation o ON ti.ksco_code=o.ksco_code ORDER BY ti.ksco_code""")
    sheets["4_추출_환경"] = q(con, """
        SELECT wc.ksco_code AS 코드, o.name AS 직업명, wc.category AS 분류, wc.value AS 환경요소, wc.evidence_span AS 근거
        FROM work_context wc LEFT JOIN ksco_occupation o ON wc.ksco_code=o.ksco_code ORDER BY wc.ksco_code""")

    # ── 중분류 28 4계층 ──
    clusters = []
    if (P28 / "dwa_clusters.json").exists():
        clusters = json.loads((P28 / "dwa_clusters.json").read_text(encoding="utf-8"))
    by_id = {c["dwa_cluster"]: c for c in clusters}
    dwa2iwa = {d: iid for iid, (_, dl, _) in IWA_DEF.items() for d in dl}

    hier = []
    for c in sorted(clusters, key=lambda x: (dwa2iwa.get(x["dwa_cluster"], "zz"), -x["size"])):
        cid = c["dwa_cluster"]; iid = dwa2iwa.get(cid, "(미배정)")
        hier.append({
            "GWA(ONET)": c["gwa_label"],
            "IWA(한국)": IWA_DEF.get(iid, ("(미배정)", [], ""))[0],
            "DWA(한국·8조항)": DWA_LABELS.get(cid, f"군집{cid}"),
            "TASK수": c["size"], "응집도": c["mean_cosine"],
            "대표TASK": " / ".join(m[:45] for m in c["members"][:3]),
        })
    sheets["5_중분류28_4계층"] = pd.DataFrame(hier)

    dwa_detail = []
    for c in clusters:
        for m in c["members"]:
            dwa_detail.append({"DWA": DWA_LABELS.get(c["dwa_cluster"], c["dwa_cluster"]),
                               "GWA": c["gwa_label"], "멤버TASK": m, "응집도": c["mean_cosine"]})
    sheets["6_중분류28_DWA군집"] = pd.DataFrame(dwa_detail)

    if (P28 / "tasks.parquet").exists():
        t28 = pd.read_parquet(P28 / "tasks.parquet")
        t28 = t28.rename(columns={"sub_code": "세분류", "sub_name": "세분류명", "statement": "TASK진술",
                                  "gwa_label": "할당GWA", "gwa_cos": "GWA유사도", "dwa_cluster": "DWA군집"})
        sheets["7_중분류28_TASK상세"] = t28[["세분류", "세분류명", "TASK진술", "할당GWA", "GWA유사도", "DWA군집"]]

    def onet(tbl):
        try: return q(con, f"SELECT * FROM external_ref.{tbl}")
        except Exception: return q(con, f"SELECT * FROM {tbl}")
    sheets["8_ONET_GWA41"] = onet("onet_gwa")
    sheets["9_ONET_IWA332"] = onet("onet_iwa")
    sheets["10_ONET_DWA2087"] = onet("onet_dwa")
    sheets["11_LLM호출로그"] = q(con, "SELECT model AS 모델, seed, cached AS 캐시, input_tokens AS 입력토큰, output_tokens AS 출력토큰, called_at AS 시각 FROM llm_call_log ORDER BY called_at")
    con.close()

    with pd.ExcelWriter(OUT, engine="openpyxl") as xw:
        for name, df in sheets.items():
            df.to_excel(xw, sheet_name=name[:31], index=False)
    print(f"저장: {OUT}")
    for name, df in sheets.items():
        print(f"  [{name}] {len(df)}행")


if __name__ == "__main__":
    main()
