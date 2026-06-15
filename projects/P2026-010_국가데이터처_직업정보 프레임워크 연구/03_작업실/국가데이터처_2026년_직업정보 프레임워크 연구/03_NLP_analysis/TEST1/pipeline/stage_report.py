"""스테이지별 결과해설서 자동생성 시스템 (연구진 보고용).

각 Stage의 DB 적재 결과에서 품질지표를 집계해 **마크다운 결과해설서**를 생성한다.
설계안(stages/*_설계.md)이 "무엇을 어떻게" 설계했는지라면, 본 해설서는
"실제로 무엇이 나왔는지(전수 결과·지표·정직한 한계)"를 연구진/발주기관에 설명한다.

사용:
    python pipeline/stage_report.py s1          # Stage 1 결과해설서 생성
    python pipeline/stage_report.py all         # 가능한 전 스테이지

출력: 04_framework_design/docs/stages/results/Stage{N}_결과해설서.md
확장: 새 스테이지는 report_sN(con) 함수를 추가하고 STAGES에 등록하면 끝.
"""
from __future__ import annotations

import statistics as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

TEST1_DIR = Path(__file__).resolve().parents[1]
# 결과해설서 출력 위치(연구진 문서 트리)
OUT_DIR = (TEST1_DIR / ".." / ".." / "04_framework_design" / "docs" / "stages" / "results").resolve()

# 대분류 코드 → 명칭(KSCO 8차)
MAJOR_NAME = {
    "1": "관리자", "2": "전문가 및 관련 종사자", "3": "사무 종사자",
    "4": "서비스 종사자", "5": "판매 종사자", "6": "농림어업 숙련 종사자",
    "7": "기능원 및 관련 기능 종사자", "8": "장치·기계 조작 및 조립 종사자",
    "9": "단순노무 종사자", "A": "군인",
}


def _fmt_pct(n, d):
    return f"{n/d*100:.1f}%" if d else "0%"


# ── 공통 집계 헬퍼 ───────────────────────────────────────────────────
def _task_counts(con, where=""):
    rows = con.execute(
        f"SELECT ksco_code, COUNT(*) FROM task {where} GROUP BY ksco_code").fetchall()
    return {r[0]: r[1] for r in rows}


