# 워크스페이스 운영 가이드

> AI 도구(Claude Code, Antigravity, Cowork)가 이 워크스페이스에서 작업할 때 반드시 참조해야 하는 규칙입니다.
>
> 최종 업데이트: 2026-03-19

---

## 1. 워크스페이스 구조

```
workspace/
├── CLAUDE.md                ← AI가 최초 읽는 전역 컨텍스트
├── WORKSPACE_GUIDE.md       ← 이 문서 (운영 규칙)
├── new-project.cmd          ← 새 프로젝트 생성 (Windows)
├── new-project.sh           ← 새 프로젝트 생성 (bash)
├── sync-tools.cmd           ← ★ 리소스 동기화 (_shared → 모든 활성 프로젝트)
│
├── _shared/                 ← 모든 프로젝트 공용 리소스
│   ├── REGISTRY.md          ← ★ 전체 리소스 마스터 카탈로그 (65+ 리소스)
│   ├── AI_TOOLS_MAP.md      ← AI 도구 설정 맵 (전체 도구/설정 위치 정리)
│   ├── skills/              ← 워크스페이스 레벨 스킬 (23개, 컨설팅+경영+학습)
│   ├── agents/              ← Claude Code 에이전트 (12개)
│   ├── workflows/           ← Antigravity 워크플로우 (7개)
│   ├── commands/            ← Claude Code 커맨드 (3개)
│   ├── templates/           ← 프로젝트 템플릿
│   └── prompts/             ← ★ 크로스도구 프롬프트 라이브러리
│       ├── common/          ← 재사용 프롬프트 조각 (역할, 톤, 규칙)
│       ├── claude-web/      ← Claude Web Projects용 시스템 지침
│       └── cowork/          ← Claude Desktop(Cowork)용 프롬프트
│
├── projects/                ← 활성 프로젝트
│   ├── P2026-001_장애인_B2B사업/
│   ├── P2026-002_컨소시엄_AX진단_컨설팅도구/
│   ├── P2026-003_선도기업_직무디자인_연구용역/
│   └── P2026-004_나라장터모니터링_웹앱/
│
├── archive/                 ← 완료된 프로젝트
└── outputs/                 ← 최종 산출물 모음
```

---

## 2. 스킬/에이전트 관리 체계 (2-Tier 원칙)

### 핵심 원칙: Single Source of Truth

스킬과 에이전트는 **두 곳에 나뉘어 관리**되며, 각각 다른 역할을 합니다.

```
┌─────────────────────────────────────────────────────────┐
│  Tier 1: 유저 레벨 (전역)                                │
│  위치: ~/.claude/skills/ (22개)                           │
│  적용: 모든 프로젝트에서 자동 로드                          │
│  성격: AI 도구, 개발, 콘텐츠 생성                          │
│  예시: card-news-generator, codex, flutter-init 등        │
├─────────────────────────────────────────────────────────┤
│  Tier 2: 워크스페이스 레벨 (프로젝트용)                     │
│  위치: workspace/_shared/skills/ (19개)                    │
│  적용: 프로젝트 생성 시 복사/심링크로 배포                   │
│  성격: 컨설팅 업무, 문서 제작                               │
│  예시: consulting-report, job-analysis, pptx 등           │
└─────────────────────────────────────────────────────────┘
```

### 수정 시 원칙

| 대상 | 원본 위치 | 수정 방법 |
|------|-----------|-----------|
| AI/개발 스킬 | `~/.claude/skills/` | 여기서 직접 수정 → 전역 즉시 반영 |
| 컨설팅 스킬 | `workspace/_shared/skills/` | 여기서 수정 → 기존 프로젝트에는 수동 배포 필요 |
| 에이전트 | `workspace/_shared/agents/` | 여기서 수정 → 기존 프로젝트에는 수동 배포 필요 |
| 워크플로우 | `workspace/_shared/workflows/` | 여기서 수정 → Antigravity 프로젝트에 수동 배포 |
| 커맨드 | `~/.claude/commands/` (유저) | 전역 적용 |
| 커맨드 | `workspace/_shared/commands/` (워크스페이스) | 프로젝트 배포 시 포함 |

### 새 스킬 추가 시 판단 기준

```
Q: 이 스킬은 모든 프로젝트에서 항상 필요한가?
  YES → Tier 1: ~/.claude/skills/에 추가
  NO  → Tier 2: workspace/_shared/skills/에 추가

Q: 컨설팅 업무 전용인가, AI/개발 범용인가?
  컨설팅 → Tier 2
  AI/개발 → Tier 1
```

