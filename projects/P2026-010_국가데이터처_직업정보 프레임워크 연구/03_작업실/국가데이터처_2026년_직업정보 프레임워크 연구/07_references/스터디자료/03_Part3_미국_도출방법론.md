# Part 3. 미국의 도출 방법론 — HumRRO 게이트키핑 + WA Project 클러스터링

## 학습 목표

1. **HumRRO 보고서**(2002/2003)의 TASK 품질관리 5단계 의사결정나무를 회상하고 적용할 수 있다.
2. **WA Project 보고서**(2014)의 7단계 클러스터링 절차와 DWA→IWA 위계 도출 방식을 설명할 수 있다.
3. **종단 파이프라인**(write-in → TASK → DWA → IWA → GWA 매핑)을 도식화할 수 있다.
4. 두 보고서의 핵심 수치(15명·67%·3.0·4 task·Kappa 0.88 등)를 발표 Q&A 카드로 정리할 수 있다.

---

## 3.1 두 보고서의 좌표

미국 O*NET 4계층 활동 체계는 단일 보고서가 아니라 **11년 간격을 두고 결합된 두 보고서**가 합쳐서 만든 결과물입니다.

```
            [ GWA  41개 ]      ←  WA 보고서가 매핑 대상으로 사용
                  ↑
            [ IWA  332개 ]     ←  WA 보고서가 신규 개발 (2014)
                  ↑
            [ DWA  2,087개 ]   ←  WA 보고서가 신규 개발 (2014)
                  ↑
            [ Tasks 19,000+ ]  ← HumRRO가 품질관리 절차 정립 (2002/2003)
                  ↑
            [ Incumbent 응답 ] ← HumRRO가 "write-in" 처리절차 정의
```

| 보고서 | 발간 | 역할 |
|--------|------|------|
| **HumRRO** | 2002 (rev. 2003) | TASK 층의 **품질 게이트키핑** 정립 — "이 진술이 진짜 task인가? 핵심인가? 신규인가?" |
| **WA Project** | 2014 | HumRRO가 거른 task들을 **귀납적 추상화**하여 DWA·IWA 도출 |

---

## 3.2 HumRRO 보고서 — TASK 품질관리

### 3.2.1 연구 설계

HumRRO 프로젝트는 노스캐롤라이나 O*NET Center가 발주한 3단계 과업 중 2단계(파일럿) 결과보고서입니다.

| 과업 | 내용 |
|------|------|
| Task 1 | Task 데이터 분석 근거(rationale)와 기준(criteria) 개발 |
| Task 2 | 8개 pretest 직업의 데이터로 기준을 검증 |
| Task 3 | O*NET 전체 데이터수집 프로그램에 적용 |

두 종류의 데이터셋을 다룹니다.

| 데이터셋 | 규모 | 출처 |
|---------|-----|-----|
| 기존 Task 진술(current task) | 87개 진술 | 8개 pretest 직업 |
| 자유응답 Task(write-in) | 1,088개 진술 (411명 응답자) | 16개 직업 (pretest 8 + 추가 8) |

> **두 데이터셋의 분석 목적이 다름**: Current task는 "기존 목록에서 무엇을 살리고 버릴지"의 **가지치기(pruning)**, write-in은 "새로 무엇을 들여올지"의 **신규편입(introduction)** 문제입니다.

### 3.2.2 평가 척도

응답자(incumbent)가 각 task에 대해 **3가지 차원**을 평정합니다.

| 차원 | 척도 | 비고 |
|------|------|------|
| **Relevance** | 이진 ("not relevant" 표시) | 직접적 relevance 질문은 없음. 응답자/비응답자 비율로 사후 계산 |
| **Importance** | 5점 (1=not important … 5=extremely important) | 평균 3.0 이상이 retain 기준 |
| **Frequency** | 7점 (1=once a year or less … 7=hourly or more) | 단독 retain 기준으로는 부적합 |

### Relevance 계산식

```
percent_relevant = (importance 또는 frequency를 평정한 응답자 수)
                   ÷
                   (importance/frequency 평정자 + "not relevant" 표기자)
```

**핵심 설계**: 응답하지 않은 사람(missing)은 분모에서 제외됨. "모르는 사람"은 빼고, "잘 아는데 무관하다고 명시한 사람"만 분모로.

