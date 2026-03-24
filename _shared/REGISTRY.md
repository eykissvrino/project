# AI 리소스 마스터 레지스트리

> 이석주의 AI 작업 환경에서 사용 가능한 모든 스킬, 에이전트, 워크플로우, 커맨드, 플러그인의 통합 카탈로그입니다.
>
> 최종 업데이트: 2026-03-19

---

## 빠른 참조

| 리소스 유형 | 수량 | 위치 |
|-------------|------|------|
| Tier 1 스킬 (전역) | 22개 | `~/.claude/skills/` |
| Tier 2 스킬 (워크스페이스) | 23개 | `workspace/_shared/skills/` |
| 에이전트 | 12개 | `workspace/_shared/agents/` |
| 워크플로우 | 7개 | `workspace/_shared/workflows/` |
| 커맨드 | 4개 | `~/.claude/commands/` + `_shared/commands/` |
| 플러그인 | 2개 | `~/.claude/plugins/` |
| 프롬프트 | - | `workspace/_shared/prompts/` |
| **합계** | **70+** | |

---

## 1. 스킬 카탈로그

### Tier 1: 전역 스킬 (22개) — `~/.claude/skills/`

> 모든 프로젝트에서 자동 로드. AI 도구/개발/콘텐츠 생성 중심.

| # | 스킬명 | 도메인 | 용도 | 도구 호환 |
|---|--------|--------|------|-----------|
| 1 | card-news-generator | 콘텐츠 | 인스타그램 카드뉴스 생성 | CC, OC |
| 2 | card-news-generator-v2 | 콘텐츠 | 카드뉴스 v2 (배경이미지 지원) | CC, OC |
| 3 | midjourney-cardnews-bg | 콘텐츠 | Midjourney 배경 프롬프트 | CC, OC |
| 4 | code-changelog | 개발 | 코드 변경 기록 HTML 뷰어 | CC, OC |
| 5 | code-prompt-coach | 개발 | 프롬프트 품질 분석/코칭 | CC, OC |
| 6 | codex | 개발 | OpenAI Codex CLI 연동 | CC, OC |
| 7 | codex-claude-loop | 개발 | Claude+Codex 듀얼 루프 | CC, OC |
| 8 | codex-claude-cursor-loop | 개발 | Claude+Codex+Cursor 트리플 루프 | CC, OC |
| 9 | design-prompt-generator-v2 | 디자인 | AI 웹빌더용 프롬프트 생성 | CC, OC |
| 10 | flutter-init | 개발 | Flutter 프로젝트 초기 셋업 | CC, OC |
| 11 | frontend-design | 개발 | 프로덕션 프론트엔드 UI | CC, OC |
| 12 | gemini-logo-remover | 유틸 | 이미지 워터마크 제거 | CC, OC |
| 13 | landing-page-guide | 개발 | 랜딩페이지 가이드 | CC, OC |
| 14 | landing-page-guide-v2 | 개발 | 랜딩페이지 v2 (디자인 강화) | CC, OC |
| 15 | meta-prompt-generator | 프롬프트 | 슬래시 커맨드 자동 생성 | CC, OC |
| 16 | nextjs15-init | 개발 | Next.js 15 프로젝트 초기 셋업 | CC, OC |
| 17 | prompt-enhancer | 프롬프트 | 프로젝트 맥락 기반 프롬프트 보강 | CC, OC |
| 18 | web-search | 유틸 | DuckDuckGo 웹 검색 | CC, OC |
| 19 | web-to-markdown | 유틸 | 웹페이지 마크다운 변환 | CC, OC |
| 20 | workthrough | 문서화 | 작업 기록 문서화 | CC, OC |
| 21 | workthrough-v2 | 문서화 | 작업 기록 v2 | CC, OC |
| 22 | (예비) | - | ~/.agents/skills/ 경로 예비 | OC |

> CC = Claude Code, OC = OpenCode

### Tier 2: 워크스페이스 스킬 (18개) — `workspace/_shared/skills/`

> 프로젝트 생성 시 배포. 컨설팅 업무/문서 제작 중심.