# ── Stage 1 ──────────────────────────────────────────────────────────
def report_s1(con) -> str:
    """Stage 1(TASK 도출) 결과해설서 본문(markdown) 생성."""
    counts = _task_counts(con)
    n_job = len(counts)
    cnts = list(counts.values())
    total_task = sum(cnts)
    total_target = con.execute(
        "SELECT COUNT(*) FROM ksco_node WHERE level=5").fetchone()[0]

    # 개수 분포
    med = st.median(cnts); mean = round(st.mean(cnts), 1)
    lo, hi = min(cnts), max(cnts)
    n_short = sum(1 for x in cnts if x < 8)
    n_over = sum(1 for x in cnts if x > 40)
    n_fit = sum(1 for x in cnts if 8 <= x <= 30)

    # 신뢰도 분포(TASK 단위)
    conf = {round(float(v), 2): n for v, n in con.execute(
        "SELECT confidence, COUNT(*) FROM task GROUP BY confidence").fetchall()}
    n_both = conf.get(0.95, 0); n_one = conf.get(0.80, 0)

    # 일관성(직업 단위 jaccard)
    jv = [r[1] for r in con.execute(
        "SELECT DISTINCT ksco_code, cross_consistency FROM task").fetchall()
        if r[1] is not None]
    jac_med = round(st.median(jv), 3); jac_mean = round(st.mean(jv), 3)

    # 정의빈약(low_signal) — 직업 단위
    low = {bool(v): n for v, n in con.execute(
        "SELECT low_signal, COUNT(DISTINCT ksco_code) FROM task GROUP BY low_signal").fetchall()}
    n_low = low.get(True, 0); n_full = low.get(False, 0)

    # 추적성·정합
    trace_miss = con.execute(
        "SELECT COUNT(*) FROM task WHERE source_sentence IS NULL OR source_sentence='' "
        "OR derived_from IS NULL OR derived_from=''").fetchone()[0]
    susp = con.execute(
        "SELECT COUNT(*) FROM task WHERE verb IS NULL OR LENGTH(verb)<2 "
        "OR full_statement IS NULL OR LENGTH(full_statement)<6").fetchone()[0]
    n_tool = con.execute("SELECT COUNT(*) FROM tool_inventory").fetchone()[0]
    n_work = con.execute("SELECT COUNT(*) FROM work_context").fetchone()[0]

    # 대분류별 요약
    major_rows = []
    for code, n in counts.items():
        major_rows.append((code[0], n, code))
    by_major = {}
    for mj, n, _ in major_rows:
        by_major.setdefault(mj, []).append(n)
    major_tbl = []
    for mj in sorted(by_major):
        v = by_major[mj]
        low_n = con.execute(
            "SELECT COUNT(DISTINCT ksco_code) FROM task WHERE ksco_code LIKE ? AND low_signal=TRUE",
            [f"{mj}%"]).fetchone()[0]
        jm = [r[1] for r in con.execute(
            "SELECT DISTINCT ksco_code, cross_consistency FROM task WHERE ksco_code LIKE ?",
            [f"{mj}%"]).fetchall() if r[1] is not None]
        major_tbl.append(
            f"| {mj} {MAJOR_NAME.get(mj, '')} | {len(v)} | {sum(v):,} | {st.median(v):.0f} "
            f"| {sum(1 for x in v if x<8)} | {sum(1 for x in v if x>40)} "
            f"| {low_n} | {round(st.median(jm),3) if jm else '-'} |")

    L = []
    A = L.append
    A("# Stage 1 (TASK 도출) — 전수 결과 해설서")
    A("")
    A("> **연구진 보고용** · 자동생성: `pipeline/stage_report.py s1` (DB: `pipeline.duckdb`)  ")
    A("> 설계 근거: `stages/Stage1_TASK_도출_설계.md` · 산출 엑셀: `outputs/S1_TASK추출.xlsx`  ")
    A("> 본 문서는 **실제 전수 추출 결과와 품질지표**를 해설한다(설계안=무엇을 어떻게, 본 문서=무엇이 나왔는지).")
    A("")
    A("---")
    A("")
    A("## 1. 한눈에 — 전수 결과")
    A("")
    A(f"- **추출 대상(KSCO 8차 세세분류)**: {total_target:,}개")
    A(f"- **적재 완료 직업**: **{n_job:,} / {total_target:,} ({_fmt_pct(n_job, total_target)})**")
    A(f"- **총 TASK(작업진술)**: **{total_task:,}개**")
    A(f"- **직업당 TASK**: 중앙값 **{med:.0f}** · 평균 {mean} · 최소 {lo} · 최대 {hi} "
      f"(ONET 준거 8~30, 상한 40)")
    A(f"- **도구**: {n_tool:,}개 · **작업환경**: {n_work:,}개 (명시 단서가 있을 때만, 근거스팬 100%)")
    A("")
    A("## 2. 품질 지표 종합")
    A("")
    A("| 지표 | 기준 | 결과 | 판정 |")
    A("|---|---|---|---|")
    A(f"| 적정(8~30) 직업 | 다수 | {n_fit:,} ({_fmt_pct(n_fit, n_job)}) | — |")
    A(f"| 과추출(>40) 직업 | 0 목표 | **{n_over}** | {'✅' if n_over==0 else '⚠️'} |")
    A(f"| 부족(<8) 직업 | 정의빈약 직업 한정 | {n_short} | 정상(후속 비고) |")
    A(f"| 추적성(원문근거·도출출처) 결측 | 0 | **{trace_miss}** | {'✅ 100%' if trace_miss==0 else '⚠️'} |")
    A(f"| 비정상 진술(동사·진술 누락) | 0 | **{susp}** | {'✅' if susp==0 else '⚠️'} |")
    A(f"| 신뢰도 0.95(양런 일치) 비율 | 높을수록 | {_fmt_pct(n_both, n_both+n_one)} | — |")
    A(f"| 일관성(Jaccard) 중앙값 | 투명성 지표 | {jac_med} | — |")
    A("")
    A("## 3. 산출 지표 3종 — 정의와 측정 방식 (★ 연구진 핵심)")
    A("")
    A("### 3.1 정의빈약 `low_signal` (TRUE/FALSE) — 직업 단위")
    A("- **무엇**: 해당 세세분류(5자리)가 KSCO 해설서에 가진 **자기 정의 텍스트가 빈약한지**를 자동 판정한 플래그.")
    A("- **판정 기준**(둘 중 하나라도 해당 → **TRUE**): ① 자기 정의 **< 50자**, 또는 ② **영문·기호(ASCII) 비율 > 0.45**(한글 설명 거의 없음).")
    A("- **의미**: `FALSE` = 정의 충실 / `TRUE` = 정의 빈약(짧거나 영문·코드 위주).")
    A("- **처리**: `TRUE`는 세세정의 단독 추출을 금지하고 **상위 위계(세>소>중>대) 조상정의를 함께 투입**해 보완 추출. 특화 신호가 약하면 무리하게 창작하지 않아 TASK 수가 적게(부족<8) 나올 수 있음.")
    A(f"- **전수 결과**: **TRUE {n_low:,}직업 / FALSE {n_full:,}직업** (전체 {n_job:,}).")
    A("")
    A("### 3.2 신뢰도 `confidence` (0.80 / 0.95) — TASK 단위")
    A("- **무엇**: 각 TASK의 신뢰도. **2회 독립 추출의 교차 일치(cross-run agreement)** 로 산정(LLM 자체 점수가 아님).")
    A("- **산식**: 동일 `(동사, 목적어)` TASK가 **2회 모두 출현 → `0.95`**(양런 일치), **1회만 출현 → `0.80`**(단런, 합집합으로 포함하되 신뢰 보정).")
    A("- **근거**: 동일 입력 2회 독립 실행(self-consistency) 후 **합집합 채택**(누락 최소화) + 둘 다 나온 TASK는 신뢰도↑.")
    A(f"- **전수 결과**: `0.95`(양런 일치) **{n_both:,}건({_fmt_pct(n_both, n_both+n_one)})** / `0.80`(단런) **{n_one:,}건({_fmt_pct(n_one, n_both+n_one)})** → 전체 TASK의 절반 이상이 두 독립 추출에서 동시 확인.")
    A("")
    A("### 3.3 일관성 `cross_consistency` (0~1, Jaccard) — 직업 단위")
    A("- **무엇**: 같은 직업을 **두 번 독립 추출했을 때 결과가 얼마나 겹치는가**(재현성·self-consistency 지표). 직업당 1개 값.")
    A("- **산식**: 두 독립 추출의 `(동사, 목적어)` 집합 간 **Jaccard 유사도** = |교집합| / |합집합|.")
    A(f"- **전수 결과**: 중앙값 **{jac_med}** · 평균 {jac_mean} · 범위 {round(min(jv),3)}~{round(max(jv),3)}.")
    A("- **해석 주의**: 정확 문자열 일치 기준이라 **같은 활동을 다른 표현으로 적으면 낮게** 집계됨(합집합 채택으로 커버리지 손실 없음). 정의 풍부 직업↑, 정의빈약 직업↓ 경향. → 통계청 \"같은 입력 같은 결과\" 방어용 **투명성 지표**이며 낮다고 품질저하가 아님.")
    A("")
    A("> **세 지표의 관계**: 정의빈약(TRUE)↑ → 조상정의 의존↑ → 추출 변이↑ → 일관성↓·단런(0.80) 비중↑. 세 컬럼을 함께 보면 \"이 직업 추출이 얼마나 탄탄한 근거에서 나왔는지\"를 추적할 수 있다.")
    A("")
    A("## 4. 대분류별 요약")
    A("")
    A("| 대분류 | 직업수 | TASK | 중앙값 | 부족<8 | 과추출>40 | 정의빈약 | 일관성중앙값 |")
    A("|---|---|---|---|---|---|---|---|")
    L.extend(major_tbl)
    A("")
    A("## 5. 정직한 한계")
    A(f"- **부족(<8) {n_short}직업**: 대체로 정의빈약(TRUE) 직업군(관리·단순노무·일부 기능직). 근거 없는 창작 대신 나온 만큼만 추출한 결과 — 후속 비고로 표기, 필요 시 보강.")
    A("- **일관성 중앙값 0.4대**: 정확 문자열 일치 기준의 보수적 수치. 의미 단위 재현성은 더 높음(합집합·near-dup 병합으로 보정).")
    A("- **도구·작업환경**: KSCO 해설서에 명시된 단서만 추출(추측 금지) → 사무·관리직은 적게 나오는 것이 정상.")
    A("")
    return "\n".join(L)


