"""Stage 3 — IWA 8조항 검증 (dwa_rules 재사용 + R4 완화).

IWA는 DWA보다 한 단계 더 일반적이므로(설계 §④ 일반화 원칙, 사용자 결정 2026-06-11),
조항 4(광의 일반어 금지)는 **경고(보고용)**로 완화하고 게이트에서 제외한다.
나머지 형식 7조항(R1 단일서술어·R2 종결·R6 예시금지·R8 빈/길이 등)은 DWA와 동일하게 적용.

근거: ONET IWA 라벨("문서·자료를 읽어 업무에 활용한다")이 'documents or materials'식
일반 목적어를 정당하게 사용 → R4 그대로면 정상 IWA 차단. 일반화는 프롬프트·DWA라벨입력·
추상도 QC로 보장하고, R4는 차단이 아니라 모니터링 지표로 둔다.

사용:
    from pipeline.iwa_rules import check_iwa, check_batch_iwa
    r = check_iwa("재무·투자 정보를 분석하여 평가한다")
    # r["passed"] 는 R4를 제외한 하드조항 기준. r["r4_warning"] 에 R4 위반어.
"""
from __future__ import annotations

from pipeline import dwa_rules

# 재노출(공용)
normalize_label = dwa_rules.normalize_label
PASS_RATE_GATE = dwa_rules.PASS_RATE_GATE


def check_iwa(label: str) -> dict:
    """IWA label 1건 검증. R4(광의 일반어)는 hard→soft(경고)로 전환.

    passed = R1·R2·R6·(빈라벨 아님) 모두 통과 (R4 제외). R4 위반은 r4_warning에 기록.
    """
    r = dwa_rules.check_dwa(label)
    rules = r["rules"]
    r4_ok = rules.get("R4_중간추상도", True)
    n_eoj = r.get("eojeol", 0)

    # R4를 게이트에서 제외한 하드 판정
    hard_ok = (rules.get("R1_단일서술어", True)
               and rules.get("R2_종결어미", True)
               and rules.get("R6_예시금지", True)
               and n_eoj > 0)

    # 위반 목록에서 R4 항목은 경고로 이동
    violations = [v for v in r["violations"] if not v.startswith("R4:")]
    r4_hits = [v for v in r["violations"] if v.startswith("R4:")]
    warnings = list(r["warnings"]) + r4_hits

    return {
        "label": r["label"],
        "passed": hard_ok,
        "violations": violations,
        "warnings": warnings,
        "r4_relaxed": (not r4_ok),     # True = R4 위반이지만 IWA에선 허용(경고)
        "r4_warning": r4_hits,
        "rules": rules,
        "eojeol": n_eoj,
    }


def check_batch_iwa(labels: list[str]) -> dict:
    """라벨 일괄 검증 + 준수율(R4 제외 기준, §⑦ ≥0.90 게이트). R4 완화율도 집계."""
    results = [check_iwa(x) for x in labels]
    n = len(results)
    n_pass = sum(1 for r in results if r["passed"])
    n_r4 = sum(1 for r in results if r["r4_relaxed"])
    rate = (n_pass / n) if n else 0.0
    return {
        "n": n, "n_pass": n_pass, "pass_rate": round(rate, 4),
        "gate_passed": rate >= PASS_RATE_GATE,
        "r4_relaxed_count": n_r4,
        "results": results,
    }


if __name__ == "__main__":
    samples = [
        "재무·투자 정보를 분석하여 평가한다",        # OK(일반 목적어)
        "문서·자료를 읽어 업무에 활용한다",          # R4(자료·업무)지만 IWA 허용 → passed
        "고객을 응대하고 상품을 판매하며 관리한다",  # R1 다중 → 위반
        "분석",                                       # R2 명사형 → 위반
        "기계 등을 점검한다",                         # R6 예시구 → 위반
    ]
    out = check_batch_iwa(samples)
    print(f"준수율(R4제외) {out['pass_rate']:.2%} (게이트 {out['gate_passed']}) · "
          f"R4완화 {out['r4_relaxed_count']}건")
    for r in out["results"]:
        flag = "✓" if r["passed"] else "✗"
        r4 = " [R4완화]" if r["r4_relaxed"] else ""
        print(f"  {flag} {r['label']}{r4}  위반={r['violations']}")
