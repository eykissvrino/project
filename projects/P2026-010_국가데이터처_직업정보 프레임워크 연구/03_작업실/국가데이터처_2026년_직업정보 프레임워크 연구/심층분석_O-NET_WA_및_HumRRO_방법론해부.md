# O*NET Work Activities 기술보고서 & HumRRO 직업과제 예비분석 — 방법론 디테일 해부

**작성 목적**: 국가데이터처 「직업분류 고도화를 위한 직업정보 프레임워크 연구」 제안발표 및 본 연구 수행 시 직접 차용·변형할 수 있는 수준으로 두 핵심 참고자료의 방법론을 단계별로 재현 가능하게 분해한다.

**대상 문헌**
1. Hansen, M.C., Norton, J.J., Gregory, C.M., Meade, A.W., & Foster Thompson, L. (2014). *O\*NET® Work Activities Project Technical Report*. National Center for O\*NET Development. (이하 "WA 보고서")
2. Van Iddekinge, C., Tsacoumis, S., & Donsbach, J. (2002, 2003 rev.). *A Preliminary Analysis of Occupational Task Statements from the O\*NET Data Collection Program* (FR-02-52). HumRRO. (이하 "HumRRO 보고서")

**핵심 메시지**
- HumRRO 보고서는 **최하위 입력층(Tasks)의 데이터 품질 보증** 방법론이다. 즉 "Task 진술이 진짜 task인가, 핵심인가, 신규인가"를 판정하는 게이트키핑 절차다.
- WA 보고서는 그 검증된 Tasks를 **상위 추상층(DWA→IWA→GWA)으로 귀납적으로 끌어올리는** 클러스터링·라이팅 절차다.
- 두 보고서를 합치면 **하나의 종단 파이프라인**이 된다: 현장 응답(write-in) → Task 정제 → Task 클러스터 → DWA 작성 → DWA 클러스터 → IWA 작성 → 기존 GWA에 매핑.
- 우리 연구의 "AI 기반 NLP + O\*NET 방법론 결합"은 이 종단 파이프라인 위에서 **인간 분석 단계를 NLP가 어디까지 대체/보조하는가**를 정의하는 작업이다.

---

## 0. 두 보고서의 좌표: O*NET 인프라 위에서 어디를 다루는가

```
            [ GWA  41개 ]      ←  WA 보고서가 매핑 대상으로 사용
                  ↑
            [ IWA  332개 ]     ←  WA 보고서가 신규 개발
                  ↑
            [ DWA  2,069개 ]   ←  WA 보고서가 신규 개발 (legacy 2,164개 대체)
                  ↑
            [ Tasks 19,450개 ] ← HumRRO 보고서가 품질관리 절차 정립
                  ↑
            [ Incumbent / Expert 응답 ] ← HumRRO가 "write-in" 처리절차 정의
```

- HumRRO 보고서(2002/2003)가 먼저 Tasks 층의 게이트키핑 규칙(15명 이상, 50% relevance, 평균 중요도 3.0 이상 등)을 만들었기에, 이후 O\*NET 18.0(2013) 시점에 19,450개 Tasks가 안정적인 입력자료로 사용될 수 있었다.
- WA 보고서(2014)는 그 입력자료를 받아 DWA·IWA를 귀납적으로 도출했다. 즉 두 보고서는 **시간순서상 단순 병렬이 아니라, 11년 간격을 두고 순차 결합된 작업**이다.
- 이는 우리 연구가 한국에서 "Tasks 품질관리 → DWA·IWA·GWA 도출"을 8개월 안에 동시 수행해야 한다는 것을 의미한다. 즉 미국이 11년에 나누어 한 일을 압축해야 한다는 점에서 자동화(NLP) 활용은 단순 차별화가 아니라 **사업기간 제약상의 필연**이다.

---

# Part I. HumRRO 보고서 방법론 해부

## 1.1 연구 설계 개요

HumRRO 프로젝트는 노스캐롤라이나 O\*NET Center가 발주한 3단계 과업 중 2단계(파일럿) 결과보고서다.

| 과업 | 내용 |
|------|------|
| Task 1 | Task 데이터 분석 근거(rationale)와 기준(criteria) 개발 |
| Task 2 | 8개 pretest 직업의 데이터로 기준을 검증 |
| Task 3 | O\*NET 전체 데이터수집 프로그램에 적용 |

본 보고서는 Task 2 결과물로, **두 종류의 데이터셋**을 동시에 다룬다.

| 데이터셋 | 규모 | 출처 직업수 |
|----------|------|-------------|
| 기존 Task 진술(current task) | 87개 진술 | 8개 pretest 직업 |
| 자유응답 Task(write-in) | 1,088개 진술 (411명 응답자) | 16개 직업 (pretest 8 + 추가 8) |

> **주의**: 두 데이터셋은 분석 목적이 완전히 다르다. Current task는 "기존 목록에서 무엇을 살리고 무엇을 버릴지"의 가지치기(pruning), write-in은 "새로 무엇을 들여올지"의 신규편입(introduction) 문제다.

## 1.2 평가 척도의 설계

응답자(incumbent)가 각 task에 대해 **3가지 차원**을 평정한다.

| 차원 | 척도 | 비고 |
|------|------|------|
| **Relevance** | 이진 (해당 task가 not relevant인지 표시) | 직접적 relevance 질문은 없음. 응답 안 한 사람과 응답한 사람의 비율로 사후 계산 |
| **Importance** | 5점 (1=not important … 5=extremely important) | 평균 3.0 이상이 retain 기준 |
| **Frequency** | 7점 (1=once a year or less … 7=hourly or more) | 단독 retain 기준으로는 부적합(중요하지만 드문 task 존재) |

### Relevance 계산식 (HumRRO 보고서 p.2)

```
percent_relevant = (importance 또는 frequency를 평정한 응답자 수)
                   ÷
                   (importance/frequency 평정자 + "not relevant" 표기자)
```