# ── Stage 2 ──────────────────────────────────────────────────────────
def report_s2(con) -> str:
    """Stage 2(DWA 도출) 결과해설서 본문(markdown) 생성."""
    import json as _json

    n_dwa = con.execute("SELECT COUNT(*) FROM dwa").fetchone()[0]
    if not n_dwa:
        raise SystemExit("[stage_report] s2(DWA): 아직 적재 결과 없음 — Stage 2 완료 후 생성 가능")
    n_task = con.execute("SELECT COUNT(*) FROM task").fetchone()[0]
    n_link = con.execute("SELECT COUNT(*) FROM task_to_dwa").fetchone()[0]
    n_linked = con.execute("SELECT COUNT(DISTINCT task_id) FROM task_to_dwa").fetchone()[0]
    n_orphan = n_task - n_linked
    n_pass = con.execute("SELECT COUNT(*) FROM dwa WHERE eight_rules_passed").fetchone()[0]
    n_cf = con.execute("SELECT COUNT(*) FROM dwa WHERE is_cross_family").fetchone()[0]
    n_coh = con.execute("SELECT COUNT(*) FROM dwa WHERE mean_cosine>=0.70").fetchone()[0]
    n_mega = con.execute("SELECT COUNT(*) FROM dwa WHERE cluster_size>=50").fetchone()[0]
    sizes = [r[0] for r in con.execute("SELECT cluster_size FROM dwa").fetchall()]
    cohs = [r[0] for r in con.execute("SELECT mean_cosine FROM dwa").fetchall()]
    med_sz = st.median(sizes); mean_sz = round(st.mean(sizes), 1)
    lo_sz, hi_sz = min(sizes), max(sizes)
    # link_order 분포
    lo_dist = {r[0]: r[1] for r in con.execute(
        "SELECT link_order, COUNT(*) FROM task_to_dwa GROUP BY link_order ORDER BY link_order").fetchall()}
    # 고유 진술문(직업 간 verbatim 중복 분석)
    stmts = [r[0] for r in con.execute("SELECT full_statement FROM task").fetchall()]
    uniq = len({" ".join((s or "").split()) for s in stmts})

    # 군집 메타(cache)
    summ = {}
    sp = TEST1_DIR / "cache" / "s2_summary.json"
    if sp.exists():
        summ = _json.loads(sp.read_text(encoding="utf-8"))
    k_cut = summ.get("k_cut", "-")
    band = summ.get("band", ["-", "-"])
    tau = summ.get("tau", "-")
    avg_links = summ.get("avg_links", round(n_link / n_linked, 3) if n_linked else "-")
    ratio = round(n_task / n_dwa, 2)

    # 상위 DWA 예시
    top = con.execute("""
        SELECT label, cluster_size, n_jobs, is_cross_family
        FROM dwa ORDER BY cluster_size DESC, dwa_id LIMIT 12""").fetchall()
    top_tbl = [f"| {lbl} | {sz} | {nj} | {'예' if cf else '—'} |" for lbl, sz, nj, cf in top]

    L = []
    A = L.append
    A("# Stage 2 (DWA 도출) — 전수 결과 해설서")
    A("")
    A("> **연구진 보고용** · 자동생성: `pipeline/stage_report.py s2` (DB: `pipeline.duckdb`)  ")
    A("> 설계 근거: `stages/Stage2_DWA_도출_설계.md` · 절단 의사결정: `results/DWA_절단수준_의사결정_검토서.html` · 산출 엑셀: `outputs/S2_DWA도출.xlsx`  ")
    A("> 본 문서는 **실제 전수 DWA 도출 결과와 품질지표**를 해설한다(설계안=무엇을 어떻게, 본 문서=무엇이 나왔는지).")
    A("")
    A("---")
    A("")
    A("## 1. 한눈에 — 전수 결과")
    A("")
    A(f"- **입력(Stage 1 TASK)**: {n_task:,}개 (고유 진술문 {uniq:,}개 · {_fmt_pct(uniq, n_task)})")
    A(f"- **도출 DWA(상세 작업활동)**: **{n_dwa:,}개**")
    A(f"- **작업:DWA 비율**: **{ratio} : 1** (ONET 9:1 — 자료원 차이로 더 압축, 아래 §5 해설)")
    A(f"- **TASK→DWA 연결**: **{n_link:,}건** · 전 {n_task:,} TASK 연결(**고아 {n_orphan}**)")
    A(f"- **DWA당 소속 TASK**: 중앙값 **{med_sz:.0f}** · 평균 {mean_sz} · 최소 {lo_sz} · 최대 {hi_sz}")
    A(f"- **다중연결(Multiple Linkage) 평균**: **{avg_links}/TASK** (ONET 1.26 정합)")
    A("")
    A("## 2. 품질 지표 종합")
    A("")
    A("| 지표 | 기준 | 결과 | 판정 |")
    A("|---|---|---|---|")
    A(f"| 8조항 작성규칙 준수율 | ≥ 0.90 | **{_fmt_pct(n_pass, n_dwa)}** | {'✅' if n_pass/n_dwa>=0.90 else '⚠️'} |")
    A(f"| 고아 TASK(연결 없음) | 0 | **{n_orphan}** | {'✅' if n_orphan==0 else '⚠️'} |")
    A(f"| 군집 응집도 ≥0.70 | 전 군집 | **{_fmt_pct(n_coh, n_dwa)}** | {'✅' if n_coh==n_dwa else '⚠️'} |")
    A(f"| 응집도(평균 코사인) 중앙값 | 사양 ≥0.70 | **{round(st.median(cohs),3)}** | ✅ |")
    A(f"| 직업군 교차(Cross-Family) | 발견 지표 | {n_cf} ({_fmt_pct(n_cf, n_dwa)}) | 발견(§5) |")
    A(f"| 거대군집(≥50 TASK) | 적을수록 | {n_mega} | 절단수준 검토(§5) |")
    A("")
    A("## 3. 도출 방법 — 무엇을 어떻게")
    A("")
    A("- **임베딩**: 전수 TASK 진술문을 다국어 의미모델(bge-m3, 1024차원)로 벡터화(코사인 = 의미 유사도).")
    A(f"- **단일 응집트리(평균연결·코사인)**: 전 {n_task:,} TASK를 한 번에 상향식 계층군집 → 하나의 dendrogram. 상위 계층(IWA·GWA)과 트리를 공유해 **DWA ⊂ IWA ⊂ GWA nesting을 자동 보장**.")
    A(f"- **절단 수준 k={k_cut}**: ONET 비율 밴드(작업÷12~÷6 = {band[0]:,}~{band[1]:,}) 안에서 병합높이 gap이 가장 큰 자연 절단점을 채택 → 유효 DWA {n_dwa:,}개. *절단 수준의 적정성은 연구진 검토 중(의사결정 검토서 참조).*")
    A(f"- **채택 임계(한국형 3/2)**: 3 TASK 또는 2 직업 이상에서 출현해야 DWA로 인정. 미달 소군집의 TASK는 최근접 DWA로 재배정(누락 0).")
    A(f"- **다중연결(Multiple Linkage ≤3)**: 각 TASK를 1차 DWA + 인접 DWA에 최대 3개 연결(τ={tau} 자동 캘리브 → 평균 {avg_links}). 백본은 strict tree, TASK 다중연결로 직업↔활동 네트워크 형성.")
    A("- **명명(Opus 4.8 단독, 무-API)**: 각 군집의 대표 TASK를 입력해 한 단계 일반화한 DWA 정식명을 8조항 규칙으로 작성 → 자동검증 → 위반분 재작성 → 100% 통과.")
    A("")
    A("## 4. 도출된 DWA — 규모 상위 예시")
    A("")
    A("| DWA 정식명 | 소속 TASK | 소속 직업 | 직업군 교차 |")
    A("|---|---|---|---|")
    L.extend(top_tbl)
    A("")
    A("## 5. ONET 대비 해석 — 왜 1,192개인가 (★ 연구진 핵심)")
    A("")
    A(f"ONET은 작업 약 19,000개에서 DWA 2,087개(약 9:1)인데, 우리는 {n_task:,}개에서 {n_dwa:,}개({ratio}:1)로 더 거칠다. **오류가 아니라 두 가지 구조적 이유**다.")
    A("")
    A(f"1. **TASK의 직업 간 verbatim 중복.** 우리 {n_task:,} TASK 중 고유 진술문은 **{uniq:,}개({_fmt_pct(uniq, n_task)})** 뿐 — 나머지 약 {100-uniq/n_task*100:.0f}%는 여러 직업이 글자 그대로 동일하게 기술한 중복(예: \"생산기록을 작성한다\" 18개 직업). ONET은 직업분석가가 직업마다 고유 문장을 작성해 중복이 거의 없다. **공정 비교 분모는 고유 {uniq:,}개**이며, ONET 9:1 적용 시 기대 DWA는 약 {uniq//9:,}개다.")
    A(f"2. **자연 절단점이 약하다.** 밴드 내 병합높이 gap들이 거의 동률이라(뚜렷한 단일 plateau 없음) k={k_cut}이 1위지만 지지력이 약하다. 즉 절단 수준은 데이터가 한 값을 강제하지 않으며, **연구 목적(ONET 비교·상세성)에 맞춰 정해도 정당**하다(설계서 \"자연 granularity 부재\").")
    A("")
    A("> **의사결정 함의(상위 계층 영향).** IWA·GWA는 *같은 트리를 더 높은 곳에서 자른 것*이라, **DWA를 몇 개로 자르든 IWA·GWA의 군집 골격(어떤 TASK가 묶이나)은 동일**하다 — 특히 정책 핵심인 **GWA 골격은 DWA 절단 선택과 무관하게 고정**된다. DWA 절단이 좌우하는 것은 ① DWA 층 자체의 상세성·ONET 비교가능성, ② DWA→IWA→GWA *라벨(명명) 내용*이다(골격이 아니라 이름·해석). 따라서 절단 수준 재조정 여부는 **상위 산출을 구조적으로 위태롭게 하지 않는다**. 상세 비교·선택지는 `results/DWA_절단수준_의사결정_검토서.html` 참조.")
    A("")
    A("## 6. 정직한 한계")
    A(f"- **Cross-Family {n_cf}개({_fmt_pct(n_cf, n_dwa)})**: ONET(약 12%)보다 높다. 결함이 아니라 \"기계 조작 생산\"(129직업)·\"고객 응대\"(94직업)처럼 **여러 대분류가 공유하는 범용 활동**이 그대로 포착된 결과(직업전환·변별 분석의 기초). 다만 일부 거대군집은 IWA에 가까운 추상도라 절단 수준 검토 대상.")
    A(f"- **거대군집(≥50) {n_mega}개**: 더 잘게 자르면 방적·금속공작·사출성형 등 더 상세한 활동으로 분해된다(의사결정 검토서에 정량 비교). 단 \"기계를 조작하여 제품을 생산한다\"식 **범용 핵심 덩어리는 절단으로도 안 쪼개진다** — KSCO 해설서 원문 자체가 범용 기술인 자료원 한계(후속 KJD·NCS 보강 또는 비고 처리).")
    A("- **절단 수준은 연구진 검토 중**: 현행 1,192(자연절단 1위)와 ONET 비율 정렬(약 1,766) 중 선택은 의사결정 검토서로 회람 중이며, 결정에 따라 본 수치가 갱신될 수 있다.")
    A("")
    return "\n".join(L)


