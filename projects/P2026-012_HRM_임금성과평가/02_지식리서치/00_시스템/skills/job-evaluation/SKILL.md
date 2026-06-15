# SKILL: Job Evaluation (직무평가)

## 목적
조직 내 직무의 상대적 가치를 체계적으로 평가하여 직무급 설계·승진체계·
교육체계의 기준을 마련한다.

## 트리거
- "직무평가", "JE 수행", "IPE 적용", "Hay Method"
- "직무 등급화", "Job Grade 설계"
- "Job Architecture 구축"

## 사전 입력 (Inputs)

| 필수/선택 | 항목 | 비고 |
|-----------|------|------|
| 필수 | 조직도 | 평가 대상 직무 식별 |
| 필수 | 현행 JD (있다면) | 없으면 Step 1에서 작성 |
| 필수 | 직무 분류 의도 | Job Family, Track 등 |
| 필수 | 평가 방법론 선택 | IPE / Hay / 한국형 / 자체 |
| 선택 | 평가위원회 구성안 | 보통 인사+사업+외부전문가 |

## 표준 워크플로우

### Step 1. JD 정비 (Job Description)
**중요: JD 정비 없이 직무평가 진행 금지**

- 직무 식별 (Job Identification)
  - 단순 명칭이 아닌 "역할 + 책임" 기준
  - 1인 1직무 X, 1직무 N명 OK
- JD 작성 (jd-development 스킬 활용)
  - 직무 목적 (Job Purpose)
  - 주요 책임 (Key Responsibilities) - 5~8개
  - 핵심 성과지표 (KPI)
  - 자격요건 (Qualifications)
  - 보고관계 (Reporting Lines)
- JD 검증: 직무수행자 + 직속상사 + 인사 3-Way 확인

### Step 2. 방법론 선정·교육

#### Option A. Mercer IPE
- 5 Factors:
  1. **Impact**: 조직 성과에 미치는 영향 (5단계)
  2. **Communication**: 의사소통 복잡성 (5단계)
  3. **Innovation**: 창의성·혁신 요구 (5단계)
  4. **Knowledge**: 요구 지식·전문성 (5단계)
  5. **Risk**: 의사결정 리스크 (5단계, 옵션)
- 각 요소별 등급 → Score
- Total Score → Position Class (PC) 매핑

#### Option B. Hay Guide Chart
- 3 Factors:
  1. **Know-How**: 깊이(Technical) × 폭(Managerial) × 인간관계
  2. **Problem Solving**: 사고환경 × 사고도전
  3. **Accountability**: 행동자유 × 영향 × 영향규모
- Profile Pattern (Up/Down/Level) 검증
- Total Points → Hay Grade

#### Option C. 한국형 자체 모델
- 4~5 Factors (예시):
  1. **지식·기술**: 요구 학력·경력·전문지식
  2. **문제해결**: 업무 복잡성·창의성
  3. **책임**: 결과 책임·인적·물적·예산
  4. **근무환경**: 신체적·정신적 부담
- Point Factor Method 적용

### Step 3. 평가위원회 구성·운영
- 위원 구성 (5~7명):
  - 인사 책임자 (위원장)
  - 사업본부 임원 2~3명
  - 외부 전문가 1~2명 (컨설턴트)
- 위원 교육:
  - 방법론 이해
  - 평가 일관성 (Calibration Session)
- Anchor Job 선정 (10~20개):
  - 시장 매칭 가능한 대표 직무
  - 전 직무 평가의 기준점

### Step 4. 평가 실행
- Anchor Job 평가 (위원회 합의)
- 나머지 직무 평가:
  - 1차: 개별 위원 평가
  - 2차: 위원회 종합 토의
  - 3차: Anchor Job 기준 정합성 확인
- 이상치 검증:
  - 직급간 점수 역전
  - 같은 Family 내 과대 격차
  - 과거 인식과 큰 괴리

### Step 5. Grade 매핑
- Score → Grade Cut-off 설정
  - 통상 5~9 Grade
  - 균등 분포보다 시장 매칭 기반 결정
- Grade 수 결정 기준:
  - 조직 계층 수
  - 직무 다양성
  - 향후 관리 부담

### Step 6. Job Architecture 구축
- Job Family 매핑 (예: 경영지원/영업/기술/운영)
- Career Track:
  - Manager Track (M1~M4)
  - Specialist Track (S1~S4)
- Grade × Family × Track 3차원 매트릭스

### Step 7. 시장 매칭
- Anchor Job 시장 임금 조회 (Mercer/WTW/Korn Ferry 데이터)
- Grade별 시장 임금 추정
- 자사 임금과 비교 (Compa-ratio)

### Step 8. 검증·확정
- 사업본부장 리뷰
- 인사위원회 최종 승인
- 결과 통보 가이드 마련 (직무수행자 커뮤니케이션)

## 산출물 (Outputs)

1. **직무평가 결과서** (전 직무 등급 매핑)
2. **JD Library** (표준 양식, 직무별)
3. **Job Architecture** (Family × Grade × Track 매트릭스)
4. **평가위원회 회의록**
5. **직무평가 운영 매뉴얼** (향후 신설/변경 직무 평가)
6. **시장 매칭 분석서**

## 품질 체크리스트

- [ ] 모든 평가 대상 직무에 JD가 있는가
- [ ] 평가위원회 구성·교육 기록이 있는가
- [ ] Anchor Job이 명확히 선정·평가되었는가
- [ ] 점수 분포가 합리적인가 (Cliff/Cluster 없음)
- [ ] Job Family·Track 매핑이 누락 없는가
- [ ] 직무 수행자 커뮤니케이션 가이드가 있는가
- [ ] 향후 운영을 위한 매뉴얼이 있는가

## 연계 에이전트·스킬

**에이전트:**
- `job-evaluation-expert` (주관)
- `research-analyst` (시장 매칭)
- `consulting-writer` (산출물 문서화)

**선행/후행 스킬:**
- 선행: `jd-development`
- 후행: `pay-structure-design`, `competency-modeling`

## 참고 지식베이스

- `01_지식베이스/방법론/Mercer_WTW_IPE.md`
- `01_지식베이스/방법론/Hay_Guide_Chart.md`
- `01_지식베이스/방법론/한국형_방법론.md`
- `01_지식베이스/케이스스터디/직무평가_사례.md`
