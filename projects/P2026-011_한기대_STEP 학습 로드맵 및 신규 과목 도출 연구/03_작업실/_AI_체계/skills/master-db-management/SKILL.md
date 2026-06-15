---
name: master-db-management
description: Master DB 스키마 정의·버전 관리·자동 검증·내보내기. RFP 자동화/매뉴얼화 윈테마의 핵심.
---

# Master DB Management

## 파일 명명 규칙

```
master_db_versions/
├── 20260601_v0.1_초기.xlsx
├── 20260615_v0.2_NCS최신화반영.xlsx
├── 20260701_v0.3_M1완료.xlsx
├── 20260801_v0.4_중간보고시점.xlsx
└── 20261115_v1.0_최종.xlsx
```

규칙: `YYYYMMDD_v[N]_[10자내요약].xlsx`

## 시트 구조 (표준)

| 시트 | 행 수 (추정) | 갱신 빈도 |
|---|---|---|
| 1. courses_meta (과목 메타) | 2,586+ | 신규 과목 추가 시 |
| 2. ncs_change_log (능력단위 변경) | 변동 | NCS 고시마다 |
| 3. unused_units (미활용) | 수백 | M1 / 매월 |
| 4. mapping_confidence (매핑 신뢰도) | 2,586 | M1 |
| 5. n1_results (세분류 순위) | 약 800 | M2 |
| 6. n2_results (능력단위 순위) | 수천 | M3 |
| 7. n3_results (개발 우선순위) | 400+ | M4 |
| 8. course_outlines_index (400 색인) | 400 | M5 |
| 9. slr_structure (도식용) | 변동 | M6 |
| 10. survey_continuous (상시 수요) | 누적 | 상시 |
| 11. change_log (DB 변경 로그) | 모든 수정 | 매 수정 |

## 변경 로그 시트 (필수)

| timestamp | sheet | cell/row | before | after | by | reason |
|---|---|---|---|---|---|---|

→ 모든 수동 수정은 이 시트에 기록. 발주처 감사 대응.

## 자동 검증 스크립트 (Python)

```python
# pipelines/03_validate_master_db.py 의사코드

def validate(xlsx_path):
    db = load(xlsx_path)
    errors = []
    
    # 1. NCS 코드 형식
    for code in db.courses_meta.competency_unit:
        if not re.match(r'^\d{10}_\d{2}v\d+', code):
            errors.append(f"Invalid code: {code}")
    
    # 2. 결측치
    for col in REQUIRED_COLS:
        nulls = db.courses_meta[col].isnull().sum()
        if nulls > 0:
            errors.append(f"{col}: {nulls} nulls")
    
    # 3. 중복
    dups = db.courses_meta.course_id.duplicated()
    if dups.any():
        errors.append(f"Duplicate course_id: {dups.sum()}")
    
    # 4. 외래 키 (NCS 코드가 실제 NCS DB에 존재)
    valid_codes = set(load_ncs_codes())
    invalid = [c for c in db.courses_meta.competency_unit if c not in valid_codes]
    if invalid:
        errors.append(f"Unknown NCS codes: {len(invalid)}")
    
    # 5. 수업 유형 일관성
    # course_type ∈ {E, V, E·V}
    
    return errors
```

## 발주처 인계 시 체크리스트

- [ ] 모든 시트에 데이터 사전(컬럼 설명 시트) 포함?
- [ ] change_log 시트 마지막 수정 일자 = 인계 일자?
- [ ] 잠금/암호 없음 (발주처가 자유롭게 편집 가능)?
- [ ] 자동화 스크립트 별도 폴더 (`pipelines/`) 포함?
- [ ] 사용 매뉴얼 (`SLR 관리매뉴얼`) 동봉?
