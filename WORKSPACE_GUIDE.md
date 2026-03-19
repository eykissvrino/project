# 워크스페이스 운영 가이드

> AI 도구(Claude Code, Antigravity, Cowork)가 이 워크스페이스에서 작업할 때 반드시 참조해야 하는 규칙입니다.

---

## 1. 워크스페이스 구조

```
workspace/
├── CLAUDE.md                ← AI가 최초 읽는 전역 컨텍스트
├── WORKSPACE_GUIDE.md       ← 이 문서 (운영 규칙)
├── new-project.cmd          ← 새 프로젝트 생성 (Windows)
├── new-project.sh           ← 새 프로젝트 생성 (bash)
│
├── _shared/                 ← 모든 프로젝트 공용 리소스
│   ├── skills/              ← 범용 스킬 (18개)
│   ├── agents/              ← 범용 에이전트 (11개)
│   ├── workflows/           ← Antigravity 워크플로우 (7개)
│   ├── commands/            ← Claude Code 커맨드 (3개)
│   ├── templates/           ← 프로젝트 템플릿
│   └── prompts/             ← 자주 쓰는 프롬프트
│
├── projects/                ← 활성 프로젝트
│   └── P2026-001_장애인_B2B사업/
│
├── archive/                 ← 완료된 프로젝트
└── outputs/                 ← 최종 산출물 모음
```

---

## 2. 프로젝트 코드 체계

### 형식: `P{년도}-{일련번호}_{프로젝트명}`

| 구성요소 | 설명 | 예시 |
|----------|------|------|
| P | 프로젝트 접두사 (고정) | P |
| 년도 | 프로젝트 시작 연도 (4자리) | 2026 |
| 일련번호 | 해당 연도 내 순차 번호 (3자리) | 001, 002, ... |
| 프로젝트명 | 간결한 한글/영문 프로젝트명 | 장애인_B2B사업 |

### 예시
- `P2026-001_장애인_B2B사업`
- `P2026-002_한화연_산업전환진단`
- `P2026-003_진테크_일터혁신`

### 규칙
- 일련번호는 `new-project.cmd` 또는 `new-project.sh` 사용 시 자동 부여
- 프로젝트명에 공백 대신 언더스코어(`_`) 사용
- 연도가 바뀌면 번호는 001부터 재시작

---

## 3. 프로젝트 폴더 구조

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

## 4. 파일 저장 규칙

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

## 5. 공유 리소스 활용

### 스킬 (18개)

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
| frontend-design | 프론트엔드 UI 설계 |
| web-design-guidelines | 웹 디자인 가이드 |
| fastapi-backend-guidelines | FastAPI 백엔드 |
| nextjs-frontend-guidelines | Next.js 프론트엔드 |
| vercel-react-best-practices | React 베스트 프랙티스 |
| pytest-backend-testing | 백엔드 테스트 |
| error-tracking | 에러 추적 |
| skill-developer | 새 스킬 개발 |

### 에이전트 (11개) — Claude Code 전용

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

### 워크플로우 (7개) — Antigravity 전용

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

## 6. AI 도구별 작업 방법

### Claude Code
```bash
cd ~/workspace/projects/P2026-001_장애인_B2B사업
claude
```
- `.claude/skills/`, `.claude/agents/`, `CLAUDE.md`를 자동 인식
- 슬래시 커맨드로 `.claude/commands/` 내 커맨드 사용 가능

### Antigravity
- 작업 디렉토리를 해당 프로젝트 폴더로 설정
- `.agent/skills/`, `.agent/workflows/`를 자동 인식

### Cowork (Claude Desktop)
- 폴더 선택 시 해당 프로젝트 폴더 또는 workspace/ 선택
- 파일 읽기/쓰기로 프로젝트 내 작업

---

## 7. 프로젝트 생명주기

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

## 8. 새 스킬/에이전트 추가 방법

### 스킬 추가
```
_shared/skills/새스킬명/SKILL.md   ← 파일 생성
```
이후 `new-project.cmd`로 생성하는 프로젝트에 자동 포함됩니다.
기존 프로젝트에 추가하려면 해당 프로젝트의 `.claude/skills/`나 `.agent/skills/`에 직접 복사하세요.

### 에이전트 추가
```
_shared/agents/새에이전트.md   ← 파일 생성
```

### 워크플로우 추가
```
_shared/workflows/새워크플로우.md   ← 파일 생성
```

---

## 9. 워크스페이스 매니저 에이전트

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

## 10. 주의사항

- **홈 폴더에서 AI 도구 실행 금지** — 반드시 프로젝트 폴더로 이동 후 실행
- **OneDrive에 AI 설정 폴더를 넣지 마세요** — `.claude/`, `.agent/` 등은 동기화 충돌 위험
- **민감 정보(API 키, 토큰)는 절대 프로젝트 폴더에 저장 금지** — 1Password 등 별도 관리
- **`_shared/`는 직접 수정 가능** — 스킬 내용을 개선하면 이후 모든 프로젝트에 반영
- **`archive/`의 파일은 수정하지 마세요** — 필요 시 `projects/`로 복사 후 작업
