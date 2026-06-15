# AI 도구 설정 맵

> 이석주의 AI 작업 환경에서 사용하는 모든 도구와 설정 파일의 위치를 정리한 문서입니다.
>
> **최종 업데이트**: 2026-05-28

---

## 1. 도구별 설정 위치

### Claude Code (CLI, 주력 도구)

| 경로 | 용도 | 수정 가능 | 비고 |
|------|------|-----------|------|
| `~/.claude.json` | 전역 설정 (API, 인증) | ⚠️ 주의 | 삭제 금지 |
| `~/.claude/settings.json` | 유저 레벨 설정 | ✅ | MCP 서버, 허용 도구 |
| `~/.claude/skills/` | **Tier 1 전역 스킬 (69개)** | ✅ | 모든 프로젝트에서 자동 로드 |
| `~/.claude/agents/` | 유저 레벨 서브에이전트 | ✅ | (있는 경우) |
| `~/.claude/commands/` | 유저 레벨 커맨드 | ✅ | 슬래시 명령어 |
| `~/.claude/plugins/` | 플러그인 (mckinsey-pptx, omc) | ✅ | |
| `~/.claude/plans/` | 작업 계획 저장 | 자동 | |
| `~/.claude/cache/` | 캐시 | 삭제 가능 | 월 1회 정리 |
| `~/.claude/projects/{프로젝트id}/memory/` | 자동 메모리 | 자동 | 영구 컨텍스트 |
| `~/.claude.json` | 전역 설정 (API) | ⚠️ | 삭제 금지 |

**프로젝트 레벨:**
| 경로 | 용도 |
|------|------|
| `프로젝트/.claude/settings.json` | 프로젝트별 Claude 설정 |
| `프로젝트/.claude/skills/` | Tier 2 배포 스킬 |
| `프로젝트/.claude/agents/` | Tier 2 배포 에이전트 |
| `프로젝트/.claude/commands/` | 프로젝트 전용 명령어 |
| `프로젝트/CLAUDE.md` | AI가 최초 읽는 프로젝트 컨텍스트 |

### Claude Desktop (Cowork — 채팅 인터페이스)

| 경로 | 용도 |
|------|------|
| `~/AppData/Roaming/Claude/` | Cowork 앱 설정·MCP·시스템 프롬프트 |
| 시스템 프롬프트 | `_core/prompts/cowork/general-assistant.md` 사용 |

### Claude Web (Projects 기능 — 핸드폰·브라우저)

| 위치 | 용도 |
|------|------|
| claude.ai/projects | 프로젝트 인스트럭션 (시스템 프롬프트) |
| 소스 프롬프트 | `_core/prompts/claude-web/` 폴더 |

### 외부 AI 도구

| 도구 | 설정 경로 | 비고 |
|------|----------|------|
| Gemini | `~/.gemini/GEMINI.md` | CLAUDE.md와 동일 역할 |
| Antigravity | `~/.antigravity/` + 프로젝트 `.agent/` | skills/, workflows/ 포함 |
| GitHub Copilot | `~/.copilot/` | |
| VS Code | `~/.vscode/` | |

---

## 2. 스킬 관리 체계 (2-Tier)

### 구조

```
Tier 1: 유저 레벨 스킬 (전역, 69개)
  위치: ~/.claude/skills/
  적용: 모든 프로젝트·모든 디바이스에서 자동 로드
  성격: AI 도구·개발·콘텐츠 생성·범용 워크플로우
  대표: gstack 계열, codex, design-html, investigate, ship,
        card-news-generator, nextjs15-init, frontend-design 등

Tier 2: 워크스페이스 스킬 (프로젝트 배포, 25개)
  위치: _core/skills/
  적용: sync-tools.cmd 실행 시 프로젝트 .claude/skills/로 복사
  성격: 컨설팅 업무·문서 제작·HR/경영 도메인
  대표: hr-consulting, business-planning, job-analysis,
        consulting-report, proposal, legal-consulting,
        branding-marketing, pptx, docx 등
```

### 신규 스킬 판단 기준

```
Q: 모든 프로젝트(또는 비-컨설팅 프로젝트 포함)에서 항상 필요한가?
  YES → Tier 1: ~/.claude/skills/
  NO  → Tier 2: _core/skills/

Q: 컨설팅 업무 전용인가, AI/개발 범용인가?
  컨설팅 → Tier 2
  AI/개발 → Tier 1
```

