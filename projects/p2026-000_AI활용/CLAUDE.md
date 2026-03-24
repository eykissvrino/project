# P2026-000 AI활용 — 비즈니스 에이전트 하네스 프로젝트

## 개요
- **프로젝트명**: AI 활용 체계 구축
- **목적**: AI 솔루션(에이전트·스킬·프롬프트)을 체계적으로 기획·관리·개발·배포하여, 모든 사업과 프로젝트를 성공시키는 AI 인프라 구축
- **참조 모델**: OhMyOpenAgent (ohmyopenagent.com) — 개발자용 에이전트 하네스를 비개발자 사업가용으로 재설계
- **사용자**: 이석주 (시앤피컨설팅 HR 솔루션팀 팀장, 비개발자)

## 핵심 철학 (매니페스토)
- **팀장이 개입해야 한다면, 시스템이 실패한 것** — AI가 마이크로매니징 당하면 안 됨
- **AI 산출물 = 시니어 컨설턴트 수준** — 구분 불가능한 품질
- **한국어로 말하면 끝** — 원하는 것만 말하면, 나머지는 시스템의 일
- **Core Loop**: 의도 → 에이전트 실행 → 검증된 산출물 → 최소 개입

## 에이전트 아키텍처 (4-Tier)

### Tier 0: 오케스트레이션 커널 (OMOA/OMC 기본 제공)
- Sisyphus(총괄), Prometheus(기획), Atlas(실행), Metis(갭분석), Momus(검증)
- Oracle(자문), Librarian(조사), Explore(탐색), Hephaestus(심층작업)

### Tier 1: 비즈니스 오너 에이전트 (7개, 신규 구축)
| 에이전트 | 그리스 원형 | 역할 |
|---------|-----------|------|
| **Athena** (아테나) | 지혜와 전략의 여신 | 경영전략·사업전략·성장전략 수립 |
| **Apollo** (아폴로) | 지식과 예언의 신 | 시장조사·경쟁분석·데이터분석·벤치마킹 |
| **Hera** (헤라) | 조직과 가정의 여신 | HRM/HRD/OD, 직무분석·조직진단·인사제도 |
| **Hermes** (헤르메스) | 소통과 전달의 신 | 모든 문서 산출물 총괄·품질 통제 |
| **Themis** (테미스) | 정의와 법의 여신 | 법률검토·계약서·규정 준수 |
| **Aphrodite** (아프로디테) | 미와 매력의 여신 | 브랜딩·네이밍·스토리텔링·마케팅 |
| **Midas** (미다스) | 황금의 손 | 사업개발·재무추정·BM설계·투자전략 |

### Tier 2: 생산/구현 전문가
- **Daedalus** (다이달로스) — 개발 총괄·아키텍트 (에이전트)
  - 하위 스킬: Arachne(FE), Talos(BE), Iris(모바일), Helios(인프라), Nike(QA)
- **Hermes** 하위 작성 스킬: Calliope(작성), pptx, docx, hwp, excel, pdf

### Tier 3: 메타·운영
- **Chronos** (크로노스) — 프로젝트 관리 (에이전트)
- **Pygmalion** — 자기진화 워크플로우 (에이전트 아님)

### 호출 규칙
1. 모든 사용자 요청 → Sisyphus로 진입 (예외 없음)
2. Sisyphus가 리드 에이전트 1명 지정
3. 리드 에이전트만 허용된 하위 스킬 호출
4. 임의 자유 호출 금지

## 품질 보증 체계

### 랄프 루프 (Ralph Loop)
- 초안 생성 → Momus 1차 검증 → 수정 → Momus 2차 검증 → 확정
- **최대 2회 수정**, 3회 이상이면 기획 단계로 되돌림 (brief 부족 의미)

### 품질계약 (Quality Contract)
- 공통: 정확성, 완결성, 일관성, 가독성, 근거성
- 유형별: PPT(스토리라인), 보고서(프레임워크), Excel(계산검증), 웹앱(요구충족)
- 위치: `_shared/quality-contracts/`

## 자기진화 (Pygmalion 루프)
- 관찰(4종 데이터 수집) → 패턴 탐지 → 개선안 생성 → 그림자 평가 → 승격/폐기
- 트리거: 같은 수정 3회/30일, 같은 흐름 5회/60일, 새 도메인 3개 프로젝트

## 진행 상태
- [x] 기획안 확정 (v2)
- [x] Phase 0-1: CLAUDE.md 작성
- [ ] Phase 0-2: workspace CLAUDE.md 업데이트
- [ ] Phase 0-3: GitHub 동기화 설정
- [ ] Phase 1: 핵심 스킬 고도화 (consulting-report, proposal, job-analysis 등)
- [ ] Phase 2: 에이전트 구축 (Tier 1~3 프롬프트 설계)
- [ ] Phase 3: 루프 체계 구축 (랄프 루프, Pygmalion)
- [ ] Phase 4: 확장·최적화

## 스킬 현황 (품질 감사 결과)
### 즉시 재작성 필요 (P0)
- consulting-report: 23줄 → 150줄 목표
- proposal: 39줄 → 120줄 목표
- job-analysis: 36줄 → 100줄 목표
- data-analysis: 34줄 → 100줄 목표

### 이미 우수 (유지)
- pptx: 489줄 Advanced
- docx: 481줄 Advanced

## 작업 규칙
- 모든 문서는 한국어로 작성
- 최종 산출물은 `outputs/` 폴더에 저장
- 참고 자료는 `data/` 폴더에 저장
- 작업 기록/메모는 `docs/` 폴더에 저장
- _shared/에서 수정 → sync-tools.cmd → 전 프로젝트 반영
- GitHub push로 집/사무실 동기화

## 참고 문서
- docs/OhMyOpenAgent_Architecture_Analysis.md — OMOA 아키텍처 분석
- docs/README_OhMyOpenAgent_Study.md — OMOA 연구 요약
- _shared/REGISTRY.md — 전체 리소스 카탈로그
- _shared/manifesto.md — 비즈니스 매니페스토 (예정)
