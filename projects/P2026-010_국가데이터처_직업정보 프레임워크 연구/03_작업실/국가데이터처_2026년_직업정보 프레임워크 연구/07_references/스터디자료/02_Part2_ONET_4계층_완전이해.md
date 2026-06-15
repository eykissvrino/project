# Part 2. O*NET 4계층 활동 체계 완전 이해 — GWA · IWA · DWA · TASK

## 학습 목표

1. O*NET 4계층(GWA—IWA—DWA—TASK)의 정의·규모·예시를 회상할 수 있다.
2. 각 층의 **추상도와 작성 규칙**을 구분하고, 어느 층에 속하는 진술인지 판별할 수 있다.
3. 4계층의 **수직 위계 관계**(parent–child)와 **수평 다중연결**(multi-link)을 설명할 수 있다.
4. ID 체계와 데이터 모델을 이해하여 향후 한국형 ID 체계 설계의 근거로 사용할 수 있다.

---

## 2.1 4계층 체계 한눈에 보기

O*NET 30.x(2026.2) 기준의 4계층 활동 체계는 다음과 같습니다.

```
                                                    [규모]      [추상도]      [공유 범위]
┌──────────────────────────────────────────┐
│  GWA  Generalized Work Activities          │  41~42개   가장 일반    전 직업
│  일반화 작업 활동                            │
│  예: "Getting Information" (정보 수집)      │
└────────────────┬─────────────────────────┘
                 │ 1:N (한 GWA에 여러 IWA)
                 ▼
┌──────────────────────────────────────────┐
│  IWA  Intermediate Work Activities         │  332개    중간 추상     여러 직무군
│  중간 작업 활동                              │
│  예: "Examine medical instruments..."      │
└────────────────┬─────────────────────────┘
                 │ 1:N (한 IWA에 여러 DWA)
                 ▼
┌──────────────────────────────────────────┐
│  DWA  Detailed Work Activities             │  2,087개  구체적         같은 직무군 내 다수 직업
│  세부 작업 활동                              │
│  예: "Test patient vision"                  │
└────────────────┬─────────────────────────┘
                 │ N:M (한 TASK가 최대 3개 DWA에 다중연결)
                 ▼
┌──────────────────────────────────────────┐
│  TASK Occupation-specific Tasks            │  19,000~ 가장 구체     1개 직업 전용
│  직업특수 과업                                │
│  예: "Administer the Snellen eye chart..."  │
└──────────────────────────────────────────┘
```

> **수치 출처**: GWA 41개·IWA 332개·DWA 2,069개는 WA Project 2014년 기준이며, 2026년 O*NET 30.x 기준으로 DWA는 2,087개로 미세 증가했습니다. 평균 직업당 17개 DWA가 연결되어 있습니다.

---

## 2.2 GWA — 일반화 작업 활동 (Generalized Work Activities)

### 정의

**모든 직업에 공통으로 적용 가능한 가장 일반적 수준의 활동**. O*NET 콘텐츠 모델의 "직업요구(Occupational Requirements)" 영역에 속하며, 본래 의도는 직업 간 비교를 가능하게 하는 **공통 좌표**입니다.

### 규모와 안정성

- 41~42개 (WA Project에서 41개 유지, 일부 문헌은 42개)
- O*NET 초기(1995)부터 거의 동일하게 유지 — **변경이 가장 드문 층**
- ID 형식: `4.A.1.b.2` 등 (콘텐츠 모델 ID 체계)

### 4대 범주

41개 GWA는 4개 대범주로 묶입니다.