> **상세 목록**: `_shared/AI_TOOLS_MAP.md` 참조

---

## 3. 프로젝트 코드 체계

### 형식: `P{년도}-{일련번호}_{프로젝트명}`

| 구성요소 | 설명 | 예시 |
|----------|------|------|
| P | 프로젝트 접두사 (고정) | P |
| 년도 | 프로젝트 시작 연도 (4자리) | 2026 |
| 일련번호 | 해당 연도 내 순차 번호 (3자리) | 001, 002, ... |
| 프로젝트명 | 간결한 한글/영문 프로젝트명 | 장애인_B2B사업 |

### 규칙
- 일련번호는 `new-project.cmd` 또는 `new-project.sh` 사용 시 자동 부여
- 프로젝트명에 공백 대신 언더스코어(`_`) 사용
- 연도가 바뀌면 번호는 001부터 재시작

---

## 4. 프로젝트 폴더 구조

새 프로젝트 생성 시 아래 구조가 자동 적용됩니다:

```
P2026-XXX_프로젝트명/
├── CLAUDE.md               ← 프로젝트 컨텍스트 (AI가 최초 읽는 파일)
├── .claude/                ← Claude Code 설정
│   ├── skills/             ← 공유 스킬 자동 포함
│   ├── agents/             ← 공유 에이전트 자동 포함
│   ├── commands/           ← 공유 커맨드 자동 포함
│   └── settings.json
├── .agent/                 ← Antigravity 설정
│   ├── skills/             ← 공유 스킬 자동 포함
│   └── workflows/          ← 공유 워크플로우 자동 포함
├── docs/                   ← 작업 메모, 회의록, 중간 문서
├── data/                   ← 원시 데이터, 참고자료
└── outputs/                ← 최종 산출물
```

---

## 5. 파일 저장 규칙

### 어디에 저장하나?

| 파일 유형 | 저장 위치 | 예시 |
|-----------|-----------|------|
| 작업 중 메모/초안 | `프로젝트/docs/` | 회의록, 분석 메모, 중간 보고 |
| 원시 데이터/참고자료 | `프로젝트/data/` | 설문 원본, 기업 제공 자료 |
| 최종 산출물 | `프로젝트/outputs/` | 보고서, 제안서, 분석 결과 |
| 클라이언트 전달용 복사본 | `workspace/outputs/` | 여러 프로젝트 산출물 취합 |

### 파일명 규칙

**산출물:**
```
[유형]_[기관명]_[내용]_v버전.확장자
```
예시:
- `결과보고서_한화연_산업전환진단_v2.1.pptx`
- `제안서_진테크_일터혁신_v1.0.pdf`
- `직무분석_엔씨소프트_워크시트_v3.xlsx`

**작업 문서:**
```
날짜_내용.확장자
```
예시:
- `20260309_킥오프회의_회의록.md`
- `20260315_설문설계_초안.xlsx`

### 버전 관리
- 진행 중: 파일명에 `_v1`, `_v2` 등 버전 표기
- 최종본 확정 시: `_최종` 또는 `_final` 접미사 추가
- 이전 버전은 `docs/_archive/`로 이동

---

## 6. 공유 리소스 목록

### Tier 2 스킬 (워크스페이스 레벨, 23개)

**컨설팅 업무용:**
| 스킬명 | 용도 |
|--------|------|
| consulting-report | 컨설팅 보고서 작성 가이드 |
| job-analysis | NCS 기반 직무분석 프레임워크 |
| proposal | 제안서/발표자료 작성 가이드 |
| data-analysis | 설문분석, HR 데이터 분석 |

**문서 제작용:**
| 스킬명 | 용도 |
|--------|------|
| pptx | PowerPoint 슬라이드 제작 |
| docx | Word 문서 제작 |
| pdf | PDF 처리/생성 |
| mermaid | 다이어그램/플로차트 |
| ppt-brand-guidelines | PPT 브랜드 가이드라인 |
| brand-guidelines | 전반적 브랜드 가이드라인 |

**개발/기술용:**
| 스킬명 | 용도 |
|--------|------|
| web-design-guidelines | 웹 디자인 가이드 |
| fastapi-backend-guidelines | FastAPI 백엔드 |
| nextjs-frontend-guidelines | Next.js 프론트엔드 |
| vercel-react-best-practices | React 베스트 프랙티스 |
| pytest-backend-testing | 백엔드 테스트 |
| error-tracking | 에러 추적 |
| skill-developer | 새 스킬 개발 |
| workspace-management | 워크스페이스 관리 |

