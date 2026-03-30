# AI 도구 설정 맵

> 이석주의 AI 작업 환경에서 사용하는 모든 도구와 설정 파일의 위치를 정리한 문서입니다.
> 
> 최종 업데이트: 2026-03-19

---

## 1. 도구별 설정 위치

### Claude Code (OhMyClaudeCode / OpenCode)

| 경로 | 용도 | 수정 가능 | 비고 |
|------|------|-----------|------|
| `~/.claude.json` | 전역 설정 (API, 인증) | ⚠️ 주의 | 삭제 금지 |
| `~/.claude/settings.json` | 유저 레벨 설정 | ✅ | MCP 서버, 허용 도구 |
| `~/.claude/skills/` | **유저 레벨 스킬 (22개)** | ✅ | 모든 프로젝트에서 자동 로드 |
| `~/.claude/commands/` | 유저 레벨 커맨드 | ✅ | 슬래시 명령어 |
| `~/.claude/plugins/` | 플러그인 관리 | ✅ | Notion, skill-creator 등 |
| `~/.claude/plans/` | 작업 계획 저장 | 자동 | Sisyphus 계획 파일 |
| `~/.claude/cache/` | 캐시 | 삭제 가능 | 월 1회 정리 권장 |
| `~/.claude/debug/` | 디버그 로그 | 삭제 가능 | 문제 해결 후 정리 |
| `~/.claude/downloads/` | 다운로드 | 삭제 가능 | |
| `~/.claude/history.jsonl` | 대화 이력 | 자동 | |
| `~/.claude/todos/` | 할 일 목록 | 자동 | |
| `~/.claude/transcripts/` | 세션 기록 | 자동 | |

**프로젝트 레벨:**

| 경로 | 용도 |
|------|------|
| `프로젝트/.claude/settings.json` | 프로젝트별 Claude 설정 |
| `프로젝트/.claude/skills/` | 프로젝트 전용 스킬 |
| `프로젝트/.claude/commands/` | 프로젝트 전용 명령어 |
| `프로젝트/CLAUDE.md` | AI가 최초 읽는 프로젝트 컨텍스트 |

### OpenCode 런타임

| 경로 | 용도 | 비고 |
|------|------|------|
| `~/.opencode/` | OhMyClaudeCode 실행 파일 | node_modules 포함, 건드리지 않기 |
| `~/.config/opencode/` | OpenCode 설정 | |

### Gemini

| 경로 | 용도 | 비고 |
|------|------|------|
| `~/.gemini/GEMINI.md` | Gemini 전역 컨텍스트 | CLAUDE.md와 동일 역할 |
| `~/.gemini/antigravity/` | Gemini-Antigravity 연동 설정 | |

### Antigravity

| 경로 | 용도 | 비고 |
|------|------|------|
| `~/.antigravity/` | Antigravity 앱 설정 | argv.json, extensions/ |
| 프로젝트 내 `.agent/` | 프로젝트별 Antigravity 설정 | skills/, workflows/ 포함 |

### Copilot / VS Code

| 경로 | 용도 | 비고 |
|------|------|------|
| `~/.copilot/` | GitHub Copilot 설정 | |
| `~/.vscode/` | VS Code 전역 설정 | |

---

## 2. 스킬 관리 체계

### 스킬 저장소 구조 (2-Tier)

```
Tier 1: 유저 레벨 스킬 (전역)
  위치: ~/.claude/skills/
  적용: 모든 프로젝트에서 자동 로드
  성격: AI 도구/개발/콘텐츠 생성

Tier 2: 워크스페이스 레벨 스킬 (프로젝트용)
  위치: workspace/_shared/skills/
  적용: 프로젝트 생성 시 복사/심링크로 배포
  성격: 컨설팅 업무/문서 제작
```

### Tier 1: 유저 레벨 스킬 (22개)

