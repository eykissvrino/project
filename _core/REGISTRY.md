# AI 리소스 마스터 레지스트리

> 이석주(시앤피컨설팅 HR솔루션팀)의 AI 작업 환경에서 사용 가능한 모든 스킬, 에이전트, 워크플로우, 커맨드, 플러그인의 통합 카탈로그입니다.
>
> **최종 업데이트**: 2026-05-28
> **자동 갱신 규칙**: 분기 1회 정기 점검 + 신규 리소스 추가/제거 즉시 → [`SYSTEM_EVOLUTION_LOOP.md`](SYSTEM_EVOLUTION_LOOP.md) 참조

---

## 빠른 참조

| 리소스 유형 | 수량 | 위치 |
|-------------|------|------|
| Tier 1 스킬 (전역, 유저 레벨) | 69개 | `~/.claude/skills/` |
| Tier 2 스킬 (워크스페이스 레벨) | 25개 | `_core/skills/` |
| 에이전트 (그리스신화 비즈니스) | 9개 | `_core/agents/` (Tier 1) |
| 에이전트 (기술/개발 레거시) | 12개 | `_core/agents/` (Tier 2) |
| 워크플로우 (자기진화·품질) | 2개 | `_core/workflows/` (Ralph·Pygmalion) |
| 워크플로우 (레거시 Antigravity) | 7개 | `_core/workflows/` (agent-01~07) |
| 품질계약 | 1개 | `_core/quality-contracts/` |
| 커맨드 (유저+워크스페이스) | 4개 | `~/.claude/commands/` + `_core/commands/` |
| 플러그인 | 2개 | `~/.claude/plugins/` (mckinsey-pptx, oh-my-claudecode) |
| 프롬프트 라이브러리 | 6개 폴더 | `_core/prompts/` (common, claude-web, cowork) |
| 활성 프로젝트 | 15개 | `projects/` |
| **합계** | **150+** | |

---

## 0. 디바이스 환경

| 디바이스 | 역할 | AI 환경 |
|----------|------|---------|
| 💻 노트북 (회사/현장) | **풀-기능 주력** | Claude Code + 모든 스킬·에이전트·MCP |
| 🖥️ 데스크탑 (집/야간) | **풀-기능 주력 (노트북 동등)** | Claude Code + 모든 스킬·에이전트·MCP |
| 📱 핸드폰 (이동 중) | 빠른 손 (보조) | Claude 앱, Claude Web Projects, Notion |

**핵심 원칙**: 노트북과 데스크탑은 **물리적 위치만 다른 동등한 풀-기능 환경**. 디바이스 패리티는 [`DEVICE_PARITY_CHECKLIST.md`](../DEVICE_PARITY_CHECKLIST.md)로 보장.

---

## 1. 활성 프로젝트 (15개)

### 영구 프로젝트 (P0000) — 연도 무관

| 코드 | 프로젝트 | 성격 |
|------|---------|------|
| P0000-000 | AI활용 | AI 도구·체계 자체 관리 (메타 프로젝트) |
| P0000-001 | 월인가술빚는날 | 개인 취미/창작 |
| P0000-002 | Book | 도서 집필/학습 |

### 2026년 업무 프로젝트 (P2026)

| 코드 | 프로젝트 | 리드 에이전트 |
|------|---------|---------------|
| P2026-001 | 장애인 B2B사업 | Midas + Hera + Themis |
| P2026-002 | AX진단 컨설팅도구 | Athena + Daedalus |
| P2026-003 | 2026 선도기업 직무디자인 연구용역 | Hera + Apollo |
| P2026-004 | 나라장터 모니터링 웹앱 | Daedalus → Arachne/Talos |
| P2026-005 | 시앤피컨설팅 직업능력컨설팅본부 홈페이지 | Daedalus + Aphrodite |
| P2026-006 | 한국상하수도협회 직무분석 | Hera (job-analysis) |
| P2026-007 | 교육자료 개발 AI | Hera (HRD) + Daedalus |
| P2026-008 | KTR 훈련로드맵 | Hera (HRD) |
| P2026-009 | MBA Study | knowledge-management |
| P2026-010 | 국가데이터처 직업정보 프레임워크 연구 | Hera + Apollo |
| P2026-011 | 한기대 STEP 학습로드맵 및 신규과목 도출 | Hera (HRD) |
| P2026-012 | HRM 임금성과평가 | Hera (HRM) |

### 프로젝트 번호 체계 (명문화)

