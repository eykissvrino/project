# Stage 1 (TASK 추출) 핸드오프 — 새 세션용

> v1.0 · 2026-06-08 · **이 문서 하나로 새 세션이 Stage 1을 이어받는다.** Stage 0(전처리)은 권위 재구현 완료.

## 0. 새 세션 첫 한마디(이석주용)
> "국가데이터처 직업정보 프레임워크 — **Stage 1 TASK 추출**을 시작하자. 핸드오프는 `04_framework_design/docs/stages/07_Stage1_TASK추출_핸드오프.md`. 이거랑 `Stage1_TASK_도출_설계.md` 읽고, 시범 중분류 28로 먼저 가보자."

## 1. 지금까지 (완료)
- **Stage 0 전처리 = 권위 원천(통계청 공식 HWPX) 직접 파싱으로 재구현 완료.**
  - 원천: `01_data_collection/00_external_references/.../한국표준직업분류_2024년 고시_8차/`
    의 **해설서**(`1. (해설서)…hwpx`, 1037p) + **분류항목표**(`제8차…분류 항목표.hwpx`).
  - 산출: **위계 트리 1,999노드**(대10·중57·소167·세495·세세1270) + 각 수준 정의 + 주요업무(L4/L5) + 예시 + 제외 + **추출컨텍스트**(빈약 세세를 조상정의로 보강).
  - 산출물: `03_NLP_analysis/TEST1/outputs/S0_전처리.xlsx` (7시트: 데이터사전·분류체계·위계트리정의·추출컨텍스트·주요업무·직업예시·커버리지요약).
  - 품질 감사 통과(다중공백 0·중복 0·정의 1270/1270·비종결 86=원문 구조특성).
- **설계 검토 완료** → Stage1 설계에 즉시수정 반영: 개수 8~30/40 통일(M1), 입력=추출컨텍스트+출처분기(C2), near-dup 병합(C3), seed 표현 교정(S1). Stage2엔 플래그(8조항 명문화 M2·군집규모/트리 C1·링키지임계 M3·임베딩벤치 M4).

## 2. 코드·DB·환경 (TEST1이 신규 정본)
- **신규 정본 코드**: `03_NLP_analysis/TEST1/pipeline/` — `parse_ksco.py`(HWPX 권위 파서)·`db.py`·`s0_preprocess.py`·`export_excel.py`. 테스트 `TEST1/tests/` 10 pass.
- **DB(SSOT)**: `03_NLP_analysis/TEST1/pipeline.duckdb` — `ksco_node`·`ksco_main_task`·`ksco_example`·`ksco_exclusion` + `external_ref.onet_*`(41/332/2087) + `mapping_ksco_keco`. 분석 산출 테이블(task 등) 0행.
- **venv**: `C:\Users\eykis\.venvs\vrin-nlp` (Python 3.13). 설치됨: duckdb·pandas·anthropic·openai·dotenv·typer·loguru·pytest·openpyxl. Stage 1엔 추가설치 불필요(임베딩은 Stage 2부터: scipy·FlagEmbedding/sentence-transformers).
- **실행**: `cd 03_NLP_analysis/TEST1 && C:\Users\eykis\.venvs\vrin-nlp\Scripts\python.exe -m pytest tests/ -q`
- ⚠️ **reconcile 필요**: 기존 `03_NLP_analysis/scripts/`에 Stage1 코드 일부(`utils/extract_tasks.py`·`consistency.py`·`llm_client.py`·프롬프트·E2E)가 구현·테스트돼 있음. **신규 TEST1 DB/S0 입력에 맞춰 이식**할지, TEST1에 새로 둘지 첫 결정.

## 3. Stage 1이 하는 일 (설계 = `Stage1_TASK_도출_설계.md`)
- 세세분류 1,270 각각에서 **TASK(동사+목적어) + 도구 + 환경** 3차원 동시 추출.
- **입력 = S0 `추출컨텍스트`**(세세+조상 정의 결합) + 상속 `main_tasks` + 예시.
- **출처 분기**: 주요업무 보유(자체167/세분류상속1027)→2-pass / **없음 76(군인 등)→정의·조상정의로만 추출** / 빈약(385)→조상정의 보강.
- **모델 = Opus 4.8 단독**(구독·Claude Code 서브에이전트, **API키/GPT 금지**). 2회 독립 실행 합집합 → **bge-m3 near-dup 병합(cos≥~0.9)**.
- 개수 **8~30 목표·상한 40**(ONET 준거). 각 TASK에 `source_sentence`·`derived_from` 추적 기록.

## 4. 권장 다음 행동
1. §2 reconcile 결정(기존 scripts 이식 vs TEST1 신규).
2. **시범 중분류 28(경영·금융, 79개 세세)** 먼저 — Opus 서브에이전트로 TASK 추출 → S1 엑셀 검수(추적성·개수·출처분기 확인).
3. 검수 통과 후 전수 확대(배치·이어달리기; DuckDB 체크포인트로 skip 재개).

## 5. 하지 말 것
- ❌ API키/GPT ❌ HDBSCAN ❌ 개수 무제한(8~30/40) ❌ 빈약 세세를 세세정의 단독으로 추출(조상정의 필수).
- ❌ 구식 문서(`10_파이프라인_사양서`·`12_도출방법론_설계서`)의 폐기결정 인용 — `stages/` 우선.