| 스킬명 | 카테고리 | 용도 |
|--------|----------|------|
| card-news-generator | 콘텐츠 | 인스타그램 카드뉴스 생성 |
| card-news-generator-v2 | 콘텐츠 | 카드뉴스 v2 (배경이미지 지원) |
| midjourney-cardnews-bg | 콘텐츠 | Midjourney 배경 프롬프트 |
| code-changelog | 개발 | 코드 변경 기록 HTML 뷰어 |
| code-prompt-coach | 개발 | 프롬프트 품질 분석 |
| codex | 개발 | OpenAI Codex CLI |
| codex-claude-loop | 개발 | Claude+Codex 듀얼 루프 |
| codex-claude-cursor-loop | 개발 | Claude+Codex+Cursor 트리플 루프 |
| design-prompt-generator-v2 | 디자인 | AI 웹빌더용 프롬프트 생성 |
| flutter-init | 개발 | Flutter 프로젝트 초기 셋업 |
| frontend-design | 개발 | 프로덕션 프론트엔드 UI |
| gemini-logo-remover | 유틸 | 이미지 워터마크 제거 |
| landing-page-guide | 개발 | 랜딩페이지 가이드 |
| landing-page-guide-v2 | 개발 | 랜딩페이지 v2 (디자인 강화) |
| meta-prompt-generator | 프롬프트 | 슬래시 커맨드 자동 생성 |
| nextjs15-init | 개발 | Next.js 15 프로젝트 초기 셋업 |
| prompt-enhancer | 프롬프트 | 프로젝트 맥락 기반 프롬프트 보강 |
| web-search | 유틸 | DuckDuckGo 웹 검색 |
| web-to-markdown | 유틸 | 웹페이지 마크다운 변환 |
| workthrough | 문서화 | 작업 기록 문서화 |
| workthrough-v2 | 문서화 | 작업 기록 v2 |

### Tier 2: 워크스페이스 레벨 스킬 (18개)

| 스킬명 | 카테고리 | 용도 |
|--------|----------|------|
| consulting-report | 컨설팅 | 컨설팅 보고서 작성 가이드 |
| job-analysis | 컨설팅 | NCS 기반 직무분석 |
| proposal | 컨설팅 | 제안서/발표자료 작성 |
| data-analysis | 컨설팅 | 설문분석, HR 데이터 분석 |
| pptx | 문서 | PowerPoint 슬라이드 제작 |
| docx | 문서 | Word 문서 제작 |
| pdf | 문서 | PDF 처리/생성 |
| mermaid | 문서 | 다이어그램/플로차트 |
| ppt-brand-guidelines | 문서 | PPT 브랜드 가이드라인 |
| brand-guidelines | 문서 | 전반적 브랜드 가이드라인 |
| web-design-guidelines | 개발 | 웹 디자인 가이드 |
| fastapi-backend-guidelines | 개발 | FastAPI 백엔드 |
| nextjs-frontend-guidelines | 개발 | Next.js 프론트엔드 |
| vercel-react-best-practices | 개발 | React 베스트 프랙티스 |
| pytest-backend-testing | 개발 | 백엔드 테스트 |
| error-tracking | 개발 | 에러 추적 |
| skill-developer | 메타 | 새 스킬 개발 |
| workspace-management | 메타 | 워크스페이스 관리 |

### 중복 스킬

| 스킬명 | Tier 1 | Tier 2 | 권장 조치 |
|--------|--------|--------|-----------|
| frontend-design | ✅ | ✅ | Tier 1(유저)을 원본으로, Tier 2에서 제거 |

---

## 3. 에이전트 관리 체계

### 에이전트 저장소 (크로스도구 교차 배포)

| 위치 | 내용 | 배포 대상 |
|------|------|-----------|
| `workspace/_shared/agents/` | **에이전트 (12개)** 원본 | → `.claude/agents/` + `.agent/workflows/` |
| `workspace/_shared/workflows/` | **워크플로우 (7개)** 원본 | → `.agent/workflows/` + `.claude/agents/` |

**교차 배포 결과**: 프로젝트 내 `.claude/agents/`에 19개, `.agent/workflows/`에 19개
→ Claude Code, OpenCode, Antigravity 어디서든 모든 에이전트/워크플로우 사용 가능
| ~~`~/.agents/workflows/`~~ | ~~중복본~~ | ✅ 삭제 완료 (2026-03-19) |
| ~~`~/.agents/agents.md-main/`~~ | ~~Next.js 프로젝트~~ | ✅ archive/로 이관 완료 |
| ~~`~/.agents/oh-my-openagent-dev/`~~ | ~~개발 프로젝트~~ | ✅ archive/로 이관 완료 |

### Claude Code 에이전트 (12개)

| 에이전트 | 용도 |
|----------|------|
| planner | 작업 계획 수립 |
| plan-reviewer | 계획 검토 |
| auto-error-resolver | 에러 자동 해결 |
| code-architecture-reviewer | 코드 아키텍처 리뷰 |
| code-refactor-master | 코드 리팩토링 |
| documentation-architect | 문서화 설계 |
| frontend-error-fixer | 프론트엔드 에러 수정 |
| web-research-specialist | 웹 리서치 |
| auth-route-debugger | 인증 라우트 디버깅 |
| auth-route-tester | 인증 라우트 테스트 |
| refactor-planner | 리팩토링 계획 |
| workspace-manager | 워크스페이스 관리 |

### Antigravity 워크플로우 (7개)