```
P{년도}-{일련번호}_{프로젝트명}

P0000-XXX = 영구·취미·메타 프로젝트 (연도 무관)
P{연도}-XXX = 해당 연도 업무 프로젝트 (P2026, P2027, ...)
```

---

## 2. 스킬 카탈로그

### Tier 1: 전역 스킬 (69개) — `~/.claude/skills/`

> 모든 프로젝트·디바이스에서 자동 로드. AI 도구/개발/콘텐츠 생성 중심.
> 전체 목록은 [`AI_TOOLS_MAP.md`](AI_TOOLS_MAP.md) 참조 — gstack 계열 (browse·codex·design-html·investigate·ship 등) 다수 포함.

### Tier 2: 워크스페이스 스킬 (25개) — `_core/skills/`

> 프로젝트 생성 시 `.claude/skills/` + `.agent/skills/`로 배포. 컨설팅 업무·문서 제작 중심.

| # | 스킬명 | 도메인 | 호출 에이전트 | 주요 용도 |
|---|--------|--------|---------------|-----------|
| 1 | consulting-report | 컨설팅 | Hermes | 컨설팅 보고서 작성 가이드 |
| 2 | job-analysis | 컨설팅 | Hera | NCS 기반 직무분석 프레임워크 |
| 3 | proposal | 컨설팅 | Hermes | 제안서/발표자료 작성 가이드 |
| 4 | data-analysis | 컨설팅 | Apollo·Midas | 설문분석, HR 데이터 분석 |
| 5 | hr-consulting | HR | Hera | HRM/HRD/OD 종합 프레임워크 |
| 6 | org-diagnosis | HR | Hera | 조직진단·조직설계·조직문화 |
| 7 | strategic-management | 경영 | Athena | 경영전략 수립·실행 (BSC/OKR) |
| 8 | business-planning | 사업 | Midas | PDCA 사업 기획·실행·보완 |
| 9 | **legal-consulting** | 법률 | **Themis** | 계약 검토, NDA, 노동법 (NEW) |
| 10 | **branding-marketing** | 브랜드 | **Aphrodite** | 네이밍, 브랜드 스토리텔링 (NEW) |
| 11 | knowledge-management | 학습 | (공통) | MBA/AI 학습·지식 축적 |
| 12 | pptx | 문서 | Hermes | PowerPoint 슬라이드 제작 |
| 13 | docx | 문서 | Hermes | Word 문서 제작 |
| 14 | pdf | 문서 | Hermes | PDF 처리/생성 |
| 15 | mermaid | 문서 | (공통) | 다이어그램/플로차트 |
| 16 | ppt-brand-guidelines | 문서 | Aphrodite | PPT 브랜드 가이드 |
| 17 | brand-guidelines | 문서 | Aphrodite | 전반 브랜드 가이드 |
| 18 | web-design-guidelines | 개발 | Daedalus | 웹 디자인 가이드 |
| 19 | fastapi-backend-guidelines | 개발 | Daedalus → Talos | FastAPI 백엔드 |
| 20 | nextjs-frontend-guidelines | 개발 | Daedalus → Arachne | Next.js 프론트엔드 |
| 21 | vercel-react-best-practices | 개발 | Daedalus → Helios | React 베스트 프랙티스 |
| 22 | pytest-backend-testing | 개발 | Daedalus → Nike | 백엔드 테스트 |
| 23 | error-tracking | 개발 | Daedalus | 에러 추적 |
| 24 | skill-developer | 메타 | (Pygmalion) | 새 스킬 개발 |
| 25 | workspace-management | 메타 | workspace-manager | 워크스페이스 관리 |

---

## 3. 에이전트 카탈로그 (21개) — `_core/agents/`

> **크로스도구**: `sync-tools.cmd` 실행 시 프로젝트의 `.claude/agents/` + `.agent/workflows/` 양쪽에 배포

### Tier 1: 비즈니스 오너 에이전트 — 그리스 신화 (9개)

> 사용자 요청 → 라우터 → 리드 에이전트 1명 지정 → 허용된 하위 스킬만 호출

