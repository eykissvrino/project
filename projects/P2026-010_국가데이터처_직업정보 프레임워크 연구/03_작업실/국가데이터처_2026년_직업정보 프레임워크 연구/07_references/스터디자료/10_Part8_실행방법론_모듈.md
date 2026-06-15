# Part 8. 실행 방법론 모듈 — HWPX·코드·QA·산출물 표준 (Track B 보강)

## 학습 목표

1. KSCO 8차 **분류항목표 HWPX**를 정형 JSON으로 파싱하는 절차를 설계할 수 있다.
2. **임베딩·클러스터링·LLM 분류** 인프라를 본 사업 8개월 일정에 맞게 구축할 수 있다.
3. **한국형 AutoCoder**의 모듈 아키텍처를 사전연구 사례(O*NET-SOC, NIOCCS, G-Code)를 차용하여 그릴 수 있다.
4. **직무기술 정의서 산출물 표준 양식**(필드·길이·검증 규칙)을 정의하고 자동 생성할 수 있다.
5. Round-Robin QC와 **Cohen's Kappa 측정 코드**를 6명·3팀 체제에 적용할 수 있다.

> **본 Part의 위치**: Track B(실행 방법론) 트랙의 최종 모듈. Part 3(미국 방법론)·Part 4(AI 활용)·Part 5(기준 설정)·Part 6(KSCO 워크플로) 뒤에 학습합니다. 코드 예시는 Python 3.11 기준이며 실제 실행 가능한 형태로 제시됩니다.

---

## 8.1 핵심 메시지

본 Part는 다음 5개 모듈로 구성됩니다.

1. **데이터 통합 모듈** — HWPX·PDF·HWP·API에서 정형 JSON으로 (사업 1~2개월차)
2. **NLP·임베딩 인프라 모듈** — BGE-m3-ko 서빙, HDBSCAN, BERTopic (1~2개월차)
3. **AutoCoder 엔진 모듈** — 사전연구 3대 사례를 합성한 한국형 코더 (4~5개월차)
4. **QA·합의 모듈** — Cohen's Kappa, F1, Silhouette 측정 + Round-Robin QC (전 기간)
5. **산출물 표준화 모듈** — 직무기술 정의서 양식·DB 스키마·ID 체계 (6~7개월차)

---

## 8.2 모듈 1 — 데이터 통합 (Data Integration)

### 8.2.1 입력 데이터원 우선순위

본 사업이 통합해야 할 7개 데이터원:

| # | 데이터원 | 형식 | 분량 | 우선순위 |
|---|---|---|---|---|
| 1 | KSCO 8차 분류항목표 | HWPX | 495 세분류 + 1,270 세세분류 | P0 |
| 2 | 한국직업사전 | PDF/XML | 약 6,000 직업 | P0 |
| 3 | NCS 능력단위 | HWP/PDF | 약 1,000 능력단위 | P0 |
| 4 | KNOW (한국직업정보) | API/LOD | 537 직업 다차원 | P0 |
| 5 | KECO 2025 직업정보 | XLSX | 약 200 직업 상세 | P1 |
| 6 | O*NET 30.x | TXT/MDB | 영문 원천 | P1 |
| 7 | 채용공고 데이터 | API/스크래핑 | 가변 | P2 |

### 8.2.2 HWPX 파싱 (한컴오피스 직접 처리)

KSCO 분류항목표는 HWPX 포맷이며, 한컴오피스 외에서 처리하려면 다음 도구를 사용합니다.

**옵션 A — pyhwpx 라이브러리** (한국어 NLP 커뮤니티 표준)

```python
# 설치: pip install pyhwpx
from pyhwpx import Hwp

hwp = Hwp(visible=False)
hwp.open("KSCO_8차_분류항목표.hwpx")

# 모든 텍스트 추출
text_content = hwp.get_text()

# 표 단위 추출 (분류항목표는 표 기반)
tables = hwp.get_tables()
for i, table in enumerate(tables):
    print(f"Table {i}: rows={len(table)}")
```

**옵션 B — pyhwp + hwp5txt** (구버전 .hwp만 지원, .hwpx는 제한적)

**옵션 C — LibreOffice 변환** (CLI 자동화)

```bash
# .hwpx → .docx 변환 후 python-docx로 처리
libreoffice --headless --convert-to docx "KSCO_8차.hwpx" --outdir ./converted/
```