> **한국 적용 시 권고**: 설문 UI에서 "해당 없음" 옵션을 명시적으로 분리해야 합니다. 그냥 무응답으로 처리하면 relevance 계산이 무너집니다.

### 3.2.3 표본 크기의 통계적 근거

"task당 최소 15명" 기준은 그냥 정한 것이 아니라 **표준오차(SEM) 시뮬레이션**으로 도출했습니다.

- 목표: 평균 중요도(7점 척도)의 SEM ≤ 0.50
- 검증 방법: 각 task에서 5명, 10명, 15명 무작위 표본의 SEM 계산
- 결과:
  - 15명 표본의 평균 SEM = 0.21 (range 0.07–0.31) → 매우 안전
  - 7명까지 줄여도 대부분 task에서 SEM < 0.50 유지
- 결정: 이전 OMB 가이드라인(KSAO 추정용 15명)과의 정합성을 위해 **15명 채택**

> **방법론적 함의**: 한국에서도 직업당 최소 응답자 수 기준을 정할 때, 단순히 미국 사례를 차용하지 말고 한국 K-NCS·KECO 데이터로 **자체 SEM 시뮬레이션**을 1회 돌려두는 것이 발표 Q&A에서 강력한 방어 카드가 됩니다.

### 3.2.4 Current Task 평가 — 초기 vs 최종 기준

#### 초기 기준 (3개 조건 AND)
1. 최소 응답자 ≥ 15명
2. Relevance ≥ 50%
3. Mean Importance ≥ 3.0

**적용 결과 (87 tasks)**:

| 기준 | retain 비율 |
|------|-----------|
| 응답자 ≥ 15명 | 100% |
| Relevance ≥ 50% | 92.36% |
| Importance ≥ 3.0 | 96.85% |
| **3개 모두 충족** | **91.23%** |

#### 흥미로운 발견: Task 수와 평정의 부적상관

> "the fewer the tasks included in an occupation, the higher the relevance, importance, and frequency ratings of those tasks. (r = -.64 for importance)"

즉 **task가 적게 정의된 직업일수록 각 task의 평균 중요도가 높게 평정됨**.

**해석**: task가 많은 직업은 응답자별로 "내가 안 하는 task"가 많아 평균이 낮아짐. task가 적은 직업은 모든 task가 핵심으로 보여 평균이 높아짐.

**방법론적 위험**: task list의 길이 자체가 중요도 평정의 편향(bias)을 만든다. 단순 평균 비교는 위험.

#### 최종 기준 — 3-tier 분류로 세분화

초기 이진 판정에서 **3개 카테고리**로 세분화되었습니다.

| 카테고리 | Relevance | Importance | 비고 |
|---------|-----------|-----------|------|
| **Core Tasks** | > 67% | > 3.0 | 직업의 핵심 task |
| **Supplementary** (Type A) | > 67% | < 3.0 | 보편적이지만 덜 중요 |
| **Supplementary** (Type B) | 10–66% | (무관) | 일부 incumbent에게만 해당 |
| **Non-relevant** | < 10% | (무관) | 폐기 |

> **변경 포인트**: 초기 50% threshold가 67%로 상향. 동시에 50% 미만이라고 무조건 버리지 않고 10%라는 완화된 임계로 supplementary 카테고리를 만듦.
>
> **한국 적용 시 권고**: 67%/10% 이중 임계는 통계청·국가데이터처 측에 "왜 이 숫자인가" 문답을 받을 가능성이 큽니다. 우리 보고서에서는 **분포 시각화(히스토그램)와 함께** 임계를 정당화해야 합니다.

### 3.2.5 Write-in Task 의사결정나무

HumRRO의 가장 큰 기여는 **3차례 진화한 의사결정나무**입니다.

#### 초기 절차 (Figure 1, 9-step)

```
1. task인가?
2. current task와 동일한가?
3. current task와 부분적 중복인가?
4. 다른 write-in과 결합 가능한가?
5. 10명 이상이 평정했는가?
6. 평균 중요도가 기준 충족인가?
7. 직업 정의·GWA와 일관되는가?
8. 적절한 specificity인가?
9. 형식(verb-object)이 맞는가?
→ 새 statement 작성
```

#### 수정 절차 (Figure 2, 7-step)

처음 두 직업 분석 후 변경:
- 일관성 검사를 Step 7 → Step 4로 이동
- 임계 응답자 수 10 → 15
- Specificity·Format을 작성단계로 이관