> **시사점**: 응답하지 않은 사람(missing)은 분모에서 제외된다. 즉 "모르는 사람"은 판정에서 빼고, "잘 아는데 무관하다고 명시한 사람"만 분모로 들인다는 설계 원칙이다. 한국 적용 시 동일한 구조를 따르려면 설문 UI에서 "해당 없음" 옵션을 명시적으로 분리해야 한다.

## 1.3 표본 크기 결정의 통계적 근거

HumRRO는 "task당 최소 15명" 기준을 그냥 정한 것이 아니라, **표준오차(SEM) 시뮬레이션**으로 도출했다.

- 목표: 평균 중요도(7점 척도)의 SEM ≤ 0.50
- 검증 방법: 각 task에서 5명, 10명, 15명 등 다양한 표본을 무작위로 추출하여 SEM 계산
- 결과:
  - 15명 표본의 평균 SEM = 0.21 (range 0.07–0.31) → 매우 안전
  - 7명까지 줄여도 대부분 task에서 SEM < 0.50 유지
- 결정: 이전 OMB 가이드라인(KSAO 추정용 15명)과의 정합성을 위해 **15명을 채택**

> **방법론적 함의**: 한국에서도 직업당 최소 응답자 수 기준을 정할 때, 단순히 미국 사례를 차용하지 말고 한국 K-NCS·KECO 데이터로 **자체 SEM 시뮬레이션**을 1회 돌려두는 것이 발표 Q&A에서 강력한 방어 카드가 된다. (예: "한국 응답자의 분산이 미국보다 큰 직업군이 있을 수 있어 직접 검증했다")

## 1.4 Current Task 평가: 초기 기준 vs 최종 기준

### 초기 기준 (보고서 p.2)
1. 최소 응답자 ≥ 15명
2. Relevance ≥ 50%
3. Mean Importance ≥ 3.0

### 적용 결과 (8개 pretest 직업, 87 tasks)

| 기준 | retain 비율 |
|------|-------------|
| 응답자 ≥ 15명 | 100% |
| Relevance ≥ 50% | 92.36% |
| Importance ≥ 3.0 | 96.85% |
| **3개 모두 충족** | **91.23%** |

### 흥미로운 발견: Task 수와 평정의 부적상관

> "the fewer the tasks included in an occupation, the higher the relevance, importance, and frequency ratings of those tasks. (r = -.64 for importance)" (HumRRO 보고서 p.3)

- 즉 **task가 적게 정의된 직업일수록 각 task의 평균 중요도가 높게 평정된다.**
- 해석: task가 많은 직업은 응답자별로 "내가 안 하는 task"가 많아 평균이 낮아지고, task가 적은 직업은 모든 task가 핵심으로 보여 평균이 높아진다.
- **방법론적 위험**: task list의 길이 자체가 중요도 평정의 편향(bias)을 만든다. 단순 평균 비교는 위험하다.

### 최종 기준 — 3-tier 분류로 세분화 (보고서 p.13)

초기 기준은 "retain/eliminate"의 이진 판정이었으나, 최종은 **3개 카테고리**로 세분화되었다.

| 카테고리 | Relevance | Importance | 비고 |
|----------|-----------|------------|------|
| **Core Tasks** | > 67% | > 3.0 | 직업의 핵심 task |
| **Supplementary Tasks** (Type A) | > 67% | < 3.0 | 보편적이지만 덜 중요 |
| **Supplementary Tasks** (Type B) | 10–66% | (무관) | 일부 incumbent에게만 해당 |
| **Non-relevant Tasks** | < 10% | (무관) | 폐기 |

> **변경 포인트**: 초기 50% threshold가 67%로 상향되었다. 이는 "core"라는 명칭이 부여되려면 더 엄격한 합의가 필요하다는 판단이다. 동시에 50% 미만이라고 무조건 버리지 않고, 10%라는 완화된 임계로 supplementary 카테고리를 만들었다.
>
> **한국 적용 시 권고**: 67%/10% 이중 임계는 통계청·국가데이터처 측에 "왜 이 숫자인가" 문답을 받을 가능성이 크다. 우리 보고서에서는 **분포 시각화(히스토그램)와 함께** 임계를 정당화해야 한다. 단순한 65/15/97 임계 차용은 위험.

## 1.5 Write-in Task 평가: 의사결정나무(Decision Tree)의 진화

HumRRO의 핵심 기여 중 하나는 **3차례 진화한 의사결정나무**다.

### 1.5.1 초기 절차 (Figure 1, 9-step)

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

### 1.5.2 수정 절차 (Figure 2, 7-step)

처음 두 직업을 분석한 결과 다음 변경:
- **단계 4의 일관성 검사를 앞으로**: 직업 정의·GWA와의 일관성 검증을 Step 7에서 Step 4로 이동
- **임계 응답자 수 10 → 15**: current task 기준(15명)과 정합 확보
- **Step 8(specificity)·9(format)을 작성단계로 이관**: 판정과 작성을 분리

### 1.5.3 최종 권고 절차 (Figure 3, 5-step)

```
1. task인가? (No → 폐기)
2. current task와 동일한가? (Yes → 폐기)
3. current task와 부분적 중복? → 관련 current task 기록
4. 다른 write-in 4개 이상과 동일/유사한가? (No → 폐기)
5. emerging task list에 추가
```

> **단계 축소의 근거**:
> - 일관성 검사(former Step 4) 제거: 실제 분석 결과 거의 모든 write-in이 직업과 일관되어, 거를 가치가 적었음 → "the write-in statements were consistent with the target occupation, which suggests the evaluation of their consistency is an unnecessary step"
> - 중요도 임계(former Step 6) 제거: write-in을 적은 응답자 대부분이 자기 task를 중요하다고 평정 → 변별력 없음 → "It is unlikely that importance ratings will be a useful criterion, as the vast majority of incumbents indicated that their write-in statements were important"
> - 임계 인원 9명 → 4명: write-in 응답자 수 자체가 적은 현실 반영
>
> **한국 적용 시 함의**: 절차를 처음부터 슬림하게 잡으려 하지 말고, **초기에 9-step 정도로 보수적으로 설계 → pilot 결과로 단계 축소** 순서가 옳다. 우리 제안서의 "AI로 자동분류" 단계도 이 진화 패턴을 따라야 한다(과적합 방지).