**옵션 D (권장) — 한컴오피스 자동화 + Win32 COM**

```python
import win32com.client

hwp = win32com.client.Dispatch("HWPFrame.HwpObject")
hwp.RegisterModule("FilePathCheckDLL", "AutomationModule")
hwp.Open("C:/path/to/KSCO_8차.hwpx")
# 표 추출 매크로 호출
```

### 8.2.3 파싱 후 표준 JSON 스키마

```json
{
  "ksco_code": "2491",
  "ksco_label": "간호사",
  "level": "세분류",
  "parent_codes": {
    "대분류": "2", "대분류명": "전문가 및 관련 종사자",
    "중분류": "24", "중분류명": "보건·사회복지 및 종교 관련직",
    "소분류": "249", "소분류명": "기타 보건 전문가"
  },
  "occupation_definition": "병원, 의원 등의 의료기관에서 의사와 함께...",
  "main_tasks": [
    "환자 상태 관찰 및 활력징후 측정",
    "의사 처방 약물 투여 및 주사 시술",
    "..."
  ],
  "skill_level": {
    "level": 4,
    "rationale": "학사 이상 교육 + 전문 자격(간호사 면허) + ..."
  },
  "skill_specialization": {
    "knowledge_domain": "의학·간호학",
    "tools_equipment": "의료기기·전자차트시스템",
    "raw_materials": "환자·환자정보·약품",
    "outputs": "환자 간호·간호기록"
  },
  "auxiliary_sources": {
    "직업사전_ids": ["..."],
    "ncs_ability_units": ["..."],
    "know_id": "...",
    "keco_code": "2491"
  },
  "ksco_version": "8th",
  "extracted_at": "2026-06-01T00:00:00Z"
}
```

### 8.2.4 데이터원 간 매핑 코드 예시

```python
# pip install sentence-transformers
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("dragonkue/BGE-m3-ko")

ksco_label = "간호사"
ksco_definition = "병원, 의원 등의 의료기관에서..."

# 한국직업사전에서 후보 직업 검색
dict_jobs = load_korean_job_dictionary()  # 약 6,000개

ksco_emb = model.encode(f"{ksco_label}. {ksco_definition}", convert_to_tensor=True)
dict_embs = model.encode(
    [f"{j['label']}. {j['description']}" for j in dict_jobs],
    convert_to_tensor=True
)

scores = util.cos_sim(ksco_emb, dict_embs)[0]
top_k = scores.argsort(descending=True)[:5]

for idx in top_k:
    print(f"score={scores[idx]:.3f} :: {dict_jobs[idx]['label']}")
# score=0.91 :: 간호사
# score=0.83 :: 가정전문간호사
# score=0.81 :: 노인전문간호사
# ...
```

매핑 후 인간 분석가가 cutoff(예: 0.75 이상) 직업을 검토하여 확정합니다.

---

## 8.3 모듈 2 — NLP·임베딩 인프라

### 8.3.1 한국어 NLP 스택

본 사업이 사용할 권장 스택:

| 계층 | 도구 | 용도 |
|---|---|---|
| 형태소 분석 | Mecab-ko (혹은 Khaiii) | 어절·품사 분석, 동사 추출 |
| 임베딩 | **BGE-m3-ko** (1024d) | 한국어 의미 벡터 |
| 차원 축소 | UMAP | 임베딩 차원 축소 (1024 → 10) |
| 클러스터링 | HDBSCAN | 군집 수 자동 결정 |
| Topic Modeling | BERTopic | 군집별 키워드 자동 추출 |
| LLM API | Claude Opus 4.6 / Sonnet 4.6 / Haiku 4.5 | 분류·생성·검증 |
| 통계 | scipy + statsmodels | SEM 시뮬레이션·Kappa |
| DataFrame | Polars (Pandas 대안) | 대량 task 처리 |

### 8.3.2 BGE-m3-ko 임베딩 인프라 구축