#### 최종 권고 절차 (Figure 3, **5-step**)

```
1. task인가? (No → 폐기)
2. current task와 동일한가? (Yes → 폐기)
3. current task와 부분적 중복? → 관련 current task 기록
4. 다른 write-in 4개 이상과 동일/유사한가? (No → 폐기)
5. emerging task list에 추가
```

> **단계 축소의 근거**:
> - 일관성 검사 제거: 거의 모든 write-in이 직업과 일관되어 거를 가치가 적었음
> - 중요도 임계 제거: write-in을 적은 응답자 대부분이 자기 task를 중요하다고 평정 → 변별력 없음
> - 임계 인원 9명 → 4명: write-in 응답자 수 자체가 적은 현실 반영
>
> **한국 적용 시 함의**: 절차를 처음부터 슬림하게 잡으려 하지 말고, **초기에 9-step 정도로 보수적으로 설계 → pilot 결과로 단계 축소** 순서가 옳음. 우리의 AI 자동분류 단계도 이 진화 패턴을 따라야 함(과적합 방지).

### 3.2.6 분석가 간 일치도 (Interrater Agreement)

HumRRO는 두 명의 I-O 심리학 박사급 연구자가 첫 3개 직업의 write-in을 **독립평정**한 뒤 일치도를 측정.

| 판정 항목 | Agreement | Cohen's Kappa |
|---------|---------|--------------|
| 1. task인가? | 93% | .83 |
| 2. current task와 완전 중복? | 96% | .86 |
| 3. current task와 부분 중복? | 96% | .95 |
| 4. 직업과 일관? | 97% | .87 |
| **평균** | **96%** | **.88** (p < .001) |

**Kappa 0.88의 의미**: Landis & Koch(1977) 분류로 "almost perfect agreement". 절차가 매우 명확해서 두 분석가가 거의 같은 판정을 내릴 수 있다는 의미.

**불일치 원인**: 대부분 "이게 task인가 KSAO/GWA인가"의 **경계 사례**. abstract level의 차이가 가장 모호한 지점.

### 3.2.7 Write-in 결과의 정량 분석

총 1,088개 write-in 진술의 분류 결과:

```
1,088 write-in
├── 376 (35%) Non-tasks
│   ├── 39% incomprehensible (이해불가)
│   ├── 27% too broad (지나치게 광범위)
│   ├── 18% KSAO (지식·기술·능력·기타특성)
│   ├── 14% GWA (일반화 직무활동)
│   └──  2% misc (예: 자격요건)
└── 712 (65%) Tasks
    ├── 56% unique (현재 목록과 무관)
    ├── 25% partially redundant
    └── 19% completely redundant
```

**최종 산출**:
- 16개 직업 × 평균 4.25개의 emerging task = **17개 task**가 emerging list에 등재
- 즉 1,088개 응답에서 17개(**1.6%**)만이 실제로 새로운 emerging task로 살아남음

> **압도적 가지치기 비율의 함의**:
> - 자유응답에서 진짜 신규 task가 살아남는 비율은 1~2% 수준으로 매우 낮음
> - **NLP 활용 정당화**: NLP가 "이 진술이 task가 아니다(35% 가지치기)"를 95% 정확도로 자동분류할 수 있다면, 인간 분석가의 작업 부하는 65%로 감소. 이는 본 연구 NLP 효율성 주장의 핵심.

### 3.2.8 운영 비용 추정

> "the time required for one researcher to analyze write-in statements for an occupation varied from 2 to 12 hours (M = 4 hours)"

- 직업당 평균 4시간/분석가
- 한국 KSCO 495개 직업 × 4시간 = **약 2,000시간(1명)** 또는 **6개월 풀타임 2명**
- 단, 이는 write-in 분석에만 해당. Current task 분석·DWA 작성은 별도.

> **제안발표용 핵심 수치**: 미국 사례에서 1명 분석가가 직업당 평균 4시간을 썼다는 점을 들어, 한국 8개월·6명 체제에서 NLP 보조 없이는 약 500개 직업이 한계임을 정량적으로 보여줄 수 있음.

---

## 3.3 WA Project 보고서 — DWA·IWA 도출

### 3.3.1 프로젝트 위상