## 1.6 분석가 간 일치도 (Interrater Agreement)

HumRRO는 두 명의 I-O 심리학 박사급 연구자가 첫 3개 직업의 write-in을 **독립평정**한 뒤 일치도를 측정했다.

| 판정 항목 | Agreement | Cohen's Kappa |
|-----------|-----------|---------------|
| 1. task인가? | 93% | .83 |
| 2. current task와 완전 중복? | 96% | .86 |
| 3. current task와 부분 중복? | 96% | .95 |
| 4. 직업과 일관? | 97% | .87 |
| **평균** | **96%** | **.88** (p < .001) |

> **Kappa 0.88의 의미**: Landis & Koch(1977) 분류로 "almost perfect agreement". 즉 절차가 매우 명확해서 두 분석가가 거의 같은 판정을 내릴 수 있다.
>
> **불일치 원인**: 대부분 "이게 task인가 KSAO/GWA인가"의 경계 사례. 즉 abstract level의 차이가 가장 모호한 지점이다. 이는 우리 연구의 직무기술 정의서 작성에서도 가장 큰 혼선 지점이 될 것이다.

## 1.7 Write-in 결과의 정량 분석

총 1,088개 write-in 진술의 분류 결과(보고서 p.11–12):

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
- 즉 1,088개 응답에서 17개(1.6%)만이 실제로 새로운 emerging task로 살아남는다.

> **압도적 가지치기 비율**의 함의:
> - 자유응답에서 진짜 신규 task가 살아남는 비율은 1–2% 수준으로 매우 낮다.
> - 이는 task 진술의 품질관리에 대단히 큰 인적·시간 비용이 드는 데 비해, 실질적 갱신 효과는 제한적임을 시사한다.
> - **NLP 활용 정당화**: 만약 NLP가 "이 진술이 task가 아니다(35% 가지치기)"를 95% 정확도로 자동분류할 수 있다면, 인간 분석가의 작업 부하는 65%로 감소한다. 이는 우리 제안의 핵심 효율성 주장이다.

## 1.8 운영 비용 추정 (보고서 p.15)

> "the time required for one researcher to analyze write-in statements for an occupation varied from 2 to 12 hours (M = 4 hours)"

- 직업당 평균 4시간/분석가
- 한국 K-NCS 약 1,000개 직업 × 4시간 = **4,000시간(2명)** 또는 **1년 풀타임 2명**
- 단, 이는 write-in 분석에만 해당. Current task 분석·DWA 작성은 별도.

> **제안발표용 핵심 수치**: 미국 사례에서 1명 분석가가 직업당 평균 4시간을 썼다는 점을 들어, 한국 8개월·6명 체제에서 NLP 보조 없이는 약 500개 직업이 한계임을 정량적으로 보여줄 수 있다. NLP가 4시간을 1시간으로 단축한다면 2,000개까지 가능하다는 식의 시나리오 분석.

---

# Part II. O*NET Work Activities 보고서 방법론 해부

## 2.1 프로젝트 위상 정리

| 차원 | 기존(legacy) | 신규(WA Project) |
|------|--------------|-------------------|
| Tasks 수 | 19,450 | 19,450 (입력 그대로) |
| GWA 수 | 41 | 41 (변경 없음, 매핑만 갱신) |
| DWA 수 | 2,164 | 2,069 (전면 재작성) |
| IWA 수 | **없음** | **332 신규 도입** |
| 계층구조 | GWA—DWA—Tasks (3층) | GWA—IWA—DWA—Tasks (4층) |

WA 프로젝트의 본질은 **DWA 전면 재작성 + IWA 신규 개발**이다. 단순 갱신이 아니라 위계의 재설계다.

## 2.2 정량 vs 정성 접근 — 의사결정의 논리

WA 보고서 Section II에서 핵심 의사결정이 명시된다 (p.13).

| 접근 | 방식 | 장점 | 단점 |
|------|------|------|------|
| **정량(NLP)** | task를 verb–object–purpose로 분해, 코드화 → 군집분석 | 빠름, 일관성 | task 구조의 변동성으로 핵심 활동 추출 신뢰도 낮음 |
| **정성(rational)** | task 전체를 인간 분석가가 의미 단위로 평가·군집 | 정밀, 정확 | 느림, 인적자원 다대 |

> **핵심 인용**: "task statement structure is so variable that it would be very difficult for a technical system to reliably derive the most important data from tasks. In short, human judgment was determined to be paramount in the development of a logical, meaningful, and useful system."

> **2014년 시점의 한계 vs 2026년 시점의 기회**:
> - WA 프로젝트가 NLP를 거부한 결정적 이유는 "task 구조의 변동성"이었다. 2014년 NLP는 BERT(2018) 이전이고 LLM은 미존재.
> - 2026년에는 LLM이 verb–object 분리뿐 아니라 의미적 군집까지 인간 수준으로 가능. **WA 보고서의 "human judgment is paramount" 결론은 더 이상 유효하지 않다**.
> - 우리 제안의 차별화 포인트는 바로 이 부분이다. "WA가 정성 방식을 택한 것은 당시 기술 한계 때문이지 원리적 우위 때문이 아니다. 2026년에는 LLM이 정량+정성 통합을 가능하게 한다."
> - 단, 이 주장을 발표에서 강하게 펼치려면 **소규모 prototype 결과**를 보여줄 수 있어야 한다 (예: 100개 task에 대해 GPT-4o가 인간 분석가와 90% 일치한 예시).

## 2.3 팀 구성과 작업 단위

| 구분 | 인원 |
|------|------|
| Development teams | 3–4개 팀 (단계에 따라 변동) |
| 팀당 인원 | 3–4명 |
| 팀 구성 | 경험있는 occupational analyst 1명 (팀장) + I-O 심리학 박사과정생 2–3명 |
| 도구 | 온라인 스프레드시트 (실시간 협업) |

