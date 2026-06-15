# [심층분석 02] O*NET Work Activities Project Technical Report — DWA·IWA 개발 방법론

## 1. 자료 메타정보

| 항목 | 내용 |
|---|---|
| 원제 | O\*NET Work Activities Project Technical Report |
| 발간 | National Center for O\*NET Development (2018), 미국 노동부 위탁 |
| 분량 | 영문 본문 + 부록(GWA·DWA 전체 목록 포함), 한글본 약 10,307행 |
| 위상 | O\*NET 18.0 데이터의 19,450개 Tasks를 군집화하여 **2,069개 DWA + 332개 IWA**를 새로 도출한 가장 최근의 표준 방법론 보고서 |
| 본 연구에서의 위치 | **NLP 4단계 파이프라인의 직접적 검증 기준** — 본 연구가 도출할 한국형 직무활동 계층의 채택·품질 임계치를 모두 이 보고서에서 차용 |

## 2. 핵심 메시지 5줄 요약

1. O\*NET 18.0의 **19,450개 Tasks를 정성 분석·군집화**하여 직업 간 공유 가능한 **2,069개 DWA**를 신규 도출했다.
2. DWA를 다시 군집화하여 GWA 41개와 Task 사이의 중간 추상도인 **332개 IWA**를 새로 만들었다 — 결과적으로 **GWA(41) → IWA(332) → DWA(2,069) → Task(19,450)** 의 4계층 구조가 완성되었다.
3. DWA는 **다중연결(multi-link)** 가능 — 하나의 DWA가 여러 직업·여러 산업에 걸쳐 사용되며, 이는 **직업 간 전환 가능성** 분석의 기초 데이터가 된다.
4. 군집화는 1차 직무군(Job Family) 분류 → 2차 GWA 할당 → 3차 GWA 내 군집화의 **3단계 절차**로 수행되었으며, 모든 단계에서 **2인 이상 평가자 합의**를 요구했다.
5. DWA 채택 임계치는 **"최소 4개 작업 또는 3개 직업에서 언급"** 이며, 모든 DWA는 GWA에 1:1 또는 1:N으로 매핑된다.

## 3. 핵심 개념·구조 정밀 정리

### 3.1 4계층 직무활동 프레임워크 (현행 O*NET)

```
[GWA] 일반 작업 활동 (41~42개)
   ├── "정보 수집" (Getting Information)
   ├── "결정 및 문제 해결" (Making Decisions and Solving Problems)
   └── ...
        │
        ▼
[IWA] 중간 작업 활동 (332개)
   ├── (GWA "정보 수집" 산하)
   │     ├── "고객·승객으로부터 정보 입수"
   │     ├── "장비·구조물·자재 점검"
   │     └── ...
        │
        ▼
[DWA] 세부 작업 활동 (2,069개)
   ├── (IWA "고객·승객으로부터 정보 입수" 산하)
   │     ├── "고객 요구사항 인터뷰" — 회계사·간호사·세무사 등 다중 직업 적용
   │     ├── "민원 청취" — ...
        │
        ▼
[Task] 직업특수 과업 (19,450개, 직업당 평균 23개)
   └── 각 직업에서 SME가 도출한 구체 과업 진술
```

### 3.2 DWA 도출 방법론 — Section III

#### 단계 1: 직무군(Job Family) 분류
- **목적**: 19,450개 Task를 22개 직무군(O\*NET-SOC 기준)으로 1차 정렬 → 군집화 작업의 분량 분산
- **방법**: 각 Task가 속한 직업의 SOC 코드를 기준으로 자동 할당
- **품질관리**: 직무군 간 경계 직업은 별도 분류 검토

#### 단계 2: GWA 할당 (Task Clustering Step 2)
- **목적**: 각 Task에 가장 적합한 GWA(41개) 부여
- **방법**: 평가자 2인이 독립적으로 GWA 할당 → 불일치 시 합의 워크시트(Disagree Worksheet)로 조정
- **품질관리**:
  - 평가자 간 1차 동의율 확보 → 한국형 적용 시 참조 임계치
  - 불일치율이 높은 Task는 별도 검토 풀로 이관

#### 단계 3: GWA 내 군집화 (Within-GWA Clustering)
- **목적**: 동일 GWA 내 Task들을 의미적으로 유사한 군으로 묶기 → DWA 후보 도출
- **방법**:
  - 의미적 유사성 기준 (행동 동사 + 대상 + 맥락)
  - 군집 크기 기준치: 최소 4개 Task 또는 3개 직업에서 언급