**HR·경영·학습 (Phase 2 신규):**
| 스킬명 | 용도 |
|--------|------|
| hr-consulting | HRM/HRD/OD 종합 컨설팅 프레임워크 |
| business-planning | PDCA 기반 사업 기획·실행·보완 |
| org-diagnosis | 조직진단·조직설계·조직문화·변화관리 |
| strategic-management | 경영전략 수립·실행 (BSC/OKR) |
| knowledge-management | MBA/AI 학습·지식 축적·관리 |

> **Tier 1 스킬 (유저 레벨, 22개)** 목록은 `_shared/AI_TOOLS_MAP.md` 참조
> **전체 리소스 목록**: `_shared/REGISTRY.md` 참조

### 에이전트 (12개) — 모든 도구 (Claude Code + OpenCode + Antigravity)

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

### 워크플로우 (7개) — 모든 도구 (Antigravity + Claude Code + OpenCode)

| 워크플로우 | 용도 |
|------------|------|
| agent-01-legal | 법률/구조 설계 자문 |
| agent-02-hr | HR/인사노무 진단 |
| agent-03-job-carving | 장애인 직무개발 (Job Carving) |
| agent-04-bm | 비즈니스 모델/재무 추정 |
| agent-05-research | 시장 리서치/경쟁 분석 |
| agent-06-branding | 브랜딩/네이밍/스토리텔링 |
| agent-07-cso | 총괄 관리/사업계획서 작성 |

---

## 7. AI 도구별 작업 방법

### Claude Code
```bash
cd ~/workspace/projects/P2026-001_장애인_B2B사업
claude
```
- Tier 1 스킬(`~/.claude/skills/`)은 자동 로드
- 프로젝트 내 `.claude/skills/`(Tier 2 배포본)도 자동 인식
- `CLAUDE.md`를 프로젝트 컨텍스트로 자동 인식
- 슬래시 커맨드로 `.claude/commands/` 내 커맨드 사용 가능

### Antigravity
- 작업 디렉토리를 해당 프로젝트 폴더로 설정
- `.agent/skills/`, `.agent/workflows/`를 자동 인식

### Cowork (Claude Desktop)
- 폴더 선택 시 해당 프로젝트 폴더 또는 workspace/ 선택
- 파일 읽기/쓰기로 프로젝트 내 작업

---

## 8. 프로젝트 생명주기

```
생성 → 진행 → 완료 → 아카이브
```

### 생성
```bash
# Windows
new-project.cmd "기관명_프로젝트명"

# bash
./new-project.sh "기관명_프로젝트명"
```

### 진행
- `projects/P2026-XXX_프로젝트명/` 에서 작업
- 산출물은 `outputs/`에 저장

### 완료 → 아카이브
```bash
# projects/ → archive/ 로 이동
mv projects/P2026-001_장애인_B2B사업 archive/
```

---

## 9. 새 스킬/에이전트 추가 방법

### 스킬 추가

**Tier 1 (전역 AI/개발 스킬):**
```
~/.claude/skills/새스킬명/SKILL.md   ← 파일 생성
```
→ 모든 프로젝트에서 즉시 사용 가능

**Tier 2 (워크스페이스 컨설팅 스킬):**
```
workspace/_shared/skills/새스킬명/SKILL.md   ← 파일 생성
```
→ 이후 `new-project.cmd`로 생성하는 프로젝트에 자동 포함
→ 기존 프로젝트에 추가하려면 해당 프로젝트의 `.claude/skills/`에 직접 복사

### 에이전트 추가
```
workspace/_shared/agents/새에이전트.md   ← 파일 생성
```

### 워크플로우 추가
```
workspace/_shared/workflows/새워크플로우.md   ← 파일 생성
```

---

## 10. 워크스페이스 매니저 에이전트

워크스페이스 전체를 관리하는 전용 에이전트가 `_shared/agents/workspace-manager.md`에 있습니다.

### 주요 기능