> **시사점**: 미국조차 박사과정 인력을 대량 투입했다. 이는 클러스터링·라이팅 단계가 단순 코딩이 아니라 **고도의 의미 판단**을 요구한다는 점을 보여준다. 한국 연구진(6명)으로는 **모든 직업을 인간이 다 다루는 것은 물리적으로 불가능**하다. NLP 자동화는 옵션이 아니라 필수다.

## 2.4 DWA 개발 — 7-step 절차의 완전 해부

### 2.4.1 Phase A: Task Clustering

#### Step 1. Job Family로 1차 분할

- 22개 O\*NET Job Family(SOC 대분류와 동등) 사용
- 결과: 134개(Legal) ~ 2,344개(Production) tasks per family

| Job Family (예시) | # 직업 | # tasks |
|-------------------|--------|---------|
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
- 데이터베이스 폼 인터페이스 사용 (Figure 3)
- 모든 팀원이 동일 GWA를 고른 task = "consensus" → 41개 GWA 워크시트로 분배
- 한 명만 다른 의견 = "majority rule" → consensus로 처리
- 의견 분기 task만 별도 워크시트로 → 토론 통해 합의

**1,683개 task의 Healthcare 직업군 예시**:
- 1,277개 (76%): consensus/majority로 즉시 GWA 분류
- 406개 (24%): 별도 토론 후 합의

> **GWA 할당의 어려움**: task 진술이 다음을 동시에 포함하기 때문이다.
> - **목적절** (purpose clauses): "to determine specifications"
> - **도구** (tools/technology): "using hand tools or power saws"
> - **예시절** (exemplar clauses): "such as updating records"
> - **복합활동** (multiple activities): "test and adjust equipment"
>
> 분석가는 이 중 **primary activity**를 식별해야 한다. 즉 task 텍스트의 의미 구문분석을 인간이 수행한 셈이다.
>
> **NLP 자동화 포인트**: LLM은 task 진술에서 verb-object pair 추출, 부수절(purpose/tools/example) 분리, primary activity 판정을 동시에 수행 가능. 이는 우리 제안의 핵심 모듈이 되어야 한다.

#### Step 3. GWA 내 클러스터링 — 7-step 세부 절차

(WA 보고서 p.21–24)

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

#### 클러스터 5대 품질 기준

| 기준 | 정의 |
|------|------|
| **Cluster Homogeneity** | 동일 활동 테마를 강하게 공유 |
| **Task-Cluster Fit** | 개별 task가 클러스터 테마에 잘 맞음 (outlier 식별) |
| **Cluster Uniqueness** | job family 내 다른 클러스터와 개념적으로 구별 |
| **Cluster Specificity** | task보다 일반적, GWA보다 구체적 |
| **Cluster Size** | 최소 2 task, 목표 **4 task & 3 occupations** |

> **4 task / 3 occupations 목표비율의 근거**:
> 1. **Cross-occupational linking**: DWA의 본질적 목적은 직업간 연결. 1–2개 직업만 연결하면 의미 없음.
> 2. **장기 안정성**: O\*NET는 task가 정기적으로 add/revise/remove됨. **여유 task가 있어야 1개 task가 사라져도 DWA가 살아남음**.
>
> **한국 적용 시**: 한국표준직업분류 세분류 495개 × 평균 task 약 20개 = 약 1만 task. 동일 비율(4 task/DWA)이라면 약 2,500개 DWA가 적정. 이는 미국 2,069 DWA와 유사 규모.

### 2.4.2 Phase B: DWA 작성 (Writing Standards)

DWA 작성 8대 규칙 (WA 보고서 p.24, Appendix B):

| # | 규칙 | 비고 |
|---|------|------|
| 1 | DWA당 주요 활동동사 1개, 동사로 시작 | |
| 2 | 동사형식: 3인칭·현재·복수 | "Inspect" not "Inspects" or "Inspecting" |
| 3 | 명사 최소화, but 구체성 유지 | "or" 사용 (multiple objects) |
| 4 | job family에 적합한 명사 사용 | "equipment"는 너무 넓음, "laser surgery robots"는 너무 좁음, "medical treatment equipment"가 적절 |
| 5 | 명료성을 위해 형용사 사용 | |
| 6 | 예시절 회피 ("such as", "including") | 꼭 필요할 때만 |
| 7 | 목적절("to ...") 최소 사용 | 단, 활동이 동일해도 목적이 다르면 KSAO가 다를 수 있어 의미 있음 |
| 8 | 8학년 가독성 (SMOG index) | 3음절 이상 단어 수로 측정 |

> **SMOG index 적용**의 함의: O\*NET DWA는 일반 사용자(구직자, 교사, 인사담당자)가 직접 읽고 이해할 수 있어야 한다는 점이 강하게 반영됨. 한국에서도 직무기술 정의서가 단순히 통계청·연구자만의 자료가 아니라, 워크넷·잡코리아 등에서 일반인이 보게 되는 자료임을 고려하면 가독성 기준 채택 권장. 한국어 가독성 지표(KOR-DALE, KU-readability 등) 검토 필요.

### 2.4.3 Phase C: Round-Robin Quality Control

3–4개 팀이 있을 때, 한 팀의 결과물은 다른 두 팀이 순차로 QC를 수행한다.

```
Team A (개발) → Team B (1차 QC, 수정권한 보유) → Team C (2차 QC) → 최종
```

QC 매뉴얼(Appendix C)에 정의된 절차에 따라 수행. 1차 QC팀은 **기존 개발팀과 상의 없이 데이터 수정 권한**을 가짐.

> **이 round-robin 구조의 장점**:
> - 개발자가 자기 결과를 평가하지 않음 (객관성)
> - 거의 모든 팀원이 전체 데이터베이스를 검토하게 됨 (정신모델 공유, 일관성)
>
> **한국 적용 권고**: 6명을 3개 팀(2명씩)으로 운영. 직무군별로 개발팀-1차QC팀-2차QC팀을 회전. 이는 우리 제안서의 "전문가 검토·조정" 단계의 구체적 구현 방식이 된다.

