"""스테이지별 엑셀 산출양식 생성기 (이번 연구의 핵심 산출).

엑셀만 봐도 도출 과정이 추적되도록 시트·컬럼을 구성한다.
각 스테이지: export_s0 / export_s1 / export_s2 / export_s3 / export_s4 / export_network.
산출 경로: TEST1/outputs/

사용:
    python pipeline/export_excel.py s0
"""
from __future__ import annotations

import sys
from pathlib import Path

# 스크립트로 직접 실행해도 `import pipeline` 가능하게 TEST1 디렉터리를 path에 추가
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd

TEST1_DIR = Path(__file__).resolve().parents[1]
OUTPUTS = TEST1_DIR / "outputs"

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# 가독성: 컬럼 너비 상한
_MAX_W = 60


def _write(path: Path, sheets: dict[str, pd.DataFrame]) -> None:
    """여러 DataFrame을 시트별로 엑셀에 기록 + 컬럼 너비 자동조정."""
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(path, engine="openpyxl") as xw:
        for name, df in sheets.items():
            df.to_excel(xw, sheet_name=name, index=False)
            ws = xw.sheets[name]
            for i, col in enumerate(df.columns, 1):
                lengths = sorted(len(str(v)) for v in df[col].tolist()
                                 if v is not None and not (isinstance(v, float) and pd.isna(v)))
                body = lengths[int(len(lengths) * 0.9)] if lengths else 10
                width = max(len(str(col)), body)
                ws.column_dimensions[ws.cell(row=1, column=i).column_letter].width = min(width + 2, _MAX_W)
    print(f"[export] {path.relative_to(TEST1_DIR)}  ({sum(len(d) for d in sheets.values())} rows)")


# ── Stage 0 ──────────────────────────────────────────────────────────
_LEVEL_KR = {1: "대분류", 2: "중분류", 3: "소분류", 4: "세분류", 5: "세세분류"}


def _data_dictionary() -> pd.DataFrame:
    """데이터사전 — 각 시트·컬럼의 의미와 표기 규칙 가이드."""
    rows = [
        ("(개요)", "—", "통계청 제8차 KSCO 공식 HWPX(해설서·분류항목표)를 직접 파싱한 전처리 결과. 세세분류 1,270 전수.", ""),
        ("분류체계", "대/중/소/세/세세분류코드·명", "5단계 분류 위계 코드와 명칭(항목표 권위)", "예: 2 / 28 / 281 / 2812 / 28120"),
        ("분류체계", "세세정의", "세세분류(5자리) 자체 정의(해설서 개념)", "11~584자, 일부 빈약"),
        ("분류체계", "주요업무수", "해당 세세분류에 부여된 주요업무 항목 수(상속 포함)", "0~다수"),
        ("분류체계", "주요업무출처", "주요업무를 어디서 가져왔는지", "세세분류 자체보유 / 세분류 상속 / 없음"),
        ("분류체계", "예시수", "해설서 '▍직업 예시' 항목 수", "0~다수"),
        ("분류체계", "low_signal", "세세 정의가 빈약한가(50자 미만 또는 영문비율>45%) → 조상정의 보강 필요", "TRUE/FALSE"),
        ("분류체계", "valid", "추출 가능한가(주요업무 또는 세세/조상 정의 보유)", "TRUE/FALSE"),
        ("분류체계", "remarks", "처리 비고(상속·보강·불가 등)", ""),
        ("위계트리정의", "수준", "분류 단계", "대분류/중분류/소분류/세분류/세세분류"),
        ("위계트리정의", "정의", "각 수준의 해설서 정의(개념). 세세가 빈약해도 조상 정의로 맥락 보완", "대분류·중분류·소분류·세분류·세세분류 정의 모두 수록"),
        ("위계트리정의", "주요업무수", "해당 노드 자체 보유 주요업무 수(L4/L5에만 존재)", "0~다수"),
        ("추출컨텍스트", "추출컨텍스트", "Stage1 TASK 추출에 투입할 입력. 세세정의+조상정의(세>소>중>대) 결합", "[세세분류 …]\\n[세분류 …]…"),
        ("추출컨텍스트", "주요업무(결합)", "상속 적용된 주요업무 전체를 줄바꿈 결합", ""),
        ("주요업무", "출처/순번/주요업무", "세세분류별 주요업무 항목 펼침(상속 포함)", "출처=세세분류 자체보유/세분류 상속"),
        ("직업예시", "예시", "해당 세세분류의 직업 예시(해설서)", ""),
        ("커버리지요약", "—", "전체 지표 + 대분류별 집계", ""),
    ]
    return pd.DataFrame(rows, columns=["시트", "컬럼", "설명", "표기값/예시"])


