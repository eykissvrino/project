# AI 체계 및 폴더 구조 설계 보고서

> P2026-011 한기대 STEP 학습 로드맵(SLR) 및 신규 과목 도출 연구
> 작성일: 2026-05-11
> 설계 범위: Phase A(수주) + Phase B(수행·납품) 전 라이프사이클

---

## 1. 설계 목표

본 사업은 **수주(Phase A) → 수행(Phase B → 11/20 납품)** 두 단계로 구성된 1.48억원 규모 정부 연구용역이다.
AI 체계는 다음 4가지를 동시에 달성해야 한다.

1. **수주 경쟁력**: 평가 기술점수 90점 중 76.5점 이상 + 1순위 협상 진입
2. **수행 효율**: 6개 모듈(M1~M6) × 6개월 일정에서 일관성·품질 유지
3. **재현 가능성**: 모든 의사결정·산출물에 출처·이력 추적 (감사·후속 사업 대비)
4. **차별화 증명**: RFP가 요구한 4대 제언 영역(제도연계/자동화/조사체계/매뉴얼화)에 실제 실행 가능한 답을 제시

## 2. 설계 원리 — "Two-Phase Mission" 통합 설계

### 핵심 원칙
> **제안서에 쓴 모든 약속(Promise)은 Phase B에서 실제로 이행 가능해야 한다.**

→ Phase A 제안서를 작성하는 에이전트와 Phase B 수행을 도와주는 에이전트가 **동일한 CLAUDE.md·메모리·스킬**을 공유한다.
→ 즉, 제안서에서 "Master DB 자동화 도구를 구축한다"고 쓰면, Phase B에서 그 도구를 실제로 만들 수 있는 스킬·에이전트가 이미 준비되어 있다.

## 3. 설계 산출물 요약

### 3.1 폴더 구조 (8개 최상위)

| 폴더 | 역할 |
|---|---|
| `_AI_체계/` | ★ 본 설계의 핵심 — AI 협업 체계 |
| `00_참고자료/` | RFP 외 모든 참고 (전년도 산출물, AI/AX 자료, NCS DB) |
| `01_제안/` | Phase A: RFP 분석 → 전략 → 정량/정성 제안서 → 발표자료 → 제출본 |
| `02_착수/` | 계약 후 착수계 + 과업수행계획서 + 선임계 + 보안각서 |
| `03_수행/` | ★ Phase B: M1~M6 + 공통 데이터 |
| `04_보고및회의/` | 착수/중간/결과 보고회 + 주차보고 + 회의록 |
| `05_최종산출물/` | 11/20 납품물 일체 |
| `99_프로젝트관리/` | PROJECT_PLAN, RISK_LOG, DECISION_LOG, CHANGE_LOG, 계약서 |

### 3.2 AI 협업 체계 (`_AI_체계/`)

```
_AI_체계/
├── CLAUDE.md                  ← 프로젝트 헌법 (모든 세션 진입점)
├── README.md (agents/, skills/, commands/ 각각 1개씩)
│
├── agents/                    ← 9개 전문가 에이전트
│   ├── rfp-analyzer.md
│   ├── proposal-writer.md
│   ├── ncs-analyst.md
│   ├── survey-designer.md
│   ├── course-spec-writer.md
│   ├── ax-curriculum-expert.md
│   ├── data-engineer.md
│   ├── report-writer.md
│   └── qa-reviewer.md
│
├── skills/                    ← 6개 도메인 스킬 SOP
│   ├── ncs-sqf-handling/SKILL.md
│   ├── master-db-management/SKILL.md
│   ├── course-outline-generation/SKILL.md
│   ├── slr-diagram-creation/SKILL.md
│   ├── proposal-formatting/SKILL.md
│   └── koreatech-style-guide/SKILL.md
│
├── commands/                  ← 9개 슬래시 커맨드 워크플로우
│   ├── ingest-rfp.md
│   ├── draft-proposal.md
│   ├── n1-pipeline.md
│   ├── make-course-outline.md
│   ├── weekly-report.md
│   ├── final-deliverable.md
│   └── ...
│
├── memory/                    ← 누적 지식 (인덱스 + 5개 파일)
│   ├── MEMORY.md (index)
│   ├── project_facts.md
│   ├── glossary.md
│   ├── stakeholder_map.md
│   ├── ax_knowledge.md
│   └── last_year_lessons.md
│
└── templates/                 ← 3개 핵심 양식
    ├── 과목개요서_template.md   (RFP 별첨 양식)
    ├── 주차보고_template.md
    └── 회의록_template.md
```

## 4. 에이전트 설계 근거

각 에이전트는 **단일 책임 원칙**에 따라 RFP의 절차·산출물과 1:1 매핑되도록 설계했다.

| 에이전트 | RFP 매핑 | 주 활동 시기 |
|---|---|---|
| `rfp-analyzer` | 전체 RFP | Phase A 초기 |
| `proposal-writer` | RFP §V (제안서 작성안내) | Phase A |
| `ncs-analyst` | RFP §II-2 가·나·다 (M1~M3) | 6~8월 |
| `survey-designer` | RFP §II-2 라 (M4) + §II-3 (재배치) | 7~8월 |
| `course-spec-writer` | RFP §II-2 마 + 별첨 양식 (M5) | 9~10월 |
| `ax-curriculum-expert` | RFP §II-1-나 융합(AI+X) 200과목 | 9~10월 ★ |
| `data-engineer` | RFP §II-1-가 Master DB + 자동화 윈테마 | M1, M6 + 상시 |
| `report-writer` | RFP §II-1-다 보고서·매뉴얼 (M6) | 10~11월 |
| `qa-reviewer` | RFP §III-1 (출처 명기) + 모든 산출 | 상시 |

