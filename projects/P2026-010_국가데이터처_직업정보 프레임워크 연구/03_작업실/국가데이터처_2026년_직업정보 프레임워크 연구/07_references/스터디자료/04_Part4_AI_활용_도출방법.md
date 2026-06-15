# Part 4. AI 기반 도출 방법 — 어떤 AI 기술을 어떻게 활용할 것인가

## 학습 목표

1. 본 연구의 각 단계에서 **AI(LLM/임베딩/클러스터링)가 어디까지 인간을 대체·보조**하는지 매트릭스로 그릴 수 있다.
2. **5대 AI 기술 요소**(LLM zero/few-shot 분류, 임베딩, 클러스터링, 생성, 검증)의 각 역할과 적용 단계를 설명할 수 있다.
3. 모델 선택의 근거(GPT-5/Claude vs 한국어 SBERT vs BGE-m3-ko)를 데이터·과제 특성에 따라 판별할 수 있다.
4. AI 활용에 대한 **품질 검증 프로토콜**(인간-AI 합의도, hallucination 차단 등)을 설계할 수 있다.

---

## 4.1 핵심 메시지

본 연구의 AI 활용은 다음 4가지 원칙을 따릅니다.

1. **AI는 인간 분석가의 대체가 아닌 가속기(accelerator)**. 최종 의미 판정은 인간이 함.
2. **단계별로 다른 기술이 적합**. LLM zero-shot이 적합한 단계, 임베딩 군집화가 적합한 단계, 생성 모델이 적합한 단계가 모두 다름.
3. **저비용·고처리량 모델(임베딩) + 고정밀 모델(LLM)의 조합**. 모든 단계에 LLM을 쓰면 비용·시간 폭증.
4. **인간-AI 합의도(human-AI agreement)를 정량 모니터링**. AI 산출물의 품질을 Kappa·F1으로 측정하며 인간 검수 비율을 동적 조정.

---

## 4.2 단계별 인간 vs AI 분담 매트릭스

본 연구의 13개 핵심 단계에 대해 AI 적합성과 권고 도구를 정리합니다.

| 단계 | 작업 내용 | AI 적합성 | 권고 도구 | 인간 검수율 |
|------|---------|---------|---------|----------|
| 1. KSCO 직업설명 텍스트 정제 | 분류항목표 HWPX 파싱 → 정형 텍스트 | 매우 높음 | 정규식 + LLM 후처리 | 5% |
| 2. 외부 자료 통합 (KNOW·NCS·KECO) | 직업 매핑 및 텍스트 통합 | 높음 | 임베딩 매칭 + LLM 검증 | 10% |
| 3. TASK 후보 추출 | 직업설명에서 동사-목적어 진술 추출 | 매우 높음 | LLM (지시기반 생성) | 20% |
| 4. HumRRO Step 1: task 여부 판정 | 진술이 task/KSAO/GWA 중 무엇? | 매우 높음 | LLM zero-shot 분류 | 5% |
| 5. HumRRO Step 2-3: 중복 판정 | semantic similarity | 매우 높음 | SBERT 임베딩 + cosine | 5% |
| 6. HumRRO 3-tier 분류 (정량 지표 기반) | Relevance·Importance 임계 적용 | 자동 (AI 불필요) | SQL/스프레드시트 | 0% |
| 7. WA Step 1: Job Family 할당 | 직업 → 대분류 매핑 | 이미 완료 | KSCO에 매핑정보 존재 | 0% |
| 8. WA Step 2: GWA 41개 할당 | task → GWA 매핑 | 높음 | LLM few-shot + 인간 합의 검증 | 30% |
| 9. WA Step 3: GWA 내 클러스터링 | 의미 군집 | 중간 | HDBSCAN + LLM 후처리 | 50% |
| 10. WA: DWA Writing | 동사 시작·8학년 가독성 진술문 작성 | 중간 | LLM 초안 → 인간 편집 | 100% |
| 11. WA: Cross-Family 통합 | 알파벳 정렬·유사도 | 매우 높음 | 임베딩 + 자동화 | 10% |
| 12. WA: Multiple Linkage | 다활동 task 분해 | 높음 | LLM (다중 verb 추출) | 30% |
| 13. WA: IWA 작성 | DWA 클러스터링 + writing | 중간 | LLM 초안 + 인간 편집 | 100% |

**인간 전담** (AI 보조 최소): 최종 QC, Single-DWA IWA 처리, 모호 의미 판정.

---

## 4.3 5대 AI 기술 요소

### 4.3.1 LLM zero-shot / few-shot 분류

