"""TEST1 파이프라인 DB — 새 스키마 생성 + 원천 데이터 시드.

기존 scripts/ 미의존(처음부터). 스테이지별 ③ 출력 스키마대로 분석 테이블을 새로 만들고,
검증된 원천/참조 데이터(KSCO 1,270 · ONET 41/332/2087)만 기존 DB에서 복사한다.

실행:
    python pipeline/db.py init          # 새 DB 생성 + 시드 (이미 있으면 거부)
    python pipeline/db.py init --force   # 기존 TEST1 DB 덮어쓰기
    python pipeline/db.py verify         # 카운트 검증(게이트 0)
"""
from __future__ import annotations

import sys
from pathlib import Path

# 스크립트로 직접 실행해도 `import pipeline` 가능하게 TEST1 디렉터리를 path에 추가
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import duckdb

# Windows 콘솔(cp949)에서도 유니코드 출력
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# ── 경로 ─────────────────────────────────────────────────────────────
TEST1_DIR = Path(__file__).resolve().parents[1]          # .../03_NLP_analysis/TEST1
NLP_DIR = TEST1_DIR.parent                                # .../03_NLP_analysis
SRC_DB = NLP_DIR / "results" / "pipeline.duckdb"          # 기존(원천) DB
DB_PATH = TEST1_DIR / "pipeline.duckdb"                   # 새 TEST1 DB
OUTPUTS = TEST1_DIR / "outputs"
CACHE = TEST1_DIR / "cache"

# 기존 DB에서 복사할 참조 테이블(외부 비교용 — KSCO 본문은 HWPX 권위 파싱으로 대체).
SEED_TABLES = [
    ("main", "mapping_ksco_keco"),
    ("external_ref", "onet_gwa"),
    ("external_ref", "onet_iwa"),
    ("external_ref", "onet_dwa"),
]

# ── KSCO 권위 원천 스키마 (HWPX 파싱 결과 적재) ──────────────────────
KSCO_SCHEMA_SQL = """
-- 전체 분류 노드(중2·소3·세4·세세5) — 완전한 위계 트리
CREATE TABLE ksco_node (
    ksco_code   VARCHAR PRIMARY KEY,
    level       INTEGER,        -- 2=중분류 3=소분류 4=세분류 5=세세분류
    name        VARCHAR,
    parent_code VARCHAR,
    major_code  VARCHAR,        -- 대분류 1자리(1~9,A)
    major_name  VARCHAR,
    definition  VARCHAR,        -- 해설서 정의(개념)
    has_own_tasks BOOLEAN
);
CREATE TABLE ksco_main_task (ksco_code VARCHAR, seq INTEGER, item VARCHAR);
CREATE TABLE ksco_example   (ksco_code VARCHAR, seq INTEGER, example VARCHAR);
CREATE TABLE ksco_exclusion (ksco_code VARCHAR, seq INTEGER, item VARCHAR);
"""