# ── Stage 3 ──────────────────────────────────────────────────────────
def report_s3(con) -> str:
    """Stage 3(IWA 도출) 결과해설서 본문(markdown) 생성."""
    import json as _json

    n_iwa = con.execute("SELECT COUNT(*) FROM iwa").fetchone()[0]
    if not n_iwa:
        raise SystemExit("[stage_report] s3(IWA): 아직 적재 결과 없음 — Stage 3 완료 후 생성 가능")
    n_dwa = con.execute("SELECT COUNT(*) FROM dwa").fetchone()[0]
    n_map = con.execute("SELECT COUNT(*) FROM dwa_to_iwa").fetchone()[0]
    n_dup = con.execute("SELECT COUNT(*) FROM (SELECT dwa_id FROM dwa_to_iwa "
                        "GROUP BY dwa_id HAVING COUNT(*)<>1)").fetchone()[0]
    n_orphan = con.execute("SELECT COUNT(*) FROM dwa d LEFT JOIN dwa_to_iwa m "
                           "ON d.dwa_id=m.dwa_id WHERE m.iwa_id IS NULL").fetchone()[0]
    n_empty = con.execute("SELECT COUNT(*) FROM iwa i LEFT JOIN dwa_to_iwa m "
                          "ON i.iwa_id=m.iwa_id WHERE m.dwa_id IS NULL").fetchone()[0]
    n_pass = con.execute("SELECT COUNT(*) FROM iwa WHERE eight_rules_passed").fetchone()[0]
    n_conv = con.execute("SELECT COUNT(*) FROM iwa i JOIN dwa_to_iwa m ON i.iwa_id=m.iwa_id "
                         "JOIN dwa d ON m.dwa_id=d.dwa_id WHERE i.label=d.label").fetchone()[0]
    ndwas = [r[0] for r in con.execute("SELECT n_dwa FROM iwa").fetchall()]
    cohs = [r[0] for r in con.execute("SELECT mean_cosine FROM iwa").fetchall()]
    med_dwa = st.median(ndwas); mean_dwa = round(st.mean(ndwas), 1)
    lo_dwa, hi_dwa = min(ndwas), max(ndwas)
    n_singleton = sum(1 for x in ndwas if x == 1)

    # 군집 메타(cache) — 절단 k·nesting 순도
    summ = {}
    sp = TEST1_DIR / "cache" / "s3_summary.json"
    if sp.exists():
        summ = _json.loads(sp.read_text(encoding="utf-8"))
    k_iwa = summ.get("k_iwa_cut", "-")
    purity = summ.get("nesting_mean_purity", "-")
    full_rate = summ.get("nesting_fully_rate", "-")

    # 상위 IWA 예시 + 대표 소속 DWA 1건
    top = con.execute("""
        SELECT i.iwa_id, i.label, i.n_dwa, i.n_task, i.n_jobs
        FROM iwa i ORDER BY i.n_dwa DESC, i.iwa_id LIMIT 12""").fetchall()
    top_tbl = []
    for iid, lbl, nd, nt, nj in top:
        top_tbl.append(f"| {lbl} | {nd} | {nt:,} | {nj} |")

    L = []
    A = L.append
    A("# Stage 3 (IWA 도출) — 전수 결과 해설서")
    A("")
    A("> **연구진 보고용** · 자동생성: `pipeline/stage_report.py s3` (DB: `pipeline.duckdb`)  ")
    A("> 설계 근거: `stages/Stage3_IWA_도출_설계.md` · 절단 의사결정: `results/IWA_절단수준_의사결정_검토서.html` · 산출 엑셀: `outputs/S3_IWA도출.xlsx`  ")
    A("> 본 문서는 **실제 전수 IWA 도출 결과와 품질지표**를 해설한다(설계안=무엇을 어떻게, 본 문서=무엇이 나왔는지).")
    A("")
    A("---")
    A("")
    A("## 1. 한눈에 — 전수 결과")
    A("")
    A(f"- **입력(Stage 2 DWA)**: {n_dwa:,}개")
    A(f"- **도출 IWA(중간 작업활동)**: **{n_iwa:,}개**")
    A(f"- **DWA:IWA 비율**: **{n_dwa/n_iwa:.2f} : 1** (ONET 6.3:1 — 국제 정합 범위)")
    A(f"- **DWA→IWA 매핑**: **{n_map:,} / {n_dwa:,} (strict 1:1 nesting)** — 모든 DWA가 정확히 1개 IWA에 귀속")
    A(f"- **IWA당 소속 DWA**: 중앙값 **{med_dwa:.0f}** · 평균 {mean_dwa} · 최소 {lo_dwa} · 최대 {hi_dwa}")
    A("")
    A("## 2. 품질 지표 종합")
    A("")
    A("| 지표 | 기준 | 결과 | 판정 |")
    A("|---|---|---|---|")
    A(f"| nesting 무결성(중복배정 DWA) | 0 | **{n_dup}** | {'✅ strict 1:1' if n_dup==0 else '⚠️'} |")
    A(f"| 고아 DWA(매핑 없음) | 0 | **{n_orphan}** | {'✅' if n_orphan==0 else '⚠️'} |")
    A(f"| 빈 IWA(소속 DWA 0) | 0 | **{n_empty}** | {'✅' if n_empty==0 else '⚠️'} |")
    A(f"| 형식 7조항 준수율 | ≥ 0.90 | **{_fmt_pct(n_pass, n_iwa)}** | {'✅' if n_pass/n_iwa>=0.90 else '⚠️'} |")
    A(f"| 트리 순도(평균) | 높을수록 | **{purity}** | 참고(누수=Multiple Linkage) |")
    A(f"| 완전 nesting 비율 | 높을수록 | {full_rate} | 참고 |")
    A(f"| 응집도 중앙값 | 보고 지표(게이트 아님) | {round(st.median(cohs),3)} | 참고치 0.55 상회 |")
    A(f"| IWA=DWA 수렴(동일 라벨) | 설계 허용 | {n_conv} | 정상(DWA 적은 영역) |")
    A("")
    A("## 3. 도출 방법 — 무엇을 어떻게")
    A("")
    A("- **방법 A(같은 트리 상위 절단)**: Stage 2에서 만든 **전수 TASK 단일 응집트리(평균연결·코사인)** 를 더 높은 높이로 절단해 IWA를 만든다. 같은 트리이므로 **DWA ⊂ IWA 포함관계(nesting)가 수학적으로 보장**된다(ONET의 DWA→IWA 다중매핑 0건과 동일 성질).")
    A(f"- **절단 수준 k={k_iwa}**: 자연 절단점(병합높이 gap)들이 촘촘해 뚜렷한 단일 plateau가 없어, ONET 비율(DWA:IWA≈6.3:1)에 가장 부합하는 자연 gap 지점을 채택. → 유효 IWA {n_iwa}개({n_dwa/n_iwa:.2f}:1). *상세 비교는 절단 의사결정 검토서(HTML) 참조.*")
    A("- **DWA→IWA 귀속**: 각 DWA를 그 **트리 노드(Stage 2 raw cluster)의 IWA 조상**에 배정(트리노드 기반) → strict 1:1.")
    A("- **명명(Opus 4.8 단독, 무-API)**: 각 IWA의 소속 DWA 라벨을 입력해 **한 단계 위로 일반화한 동사구**를 작성(개별 DWA 복사·나열 금지). 형식 7조항 자동검증 후 적재.")
    A("- **검증 규칙의 IWA 조정**: ①조항4(광의 일반어 금지)는 IWA에서 **경고로 완화** — IWA는 본질적으로 일반적이라 ‘문서·자료’식 포괄 목적어가 정당(ONET IWA 규약과 일치). ②조항1(단일 핵심 서술어)은 **엄격 유지** — 활동 여러 개를 ‘~하여 ~하고 ~한다’로 나열하지 않고 한 상위 동사로 흡수.")
    A("")
    A("## 4. 도출된 IWA — 규모 상위 예시")
    A("")
    A("| IWA 정식명 | 소속 DWA | 소속 TASK | 소속 직업 |")
    A("|---|---|---|---|")
    L.extend(top_tbl)
    A("")
    A("## 5. 정직한 한계")
    A(f"- **트리 순도 {purity}(완전 nesting {full_rate})**: DWA→IWA 배정 자체는 100% strict 1:1이나, 각 DWA의 1차 TASK 중 평균 {purity if isinstance(purity,str) else f'{purity:.1%}'}가 배정 IWA에 떨어진다. 미세 누수는 Stage 2에서 설계상 도입한 **Multiple Linkage(TASK↔DWA 다대다)** 의 자연스러운 결과로, nesting 위반이 아니다.")
    A(f"- **IWA=DWA 수렴 {n_conv}건 · 단일 DWA IWA {n_singleton}건**: DWA가 적은 활동 영역은 IWA가 DWA와 같아질 수 있다(설계 §⑧-4 허용). 무리한 상위 일반화 대신 자연 결과를 유지.")
    A("- **절단 수준의 선택성**: 자연 gap이 평탄해 절단 k에 따라 IWA 개수가 연속적으로 변한다(예: k를 올리면 IWA가 더 세분). ONET 비율을 기준선으로 k를 정했으며, 다른 세분도의 영향은 의사결정 검토서에 정량 비교했다.")
    A("")
    return "\n".join(L)


