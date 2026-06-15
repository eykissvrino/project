"""
KSCO 8차 해설서 (1,036p PDF) → ksco_occupation 테이블 import
v1.4

세분류·세세분류 단위로:
  - 코드 (4자리/5자리)
  - 명칭
  - 정의 (세분류 본문 첫 1~3문장)
  - "주요 업무" 섹션 글머리표
  - 직업 예시
를 추출하여 ksco_occupation 에 저장한다.

본 파서는 M+1 (1차 가동) 직후 첫 실행되며, 추출 정확도는
M+2 파일럿 결과로 검증·튜닝한다.
"""

from __future__ import annotations

import re
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional, Iterable

import duckdb
from pypdf import PdfReader
from loguru import logger


# ============================================================
# 패턴
# ============================================================
# 4자리 세분류 코드 (1xxx ~ 9xxx, A0xx 군인)
RX_CODE_4 = re.compile(r"(?<!\d)([1-9]\d{3}|A0\d{2})(?!\d)")
# 5자리 세세분류 (10000~99999, A0xxx)
RX_CODE_5 = re.compile(r"(?<!\d)([1-9]\d{4}|A0\d{3})(?!\d)")
# "주요 업무" 마커 (공백 변형 허용)
RX_MAIN_TASKS = re.compile(r"▍?\s*주\s*요\s*업\s*무")
# 직업 예시 마커
RX_JOB_EXAMPLES = re.compile(r"▍?\s*직\s*업\s*예\s*시")
# 글머리표
RX_BULLET = re.compile(r"·\s*([^·\n]+)")
# 8차 변동 사항 키워드
RX_V8_CHANGE = re.compile(r"(분리\s*신설|분류\s*이동|명칭\s*변경|통합)")


# ============================================================
# 데이터 모델
# ============================================================
@dataclass
class KscoEntry:
    ksco_code: str
    name: str
    name_en: Optional[str]
    code_length: int
    parent_code: Optional[str]
    major_class: str
    mid_class: str
    job_family_id: Optional[str]
    definition_text: Optional[str]
    main_tasks_text: Optional[str]
    examples_text: Optional[str]
    has_main_tasks: bool
    v8_change_flag: Optional[str]


# ============================================================
# 추출
# ============================================================
def extract_full_text(pdf_path: Path) -> str:
    """PDF 전체를 단일 문자열로."""
    logger.info(f"PDF 로드: {pdf_path.name} ({pdf_path.stat().st_size/1024/1024:.1f} MB)")
    reader = PdfReader(str(pdf_path))
    pages = []
    for i, p in enumerate(reader.pages):
        t = p.extract_text() or ""
        pages.append(t)
    full = "\n".join(pages)
    logger.info(f"추출 완료: {len(reader.pages)} 페이지, {len(full):,} 글자")
    return full


def split_into_blocks(full_text: str) -> list[tuple[str, str]]:
    """
    텍스트를 (코드, 블록 텍스트) 쌍으로 분리.

    각 세분류·세세분류는 (코드 + 이름) 으로 시작하고,
    다음 코드 직전까지가 해당 블록.

    제8차 해설서는 4자리·5자리 코드가 섞여 등장한다.
    1차 단순 구현: 4자리 코드 단위로 자르고, 그 안에 5자리 코드들이 포함되도록 둔다.
    """
    blocks = []
    # 4자리 코드의 모든 등장 위치
    matches = list(RX_CODE_4.finditer(full_text))
    if not matches:
        logger.warning("4자리 코드 매치 없음")
        return blocks

    for i, m in enumerate(matches):
        code = m.group(1)
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(full_text)
        block = full_text[start:end].strip()
        # 4자리 코드 다음에 보통 한글 이름이 옴 → 첫 줄을 이름으로 본다
        blocks.append((code, block))

    logger.info(f"4자리 코드 블록 수: {len(blocks)}")
    return blocks