## 2.5 DWA Refinements — 4가지 후처리

### 2.5.1 Cross-Job Family DWAs (7-step)

같은/유사한 DWA가 서로 다른 job family에서 발견되면 통합 가능성 검토.

```
1. 알파벳 정렬 → identical DWA flag
2. linked task 검토하여 cross-linking 확정
3. near-identical DWA flag
4. linked task의 중복도 평가
5. near-identical DWA를 표준 DWA로 통합 (또는 더 일반적 표현으로 통합)
6. cross-family DWA의 클러스터 동질성 재검토
7. 최종 데이터셋에 반영
```

### 2.5.2 Multiple Linkage Identification

하나의 task가 여러 활동을 포함하면, **최대 3개 DWA에 다중연결**.

예시 task: "Measure, cut and install tackless strips along the baseboard or wall"
→ DWA 후보:
1. Measurement
2. Cutting materials
3. Material installation

**연결 분석가 3중 검증**:
- **분석가 1**: 1차 연결 (primary activity), 가능시 2차·3차 연결 추가
- **분석가 2**: 분석가 1의 결과 검토 → 확정/대안제시/거부
- **분석가 3**: 두 분석가 간 분기 해소 (제3안 가능)

**최종 결과**:
- 22,714 task–DWA 연결 중 1차 연결: **18,291개 (81%)**
- 2차 연결: 3,851개 (17%)
- 3차 연결: 572개 (2.5%)

> 이는 task의 평균 약 1.24개 DWA에 연결됨을 의미. 즉 **태깅의 다중성**이 데이터 풍부도의 핵심.

### 2.5.3 Legacy DWA Integration — 외적 타당도 검증

신규 DWA(2,069개)와 기존 DWA(2,164개)의 비교는 **외적 타당도(external validity) 검증**의 의미.

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

> **결과의 의미**:
> - 2,164개 legacy 중 단 10개(0.46%)만 새로 추가 → **신규 방법론이 거의 모든 legacy 정보를 포착했다는 외적 타당도 증거**
> - 동시에 정말 가치있는 미커버 영역 10개를 보완

## 2.6 IWA 개발 — DWA 위에 한 층 더

IWA 개발은 DWA 개발과 **거의 동일한 절차**(클러스터링 → 라이팅), 차이점만 정리:

| 차이점 | DWA | IWA |
|--------|-----|-----|
| 입력 | 19,450 tasks | 2,069 DWAs |
| 1차 분할 | Job Family로 22개 | **분할하지 않음** (IWA는 family-cross 목적) |
| 클러스터 최소 크기 | 2 tasks | **1 DWA도 허용** |
| 분석팀 | 3–4 팀 × 3–4명 | 1 팀 × 4명 (data가 작아서) |
| 결과 | 2,069개 | 332개 |

### Single-DWA IWA 처리의 데이터베이스 설계 논의

이 부분은 보고서에서 가장 흥미로운 데이터모델링 토론(p.32–33).

**문제**: 클러스터에 DWA가 1개만 있는 경우 → IWA를 어떻게 만들 것인가?

**선택지 비교**:
1. 비할당(unassigned) DWA 허용 → "GWA 조부모는 있는데 IWA 부모가 없는" DB 무결성 위반
2. **잔여(residual) IWA 도입** ("All Other ...") → SOC 방식. 하지만 IWA가 완전 분류로 오해받을 위험
3. **단일 DWA IWA 허용 (선택안)** → 1:1 부모-자식 관계 추가

**채택 근거**:
- SOC, NAICS, O\*NET Content Model 모두 child가 immediate parent를 갖도록 설계되어 있음 → 이 관행을 따름
- IWA는 "모든 활동을 망라한 분류"가 아니므로, "All Other"식 잔여 카테고리는 오해 유발

**부작용 완화**:
- IWA 작성단계에서 single-DWA IWA의 표현을 더 일반화하려 시도 (예: DWA "Secure watercraft to docks" → IWA "Tend watercraft")
- 일부는 그대로 유지 (DWA "Train animals" → IWA 동일)
- 향후 신규 task가 추가되면 single-DWA IWA가 conventional IWA로 진화할 것

> **이 의사결정의 일반화된 교훈**:
> - 위계적 분류 시스템에서 **부모 없는 자식 노드를 허용하지 않는 것**이 데이터모델의 표준
> - "잔여 카테고리"의 함정 — 통계청이 한국표준직업분류 8차에서 "기타 ~"를 자주 사용하는데, 이게 분류 완전성에 대한 오해를 유발할 수 있음
> - **한국 적용 시**: 우리 IWA-등가 층을 도입할 때 single-DWA IWA를 허용하되 명시적으로 "임시(placeholder)" 라벨 부여를 권장

## 2.7 식별자(ID) 체계

```
GWA ID:   4.A.1.b.2                                    (Inspecting Equipment, Structures, or Material)
IWA ID:   4.A.1.b.2.I01                                (Administer diagnostic tests to assess patient health)
DWA ID:   4.A.1.b.2.I01.D03                            (Test patient vision)
```

- IWA는 부모 GWA의 9-character ID + "." + "I" + 2-digit
- DWA는 부모 IWA의 ID + "." + "D" + 2-digit
- **IWA·DWA의 번호는 무작위(random) 부여** — 미래 추가 시 번호 재배치 불필요

> **방법론적 미덕**: ID에 의미적 순서를 넣지 않은 결정. 한국에서도 동일 원칙 권장. 한국표준직업분류는 코드에 의미적 순서가 강해서 신규 직업 추가가 어려움.

## 2.8 결과의 정량 지표

| 지표 | DWA | IWA |
|------|-----|-----|
| 총 개수 | 2,069 | 332 |
| Task per unit | 10.98 | 66.36 |
| Occupation per unit | 8.29 | 43.86 |
| Job family per unit (median) | 1 (single family) | 3 |
| Hierarchy span | min 1 family | 53/332 single family, 15/332 ≥10 families |
| 미할당 입력 | 1,159 tasks (6%) | 0 (1:1 강제) |

