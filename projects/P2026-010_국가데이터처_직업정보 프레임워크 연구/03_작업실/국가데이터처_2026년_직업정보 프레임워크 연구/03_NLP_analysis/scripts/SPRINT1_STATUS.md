# Sprint 1 구현 현황 (2026-05-30)

> 설계 기준선: `04_framework_design/docs/12_도출방법론_설계서.md` (D0~D6)

## 환경
- **venv**: `C:\Users\eykis\.venvs\vrin-nlp` (OneDrive 밖 — 동기화 회피)
- 설치됨(최소): duckdb 1.5.3, pandas, anthropic, openai, python-dotenv, typer, loguru, pytest
- **미설치(Sprint 3)**: sentence-transformers, hdbscan, mecab-python3, kss — Windows 빌드 리스크라 군집 단계에서 설치
- 테스트 실행: `cd 03_NLP_analysis/scripts && C:\Users\eykis\.venvs\vrin-nlp\Scripts\python.exe -m pytest tests/ -q`

## DB 상태
- `results/pipeline.duckdb` 무결성 OK (세분류 495 + 세세분류 1,270, 정의 98.5%)
- **Phase 0의 stale WAL을 백업 이동**: `pipeline.duckdb.wal.bak_20260530_122347` (재생 충돌 원인, main DB가 최신이라 안전). 문제 시 복원 가능.
- DDL 확장 적용됨: `tool_inventory`, `work_context`, `gwa.kr_label/kr_definition`, `task.parent_code/low_signal`

## 구현·테스트 완료 (키 무관, 41 테스트 통과)
| 파일 | 역할 | 테스트 |
|---|---|---|
| `utils/consistency.py` | Jaccard self-consistency + cross-model 다수결 + R3축 일관성 (§1.4) | `tests/test_consistency.py` (15) |
| `utils/llm_client.py` | LLM 호출 + 캐시 + llm_call_log + JSON 재시도 (§0.3) | `tests/test_llm_client.py` (11) |
| `utils/ksco_fetch.py` | **세세분류 + 부모 세분류 주요업무 상속(D0)** + 저신뢰 플래그(길이+ASCII) + scope 이터 | `tests/test_ksco_fetch.py` (12, 실DB) |
| `utils/extract_tasks.py` | 추출 오케스트레이션 extract_one + persist (§1) | `tests/test_extract_tasks.py` (6, mock+mem) |
| `prompts/extract_tasks_system.md` | 시스템 프롬프트 §1.2 (토씨 보존) | — |
| `prompts/extract_tasks_user.template.md` | 사용자 템플릿 §1.3 v1.1 (상속 필드) | — |
| `parsers/ddl_extension.sql` + `apply_ddl_extension.py` | DDL 보강 §10 | 적용 검증 OK |
| `cli/kfw.py` `run extract-tasks` | 세세분류 단위 E2E 배선 (키 게이트 포함) | 키 게이트 exit 1 검증 |

## ✅ E2E 게이트 통과 (2026-05-30, 하이브리드 — API 0원)
- `tools/e2e_28120_manual.py` — Claude Code(구독)가 §1.2 규약대로 28120 회계사 추출, production 경로(extract_one→consistency→persist→DuckDB)로 적재.
- 결과: **task 12 / tool 1 / work_context 3**, self-consistency **jaccard 1.000 auto_accept**, llm_call_log 2행(seed 0·1), 캐시 생성·재실행 시 cached=True(호출 0회).
- 정직한 관찰: 도구 1건(DoD 3~10 미달) = 사무·전문직 도구 약함(§1.5)과 정합. 기술·정비직에서 도구 다수 기대.
- 재현성 주의: 구독 단일추출이라 seed별 변동 없음(jaccard=1.0). 전수 본가동은 API(temp=0·seed)로 재현성 도장.

## E2E 게이트 (API 자동가동 시 — 전수 본가동용)
```
# .env (03_NLP_analysis/scripts/.env) 에 ANTHROPIC_API_KEY=, OPENAI_API_KEY= 입력 후:
C:\Users\eykis\.venvs\vrin-nlp\Scripts\python.exe cli/kfw.py run extract-tasks --scope 28120
# 다자식 상속·저신뢰 검증: --scope 2843  (28431 특화 / 28433 LOW_SIGNAL)
```
DoD: task 5~15건, 도구·환경 동시(빈값 허용), self-consistency jac≥0.85, llm_call_log 적재, 캐시 생성(재실행 0회).

## ✅ ONET 참조 적재 완료 (2026-05-30, Sprint 1 Step 1)
- `parsers/download_onet.py` → O*NET DB v29.3 텍스트 3종 다운로드(`01_data_collection/.../02_ONET_WorkActivities_DWA/onet_data/`)
- `parsers/onet_reference_loader.py` → external_ref 적재: **onet_gwa 41 / onet_iwa 332 / onet_dwa 2,087** 검증 OK
- Sprint 3 gwa-bucket(ONET 41 zero-shot)·map-iwa-gwa 비교의 기준 데이터 확보.

## ✅ 도구 커버리지 = 직업군 의존 (실데이터 입증, 2026-05-30)
| 직업 | task | tool | context | 해석 |
|---|---|---|---|---|
| 28120 회계사 (사무·전문) | 12 | **1** | 3 | 도구 약함 — KSCO 텍스트 한계, 시스템 결함 아님 |
| 74061 가스 용접원 (기술·기능, low_signal) | 10 | **6** | 1 | 도구 풍부(용접장비·전극·용접봉·토치팁·그라인더·철솔) |
→ §1.5 가설 입증: 도구 추출량은 *직업군*에 의존. 74061은 정의 40자(low_signal)였지만 **부모 7406 주요업무 상속**으로 10 task 확보(D0 작동). 통계청 방어 논리 확보.

## 미결 (다음)
- 골든셋 정확도 검증 보류(CEO 결정, M+4 전 재검토) — doc 12 §8.1
- 무거운 ML deps(sentence-transformers·hdbscan·mecab) 설치 + 군집 단계 (Sprint 3)
- 전수 본가동 시 API 결제(재현성 도장) — 시범은 하이브리드로 무료 진행 가능