def parse_block(code: str, block: str) -> Optional[KscoEntry]:
    """단일 4자리 코드 블록을 KscoEntry로 변환."""
    if not block:
        return None

    # 이름: 블록 시작 ~ 줄바꿈 또는 영문 시작
    name_match = re.match(r"\s*([가-힣\s·‧\(\)A-Z]+?)(?:\n|[A-Z][a-z])", block)
    name = name_match.group(1).strip() if name_match else block[:30].split("\n")[0].strip()

    # 정의: 첫 ▍주요업무 또는 다음 5자리 코드 전까지
    main_tasks_match = RX_MAIN_TASKS.search(block)
    examples_match = RX_JOB_EXAMPLES.search(block)

    # 정의 본문: 이름 다음 ~ ▍주요 업무 또는 ▍직업 예시 전까지
    after_name_idx = name_match.end() if name_match else 0
    cutoff = len(block)
    if main_tasks_match:
        cutoff = min(cutoff, main_tasks_match.start())
    elif examples_match:
        cutoff = min(cutoff, examples_match.start())
    definition_text = block[after_name_idx:cutoff].strip()[:500]

    # 주요 업무 텍스트: ▍주요 업무 ~ ▍직업 예시 (또는 끝)
    main_tasks_text = None
    if main_tasks_match:
        mt_start = main_tasks_match.end()
        mt_end = examples_match.start() if examples_match else len(block)
        main_tasks_text = block[mt_start:mt_end].strip()[:2000]

    # 직업 예시
    examples_text = None
    if examples_match:
        examples_text = block[examples_match.end():].strip()[:1000]

    # 8차 변동
    v8_change = None
    v8_match = RX_V8_CHANGE.search(block)
    if v8_match:
        v8_change = v8_match.group(1)

    # 메타
    major_class = code[0]
    mid_class = code[:2]
    parent_code = None  # 5자리에만 의미 있음

    return KscoEntry(
        ksco_code=code,
        name=name,
        name_en=None,  # 영문은 분류항목표에서 별도 매칭 권장
        code_length=4,
        parent_code=parent_code,
        major_class=major_class,
        mid_class=mid_class,
        job_family_id=None,  # KECO 매핑은 별도 단계
        definition_text=definition_text,
        main_tasks_text=main_tasks_text,
        examples_text=examples_text,
        has_main_tasks=bool(main_tasks_match),
        v8_change_flag=v8_change,
    )


# ============================================================
# 로드
# ============================================================
def load_to_duckdb(entries: list[KscoEntry], db_path: Path) -> None:
    """KscoEntry 리스트를 ksco_occupation 테이블에 upsert."""
    con = duckdb.connect(str(db_path))
    # 임시 테이블로 적재 후 INSERT OR REPLACE
    import pandas as pd
    df = pd.DataFrame([asdict(e) for e in entries])
    con.register("tmp_ksco", df)
    con.execute("""
        INSERT OR REPLACE INTO ksco_occupation
        SELECT * FROM tmp_ksco
    """)
    n = con.execute("SELECT COUNT(*) FROM ksco_occupation").fetchone()[0]
    logger.info(f"ksco_occupation 행 수: {n}")
    con.close()


# ============================================================
# 진입점
# ============================================================
def parse_and_load(pdf_path: Path, version: int, db_path: Path) -> None:
    """KSCO 해설서 PDF → DuckDB load."""
    assert version == 8, "현재 v1.4는 8차만 지원"
    full = extract_full_text(pdf_path)
    blocks = split_into_blocks(full)
    entries = []
    for code, block in blocks:
        e = parse_block(code, block)
        if e:
            entries.append(e)
    logger.info(f"파싱 완료: {len(entries)} 세분류 (예상 495)")
    # 통계
    with_main = sum(1 for e in entries if e.has_main_tasks)
    logger.info(f"주요 업무 섹션 보유: {with_main} / {len(entries)} (보강 트리거 대상: {len(entries)-with_main})")
    # 로드
    load_to_duckdb(entries, db_path)


if __name__ == "__main__":
    import sys
    pdf = Path(sys.argv[1])
    db = Path(sys.argv[2])
    parse_and_load(pdf, version=8, db_path=db)
