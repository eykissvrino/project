---
name: slr-diagram-creation
description: STEP 학습 로드맵(SLR) 10대 분야 도식(PPT)을 Master DB로부터 자동 생성한다.
---

# SLR Diagram Creation

## 10대 분야 (RFP §II-1-나 평생직업능력개발 + 디지털)

평생직업능력개발 10대 NCS 대분류:
1. 문화·예술·디자인·방송
2. 운전·운송
3. 건설
4. 기계
5. 재료
6. 화학·바이오
7. 전기·전자
8. 정보통신
9. 인쇄·목재·가구·공예
10. 환경·에너지·안전

## SLR 도식 구조 (작년 시앤피 산출물 분석 기반)

각 분야 도식 = 1개 PPT 슬라이드

```
┌──────────────────────────────────────────┐
│ [분야명] STEP 학습 로드맵 (예: 게임콘텐츠제작) │
├──────────────────────────────────────────┤
│  직무 1     직무 2     직무 3     ...      │
│   ↓          ↓          ↓                  │
│  기초─중급─고급  기초─중급─고급  ...        │
│   (과목 코드 / 과목명 / 회차 / E·V)         │
│   ↓                                        │
│  자격증·SQF 연계                           │
└──────────────────────────────────────────┘
```

## 자동 생성 절차

### Step 1: Master DB → SLR 구조 추출
```python
# Master DB의 slr_structure 시트
# 컬럼: field, sub_field, job, level, course_id, course_name, sessions, type
```

### Step 2: python-pptx로 PPT 생성
```python
from pptx import Presentation
from pptx.util import Inches, Pt

for field in 10_fields:
    slide = create_slide(field)
    for job in field.jobs:
        add_job_column(slide, job)
        for course in job.courses_by_level:
            add_course_box(slide, course)
    add_qualification_links(slide, field.qualifications)
```

### Step 3: 디자인 적용
- 한기대 BI 색상 (브랜드 가이드 참조)
- 분야별 색상 코드 일관 (예: 정보통신 = 푸른색)
- 레벨별 셰이딩 (기초 옅음 → 고급 진함)

### Step 4: 출력
- `03_수행/M6_결과정리/01_SLR도식화_10대분야/[YYMMDD]_SLR도식_v[N].pptx`
- 분야별 단일 슬라이드 + 통합본 모두 생성

## 갱신 정책 (SLR 관리매뉴얼 연계)

- Master DB 변경 → 자동 재생성 가능 (`pipelines/05_generate_slr_diagram.py`)
- 디자인 수정 = PPT 직접 편집 (자동화 영역 밖)
- 분야 추가·삭제 = 발주처 협의 후 코드 수정

## 작년 사업 산출물 참조

- `00_참고자료/2025년_결과물/` 의 `[시앤피컨설팅]...최종보고서.pdf` 에 포함된 TTR 도식 참조
- 단, **명칭은 SLR** (TTR 아님)
- 작년 대비 개선: AX·GX 분야 추가 가능성 검토 (발주처 협의)