#### 작동 원리
대형 언어모델(GPT-5, Claude Opus 4.6, Sonnet 4.6 등)에 지시문(prompt)으로 분류 기준을 알려주고, 입력 텍스트를 분류하도록 요청합니다.

- **Zero-shot**: 예시 없이 정의만 제시 → 가장 유연하나 정확도 변동
- **Few-shot**: 정답 예시 3~10개 동봉 → 정확도 상승, 비용 약간 증가
- **Chain-of-thought**: 모델이 단계별 추론을 출력하도록 유도 → 어려운 경계 사례에서 강력

#### 본 연구 적용 단계

**(가) HumRRO Step 1: task 여부 판정**

```
Prompt:
다음 진술은 직업 과업(task), 지식·기술·능력(KSAO), 일반화 직무활동(GWA),
이해불가(incomprehensible), 너무 광범위(too broad) 중 무엇입니까?

진술: "환자의 알레르기 정보를 확인하여 약물 투여 전 의사에게 보고한다"

판정 기준:
- task: 동사+목적어 구조, 직업특수 행동
- KSAO: 개인의 속성·역량 진술
- GWA: 직업 비특수, 매우 일반적
- ...

응답 형식: {"category": "...", "reasoning": "...", "confidence": 0.0~1.0}
```

**(나) WA Step 2: GWA 41개 할당**

```
Prompt:
다음 task가 41개 GWA 중 어디에 속하는지 1차 선택과 2차 선택을 제시하세요.

Task: "환자에게 증상 발현 시점·강도를 인터뷰한다"

GWA 목록:
1. Getting Information — Observing, receiving, and otherwise obtaining information
   from all relevant sources.
2. Monitoring Processes, Materials, or Surroundings — ...
... (41개 모두)

응답 형식: {"primary": "1", "secondary": "5", "reasoning": "..."}
```

#### 모델 선택 가이드

| 과제 | 권고 모델 | 이유 |
|------|---------|------|
| 한국어 task 진술 분류 | **Claude Sonnet 4.6** 또는 GPT-5 | 한국어 능력 우수, 8K context로 GWA 41개 동봉 가능 |
| 대량 자동분류 (수만 건) | **Claude Haiku 4.5** 또는 GPT-5 mini | 비용 1/10 수준, 정확도 충분 |
| 경계 사례 검토 (수백 건) | **Claude Opus 4.6** | 최고 정확도, 비용 감수 |

#### 검증 방법

LLM zero-shot의 정확도는 **인간-AI Kappa**로 측정합니다.
- 표본 100~200건을 인간 2명이 독립 라벨링
- LLM 라벨과 인간 합의 라벨의 Cohen's Kappa 계산
- Kappa 0.7 이상이면 자동분류 채택, 0.5~0.7이면 인간 검수 50%, 0.5 미만이면 prompt 개선

### 4.3.2 임베딩 (Embedding)

#### 작동 원리
텍스트를 고차원 벡터로 변환하여, 의미적으로 유사한 텍스트가 벡터공간에서 가까워지도록 합니다.

- **목적**: 유사도 계산, 군집화, 검색
- **차원**: 보통 384·768·1024·1536 (모델에 따라)
- **모델**: Sentence-BERT, OpenAI text-embedding-3-large, BGE-m3, KR-SBERT 등

#### 본 연구 적용 단계

**(가) HumRRO Step 2-3: 중복 판정**

```
새 task: "환자의 알레르기 정보를 확인하여 약물 투여 전 의사에게 보고한다"
기존 tasks: [...수백 개...]

1. 모든 task를 임베딩으로 변환
2. cosine similarity 계산
3. similarity > 0.90 → 완전 중복
4. similarity 0.75~0.90 → 부분 중복
5. similarity < 0.75 → 신규 후보
```

**(나) Cross-Family DWA 통합**

```
DWA "Inspect medical equipment" (Healthcare family) — vec_A
DWA "Inspect mechanical equipment" (Production family) — vec_B
cosine(vec_A, vec_B) = 0.87 → 통합 검토 대상으로 flag
```

#### 모델 선택 가이드

| 과제 | 권고 모델 | 이유 |
|------|---------|------|
| 한국어 task 진술 임베딩 | **BGE-m3-ko** (1024차원) | XLM-RoBERTa 기반, 한국어 강력, 8192 토큰 입력 가능 |
| 다국어 (한·영 혼재) | **BGE-M3** 또는 paraphrase-multilingual-MiniLM | 영문 O*NET 자료와 직접 비교 가능 |
| 빠른 처리 (대용량) | **paraphrase-multilingual-MiniLM-L12-v2** | 384차원, 처리 속도 빠름 |
| 최고 품질 (소량 정밀) | **OpenAI text-embedding-3-large** | 3,072차원, 비용 있음 |