```python
from sentence_transformers import SentenceTransformer
import torch

# CUDA 권장 (CPU도 가능하나 속도 차이 큼)
device = "cuda" if torch.cuda.is_available() else "cpu"
model = SentenceTransformer("dragonkue/BGE-m3-ko", device=device)

# 배치 임베딩
def embed_tasks(task_list, batch_size=32):
    return model.encode(
        task_list,
        batch_size=batch_size,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True  # cosine similarity 사용 시 권장
    )

# 사용 예
task_statements = ["환자의 활력징후를 측정한다", "약물을 투여한다", ...]
embeddings = embed_tasks(task_statements)  # (N, 1024) numpy array
```

### 8.3.3 HDBSCAN + UMAP 클러스터링

```python
import umap
import hdbscan

# 차원 축소
reducer = umap.UMAP(
    n_neighbors=15,
    n_components=10,
    min_dist=0.0,
    metric="cosine",
    random_state=42
)
reduced = reducer.fit_transform(embeddings)

# 클러스터링
clusterer = hdbscan.HDBSCAN(
    min_cluster_size=4,    # DWA 최소 task 수 (한국 보정 3 권장)
    min_samples=2,
    metric="euclidean",     # UMAP 후 euclidean
    cluster_selection_method="leaf"  # 잎노드 = 더 세밀한 군집
)
labels = clusterer.fit_predict(reduced)

# 결과
n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
n_noise = (labels == -1).sum()
print(f"군집 수: {n_clusters} | 노이즈 task: {n_noise}")
```

### 8.3.4 BERTopic — 군집별 키워드 자동 추출

```python
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("dragonkue/BGE-m3-ko")
topic_model = BERTopic(
    embedding_model=model,
    umap_model=reducer,
    hdbscan_model=clusterer,
    language="multilingual",
    calculate_probabilities=True,
    verbose=True
)

topics, probs = topic_model.fit_transform(task_statements, embeddings)

# 군집별 대표 단어
for topic_id in set(topics):
    if topic_id == -1:
        continue
    words = topic_model.get_topic(topic_id)
    print(f"Topic {topic_id}: {words[:5]}")
# Topic 0: [('환자', 0.45), ('관찰', 0.32), ('상태', 0.28), ('활력', 0.18), ('측정', 0.15)]
```

이 대표 단어가 DWA 작성의 초안 단서가 됩니다.

### 8.3.5 LLM API 호출 표준 패턴

```python
import anthropic
import json

client = anthropic.Anthropic()

GWA_DEFINITIONS = """
[1] Getting Information - Observing, receiving, and otherwise obtaining information...
[2] Monitoring Processes, Materials, or Surroundings - ...
... (41개)
"""

def classify_task_to_gwa(task_statement: str) -> dict:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        messages=[{
            "role": "user",
            "content": f"""당신은 직업분석 전문가입니다.
다음 task가 O*NET 41개 GWA 중 어디에 속하는지 1차·2차 선택을 JSON으로 답하세요.

GWA 정의:
{GWA_DEFINITIONS}

Task: "{task_statement}"

응답 형식:
{{"primary_id": "...", "primary_label": "...", "secondary_id": "...", "secondary_label": "...", "reasoning": "...", "confidence": 0.0~1.0}}
"""
        }]
    )
    return json.loads(response.content[0].text)

# 사용 예
result = classify_task_to_gwa("환자의 활력징후를 정기적으로 측정한다")
print(result)
# {"primary_id": "4.A.1.b.1", "primary_label": "Monitoring Processes...", "confidence": 0.92}
```

---

## 8.4 모듈 3 — 한국형 AutoCoder 엔진

### 8.4.1 사전연구 3대 사례의 합성

사전연구 ②(직업문항)가 분석한 3대 AutoCoder를 본 사업 한국형 AutoCoder로 합성하는 설계:

```
┌─────────────────────────────────────────────────────────┐
│           한국형 AutoCoder (KOA, Korean Occupation       │
│                          AutoCoder)                       │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
[O*NET-SOC 차용]      [NIOCCS 차용]        [G-Code 차용]
- NLP + ML            - SOC 808 코드        - FastText + XGBoost
- 시간당 10만건         - 무료/웹기반          - 영·한 다중모델링
- 적합도 점수          - 직업안전 특화          - 자동+수작업 통합
        │                     │                     │
        └─────────────────────┴─────────────────────┘
                              │
                              ▼
              ┌───────────────────────────┐
              │   한국형 AutoCoder 설계     │
              │   - 입력: 11개 개선 직업문항│
              │   - 출력: KSCO 4자리 + DWA  │
              │           + K-SLF 4차원     │
              │   - 엔진: BGE-m3-ko +       │
              │           Claude few-shot   │
              │           + XGBoost 보조    │
              │   - 인터페이스: 웹 (FastAPI)│
              └───────────────────────────┘
```