### Tier 2 스킬 전체 (25개)

| 카테고리 | 스킬 |
|----------|------|
| **컨설팅 핵심** | consulting-report, proposal, job-analysis, data-analysis |
| **HR/경영** | hr-consulting, org-diagnosis, strategic-management, business-planning |
| **법률·브랜드 (NEW)** | **legal-consulting** ✅, **branding-marketing** ✅ |
| **학습** | knowledge-management |
| **문서** | pptx, docx, pdf, mermaid, brand-guidelines, ppt-brand-guidelines |
| **개발** | web-design-guidelines, fastapi-backend-guidelines, nextjs-frontend-guidelines, vercel-react-best-practices, pytest-backend-testing, error-tracking |
| **메타** | skill-developer, workspace-management |

---

## 3. 에이전트 관리 체계 (21개)

### Tier 1: 그리스 신화 비즈니스 에이전트 (9개)

> 사용자 요청을 받아 적절한 영역의 작업을 수행하는 도메인 오너.
> **사용자가 한국어로 말하면 → AI가 라우팅 → 리드 에이전트 1명 지정**

| 에이전트 | 그리스 원형 | 영역 | 트리거 한국어 |
|----------|-----------|------|---------------|
| **Athena** | 지혜의 여신 | 경영/전략 | "전략 수립", "사업 방향" |
| **Apollo** | 지식의 신 | 시장조사 | "시장조사", "경쟁분석" |
| **Hera** | 조직의 여신 | HR/조직 | "직무분석", "조직진단", "인사제도" |
| **Hermes** | 전달의 신 | 문서/품질 | "보고서", "제안서", "발표자료" |
| **Themis** ✅ | 정의의 여신 | 법률 | "법률 검토", "계약 검토", "NDA" |
| **Aphrodite** ✅ | 미의 여신 | 브랜드 | "브랜딩", "네이밍", "마케팅 카피" |
| **Midas** | 황금의 손 | 사업/재무 | "사업계획", "재무 추정", "BM" |
| **Daedalus** | 장인의 신 | 개발 총괄 | "웹사이트", "앱", "백엔드" |
| **Chronos** | 시간의 신 | 프로젝트 관리 | "프로젝트 현황", "일정 관리" |

### Daedalus 하위 (전문 개발 에이전트)

| 하위 에이전트 | 역할 |
|---------------|------|
| Arachne | 프론트엔드 (Next.js·React) |
| Talos | 백엔드 (FastAPI·Node) |
| Iris | 모바일 (Flutter) |
| Helios | 인프라·배포 (Vercel·클라우드) |
| Nike | QA·테스트 |

### Tier 2: 기술/개발 레거시 에이전트 (12개)

| 에이전트 | 역할 |
|----------|------|
| planner | 작업 계획 수립 |
| plan-reviewer | 계획 검토 |
| workspace-manager | 워크스페이스 관리 |
| auto-error-resolver | 에러 자동 해결 |
| code-architecture-reviewer | 아키텍처 리뷰 |
| code-refactor-master | 코드 리팩토링 |
| documentation-architect | 문서화 설계 |
| frontend-error-fixer | 프론트엔드 에러 |
| web-research-specialist | 웹 리서치 |
| auth-route-debugger | 인증 디버깅 |
| auth-route-tester | 인증 테스트 |
| refactor-planner | 리팩토링 계획 |

---

## 4. 워크플로우 (9개) — `_core/workflows/`

### 핵심 (2개)
| 워크플로우 | 용도 | 트리거 |
|-----------|------|--------|
| **ralph-loop** | 품질 검증 루프 | 모든 산출물 |
| **pygmalion** | 자기진화 사이클 | 분기 1회 |

### 레거시 Antigravity (7개) — 그리스신화 에이전트로 점진 이관
| 워크플로우 | 대체 에이전트 |
|-----------|---------------|
| agent-01-legal | Themis |
| agent-02-hr | Hera |
| agent-03-job-carving | (P2026-001 전용 유지) |
| agent-04-bm | Midas |
| agent-05-research | Apollo |
| agent-06-branding | Aphrodite |
| agent-07-cso | Athena + Midas |

---

## 5. 플러그인·MCP·커맨드