#### 검증 방법

임베딩 품질은 **유사도 매칭 정확도**로 측정합니다.
- 인간이 100쌍의 task에 대해 "중복/부분중복/무관" 라벨링
- 임베딩 유사도와 인간 라벨의 상관계수
- 0.7 이상 권장

### 4.3.3 클러스터링 (Clustering)

#### 작동 원리
임베딩 벡터들을 의미적 유사도에 따라 군집으로 묶습니다.

**핵심 알고리즘 비교**:

| 알고리즘 | 특성 | 본 연구 적합도 |
|---------|------|------------|
| K-means | 군집 수 K 사전 지정, 구형 군집 가정 | ✗ (DWA 수를 사전에 모름) |
| **HDBSCAN** | 밀도 기반, 군집 수 자동, 노이즈 분리 | ✓ (강력 권고) |
| Agglomerative (계층적) | 위계 구조, dendrogram 시각화 | ✓ (DWA → IWA → GWA 위계 구축에 적합) |
| **BERTopic** | 임베딩 + UMAP + HDBSCAN + c-TF-IDF | ✓ (군집별 키워드 자동 추출) |

#### 본 연구 적용 — WA Step 3: GWA 내 클러스터링

```
Step 1: GWA 5 ("Inspecting Equipment") 산하 task 1,200개 추출
Step 2: BGE-m3-ko로 임베딩 (1,200 × 1024 행렬)
Step 3: UMAP으로 차원 축소 (1024 → 10차원)
Step 4: HDBSCAN으로 군집화
        - min_cluster_size=4 (DWA 최소 task 수)
        - min_samples=2
Step 5: BERTopic c-TF-IDF로 군집별 키워드 추출
Step 6: 인간 분석가가 군집 검토 → DWA 작성
```

#### 클러스터링 후 후처리

군집 결과는 그 자체로 DWA가 아닙니다. **추가 작업**이 필요합니다.

1. **클러스터 5대 품질 기준 검증**: Homogeneity, Fit, Uniqueness, Specificity, Size
2. **이상치 task 재배치**: outlier task를 다른 군집으로 이동
3. **너무 큰 군집 분할**: task가 30개 넘는 군집은 의미적 하위군집으로 분할
4. **너무 작은 군집 통합**: task 3개 이하 군집은 인접 군집과 통합 검토

### 4.3.4 LLM 생성 (Generation)

#### 작동 원리
LLM에게 짧은 진술문 작성을 요청합니다.

#### 본 연구 적용 단계

**(가) DWA Writing 초안 생성**

```
Prompt:
다음 task 군집의 공통 활동을 나타내는 DWA 진술문을 작성하세요.

군집 내 task:
1. "환자의 증상을 인터뷰하여 차트에 기록한다"
2. "내원 사유와 통증 부위를 문진한다"
3. "환자 가족력을 청취한다"
... (10개)

작성 규칙:
- 동사로 시작, 3인칭·현재·복수
- 명사 최소화, 직무군 적합
- 예시절·목적절 회피
- 8학년 가독성

초안 3개를 작성하고 각 초안의 장단점을 평가하세요.
```

LLM은 다음과 같은 초안을 생성합니다.

```
초안 1: "Interview patients to gather medical history" — 명확, 8학년 적합
초안 2: "Collect patient medical information" — 너무 광범위
초안 3: "Document patient symptoms and history" — 활동 2개 포함

권고: 초안 1
```

인간 분석가는 이 초안을 받아 최종 진술을 확정합니다.

**(나) IWA 진술문 생성**: DWA 군집을 상위 추상도로 추출.

#### 모델 선택 가이드

이 단계는 **창의성과 정확성을 모두 요구**합니다.

| 과제 | 권고 모델 | 이유 |
|------|---------|------|
| 한국어 DWA 초안 | **Claude Opus 4.6** | 한국어 생성 품질 최고, 규칙 준수 우수 |
| 영문 동시 생성 (병행 검증용) | GPT-5 + Claude Opus 4.6 비교 | 다국어 일관성 확보 |
| 대량 초안 (수백 건) | Claude Sonnet 4.6 | 속도·품질 균형 |

#### 검증

LLM이 만든 DWA 진술은 **8대 작성 규칙 자동 검증기**를 거쳐야 합니다.