| 요청 | 수행 내용 |
|------|----------|
| "새 프로젝트 만들어" | 코드 부여 + 폴더 생성 + 리소스 연결 |
| "프로젝트 상태 보여줘" | 활성/아카이브 현황 리포트 |
| "워크스페이스 점검해" | 헬스체크 전체 실행 |
| "산출물 정리해" | 프로젝트 → 전역 outputs 동기화 |
| "스킬 추가해" | 새 스킬 생성 + 전 프로젝트 배포 |
| "리소스 동기화" | _shared/ → 모든 활성 프로젝트에 배포 |
| "이 프로젝트 아카이빙해" | archive/로 이동 |
| "폴더 정리해" | 미분류 파일 감지 + 정리 |

### 산출물 유형별 분류

| 유형 | 확장자 | outputs/ 하위 폴더 |
|------|--------|-------------------|
| 보고서/문서 | .docx, .pdf, .md | documents/ |
| 프레젠테이션 | .pptx | presentations/ |
| 데이터/분석 | .xlsx, .csv | data-analysis/ |
| 웹앱/웹사이트 | .html, .jsx, 폴더 | web-apps/ |
| 모바일앱 | .apk, 프로젝트 폴더 | mobile-apps/ |
| SaaS/서비스 | 프로젝트 폴더 | services/ |
| 이미지/디자인 | .png, .svg | design/ |

### 관련 파일
- 에이전트: `_shared/agents/workspace-manager.md`
- 스킬: `_shared/skills/workspace-management/SKILL.md`

---

## 11. 홈 디렉토리 관리

### AI 도구 설정 폴더 맵

홈 디렉토리(`C:\Users\eykis\`)에는 여러 AI 도구의 설정 폴더가 존재합니다.
각 폴더의 역할과 관리 방법은 `_shared/AI_TOOLS_MAP.md`에 상세 기술되어 있습니다.

```
~/ (홈 디렉토리)
├── .claude/        ← Claude Code 설정 + Tier 1 스킬 (건드리지 않기)
├── .claude.json    ← Claude Code 전역 인증 (삭제 금지)
├── .opencode/      ← OhMyClaudeCode 런타임 (건드리지 않기)
├── .config/        ← OpenCode 설정
├── .gemini/        ← Gemini 설정
├── .antigravity/   ← Antigravity 설정
├── .agents/        ← ⚠️ 정리 필요 (아래 참조)
├── .copilot/       ← GitHub Copilot
├── .vscode/        ← VS Code
└── workspace/      ← ★ 모든 작업은 여기서 수행
```

### 정리 완료 항목 (2026-03-19)

| 파일/폴더 | 조치 | 결과 |
|-----------|------|------|
| `~/.agents/agents.md-main/` | `workspace/archive/`로 이관 | ✅ 완료 |
| `~/.agents/oh-my-openagent-dev/` | `workspace/archive/`로 이관 | ✅ 완료 |
| `~/.agents/workflows/` | 중복본 삭제 | ✅ 완료 |
| `~/nul` | 불필요 파일 삭제 | ✅ 완료 |
| `_shared/skills/frontend-design/` | Tier 1 중복 삭제 | ✅ 완료 |
| `_shared/AI_도구_폴더관리_가이드.md` | AI_TOOLS_MAP.md로 대체 | ✅ 완료 |

### 정기 관리 체크리스트

| 주기 | 작업 |
|------|------|
| 수시 | 프로젝트 완료 시 `projects/` → `archive/` 이관 |
| 월 1회 | `~/.claude/cache/`, `~/.claude/debug/` 정리 |
| 분기 1회 | 스킬/에이전트 목록 최신화, 미사용 스킬 정리 |
| 분기 1회 | AI_TOOLS_MAP.md 업데이트 |
| 연 1회 | `archive/` 오래된 프로젝트 외부 백업 |

---

## 12. 주의사항

- **홈 폴더에서 AI 도구 실행 금지** — 반드시 프로젝트 폴더로 이동 후 실행
- **OneDrive에 AI 설정 폴더를 넣지 마세요** — `.claude/`, `.agent/` 등은 동기화 충돌 위험
- **민감 정보(API 키, 토큰)는 절대 프로젝트 폴더에 저장 금지** — 1Password 등 별도 관리
- **`_shared/`는 직접 수정 가능** — 스킬 내용을 개선하면 이후 모든 프로젝트에 반영
- **`archive/`의 파일은 수정하지 마세요** — 필요 시 `projects/`로 복사 후 작업
- **스킬 중복 금지** — Tier 1과 Tier 2에 같은 스킬이 있으면 혼란 발생 (AI_TOOLS_MAP.md에서 관리)