| # | 에이전트 | 원형 | 도메인 | 활용 스킬 |
|---|----------|------|--------|----------|
| 1 | **athena** | 지혜의 여신 | 경영/사업/성장전략 | strategic-management, data-analysis |
| 2 | **apollo** | 지식의 신 | 시장조사·경쟁분석·벤치마킹 | data-analysis |
| 3 | **hera** | 조직의 여신 | HRM/HRD/OD·직무분석·조직진단 | job-analysis, hr-consulting, org-diagnosis |
| 4 | **hermes** | 전달의 신 | 문서 산출물 총괄·품질 통제 | consulting-report, proposal, pptx, docx, pdf |
| 5 | **themis** | 정의의 여신 | 법률검토·계약·규정 준수 | **legal-consulting** ✅ |
| 6 | **aphrodite** | 미의 여신 | 브랜딩·네이밍·마케팅 | **branding-marketing** ✅, brand-guidelines |
| 7 | **midas** | 황금의 손 | 사업계획·재무추정·BM설계 | business-planning, data-analysis |
| 8 | **daedalus** | 장인의 신 | 개발 총괄 아키텍트 | (하위) Arachne·Talos·Iris·Helios·Nike |
| 9 | **chronos** | 시간의 신 | 프로젝트 관리·WBS·일정 | workspace-management |

### Tier 2: 기술/개발 에이전트 (12개)

| # | 에이전트 | 역할 |
|---|----------|------|
| 10 | planner | 작업 계획 수립 |
| 11 | plan-reviewer | 계획 검토 |
| 12 | workspace-manager | 워크스페이스 관리 |
| 13 | auto-error-resolver | 에러 자동 해결 |
| 14 | code-architecture-reviewer | 코드 아키텍처 리뷰 |
| 15 | code-refactor-master | 코드 리팩토링 |
| 16 | documentation-architect | 문서화 설계 |
| 17 | frontend-error-fixer | 프론트엔드 에러 수정 |
| 18 | web-research-specialist | 웹 리서치 |
| 19 | auth-route-debugger | 인증 라우트 디버깅 |
| 20 | auth-route-tester | 인증 라우트 테스트 |
| 21 | refactor-planner | 리팩토링 계획 |

---

## 4. 워크플로우 카탈로그 (9개) — `_core/workflows/`

### Tier 1: 핵심 워크플로우 (자기진화·품질)

| # | 워크플로우 | 역할 | 트리거 |
|---|-----------|------|--------|
| 1 | **ralph-loop** | 품질 검증 루프 | 모든 산출물 (초안→Momus검증→수정→확정) |
| 2 | **pygmalion** | 자기진화 워크플로우 | 분기 1회 (관찰→패턴→개선→시험→승격) |

### Tier 2: 레거시 Antigravity 워크플로우 (7개)

> 그리스신화 에이전트로 점진 이관 중. 신규 업무는 에이전트 우선 사용.

| # | 워크플로우 | 대체 에이전트 |
|---|-----------|---------------|
| 3 | agent-01-legal | → **Themis** |
| 4 | agent-02-hr | → **Hera** |
| 5 | agent-03-job-carving | (P2026-001 전용 유지) |
| 6 | agent-04-bm | → **Midas** |
| 7 | agent-05-research | → **Apollo** |
| 8 | agent-06-branding | → **Aphrodite** |
| 9 | agent-07-cso | → **Athena** + **Midas** |

---

## 5. 품질계약 (`_core/quality-contracts/`)

| # | 문서 | 역할 |
|---|------|------|
| 1 | **QUALITY_CONTRACT.md** | 산출물 유형별 품질 기준 + 등급 체계(A/B/C) |

> Ralph 루프와 연동: 모든 산출물은 품질계약 기준에 따라 자동 등급 부여, 등급 누적 분석으로 진화.

---

## 6. 커맨드·플러그인·프롬프트

### 커맨드
| 위치 | 적용 범위 | 내용 |
|------|-----------|------|
| `~/.claude/commands/` | 유저 전역 | narajan-webapp 등 |
| `_core/commands/` | 워크스페이스 | dev-docs, route-research |

### 플러그인 (`~/.claude/plugins/`)
| 플러그인 | 용도 |
|----------|------|
| mckinsey-pptx | 맥킨지 스타일 PPTX 자동 생성 |
| oh-my-claudecode | OMC 멀티에이전트 오케스트레이션 |

### MCP 서버 (Claude Code/Desktop)
| MCP | 용도 |
|-----|------|
| hwp-mcp | 한글(HWP) 문서 처리 (Code/Desktop만, Cowork 제외) |
| notion | Notion DB·페이지·검색 연동 |
| figma | 디자인 ↔ 코드 양방향 |
| (외) | 다수 — 세션 시작 시 자동 로드 |

### 프롬프트 라이브러리 (`_core/prompts/`)
| 폴더 | 대상 도구 | 내용 |
|------|-----------|------|
| `common/` | 전 도구 | role-hr-consultant, role-business-planner, tone-consulting |
| `claude-web/` | Claude Web Projects | hr-consulting-project, business-development-project |
| `cowork/` | Claude Desktop (Cowork) | general-assistant |