| 범주 | GWA 예시 | 핵심 동사 |
|------|---------|----------|
| **A. 정보 입력 (Information Input)** | Getting Information / Identifying Objects, Actions, and Events / Monitoring Processes, Materials, or Surroundings / Inspecting Equipment, Structures, or Material | 수집·확인·관찰·점검 |
| **B. 정신적 과정 (Mental Processes)** | Judging the Qualities of Things / Processing Information / Analyzing Data or Information / Making Decisions and Solving Problems / Thinking Creatively / Updating and Using Relevant Knowledge / Developing Objectives and Strategies / Scheduling Work and Activities / Organizing, Planning, and Prioritizing Work | 판단·처리·분석·결정·계획 |
| **C. 업무 산출 (Work Output)** | Performing General Physical Activities / Handling and Moving Objects / Controlling Machines and Processes / Operating Vehicles, Mechanized Devices, or Equipment / Interacting with Computers / Drafting, Laying Out, and Specifying Technical Devices / Documenting/Recording Information | 수행·조작·운영·기록 |
| **D. 타인과의 상호작용 (Interacting with Others)** | Communicating / Establishing and Maintaining Relationships / Coordinating Work / Developing and Building Teams / Coaching and Developing Others / Resolving Conflicts and Negotiating / Performing for or Working Directly with the Public / Selling or Influencing | 소통·조정·지도·협상·판매 |

### GWA의 특성

- **국가·문화 의존도가 매우 낮음**: GWA는 보편적이라서 미국·한국·유럽 어디서나 거의 동일하게 사용 가능
- **AI 자동화 가능성 분석의 시작점**: 예를 들어 "Interacting with Computers"는 자동화 가능, "Resolving Conflicts"는 자동화 어려움 등 GWA 단위 분석이 가능
- **본 연구의 한국 적용 전략**: GWA 41개는 그대로 한글 번역하여 차용하는 것이 합리적. 8개월 사업기간 안에 자체 개발하는 것은 비효율

---

## 2.3 IWA — 중간 작업 활동 (Intermediate Work Activities)

### 정의와 도입 배경

**GWA와 DWA 사이의 중간 추상도**. 2014년 WA Project에서 신규 도입되었으며, 이전 O*NET에는 없었던 층입니다. 도입 이유는 다음과 같습니다.

- DWA(2,000여 개)를 GWA(41개)에 직접 매핑하면 1:50의 부담스러운 비율
- 분석가가 한 번에 50개 DWA를 다루기 어려우며, **인지 부하 관리** 차원에서 중간 층 필요
- 또한 "여러 직무군에 걸치는 활동"을 식별하기 위한 **수평 통합 단위**가 필요

### 규모와 분포

- 332개
- 평균 1 GWA당 8개 IWA
- 평균 1 IWA당 6.2개 DWA
- 평균 1 IWA당 66.4개 task (직업 간)
- Median job families per IWA: 3 (즉 IWA 1개가 평균 3개 직무군에 걸침)
- Single-family IWA: 53/332 (16%) — 1개 직무군에만 속함
- Cross-family IWA(≥10 families): 15/332 (4.5%) — 매우 일반적

### 예시 (GWA "Inspecting Equipment, Structures, or Material" 산하)

```
GWA: Inspecting Equipment, Structures, or Material
├── IWA: Administer diagnostic tests to assess patient health
│   ├── DWA: Test patient vision
│   ├── DWA: Test patient hearing
│   └── DWA: Assess physical condition of patients...
├── IWA: Inspect mechanical or electrical equipment
│   ├── DWA: Inspect motor vehicles
│   └── DWA: ...
└── ...
```

### Single-DWA IWA 문제

WA Project가 가장 고민한 부분 중 하나입니다. 어떤 IWA는 **자식 DWA가 1개뿐**입니다 (예: "Train animals"라는 DWA 하나만 갖는 IWA). 이를 어떻게 처리할 것인가?

**선택지**:
1. 부모 없는 DWA 허용 → 데이터 무결성 위반
2. "All Other ..." 잔여 IWA 도입 → SOC 방식. 하지만 IWA가 완전 분류로 오해될 위험
3. **단일 DWA IWA 허용 (선택안)** → DWA = IWA의 1:1 관계 허용

