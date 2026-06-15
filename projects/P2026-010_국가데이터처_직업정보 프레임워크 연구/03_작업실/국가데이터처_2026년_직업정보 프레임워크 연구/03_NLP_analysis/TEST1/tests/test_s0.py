"""Stage 0 전처리 테스트 — 권위 파싱 + 위계 + 상속 + 플래그."""
import pytest

from pipeline import db, s0_preprocess as s0


# ── 순수 함수 ────────────────────────────────────────────────────────
def test_normalize_ws():
    assert s0.normalize_ws("  여러   공백\n줄바꿈 ") == "여러 공백 줄바꿈"


def test_is_low_signal():
    assert s0.is_low_signal("짧은정의")
    assert s0.is_low_signal("Business Support Managers nec")
    assert not s0.is_low_signal(
        "회계에 관한 용역 업무를 계획하고 관리하며, 의뢰인의 위임에 따라 재무회계 서류를 작성하고, "
        "기업의 소득세 신고서를 작성하며, 재무회계 감사를 수행하거나 증명하는 업무를 담당한다.")


# ── DB 통합 (권위 파싱 TEST1 DB) ─────────────────────────────────────
@pytest.fixture(scope="module")
def con():
    c = db.get_con(read_only=True)
    yield c
    c.close()


@pytest.fixture(scope="module")
def cache(con):
    return s0._load_caches(con)


def test_full_lineage_with_names(con, cache):
    # 28120 회계사 — 대>중>소>세>세세 명칭이 모두 채워져야 함
    r = s0.build_record(con, "28120", cache)
    assert r["major_code"] == "2" and r["major_name"] == "전문가 및 관련 종사자"
    assert r["mid_code"] == "28" and "경영" in r["mid_name"]
    assert r["minor_code"] == "281"
    assert r["broad_code"] == "2812" and r["broad_name"] == "회계사"
    assert r["name"] == "회계사"
    assert all(r[k] for k in ["major_name", "mid_name", "minor_name", "broad_name"])


def test_own_tasks(con, cache):
    r = s0.build_record(con, "28120", cache)
    assert r["main_tasks_source"] == s0.SRC_SELF
    assert r["has_tasks"] and r["valid"]
    assert any("회계" in t for t in r["main_tasks"])


def test_inherited_tasks(con, cache):
    # 28151 경영 컨설턴트 — 부모 2815 주요업무 상속
    r = s0.build_record(con, "28151", cache)
    assert r["main_tasks_source"] == s0.SRC_PARENT
    assert r["has_tasks"] and len(r["main_tasks"]) > 0


def test_ancestor_definitions_present(con, cache):
    # 조상 정의 노출 + 추출컨텍스트 결합. (단일자식 가족은 세분류 정의가 비고 세세에 있음)
    r = s0.build_record(con, "28120", cache)
    assert r["major_def"] and "전문지식" in r["major_def"]   # 대분류 2 정의
    assert r["mid_def"]                                        # 중분류 28 정의
    assert "[세세분류 28120" in r["extraction_context"]
    assert "[대분류 2" in r["extraction_context"]
    # 조상 정의는 최소 하나 이상 존재해야(맥락 보강 가능)
    assert any([r["major_def"], r["mid_def"], r["minor_def"], r["broad_def"]])


def test_thin_def_borrows_ancestors(con, cache):
    # 정의 빈약(low_signal) 직업도 조상정의로 valid 확보
    recs = s0.build_all(con)
    thin = [r for r in recs if r["low_signal"]]
    assert thin and all(r["valid"] for r in thin)
    # 적어도 일부는 조상정의가 채워져 컨텍스트가 세세정의보다 길어야
    assert any(len(r["extraction_context"]) > len(r["definition"]) + 20 for r in thin)


def test_tricky_code_name(con, cache):
    # 24911 = "119 구조대원" (코드+이름 글루 시 24911119 혼동 케이스)
    r = s0.build_record(con, "24911", cache)
    assert r["name"] == "119 구조대원"
    assert r["definition"]


def test_former_broken_now_valid(con, cache):
    # 27111 판사 — 기존 DB에선 깨졌으나 권위 파싱에선 정상 정의 보유
    r = s0.build_record(con, "27111", cache)
    assert "재판" in r["definition"]
    assert r["valid"]


def test_coverage_full_1270(con):
    recs = s0.build_all(con)
    cov = s0.coverage_report(recs)
    assert cov["총_세세분류"] == 1270
    assert cov["valid"] == 1270            # 전 직업 정의 보유 → 전수 추출가능
    assert cov["주요업무보유"] >= 1190
    assert all(r["major_name"] and r["broad_name"] for r in recs)