def export_s0(records: list[dict], cov: dict, tree_rows: list[dict]) -> Path:
    """S0_전처리.xlsx — 데이터사전/분류체계/위계트리정의/추출컨텍스트/주요업무/직업예시/커버리지요약."""
    # 1) 분류체계 (개요)
    df_cls = pd.DataFrame([{
        "대분류코드": r["major_code"], "대분류명": r["major_name"],
        "중분류코드": r["mid_code"], "중분류명": r["mid_name"],
        "소분류코드": r["minor_code"], "소분류명": r["minor_name"],
        "세분류코드": r["broad_code"], "세분류명": r["broad_name"],
        "세세분류코드": r["ksco_code"], "세세분류명": r["name"],
        "세세정의": r["definition"],
        "주요업무수": len(r["main_tasks"]), "주요업무출처": r["main_tasks_source"],
        "예시수": len(r["examples"]),
        "low_signal": r["low_signal"], "valid": r["valid"], "remarks": r["remarks"],
    } for r in records])

    # 2) 위계트리정의 — 전 노드(대~세세)의 정의 (조상 설명 노출)
    df_tree = pd.DataFrame([{
        "코드": t["ksco_code"], "수준": _LEVEL_KR.get(t["level"], t["level"]),
        "명칭": t["name"], "상위코드": t["parent_code"] or "—",
        "대분류": t["major_name"], "정의": t["definition"] or "",
        "주요업무수": t["task_n"],
    } for t in tree_rows])

    # 3) 추출컨텍스트 — Stage1 입력
    df_ctx = pd.DataFrame([{
        "세세분류코드": r["ksco_code"], "세세분류명": r["name"],
        "low_signal": r["low_signal"], "추출컨텍스트": r["extraction_context"],
        "주요업무출처": r["main_tasks_source"],
        "주요업무(결합)": "\n".join(f"- {t}" for t in r["main_tasks"]),
    } for r in records])

    # 4) 주요업무 (펼침)
    df_tasks = pd.DataFrame([{
        "세세분류코드": r["ksco_code"], "세세분류명": r["name"],
        "출처": r["main_tasks_source"], "순번": i, "주요업무": t,
    } for r in records for i, t in enumerate(r["main_tasks"], 1)])

    # 5) 직업예시
    df_ex = pd.DataFrame([{
        "세세분류코드": r["ksco_code"], "세세분류명": r["name"], "순번": i, "예시": e,
    } for r in records for i, e in enumerate(r["examples"], 1)])

    # 6) 커버리지요약
    head = pd.DataFrame([
        {"지표": "총 세세분류", "값": cov["총_세세분류"]},
        {"지표": "추출가능(valid)", "값": cov["valid"]},
        {"지표": "valid율", "값": cov["valid율"]},
        {"지표": "세세정의 빈약(low_signal)", "값": cov["low_signal"]},
        {"지표": "주요업무 보유", "값": cov["주요업무보유"]},
        {"지표": "  └ 세세분류 자체보유", "값": cov["주요업무_self"]},
        {"지표": "  └ 세분류 상속", "값": cov["주요업무_parent"]},
        {"지표": "  └ 없음(정의로만 추출)", "값": cov["주요업무_none"]},
        {"지표": "주요업무보유율", "값": cov["주요업무보유율"]},
    ])
    df_major = pd.DataFrame(cov["by_major"])
    df_major["valid율"] = (df_major["valid"] / df_major["직업수"]).round(3)
    cols = df_major.columns
    spacer = pd.DataFrame([{c: "" for c in cols}])
    df_cov = pd.concat([
        head.rename(columns={"지표": cols[0], "값": cols[1]}).reindex(columns=cols).fillna(""),
        spacer, df_major,
    ], ignore_index=True)

    path = OUTPUTS / "S0_전처리.xlsx"
    _write(path, {
        "데이터사전": _data_dictionary(),
        "분류체계": df_cls,
        "위계트리정의": df_tree,
        "추출컨텍스트": df_ctx,
        "주요업무": df_tasks,
        "직업예시": df_ex,
        "커버리지요약": df_cov,
    })
    return path


def _run_s0() -> None:
    from pipeline import db, s0_preprocess as s0
    con = db.get_con(read_only=True)
    records = s0.build_all(con)
    cov = s0.coverage_report(records)
    # 위계트리정의용 전 노드 + 자체 주요업무 수
    tree_rows = con.execute("""
        SELECT n.ksco_code, n.level, n.name, n.parent_code, n.major_name, n.definition,
               COALESCE(t.cnt, 0) AS task_n
        FROM ksco_node n
        LEFT JOIN (SELECT ksco_code, COUNT(*) cnt FROM ksco_main_task GROUP BY ksco_code) t
          ON n.ksco_code = t.ksco_code
        ORDER BY n.level, n.ksco_code""").fetchall()
    keys = ["ksco_code", "level", "name", "parent_code", "major_name", "definition", "task_n"]
    tree = [dict(zip(keys, row)) for row in tree_rows]
    con.close()
    export_s0(records, cov, tree)
    print(f"  총 {cov['총_세세분류']} · valid {cov['valid']}({cov['valid율']:.1%}) · "
          f"low_signal {cov['low_signal']} · 주요업무 {cov['주요업무보유']}"
          f"({cov['주요업무보유율']:.1%}; 자체 {cov['주요업무_self']}/상속 {cov['주요업무_parent']}/없음 {cov['주요업무_none']})")