---

## 7. 업무 도메인별 매핑

### HR 컨설팅
| 업무 | 리드 | 스킬 | 품질검증 |
|------|------|------|---------|
| 직무분석 | Hera | job-analysis, data-analysis | Ralph |
| 조직진단 | Hera | org-diagnosis, data-analysis | Ralph |
| 인사제도 설계 | Hera | hr-consulting | Ralph |
| HR 보고서 작성 | Hermes | consulting-report, pptx, docx | Ralph |

### 경영전략·사업개발
| 업무 | 리드 | 스킬 | 품질검증 |
|------|------|------|---------|
| 전략 수립 | Athena | strategic-management | Ralph |
| 시장조사/경쟁분석 | Apollo | data-analysis | Ralph |
| 사업계획서 | Midas | business-planning, data-analysis | Ralph |
| 재무추정 | Midas | data-analysis | Ralph |
| 제안서 작성 | Hermes | proposal, pptx | Ralph |

### 법률·브랜드
| 업무 | 리드 | 스킬 | 품질검증 |
|------|------|------|---------|
| 계약·NDA 검토 | **Themis** | **legal-consulting** | Ralph |
| 노동법·HR 규정 | **Themis** | **legal-consulting** | Ralph |
| 네이밍·브랜드 | **Aphrodite** | **branding-marketing** | Ralph |
| 마케팅 카피 | **Aphrodite** | **branding-marketing** | Ralph |

### 웹/앱 개발
| 업무 | 리드 | 하위 | 스킬 |
|------|------|------|------|
| 프론트엔드 | Daedalus | Arachne | nextjs-frontend-guidelines |
| 백엔드 | Daedalus | Talos | fastapi-backend-guidelines |
| 인프라 | Daedalus | Helios | vercel-react-best-practices |
| 테스트 | Daedalus | Nike | pytest-backend-testing |

### 프로젝트 관리·학습
| 업무 | 리드 | 도구 |
|------|------|------|
| 일정·리스크 | Chronos | WBS, 간트, 리스크 매트릭스 |
| 학습 노트 | (공통) | knowledge-management |
| 워크스페이스 관리 | workspace-manager | workspace-management 스킬 |

---

## 8. 관리·진화 규칙

### 변경 시 즉시 갱신할 문서
| 변경 종류 | 갱신 대상 |
|----------|----------|
| 스킬 추가/제거 | REGISTRY.md, AI_TOOLS_MAP.md |
| 에이전트 추가/제거 | REGISTRY.md, AI_TOOLS_MAP.md, CLAUDE.md (라우팅표) |
| 프로젝트 생성/완료 | REGISTRY.md (활성 목록), WORKSPACE_GUIDE.md |
| 디바이스 환경 변경 | MULTI_DEVICE_GUIDE.md, DEVICE_PARITY_CHECKLIST.md |

### 정기 점검 (자기진화 루프)
| 주기 | 작업 | 워크플로우 |
|------|------|-----------|
| 매 산출물 | 품질 검증·등급 부여 | **Ralph** |
| 매주 (월요일) | 신규 패턴/스킬 후보 수집 | 사용자 검토 |
| 매월 (말일) | 가이드 정합성 점검 (문서 vs 실제) | workspace-manager |
| 매분기 (3·6·9·12월) | 리소스 진화 사이클 | **Pygmalion** |
| 연 1회 | archive/ 외부 백업 | 사용자 |

상세: [`SYSTEM_EVOLUTION_LOOP.md`](SYSTEM_EVOLUTION_LOOP.md)

---

## 9. 참조 문서

- 운영 가이드: [`../WORKSPACE_GUIDE.md`](../WORKSPACE_GUIDE.md)
- 도구 설정 맵: [`AI_TOOLS_MAP.md`](AI_TOOLS_MAP.md)
- 멀티디바이스: [`../MULTI_DEVICE_GUIDE.md`](../MULTI_DEVICE_GUIDE.md)
- 디바이스 패리티: [`../DEVICE_PARITY_CHECKLIST.md`](../DEVICE_PARITY_CHECKLIST.md)
- 자기진화 루프: [`SYSTEM_EVOLUTION_LOOP.md`](SYSTEM_EVOLUTION_LOOP.md)
- 전역 컨텍스트: [`../CLAUDE.md`](../CLAUDE.md)
