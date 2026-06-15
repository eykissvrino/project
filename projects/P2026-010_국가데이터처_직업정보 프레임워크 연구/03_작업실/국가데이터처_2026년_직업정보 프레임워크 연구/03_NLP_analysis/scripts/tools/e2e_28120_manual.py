"""하이브리드 E2E: 28120 회계사 — Claude Code(구독)가 추출, production 경로로 적재.

API 키 없이 동작한다. provider 함수가 Claude Code(이 대화)의 추출 결과를 반환하고,
나머지(extract_one self-consistency → persist → DuckDB)는 실제 코드 그대로 흐른다.

실행: python tools/e2e_28120_manual.py
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

# ── Claude Code 추출 결과 (§1.2 규약: 동사+목적어, 복합행동 분할, 일반진술·예시 제외) ──
# 입력: 28120 회계사 정의 + 부모 2812 주요업무 9항(상속). "대분류 2" 헤더 노이즈는 무시.
EXTRACTION = {
    "ksco_code": "28120",
    "tasks": [
        {"verb": "관리하다", "object": "회계 용역 업무",
         "full_statement": "회계에 관한 용역 업무를 계획하고 관리한다",
         "source_sentence": "회계에 관한 용역 업무를 계획‧관리하고", "confidence": 0.9},
        {"verb": "작성하다", "object": "재무회계 서류",
         "full_statement": "의뢰인의 위임에 따라 재무회계 서류를 작성한다",
         "source_sentence": "의뢰인의 위임에 따라 재무회계 서류의 작성", "confidence": 0.9},
        {"verb": "작성하다", "object": "소득세신고서",
         "full_statement": "기업의 소득세보고서(신고서)를 작성한다",
         "source_sentence": "회계보고서를 통해 소득세신고서를 작성한다", "confidence": 0.92},
        {"verb": "수행하다", "object": "재무회계감사",
         "full_statement": "재무회계감사를 수행하거나 증명한다",
         "source_sentence": "재무회계감사 또는 증명을 하고", "confidence": 0.9},
        {"verb": "조사하다", "object": "회계기록",
         "full_statement": "회계기록과 재무거래 기록을 조사한다",
         "source_sentence": "회계기록을 조사하고 재무제표 및 보고서를 작성한다", "confidence": 0.9},
        {"verb": "작성하다", "object": "재무제표",
         "full_statement": "재무제표 및 회계보고서를 작성한다",
         "source_sentence": "회계기록을 조사하고 재무제표 및 보고서를 작성한다", "confidence": 0.92},
        {"verb": "분석하다", "object": "재무제표",
         "full_statement": "재무제표 및 보고서를 분석한다",
         "source_sentence": "재무제표 및 보고서를 분석하고", "confidence": 0.9},
        {"verb": "제공하다", "object": "재무 자문",
         "full_statement": "재무·사업·세금에 대한 자문을 제공한다",
         "source_sentence": "재무, 사업 및 세금에 대한 자문을 해준다", "confidence": 0.9},
        {"verb": "관리하다", "object": "내부규제절차",
         "full_statement": "내부규제절차를 만들고 유지·관리한다",
         "source_sentence": "내부규제절차를 만들고 유지‧ 관리한다", "confidence": 0.88},
        {"verb": "확인하다", "object": "재무기록 정확성",
         "full_statement": "회계기준·절차·내부규정 일치 여부와 재무기록의 정확성을 확인한다",
         "source_sentence": "회계기준, 절차 및 내부규정 일치여부, 재무기록의 정확성 여부 등을 확인", "confidence": 0.88},
        {"verb": "작성하다", "object": "개선 권고안",
         "full_statement": "회계 및 경영실무 개선을 위한 권고안을 작성한다",
         "source_sentence": "경영실무를 개선하기 위한 권고안을 만든다", "confidence": 0.9},
        {"verb": "수행하다", "object": "사업현장 감사",
         "full_statement": "소득세법 규정 준수를 확인하기 위해 사업현장 감사를 수행한다",
         "source_sentence": "소득세법 규정이나 기타 요건에 맞는지 확인하기 위해 사업현장 감사를 수행한다", "confidence": 0.9},
    ],
    "tools": [
        {"name": "회계시스템", "category": "시스템",
         "evidence_span": "회계시스템을 계획, 설정하고 관리하며"},
    ],
    "work_context": [
        {"category": "장소", "value": "회계법인·회계사무소·일반기업체 사무실",
         "evidence_span": "회계법인, 합동회계사무소, 감사반이나 일반기업체에서 일하며"},
        {"category": "사회적", "value": "의뢰인 위임·상담 응대",
         "evidence_span": "의뢰인의 위임에 따라 ... 상담한다"},
        {"category": "장소", "value": "사업현장 출장 감사",
         "evidence_span": "사업현장 감사를 수행한다"},
    ],
}


def provider(model, system, user, temperature, seed):
    """Claude Code 추출 결과 반환(두 seed 동일 → self-consistency auto_accept).
    실제 API 2-run은 seed별 미세 변동이 있을 수 있음(여기선 구독 단일 추출)."""
    return json.dumps(EXTRACTION, ensure_ascii=False), 1300, 620


def main():
    con = duckdb.connect(DB)
    ctx = F.fetch_for_extraction(con, "28120")
    res = extract_one(ctx, con=con, provider=provider, use_cache=True)
    counts = persist(con, res)

    print("="*72)
    print(f"28120 회계사 | parent {ctx['parent_code']} {ctx['parent_name']} | low_signal={ctx['low_signal']}")
    print(f"status={res['status']}  jaccard={res['cross_consistency']:.3f}  runs={res['extraction_runs']}")
    print(f"적재: task {counts['tasks']} / tool {counts['tools']} / work_context {counts['work_context']}")
    print("-"*72)
    print("[task 테이블]")
    for r in con.execute(
        "SELECT object, verb, confidence FROM task WHERE ksco_code='28120' ORDER BY task_id").fetchall():
        print(f"   {r[0]:<16} {r[1]:<8} conf={r[2]}")
    print("[tool_inventory]")
    for r in con.execute(
        "SELECT name, category FROM tool_inventory WHERE ksco_code='28120'").fetchall():
        print(f"   {r[0]} ({r[1]})")
    print("[work_context]")
    for r in con.execute(
        "SELECT category, value FROM work_context WHERE ksco_code='28120'").fetchall():
        print(f"   {r[0]}: {r[1]}")
    print("[llm_call_log — 최근 4]")
    for r in con.execute(
        "SELECT model, seed, cached, input_tokens, output_tokens FROM llm_call_log "
        "ORDER BY called_at DESC LIMIT 4").fetchall():
        print(f"   {r[0]} seed={r[1]} cached={r[2]} in={r[3]} out={r[4]}")
    con.close()


if __name__ == "__main__":
    main()