# ── 분석 산출 스키마 (스테이지 ③ 설계대로 신규) ───────────────────────
SCHEMA_SQL = """
-- Stage 1: TASK / 도구 / 작업환경
CREATE TABLE task (
    task_id           VARCHAR PRIMARY KEY,
    ksco_code         VARCHAR,
    parent_code       VARCHAR,
    verb              VARCHAR,
    object            VARCHAR,
    full_statement    VARCHAR,
    source_sentence   VARCHAR,   -- 원문 근거(추적)
    derived_from      VARCHAR,   -- 부모 글머리/자기정의 어디서 특화됐는지(추적)
    layer             VARCHAR,
    source            VARCHAR,
    source_subject    VARCHAR,
    confidence        DOUBLE,
    extraction_runs   INTEGER,
    cross_consistency DOUBLE,
    low_signal        BOOLEAN
);
CREATE TABLE tool_inventory (
    tool_id        VARCHAR PRIMARY KEY,
    ksco_code      VARCHAR,
    name           VARCHAR,
    canonical_name VARCHAR,
    category       VARCHAR,    -- HW/SW/도구/장비/시스템
    evidence_span  VARCHAR,
    confidence     DOUBLE
);
CREATE TABLE work_context (
    context_id    VARCHAR PRIMARY KEY,
    ksco_code     VARCHAR,
    category      VARCHAR,     -- 장소/위험/사회적/신체적/시간적
    value         VARCHAR,
    standardized  VARCHAR,
    evidence_span VARCHAR,
    confidence    DOUBLE
);

-- Stage 2: DWA + TASK↔DWA(Multiple Linkage)
CREATE TABLE dwa (
    dwa_id             VARCHAR PRIMARY KEY,
    label              VARCHAR,   -- 8조항 정식명
    definition         VARCHAR,
    cluster_size       INTEGER,
    n_jobs             INTEGER,
    mean_cosine        DOUBLE,
    eight_rules_passed BOOLEAN,
    is_cross_family    BOOLEAN
);
CREATE TABLE task_to_dwa (
    task_id    VARCHAR,
    dwa_id     VARCHAR,
    link_order INTEGER,           -- 1=primary, 2~3=인접 DWA
    PRIMARY KEY (task_id, dwa_id)
);

-- Stage 3: IWA + DWA↔IWA(strict nesting)
CREATE TABLE iwa (
    iwa_id             VARCHAR PRIMARY KEY,
    label              VARCHAR,   -- 동사구(일반)
    definition         VARCHAR,
    n_dwa              INTEGER,
    n_task             INTEGER,
    n_jobs             INTEGER,
    mean_cosine        DOUBLE,
    eight_rules_passed BOOLEAN
);
CREATE TABLE dwa_to_iwa (
    dwa_id VARCHAR PRIMARY KEY,   -- 1 DWA → 정확히 1 IWA
    iwa_id VARCHAR
);

-- Stage 4: GWA + IWA↔GWA + 탐색(상향식)
CREATE TABLE gwa (
    gwa_id        VARCHAR PRIMARY KEY,
    label_kr      VARCHAR,
    onet_gwa_id   VARCHAR,
    onet_label_en VARCHAR,
    domain        VARCHAR,        -- 4대영역: 정보입력/정신과정/작업산출/타인상호작용
    is_kr_unique  BOOLEAN,
    source        VARCHAR         -- ONET_adopt | KR_bottomup
);
CREATE TABLE iwa_to_gwa (
    iwa_id VARCHAR PRIMARY KEY,   -- 1 IWA → 정확히 1 GWA(주 트랙)
    gwa_id VARCHAR,
    cosine DOUBLE,
    method VARCHAR                -- mapped | clustered
);
CREATE TABLE gwa_bottomup (
    kr_gwa_id    VARCHAR PRIMARY KEY,
    label_kr     VARCHAR,
    n_iwa        INTEGER,
    nearest_onet VARCHAR,
    cosine       DOUBLE
);

-- 재현성: LLM 호출/캐시 로그
CREATE TABLE llm_call_log (
    call_id       VARCHAR,
    model         VARCHAR,
    seed          INTEGER,
    prompt_hash   VARCHAR,
    cached        BOOLEAN,
    input_tokens  INTEGER,
    output_tokens INTEGER,
    note          VARCHAR
);
"""

ANALYSIS_TABLES = [
    "task", "tool_inventory", "work_context",
    "dwa", "task_to_dwa", "iwa", "dwa_to_iwa",
    "gwa", "iwa_to_gwa", "gwa_bottomup", "llm_call_log",
]


def get_con(read_only: bool = False) -> duckdb.DuckDBPyConnection:
    """TEST1 DB 연결."""
    return duckdb.connect(str(DB_PATH), read_only=read_only)


def init(force: bool = False) -> None:
    """새 DB 생성 → 분석 스키마 → 원천 시드."""
    for d in (TEST1_DIR, OUTPUTS, CACHE):
        d.mkdir(parents=True, exist_ok=True)

    if DB_PATH.exists():
        if not force:
            raise SystemExit(f"이미 존재: {DB_PATH}\n  덮어쓰려면: python pipeline/db.py init --force")
        DB_PATH.unlink()

    if not SRC_DB.exists():
        raise SystemExit(f"원천 DB 없음: {SRC_DB}")

    con = get_con()
    con.execute(KSCO_SCHEMA_SQL)
    con.execute(SCHEMA_SQL)
    con.execute("CREATE SCHEMA IF NOT EXISTS external_ref")

    # 참조 테이블(ONET·KECO 매핑)은 기존 DB에서 복사
    con.execute(f"ATTACH '{SRC_DB.as_posix()}' AS src (READ_ONLY)")
    for schema, tbl in SEED_TABLES:
        con.execute(f"CREATE TABLE {schema}.{tbl} AS SELECT * FROM src.{schema}.{tbl}")
    con.execute("DETACH src")

    # KSCO 본문 = HWPX 권위 파싱으로 적재
    _seed_ksco(con)
    con.close()
    print(f"[init] 생성 완료: {DB_PATH}")
    verify()