**Reading level**: DWA·IWA 평균 8학년 (SMOG). 단 기술분야 일부 job family는 10학년 이상.

> **6% 미할당 task의 의미**: O\*NET이 "완전 분류"를 추구하지 않음을 보여줌. 일부 task는 본질적으로 idiosyncratic. 한국 연구에서도 100% 할당을 목표로 잡으면 무리가 발생할 수 있다.

## 2.9 새 DWA 데이터의 4대 개선 차원 (보고서 Section VII)

1. **Relevance(현재성)**: 신·신생직업 반영 (그린·바이오·나노·지오스페이셜)
2. **Completeness(완전성)**: 4-tier 통합 위계로 다중 진입점 확보
3. **Formatting(형식성)**: "use", "follow" 같은 모호 동사 → "operate", "investigate", "measure"로 대체
4. **Specificity(구체성)**: 모호 DWA 제거

> **모호 동사 회피의 사례**:
> - **모호**: use a computer
> - **명확**: operate computers / investigate data / measure performance metrics
>
> 이는 한국어에서도 "사용한다"·"활용한다"·"수행한다" 같은 모호 동사를 피하고, "조작한다"·"점검한다"·"측정한다" 같은 구체동사를 강제하는 것으로 적용 가능.

---

# Part III. 두 보고서를 통합한 종단 파이프라인

## 3.1 통합 파이프라인 도식

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
[ DWA Refined ]
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

## 3.2 단계별 인간 vs NLP 분담 매트릭스

우리 연구의 핵심 차별화 주장은 "AI 기반 NLP + O\*NET 방법론 결합"이다. 두 보고서를 통합하면 단계별로 NLP의 적합성이 달라진다.

| 단계 | 작업 내용 | NLP 적합성 | 권고 |
|------|----------|-----------|------|
| HumRRO Step 1: task 여부 판정 | "이 진술이 task vs KSAO/GWA/jargon" | **매우 높음** | LLM zero-shot 분류 → 인간 검수 5% |
| HumRRO Step 2: current task와 중복 판정 | semantic similarity | **매우 높음** | 임베딩 + cosine similarity |
| HumRRO 3-tier 분류 | 정량 지표 기반 | 자동 (NLP 불필요) | SQL/스프레드시트 |
| WA Step 1: Job Family 할당 | 직업 → 대분류 매핑 | **이미 완료된 작업** | KSCO에 매핑정보 존재 |
| WA Step 2: GWA 41개 할당 | task → GWA 매핑 | **높음** | LLM few-shot, 그러나 다중 활동 분리 필요 |
| WA Step 3: GWA 내 클러스터링 | 의미 군집 | **중간** | HDBSCAN + LLM 후처리. 단 cluster homogeneity 판정은 인간 |
| WA: DWA Writing | 동사 시작·8학년 가독성 | **중간** | LLM 초안 → 인간 편집 |
| WA: Cross-Family 통합 | 알파벳 정렬·유사도 | **매우 높음** | 자동화 가능 |
| WA: Multiple Linkage | 다활동 task 분해 | **높음** | LLM이 verb 다중 추출 |
| WA: IWA 작성 | DWA 클러스터링 + writing | **중간** | LLM 초안 + 인간 편집 |
| **인간 전담**: 최종 QC, Single-DWA IWA 처리, 모호한 의미 판정 | 의미·맥락 이해 | 낮음 | 인간 분석가 |

## 3.3 미국 사례의 자원 투입 추정 (역산)

WA 보고서·HumRRO 보고서에서 직접 명시한 자원 정보는 부분적이지만, 다음을 종합하면 추정 가능.

**WA 프로젝트 (2014)**:
- 4개 development team × 평균 3.5명 = 14명 (graduate student 다수)
- 프로젝트 기간: 보고서에 명시되지 않으나, 19,450 task의 다회 검토를 고려하면 12–18개월
- 추정 인시: 14명 × 약 12개월 = **168 person-month**

**HumRRO 파일럿 (2002–2003)**:
- 박사급 연구자 2명 × 16개 직업 × 4시간 = 128시간 (write-in만)
- + current task 분석, 의사결정나무 개발 = 추정 6 person-month

**한국 P2026-010 사업 비교**:
- 6명 × 8개월 = **48 person-month**
- 즉 미국 WA 사업의 **약 30% 자원**으로 동등 결과를 내야 함
- → NLP를 통한 작업효율 3배 이상 향상이 산술적으로 필요

> **발표 Q&A 핵심 카드**: "미국 WA 프로젝트는 약 168 person-month, 우리는 48 person-month. 약 3.5배 효율을 NLP로 보완하는 것이 본 사업의 합리적 설계"

---

# Part IV. 한국 적용 시 핵심 의사결정 포인트

## 4.1 개념 매핑

| 미국 (O\*NET) | 한국 (현행) | 비고 |
|----------------|--------------|------|
| O\*NET-SOC (1,110 occ.) | 한국표준직업분류 8차 (5단계) | 8차에서 ISCO-08 정합화 |
| 22 Job Families = SOC 대분류 | 한국표준직업분류 대분류 10개, 중분류 52개 | **대분류가 10개로 미국 22개보다 적음** |
| 41 GWAs | (없음) | 신규 도입 필요 |
| 332 IWAs | (없음) | 신규 도입 필요 |
| 2,069 DWAs | (없음) | 신규 도입 필요 |
| 19,450 Tasks | KECO 직무기술 일부 / NCS 능력단위 | 부분적 존재, 통합 필요 |

> **첫 번째 결정**: GWA 등가 층을 도입할 것인가? 도입한다면 미국 41개를 그대로 가져올지, 한국 산업·문화를 반영해 재정의할지.
>
> **권고**: 41개 GWA는 일반화 수준이 매우 높아 문화·국가 의존도가 낮음(예: "Getting Information", "Handling and Moving Objects"). **그대로 한글 번역하여 차용**하는 것이 8개월 사업기간 내 합리적. 단, 한국 노동시장 특수성(예: 회식·경조사 같은 활동) 반영 필요시 일부 보완.