# ── Stage 1 ──────────────────────────────────────────────────────────
def _s1_data_dictionary() -> pd.DataFrame:
    rows = [
        ("(개요)", "—", "Stage 1 TASK 추출 결과. 세세분류별 TASK(동사+목적어)·도구·작업환경 3차원. Opus 4.8 2회 독립추출 합집합 + bge-m3 near-dup(cos≥0.9) 병합.", ""),
        ("(용어)", "TASK/DWA/IWA/GWA", "직무활동 4계층은 영문 표준 약어로 통일(혼용 금지). TASK=직무활동 단위(동사+목적어) → DWA(세부작업활동) → IWA(중간작업활동) → GWA(일반작업활동). 본 단계는 TASK.", "Stage1=TASK · Stage2=DWA · Stage3=IWA · Stage4=GWA"),
        ("TASK", "동사/목적어/TASK진술문", "단일 행동진술(동사 1개·~한다 종결). TASK진술문=full_statement", "예: 검토하다 / 도면 / 도면을 검토하여 형태를 확인한다"),
        ("TASK", "source_sentence(원문근거)", "그 TASK의 원문 근거 문장(추적)", "추출컨텍스트·주요업무 원문 발췌"),
        ("TASK", "derived_from", "도출 출처·경로(추적)", "상속 주요업무 / 세세분류 정의 / 조상정의(…)"),
        ("TASK", "confidence", "신뢰도(2회 모두 0.95·1회 0.80, 병합 시 대표값)", "0.0~1.0"),
        ("TASK", "extraction_runs/cross_consistency", "독립 추출 횟수 / 2회 (verb,object) Jaccard 일치율", "2 / 0~1"),
        ("도구", "name/category/evidence_span", "도구·시스템·장비명 + 분류 + 근거스팬", "category=HW/SW/도구/장비/시스템"),
        ("작업환경", "category/value/evidence_span", "작업환경 단서 + 근거스팬", "category=장소/위험/사회적/신체적/시간적"),
        ("직업별요약", "task수/8~30충족", "직업당 TASK 개수와 ONET 준거(8~30 목표·40 상한) 충족여부", "적정/부족/과추출"),
        ("커버리지", "—", "전체 직업·TASK 집계 + 개수 분포", ""),
    ]
    return pd.DataFrame(rows, columns=["시트", "컬럼", "설명", "표기값/예시"])


def export_s1(scope=None) -> Path:
    """S1_TASK추출.xlsx — 데이터사전/TASK/도구/작업환경/직업별요약/커버리지."""
    import statistics
    from pipeline import db, s0_preprocess as s0

    con = db.get_con(read_only=True)
    where, params = "", []
    if scope:
        prefixes = tuple(str(s) for s in scope)
        where = " WHERE " + " OR ".join(["t.ksco_code LIKE ?"] * len(prefixes))
        params = [f"{p}%" for p in prefixes]

    df_task = con.execute(f"""
        SELECT n.parent_code 세분류코드, b.name 세분류명,
               t.ksco_code 세세분류코드, n.name 세세분류명, t.verb 동사, t.object 목적어,
               t.full_statement "TASK진술문", t.source_sentence 원문근거, t.derived_from 도출출처,
               t.confidence 신뢰도, t.extraction_runs 추출횟수, t.cross_consistency 일관성,
               t.source 출처, t.source_subject 원직업명, t.low_signal 정의빈약
        FROM task t LEFT JOIN ksco_node n ON t.ksco_code = n.ksco_code
                    LEFT JOIN ksco_node b ON n.parent_code = b.ksco_code
        {where} ORDER BY t.ksco_code, t.task_id""", params).df()
    df_tool = con.execute(f"""
        SELECT n.parent_code 세분류코드, b.name 세분류명,
               t.ksco_code 세세분류코드, n.name 세세분류명, t.name 도구명,
               t.category 분류, t.evidence_span 근거스팬, t.confidence 신뢰도
        FROM tool_inventory t LEFT JOIN ksco_node n ON t.ksco_code = n.ksco_code
                              LEFT JOIN ksco_node b ON n.parent_code = b.ksco_code
        {where} ORDER BY t.ksco_code, t.tool_id""", params).df()
    df_work = con.execute(f"""
        SELECT n.parent_code 세분류코드, b.name 세분류명,
               t.ksco_code 세세분류코드, n.name 세세분류명, t.category 분류,
               t.value 단서, t.evidence_span 근거스팬, t.confidence 신뢰도
        FROM work_context t LEFT JOIN ksco_node n ON t.ksco_code = n.ksco_code
                            LEFT JOIN ksco_node b ON n.parent_code = b.ksco_code
        {where} ORDER BY t.ksco_code, t.context_id""", params).df()

    # 직업별 요약 (DB 카운트 + S0 출처분기·low_signal)
    codes = [r[0] for r in con.execute(
        f"SELECT DISTINCT t.ksco_code FROM task t {where} ORDER BY t.ksco_code",
        params).fetchall()]
    cache = s0._load_caches(con)
    sum_rows = []
    for c in codes:
        rec = s0.build_record(con, c, cache)
        ntask = int(con.execute("SELECT COUNT(*) FROM task WHERE ksco_code=?", [c]).fetchone()[0])
        ntool = int(con.execute("SELECT COUNT(*) FROM tool_inventory WHERE ksco_code=?", [c]).fetchone()[0])
        nwork = int(con.execute("SELECT COUNT(*) FROM work_context WHERE ksco_code=?", [c]).fetchone()[0])
        jac = con.execute("SELECT MAX(cross_consistency) FROM task WHERE ksco_code=?", [c]).fetchone()[0]
        fit = "적정" if 8 <= ntask <= 30 else ("부족" if ntask < 8 else ("상한근접" if ntask <= 40 else "과추출"))
        sum_rows.append({
            "세분류코드": rec["broad_code"], "세분류명": rec["broad_name"],
            "세세분류코드": c, "세세분류명": rec["name"], "주요업무출처": rec["main_tasks_source"],
            "정의빈약": rec["low_signal"], "TASK수": ntask, "8~30충족": fit,
            "도구수": ntool, "작업환경수": nwork, "일관성(jaccard)": jac})
    df_sum = pd.DataFrame(sum_rows)

    # 커버리지
    counts = [r["TASK수"] for r in sum_rows]
    cov_rows = [
        {"지표": "추출 직업 수", "값": len(codes)},
        {"지표": "총 TASK 수", "값": int(sum(counts)) if counts else 0},
        {"지표": "직업당 평균", "값": round(statistics.mean(counts), 1) if counts else 0},
        {"지표": "직업당 중앙값", "값": statistics.median(counts) if counts else 0},
        {"지표": "최소 / 최대", "값": f"{min(counts)} / {max(counts)}" if counts else "0 / 0"},
        {"지표": "8 미만(부족) 직업", "값": sum(1 for x in counts if x < 8)},
        {"지표": "8~30(적정) 직업", "값": sum(1 for x in counts if 8 <= x <= 30)},
        {"지표": "40 초과(과추출) 직업", "값": sum(1 for x in counts if x > 40)},
        {"지표": "총 도구 수", "값": int(len(df_tool))},
        {"지표": "총 작업환경 수", "값": int(len(df_work))},
    ]
    df_cov = pd.DataFrame(cov_rows)
    con.close()

    path = OUTPUTS / "S1_TASK추출.xlsx"
    _write(path, {
        "데이터사전": _s1_data_dictionary(),
        "TASK": df_task, "도구": df_tool, "작업환경": df_work,
        "직업별요약": df_sum, "커버리지": df_cov,
    })
    print(f"  직업 {len(codes)} · TASK {int(sum(counts)) if counts else 0} · "
          f"중앙값 {statistics.median(counts) if counts else 0} · "
          f"부족 {sum(1 for x in counts if x < 8)} · 과추출 {sum(1 for x in counts if x > 40)}")
    return path


