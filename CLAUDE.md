# 시앤피컨설팅 AI 워크스페이스

## 사용자 프로필
- **이석주** — 시앤피컨설팅 HR 솔루션팀 팀장
- **비개발자** — CLI/코드에 익숙하지 않음. 한국어로 자연스럽게 지시하면 AI가 알아서 실행
- **전문 분야**: HR 컨설팅(HRM/HRD/OD), 사업기획, 경영전략, 조직관리

## 핵심 원칙

### 1. 한국어 자연어 인터페이스
- 사용자는 **일상적인 한국어**로 지시함 (CLI 명령어 사용 안 함)
- AI가 의도를 파악하여 적절한 도구/스킬/에이전트를 **자동으로 선택·실행**
- 모든 응답, 문서, 산출물은 **한국어**로 작성
- 기술 용어 대신 쉬운 말로 설명 (필요 시 용어 병기)

### 2. 자동 리소스 매칭
사용자가 업무를 말하면 AI가 적절한 스킬을 자동 적용:

| 사용자 말 | 리드 에이전트 | 자동 적용 스킬 |
|-----------|-------------|---------------|
| "전략 수립해줘" | **Athena** | strategic-management |
| "시장조사 해줘" | **Apollo** | market-research, data-analysis |
| "직무분석 해줘" | **Hera** | job-analysis, hr-consulting |
| "조직진단 해줘" | **Hera** | org-diagnosis, data-analysis |
| "제안서 만들어줘" | **Hermes** + Midas | proposal, pptx |
| "보고서 써줘" | **Hermes** | consulting-report, pptx/docx |
| "사업계획서 만들어줘" | **Midas** | business-planning, financial-analysis |
| "법률 검토해줘" | **Themis** | legal-consulting |
| "브랜딩 해줘" | **Aphrodite** | branding-marketing |
| "웹사이트 만들어줘" | **Daedalus** | Arachne(FE), Talos(BE), Helios(인프라) |
| "앱 만들어줘" | **Daedalus** | Iris(모바일), Talos(BE) |
| "프로젝트 현황 보여줘" | **Chronos** | project-management |
| "새 프로젝트 만들어" | workspace-manager | workspace-management |
| "리소스 동기화해줘" | — | sync-tools.cmd 실행 |
| "학습 정리해줘" | — | knowledge-management |

> **에이전트 체계 상세**: `projects/p2026-000_AI활용/CLAUDE.md` 참조

### 3. 컨설팅 품질 기준
- 전문적이고 공식적인 톤 유지
- 주장에는 반드시 근거(데이터, 이론, 사례) 제시
- 검증된 프레임워크 활용 (SWOT, BSC, NCS 등)
- 한국 HR/노동 환경 반영

## 워크스페이스 구조
```
workspace/
├── _shared/              ← 공유 리소스 (Single Source of Truth)
│   ├── REGISTRY.md       ← 전체 리소스 카탈로그 (70+ 리소스)
│   ├── AI_TOOLS_MAP.md   ← AI 도구별 설정 경로
│   ├── skills/ (23개)    ← 컨설팅/경영/학습 스킬
│   ├── agents/ (12개)    ← 에이전트 (크로스도구)
│   ├── workflows/ (7개)  ← 워크플로우 (크로스도구)
│   ├── commands/         ← CLI 커맨드
│   ├── prompts/          ← 크로스도구 프롬프트 라이브러리
│   └── templates/        ← 프로젝트 템플릿
├── projects/             ← 활성 프로젝트
├── archive/              ← 완료 프로젝트
└── outputs/              ← 최종 산출물 모음
```

## 프로젝트 관리
- 프로젝트 코드: `P{년도}-{일련번호}_{프로젝트명}` (예: P2026-001_장애인_B2B사업)
- 새 프로젝트: `new-project.sh "프로젝트명"` 으로 자동 생성
- 완료 시: `projects/` → `archive/` 이동
- 산출물: 프로젝트 내 `outputs/`에 저장, 필요 시 루트 `outputs/`에 복사

## 스킬 체계 (2-Tier)
- **Tier 1** (전역, 22개): `~/.claude/skills/` — AI/개발/콘텐츠 스킬 (자동 로드)
- **Tier 2** (워크스페이스, 23개): `_shared/skills/` — 컨설팅/경영/학습 스킬 (프로젝트 배포)
- 상세 목록: `_shared/REGISTRY.md` 참조

## 자주 쓰는 산출물 유형
- 직무분석 보고서 (pptx, xlsx)
- 제안서/발표자료 (pptx)
- 컨설팅 결과보고서 (pptx, pdf)
- 사업계획서 (pptx, docx)
- 훈련과정 로드맵 (pptx, xlsx)
- 데이터 분석 결과 (xlsx)
- 조직진단 보고서 (pptx)
- 경영전략 보고서 (pptx)

## 참고 문서
- 운영 가이드: `WORKSPACE_GUIDE.md`
- 리소스 목록: `_shared/REGISTRY.md`
- 도구 설정: `_shared/AI_TOOLS_MAP.md`
