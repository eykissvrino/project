# SKILL: Salary Benchmarking (임금 벤치마킹)

## 목적
자사 임금의 시장경쟁력을 진단하고 직무·직급별 시장 임금을 매칭하여
임금구조 설계의 기초 데이터를 제공한다.

## 트리거
- "임금 벤치마킹", "시장경쟁력 분석"
- "Salary Survey", "Compa-ratio 분석"
- "Job Pricing"

## 사전 입력
- 자사 임금 데이터 (직급·직무별, 익명화)
- 직무 정보 (JD 또는 Job Title)
- 벤치마크 대상 시장 정의 (산업·규모·지역)
- 활용 가능한 임금조사 자료

## 표준 워크플로우

### Step 1. 시장 정의
- 비교 대상 산업 / 규모(매출, 인원) / 지역
- 인재 경쟁 시장 (Talent Market) 우선
  - 동종업계 vs 동지역·동규모

### Step 2. 데이터 소스 확보
- **무료**: 고용부 사업체 노동력 조사, 통계청 데이터, 경총 임금조사
- **유료**: Mercer TRS, Korn Ferry, WTW Survey
- **DART 공시**: 사업보고서 직원 현황·임원 보수
- **채용 공고**: 직무·연봉 공개분 활용

### Step 3. Job Matching
- Anchor Job 10~20개 선정
- 자사 직무 → 시장 직무 매칭 (Job Title이 아닌 Content 기준)
- Matching Confidence 평가 (Strong / Medium / Weak)

### Step 4. Aging
- 조사 시점 → 현재 환산
- 인상률 적용 (해당 시장 평균 인상률)

### Step 5. 분포 비교
- 자사 임금 vs 시장 P25 / P50 / P75
- Compa-ratio 산정 (자사 / 시장 중위값)
- 직무별·직급별 시각화 (Box Plot)

### Step 6. 시사점 도출
- Lead / Match / Lag 직무군 식별
- 핵심 인재 보유 리스크 (시장 대비 저보상 직무)
- 과보상 영역 (시장 대비 고비용)

## 산출물

1. 시장경쟁력 분석 보고서
2. 직무별 Compa-ratio Map
3. 시장 임금 분포 시각화 (직무 × Percentile)
4. Job Matching Table

## 품질 체크리스트

- [ ] 시장 정의가 명확한가 (인재 경쟁 시장 기준)
- [ ] Job Matching이 Content 기준인가 (Title X)
- [ ] 데이터 출처·시점·표본수가 명시되었는가
- [ ] Aging이 적용되었는가
- [ ] 평균 아닌 P25/P50/P75 분포가 제시되었는가

## 연계
- 에이전트: `research-analyst` (주관), `compensation-expert` (활용)
- 선행: -
- 후행: `pay-structure-design`, `job-evaluation`

## 참고 지식베이스
- `01_지식베이스/시장정보/임금조사_레퍼런스.md`
- `01_지식베이스/시장정보/공시자료_활용.md`