def _run_s1(scope=None) -> None:
    export_s1(scope)


# ── Stage 2 ──────────────────────────────────────────────────────────
def _s2_data_dictionary() -> pd.DataFrame:
    rows = [
        ("(개요)", "—", "Stage 2 DWA(상세 작업활동) 도출 결과. 전수 16,168 TASK를 bge-m3 임베딩→평균연결·코사인 단일 응집트리→ONET밴드 자연절단→채택임계(한국형 3/2)→Multiple Linkage(≤3)로 군집. Opus 4.8 단독 8조항 명명.", ""),
        ("(용어)", "TASK/DWA/IWA/GWA", "직무활동 4계층 표준 약어(혼용 금지). DWA=여러 직업·여러 TASK가 공유하는 중간 추상 작업활동.", "Stage2=DWA"),
        ("DWA", "label(정식명)", "8조항 준수 DWA 진술(동사 단일·~한다 종결·중간추상도)", "예: 재무기록을 조사하여 재무제표를 작성한다"),
        ("DWA", "cluster_size/n_jobs", "1차연결 소속 TASK 수 / 소속 직업 수", "채택임계: ≥3 TASK 또는 ≥2 직업"),
        ("DWA", "mean_cosine(응집도)", "멤버-중심 평균 코사인(≥0.70 양호)", "0~1"),
        ("DWA", "eight_rules_passed", "8조항 자동검증 통과(하드조항)", "TRUE/FALSE"),
        ("DWA", "is_cross_family", "서로 다른 대분류 직업이 묶임(직업전환·변별 기초)", "TRUE/FALSE"),
        ("TASK-DWA연결", "link_order", "Multiple Linkage 순위(1=주연결, 2~3=인접DWA)", "1~3"),
        ("DWA별TASK", "—", "DWA → 소속 TASK → 직업 역추적(주연결 link_order=1)", ""),
        ("커버리지", "—", "DWA 수·비율·응집도·cross-family 집계", ""),
    ]
    return pd.DataFrame(rows, columns=["시트", "컬럼", "설명", "표기값/예시"])


