"""중분류 28 4계층 2단계: DWA 라벨(8조항) → IWA 묶기 → GWA 매핑 → 위계 엑셀.

1단계(pipeline_test_28.py) 산출 dwa_clusters.json 을 입력으로,
Claude Code가 8조항 DWA 라벨·IWA 그룹을 부여(하이브리드) → 4계층 위계 완성.
출력: results/4계층_도출결과_28_<날짜>.xlsx
"""
import io
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, ".")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

import pandas as pd

OUT = Path("../results/pipeline_test_28")
KST = timezone(timedelta(hours=9))
XLSX = Path("../results") / f"4계층_도출결과_28_{datetime.now(KST).strftime('%Y%m%d_%H%M')}.xlsx"

# ── Claude Code 부여: DWA 라벨(8조항: 단일동사·현재서술형·JobFamily 일반화) ──
DWA_LABELS = {
    0: "통계 자료를 분석하여 위험과 확률을 산정한다",
    1: "재무·인사 자료를 조사하고 분석하여 의사결정 정보를 제공한다",
    2: "조직 체계와 업무 절차를 진단하여 개선안을 제안한다",
    3: "자산 포트폴리오를 운용하고 투자 전략을 수립한다",
    4: "전문 분야의 정책과 규정을 해석하여 자문한다",
    5: "고객의 요구를 파악하여 적합한 상품이나 서비스를 추천한다",
}

# ── IWA(한 단계 상위) 그룹 + ONET GWA 매핑 ──
# iwa_id: (라벨, [속한 dwa_cluster], onet_gwa_label)
IWA_DEF = {
    "IWA_KR_28_01": ("자료를 분석하여 정보·판단을 산출한다", [0, 1], "Analyzing Data or Information"),
    "IWA_KR_28_02": ("조직·자산의 전략과 체계를 설계한다", [2, 3], "Developing Objectives and Strategies"),
    "IWA_KR_28_03": ("전문 자문과 고객 상담을 제공한다", [4, 5], "Providing Consultation and Advice to Others"),
}


def main():
    clusters = json.loads((OUT / "dwa_clusters.json").read_text(encoding="utf-8"))
    by_id = {c["dwa_cluster"]: c for c in clusters}

    # DWA → IWA 역매핑
    dwa2iwa = {}
    for iwa_id, (_, dwa_list, _) in IWA_DEF.items():
        for d in dwa_list:
            dwa2iwa[d] = iwa_id

    # 위계 테이블 (GWA → IWA → DWA → 대표 TASK)
    rows = []
    for c in sorted(clusters, key=lambda x: (dwa2iwa.get(x["dwa_cluster"], "zz"), -x["size"])):
        cid = c["dwa_cluster"]
        iwa_id = dwa2iwa.get(cid, "(미배정)")
        iwa_label = IWA_DEF.get(iwa_id, ("(미배정)", [], ""))[0]
        rows.append({
            "GWA(ONET)": c["gwa_label"],
            "IWA(한국)": iwa_label,
            "DWA(한국, 8조항)": DWA_LABELS.get(cid, f"군집{cid}"),
            "TASK수": c["size"],
            "응집도": c["mean_cosine"],
            "대표 TASK 3건": " / ".join(m[:40] for m in c["members"][:3]),
        })
    hier = pd.DataFrame(rows)

    # 요약: 계층별 개수
    summary = pd.DataFrame([
        {"계층": "TASK (규칙추출)", "개수": int(pd.read_parquet(OUT / "tasks.parquet").shape[0])},
        {"계층": "DWA (한국, 도출)", "개수": len(DWA_LABELS)},
        {"계층": "IWA (한국, 도출)", "개수": len(IWA_DEF)},
        {"계층": "GWA (ONET 매핑)", "개수": hier["GWA(ONET)"].nunique()},
    ])

    with pd.ExcelWriter(XLSX, engine="openpyxl") as xw:
        summary.to_excel(xw, sheet_name="계층_요약", index=False)
        hier.to_excel(xw, sheet_name="4계층_위계", index=False)
        # IWA→GWA 매핑표
        iwa_map = pd.DataFrame([
            {"IWA(한국)": lbl, "→ GWA(ONET)": gwa, "포함 DWA수": len(dl)}
            for _, (lbl, dl, gwa) in IWA_DEF.items()])
        iwa_map.to_excel(xw, sheet_name="IWA_GWA매핑", index=False)

    print(f"저장: {XLSX}")
    print("\n=== 4계층 위계 (TASK 137 → DWA 6 → IWA 3 → GWA 3) ===")
    for iwa_id, (lbl, dl, gwa) in IWA_DEF.items():
        print(f"\nGWA: {gwa}")
        print(f"  └ IWA: {lbl}")
        for d in dl:
            print(f"      └ DWA: {DWA_LABELS[d]}  (TASK {by_id[d]['size']})")


if __name__ == "__main__":
    main()