## 5. 폴더 구조 설계 근거

### 5.1 RFP의 6대 연구절차 = M1~M6 모듈
RFP §II-2 (가~바)와 1:1 매핑되며, 각 모듈 내부는 **단계 → 산출물** 구조로 동일하게 표준화했다.

### 5.2 산출물 추적성
RFP §III-4 표(p.15)의 모든 납품 산출물이 `05_최종산출물/` 하위에 1:1 폴더로 대응한다.

### 5.3 보고·회의 격리
주차보고/중간보고/최종보고 + 수시협의 + 자문위원회의를 분리하여 검색·증빙 용이.

### 5.4 RFP의 4대 제언 영역 반영
- **제도연계** → `report-writer` + 보고서 제8장
- **자동화** → `data-engineer` + `pipelines/` (DB 관리스킬에 정의)
- **조사체계 개선** → `survey-designer` + M4 시나리오 비교
- **매뉴얼화** → `report-writer` SLR 관리매뉴얼 + 각 스킬 SOP

## 6. 윈테마 — 우리가 평가위원에게 약속할 5가지

CLAUDE.md와 `01_제안/02_전략/` 폴더(미작성, 사용자 작업 영역)에서 구체화될 윈테마:

1. **ISC-NCS 양방향 동기화 시스템** (작년 38% 매칭률 → 90%+ 달성)
2. **Master DB 자동화 + 변경 로그 감사 추적** (수기 관리 탈피)
3. **설문 단계 재배치 + 상시 수요조사 채널** (응답 신뢰도↑)
4. **AX 200과목 × GX × 안전(로봇) 융합 매트릭스 설계** (AI 리터러시 확장)
5. **미활용 과목개요서 1년/2년 정책 + 자동 만료** (사후처리 매뉴얼화)

## 7. 활용 시나리오

### 시나리오 1: "RFP 다시 분석해줘"
→ Claude는 CLAUDE.md → `commands/ingest-rfp.md` → `rfp-analyzer` 호출
→ `01_제안/01_분석/`에 4종 산출

### 시나리오 2: "이번 주 주차보고 만들어줘"
→ `commands/weekly-report.md` → `templates/주차보고_template.md` 자동 채움
→ `04_보고및회의/02_주차보고/`에 저장

### 시나리오 3: "AX 과목 10개 작성해줘"
→ `commands/make-course-outline.md` × 10
→ `course-spec-writer` + `ax-curriculum-expert` 협업
→ `qa-reviewer` 검수
→ `03_수행/M5_과목개요서/03_융합AIX_200/AX_AITransformation/`에 저장

### 시나리오 4: "11/20 납품 준비"
→ `commands/final-deliverable.md` → 산출물 12종 체크리스트 자동 실행
→ 인쇄·USB·납품확인서까지 일괄 가이드

## 8. 적용 권장 사항 (사용자 액션)

1. **CLAUDE.md 검토 및 보강** — 우리 회사명, 책임자명, BI 색상 등 확정
2. **참여 인력 정보 입력** — `_AI_체계/memory/stakeholder_map.md`
3. **자문위원 풀 사전 확보** — `_AI_체계/memory/stakeholder_map.md` 자문위원 칸
4. **PROJECT_PLAN 일정 확정** — RFP 공고 마감일·발표일 확정 후
5. **CLAUDE Code / Cowork 연동** — `_AI_체계` → `.claude` 심볼릭 링크 또는 복사 검토
6. **첫 작업 권장**: `ingest-rfp` 커맨드 실행하여 4종 분석 문서 자동 생성

## 9. 본 설계의 차별점 (vs 일반 프로젝트 관리)

| 항목 | 일반 폴더 구조 | 본 설계 |
|---|---|---|
| 목적 | 파일 분류 | + AI 협업 전제 |
| 단위 | 시간순/문서순 | RFP 절차순·산출물 단위 |
| 메타데이터 | 폴더명만 | CLAUDE.md + 에이전트 카드 + 스킬 SOP |
| 일관성 | 사람 주의력 | 자동 검수(`qa-reviewer`) + 템플릿 강제 |
| 재현성 | 메일·구두 | DECISION_LOG + CHANGE_LOG + 버전된 Master DB |
| 차별화 | (없음) | RFP 4대 제언 윈테마 사전 매핑 |

## 10. 결론

본 설계는 **수주 → 수행 → 납품 → 후속사업**의 전체 라이프사이클을 단일 AI 협업 체계로 통합했다.

- ✅ 폴더 구조 = RFP 절차와 1:1 매핑
- ✅ 에이전트 = 단일 책임 + 모듈 매핑
- ✅ 스킬 = RFP 차별화 윈테마의 실행 도구
- ✅ 메모리 = 작년 사업 교훈 + 발주처 협의 누적
- ✅ 커맨드 = 반복 워크플로우 표준화
- ✅ QA = 모든 산출물의 마지막 게이트

이제 다음 단계는 사용자(인간 PM)가 윈테마를 확정하고 첫 슬래시 커맨드(`/ingest-rfp` 또는 `/draft-proposal`)를 실행하는 것이다.

---

*Designed by Claude — 2026-05-11*
