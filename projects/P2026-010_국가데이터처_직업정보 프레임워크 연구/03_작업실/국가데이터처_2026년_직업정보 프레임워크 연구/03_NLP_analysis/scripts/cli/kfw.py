"""
kfw — Korean Framework Workflow CLI
직업정보 프레임워크 연구 v1.4 단일 진입점

사용:
    python kfw.py ingest ksco --version 8 --source <path>
    python kfw.py run preprocess --layer L0 --scope 28,22,24
    python kfw.py run extract-tasks --batch 50 --runs 2
    python kfw.py run cluster-dwa --by gwa --min-size 4
    python kfw.py web --port 8501
    python kfw.py report build --target interim_1
    python kfw.py eval all --metrics 9
"""

from __future__ import annotations

import sys
import typer
from pathlib import Path
from loguru import logger
from typing import Optional

# scripts/ 를 sys.path 에 올려 `from utils...`, `from parsers...` 가 cwd 무관 동작하게
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

app = typer.Typer(help="kfw — 직업정보 프레임워크 연구 CLI (v1.4)")
ingest_app = typer.Typer(help="외부 데이터 import → DuckDB")
run_app = typer.Typer(help="NLP 파이프라인 5단계 실행")
report_app = typer.Typer(help="보고서·산출물 생성")
eval_app = typer.Typer(help="평가지표 9종 측정")
app.add_typer(ingest_app, name="ingest")
app.add_typer(run_app, name="run")
app.add_typer(report_app, name="report")
app.add_typer(eval_app, name="eval")

# 프로젝트 루트 (스크립트 기준)
ROOT = Path(__file__).resolve().parents[3]
DUCKDB_PATH = ROOT / "03_NLP_analysis" / "results" / "pipeline.duckdb"
DDL_PATH = ROOT / "04_framework_design" / "docs" / "11_DuckDB_스키마_DDL.sql"


# ============================================================
# 공통 헬퍼
# ============================================================
def get_db():
    import duckdb
    if not DUCKDB_PATH.exists():
        logger.warning(f"pipeline.duckdb 없음. 초기화 필요: {DUCKDB_PATH}")
    return duckdb.connect(str(DUCKDB_PATH))


# ============================================================
# init
# ============================================================
@app.command()
def init():
    """DuckDB 초기화 — DDL 실행."""
    import duckdb
    DUCKDB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(DUCKDB_PATH))
    ddl = DDL_PATH.read_text(encoding="utf-8")
    con.execute(ddl)
    logger.info(f"초기화 완료: {DUCKDB_PATH}")
    # 검증
    tables = con.execute("SHOW TABLES").fetchall()
    logger.info(f"테이블 {len(tables)}개 생성: {[t[0] for t in tables]}")


# ============================================================
# ingest
# ============================================================
@ingest_app.command("ksco")
def ingest_ksco(
    version: int = typer.Option(8, "--version"),
    source: str = typer.Option(..., "--source", help="KSCO 해설서 PDF 경로"),
):
    """KSCO 8차 해설서 → ksco_occupation 테이블 import."""
    from parsers.ksco_handbook_parser import parse_and_load
    parse_and_load(Path(source), version=version, db_path=DUCKDB_PATH)


@ingest_app.command("keco")
def ingest_keco(version: int = typer.Option(2025, "--version")):
    """KECO 2025 항목표 → job_family + mapping_ksco_keco."""
    logger.info(f"KECO {version} import — TODO: parsers/keco_parser.py 호출")


@ingest_app.command("kjd")
def ingest_kjd(version: int = typer.Option(2020, "--version")):
    """한국직업사전 → mapping_ksco_kjd + L1 raw."""
    logger.info(f"한국직업사전 {version} import — TODO: parsers/kjd_parser.py 호출")


@ingest_app.command("onet")
def ingest_onet(version: int = typer.Option(18, "--version")):
    """ONET 18.0 → external_ref schema."""
    logger.info(f"ONET {version} import — TODO: parsers/onet_parser.py 호출")


@ingest_app.command("mapping")
def ingest_mapping(source: str = typer.Option(..., "--source")):
    """ISCO 평가연구 부록4 등 매핑표 import."""
    logger.info(f"매핑 import: {source} — TODO: parsers/isco_appendix4_parser.py")


# ============================================================
# run (NLP 5단계)
# ============================================================
@run_app.command("preprocess")
def run_preprocess(layer: str = "L0", scope: str = "28,22,24"):
    """① 전처리 — 형태소·문장분할·동의어 정규화."""
    logger.info(f"전처리: layer={layer}, scope={scope} — TODO: utils/preprocess.py")