def export_s2(scope=None) -> Path:
    """S2_DWA도출.xlsx — 데이터사전/DWA/TASK-DWA연결/DWA별TASK/커버리지."""
    import statistics
    from pipeline import db

    con = db.get_con(read_only=True)
    df_dwa = con.execute("""
        SELECT dwa_id "DWA코드", label "DWA정식명", definition 정의,
               cluster_size "소속TASK수", n_jobs 소속직업수, mean_cosine "응집도(코사인)",
               eight_rules_passed "8조항통과", is_cross_family "직업군교차"
        FROM dwa ORDER BY cluster_size DESC, dwa_id""").df()

    # TASK-DWA 연결 + TASK/직업 추적
    df_link = con.execute("""
        SELECT l.dwa_id "DWA코드", d.label "DWA정식명", l.link_order 연결순위,
               l.task_id "TASK코드", t.ksco_code 세세분류코드, nn.name 세세분류명,
               t.full_statement "TASK진술문"
        FROM task_to_dwa l
        JOIN dwa d ON l.dwa_id = d.dwa_id
        JOIN task t ON l.task_id = t.task_id
        LEFT JOIN ksco_node nn ON t.ksco_code = nn.ksco_code
        ORDER BY l.dwa_id, l.link_order, l.task_id""").df()

    # DWA별 TASK(주연결만) — 역추적 펼침
    df_members = con.execute("""
        SELECT l.dwa_id "DWA코드", d.label "DWA정식명",
               t.ksco_code 세세분류코드, nn.name 세세분류명, t.full_statement "TASK진술문"
        FROM task_to_dwa l
        JOIN dwa d ON l.dwa_id = d.dwa_id
        JOIN task t ON l.task_id = t.task_id
        LEFT JOIN ksco_node nn ON t.ksco_code = nn.ksco_code
        WHERE l.link_order = 1
        ORDER BY l.dwa_id, t.ksco_code""").df()

    n_dwa = int(con.execute("SELECT COUNT(*) FROM dwa").fetchone()[0])
    n_task_linked = int(con.execute(
        "SELECT COUNT(DISTINCT task_id) FROM task_to_dwa").fetchone()[0])
    n_total_task = int(con.execute("SELECT COUNT(*) FROM task").fetchone()[0])
    n_links = int(con.execute("SELECT COUNT(*) FROM task_to_dwa").fetchone()[0])
    n_pass = int(con.execute(
        "SELECT COUNT(*) FROM dwa WHERE eight_rules_passed").fetchone()[0])
    n_cf = int(con.execute("SELECT COUNT(*) FROM dwa WHERE is_cross_family").fetchone()[0])
    n_coh = int(con.execute("SELECT COUNT(*) FROM dwa WHERE mean_cosine>=0.70").fetchone()[0])
    sizes = [r[0] for r in con.execute("SELECT cluster_size FROM dwa").fetchall()]
    cohs = [r[0] for r in con.execute("SELECT mean_cosine FROM dwa").fetchall()]
    con.close()

    cov_rows = [
        {"지표": "DWA 수", "값": n_dwa},
        {"지표": "TASK:DWA 비율", "값": round(n_total_task / n_dwa, 2) if n_dwa else 0},
        {"지표": "연결된 TASK 수", "값": f"{n_task_linked} / {n_total_task}"},
        {"지표": "총 연결 수(Multiple Linkage)", "값": n_links},
        {"지표": "TASK당 평균 연결", "값": round(n_links / n_task_linked, 3) if n_task_linked else 0},
        {"지표": "DWA당 평균 TASK", "값": round(statistics.mean(sizes), 1) if sizes else 0},
        {"지표": "DWA당 중앙값 TASK", "값": statistics.median(sizes) if sizes else 0},
        {"지표": "8조항 통과", "값": f"{n_pass} ({n_pass/n_dwa:.1%})" if n_dwa else 0},
        {"지표": "응집도≥0.70", "값": f"{n_coh} ({n_coh/n_dwa:.1%})" if n_dwa else 0},
        {"지표": "응집도 중앙값", "값": round(statistics.median(cohs), 3) if cohs else 0},
        {"지표": "직업군 교차(cross-family)", "값": f"{n_cf} ({n_cf/n_dwa:.1%})" if n_dwa else 0},
    ]
    df_cov = pd.DataFrame(cov_rows)

    path = OUTPUTS / "S2_DWA도출.xlsx"
    _write(path, {
        "데이터사전": _s2_data_dictionary(),
        "DWA": df_dwa,
        "TASK-DWA연결": df_link,
        "DWA별TASK": df_members,
        "커버리지": df_cov,
    })
    print(f"  DWA {n_dwa} · 연결 {n_links} · 8조항통과 {n_pass} · cross-family {n_cf}")
    return path


def _run_s2(scope=None) -> None:
    export_s2(scope)


