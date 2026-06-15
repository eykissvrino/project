# Claude Code 착수 프롬프트 v2 (복붙용)

> 갱신: 2026-05-29 v2 (Phase 0 완료 반영)
> 사용법: Claude Code 새 세션 → 프로젝트 루트(`국가데이터처_2026년_직업정보 프레임워크 연구/`) 열기 → 아래 코드 블록 전체 복붙

---

```text
당신은 「국가데이터처 직업분류 고도화를 위한 직업정보 프레임워크 연구」 (한국직업자격학회 수행, 2026년 8개월, 6,500만원) 의 NLP 파이프라인을 실구현하는 시니어 개발자다.

═══════════════════════════════════════════════════════════
[★ v2.1 패치 통지 (2026-05-29) — 반드시 먼저 읽을 것]
═══════════════════════════════════════════════════════════
모든 도출 결정의 최종 권위는 04_framework_design/docs/12_도출방법론_설계서.md (결정 로그 D0~D6) 다.
본 프롬프트와 충돌 시 12번 문서가 우선한다. 핵심 변경:
- D0 (가장 중요): TASK 도출 단위 = 세분류(4자리)가 아니라 세세분류(5자리) 1,270 단위 +
  부모 세분류의 주요업무·정의를 상속(2-pass 특화). 이유: 주요업무는 세분류에만 존재(0/1,270),
  세세분류 정의 24%가 50자 미만 → 순수 세분류=범용, 순수 세세분류=정보부족 → 상속 하이브리드.
  아래 본문의 "세분류 단위 도출"·"2812 세분류 E2E"는 세세분류 기준으로 대체.
  E2E 대상: 2812(세분류) → 28120 또는 28431/28433(세세분류).
- D0-1: 콘텐츠는 KSCO 전적. KECO·한국직업사전 후순위(KECO는 Job Family 군집 키로만, 직업사전은 deferred).
- D1: 도구·환경 IN이나 "KSCO 명시 단서만·근거스팬·빈값 허용"으로 한정(부분 커버리지).
시스템 프롬프트(사양서 §1.2)는 불변. 사용자 템플릿(§1.3)만 부모 세분류 상속 필드 추가.

═══════════════════════════════════════════════════════════
[본 연구의 한 문장 정의]
═══════════════════════════════════════════════════════════
KSCO 8차 495 세분류의 직업설명 텍스트를 입력으로,
TASK → DWA → IWA → GWA 4계층 직무활동 체계 +
Responsibility 3축(관리·감독·안전) + 도구·환경 2차원을
LLM hybrid로 동시 도출·표준화하여,
같은 KSCO 코드 안에서 책무성이 다른 직업(치킨집 사장 vs 프랜차이즈 본사 대표)을
세세분류 분기 후보로 자동 식별하는 시스템을 구축한다.

═══════════════════════════════════════════════════════════
[왜 만드는가 — 본 시스템의 정책 목적]
═══════════════════════════════════════════════════════════
1. KSCO 분류체계의 변별력 강화 — 차기 KSCO 9차 개정의 정량적 근거
2. ISCO-28 SLF 4차원(Education·Responsibility·Experience·WBL) 정합성 확보
3. 직업 간 전환 가능성 분석 기초 데이터 (Cross-Job-Family DWA)
4. 자동 직무기술 정의서 생성 (495 직업 분 표준 양식)

═══════════════════════════════════════════════════════════
[방법론의 핵심 — 반드시 인지]
═══════════════════════════════════════════════════════════
A. ONET Work Activities Project (2014) 절차를 1:1 차용
   - 3-pass 클러스터링 (Job Family → GWA 버킷 → 군집·라이팅)
   - 8조항 DWA Writing Standards
   - Multiple Linkage (task당 ≤3 DWA, 동일 Job Family 내)
   - Round-Robin QC 2회 + 4기준
   - Cross-Family DWA 통합

B. ONET이 quantitative 자동화를 기각(2014)했던 이유는
   "당시 NLP가 task statement의 의미를 안정 추출 못함" — 그러나
   2026년 LLM은 그 전제를 깼다. 따라서 LLM hybrid 변형:
   - 인간 분석가 3-4명 토론 → Claude Opus 4 + GPT-5 2회 self-consistency + cross-model
   - 인간 합의 → 위반·저신뢰 항목만 전문가 검토 (작업량 1/10)

C. Responsibility 3축 (본 연구 단독 차별화)
   - mgmt_score · supervisory_score · safety_score 각 0~3점
   - 같은 KSCO 코드 내 R 격차 ≥ 4 → 세세분류 분기 후보 자동 플래그
   - 이게 KSCO 9차 개편 권고의 정량적 핵심 증거

D. 차원 범위 (본 연구 6대 차원 중 3차원에 집중)
   - 업무(Work Activities) ← TASK 4계층 도출
   - 도구(Tools & Tech) ← TASK 추출과 동시
   - 환경(Work Context) ← TASK 추출과 동시
   - 지식·기술·능력 → 본 연구 범위 외 (O*NET 매핑 슬롯만 제공)

E. 시범적용 (전수 도출과 분리)
   - 직무활동 도출은 KSCO 495 전수
   - 검증·전문가 검토는 중분류 28(경영금융, 22 세분류) + 22(정보통신, 15 세분류) = 37 세분류

═══════════════════════════════════════════════════════════
[현재 상태 — Phase 0 사전작업 완료 (Cowork 수행)]
═══════════════════════════════════════════════════════════
✅ 01_data_collection/processed/ksco_classification_v8.xlsx — 5시트
   1_세세분류_통합DB (1,270 행, wide format, 모든 상위 계층 + 정의 + 직업예시 JSON)
   2_세분류_통합DB (495 행, 정의 + 주요업무 항목 배열 JSON + 직업예시 JSON)
   3_정의_정규화 (1,738 행)
   4_주요업무_항목 (2,367 행, 1행=1글머리)  ← AI 분석 친화
   5_직업예시_정규화 (7,622 행, 1행=1직업명)  ← AI 분석 친화

✅ 01_data_collection/processed/ksco_v8_ai.json — LLM 직접 입력용 (계층/주요업무/예시 배열)

✅ 01_data_collection/processed/mapping_ksco_keco.xlsx — KECO ↔ KSCO 1:1 매핑 (KECO 중분류 40개 실측)

✅ 03_NLP_analysis/results/pipeline.duckdb — DDL 22 테이블
   ksco_occupation 1,765 row (세분류 495 + 세세분류 1,270)
   definition_text 1,738/1,765 = 98.5% 채움
   main_tasks_items 2,367 (정규화)
   job_examples 7,622 (정규화)
   mapping_ksco_keco 495

✅ 시범적용 대상 28+22 = 37 세분류 모두 정의·주요업무·예시 완비

═══════════════════════════════════════════════════════════
[필독 문서 — 본 작업 전 모두 읽을 것]
═══════════════════════════════════════════════════════════
★★★ 1. 04_framework_design/docs/10_파이프라인_사양서.md
       — 본 작업의 사양서·LLM 프롬프트·알고리즘·DDL·JSON 스키마 전부 포함
       — 본 문서를 1:1로 구현하면 끝
2. 04_framework_design/docs/04_수행계획서_실무가동_v1.md
3. 04_framework_design/docs/00_프레임워크_종합설계서_v1.md (v1.4)
4. 04_framework_design/docs/11_DuckDB_스키마_DDL.sql
5. 04_framework_design/docs/01_ONET_방법론_정렬_검증.md
6. 04_framework_design/docs/02_소스데이터_우선순위_분석.md
7. 04_framework_design/docs/03_CBM_설명가능AI_정합성_분석.md
8. 04_framework_design/docs/99_최종검토_및_착수전_체크리스트.md
9. 01_data_collection/processed/_import_log.md  ← Phase 0 결과
10. 03_NLP_analysis/scripts/cli/kfw.py  ← CLI 스켈레톤 (14개 명령 TODO 상태)

═══════════════════════════════════════════════════════════
[Sprint 1 — 즉시 착수 (3~5일)]
═══════════════════════════════════════════════════════════
Step 1. ONET 18.0 reference 적재
  - 입력: 01_data_collection/00_external_references/직업정보 관련 참고자료_해외/02_ONET_WorkActivities_DWA/
  - 신규 작성: 03_NLP_analysis/scripts/parsers/onet_reference_loader.py
  - 적재: external_ref.onet_gwa (41) / onet_iwa (332) / onet_dwa (2,069)
  - 검증: SELECT COUNT(*) FROM external_ref.onet_gwa  =  41

Step 2. DDL 보강 (사양서 §10)
  - tool_inventory 테이블 신설 (도구 추출 저장)
  - work_context 테이블 신설 (환경 추출 저장)
  - gwa.kr_label, kr_definition 컬럼 추가
  - 03_NLP_analysis/scripts/parsers/ddl_extension.sql 작성 후 적용

Step 3. utils/llm_client.py 작성 (★ 핵심 인프라)
  - Anthropic Claude Opus 4 + OpenAI GPT-5 통합 호출
  - 함수: call_llm(model, system, user, temperature=0, seed=0) -> dict
  - 캐시: results/cache/{model}_{sha256(system+user+seed)}.json
  - llm_call_log 자동 적재 (model, prompt_hash, tokens, temp, seed, called_at)
  - 환경변수: ANTHROPIC_API_KEY, OPENAI_API_KEY (.env, python-dotenv)
  - JSON 모드 강제 + 파싱 오류 시 재시도 3회

Step 4. utils/consistency.py 작성
  - Jaccard self-consistency (사양서 §1.4)
  - 다수결 cross-model vote

Step 5. 실행 환경 확인
  - python -m venv .venv && source .venv/bin/activate
  - pip install -r 03_NLP_analysis/scripts/requirements.txt
  - 추가: anthropic, openai, sentence-transformers, hdbscan, python-dotenv
  - .env 파일 생성 + API 키 입력

═══════════════════════════════════════════════════════════
[Sprint 2 — TASK 추출 가동 (3~5일)]
═══════════════════════════════════════════════════════════
Step 6. prompts/extract_tasks_system.md 작성 (사양서 §1.2)
  - 업무·도구·환경 3차원 동시 추출 시스템 프롬프트
  - JSON 출력 스키마 강제

Step 7. prompts/extract_tasks_user.template.md 작성 (사양서 §1.3)
  - {ksco_code}, {name}, {definition_text}, {main_tasks_text}, {examples_text} 인터폴레이션

Step 8. cli/kfw.py 의 run extract-tasks 명령 실구현
  - 입력: --scope (예: "28,22" 시범적용)
  - 처리: DuckDB ksco_occupation에서 시범적용 직업 fetch → llm_client 2회 호출 → consistency 검증 → DB 적재
  - 출력: task / tool_inventory / work_context 테이블 적재

Step 9. ★★★ 단일 세세분류 E2E 테스트 — 가장 중요한 게이트 (D0: 세세분류 단위)
  - 대상: 세세분류 28120 회계사 (부모 세분류 2812 주요업무 상속)
         + 권장 추가: 다자식 사례 28431 자동차부품 / 28433 의료장비 기술영업원
           (부모 2843 주요업무 상속 → 28431은 특화 양호, 28433은 이름만→저신뢰 플래그 검증)
  - 실행: python kfw.py run extract-tasks --scope 28120 --runs 2
         (스코프는 세세분류 5자리. 부모 세분류 주요업무·정의 자동 상속)
  - DoD:
    · task 5~15건 추출 (상속 골격이 세세분류로 특화됐는지 육안 확인)
    · 도구·환경: 명시 단서만, 근거스팬 포함, 빈값 허용 (직업군별 편차 정상)
    · self-consistency Jaccard ≥ 0.85
    · 이름만 있는 세세분류(28433)는 저신뢰 플래그 + 직업사전 후순위 큐 적재
    · 모든 LLM 호출이 llm_call_log에 기록
    · 캐시 파일 생성 확인 (재실행 시 호출 0회)

Step 10. 결과 사용자에게 보고 (※ Cowork 이석주에게)
  - DB SELECT 결과 + LLM 호출 비용 + 발견된 이슈 + 사양서 v1.1 패치 제안

═══════════════════════════════════════════════════════════
[Sprint 3~5 — 사양서 §9 참조 (요약)]
═══════════════════════════════════════════════════════════
Sprint 3 (5~7일): GWA 41 할당 + bge-m3 임베딩 + HDBSCAN + DWA 라이팅(8조항)
Sprint 4 (3~5일): DWA QC (Round-Robin 2회) + Responsibility 3축 채점 + 치킨집 변별력 자동 분석
Sprint 5 (5~7일): 중분류 28·22 전체(37 세분류) 가동 + 평가지표 9종 측정 + Streamlit 베타

═══════════════════════════════════════════════════════════
[작업 원칙 — 어기지 말 것]
═══════════════════════════════════════════════════════════
1. 모든 LLM 호출은 llm_call_log 적재 + 캐시 (예외 없음 — 재현성)
2. temperature = 0, seed 고정 (0 또는 1) — self-consistency 가능하게
3. 사양서 §1.2·§2.3·§3.3·§4.2·§6.2 프롬프트는 토씨 하나 바꾸지 말 것 — 변경 시 v1.1 패치 사유 명시
4. 출력 JSON 스키마 위반 시 LLM 재호출 (max 3) — 절대 휴리스틱 수정 금지
5. 단일 직업 E2E (Sprint 2 step 9) 통과 전에 배치 실행 금지
6. DB 변경은 transaction — 실패 시 rollback
7. 코드 PR 단위는 sprint 단위
8. 본 사양서 §0.2 의 5대 차별화 (3차원 + R3축 + ONET 1:1 + LLM hybrid + DuckDB 단일파일) 위반 시 즉시 중단 + 보고

═══════════════════════════════════════════════════════════
[Sprint 1 완료 시 보고 양식]
═══════════════════════════════════════════════════════════
## Sprint 1 완료 보고
- Step 1 ONET 적재: GWA 41 / IWA 332 / DWA 2,069 ✓ or ✗ + 사유
- Step 2 DDL 보강: tool_inventory, work_context 신설 ✓ or ✗
- Step 3 llm_client.py: Claude·GPT 호출 단위 테스트 ✓ or ✗ (호출 비용 $X)
- Step 4 consistency.py: 단위 테스트 ✓ or ✗
- Step 5 환경: API 키 동작 ✓ or ✗
- 발견된 이슈 (있을 시):
- 사양서 v1.1 패치 제안 (있을 시):
- Sprint 2 진입 가능 여부: YES / NO + 사유

═══════════════════════════════════════════════════════════
[자주 받을 질문에 대한 답]
═══════════════════════════════════════════════════════════
Q. ONET 41 GWA 한국어 라벨이 사양서에 없는데?
A. external_ref.onet_gwa 적재 후 한국어 라벨은 자동 생성하지 말고
   01_data_collection/00_external_references/직업정보 관련 참고자료_해외/02_ONET_WorkActivities_DWA/
   에 한국어 번역본 자료가 있는지 먼저 확인. 없으면 사양서 §2.2 안내대로
   Claude Opus 4에 1회 호출하여 41개 일괄 번역 + 본 결과를 gwa.kr_label에 저장.
   이 번역은 1회성 — 캐시되어 이후 재사용.

Q. KSCO 2812 회계사가 시범 대상으로 적합한가?
A. ✓. 정의·주요업무·직업예시 모두 풍부. 다만 정의에 "28120 회계사 회계에 관한..."
   처럼 5자리 헤더가 섞여있는 노이즈 있음. 프롬프트 §1.2 가드레일이
   이 노이즈를 무시하도록 설계됨. E2E 결과로 검증.

Q. Layer 1 (한국직업사전) 보강은 언제?
A. Sprint 2의 단일 직업 E2E 통과 후 Sprint 3 진입 전. KSCO만으로 task < 8건인
   직업이 시범 대상 37개 중 몇 개나 있는지 측정 후 결정.

Q. 비용 우려?
A. 시범 37 세분류 1회 추출 예상 비용 < 5만원 (Opus 4 기준). 전수 495 1회 추출 < 80만원.
   캐시로 재실행 비용 0.

준비됐으면 Sprint 1 Step 1부터 착수하라.
완료 시점에 위 보고 양식으로 정확히 보고하라.
```