### 8.4.2 KOA 4단계 처리 파이프라인

```python
class KoreanOccupationAutoCoder:
    def __init__(self, ksco_db, dwa_db, klsf_db, embedder, llm_client):
        self.ksco_db = ksco_db        # KSCO 8차 분류항목표 + 직무기술 정의서
        self.dwa_db = dwa_db          # 한국형 DWA 약 2,000개
        self.klsf_db = klsf_db        # K-SLF 4차원 기준
        self.embedder = embedder      # BGE-m3-ko
        self.llm = llm_client         # Claude Sonnet 4.6

    def code(self, occupation_response: dict) -> dict:
        """
        occupation_response: 사전연구 ②의 11개 개선 직업문항 응답
        Returns: {ksco_code, dwa_ids, k_slf_levels, confidence}
        """
        # Step 1. 직업명·수행업무로 KSCO 코드 후보 검색 (Retrieval)
        candidates = self._retrieve_ksco_candidates(occupation_response)

        # Step 2. LLM이 후보 중에서 정답 선택 (Re-ranking)
        ksco_code = self._llm_rerank(occupation_response, candidates)

        # Step 3. DWA 다중연결 (최대 3개)
        dwa_ids = self._link_to_dwas(occupation_response, ksco_code)

        # Step 4. K-SLF 4차원 추출
        k_slf = self._infer_k_slf(occupation_response, ksco_code)

        return {
            "ksco_code": ksco_code,
            "dwa_ids": dwa_ids,
            "k_slf": k_slf,
            "confidence": self._compute_confidence(...)
        }

    def _retrieve_ksco_candidates(self, resp, top_k=10):
        query = f"{resp['job_title']}. {resp['main_tasks']}. {resp['industry']}"
        q_emb = self.embedder.encode(query)
        # ksco_db에 직업별 임베딩 사전 계산되어 있다고 가정
        scores = cosine_similarity(q_emb, self.ksco_db.embeddings)
        return self.ksco_db.iloc[scores.argsort()[-top_k:][::-1]]

    # ... 이하 _llm_rerank, _link_to_dwas, _infer_k_slf 구현
```

### 8.4.3 KOA 성능 목표 (사전연구 벤치마크 대비)

| 지표 | O*NET-SOC | NIOCCS | G-Code | **KOA 목표** |
|---|---|---|---|---|
| 정확도 | 85%+ | ~80% | ~85% | **≥ 85%** (사전연구 파일럿 97.8% 매칭률을 활용하면 가능) |
| 처리속도 | 10만/시간 | - | - | ≥ 1만/시간 (한국어 LLM 비용 고려 시 OK) |
| 인간 검수 | 가능 | 가능 | 통합 워크플로 | 통합 워크플로 (G-Code 방식) |
| 무료 공개 | 부분 유료 | 무료 | 정부 내부 | 정부 공공API (권장) |

---

## 8.5 모듈 4 — QA·합의 (Quality Assurance & Consensus)

### 8.5.1 Cohen's Kappa 측정 코드

```python
from sklearn.metrics import cohen_kappa_score

def measure_kappa(rater1_labels, rater2_labels, labels=None):
    """
    두 평정자의 라벨 일치도 (Cohen's Kappa)
    """
    kappa = cohen_kappa_score(rater1_labels, rater2_labels, labels=labels)
    return kappa

# 사용 예: GWA 41개 분류에서 두 분석가의 일치도
rater_A_gwa = ["4.A.1.b.1", "4.A.1.b.2", "4.A.2.a.4", ...]
rater_B_gwa = ["4.A.1.b.1", "4.A.1.b.1", "4.A.2.a.4", ...]
kappa = measure_kappa(rater_A_gwa, rater_B_gwa)
print(f"GWA 분류 Cohen's Kappa = {kappa:.3f}")  # 목표 ≥ 0.80
```

### 8.5.2 F1 / Precision / Recall

