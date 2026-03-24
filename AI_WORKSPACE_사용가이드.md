# AI 워크스페이스 사용 가이드

> 이석주님을 위한 AI 작업 환경 활용 가이드입니다.
> CLI 명령어를 외울 필요 없습니다. 한국어로 말하면 AI가 알아서 합니다.
>
> 최종 업데이트: 2026-03-19

---

## 1. 이 체계가 뭔가요?

여러 AI 도구(Claude Code, OpenCode, Antigravity, Claude Web 등)를 사용할 때, **어떤 도구를 열든 같은 스킬, 에이전트, 프롬프트를 쓸 수 있도록** 만든 통합 관리 시스템입니다.

### 비유로 이해하기

```
워크스페이스 = 사무실
├── _shared/      = 공용 자료실 (모든 부서가 가져다 쓰는 양식, 매뉴얼, 도구)
├── projects/     = 내 책상 (지금 진행 중인 프로젝트 서류들)
├── archive/      = 캐비닛 (끝난 프로젝트 보관함)
└── outputs/      = 납품함 (클라이언트에게 보낼 최종 산출물)
```

---

## 2. 사용 가능한 AI 도구

| 도구 | 어디서 쓰나 | 특징 |
|------|------------|------|
| **Claude Code** | 터미널 (VS Code 등) | 파일 생성/수정, 코드 작성, 프로젝트 작업 |
| **OpenCode** | 터미널 | Claude Code + 멀티 에이전트 오케스트레이션 |
| **Antigravity** | 데스크톱 앱 | 시각적 인터페이스, 워크플로우 실행 |
| **Claude Web** | 웹 브라우저 | 빠른 질문, 분석, 초안 작성 |
| **Claude Desktop (Cowork)** | 데스크톱 앱 | 파일 읽기/쓰기, 업무 보조 |

**핵심**: 어떤 도구를 열든 같은 스킬과 에이전트가 준비되어 있습니다.

---

## 3. 이렇게 말하면 됩니다 (예시)

### 프로젝트 관리

| 이렇게 말하세요 | AI가 하는 일 |
|----------------|-------------|
| "새 프로젝트 만들어, OO기업 직무분석" | 프로젝트 폴더 생성 (P2026-005_OO기업_직무분석), 스킬/에이전트 자동 배포 |
| "지금 진행 중인 프로젝트 뭐 있어?" | projects/ 폴더 확인해서 목록 알려줌 |
| "장애인 B2B 프로젝트 끝났어, 정리해줘" | projects/ → archive/ 이동 |
| "리소스 동기화해줘" | 모든 프로젝트에 최신 스킬/에이전트 배포 |

### HR 컨설팅

| 이렇게 말하세요 | AI가 하는 일 |
|----------------|-------------|
| "직무분석 보고서 초안 써줘" | job-analysis + consulting-report 스킬로 보고서 작성 |
| "이 회사 조직진단 해줘" | org-diagnosis 스킬로 진단 프레임워크 적용 |
| "역량모델링 해야 해" | hr-consulting 스킬로 역량체계 설계 |
| "교육훈련 체계 만들어줘" | hr-consulting 스킬로 교육체계 설계 |
| "설문 데이터 분석해줘" | data-analysis 스킬로 통계 분석 |

### 사업기획

| 이렇게 말하세요 | AI가 하는 일 |
|----------------|-------------|
| "새 사업 아이디어 브레인스토밍 하자" | business-planning 스킬로 아이디어 발굴 |
| "사업계획서 만들어줘" | business-planning + strategic-management 스킬 |
| "시장 분석 해줘" | 웹 검색 + business-planning 스킬 |
| "손익 추정해줘" | business-planning 스킬의 재무추정 프레임워크 |
| "이 사업 PDCA 점검해줘" | business-planning 스킬의 Check 단계 |

### 보고서/문서 작성