WA Project는 3안을 채택했습니다. 이유는 SOC·NAICS·O*NET Content Model의 모든 위계 분류에서 child가 immediate parent를 가지도록 설계되어 있는 표준 관행을 따른 것입니다.

> **한국 적용 시 함의**: 한국에서도 single-DWA IWA가 발생하면 1:1 관계로 허용하되, "임시(placeholder)" 라벨을 명시적으로 부여하여 추후 신규 DWA 발견 시 자연스럽게 conventional IWA로 진화하도록 설계해야 합니다.

---

## 2.4 DWA — 세부 작업 활동 (Detailed Work Activities)

### 정의

**같은 직무군(Job Family) 안의 다수 직업에서 공유되는 구체적 작업 활동**. 본 연구의 산출물 중 가장 핵심이며, 양도 가장 큽니다.

### 규모와 분포 (O*NET 30.x 기준)

- 2,087개 DWA
- 평균 1 DWA당 task 약 11개
- 평균 1 DWA당 occupation 약 8.3개
- 평균 1 직업당 17개 DWA

### 5대 클러스터 품질 기준

DWA가 "좋은" DWA로 인정받기 위한 5개 기준입니다. 이 기준은 본 연구의 한국 DWA 도출에도 그대로 차용됩니다.

| 기준 | 정의 | 위반 시 문제 |
|------|------|-----------|
| **Cluster Homogeneity (동질성)** | 동일 활동 테마를 강하게 공유 | 다른 활동이 섞이면 의미가 흐려짐 |
| **Task-Cluster Fit (적합성)** | 개별 task가 클러스터 테마에 잘 맞음 | outlier task가 있으면 DWA 정의가 부정확해짐 |
| **Cluster Uniqueness (유일성)** | job family 내 다른 클러스터와 개념적으로 구별 | 중복 DWA는 분류 효율을 떨어뜨림 |
| **Cluster Specificity (구체성)** | task보다 일반적, GWA보다 구체적 | 너무 일반적이면 IWA·GWA와 구분 안 됨 |
| **Cluster Size (규모)** | 최소 2 task, 목표 **4 task & 3 occupations** | 너무 작으면 cross-occupational linking 효과 없음 |

### DWA 작성 8대 규칙 (Writing Standards)

| # | 규칙 | 예시 |
|---|------|------|
| 1 | DWA당 주요 활동동사 1개, 동사로 시작 | "Inspect..." ✓ / "The inspection of..." ✗ |
| 2 | 동사형식: 3인칭·현재·복수 | "Inspect" ✓ / "Inspects" "Inspecting" ✗ |
| 3 | 명사 최소화, but 구체성 유지 | "or" 사용 (multiple objects) |
| 4 | 직무군에 적합한 명사 사용 | "equipment"는 너무 넓음 / "laser surgery robots"는 너무 좁음 / **"medical treatment equipment"** ✓ |
| 5 | 명료성을 위해 형용사 사용 | |
| 6 | 예시절 회피 ("such as", "including") | 꼭 필요할 때만 |
| 7 | 목적절("to ...") 최소 사용 | 단, 활동이 동일해도 목적이 다르면 KSAO가 다를 수 있어 의미 있음 |
| 8 | 8학년 가독성 (SMOG index) | 3음절 이상 단어 수로 측정 |

### 모호 동사 회피

WA Project가 강조한 핵심 작성 원칙입니다.

| 모호 동사 | 명확한 대체 |
|---------|------------|
| use a computer | **operate** computers / **interact with** computers |
| follow procedures | **adhere to** standardized procedures |
| handle data | **analyze** data / **investigate** data |
| work with people | **coordinate** with staff / **counsel** clients |

> **한국 적용 시**: "사용한다"·"수행한다"·"활용한다" 같은 한국어 모호 동사도 회피하고, "조작한다"·"점검한다"·"측정한다"·"조정한다" 등 구체동사를 강제해야 합니다.