| 차원 | 기존(legacy) | 신규(WA Project) |
|------|------------|-----------------|
| Tasks 수 | 19,450 | 19,450 (입력 그대로) |
| GWA 수 | 41 | 41 (변경 없음, 매핑만 갱신) |
| DWA 수 | 2,164 | 2,069 (전면 재작성) |
| IWA 수 | **없음** | **332 신규 도입** |
| 계층구조 | GWA—DWA—Tasks (3층) | GWA—IWA—DWA—Tasks (**4층**) |

WA Project의 본질은 **DWA 전면 재작성 + IWA 신규 개발**. 단순 갱신이 아니라 위계의 재설계.

### 3.3.2 정량 vs 정성 — 의사결정의 논리 (중요)

WA 보고서가 처음에 결정한 가장 중요한 선택입니다.

| 접근 | 방식 | 장점 | 단점 |
|------|------|------|------|
| **정량(NLP)** | task를 verb–object–purpose로 분해, 코드화 → 군집분석 | 빠름, 일관성 | task 구조 변동성으로 핵심 활동 추출 신뢰도 낮음 |
| **정성(rational)** | task 전체를 인간 분석가가 의미 단위로 평가·군집 | 정밀, 정확 | 느림, 인적자원 다대 |

핵심 인용:

> "task statement structure is so variable that it would be very difficult for a technical system to reliably derive the most important data from tasks. In short, **human judgment was determined to be paramount** in the development of a logical, meaningful, and useful system."

> **2014년 시점의 한계 vs 2026년 시점의 기회**:
> - WA 프로젝트가 NLP를 거부한 결정적 이유는 "task 구조의 변동성"이었음. 2014년 NLP는 BERT(2018) 이전이고 LLM은 미존재.
> - 2026년에는 LLM이 verb–object 분리뿐 아니라 의미적 군집까지 인간 수준으로 가능. **WA 보고서의 "human judgment is paramount" 결론은 더 이상 유효하지 않음**.
> - 본 제안의 차별화 포인트: "WA가 정성 방식을 택한 것은 당시 기술 한계 때문이지 원리적 우위 때문이 아니다. 2026년에는 LLM이 정량+정성 통합을 가능하게 한다."

### 3.3.3 팀 구성과 작업 단위

| 구분 | 인원 |
|------|------|
| Development teams | 3–4개 팀 (단계에 따라 변동) |
| 팀당 인원 | 3–4명 |
| 팀 구성 | 경험있는 occupational analyst 1명(팀장) + I-O 심리학 박사과정생 2–3명 |
| 도구 | 온라인 스프레드시트 (실시간 협업) |

> **시사점**: 미국조차 박사과정 인력을 대량 투입했음. 본 사업은 6명 체제 — **모든 직업을 인간이 다 다루는 것은 물리적으로 불가능**. NLP 자동화는 옵션이 아니라 필수.

### 3.3.4 DWA 개발 — Phase A: Task Clustering

#### Step 1. Job Family로 1차 분할

22개 O*NET Job Family(SOC 대분류와 동등) 사용. 결과: 134개(Legal) ~ 2,344개(Production) tasks per family.

| Job Family (예시) | # 직업 | # tasks |
|-----------------|--------|---------|
| Production | 112 | 2,344 |
| Healthcare Practitioners | 86 | 1,683 |
| Education, Training, Library | 61 | 1,591 |
| Architecture & Engineering | 71 | 1,431 |
| Management | 59 | 1,294 |
| ... | ... | ... |
| Legal | 8 | 134 |

**근거**: DWA는 정의상 "단일 job family 내 다수 직업에 적용"되므로 family별 분할이 클러스터 동질성 확보에 필수.

#### Step 2. GWA 41개에 task 할당

- 3–4명의 분석가가 **독립적으로** 각 task에 가장 적합한 GWA 1개 선택
- 모든 팀원이 동일 GWA를 고른 task = "consensus"
- 한 명만 다른 의견 = "majority rule" → consensus로 처리
- 의견 분기 task만 별도 워크시트로 → 토론 통해 합의

**Healthcare 1,683개 task 예시**:
- 1,277개 (76%): consensus/majority로 즉시 GWA 분류
- 406개 (24%): 별도 토론 후 합의

> **GWA 할당의 어려움**: task 진술이 다음을 동시에 포함하기 때문.
> - **목적절** (purpose clauses): "to determine specifications"
> - **도구** (tools/technology): "using hand tools or power saws"
> - **예시절** (exemplar clauses): "such as updating records"
> - **복합활동** (multiple activities): "test and adjust equipment"
>
> 분석가는 이 중 **primary activity**를 식별해야 함. task 텍스트의 의미 구문분석을 인간이 수행한 셈.