def _s3_data_dictionary() -> pd.DataFrame:
    rows = [
        ("(개요)", "—", "Stage 3 IWA(중간 작업활동) 도출 결과. Stage 2와 같은 TASK 응집트리를 더 높은 높이로 절단(방법 A·k=214)→DWA를 그 IWA 조상에 배정(트리노드 기반). DWA⊂IWA strict 1:1 nesting. Opus 4.8 단독 명명(소속 DWA 라벨 일반화).", ""),
        ("(용어)", "TASK/DWA/IWA/GWA", "직무활동 4계층 표준 약어(혼용 금지). IWA=여러 DWA를 포괄하는 한 단계 위 일반 작업활동(DWA 상세 ↔ GWA 일반의 다리).", "Stage3=IWA"),
        ("IWA", "label(정식명)", "ONET 규약 동사구·일반(소속 DWA보다 일반, 단일 핵심서술어 ~한다 종결)", "예: 전문 분야를 연구하여 기술·제품을 개발한다"),
        ("IWA", "n_dwa/n_task/n_jobs", "소속 DWA 수 / 소속 TASK 수 / 소속 직업 수", "IWA당 평균 DWA ~6.7(ONET 6.3:1)"),
        ("IWA", "mean_cosine(응집도)", "소속 DWA 중심-IWA중심 평균 코사인(보고 지표, 게이트 아님)", "참고치 ~0.55"),
        ("IWA", "eight_rules_passed", "형식 7조항 자동검증 통과(R4 광의일반어는 IWA서 경고로 완화)", "TRUE/FALSE"),
        ("DWA-IWA연결", "—", "각 DWA → 정확히 1 IWA(strict nesting). 중복·고아 0.", ""),
        ("IWA별DWA", "—", "IWA → 소속 DWA → (TASK·직업) 역추적", ""),
        ("커버리지", "—", "IWA 수·DWA:IWA 비율·nesting 무결성·응집도 집계", ""),
    ]
    return pd.DataFrame(rows, columns=["시트", "컬럼", "설명", "표기값/예시"])


def export_s3(scope=None) -> Path:
    """S3_IWA도출.xlsx — 데이터사전/IWA/DWA-IWA연결/IWA별DWA/커버리지."""
    import statistics
    from pipeline import db

    con = db.get_con(read_only=True)
    df_iwa = con.execute("""
        SELECT iwa_id "IWA코드", label "IWA정식명", definition 정의,
               n_dwa "소속DWA수", n_task "소속TASK수", n_jobs 소속직업수,
               mean_cosine "응집도(코사인)", eight_rules_passed "7조항통과"
        FROM iwa ORDER BY n_dwa DESC, iwa_id""").df()

    # DWA→IWA 연결(1:1) + DWA 라벨
    df_link = con.execute("""
        SELECT m.iwa_id "IWA코드", i.label "IWA정식명",
               m.dwa_id "DWA코드", d.label "DWA정식명",
               d.cluster_size "DWA소속TASK수", d.n_jobs "DWA소속직업수"
        FROM dwa_to_iwa m
        JOIN iwa i ON m.iwa_id = i.iwa_id
        JOIN dwa d ON m.dwa_id = d.dwa_id
        ORDER BY m.iwa_id, d.cluster_size DESC""").df()

    # IWA별 소속 DWA(역추적 펼침)
    df_members = df_link.copy()

    n_iwa = int(con.execute("SELECT COUNT(*) FROM iwa").fetchone()[0])
    n_dwa = int(con.execute("SELECT COUNT(*) FROM dwa").fetchone()[0])
    n_map = int(con.execute("SELECT COUNT(*) FROM dwa_to_iwa").fetchone()[0])
    n_dup = int(con.execute("SELECT COUNT(*) FROM (SELECT dwa_id FROM dwa_to_iwa "
                            "GROUP BY dwa_id HAVING COUNT(*)<>1)").fetchone()[0])
    n_orphan = int(con.execute("SELECT COUNT(*) FROM dwa d LEFT JOIN dwa_to_iwa m "
                               "ON d.dwa_id=m.dwa_id WHERE m.iwa_id IS NULL").fetchone()[0])
    n_pass = int(con.execute(
        "SELECT COUNT(*) FROM iwa WHERE eight_rules_passed").fetchone()[0])
    n_conv = int(con.execute("SELECT COUNT(*) FROM iwa i JOIN dwa_to_iwa m ON i.iwa_id=m.iwa_id "
                             "JOIN dwa d ON m.dwa_id=d.dwa_id WHERE i.label=d.label").fetchone()[0])
    ndwas = [r[0] for r in con.execute("SELECT n_dwa FROM iwa").fetchall()]
    cohs = [r[0] for r in con.execute("SELECT mean_cosine FROM iwa").fetchall()]
    con.close()

    cov_rows = [
        {"지표": "IWA 수", "값": n_iwa},
        {"지표": "DWA:IWA 비율", "값": round(n_dwa / n_iwa, 2) if n_iwa else 0},
        {"지표": "ONET DWA:IWA(참고)", "값": "6.3:1"},
        {"지표": "DWA→IWA 매핑 수", "값": f"{n_map} / {n_dwa}"},
        {"지표": "nesting 무결성(중복배정 DWA)", "값": f"{n_dup} (0=strict 1:1)"},
        {"지표": "고아 DWA(매핑없음)", "값": n_orphan},
        {"지표": "IWA당 평균 DWA", "값": round(statistics.mean(ndwas), 1) if ndwas else 0},
        {"지표": "IWA당 중앙값 DWA", "값": statistics.median(ndwas) if ndwas else 0},
        {"지표": "7조항 통과(R4완화)", "값": f"{n_pass} ({n_pass/n_iwa:.1%})" if n_iwa else 0},
        {"지표": "응집도 중앙값", "값": round(statistics.median(cohs), 3) if cohs else 0},
        {"지표": "IWA=DWA 수렴(동일라벨)", "값": f"{n_conv} (DWA적은 영역, 설계 허용)"},
    ]
    df_cov = pd.DataFrame(cov_rows)

    path = OUTPUTS / "S3_IWA도출.xlsx"
    _write(path, {
        "데이터사전": _s3_data_dictionary(),
        "IWA": df_iwa,
        "DWA-IWA연결": df_link,
        "IWA별DWA": df_members,
        "커버리지": df_cov,
    })
    print(f"  IWA {n_iwa} · 매핑 {n_map} · 7조항통과 {n_pass} · nesting중복 {n_dup}")
    return path