def _seed_ksco(con) -> None:
    """HWPX 권위 파싱 결과를 ksco_node + 항목 테이블에 적재."""
    from pipeline import parse_ksco as P
    _, nodes = P.build_nodes()
    con.execute("BEGIN")
    try:
        for code, nd in nodes.items():
            con.execute(
                """INSERT INTO ksco_node
                   (ksco_code, level, name, parent_code, major_code, major_name,
                    definition, has_own_tasks) VALUES (?,?,?,?,?,?,?,?)""",
                [code, nd["level"], nd["name"], nd["parent_code"], nd["major_code"],
                 nd["major_name"], nd["definition"], bool(nd["main_tasks"])])
            for i, it in enumerate(nd["main_tasks"], 1):
                con.execute("INSERT INTO ksco_main_task VALUES (?,?,?)", [code, i, it])
            for i, ex in enumerate(nd["examples"], 1):
                con.execute("INSERT INTO ksco_example VALUES (?,?,?)", [code, i, ex])
            for i, it in enumerate(nd["exclusions"], 1):
                con.execute("INSERT INTO ksco_exclusion VALUES (?,?,?)", [code, i, it])
        con.execute("COMMIT")
    except Exception:
        con.execute("ROLLBACK")
        raise
    n5 = con.execute("SELECT COUNT(*) FROM ksco_node WHERE level=5").fetchone()[0]
    print(f"[seed] ksco_node {len(nodes)}개 (세세분류 {n5}) 적재")


def verify() -> dict:
    """게이트 0 — 카운트 검증."""
    con = get_con(read_only=True)
    out = {}
    out["세세분류(5자리)"] = con.execute(
        "SELECT COUNT(*) FROM ksco_node WHERE level=5").fetchone()[0]
    out["세분류(4자리)"] = con.execute(
        "SELECT COUNT(*) FROM ksco_node WHERE level=4").fetchone()[0]
    out["정의보유(세세)"] = con.execute(
        "SELECT COUNT(*) FROM ksco_node WHERE level=5 AND definition<>''").fetchone()[0]
    out["주요업무항목"] = con.execute("SELECT COUNT(*) FROM ksco_main_task").fetchone()[0]
    out["onet_gwa"] = con.execute("SELECT COUNT(*) FROM external_ref.onet_gwa").fetchone()[0]
    out["onet_iwa"] = con.execute("SELECT COUNT(*) FROM external_ref.onet_iwa").fetchone()[0]
    out["onet_dwa"] = con.execute("SELECT COUNT(*) FROM external_ref.onet_dwa").fetchone()[0]
    # 분석 산출 테이블은 전부 0행이어야 함
    analysis_counts = {t: con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
                       for t in ANALYSIS_TABLES}
    con.close()

    print("── 게이트 0: TEST1 카운트 검증 ──")
    for k, v in out.items():
        print(f"  {k}: {v}")
    nonzero = {t: c for t, c in analysis_counts.items() if c}
    print(f"  분석 산출 테이블({len(ANALYSIS_TABLES)}개): " +
          ("전부 0행 ✓" if not nonzero else f"⚠️ 비어있지 않음 {nonzero}"))

    ok = (out["세세분류(5자리)"] == 1270 and out["세분류(4자리)"] == 495
          and out["정의보유(세세)"] == 1270 and out["onet_gwa"] == 41
          and out["onet_iwa"] == 332 and out["onet_dwa"] == 2087 and not nonzero)
    print("  판정:", "PASS ✓" if ok else "FAIL ✗")
    return {**out, "analysis_nonzero": nonzero, "pass": ok}


if __name__ == "__main__":
    args = sys.argv[1:]
    cmd = args[0] if args else "verify"
    if cmd == "init":
        init(force="--force" in args)
    elif cmd == "verify":
        verify()
    else:
        raise SystemExit(f"unknown cmd: {cmd} (init|verify)")