| # | 스킬명 | 도메인 | 용도 | 프로젝트 배포 |
|---|--------|--------|------|---------------|
| 1 | consulting-report | 컨설팅 | 컨설팅 보고서 작성 가이드 | .claude/ + .agent/ |
| 2 | job-analysis | 컨설팅 | NCS 기반 직무분석 프레임워크 | .claude/ + .agent/ |
| 3 | proposal | 컨설팅 | 제안서/발표자료 작성 가이드 | .claude/ + .agent/ |
| 4 | data-analysis | 컨설팅 | 설문분석, HR 데이터 분석 | .claude/ + .agent/ |
| 5 | pptx | 문서 | PowerPoint 슬라이드 제작 | .claude/ + .agent/ |
| 6 | docx | 문서 | Word 문서 제작 | .claude/ + .agent/ |
| 7 | pdf | 문서 | PDF 처리/생성 | .claude/ + .agent/ |
| 8 | mermaid | 문서 | 다이어그램/플로차트 | .claude/ + .agent/ |
| 9 | ppt-brand-guidelines | 문서 | PPT 브랜드 가이드라인 | .claude/ + .agent/ |
| 10 | brand-guidelines | 문서 | 전반적 브랜드 가이드라인 | .claude/ + .agent/ |
| 11 | web-design-guidelines | 개발 | 웹 디자인 가이드 | .claude/ + .agent/ |
| 12 | fastapi-backend-guidelines | 개발 | FastAPI 백엔드 | .claude/ + .agent/ |
| 13 | nextjs-frontend-guidelines | 개발 | Next.js 프론트엔드 | .claude/ + .agent/ |
| 14 | vercel-react-best-practices | 개발 | React 베스트 프랙티스 | .claude/ + .agent/ |
| 15 | pytest-backend-testing | 개발 | 백엔드 테스트 | .claude/ + .agent/ |
| 16 | error-tracking | 개발 | 에러 추적 | .claude/ + .agent/ |
| 17 | skill-developer | 메타 | 새 스킬 개발 | .claude/ |
| 18 | workspace-management | 메타 | 워크스페이스 관리 | .claude/ |

| 19 | hr-consulting | HR | HRM/HRD/OD 종합 컨설팅 프레임워크 | .claude/ + .agent/ |
| 20 | business-planning | 사업 | PDCA 기반 사업 기획·실행·보완 | .claude/ + .agent/ |
| 21 | org-diagnosis | HR | 조직진단·조직설계·조직문화 분석 | .claude/ + .agent/ |
| 22 | strategic-management | 경영 | 경영전략 수립·실행 | .claude/ + .agent/ |
| 23 | knowledge-management | 학습 | MBA/AI 학습 노트·지식 축적 | .claude/ + .agent/ |

---

## 2. 에이전트 카탈로그 (12개) — `workspace/_shared/agents/`

> **크로스도구**: sync-tools.cmd 실행 시 `.claude/agents/` + `.agent/workflows/` 양쪽에 배포됨
> Claude Code, OpenCode, Antigravity 모든 도구에서 사용 가능

| # | 에이전트 | 역할 | 컨설팅 업무 매핑 |
|---|----------|------|-----------------|
| 1 | planner | 작업 계획 수립 | 프로젝트 기획, WBS 작성 |
| 2 | plan-reviewer | 계획 검토 | 기획안 품질 검토 |
| 3 | workspace-manager | 워크스페이스 관리 | 프로젝트 생성/아카이빙/동기화 |
| 4 | auto-error-resolver | 에러 자동 해결 | 기술 문제 자동 해결 |
| 5 | code-architecture-reviewer | 코드 아키텍처 리뷰 | 시스템 설계 검토 |
| 6 | code-refactor-master | 코드 리팩토링 | 코드 품질 개선 |
| 7 | documentation-architect | 문서화 설계 | 보고서 구조 설계 |
| 8 | frontend-error-fixer | 프론트엔드 에러 수정 | UI 문제 해결 |
| 9 | web-research-specialist | 웹 리서치 | 시장조사, 벤치마킹 |
| 10 | auth-route-debugger | 인증 라우트 디버깅 | 인증 시스템 디버깅 |
| 11 | auth-route-tester | 인증 라우트 테스트 | 인증 시스템 테스트 |
| 12 | refactor-planner | 리팩토링 계획 | 개선 계획 수립 |

---

## 3. 워크플로우 카탈로그 (7개) — `workspace/_shared/workflows/`

> **크로스도구**: sync-tools.cmd 실행 시 `.agent/workflows/` + `.claude/agents/` 양쪽에 배포됨
> Antigravity, Claude Code, OpenCode 모든 도구에서 사용 가능

| # | 워크플로우 | 역할 | 활용 장면 |
|---|------------|------|-----------|
| 1 | agent-01-legal | 법률/구조 설계 자문 | 법인 설립, 계약서 검토 |
| 2 | agent-02-hr | HR/인사노무 진단 | 인사제도 진단, 노무 자문 |
| 3 | agent-03-job-carving | 장애인 직무개발 | Job Carving 컨설팅 |
| 4 | agent-04-bm | 비즈니스 모델/재무 추정 | 사업 타당성 분석, 손익 추정 |
| 5 | agent-05-research | 시장 리서치/경쟁 분석 | 시장조사, 경쟁사 분석 |
| 6 | agent-06-branding | 브랜딩/네이밍/스토리텔링 | 브랜드 전략, 네이밍 |
| 7 | agent-07-cso | 총괄 관리/사업계획서 | 사업계획서 작성, 총괄 관리 |

---

## 4. 커맨드 카탈로그 (4개)