| 이렇게 말하세요 | AI가 하는 일 |
|----------------|-------------|
| "제안서 PPT 만들어줘" | proposal + pptx 스킬 |
| "컨설팅 결과보고서 써줘" | consulting-report + pptx 스킬 |
| "경영전략 보고서 작성해줘" | strategic-management + consulting-report 스킬 |
| "이거 워드로 정리해줘" | docx 스킬 |
| "차트/다이어그램 그려줘" | mermaid 스킬 |

### 학습/지식관리

| 이렇게 말하세요 | AI가 하는 일 |
|----------------|-------------|
| "이 논문 요약해줘" | knowledge-management 스킬로 학습노트 작성 |
| "MBA 수업 내용 정리해줘" | knowledge-management 스킬 |
| "AI 최신 트렌드 알려줘" | 웹 검색 + knowledge-management 스킬 |
| "이 개념 쉽게 설명해줘" | 해당 도메인 스킬 자동 적용 |

---

## 4. 보유 중인 리소스 한눈에 보기

### 스킬 (45개) — "AI에게 부여하는 전문 능력"

스킬은 AI가 특정 업무를 잘할 수 있도록 하는 **매뉴얼**입니다.
직무분석 스킬을 가진 AI는 NCS 기반 직무분석을 체계적으로 수행합니다.

**항상 자동 로드되는 스킬 (Tier 1, 22개):**

| 분류 | 스킬 | 하는 일 |
|------|------|---------|
| 콘텐츠 | card-news-generator | 인스타그램 카드뉴스 자동 제작 |
| 콘텐츠 | midjourney-cardnews-bg | 카드뉴스 배경 이미지 프롬프트 |
| 개발 | nextjs15-init | Next.js 웹앱 프로젝트 생성 |
| 개발 | flutter-init | Flutter 모바일앱 프로젝트 생성 |
| 개발 | frontend-design | 웹 프론트엔드 UI 디자인 |
| 개발 | landing-page-guide-v2 | 랜딩페이지 제작 |
| 유틸 | web-search | 인터넷 검색 |
| 유틸 | web-to-markdown | 웹페이지를 문서로 변환 |
| 유틸 | gemini-logo-remover | 이미지에서 워터마크 제거 |
| 프롬프트 | prompt-enhancer | 내 지시를 더 좋은 프롬프트로 보강 |
| 프롬프트 | meta-prompt-generator | 새 슬래시 명령어 자동 생성 |
| 문서화 | workthrough | 작업 기록 자동 문서화 |
| ... | ... | (총 22개) |

**프로젝트마다 배포되는 스킬 (Tier 2, 23개):**

| 분류 | 스킬 | 하는 일 |
|------|------|---------|
| **HR** | hr-consulting | HRM/HRD/OD 종합 컨설팅 프레임워크 |
| **HR** | job-analysis | NCS 기반 직무분석, 직무기술서 작성 |
| **HR** | org-diagnosis | 조직진단, 조직설계, 조직문화, 변화관리 |
| **사업** | business-planning | PDCA 기반 사업 기획·실행·보완 |
| **경영** | strategic-management | 경영전략 수립 (SWOT, BSC, OKR 등) |
| **학습** | knowledge-management | MBA/AI 학습, 지식 축적·관리 |
| **컨설팅** | consulting-report | 컨설팅 보고서 작성 가이드 |
| **컨설팅** | proposal | 제안서/발표자료 작성 |
| **컨설팅** | data-analysis | 설문분석, HR 데이터 분석 |
| **문서** | pptx | PowerPoint 슬라이드 제작 |
| **문서** | docx | Word 문서 제작 |
| **문서** | pdf | PDF 처리/생성 |
| **문서** | mermaid | 다이어그램/플로차트 그리기 |
| **문서** | brand-guidelines | 브랜드 가이드라인 |
| **문서** | ppt-brand-guidelines | PPT 브랜드 가이드라인 |
| **개발** | web-design-guidelines | 웹 디자인 가이드 |
| **개발** | nextjs-frontend-guidelines | Next.js 프론트엔드 |
| **개발** | fastapi-backend-guidelines | FastAPI 백엔드 |
| **개발** | vercel-react-best-practices | React 개발 |
| **개발** | pytest-backend-testing | 백엔드 테스트 |
| **개발** | error-tracking | 에러 추적 |
| **메타** | skill-developer | 새 스킬 만들기 |
| **메타** | workspace-management | 워크스페이스 관리 |