```python
from sklearn.metrics import f1_score, precision_score, recall_score, classification_report

# AI 자동분류 vs 인간 정답
y_true = [...]  # 인간 정답
y_pred = [...]  # AI 분류 결과

print(classification_report(y_true, y_pred, digits=3))
# precision  recall  f1-score  support
# 4.A.1.b.1    0.92    0.88     0.90     250
# ...
# weighted avg 0.87    0.85     0.86     ...
```

### 8.5.3 Silhouette Score (군집 품질)

```python
from sklearn.metrics import silhouette_score, davies_bouldin_score

# HDBSCAN 결과
labels = clusterer.labels_
mask = labels != -1  # 노이즈 제외

sil = silhouette_score(reduced[mask], labels[mask])
db = davies_bouldin_score(reduced[mask], labels[mask])

print(f"Silhouette: {sil:.3f} (≥0.30 권장)")
print(f"Davies-Bouldin: {db:.3f} (≤1.0 권장)")
```

### 8.5.4 SEM 시뮬레이션 (한국 보정 임계 결정)

```python
import numpy as np

def simulate_sem(all_responses, n_sizes=[5, 10, 15, 20, 30], n_repeat=1000):
    """
    표본 크기별 평균 중요도의 SEM 추정 → 임계 N 결정
    """
    results = {}
    for n in n_sizes:
        sems = []
        for _ in range(n_repeat):
            sample = np.random.choice(all_responses, size=n, replace=False)
            sems.append(np.std(sample, ddof=1) / np.sqrt(n))
        results[n] = {
            "mean_sem": np.mean(sems),
            "max_sem": np.max(sems),
            "pct_above_0.5": np.mean([s > 0.5 for s in sems])
        }
    return results

# 사용 예
nurse_importance_ratings = [4, 5, 3, 4, 5, ...]  # 가정 응답 수십~수백 건
result = simulate_sem(nurse_importance_ratings)
# n=15 mean_sem=0.21 → HumRRO와 유사. n=12부터 SEM≤0.50 만족 시 한국 보정 N=12 채택 가능
```

### 8.5.5 Round-Robin QC 운영 (6명·3팀)

```
[1주차]
   Team A — KSCO 중분류 #X 개발
   Team B — KSCO 중분류 #Y 개발
   Team C — KSCO 중분류 #Z 개발

[2주차]
   Team A → Team C 결과 1차 QC (수정 권한 보유)
   Team B → Team A 결과 1차 QC
   Team C → Team B 결과 1차 QC

[3주차]
   Team A → Team B 결과 2차 QC
   Team B → Team C 결과 2차 QC
   Team C → Team A 결과 2차 QC

→ 모든 팀이 다른 두 팀의 결과를 검토하게 됨 = 정신모델 공유
```

매 20개 직업마다 Kappa 측정 — 0.7 미만 시 즉시 회의 소집.

---

## 8.6 모듈 5 — 산출물 표준화

### 8.6.1 직무기술 정의서 표준 양식 (1쪽 1직업)

