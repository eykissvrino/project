# SKILL: JD Development (Job Description 작성·표준화)

## 목적
직무기술서(JD)를 표준 양식으로 작성·정비하여 채용·평가·교육·직무평가의
기준 자료로 활용한다.

## 트리거
- "JD 작성", "직무기술서", "Job Description"
- "직무분석", "Job Analysis"

## 사전 입력
- 직무 리스트 (조직도 기반)
- 현행 JD (있다면)
- 직무수행자·상사 인터뷰 가능 여부

## 표준 워크플로우

### Step 1. JD 표준 양식 정의
```
[Job Title]
[Job Family / Sub-family]
[Reports To] / [Direct Reports]

1. Job Purpose (직무 목적) - 2~3문장
   - 이 직무는 왜 존재하는가
   - 조직에 어떻게 기여하는가

2. Key Responsibilities (주요 책임) - 5~8개
   - [동사] + [대상] + [목적/결과]
   - 예: "월간 매출 데이터 분석을 통해 영업 KPI를 모니터링한다"

3. Key Performance Indicators (성과지표)
   - 정량 지표 우선

4. Qualifications (자격요건)
   - 학력
   - 경력 (년수, 분야)
   - 필수 스킬·자격증
   - 우대사항

5. Competencies (요구 역량)
   - 핵심역량
   - 직무역량 (Level 명시)

6. Working Conditions (근무 조건)
   - 출장·교대 등 특이사항
```

### Step 2. 직무 정보 수집
- **방법**:
  - 직무수행자 인터뷰 (1~1.5시간)
  - 상사 인터뷰
  - Job Diary (1주일 업무 기록)
  - 관찰 (현장직)
  - 설문 (대량 직무)
- **질문 예시**:
  - "하루/주/월 업무를 시간 비중대로 알려주세요"
  - "이 직무가 잘됐다는 것을 무엇으로 판단합니까"
  - "어떤 능력·경험이 있어야 잘할 수 있나요"
  - "어떤 의사결정 권한이 있습니까"
  - "누구와 가장 자주 협업합니까"

### Step 3. JD 초안 작성
- 표준 양식 적용
- 책임은 "동사로 시작" + "측정 가능한 결과" 지향
- 일반적 표현 → 구체적 표현
  - 나쁜 예: "재무 업무 수행"
  - 좋은 예: "월결산, 자금 운용, 세무 신고를 담당하여..."

### Step 4. 검증 (3-Way Validation)
- 직무수행자 검토
- 직속상사 검토
- 인사 검토 (양식·일관성)

### Step 5. 통합 관리
- JD Library 구축 (전사 통합)
- 버전 관리 (개정 이력)
- 정기 업데이트 사이클 (연 1회)

## 산출물

1. JD 표준 양식 (Master Template)
2. JD Library (직무별)
3. JD 작성 가이드 (운영 매뉴얼)

## 품질 체크리스트

- [ ] Job Purpose가 명확한가 (Why exists)
- [ ] Key Responsibilities가 5~8개로 정리되었는가
- [ ] 책임이 동사+결과로 구체적인가
- [ ] 자격요건이 측정 가능한가
- [ ] 3-Way Validation을 거쳤는가
- [ ] 양식이 전 직무에 일관 적용되었는가

## 연계
- 에이전트: `job-evaluation-expert` (주관), `consulting-writer`
- 후행: `job-evaluation`, `competency-modeling`

## 참고 템플릿
- `02_템플릿/매뉴얼/JD_표준양식.md`