### 4 task / 3 occupations 목표 비율의 근거

DWA의 최소 크기가 "4 task / 3 occupations"인 이유:

1. **Cross-occupational linking**: DWA의 본질적 목적은 직업 간 연결. 1~2개 직업만 연결하면 의미가 없음.
2. **장기 안정성**: O*NET는 task가 정기적으로 add/revise/remove됨. 여유 task가 있어야 1개 task가 사라져도 DWA가 살아남음.

---

## 2.5 TASK — 직업특수 과업

### 정의

**특정 직업에서 수행되는 구체적 진술**. 다른 모든 층의 기초가 되는 가장 낮은 추상도 단위입니다. 직업당 평균 20여 개 task가 정의됩니다.

### 규모와 출처

- O*NET 18.0 기준 19,450개
- O*NET 30.x 기준 약 19,000~21,000개 (지속적 갱신)
- 출처: **재직자(incumbent) 응답** + **직업 전문가(SME) 검토**

### TASK 진술의 구조

표준적 task 진술은 다음 요소를 포함합니다.

```
[Verb]   [Object]              [Purpose/Tool/Context]
 동사      목적어                  목적/도구/맥락
 │          │                       │
 ▼          ▼                       ▼
"Measure, cut and install tackless strips along the baseboard or wall"
 ↑복합동사    ↑복합 목적어              ↑맥락절
```

이 task는 **단일 진술이지만 3개 활동을 포함**합니다. 따라서 DWA 매핑 시 다음 3개에 다중연결됩니다.

- DWA 1: Measurement
- DWA 2: Cutting materials
- DWA 3: Material installation

### TASK의 품질 분류 (HumRRO 기준)

본 연구의 한국 TASK 풀에도 이 분류가 적용됩니다.

| 카테고리 | Relevance | Importance | 비고 |
|---------|-----------|-----------|------|
| **Core Tasks** | > 67% | > 3.0 | 직업의 핵심 task |
| **Supplementary Tasks** (Type A) | > 67% | < 3.0 | 보편적이지만 덜 중요 |
| **Supplementary Tasks** (Type B) | 10–66% | (무관) | 일부 incumbent에게만 해당 |
| **Non-relevant Tasks** | < 10% | (무관) | 폐기 |

---

## 2.6 4계층의 수직·수평 관계

### 수직 위계 (Parent–Child)

```
GWA  ──(1:N)──▶  IWA  ──(1:N)──▶  DWA  ──(N:M)──▶  TASK
```

- GWA → IWA: 1:N (한 GWA가 여러 IWA를 가짐)
- IWA → DWA: 1:N (한 IWA가 여러 DWA를 가짐, 단 single-DWA IWA 허용)
- DWA → TASK: **N:M** (한 DWA가 여러 task와 연결, **한 task도 최대 3개 DWA에 다중연결**)

### Task → DWA 다중연결의 정량 (WA Project)

| 연결 유형 | 수 | 비율 |
|---------|---|------|
| 1차 연결 (primary activity) | 18,291 | 81% |
| 2차 연결 | 3,851 | 17% |
| 3차 연결 | 572 | 2.5% |
| **총 연결** | **22,714** | **100%** |

즉 task의 평균 약 1.24개 DWA에 연결됩니다. 다중연결은 직업 간 전환 분석의 풍부도를 결정짓는 핵심 데이터입니다.

### 수평 다중연결 (Multi-link)

수직 위계 외에 가장 중요한 데이터 특성입니다. **동일한 GWA·IWA·DWA가 여러 직업에서 사용**된다는 점입니다.

예시:
- DWA "Inspect mechanical equipment" → 자동차정비사, 항공정비사, 산업기계정비사 모두에 적용
- 이 다중연결을 이용해 "정비사 직군 내 직업 전환 가능성"을 분석 가능