## 4.2 Job Family 단위 — 미국 22 vs 한국 10의 함의

미국이 22개 family로 task를 1차 분할한 핵심 이유는 **DWA의 family-내 적용성** 보장. 한국은 대분류가 10개라 family당 task 수가 미국보다 2배 이상 많아질 수 있음.

| 시나리오 | 1차 분할 단위 | 분할 후 평균 task 수 |
|----------|--------------|---------------------|
| 한국 대분류 10개 사용 | 평균 1,000 tasks/family | 너무 큼 |
| **한국 중분류 52개 사용** | 평균 200 tasks/family | 적정 |
| 한국 소분류 156개 사용 | 평균 60 tasks/family | 너무 작음 (cross-occupational linking 효과 감소) |

> **권고**: **한국표준직업분류 중분류 52개를 1차 분할 단위로 사용**. 이는 미국 22개와 분할 효과가 유사하면서 한국 분류체계와의 정합성 유지.

## 4.3 임계 수치의 한국 보정 필요성

HumRRO의 핵심 임계는 다음과 같다.

| 임계 | HumRRO | 한국 보정 권고 |
|------|--------|----------------|
| 최소 응답자/task | 15명 | **자체 SEM 시뮬레이션 후 결정** (Q&A 대비) |
| Core relevance | > 67% | **분포 검토 후 결정**. 한국 직업의 incumbent 다양성이 미국보다 작을 수 있음 |
| Core importance | > 3.0 | 5점 척도 동일 사용시 그대로 가능 |
| Non-relevant | < 10% | 그대로 가능 |
| DWA 최소 task | 4 | 그대로 가능 |
| DWA 최소 occupation | 3 | **2로 하향 검토**. 한국 중분류당 직업 수가 미국보다 적음 |

## 4.4 사업기간 8개월 내 실행 시나리오

```
[1개월]   참고자료 학습 + 한국 보정 임계 자체 시뮬레이션 + NLP prototype
[2-3개월] 중분류 52개 단위 task 자료 통합 (KECO·NCS 등)
          NLP 자동 1차 분류 → 인간 분석가 검수
          HumRRO 5-step decision tree 구현
[4-5개월] WA Phase A·B 수행: GWA 매핑 → 클러스터 → DWA 작성
          NLP 보조 + 인간 검수 round-robin
[6개월]   WA Phase C·D: DWA Refinement, IWA 도출
          시뮬레이션 검증 (제안서 4번째 영역)
[7개월]   전문가 검토·조정, ID 체계 부여
[8개월]   최종 보고서, 시범 직업군 직무기술 정의서 작성
```

---

# Part V. 발표 Q&A 대비 — 두 보고서에서 도출되는 핵심 방어 카드

## 5.1 "왜 정성+정량 결합인가? 정량(NLP)만으로 안 되는가?"

**답변 카드**:
> WA 보고서는 2014년에 정량 접근(NLP·군집분석)을 명시적으로 거부했습니다. 이유는 "task 진술의 구조적 변동성"이었습니다. 그러나 2014년은 BERT 이전, LLM 미존재 시대였습니다. 2026년 현재 LLM은 verb-object 분리, 다활동 분해, 의미적 군집을 인간 수준으로 수행 가능합니다.
>
> 그럼에도 우리가 정량+정성 결합을 채택한 이유는, WA 보고서가 강조한 5대 클러스터 품질 기준(Homogeneity, Fit, Uniqueness, Specificity, Size) 중 **Specificity와 Uniqueness 판정은 여전히 인간의 도메인 지식이 필수**이기 때문입니다. NLP는 1차 분류의 70–80%까지는 자동화하나, 최종 의미 판정은 인간이 수행해야 신뢰성이 확보됩니다.

## 5.2 "65,000천원·8개월·6명으로 미국 사업과 비교 가능한가?"

**답변 카드**:
> 미국 WA 프로젝트는 추정 약 168 person-month, 한국은 48 person-month로 약 30% 자원입니다. 단 이는 절대치 비교이고, 본 사업은 다음 3가지 효율 레버를 활용합니다.
>
> 1. **NLP 자동화**: HumRRO Decision Tree의 task 판정·중복 판정은 LLM이 90%+ 정확도로 자동화 가능. 이는 미국 사례 대비 분석시간 70% 절감.
> 2. **선택적 시뮬레이션**: 본 사업은 일부 직업군만 시뮬레이션 적용으로 명시되어 있어, 전체 1만 task를 한 번에 처리할 필요가 없음.
> 3. **참조 활용**: O\*NET 41 GWA, 332 IWA, 2,069 DWA 자체를 출발점으로 활용. 미국이 11년에 거쳐 한 일을 다시 하지 않음.

## 5.3 "임계값(67%, 3.0, 4 task/3 occ)을 그대로 차용하는가?"

**답변 카드**:
> 미국 임계는 미국 데이터 기반의 통계적 시뮬레이션 결과이므로 그대로 차용은 부적절합니다. 본 사업 1개월차에 한국 K-NCS·KECO 데이터로 SEM 시뮬레이션을 수행하여 한국 보정 임계를 도출할 계획입니다. 단, **분류 임계의 구조(2-tier, 3-tier 등)와 척도(5점·7점)는 동일하게 유지**하여 국제 비교가능성을 확보합니다.

## 5.4 "Single-DWA IWA를 어떻게 다룰 것인가?"

**답변 카드**:
> WA 보고서가 제시한 3가지 선택지(unassigned 허용/잔여 IWA/single-DWA IWA) 중 본 사업은 **single-DWA IWA를 placeholder 라벨과 함께 채택**합니다. 이는 SOC·NAICS의 표준 데이터모델 관행에 부합하며, 향후 신규 task 추가 시 conventional IWA로 자연스럽게 진화할 수 있는 구조입니다. "기타 ~"식 잔여 카테고리는 분류 완전성에 대한 오해를 유발하므로 회피합니다.