```python
def validate_dwa(statement):
    rules = {
        "starts_with_verb": starts_with_verb(statement),
        "3rd_person_present_plural": is_3rd_person_present_plural(statement),
        "min_nouns": count_nouns(statement) <= MAX_NOUNS,
        "no_example_clause": "such as" not in statement and "including" not in statement,
        "minimal_purpose_clause": count_purpose_clauses(statement) <= 1,
        "smog_grade": calculate_smog(statement) <= 8,
        # ...
    }
    return rules
```

### 4.3.5 LLM 검증·합의 (Validation & Consensus)

#### 작동 원리
다수의 LLM 또는 LLM과 인간의 라벨을 비교하여 일치도를 측정합니다.

#### 본 연구 적용

**(가) Multi-Model Voting**

```
Task: GWA 할당 (41개 중 선택)
- Claude Opus 4.6 → GWA 5 (Inspecting...)
- GPT-5 → GWA 5 (Inspecting...)
- Gemini → GWA 7 (Monitoring...)

판정: 2/3 다수결로 GWA 5 채택, 단 GPT-5/Gemini 불일치이므로 인간 검수 대상으로 flag
```

**(나) Self-Consistency**

같은 모델에 같은 질문을 5회 묻고, 답의 일관성을 측정.
- 5/5 동일 → 신뢰
- 4/5 → 약한 신뢰
- 3/5 이하 → 인간 검수

**(다) 인간-AI 합의도 모니터링**

매 20개 직업마다 인간 분석가 1명이 LLM 자동 라벨을 검토하여 Cohen's Kappa 계산. Kappa가 0.7 이하로 떨어지면 prompt 재설계.

---

## 4.4 본 연구를 위한 AI 파이프라인 아키텍처

```
┌──────────────────────────────────────────────────────────┐
│                  Layer 1: 데이터 입력                      │
│ KSCO 분류항목표 HWPX + 한국직업사전 + NCS + KNOW + KECO    │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│              Layer 2: 정제·통합 (NLP 기초)                  │
│  - 형태소 분석 (Mecab, Khaiii)                              │
│  - 표준화 (동의어 사전, 약어 풀이)                          │
│  - 직업 단위 정렬 (KSCO 세분류 단위)                        │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│           Layer 3: TASK 추출 (LLM 생성·분류)                │
│  - LLM zero-shot: 동사-목적어 형식 task 추출                │
│  - HumRRO 5-step 의사결정나무 자동 실행                     │
│  - Output: 검증된 TASK pool                                │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│           Layer 4: 임베딩 (BGE-m3-ko)                       │
│  - TASK 진술 → 1024차원 벡터                                 │
│  - Output: TASK × 1024 embedding matrix                    │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│        Layer 5: GWA 할당 (LLM few-shot)                    │
│  - 다수결 (Claude / GPT / Gemini)                          │
│  - 인간-AI 합의도 검증                                      │
│  - Output: TASK × GWA 41개 매트릭스                         │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│        Layer 6: GWA 내 클러스터링 (HDBSCAN + BERTopic)      │
│  - 41개 GWA 산하 task 군집화                                 │
│  - 5대 품질 기준 자동 검증                                   │
│  - Output: DWA 후보 군집                                    │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│        Layer 7: DWA Writing (LLM 생성 + 인간 편집)          │
│  - Claude Opus 4.6 초안                                    │
│  - 8대 작성 규칙 자동 검증                                   │
│  - 인간 분석가 최종 확정                                     │
│  - Output: 한국형 DWA 약 2,000개                            │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│        Layer 8: IWA 도출 (DWA 클러스터링 + LLM)             │
│  - GWA 분할하지 않음 (cross-family 목적)                    │
│  - Output: 한국형 IWA 약 300개                              │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│       Layer 9: QC + ID 체계 부여 (Round-Robin)              │
│  - 3개 팀 회전 검증                                          │
│  - Kappa 0.7+ 모니터링                                       │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│    Layer 10: 시뮬레이션 검증 (중분류 2~3개)                  │
│    Output: 검증 보고서 + 직무기술 정의서 시제품              │
└──────────────────────────────────────────────────────────┘
```

---

## 4.5 모델·도구 결정 매트릭스

본 연구에서 실제 사용할 후보 모델·도구를 정리합니다.