| 워크플로우 | 용도 |
|------------|------|
| agent-01-legal | 법률/구조 설계 자문 |
| agent-02-hr | HR/인사노무 진단 |
| agent-03-job-carving | 장애인 직무개발 |
| agent-04-bm | 비즈니스 모델/재무 추정 |
| agent-05-research | 시장 리서치/경쟁 분석 |
| agent-06-branding | 브랜딩/네이밍/스토리텔링 |
| agent-07-cso | 총괄 관리/사업계획서 |

---

## 4. 플러그인

| 위치 | 도구 | 비고 |
|------|------|------|
| `~/.claude/plugins/` | Claude Code 플러그인 | Notion, skill-creator 등 |

---

## 5. 커맨드

| 위치 | 적용 범위 | 내용 |
|------|-----------|------|
| `~/.claude/commands/` | 유저 레벨 (전역) | narajan-webapp.md |
| `workspace/_shared/commands/` | 워크스페이스 레벨 | dev-docs.md, dev-docs-update.md, route-research-for-testing.md |

---

## 6. 프롬프트 라이브러리 — `workspace/_shared/prompts/`

| 폴더 | 대상 도구 | 파일 | 용도 |
|------|-----------|------|------|
| `common/` | 모든 도구 | role-hr-consultant.md | HR 컨설턴트 역할 정의 |
| `common/` | 모든 도구 | role-business-planner.md | 사업기획 전문가 역할 정의 |
| `common/` | 모든 도구 | tone-consulting.md | 컨설팅 문서 톤/스타일 가이드 |
| `claude-web/` | Claude Web | hr-consulting-project.md | HR 컨설팅 프로젝트 지침 |
| `claude-web/` | Claude Web | business-development-project.md | 사업개발 프로젝트 지침 |
| `cowork/` | Claude Desktop | general-assistant.md | 범용 업무 보조 지침 |

**사용법:**
- **Claude Web**: Projects 기능에서 `claude-web/` 내 파일을 시스템 지침으로 복사
- **Claude Desktop**: 설정에서 `cowork/` 내 파일을 시스템 프롬프트로 설정
- **Claude Code/OpenCode**: `common/` 내 역할/톤 파일을 CLAUDE.md에 참조

---

## 7. 관리 원칙

### Single Source of Truth (진실의 원천)

```
스킬:
  Tier 1 원본 → ~/.claude/skills/           (AI 도구/개발용, 전역 자동 로드)
  Tier 2 원본 → workspace/_shared/skills/   (컨설팅 업무용, 프로젝트 배포)

에이전트:
  원본 → workspace/_shared/agents/          (Claude Code 에이전트)
  원본 → workspace/_shared/workflows/       (Antigravity 워크플로우)

프로젝트:
  활성 → workspace/projects/
  완료 → workspace/archive/
  산출물 → workspace/outputs/
```

### 금지 사항

- ❌ 홈 디렉토리에서 직접 AI 도구 실행 (프로젝트 폴더로 이동 후 실행)
- ❌ `~/.claude.json` 직접 수정/삭제
- ❌ `~/.opencode/` 내부 수정
- ❌ AI 설정 폴더(.claude/, .agent/)를 OneDrive에 저장
- ❌ 민감 정보(API 키, 토큰)를 프로젝트 폴더에 저장

### 정기 관리

| 주기 | 작업 |
|------|------|
| 수시 | 프로젝트 완료 시 archive/ 이관 |
| 월 1회 | `~/.claude/cache/`, `~/.claude/debug/` 정리 |
| 분기 1회 | 스킬/에이전트 목록 최신화, 미사용 스킬 정리 |
| 연 1회 | archive/ 오래된 프로젝트 외부 백업 |

---

## 7. 정리 필요 항목

### 즉시 조치 권장

| 항목 | 현재 위치 | 권장 조치 |
|------|-----------|-----------|
| ~~agents.md-main~~ | ~~`~/.agents/agents.md-main/`~~ | ✅ `workspace/archive/`로 이관 완료 (2026-03-19) |
| ~~oh-my-openagent-dev~~ | ~~`~/.agents/oh-my-openagent-dev/`~~ | ✅ `workspace/archive/`로 이관 완료 (2026-03-19) |
| ~~workflows 중복본~~ | ~~`~/.agents/workflows/`~~ | ✅ 삭제 완료 (2026-03-19) |
| ~~frontend-design 중복~~ | ~~`workspace/_shared/skills/frontend-design/`~~ | ✅ 삭제 완료 (2026-03-19) |
| ~~nul 파일~~ | ~~`~/nul`~~ | ✅ 삭제 완료 (2026-03-19) |
| ~~AI_도구_폴더관리_가이드.md~~ | ~~`workspace/_shared/`~~ | ✅ 삭제 완료 — AI_TOOLS_MAP.md로 대체 |