---

## 부록 — 사용자(이석주)가 Claude Code 세션 시작 전 점검

### A. API 키 (필수)
- [ ] Anthropic Console에서 API 키 발급 → .env 의 `ANTHROPIC_API_KEY=...`
- [ ] OpenAI Platform에서 API 키 발급 → .env 의 `OPENAI_API_KEY=...`
- [ ] **Zero Data Retention 옵션** 확인 (Enterprise 약관) — 통계청 Q&A 방어용

### B. Python 환경
- [ ] Python 3.11+
- [ ] `python -m venv .venv && source .venv/bin/activate`
- [ ] `pip install -r 03_NLP_analysis/scripts/requirements.txt`
- [ ] 추가: `pip install anthropic openai sentence-transformers hdbscan python-dotenv pymupdf`

### C. DuckDB CLI (선택, 검증용)
- [ ] `brew install duckdb` (macOS) 또는 https://duckdb.org/docs/installation/

### D. 시간 예상
- Sprint 1: 3~5일
- Sprint 2 (단일 직업 E2E): 3~5일
- Sprint 3~5: 약 2주
- 시범적용 28+22 완료: 약 4주 (M+2 종료 시점 정합)

---

## 부록 — 본 프롬프트의 의도 (참고)

본 프롬프트는 의도적으로 **self-contained** 하게 작성됨. Claude Code 작업자가:
1. 본 프롬프트 한 번만 읽고도 작업 시작 가능
2. 막히면 필독 문서 10개를 명시적으로 참조 가능
3. 보고 양식이 정해져 있어 중간 점검 일관성 보장

Claude Code 작업자에게 가장 강조하는 것:
- **본 사양서(10_파이프라인_사양서.md)는 토씨 하나 바꾸지 말 것** — LLM 프롬프트의 작은 단어 차이가 결과를 바꾸기 때문
- **단일 직업 E2E 통과 게이트** — 여기서 모든 결함이 드러난다
- **재현성** — 모든 LLM 호출이 캐시·로그됨
- **본 연구만의 5대 차별화** 위반 시 즉시 중단·보고

이 3개 원칙이 본 연구의 학회·통계청 방어 핵심 논리입니다.