| 카테고리 | 1순위 | 2순위 | 비고 |
|---------|------|------|------|
| 한국어 임베딩 | **BGE-m3-ko** (1024d) | KR-SBERT | 본 연구의 주력 |
| 다국어 임베딩 | **BGE-M3** (1024d) | text-embedding-3-large | 영문 O*NET과 비교 시 |
| LLM 분류·생성 (고품질) | **Claude Opus 4.6** | GPT-5 | 한국어 task에 강점 |
| LLM 분류 (대량) | **Claude Haiku 4.5** | GPT-5 mini | 비용 최소화 |
| 클러스터링 | **HDBSCAN + UMAP** | Agglomerative | 군집 수 자동 |
| Topic Modeling | **BERTopic** | LDA | 군집별 키워드 추출 |
| 한국어 형태소 분석 | **Mecab-ko** | Khaiii | 표준 |
| 통계 분석 | Python + Polars | R | SEM 시뮬레이션 |
| 협업 도구 | Notion / Google Sheets | Airtable | round-robin QC |

---

## 4.6 비용·시간 추정

본 연구에 LLM·임베딩을 사용할 경우의 추정 비용:

| 항목 | 처리량 | 추정 비용(USD) | 추정 시간 |
|------|------|-------------|---------|
| 임베딩 (TASK 약 20,000개) | 1024d × 20,000 = 약 50M 토큰 | $5 (text-embedding-3-large) 또는 $0 (BGE-m3-ko 자체 서빙) | 1일 |
| GWA 자동분류 (TASK 20,000개) | 20,000 × 2K 토큰 = 40M | $200 (Sonnet 4.6) 또는 $20 (Haiku 4.5) | 1일 |
| DWA Writing 초안 (2,000개 군집) | 2,000 × 5K 토큰 = 10M | $300 (Opus 4.6) | 1주 |
| 인간 검수 (Round-Robin) | 약 200 person-hour | (인건비 별도) | 4주 |
| **총 AI 추정 비용** | - | **약 $500~700** | - |

LLM·임베딩 비용은 사업 예산(65,000천원)의 0.1% 이하로, **연구원 인건비 대비 무시할 수준**입니다.

---

## 4.7 AI 활용의 4대 위험과 대응

| 위험 | 설명 | 대응 |
|------|------|------|
| **Hallucination** | LLM이 없는 task·DWA를 만들어냄 | 8대 작성 규칙 자동 검증기 + 인간 100% 검수 |
| **모드 붕괴 (mode collapse)** | LLM이 유사 표현만 반복 생성 | Temperature 조정 + 다양성 강제 prompt |
| **편향 (bias)** | 영어권 직업에 유리, 한국 특수 직업에 약함 | 한국 데이터 fine-tuning 또는 RAG (Retrieval-Augmented Generation) |
| **반복가능성 (reproducibility)** | 같은 prompt에 다른 답 | seed 고정 + multi-run voting |

---

## 4.8 실전 적용 사례 — Anthropic Economic Index

2025년 Anthropic은 Claude AI 사용자 데이터를 O*NET task 분류에 매핑하는 **Economic Index** 데이터셋을 공개했습니다. 이는 본 연구가 차용할 수 있는 직접 사례입니다.

- **데이터**: Claude 사용자 수백만 건의 대화를 O*NET 19,000+ task에 자동 매핑
- **방법**: LLM 자체가 자기 사용 사례를 직업 task로 분류 (메타-분류)
- **시사점**: LLM의 task 분류 능력이 O*NET 데이터 갱신 수준에서 검증됨

또한 2026년에 발표된 ["Where can AI be used? Insights from a deep ontology of work activities"](https://arxiv.org/abs/2603.20619) 연구는 O*NET의 20,000개 활동을 재구성하여 13,275개 AI 소프트웨어와 매핑한 사례를 보여줍니다.

> **본 연구 시사점**: AI가 직업 분류·활동 매핑을 인간 수준으로 수행 가능하다는 것은 2025-2026년 시점에 학술·산업 양쪽에서 입증됨. 본 연구의 NLP 활용 정당성은 충분.

---

## 4.9 본 Part 요약 카드

- AI는 13개 단계 중 **9개에서 인간 작업을 절감**. 단 최종 의미 판정은 인간이 함
- **5대 AI 기술 요소**: LLM zero/few-shot, 임베딩, 클러스터링, 생성, 검증·합의
- 권고 스택: **BGE-m3-ko + HDBSCAN + BERTopic + Claude Opus/Sonnet 4.6**
- 인간-AI **Cohen's Kappa 0.7+**를 모니터링 지표로 사용
- AI 활용 추정 비용은 사업 예산의 0.1% 이하 — 인건비 효율의 ROI가 압도적

---

## 4.10 다음 단계

Part 5에서는 AI를 활용한 도출이 **어떤 정량 기준**을 충족해야 하는지 — 임계값 설정, 5대 품질 기준, Kappa 임계 등을 학습합니다.