### 에이전트 (19개) — "AI에게 부여하는 역할"

에이전트는 AI가 특정 **역할**을 맡도록 하는 설정입니다.
모든 도구(Claude Code, OpenCode, Antigravity)에서 사용 가능합니다.

**컨설팅/사업 에이전트 (7개):**

| 에이전트 | 역할 | 언제 쓰나 |
|----------|------|-----------|
| agent-01-legal | 법률/구조 설계 자문 | 법인 설립, 계약서 검토할 때 |
| agent-02-hr | HR/인사노무 진단 | 장애인 고용, 인사제도 진단할 때 |
| agent-03-job-carving | 장애인 직무개발 | Job Carving 컨설팅할 때 |
| agent-04-bm | 비즈니스 모델/재무 추정 | 사업 타당성 분석, 손익 추정할 때 |
| agent-05-research | 시장 리서치/경쟁 분석 | 시장조사, 경쟁사 분석할 때 |
| agent-06-branding | 브랜딩/네이밍 | 브랜드 전략, 네이밍할 때 |
| agent-07-cso | 총괄 관리/사업계획서 | 사업계획서 작성, 전략 총괄할 때 |

**개발/기술 에이전트 (12개):**

| 에이전트 | 역할 | 언제 쓰나 |
|----------|------|-----------|
| planner | 작업 계획 수립 | 복잡한 작업의 계획을 세울 때 |
| plan-reviewer | 계획 검토 | 세운 계획을 검토할 때 |
| workspace-manager | 워크스페이스 관리 | 프로젝트 생성/정리/동기화할 때 |
| web-research-specialist | 웹 리서치 | 인터넷에서 정보를 찾을 때 |
| documentation-architect | 문서화 설계 | 보고서 구조를 설계할 때 |
| auto-error-resolver | 에러 자동 해결 | 기술 오류를 해결할 때 |
| code-architecture-reviewer | 코드 설계 리뷰 | 시스템 설계를 검토할 때 |
| code-refactor-master | 코드 리팩토링 | 코드 품질을 개선할 때 |
| frontend-error-fixer | 프론트엔드 에러 수정 | UI 문제를 해결할 때 |
| auth-route-debugger | 인증 디버깅 | 로그인/인증 문제 해결할 때 |
| auth-route-tester | 인증 테스트 | 인증 시스템을 테스트할 때 |
| refactor-planner | 개선 계획 | 코드 개선 계획을 세울 때 |

### 프롬프트 라이브러리 — "AI에게 주는 역할 카드"

| 파일 | 어디서 쓰나 | 용도 |
|------|------------|------|
| role-hr-consultant.md | 모든 도구 | HR 컨설턴트 역할 부여 |
| role-business-planner.md | 모든 도구 | 사업기획 전문가 역할 부여 |
| tone-consulting.md | 모든 도구 | 전문적 문서 톤 설정 |
| hr-consulting-project.md | Claude Web | HR 프로젝트 지침 (복사해서 붙여넣기) |
| business-development-project.md | Claude Web | 사업개발 프로젝트 지침 |
| general-assistant.md | Claude Desktop | 범용 업무 보조 설정 |

---

## 5. 프로젝트 작업 흐름

### 새 프로젝트 시작