```
══════════════════════════════════════════════════════════════
[직무기술 정의서]
════════════════════════════════════════════════════════════��

직업명:    간호사
KSCO 코드: 2491 (세분류)
KSCO 8차:  대분류 2 / 중분류 24 / 소분류 249 / 세분류 2491
발행일:    2026-XX-XX
버전:      1.0
승인:      국가데이터처 통계기준과

──────────────────────────────────────────────────────────────
① 직업개요 (300~500자)
──────────────────────────────────────────────────────────────
환자의 신체적·정신적 상태를 관찰·평가하며, 의사의 처방에 따라 약물·치료를
시행하고, 환자와 가족에게 정보·정서적 지지를 제공한다. 의료기관에서 의사·
다른 의료진과 협력하여 환자의 회복을 지원한다. ...

──────────────────────────────────────────────────────────────
② 주요업무내용 (5~10개 항목, 각 50~100자)
──────────────────────────────────────────────────────────────
• 환자 활력징후 측정 및 신체 상태 관찰
• 처방약물 투여 및 치료 시행
• 환자 차트·간호기록 작성
• 환자·보호자 교육 및 상담
• ...

──────────────────────────────────────────────────────────────
③ 핵심직무활동 (TASK 15~30개 + DWA 다중연결)
──────────────────────────────────────────────────────────────
TASK 01 | 환자의 활력징후(혈압·맥박·호흡·체온)를 정기적으로 측정한다
         | 중요도 4.5 | 빈도 6.2 | 핵심도 0.94
         | 1차 DWA: D0012 환자의 신체 상태와 반응을 관찰한다
         | 2차 DWA: D0045 의료 측정 장비를 사용한다

TASK 02 | 의사 처방에 따라 환자에게 약물을 정맥·근육·경구 경로로 투여한다
         | 중요도 4.8 | 빈도 5.5 | 핵심도 0.91
         | 1차 DWA: D0017 처방약물을 정확한 경로로 투여한다

... (15~30개)

──────────────────────────────────────────────────────────────
④ 표준화직무요소 (3차원 통합)
──────────────────────────────────────────────────────────────
[GWA 프로파일] — task 수 기준
   • 4.A.1.b.1 Monitoring Processes      ████████ 8
   • 4.A.3.a.1 Performing Physical       ██████   6
   • 4.A.4.a.1 Communicating             █████    5
   • 4.A.2.a.4 Documenting Information   ████     4
   • ...

[연결된 DWA — 총 17개]
   D0012  환자의 신체 상태와 반응을 관찰한다 (IWA I02, GWA 4.A.1.b.1)
   D0017  처방약물을 정확한 경로로 투여한다 (IWA I05, GWA 4.A.3.b.6)
   D0045  의료 측정 장비를 사용한다 (IWA I12, GWA 4.A.3.b.4)
   ...

[K-SLF 직능수준 4차원]
   교육 (Education):           ISCED 6 (학사) 이상 — 간호학 학사
   책임성 (Responsibility):     관리 < 감독 < 안전 — 환자안전 직접책임
   경험 (Experience):           신규 1년 + 숙련 3년 (사전연구 숙련기간)
   업무기반학습 (WBL):          일학습병행 부분 적용 / OJT 표준 6개월
   → 종합 직능수준: 4 (최적합 원칙 적용)

[직업 간 전환 가능성] — DWA 공유 수 기준 상위 5
   • 의사 (2492):       18개 공유
   • 임상병리사 (2493): 12개 공유
   • 응급구조사 (2494): 10개 공유
   • 물리치료사 (2495):  9개 공유
   • 약사 (2412):       7개 공유

──────────────────────────────────────────────────────────────
⑤ 참조 데이터
──────────────────────────────────────────────────────────────
한국직업사전: 간호사, 가정전문간호사, 노인전문간호사, ... (총 8건)
NCS 능력단위: NCS-06010101-04 환자관찰, NCS-06010101-05 약물투여, ... (12건)
KNOW: 간호사 (KNOW ID 123)
KECO 2025: 2491

══════════════════════════════════════════════════════════════
[발행: 국가데이터처] [작성: (사)한국직업자격학회] [검증: 외부 패널 5인]
══════════════════════════════════════════════════════════════
```

### 8.6.2 DB 스키마 (PostgreSQL 권장)

```sql
-- 직업 (KSCO 세분류 단위)
CREATE TABLE occupation (
  ksco_code     VARCHAR(5) PRIMARY KEY,
  ksco_label    TEXT NOT NULL,
  parent_codes  JSONB,
  definition    TEXT,
  k_slf         JSONB,    -- {education, responsibility, experience, wbl, composite_level}
  version       VARCHAR(10) DEFAULT '8th'
);

-- GWA (41개)
CREATE TABLE gwa (
  gwa_id        VARCHAR(20) PRIMARY KEY,  -- 예: 4.A.1.b.1
  category      VARCHAR(50),               -- A. Information Input 등
  label_en      TEXT,
  label_ko      TEXT,
  definition_ko TEXT
);

-- IWA (한국형 약 300개)
CREATE TABLE iwa (
  iwa_id        VARCHAR(30) PRIMARY KEY,  -- 예: 4.A.1.b.1.I02
  gwa_id        VARCHAR(20) REFERENCES gwa(gwa_id),
  label_ko      TEXT,
  is_placeholder BOOLEAN DEFAULT FALSE
);

-- DWA (한국형 약 2,000개)
CREATE TABLE dwa (
  dwa_id        VARCHAR(40) PRIMARY KEY,  -- 예: 4.A.1.b.1.I02.D01
  iwa_id        VARCHAR(30) REFERENCES iwa(iwa_id),
  label_ko      TEXT,
  job_family    VARCHAR(50),
  embedding     VECTOR(1024),              -- pgvector 확장
  quality_scores JSONB                     -- {homogeneity, fit, uniqueness, ...}
);

-- TASK (직업 × task)
CREATE TABLE task (
  task_id       SERIAL PRIMARY KEY,
  ksco_code     VARCHAR(5) REFERENCES occupation(ksco_code),
  statement     TEXT,
  importance    NUMERIC(3,2),
  frequency     NUMERIC(3,2),
  relevance     NUMERIC(4,3),
  core_label    VARCHAR(20),   -- core / supp_A / supp_B / non_relevant
  embedding     VECTOR(1024)
);

-- TASK ↔ DWA 다중연결 (N:M, 최대 3개)
CREATE TABLE task_dwa_link (
  task_id       INT REFERENCES task(task_id),
  dwa_id        VARCHAR(40) REFERENCES dwa(dwa_id),
  link_order    SMALLINT,  -- 1, 2, 3
  reviewer      VARCHAR(50),
  reviewed_at   TIMESTAMP,
  PRIMARY KEY (task_id, dwa_id)
);
```

