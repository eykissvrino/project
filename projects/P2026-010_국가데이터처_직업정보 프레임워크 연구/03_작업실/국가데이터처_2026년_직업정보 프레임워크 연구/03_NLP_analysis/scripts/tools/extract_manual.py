"""하이브리드 수동 추출(범용) — Claude Code(구독)가 추출, production 경로 적재. API 0원.

사용: python tools/extract_manual.py <세세분류코드>
등록된 코드의 추출 결과(EXTRACTIONS)를 provider로 주입 → extract_one→persist→DuckDB.
새 직업은 EXTRACTIONS 에 항목 추가.
"""
import io
import json
import sys

sys.path.insert(0, ".")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

import duckdb

from utils import ksco_fetch as F
from utils.extract_tasks import extract_one, persist

DB = "../results/pipeline.duckdb"

EXTRACTIONS = {
    # ── 74061 가스 용접원 (기술·기능직, 도구 풍부 / low_signal) ──────────────
    "74061": {
        "tasks": [
            {"verb": "검토하다", "object": "도면", "full_statement": "명세치수와 작업절차를 결정하기 위해 도면 또는 작업지시서를 검토한다", "source_sentence": "명세치수 및 작업절차를 결정하기 위하여 도면 또는 작업 지시서를 검토한다", "confidence": 0.9},
            {"verb": "제거하다", "object": "이물질", "full_statement": "용접부위를 손질하여 이물질을 제거한다", "source_sentence": "용접부위를 손질하여 이물질을 제거하고", "confidence": 0.88},
            {"verb": "표시하다", "object": "용접점", "full_statement": "용접점이나 절단선을 표시한다", "source_sentence": "용접점이나 절단선을 표시한다", "confidence": 0.88},
            {"verb": "파악하다", "object": "용접물 재료", "full_statement": "용접물의 재료·두께·형태를 파악한다", "source_sentence": "용접물의 재료, 두께, 형태 등을 파악하고", "confidence": 0.88},
            {"verb": "조정하다", "object": "용접장비", "full_statement": "용접물에 적합하게 용접장비를 조정한다", "source_sentence": "적합하게 용접장비를 조정 한다", "confidence": 0.9},
            {"verb": "용접하다", "object": "접합부", "full_statement": "전극·용접봉·토치팁 등 공구를 사용하여 접합부나 이음매를 용접한다", "source_sentence": "적절한 전극, 용접봉, 토치팁 및 기타 필요한 공구를 사용하여 접합부나 이음매를 용접하거나", "confidence": 0.92},
            {"verb": "절단하다", "object": "공작물", "full_statement": "절단선을 따라 공작물을 절단한다", "source_sentence": "절단선을 따라 절단 한다", "confidence": 0.88},
            {"verb": "검사하다", "object": "용접 비드", "full_statement": "완성된 접합체의 비드 크기·침투력을 명세서와 비교·검사한다", "source_sentence": "완성된 접합체의 비드 크기, 침투력 및 기타 특성을 명세서와 비교‧ 검사한다", "confidence": 0.9},
            {"verb": "손질하다", "object": "용접부위", "full_statement": "철솔·그라인더·화공약품을 사용하여 용접부위를 손질한다", "source_sentence": "철솔, 그라인더 및 화공약품을 사용하여 용접부위를 손질한다", "confidence": 0.9},
            {"verb": "용접하다", "object": "금속", "full_statement": "아세틸렌·산소-아세틸렌으로 금속을 용접한다", "source_sentence": "아세틸렌, 산소-아세틸렌 등으로 금속을 용접한다", "confidence": 0.92},
        ],
        "tools": [
            {"name": "용접장비", "category": "장비", "evidence_span": "적합하게 용접장비를 조정"},
            {"name": "토치팁", "category": "도구", "evidence_span": "용접봉, 토치팁 및 기타 필요한 공구"},
            {"name": "용접봉", "category": "도구", "evidence_span": "전극, 용접봉, 토치팁"},
            {"name": "전극", "category": "도구", "evidence_span": "적절한 전극, 용접봉"},
            {"name": "그라인더", "category": "장비", "evidence_span": "철솔, 그라인더 및 화공약품"},
            {"name": "철솔", "category": "도구", "evidence_span": "철솔, 그라인더 및 화공약품"},
        ],
        "work_context": [
            {"category": "위험", "value": "화공약품 취급", "evidence_span": "화공약품을 사용하여 용접부위를 손질"},
        ],
    },
}


def provider_for(code):
    payload = dict(EXTRACTIONS[code], ksco_code=code)

    def provider(model, system, user, temperature, seed):
        return json.dumps(payload, ensure_ascii=False), 1400, 700
    return provider


def main(code):
    if code not in EXTRACTIONS:
        print(f"등록 안 된 코드: {code}. 등록: {list(EXTRACTIONS)}")
        return 1
    con = duckdb.connect(DB)
    ctx = F.fetch_for_extraction(con, code)
    res = extract_one(ctx, con=con, provider=provider_for(code), use_cache=True)
    counts = persist(con, res)
    print("="*72)
    print(f"{code} {ctx['name']} | parent {ctx['parent_code']} {ctx['parent_name']} | low_signal={ctx['low_signal']}")
    print(f"status={res['status']} jaccard={res['cross_consistency']:.3f} runs={res['extraction_runs']}")
    print(f"적재: task {counts['tasks']} / tool {counts['tools']} / work_context {counts['work_context']}")
    print("[tool_inventory]")
    for r in con.execute("SELECT name, category FROM tool_inventory WHERE ksco_code=? ORDER BY tool_id", [code]).fetchall():
        print(f"   {r[0]} ({r[1]})")
    con.execute("CHECKPOINT")
    con.close()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "74061"))