def _run_s3(scope=None) -> None:
    export_s3(scope)


# ── Stage 4 ──────────────────────────────────────────────────────────
def _s4_data_dictionary() -> pd.DataFrame:
    rows = [
        ("(개요)", "—", "Stage 4 GWA(일반 작업활동) 도출 결과. 2트랙. (주)하이브리드=ONET 41 GWA를 한국어로 채택(Opus 번역)하고 각 IWA를 Opus zero-shot으로 41 중 1개에 배정(임베딩은 후보 생성·cosine 기록). (탐색)순수 상향식=같은 응집트리 최상위 절단으로 한국형 GWA 자생→ONET 41 일치도 비교(가설 검증).", ""),
        ("(용어)", "TASK/DWA/IWA/GWA", "직무활동 4계층 표준 약어(혼용 금지). GWA=직업·산업 무관 가장 일반적인 작업활동 범주(최상위). ONET 41개·4대 영역. 형태는 명사형.", "Stage4=GWA"),
        ("(방법주석)", "임베딩 vs 전문가매핑", "GWA는 데이터 군집이 아니라 전문가 설계 분류체계(ONET Content Model). 추상 수준이 높아 임베딩 최근접의 변별력이 낮음(상위후보 간 cosine 격차 중앙값 0.017) → ONET이 실제로 한 방식(전문가 매핑)대로 Opus가 41 중 1개를 zero-shot 분류. 임베딩 cosine은 정합성 참고지표로 병기.", ""),
        ("GWA", "label_kr/onet_label_en/domain", "ONET 41 GWA 한국어 정식명(명사형)·원문영문·4대영역(정보입력/정신과정/작업산출/타인상호작용)", ""),
        ("GWA", "source/소속IWA수", "GWA 출처(ONET_adopt=주트랙) / 이 GWA에 배정된 IWA 수", "ONET_adopt"),
        ("IWA-GWA연결", "cosine/method", "IWA↔배정GWA 임베딩 코사인(참고) / 배정 방법(llm=Opus zero-shot 정본)", "method=llm"),
        ("GWA별IWA", "—", "GWA → 소속 IWA → (DWA·TASK·직업) 역추적", ""),
        ("상향식탐색", "—", "(탐색 트랙) KSCO만으로 자생한 한국형 GWA 군집과 ONET 41 최근접 비교. 자연절단이 ~2개 거대군집만 산출 → GWA는 상향식으로 재현 불가(전문가 설계)임을 실증. 가설 검증 결과.", ""),
        ("커버리지", "—", "GWA 수·사용 GWA·영역분포·nesting 무결성·상향식 비교 집계", ""),
    ]
    return pd.DataFrame(rows, columns=["시트", "컬럼", "설명", "표기값/예시"])