### 유저 레벨 — `~/.claude/commands/`

| # | 커맨드 | 용도 |
|---|--------|------|
| 1 | narajan-webapp | 나라장터 키워드 기반 크롤링 웹앱 생성 |

### 워크스페이스 레벨 — `workspace/_shared/commands/`

| # | 커맨드 | 용도 |
|---|--------|------|
| 2 | dev-docs | 개발 문서 생성 |
| 3 | dev-docs-update | 개발 문서 업데이트 |
| 4 | route-research-for-testing | 라우트 리서치 (테스트용) |

---

## 5. 플러그인 카탈로그

| # | 플러그인 | 용도 | 도구 |
|---|----------|------|------|
| 1 | Notion | Notion 워크스페이스 연동 (DB, 페이지, 검색) | Claude Code |
| 2 | skill-creator | 스킬 생성/수정/평가 | Claude Code |

---

## 6. 프롬프트 라이브러리 — `workspace/_shared/prompts/`

| 폴더 | 대상 도구 | 용도 |
|------|-----------|------|
| `common/` | 모든 도구 | 재사용 프롬프트 조각 (역할 정의, 톤, 규칙) |
| `claude-web/` | Claude Web (Projects) | 프로젝트별 시스템 지침 |
| `cowork/` | Claude Desktop (Cowork) | 데스크톱 앱용 프롬프트 |

---

## 7. 도구별 리소스 접근 맵

```
                    ┌──────────────────────────┐
                    │   workspace/_shared/      │
                    │   (Single Source of Truth) │
                    └─────────┬────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
  ┌──────▼───────┐    ┌──────▼───────┐    ┌──────▼───────┐
  │ Claude Code  │    │ Antigravity  │    │ Claude Web   │
  │ + OpenCode   │    │              │    │ + Cowork     │
  ├──────────────┤    ├──────────────┤    ├──────────────┤
  │ Tier 1 스킬  │    │ .agent/      │    │ prompts/     │
  │ (자동 로드)  │    │  skills/     │    │  claude-web/ │
  │              │    │  workflows/  │    │  cowork/     │
  │ Tier 2 스킬  │    │              │    │              │
  │ (프로젝트별) │    │              │    │              │
  │              │    │              │    │              │
  │ ★에이전트19개│    │ ★에이전트19개│    │              │
  │ .claude/     │    │ .agent/      │    │              │
  │  agents/     │    │  workflows/  │    │              │
  │              │    │              │    │              │
  │ 커맨드       │    │              │    │              │
  │ 플러그인     │    │              │    │              │
  └──────────────┘    └──────────────┘    └──────────────┘

  ★ 교차 배포: agents(12) + workflows(7) = 19개 양쪽 모두 배포
```

---

## 8. 업무 도메인별 리소스 매핑

### HR 컨설팅

| 업무 | 사용 스킬 | 사용 에이전트/워크플로우 |
|------|-----------|------------------------|
| 직무분석 | job-analysis, data-analysis | agent-02-hr |
| 조직진단 | consulting-report, data-analysis | agent-02-hr, web-research-specialist |
| 보고서 작성 | consulting-report, pptx, docx | documentation-architect |
| 제안서 작성 | proposal, pptx | planner, plan-reviewer |

### 사업개발

| 업무 | 사용 스킬 | 사용 에이전트/워크플로우 |
|------|-----------|------------------------|
| 시장조사 | web-search, data-analysis | agent-05-research, web-research-specialist |
| 사업계획 | proposal | agent-04-bm, agent-07-cso |
| 재무추정 | data-analysis | agent-04-bm |
| 법률검토 | - | agent-01-legal |

### 웹/앱 개발

| 업무 | 사용 스킬 | 사용 에이전트/워크플로우 |
|------|-----------|------------------------|
| 프론트엔드 | frontend-design, nextjs15-init | frontend-error-fixer |
| 백엔드 | fastapi-backend-guidelines | code-architecture-reviewer |
| 테스트 | pytest-backend-testing | auth-route-tester |

---

## 9. 관리 규칙

### 새 리소스 추가 시

1. 이 REGISTRY.md에 먼저 등록
2. 해당 위치에 파일 생성
3. `sync-tools.cmd` 실행하여 활성 프로젝트에 배포

### 리소스 수정 시

1. 원본 위치에서 수정 (Tier 1: ~/.claude/skills/, Tier 2: _shared/skills/)
2. `sync-tools.cmd` 실행하여 프로젝트에 반영
3. REGISTRY.md 업데이트

### 정기 점검

| 주기 | 작업 |
|------|------|
| 프로젝트 시작 시 | 필요 스킬 확인, 없으면 생성 |
| 프로젝트 완료 시 | 새로 만든 스킬/프롬프트를 _shared/에 등록 |
| 분기 1회 | 전체 레지스트리 최신화, 미사용 리소스 정리 |