#### Step 3. GWA 내 클러스터링 — 7-step 세부 절차

```
3.1 분석가 1인이 GWA 워크시트 부분집합 받음
3.2 task의 GWA 적합도 재검토 → 부적합 task 표시
3.3 다활동 task(multiple activity) flag
3.4 활동 테마별로 코드 부여 (예: 1=assembly, 2=installation, 3=disassembly)
    → 코드 기준 정렬 → 초기 클러스터 형성
3.5 다른 팀원이 코멘트·제안 → 정신모델 공유
3.6 팀장이 부적합 task를 다른 GWA 워크시트로 이동 → 다시 정제
3.7 최종 단일 워크시트로 통합 → 41개 GWA 통합 검토
```

### 3.3.5 DWA 개발 — Phase B: DWA Writing

Part 2에서 다룬 **8대 작성 규칙**을 적용. 핵심 요약:

1. DWA당 동사 1개, 동사로 시작
2. 3인칭·현재·복수형
3. 명사 최소화, "or" 사용 (multiple objects)
4. 직무군 적합 명사
5. 명료성을 위한 형용사
6. 예시절 회피
7. 목적절 최소
8. 8학년 가독성 (SMOG index)

### 3.3.6 DWA 개발 — Phase C: Round-Robin Quality Control

3–4개 팀이 있을 때, 한 팀의 결과물은 다른 두 팀이 순차로 QC 수행.

```
Team A (개발) → Team B (1차 QC, 수정권한 보유) → Team C (2차 QC) → 최종
```

> **장점**: 개발자가 자기 결과를 평가하지 않음(객관성). 거의 모든 팀원이 전체 데이터베이스를 검토(정신모델 공유).
>
> **한국 적용 권고**: 6명을 3개 팀(2명씩)으로 운영. 직무군별로 개발팀–1차QC팀–2차QC팀을 회전.

### 3.3.7 DWA 후처리 4가지

#### Cross-Job Family DWAs (7-step)

같은/유사한 DWA가 서로 다른 job family에서 발견되면 통합 가능성 검토.

```
1. 알파벳 정렬 → identical DWA flag
2. linked task 검토하여 cross-linking 확정
3. near-identical DWA flag
4. linked task의 중복도 평가
5. near-identical DWA를 표준 DWA로 통합
6. cross-family DWA의 클러스터 동질성 재검토
7. 최종 데이터셋에 반영
```

#### Multiple Linkage Identification

하나의 task가 여러 활동을 포함하면, **최대 3개 DWA에 다중연결**.

**연결 분석가 3중 검증**:
- **분석가 1**: 1차 연결 (primary), 가능시 2차·3차 연결 추가
- **분석가 2**: 분석가 1의 결과 검토 → 확정/대안제시/거부
- **분석가 3**: 두 분석가 간 분기 해소

**최종 결과**:
- 22,714 task–DWA 연결 중 1차: 18,291 (81%) / 2차: 3,851 (17%) / 3차: 572 (2.5%)

#### Legacy DWA Integration — 외적 타당도 검증

```
2,164 legacy DWA + 2,069 new DWA → 알파벳 정렬
   ↓
561 legacy DWA가 잠재적 mismatch
   ↓
561 → 51로 축소 (general coverage / too specific / poor wording / obsolete 사유)
   ↓
51 중 4 task & 3 occupation 기준 충족 = 10개
   ↓
10개 legacy DWA를 신규 DB에 통합
```

> 2,164개 legacy 중 단 10개(0.46%)만 새로 추가 → **신규 방법론이 거의 모든 legacy 정보를 포착했다는 외적 타당도 증거**.

### 3.3.8 IWA 개발

IWA 개발은 DWA 개발과 **거의 동일한 절차**(클러스터링 → 라이팅).

| 차이점 | DWA | IWA |
|--------|-----|-----|
| 입력 | 19,450 tasks | 2,069 DWAs |
| 1차 분할 | Job Family로 22개 | **분할하지 않음** (IWA는 family-cross 목적) |
| 클러스터 최소 크기 | 2 tasks | **1 DWA도 허용** |
| 분석팀 | 3–4 팀 × 3–4명 | 1 팀 × 4명 |
| 결과 | 2,069개 | 332개 |