- **산출**: 2,164개 DWA 초안 → 검토·통합 후 **2,069개** 최종 확정

#### 단계 4: DWA 진술문 작성 (DWA Statement Writing) — 부록 B

DWA 작성 표준:
- **행동 동사 시작** (예: "Interview", "Analyze", "Coordinate")
- **구체적 대상** 명시 (예: "customers" / "data" / "personnel")
- **맥락 제한 최소화** — DWA는 다수 직업에 걸치는 표현이어야 함
- **전문 용어 회피** — 일반 독자도 이해 가능한 수준
- **GWA 1:N 매핑** — 하나의 DWA가 여러 GWA에 속할 수 있음

### 3.3 IWA 개발 방법론 — Section V

#### IWA의 위치
- DWA(2,069개)와 GWA(41개) 사이의 추상도 — DWA를 GWA로 곧바로 묶기엔 너무 거친 점을 보완
- 평균: 1 GWA 당 8개 IWA, 1 IWA 당 6.2개 DWA

#### 도출 절차
1. **DWA Clustering Step 1: GWA 할당** — 각 DWA를 GWA에 명확히 배치
2. **DWA Clustering Step 2: GWA 내 군집화** — 동일 GWA 내 DWA들을 의미 그룹으로
3. **IWA Statement Writing** — 각 군집을 대표하는 중간 추상도 진술문 작성
4. **Final Content Review and Quality Control** — 부록 C 절차로 최종 검증

### 3.4 DWA 정제 (Section IV) — 다중연결·교차 직무군

#### Cross-Job Family DWAs
- 단일 직무군에 머무르지 않고 **여러 직무군에 걸치는 DWA** 식별
- 예: "Document financial transactions" — Business/Finance 직무군 + Healthcare 직무군 모두에 출현

#### Multiple Linkage Identification (다중연결 식별)
- 동일 DWA가 N개 직업에서 출현하는 빈도 측정
- **활용**: 직업 간 전환 가능성, 평생학습 경로 설계, 인력 재배치 분석
- 본 연구에서는 RFP가 요구하는 "**직업 간 전환 가능성 분석 기초 자료**"로 직결

#### Legacy DWA Integration
- 기존 DWA 데이터와의 호환 보장 → 본 연구도 KSCO 7차 → 8차 매핑 시 동일 원리 적용

### 3.5 GWA 41개 (부록 A 발췌) — 4대 범주

| 범주 | GWA 예시 | 본 연구 매핑 |
|---|---|---|
| **A. 정보 입력 (Information Input)** | Getting Information / Identifying Objects, Actions, and Events / Monitoring Processes, Materials, or Surroundings / Inspecting Equipment, Structures, or Material | 한국형 GWA 1차안의 정보 처리 영역 |
| **B. 정신적 과정 (Mental Processes)** | Judging the Qualities of Things / Processing Information / Analyzing Data / Making Decisions and Solving Problems / Thinking Creatively / Updating and Using Relevant Knowledge / Developing Objectives and Strategies / Scheduling Work and Activities / Organizing, Planning, and Prioritizing Work | 한국형 GWA 1차안의 분석·의사결정 영역 |
| **C. 업무 산출 (Work Output)** | Performing General Physical Activities / Handling and Moving Objects / Controlling Machines and Processes / Operating Vehicles, Mechanized Devices, or Equipment / Interacting with Computers / Drafting, Laying Out, and Specifying Technical Devices / Documenting/Recording Information | 한국형 GWA 1차안의 실행·생산 영역 |
| **D. 타인과의 상호작용 (Interacting with Others)** | Communicating / Establishing and Maintaining Relationships / Coordinating Work / Developing and Building Teams / Coaching and Developing Others / Resolving Conflicts and Negotiating / Performing for or Working Directly with the Public / Selling or Influencing | 한국형 GWA 1차안의 대인서비스 영역 |

## 4. 본 연구에의 적용 매핑

### 4.1 NLP 4단계 파이프라인 ↔ DWA 방법론 1:1 대응

| 본 연구 NLP 단계 | O*NET DWA 단계 | 산출물 |
|---|---|---|
| ① 텍스트 수집·정제 | (KSCO 426 + 한국직업사전 6,000 + NCS 능력단위 통합) | 정제된 직업 설명 코퍼스 |
| ② NLP 구문·의미 분석 | Task Clustering Step 1: 직무군 분류 | KSCO 중분류 35개 단위로 정렬 |
| ③ 행동 중심 동사 추출 | Task Clustering Step 2: GWA 할당 | 한국형 GWA 후보군 도출 |
| ④ 의미적 군집화 | Task Clustering Step 3: Within-GWA Clustering + DWA Writing | 한국형 DWA 초안 + 진술문 |
| (시뮬레이션 ④단계) | DWA Refinement: Multiple Linkage Identification | 한국형 다중연결 DWA 목록 |