이것이 본 연구가 RFP에서 요구하는 "직업 간 전환 가능성 분석 기초 자료"를 직접 충족하는 데이터 구조입니다.

---

## 2.7 ID 체계

O*NET의 4계층은 다음과 같은 ID 체계로 표현됩니다.

```
GWA ID:   4.A.1.b.2                       (Inspecting Equipment, Structures, or Material)
IWA ID:   4.A.1.b.2.I01                   (Administer diagnostic tests to assess patient health)
DWA ID:   4.A.1.b.2.I01.D03               (Test patient vision)
```

| 구성 | 의미 |
|------|------|
| `4.A.1.b.2` | GWA 9-character 콘텐츠 모델 ID |
| `.I01` | IWA 번호 (2-digit) |
| `.D03` | DWA 번호 (2-digit) |

### 핵심 설계 원칙

**IWA·DWA의 번호는 무작위(random) 부여** — 의미적 순서를 넣지 않습니다. 이유는 미래 신규 IWA·DWA 추가 시 번호 재배치가 불필요하기 때문입니다.

> **한국 적용 시**: KSCO 코드는 의미적 순서가 강해서 신규 직업 추가가 어렵습니다. 한국형 GWA·IWA·DWA ID는 O*NET 방식을 따라 무의미 무작위 번호를 권장합니다.

---

## 2.8 4계층의 데이터 모델

```
┌─────────────────────────────────────────────┐
│  GWA (id PK, label, category, definition)   │
└──────────────┬──────────────────────────────┘
               │ 1
               │
               │ N
┌──────────────▼──────────────────────────────┐
│  IWA (id PK, gwa_id FK, label, definition)  │
└──────────────┬──────────────────────────────┘
               │ 1
               │
               │ N (single-DWA IWA → N=1 허용)
┌──────────────▼──────────────────────────────┐
│  DWA (id PK, iwa_id FK, label, definition)  │
└──────────────┬──────────────────────────────┘
               │ 1
               │
               │ N
┌──────────────▼──────────────────────────────┐
│  DWA_TASK_LINK (dwa_id FK, task_id FK,      │
│                 link_order INT)              │  ← N:M
└──────────────┬──────────────────────────────┘
               │ M
               │
               │ 1
┌──────────────▼──────────────────────────────┐
│  TASK (id PK, occupation_code FK, statement)│
└──────────────┬──────────────────────────────┘
               │ N
               │
               │ 1
┌──────────────▼──────────────────────────────┐
│  OCCUPATION (code PK, ksco_code, label,...) │
└─────────────────────────────────────────────┘
```

### 본 연구의 데이터 모델 권고

본 연구가 한국형 4계층을 구현할 때, **이 데이터 모델을 그대로 차용**할 것을 권장합니다. 추가로 다음을 보강합니다.

- **TASK 메타데이터**: relevance, importance, frequency, core/supplementary 라벨
- **DWA_TASK_LINK 메타데이터**: link_order(1·2·3), 평가자 합의 정보
- **버전 관리**: KSCO 7차 → 8차 변경에 따른 task·DWA의 시계열 추적

---

## 2.9 본 Part 요약 카드

- O*NET 4계층: **GWA(41) ← IWA(332) ← DWA(2,087) ← TASK(19,000+)**
- 수직 관계는 1:N·N:M, 수평 다중연결로 직업 간 비교가 가능
- DWA 작성은 **5대 품질 기준 + 8대 작성 규칙**을 따름
- TASK는 N:M으로 최대 3개 DWA에 다중연결됨 (81%/17%/2.5%)
- ID 체계는 무작위 번호 부여를 통해 신규 추가 시 재배치 불필요하게 설계

---

## 2.10 다음 단계

Part 3에서는 미국이 이 4계층을 어떻게 도출했는지 — HumRRO의 TASK 품질관리 절차와 WA Project의 클러스터링·라이팅 절차 — 의 구체적 방법론을 학습합니다.