```
1. "새 프로젝트 만들어, OO기업 직무분석" 이라고 말하기
   → P2026-005_OO기업_직무분석 폴더 자동 생성
   → 23개 스킬 + 19개 에이전트 자동 배포

2. 해당 프로젝트 폴더에서 AI 도구 실행
   → Claude Code, OpenCode, Antigravity 아무거나 OK

3. 작업 시작!
   → "직무분석 보고서 써줘", "설문 설계해줘" 등
```

### 프로젝트 진행 중

```
작업 중 메모/초안  → 프로젝트/docs/ 에 저장
원시 데이터/참고자료 → 프로젝트/data/ 에 저장
최종 산출물       → 프로젝트/outputs/ 에 저장
```

### 파일 이름 규칙

```
산출물: [유형]_[기관명]_[내용]_v버전.확장자
  예: 결과보고서_한화연_산업전환진단_v2.1.pptx
      제안서_진테크_일터혁신_v1.0.pdf

작업문서: 날짜_내용.확장자
  예: 20260309_킥오프회의_회의록.md
      20260315_설문설계_초안.xlsx
```

### 프로젝트 완료

```
"이 프로젝트 끝났어, 정리해줘" 라고 말하기
→ projects/ 에서 archive/ 로 자동 이동
→ 더 이상 동기화 대상이 아님 (보관만)
→ 나중에 필요하면 다시 꺼낼 수 있음
```

---

## 6. 도구별 시작 방법

### Claude Code / OpenCode (터미널)
```
1. 프로젝트 폴더로 이동
2. claude (또는 opencode) 실행
3. 한국어로 원하는 작업 말하기
```

### Antigravity (데스크톱 앱)
```
1. 앱 실행
2. 작업 디렉토리를 프로젝트 폴더로 설정
3. 워크플로우 또는 자유 대화로 작업
```

### Claude Web (브라우저)
```
1. claude.ai 접속
2. Projects에서 해당 프로젝트 선택
3. _shared/prompts/claude-web/ 파일을 시스템 지침에 복사 (처음 1회)
4. 자유롭게 대화
```

### Claude Desktop / Cowork (데스크톱 앱)
```
1. 앱 실행
2. _shared/prompts/cowork/general-assistant.md 내용을 시스템 프롬프트에 설정 (처음 1회)
3. 자유롭게 대화
```

---

## 7. 주요 용어 설명

| 용어 | 쉬운 설명 |
|------|-----------|
| **스킬 (Skill)** | AI에게 부여하는 전문 능력. "직무분석 매뉴얼"처럼 AI가 참고하는 지침서 |
| **에이전트 (Agent)** | AI에게 부여하는 역할. "HR 컨설턴트 모드"처럼 특정 역할을 맡김 |
| **워크플로우 (Workflow)** | 에이전트와 같은 개념. Antigravity에서 부르는 이름 |
| **프롬프트 (Prompt)** | AI에게 주는 지시/역할 카드. 복사해서 붙여넣기 하면 됨 |
| **플러그인 (Plugin)** | AI 도구에 추가 기능을 붙이는 것 (예: Notion 연동) |
| **MCP** | AI가 외부 도구(웹 검색, 파일 등)를 사용할 수 있게 하는 연결 장치 |
| **Tier 1 / Tier 2** | 스킬의 등급. Tier 1은 항상 켜져 있고, Tier 2는 프로젝트마다 배포 |
| **교차 배포** | 에이전트를 모든 도구에서 쓸 수 있도록 양쪽에 복사하는 것 |
| **동기화 (Sync)** | 공용 자료실(_shared/)의 최신 내용을 모든 프로젝트에 반영하는 것 |
| **아카이브 (Archive)** | 완료된 프로젝트를 보관함으로 옮기는 것. 삭제가 아닌 보관 |
| **PDCA** | Plan-Do-Check-Act. 기획→실행→점검→개선 순환 사이클 |
| **NCS** | 국가직무능력표준. 한국의 직무분석 표준 체계 |
| **BSC** | 균형성과표. 재무/고객/프로세스/학습 4관점 성과관리 |
| **OKR** | 목표와 핵심 결과. 도전적 목표 설정 프레임워크 |
| **BMC** | 비즈니스 모델 캔버스. 사업모델을 9개 블록으로 정리 |