### 8.6.3 ID 명명 규칙

| 객체 | ID 형식 | 예 |
|---|---|---|
| KSCO 직업 | 4자리 숫자 | `2491` |
| GWA | 5-part 도트 ID | `4.A.1.b.1` |
| IWA | GWA + `.I` + 2자리 | `4.A.1.b.1.I02` |
| DWA | IWA + `.D` + 2자리 | `4.A.1.b.1.I02.D01` |
| TASK | `T` + 직업코드 + 4자리 시퀀스 | `T2491-0001` |

**핵심 원칙**: IWA·DWA 번호는 **무작위 부여** (의미 순서 X). 추가 시 재배치 불필요.

---

## 8.7 8개월 실행 일정 매핑 (전체 모듈 통합)

```
[1개월] 모듈 1 데이터 통합 + 모듈 2 NLP 인프라
        - HWPX 파서·임베딩 서빙·LLM API 키 확보
        - 분석가 paired 훈련 (Kappa 0.7 도달)
        - SEM 시뮬레이션 1회

[2-3개월] 모듈 1 후반: 직업당 통합 코퍼스 구축
          모듈 4 시작: Kappa·F1 모니터링

[4-5개월] 모듈 3 KOA 엔진 구축
          - GWA 매핑·DWA 군집·DWA 작성
          - Round-Robin QC 1주차부터 시작

[6개월]   모듈 3 후반: IWA 도출 + DWA Refinement
          모듈 5 산출물 표준화 — 직무기술 정의서 양식 확정

[7개월]   외부 전문가 5인 패널 검토
          KOA 파일럿 테스트 (500 응답 자동코딩 정확도)
          시뮬레이션 중분류 2~3개 완성

[8개월]   최종 보고서 + 직무기술 정의서 시제품 + KOA 데모
```

---

## 8.8 본 Part 요약 카드

- **5개 모듈**: 데이터 통합 / NLP 인프라 / KOA 엔진 / QA·합의 / 산출물 표준
- **KSCO HWPX**는 pyhwpx 또는 win32com 또는 LibreOffice 변환으로 처리
- 한국어 NLP 스택: **Mecab-ko · BGE-m3-ko · UMAP · HDBSCAN · BERTopic · Claude**
- **KOA(한국형 AutoCoder)**: O*NET-SOC + NIOCCS + G-Code 합성 설계
- **Cohen's Kappa·F1·Silhouette·SEM 시뮬레이션** 코드 모듈화
- **직무기술 정의서 1쪽 표준 양식** + PostgreSQL DB 스키마 + ID 명명 규칙

---

## 8.9 다음 단계

본 Part까지 학습하면 Track B(방법론·실행) 트랙이 완료됩니다. 부록(`08_부록_용어집_체크리스트_연습문제.md`)에서 학습 정도를 점검하세요.

또한 본 사업 1개월차에 본 Part의 코드 예시를 **실제 실행**해 보는 것을 권장합니다. 특히:
- HWPX 파서 1회 완성
- BGE-m3-ko 임베딩 서빙 1회 구축
- LLM API 호출 100건 테스트 (Cohen's Kappa 측정)
- 1개 직업으로 KOA 엔진 프로토타입 1회 구현