## 5.5 "Cohen's Kappa는 어느 수준을 목표로 하는가?"

**답변 카드**:
> HumRRO는 분석가 간 Kappa 0.88(almost perfect)을 달성했습니다. 본 사업은 이를 벤치마크로 삼되, 동일 수준 도달을 위해 다음 조치를 취합니다.
>
> 1. 분석가 훈련 단계에서 **2–3개 직업을 paired 분석** (HumRRO 권고).
> 2. 매 20개 직업마다 2명이 동일 직업을 평정하여 **periodic interrater agreement 모니터링** (HumRRO 권고).
> 3. 불일치 사례를 학습 데이터로 NLP 재훈련 → 자동분류 정확도 동시 향상.

---

# Part VI. 부록 — 핵심 인용 및 수치 모음

## A. WA 보고서 핵심 수치 (검증된 값)

| 항목 | 값 |
|------|---|
| 입력 task 수 | 19,450 |
| 입력 occupation 수 | 974 |
| 신규 DWA | 2,069 (legacy 2,164 대체) |
| 신규 IWA | 332 (전면 신규) |
| 기존 GWA | 41 (변경 없음) |
| Task–DWA 연결 총수 | 22,714 |
| 1차 연결 | 18,291 (81%) |
| 2차 연결 | 3,851 (17%) |
| 3차 연결 | 572 (2.5%) |
| 미할당 task | 1,159 (6%) |
| Task per DWA (avg) | 10.98 |
| Occupation per DWA (avg) | 8.29 |
| Task per IWA (avg) | 66.36 |
| DWA per IWA (avg) | 6.23 |
| Median job families per IWA | 3 |
| Single-family IWA | 53 / 332 |
| Cross-family IWA (≥10 families) | 15 / 332 |
| DWA 가독성 | 평균 8학년 (SMOG) |
| Job Family 수 | 22 |
| Legacy DWA 통합 결과 | 561 후보 → 51 → 10 채택 |

## B. HumRRO 보고서 핵심 수치 (검증된 값)

| 항목 | 값 |
|------|---|
| Pretest 직업 수 | 8 (current task 분석용) |
| 추가 직업 수 | 8 (write-in 분석용) |
| 총 분석 직업 | 16 |
| Current task 진술 수 | 87 |
| Write-in 진술 수 | 1,088 |
| Write-in 응답자 수 | 411 (평균 2.65 진술/명) |
| 최소 응답자 기준 (재) | 15 |
| Core 기준 (최종) | Relevance > 67% AND Importance > 3.0 |
| Non-relevant 기준 | Relevance < 10% |
| Write-in 중 task 비율 | 712 / 1,088 = 65.4% |
| Non-task 내부분포 | 39% incomprehensible / 27% too broad / 18% KSAO / 14% GWA / 2% misc |
| Task 중 unique | 56% |
| Task 중 partial redundant | 25% |
| Task 중 complete redundant | 19% |
| 최종 emerging task 수 | 17 / 1,088 = 1.6% |
| 분석가 일치도 (Agreement) | 96% (4개 판정 평균) |
| 분석가 일치도 (Cohen's κ) | 0.88 |
| 직업당 분석시간 (1명) | 평균 4시간 (range 2–12시간) |
| Importance–Frequency 상관 (직업별 평균) | r = 0.53 |
| Task 수–평정 평균 상관 | r = -0.64 |

## C. 핵심 인용 (영문 원문)

> "task statement structure is so variable that it would be very difficult for a technical system to reliably derive the most important data from tasks. In short, human judgment was determined to be paramount." — WA 보고서 p.13
>
> "It is unlikely that importance ratings will be a useful criterion, as the vast majority of incumbents indicated that their write-in statements were important to the occupation." — HumRRO p.14
>
> "the fewer the tasks included in an occupation, the higher the relevance, importance, and frequency ratings of those tasks. (-.64 for importance ratings)" — HumRRO p.3
>
> "DWAs serve as a useful starting point for many workforce decisions. The broader IWAs provide an extension of this information, linking occupations across job families." — WA 보고서 p.10
>
> "If the new DWAs meet these criteria, the project team searches for an IWA to which to link the DWA. If no IWA encompasses the activity theme in the DWA, the DWA will be evaluated to determine if it is acceptable as a single-DWA IWA." — WA 보고서 p.40

---

# 결론 및 다음 단계

두 보고서는 **상보적**이다. HumRRO는 **입력 데이터의 품질 게이트키핑**을 정의하고, WA는 **귀납적 추상화를 통한 위계적 추출**을 정의한다. 우리 연구는 이 종단 파이프라인을 한국에 이식하면서 **NLP를 통한 작업 효율화**라는 한 층을 더한다.

발표 준비 측면에서 **세 가지가 가장 중요**하다.

1. **방법론적 권위**: 두 보고서의 정량 수치(특히 Kappa 0.88, 직업당 4시간, DWA 4 task 기준)를 발표 내내 인용하여 우리 절차가 자의적 설계가 아니라 **정립된 국제 사례의 한국 보정**임을 강조.

2. **NLP 정당화의 시점성**: WA 보고서가 NLP를 거부한 것은 2014년의 기술 한계 때문이었다는 점을 명시. 2026년 LLM은 그 한계를 해소했으며, 우리는 **방법론을 갱신하는 것이 아니라 같은 목적을 더 효율적으로 달성**한다는 메시지.

3. **자원 비교의 정량화**: 168 vs 48 person-month라는 구체 수치로 효율 압박을 인정하면서도, NLP·선택적 시뮬레이션·참조 활용이라는 3대 효율 레버로 그 격차를 메운다는 시나리오 제시.

다음 단계는 (1) 한국 K-NCS·KECO 데이터로 자체 SEM 시뮬레이션 1회 수행 (2) 100개 한국 task에 LLM zero-shot 분류를 적용한 prototype 결과 1건 확보 (3) 이 두 자료를 발표 백업 슬라이드로 준비하는 것이다.