### 3.3.9 결과의 정량 지표

| 지표 | DWA | IWA |
|------|-----|-----|
| 총 개수 | 2,069 (현 30.x 기준 2,087) | 332 |
| Task per unit | 10.98 | 66.36 |
| Occupation per unit | 8.29 | 43.86 |
| Job family per unit (median) | 1 | 3 |
| Single-family | (대부분 single) | 53/332 |
| Cross-family (≥10) | - | 15/332 |
| 미할당 task | 1,159 (6%) | 0 (1:1 강제) |
| Reading level | 평균 8학년 | 평균 8학년 |

> **6% 미할당 task의 의미**: O*NET이 "완전 분류"를 추구하지 않음을 보여줌. 일부 task는 본질적으로 idiosyncratic. 한국 연구에서도 100% 할당을 목표로 잡으면 무리가 발생.

---

## 3.4 두 보고서를 통합한 종단 파이프라인

```
[ 응답자 자유응답 ]
         ↓
   ┌─────────────┐
   │ HumRRO 절차  │  Decision Tree (5-step) — task 여부 / 중복도 / emerging 판정
   └─────────────┘
         ↓
[ 검증된 Task pool ]
         ↓
   ┌─────────────┐
   │ HumRRO 절차  │  3-tier 분류 (Core / Supplementary / Non-relevant)
   └─────────────┘
         ↓
[ Core + Supplementary Tasks ]
         ↓
   ┌─────────────┐
   │  WA Phase A  │  Job Family 분할 → GWA 할당 → GWA 내 클러스터링
   └─────────────┘
         ↓
[ Task Cluster ]
         ↓
   ┌─────────────┐
   │  WA Phase B  │  DWA Writing (8 규칙)
   └─────────────┘
         ↓
[ DWA 2,069 ]
         ↓
   ┌─────────────┐
   │  WA Phase C  │  DWA Refinements (cross-family / multi-link / legacy)
   └─────────────┘
         ↓
   ┌─────────────┐
   │  WA Phase D  │  DWA 클러스터링 → IWA Writing
   └─────────────┘
         ↓
[ GWA—IWA—DWA—Task 4-tier DB ]
         ↓
   ┌─────────────┐
   │  WA Phase E  │  ID 체계 부여, Round-Robin QC
   └─────────────┘
         ↓
[ 최종 데이터베이스 ]
```

---

## 3.5 미국 자원 투입 추정 (역산)

| 항목 | 값 |
|------|---|
| WA 프로젝트 development team | 4팀 × 평균 3.5명 = 14명 |
| 프로젝트 기간 | 추정 12~18개월 |
| 추정 인시 | 14명 × 12개월 = **168 person-month** |
| HumRRO 파일럿 | 추정 6 person-month |

**한국 P2026-010 사업 비교**:
- 6명 × 8개월 = **48 person-month**
- 즉 미국 WA 사업의 **약 30% 자원**으로 동등 결과를 내야 함
- → NLP를 통한 작업효율 **3배 이상 향상**이 산술적으로 필요

> **발표 Q&A 핵심 카드**: "미국 WA 프로젝트는 약 168 person-month, 우리는 48 person-month. 약 3.5배 효율을 NLP로 보완하는 것이 본 사업의 합리적 설계"

---

## 3.6 본 Part 요약 카드

- **HumRRO**(2002/2003)는 TASK 층 **품질관리**: 5-step 의사결정나무, 3-tier 분류, Kappa 0.88
- **WA Project**(2014)는 TASK → DWA → IWA 도출: 22 job family → GWA 할당 → 7-step 클러스터링 → 8-rule writing → round-robin QC
- 두 보고서를 합치면 **write-in → TASK → DWA → IWA → GWA 매핑**의 종단 파이프라인 완성
- 미국은 168 person-month, 한국은 48 person-month → **3.5배 효율을 NLP로 확보 필요**
- WA Project가 2014년에 NLP를 거부한 이유는 task 진술의 구조적 변동성. 2026년 LLM은 이 한계를 해소함

---

## 3.7 다음 단계

Part 4에서는 LLM과 임베딩, 클러스터링 기술이 미국식 절차의 각 단계에서 **어떤 기술 요소를 어떻게 활용**하여 인간 분석가를 보조할 수 있는지를 학습합니다. 본 연구의 핵심 차별화 포인트입니다.