---

## 8. 자주 묻는 질문

### Q: 새 스킬을 추가하고 싶어요
**A:** "OO 스킬 만들어줘"라고 말하세요. AI가 `_shared/skills/` 에 새 스킬을 만들고 REGISTRY.md에 등록합니다.

### Q: 스킬을 수정하고 싶어요
**A:** "직무분석 스킬에 OO 내용 추가해줘"라고 말하세요. AI가 해당 SKILL.md를 수정합니다.

### Q: 다른 프로젝트에도 변경사항을 반영하고 싶어요
**A:** "리소스 동기화해줘"라고 말하세요. 모든 활성 프로젝트에 최신 스킬/에이전트가 배포됩니다.

### Q: 예전 프로젝트 자료를 다시 보고 싶어요
**A:** "아카이브에서 OO 프로젝트 꺼내줘"라고 말하세요. archive/ → projects/로 다시 이동합니다.

### Q: 어떤 스킬/에이전트가 있는지 모르겠어요
**A:** 이 문서의 4장을 보거나, "지금 쓸 수 있는 스킬 뭐 있어?"라고 물어보세요.

### Q: Claude Web에서는 스킬이 자동으로 안 되나요?
**A:** Claude Web은 로컬 파일을 직접 못 읽어서, Projects 기능에 프롬프트를 복사해 넣어야 합니다. `_shared/prompts/claude-web/` 파일을 시스템 지침에 한 번만 붙여넣으면 됩니다.

---

## 9. 전체 구조 한눈에 보기

```
C:\Users\eykis\
│
├── workspace/                        ← ★ 모든 작업은 여기서
│   ├── AI_WORKSPACE_사용가이드.md     ← 이 문서
│   ├── CLAUDE.md                     ← AI가 제일 먼저 읽는 파일
│   ├── WORKSPACE_GUIDE.md            ← 상세 운영 규칙
│   ├── new-project.cmd / .sh         ← 새 프로젝트 만들기
│   ├── sync-tools.cmd / .sh          ← 리소스 동기화
│   │
│   ├── _shared/                      ← 공용 자료실 (원본 저장소)
│   │   ├── REGISTRY.md               ← 전체 리소스 목록
│   │   ├── AI_TOOLS_MAP.md           ← AI 도구별 설정 위치
│   │   ├── skills/ (23개)            ← 스킬 원본
│   │   ├── agents/ (12개)            ← 에이전트 원본
│   │   ├── workflows/ (7개)          ← 워크플로우 원본
│   │   ├── commands/ (3개)           ← 명령어
│   │   ├── prompts/                  ← 프롬프트 라이브러리
│   │   │   ├── common/              ← 공통 역할/톤 정의
│   │   │   ├── claude-web/          ← Claude Web용
│   │   │   └── cowork/             ← Claude Desktop용
│   │   └── templates/               ← 프로젝트 틀
│   │
│   ├── projects/                     ← 진행 중인 프로젝트들
│   │   ├── P2026-001_장애인_B2B사업/
│   │   ├── P2026-002_AX진단_컨설팅도구/
│   │   ├── P2026-003_직무디자인_연구용역/
│   │   └── P2026-004_나라장터_웹앱/
│   │
│   ├── archive/                      ← 끝난 프로젝트 보관함
│   └── outputs/                      ← 최종 산출물 모음
│
├── .claude/                          ← Claude Code 전역 설정 (건드리지 않기)
│   └── skills/ (22개)               ← Tier 1 스킬 (항상 자동 로드)
│
└── .agents/                          ← 예비 폴더 (향후 확장용)
```

---

> **기억할 것 하나**: 그냥 하고 싶은 일을 한국어로 말하세요. 나머지는 AI가 합니다.