### Claude Code 플러그인 (`~/.claude/plugins/`)
| 플러그인 | 용도 |
|----------|------|
| **mckinsey-pptx** | 맥킨지 스타일 PPTX 자동 생성 |
| **oh-my-claudecode** | 멀티에이전트 오케스트레이션 (`/team`, `/ultrawork` 등) |

### MCP 서버 (양 PC 동일하게 유지)
| MCP | 도구 | 용도 |
|-----|------|------|
| **hwp-mcp** | Claude Code + Desktop | 한글(.hwp) 문서 처리 |
| **notion** | Code + Desktop | Notion DB·페이지 |
| **figma** | Code | 디자인 ↔ 코드 |
| (기타) | 자동 로드 | 세션 시작 시 표시됨 |

### 커맨드
| 위치 | 적용 |
|------|------|
| `~/.claude/commands/` | 유저 전역 |
| `_core/commands/` | 워크스페이스 |

---

## 6. 프롬프트 라이브러리 (`_core/prompts/`)

| 폴더 | 대상 도구 | 파일 | 용도 |
|------|----------|------|------|
| `common/` | 전 도구 | role-hr-consultant.md | HR 컨설턴트 역할 |
| `common/` | 전 도구 | role-business-planner.md | 사업기획 전문가 역할 |
| `common/` | 전 도구 | tone-consulting.md | 컨설팅 톤·스타일 |
| `claude-web/` | Claude Web Projects | hr-consulting-project.md | HR 컨설팅 (모바일) |
| `claude-web/` | Claude Web Projects | business-development-project.md | 사업개발 (모바일) |
| `cowork/` | Claude Desktop | general-assistant.md | 범용 업무 보조 |

**사용법:**
- **Claude Web (핸드폰·브라우저)**: Projects → `claude-web/` 파일을 인스트럭션에 복사
- **Claude Desktop**: 설정 → `cowork/` 파일을 시스템 프롬프트로
- **Claude Code**: `common/` 역할·톤을 프로젝트 CLAUDE.md에 참조

---

## 7. 관리 원칙

### Single Source of Truth

```
스킬:
  Tier 1 원본 → ~/.claude/skills/        (양 PC 동기화 — backup-user-settings.cmd)
  Tier 2 원본 → _core/skills/             (OneDrive 자동 동기화)

에이전트·워크플로우:
  원본 → _core/agents/ + _core/workflows/  (OneDrive 자동 동기화)
  배포 → 프로젝트 .claude/agents/ + .agent/workflows/ (sync-tools.cmd)
```

### 금지 사항
- ❌ 홈 디렉토리에서 직접 AI 도구 실행 (프로젝트 폴더로 이동 후 실행)
- ❌ `~/.claude.json` 직접 수정·삭제
- ❌ AI 설정 폴더(`.claude/`, `.agent/`)를 OneDrive에 저장 — junction으로 분리
- ❌ 민감 정보(API 키, 토큰)를 프로젝트 폴더에 저장

### 정기 관리

| 주기 | 작업 | 워크플로우 |
|------|------|-----------|
| 매 산출물 | 품질 등급 부여 | Ralph |
| 매주 월요일 | 신규 패턴 후보 수집 | 사용자 |
| 매월 말일 | 가이드 vs 실제 정합성 점검 | workspace-manager |
| 매분기 | Pygmalion 진화 사이클 | Pygmalion |
| 연 1회 | archive/ 외부 백업 | 사용자 |

상세: [`../SYSTEM_EVOLUTION_LOOP.md`](../SYSTEM_EVOLUTION_LOOP.md)

---

## 8. 디바이스 패리티 (노트북 = 데스크탑)

| 항목 | 양 PC 동일 보장 방법 |
|------|--------------------|
| Tier 1 스킬 69개 | `backup-user-settings.cmd`로 백업 → 다른 PC에서 복원 |
| settings.json | 백업·복원 (또는 양쪽 동일하게 수동 편집) |
| MCP 서버 | settings.json에 동일하게 등록 |
| 플러그인 (mckinsey-pptx, omc) | 백업·복원 또는 양쪽 동일 설치 |
| OMC 버전 | `omc update` 양쪽에서 |
| 인증 (Anthropic) | 양쪽 각각 `claude` 실행 후 로그인 |

체크리스트: [`../DEVICE_PARITY_CHECKLIST.md`](../DEVICE_PARITY_CHECKLIST.md)
