---
command: /n1-pipeline
description: M2 세분류 수요분석 파이프라인 (N₁ 도출)
agents: [ncs-analyst, data-engineer, qa-reviewer]
---

# /n1-pipeline

## 입력
- Master DB v0.2 이상 (M1 완료 상태)
- NCS 11개 정량지표 원본 데이터
- 정성평가단 (ISC+교강사+산업전문가) 구성 확정

## 단계

1. **정량 데이터 수집·표준화** (`ncs-analyst`)
   - 11지표 각각 데이터 확보 + 결측치 정책 적용
   - NCS 세분류 단위로 표준화
2. **정성평가 실시**
   - 5점 리커트 척도, 3지표
   - 평가자별 응답 수집 → 정량화
3. **종합 점수 계산** (`data-engineer`)
   - 가중치 적용 (발주처 승인 비율)
   - 세분류 순위 N₁ 산출
4. **경향성 분석**
   - 전년 대비 순위 변화
   - 상승/하락 사유 해석
5. **검수** (`qa-reviewer`)
6. **산출 저장**: `03_수행/M2_세분류수요분석/03_N1_세분류순위/[YYMMDD]_N1_v[N].xlsx`
7. **Master DB 동기화**: `n1_results` 시트 갱신