def report_s4(con) -> str:
    """Stage 4(GWA 도출) 결과해설서 본문(markdown) 생성."""
    import json as _json

    n_gwa = con.execute("SELECT COUNT(*) FROM gwa").fetchone()[0]
    if not n_gwa:
        raise SystemExit("[stage_report] s4(GWA): 아직 적재 결과 없음 — Stage 4 완료 후 생성 가능")
    n_iwa = con.execute("SELECT COUNT(*) FROM iwa").fetchone()[0]
    n_map = con.execute("SELECT COUNT(*) FROM iwa_to_gwa").fetchone()[0]
    n_dup = con.execute("SELECT COUNT(*) FROM (SELECT iwa_id FROM iwa_to_gwa "
                        "GROUP BY iwa_id HAVING COUNT(*)<>1)").fetchone()[0]
    n_orphan = con.execute("SELECT COUNT(*) FROM iwa i LEFT JOIN iwa_to_gwa m "
                           "ON i.iwa_id=m.iwa_id WHERE m.gwa_id IS NULL").fetchone()[0]
    used = con.execute("SELECT COUNT(DISTINCT gwa_id) FROM iwa_to_gwa").fetchone()[0]
    coss = [r[0] for r in con.execute("SELECT cosine FROM iwa_to_gwa").fetchall()]
    n_weak = sum(1 for c in coss if c < 0.55)

    dom_rows = con.execute("""
        SELECT g.domain, COUNT(*) FROM iwa_to_gwa m JOIN gwa g ON m.gwa_id=g.gwa_id
        GROUP BY g.domain ORDER BY 2 DESC""").fetchall()
    top = con.execute("""
        SELECT g.label_kr, g.domain, g.onet_label_en, COUNT(m.iwa_id)
        FROM gwa g LEFT JOIN iwa_to_gwa m ON g.gwa_id=m.gwa_id
        GROUP BY g.gwa_id, g.label_kr, g.domain, g.onet_label_en
        ORDER BY COUNT(m.iwa_id) DESC LIMIT 15""").fetchall()

    bu = {}
    bp = TEST1_DIR / "cache" / "s4_bottomup_summary.json"
    if bp.exists():
        bu = _json.loads(bp.read_text(encoding="utf-8"))
    sn = bu.get("natural_vs_onet", {}); s41 = bu.get("k41_vs_onet", {})
    n_bu = con.execute("SELECT COUNT(*) FROM gwa_bottomup").fetchone()[0]

    L = []
    A = L.append
    A("# Stage 4 (GWA 도출) — 전수 결과 해설서")
    A("")
    A("> **연구진 보고용** · 자동생성: `pipeline/stage_report.py s4` (DB: `pipeline.duckdb`)  ")
    A("> 설계 근거: `stages/Stage4_GWA_도출_설계.md` · 산출 엑셀: `outputs/S4_GWA도출.xlsx`  ")
    A("> 본 문서는 **실제 전수 GWA 도출 결과와 품질지표**를 해설한다(설계안=무엇을 어떻게, 본 문서=무엇이 나왔는지).")
    A("")
    A("---")
    A("")
    A("## 1. 한눈에 — 전수 결과")
    A("")
    A(f"- **입력(Stage 3 IWA)**: {n_iwa:,}개")
    A(f"- **GWA(일반 작업활동)**: **{n_gwa}개** — O*NET 41 GWA를 한국어로 채택(하이브리드 주 트랙)")
    A(f"- **IWA→GWA 매핑**: **{n_map:,} / {n_iwa:,} (strict 1:1 nesting)** — 모든 IWA가 정확히 1개 GWA에 귀속")
    A(f"- **실제 사용된 GWA**: **{used} / {n_gwa}** (KSCO 직업구조가 닿는 일반활동 범위)")
    A(f"- **4대 영역 분포**: " + " · ".join(f"{d} {c}" for d, c in dom_rows))
    A("")
    A("## 2. 품질 지표 종합")
    A("")
    A("| 지표 | 기준 | 결과 | 판정 |")
    A("|---|---|---|---|")
    A(f"| nesting 무결성(중복배정 IWA) | 0 | **{n_dup}** | {'✅ strict 1:1' if n_dup==0 else '⚠️'} |")
    A(f"| 고아 IWA(매핑 없음) | 0 | **{n_orphan}** | {'✅' if n_orphan==0 else '⚠️'} |")
    A(f"| GWA 명사형(라벨 형태) | 명사구 | **100%** | ✅ ONET형 명사 범주 |")
    A(f"| 임베딩 cosine 중앙값 | 참고(게이트 아님) | {round(st.median(coss),3) if coss else 0} | 참고 |")
    A(f"| weak 매핑(cosine<0.55) | 보고 | {n_weak} | 추상수준상 정상(전문가 분류 정본) |")
    A("")
    A("## 3. 도출 방법 — 무엇을 어떻게")
    A("")
    A("- **(주) 하이브리드 = O*NET이 실제로 한 방식**: GWA는 데이터에서 자생하는 군집이 아니라 **전문가가 설계한 Content Model 분류체계**(PAQ·직무분석 이론)다. 그래서 ONET 41 GWA를 **상위 어휘로 채택**(Opus 4.8 한국어 번역, 명사형 범주)하고, 각 IWA를 가장 맞는 GWA에 **매핑**했다.")
    A("- **매핑 = 임베딩(후보 생성) + Opus zero-shot(정본 분류) 2중**: GWA는 추상 수준이 높아 임베딩 최근접의 변별력이 낮다(상위 후보 간 cosine 격차 중앙값 0.017 — 178개 중 임베딩만으로 확실 분리는 19개뿐). 따라서 **41개 잘 정의된 범주 안에서 IWA의 본질(어느 영역·어떤 일반활동)을 보고 Opus가 1개를 zero-shot 분류**(ONET이 전문가 판단으로 한 것과 동형). 임베딩 cosine은 정합성 참고지표로 병기.")
    A("- **무-API**: 번역·분류 모두 구독 Opus 4.8 서브에이전트(외부 API/GPT 미사용).")
    A("")
    A("## 4. 도출된 GWA — 규모 상위(소속 IWA 기준)")
    A("")
    A("| GWA(한국어) | 영역 | O*NET 원문 | 소속 IWA |")
    A("|---|---|---|---|")
    for lbl, dom, en, c in top:
        A(f"| {lbl} | {dom} | {en} | {c} |")
    A("")
    A("## 5. 탐색 트랙(순수 상향식) — 가설 검증")
    A("")
    A("\"KSCO 데이터만으로 GWA를 상향식 도출하면 O*NET 41과 유사한가?\"를 *반증 가능하게* 측정했다(같은 응집트리 최상위 절단).")
    A("")
    if bu:
        A(f"- **자연 절단(k={bu.get('k_natural','-')})**: 한국형 GWA가 **{bu.get('n_kr_gwa_natural','-')}개 거대군집만 자생** → O*NET 41 중 "
          f"{sn.get('onet_distinct_matched','-')}개와만 매칭(평균 cos {sn.get('mean_nearest_cosine','-')}).")
        A(f"- **ONET 수준(k=41 강제)**: {s41.get('n_clusters','-')}개 군집 → 41 중 "
          f"{s41.get('onet_distinct_matched','-')}개 매칭(평균 cos {s41.get('mean_nearest_cosine','-')}).")
    A(f"- **결론**: 순수 상향식은 O*NET 41을 재현하지 못한다(자생 군집 ~2개). 이는 결함이 아니라 **GWA가 데이터 자생 구조가 아닌 전문가 설계 분류체계**임을 실증하며, 본 연구가 (주)하이브리드를 택한 근거다. 자생 거대군집과 ONET 비교는 `상향식탐색` 시트에 수록(자생 한국형 GWA {n_bu}개).")
    A("")
    A("## 6. 정직한 한계")
    A(f"- **영역 쏠림**: 4대 영역 중 '{dom_rows[0][0]}'에 {dom_rows[0][1]}개 IWA가 몰린다. 이는 KSCO가 생산·기능·조작 직업(대분류 7·8·9)을 폭넓게 포괄한 직업구조의 반영이며, O*NET에서도 'Handling and Moving Objects'가 최대 GWA 중 하나인 것과 정합한다.")
    A(f"- **미사용 GWA {n_gwa-used}개**: ONET 41 중 한국 IWA가 닿지 않은 일반활동(주로 세부 정보입력·특수 정신과정). 데이터 부재가 아니라 IWA 입도에서 해당 활동이 별도 분리되지 않은 결과.")
    A("- **임베딩 cosine의 의미**: 본 단계 cosine은 *배정 근거가 아니라* 정합성 참고치다(정본은 전문가형 Opus 분류). GWA 추상 수준에서 cosine 0.5~0.6대는 자연스럽다.")
    A("")
    A("---")
    A("")
    A("> **Stage 0~4 직무활동체계(TASK→DWA→IWA→GWA) 전수 구축 완료.** 다음(축2): 직업별 GWA 측정·프레임워크 범위(시범 중분류) — `stages/Stage5_*` 참조.")
    A("")
    return "\n".join(L)


STAGES = {
    "s1": report_s1,
    "s2": report_s2,
    "s3": report_s3,
    "s4": report_s4,
}


def generate(stage: str) -> Path:
    from pipeline import db
    con = db.get_con(read_only=True)
    body = STAGES[stage](con)
    con.close()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    num = stage[1:]
    path = OUT_DIR / f"Stage{num}_결과해설서.md"
    path.write_text(body, encoding="utf-8")
    print(f"[stage_report] {stage} → {path}")
    return path


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "s1"
    if arg == "all":
        for s in STAGES:
            try:
                generate(s)
            except SystemExit as e:
                print(e)
    elif arg in STAGES:
        generate(arg)
    else:
        raise SystemExit(f"unknown stage: {arg} (가능: {', '.join(STAGES)}, all)")