### 4.2 한국형 임계치 설정 (DWA 채택 기준)

| 기준 | O*NET (미국) | 본 연구 한국형 (안) | 근거 |
|---|---|---|---|
| 최소 작업 수 | 4개 이상 | **3개 이상** | 한국 데이터 규모(KSCO 426 + 한국직업사전 6,000)가 미국(19,450)보다 작음 |
| 최소 직업 수 | 3개 이상 | **2개 이상** | 同 |
| 평가자 합의 | 2인 독립 + 합의 | 2인 독립 + 전문가 1인 조정 | 한국형 검토 패널 5인의 일부 활용 |
| GWA 매핑 | 1:N 허용 | 1:N 허용 | 동일 |

### 4.3 산출물 형식 (DWA Writing Standards 한국화)

본 연구 한국형 DWA 작성 규칙:
1. **행동 동사 시작** — "수집", "분석", "조정", "지도" 등 (Sino-Korean 동사 우선)
2. **구체적 대상** — "고객", "데이터", "장비", "팀원" 등
3. **맥락 제한 최소화** — 산업·직업 특수성 배제
4. **전문 용어 회피** — KSCO 6학년 가독성 수준
5. **GWA 매핑 명시** — 작성 시 어느 GWA에 속하는지 함께 기록

## 5. 착수보고서 인용 가능 표현

> 본 연구의 직무활동 추출 방법론은 **NCO-NET(2018)이 O\*NET 18.0의 19,450개 Task를 군집화하여 2,069개 DWA를 도출한 절차**를 한국 맥락에 맞게 재현한 것이다. 본 연구는 이 절차를 NLP 자동화로 가속하되, **모든 군집화 결과는 전문가 2인 독립 평가 + 1인 조정**의 합의 절차를 거쳐 확정한다.

> 한국형 DWA 채택 임계치는 한국 데이터 규모를 고려하여 "**최소 3개 작업 또는 2개 직업에서 언급**"으로 설정한다 (O\*NET 미국 기준 "4개 작업 또는 3개 직업"의 한국화 조정).

> DWA의 **다중연결(multi-link)** 식별은 RFP 요구사항인 *직업 간 전환 가능성 분석 기초 자료*를 직접 충족하며, 본 연구의 시뮬레이션 ④단계 변별력 검토에 핵심 지표로 활용된다.

## 6. 한계·주의점

| 항목 | 내용 | 본 연구 대응 |
|---|---|---|
| **18.0 데이터 기준** | 2018년 데이터로, 그 이후 신생 직업(생성형 AI·플랫폼 등) 미반영 | KECO 2025 신설 직업의 별도 보강 |
| **영문 의미 군집화** | 영어 동사·표현 기반 군집 → 한국어 NLP에서는 다른 패턴 가능 | 한국어 형태소 분석기(Mecab/Khaiii) + 의미 임베딩 병행 |
| **재직자 응답 → Task** | 미국 Task 자체가 재직자 응답에서 도출 → KSCO 텍스트는 행정·전문가 작성이라 성격 차이 | 한국직업사전·NCS·KNOW 등 다출처 텍스트 통합으로 응답자 다양성 확보 |
| **전문가 합의 비용** | 모든 단계에 2인 평가자 → 인건비 부담 | NLP 1차 → 의견 일치 항목은 자동 채택 / 불일치 항목만 전문가 검토 (효율 모드) |

## 7. 추가 인용·심화 검토 권고

- **부록 A (GWA 41 전체 목록)** — 본 연구 한국형 GWA 1차안 작성 시 직접 비교 대상
- **부록 B (DWA·IWA Writing Standards)** — 본 연구 작성 가이드라인의 모태
- **부록 C (Content Review and Quality Control Process)** — 본 연구 품질관리 절차의 모태
- **부록 H, I (GWA 31 "갈등 해결" 데이터 하위 집합 예시)** — 시뮬레이션 단계 예시 분석에 활용
- **Section VIII (Application of Revised DWA Data)** — 정책 활용 사례, 본 연구 정책활용 방안 작성 시 참조