def export_s4(scope=None) -> Path:
    """S4_GWA도출.xlsx — 데이터사전/GWA/IWA-GWA연결/GWA별IWA/상향식탐색/커버리지."""
    import json as _json
    import statistics
    from pipeline import db

    con = db.get_con(read_only=True)
    df_gwa = con.execute("""
        SELECT g.gwa_id "GWA코드", g.label_kr "GWA정식명(한국어)",
               g.onet_label_en "ONET원문(영문)", g.domain 영역,
               g.source 출처, COALESCE(c.n, 0) "소속IWA수"
        FROM gwa g
        LEFT JOIN (SELECT gwa_id, COUNT(*) n FROM iwa_to_gwa GROUP BY gwa_id) c
          ON g.gwa_id = c.gwa_id
        ORDER BY c.n DESC NULLS LAST, g.gwa_id""").df()

    df_link = con.execute("""
        SELECT m.gwa_id "GWA코드", g.label_kr "GWA정식명", g.domain 영역,
               m.iwa_id "IWA코드", i.label "IWA정식명",
               i.n_dwa "IWA소속DWA수", i.n_task "IWA소속TASK수", i.n_jobs "IWA소속직업수",
               m.cosine "임베딩cosine(참고)", m.method 배정방법
        FROM iwa_to_gwa m
        JOIN gwa g ON m.gwa_id = g.gwa_id
        JOIN iwa i ON m.iwa_id = i.iwa_id
        ORDER BY m.gwa_id, i.n_dwa DESC""").df()

    df_members = df_link.copy()

    df_bu = con.execute("""
        SELECT kr_gwa_id "한국형GWA코드", label_kr "한국형GWA명(자생)",
               n_iwa "소속IWA수", nearest_onet "최근접ONET코드",
               cosine "최근접cosine"
        FROM gwa_bottomup ORDER BY n_iwa DESC""").df()
    # 최근접 ONET 라벨 부착
    if len(df_bu):
        on = {r[0]: r[1] for r in con.execute("SELECT gwa_id, label_kr FROM gwa").fetchall()}
        df_bu.insert(4, "최근접ONET명", df_bu["최근접ONET코드"].map(on))

    n_gwa = int(con.execute("SELECT COUNT(*) FROM gwa").fetchone()[0])
    n_map = int(con.execute("SELECT COUNT(*) FROM iwa_to_gwa").fetchone()[0])
    n_iwa = int(con.execute("SELECT COUNT(*) FROM iwa").fetchone()[0])
    used = int(con.execute("SELECT COUNT(DISTINCT gwa_id) FROM iwa_to_gwa").fetchone()[0])
    n_dup = int(con.execute("SELECT COUNT(*) FROM (SELECT iwa_id FROM iwa_to_gwa "
                            "GROUP BY iwa_id HAVING COUNT(*)<>1)").fetchone()[0])
    n_orphan = int(con.execute("SELECT COUNT(*) FROM iwa i LEFT JOIN iwa_to_gwa m "
                               "ON i.iwa_id=m.iwa_id WHERE m.gwa_id IS NULL").fetchone()[0])
    dom_rows = con.execute("""
        SELECT g.domain, COUNT(*) FROM iwa_to_gwa m JOIN gwa g ON m.gwa_id=g.gwa_id
        GROUP BY g.domain ORDER BY 2 DESC""").fetchall()
    coss = [r[0] for r in con.execute("SELECT cosine FROM iwa_to_gwa").fetchall()]

    # 상향식 비교 요약(cache)
    bu = {}
    bp = TEST1_DIR / "cache" / "s4_bottomup_summary.json"
    if bp.exists():
        bu = _json.loads(bp.read_text(encoding="utf-8"))
    con.close()

    cov_rows = [
        {"지표": "GWA 수(ONET 채택)", "값": n_gwa},
        {"지표": "IWA→GWA 매핑", "값": f"{n_map} / {n_iwa}"},
        {"지표": "사용된 GWA", "값": f"{used} / {n_gwa}"},
        {"지표": "nesting 무결성(중복배정 IWA)", "값": f"{n_dup} (0=strict 1:1)"},
        {"지표": "고아 IWA(매핑 없음)", "값": n_orphan},
        {"지표": "임베딩 cosine 중앙값(참고)", "값": round(statistics.median(coss), 3) if coss else 0},
        {"지표": "배정 방법", "값": "Opus zero-shot 전수(임베딩=후보·cosine 기록)"},
    ]
    for d, c in dom_rows:
        cov_rows.append({"지표": f"  영역 · {d}", "값": f"{c} IWA"})
    if bu:
        sn = bu.get("natural_vs_onet", {}); s41 = bu.get("k41_vs_onet", {})
        cov_rows += [
            {"지표": "─ 상향식 탐색(가설 검증) ─", "값": ""},
            {"지표": "자연절단 k", "값": bu.get("k_natural", "-")},
            {"지표": "자생 한국형 GWA(자연)", "값": bu.get("n_kr_gwa_natural", "-")},
            {"지표": "자연 vs ONET 매칭", "값": f"{sn.get('onet_distinct_matched','-')}/41 "
             f"(평균cos {sn.get('mean_nearest_cosine','-')})"},
            {"지표": "k=41 강제 vs ONET 매칭", "값": f"{s41.get('onet_distinct_matched','-')}/41 "
             f"(평균cos {s41.get('mean_nearest_cosine','-')})"},
            {"지표": "해석", "값": "순수 상향식은 ~2개 거대군집만 자생 → GWA는 전문가 설계 분류(하이브리드 채택 정당)"},
        ]
    df_cov = pd.DataFrame(cov_rows)

    path = OUTPUTS / "S4_GWA도출.xlsx"
    sheets = {
        "데이터사전": _s4_data_dictionary(),
        "GWA": df_gwa,
        "IWA-GWA연결": df_link,
        "GWA별IWA": df_members,
        "커버리지": df_cov,
    }
    if len(df_bu):
        sheets["상향식탐색"] = df_bu
    _write(path, sheets)
    print(f"  GWA {n_gwa} · 매핑 {n_map}/{n_iwa} · 사용 {used} · nesting중복 {n_dup}")
    return path


def _run_s4(scope=None) -> None:
    export_s4(scope)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "s0"
    scope = sys.argv[2].split(",") if len(sys.argv) > 2 else None
    if cmd == "s0":
        _run_s0()
    elif cmd == "s1":
        _run_s1(scope)
    elif cmd == "s2":
        _run_s2(scope)
    elif cmd == "s3":
        _run_s3(scope)
    elif cmd == "s4":
        _run_s4(scope)
    else:
        raise SystemExit(f"unknown stage: {cmd}")