@run_app.command("extract-tasks")
def run_extract_tasks(
    scope: str = typer.Option(..., "--scope", help="세세분류5 / 세분류4 / 중분류2 (콤마 다중). 예: 28120 또는 2843 또는 28,22"),
    runs: int = typer.Option(2, "--runs", help="self-consistency 독립 실행 횟수(고정 2)"),
    limit: Optional[int] = typer.Option(None, "--limit", help="처리 세세분류 수 상한"),
    no_cache: bool = typer.Option(False, "--no-cache", help="캐시 무시(재호출)"),
):
    """② TASK 추출 — 세세분류 단위 + 부모 세분류 주요업무 상속(D0), LLM 2회 self-consistency.

    실행 예(E2E 게이트): python cli/kfw.py run extract-tasks --scope 28120
    키 필요: ANTHROPIC_API_KEY (+ cross-check 시 OPENAI_API_KEY).
    """
    import os
    import duckdb
    from utils import ksco_fetch as F
    from utils.extract_tasks import extract_one, persist

    if not os.environ.get("ANTHROPIC_API_KEY"):
        logger.error("ANTHROPIC_API_KEY 없음 — 03_NLP_analysis/scripts/.env 설정 후 재시도. "
                     "(키 무관 로직은 `python -m pytest tests/` 로 검증 가능)")
        raise typer.Exit(code=1)

    con = duckdb.connect(str(DUCKDB_PATH))
    codes = list(F.iter_scope(con, scope))
    if limit:
        codes = codes[:limit]
    if not codes:
        logger.warning(f"scope '{scope}' 에 해당하는 세세분류 없음")
        raise typer.Exit(code=1)

    logger.info(f"TASK 추출 시작: {len(codes)}개 세세분류, runs={runs}, scope={scope}")
    total = {"tasks": 0, "tools": 0, "work_context": 0}
    for i, code in enumerate(codes, 1):
        ctx = F.fetch_for_extraction(con, code)
        res = extract_one(ctx, con=con, use_cache=not no_cache)
        counts = persist(con, res)
        for k in total:
            total[k] += counts[k]
        flag = " [LOW_SIGNAL]" if res["low_signal"] else ""
        logger.info(f"[{i}/{len(codes)}] {code} {ctx['name']}: "
                    f"task {counts['tasks']} · tool {counts['tools']} · ctx {counts['work_context']} "
                    f"| {res['status']} jac={res['cross_consistency']:.2f}{flag}")
    con.close()
    logger.info(f"완료: task {total['tasks']} / tool {total['tools']} / "
                f"work_context {total['work_context']} (세세분류 {len(codes)}개)")


@run_app.command("jf-split")
def run_jf_split(scheme: str = "KECO_mid"):
    """③ Step 3a — Job Family 분할."""
    logger.info(f"Job Family 분할: scheme={scheme}")


@run_app.command("gwa-bucket")
def run_gwa_bucket(consistency_runs: int = 2):
    """③ Step 3b — ONET 41 GWA 1:1 할당."""
    logger.info(f"GWA 버킷 할당: runs={consistency_runs}")


@run_app.command("cluster-dwa")
def run_cluster_dwa(
    by: str = "gwa",
    min_size: int = 4,
    threshold_test: Optional[str] = typer.Option(None, "--threshold-test"),
):
    """③ Step 3c — GWA 내 임베딩+HDBSCAN+DWA 라이팅."""
    logger.info(f"DWA 군집: by={by}, min_size={min_size}, threshold_test={threshold_test}")


@run_app.command("dwa-qc")
def run_dwa_qc(rr: int = 2, rules: int = 8):
    """③ Step 3d — Round-Robin QC + 4기준 + 8조항."""
    logger.info(f"DWA QC: rr={rr}, rules={rules}")


@run_app.command("cross-family-dwa")
def run_cross_family_dwa():
    """④ Step 4a — Cross-Family DWA 통합."""
    logger.info("Cross-Family DWA 식별·통합")


@run_app.command("multi-linkage")
def run_multi_linkage(max_links: int = typer.Option(3, "--max")):
    """④ Step 4b — Multiple Linkage (task당 ≤3, 동일 Job Family)."""
    logger.info(f"Multiple Linkage: max={max_links}")


@run_app.command("cluster-iwa-kr")
def run_cluster_iwa_kr():
    """④ Step 4c — 한국 DWA 재클러스터링 → 한국 IWA."""
    logger.info("한국 IWA 도출")


@run_app.command("map-iwa-gwa")
def run_map_iwa_gwa(onet_ref: str = "onet_18.parquet"):
    """④ Step 4d — ONET IWA 332 / GWA 41 비교 매핑."""
    logger.info(f"ONET 비교 매핑: ref={onet_ref}")


@run_app.command("score-resp")
def run_score_resp(runs: int = 2):
    """⑤ Responsibility 3축 점수화."""
    logger.info(f"Responsibility 점수화: runs={runs}")


# ============================================================
# web
# ============================================================
@app.command()
def web(port: int = 8501):
    """Streamlit 전문가 검토 웹 (= CBM Intervention Layer)."""
    import subprocess
    web_app = ROOT / "03_NLP_analysis" / "scripts" / "web_streamlit" / "app.py"
    logger.info(f"검토 웹 가동: http://localhost:{port}")
    subprocess.run(["streamlit", "run", str(web_app), "--server.port", str(port)])


# ============================================================
# report
# ============================================================
@report_app.command("build")
def report_build(target: str = "interim_1"):
    """보고서 생성: kickoff / interim_1 / interim_2 / final."""
    logger.info(f"보고서 생성: {target}")


@report_app.command("definition")
def report_definition(ksco: str, format: str = "docx"):
    """단일 직업 직무기술 정의서."""
    logger.info(f"정의서 생성: KSCO {ksco}, format={format}")


# ============================================================
# eval
# ============================================================
@eval_app.command("all")
def eval_all(metrics: int = 9, scope: str = "28,22,24"):
    """평가지표 9종 측정."""
    logger.info(f"평가: metrics={metrics}, scope={scope}")


if __name__ == "__main__":
    app()
