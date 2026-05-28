# VRIN AI Hub — 시앤피컨설팅 AI 마스터 체계

> AI 도구가 이 워크스페이스에서 작업할 때 가장 먼저 읽는 전역 컨텍스트.
> **최종 업데이트**: 2026-05-28

---

## 사용자 프로필
- **이석주** — 시앤피컨설팅 HR 솔루션팀 팀장
- **비개발자** — 일상적인 한국어로 지시. CLI 명령어 사용 안 함.
- **전문 분야**: HR 컨설팅(HRM/HRD/OD), 사업기획, 경영전략, 조직관리

## 작업 환경 — 3-디바이스 통합

| 디바이스 | 역할 | 특징 |
|----------|------|------|
| 💻 노트북 (회사/현장) | **풀-기능 주력** | 데스크탑과 100% 동등 — 심층 분석·대량 산출물 가능 |
| 🖥️ 데스크탑 (집/야간) | **풀-기능 주력** | 노트북과 동등 — 위치만 다름 |
| 📱 핸드폰 (이동 중) | 빠른 손 (보조) | Claude 앱·Claude Web Projects·Notion·OneDrive 앱 |

**원칙**: 노트북과 데스크탑은 같은 스킬·에이전트·플러그인·MCP·인증을 갖춘 동등 환경. 디바이스 패리티 점검: [`DEVICE_PARITY_CHECKLIST.md`](DEVICE_PARITY_CHECKLIST.md)

---

## 핵심 원칙

### 1. 한국어 자연어 인터페이스
- 사용자는 **일상 한국어**로 지시 (CLI 명령어 X)
- AI가 의도를 파악해 적절한 도구·스킬·에이전트를 **자동 선택·실행**
- 모든 응답·문서·산출물은 **한국어**
- 기술 용어 대신 쉬운 말로 설명 (필요 시 용어 병기)

### 2. 자동 리소스 매칭 (그리스신화 에이전트 라우팅)

| 사용자 말 | 리드 에이전트 | 자동 적용 스킬 |
|-----------|---------------|---------------|
| "전략 수립해줘" | **Athena** | strategic-management |
| "시장조사 / 경쟁분석" | **Apollo** | data-analysis |
| "직무분석 / 조직진단 / 인사제도" | **Hera** | job-analysis, hr-consulting, org-diagnosis |
| "보고서 / 제안서 / 발표자료" | **Hermes** | consulting-report, proposal, pptx, docx |
| "사업계획서 / 재무 추정" | **Midas** | business-planning, data-analysis |
| "법률 검토 / 계약서 / NDA" | **Themis** | legal-consulting |
| "브랜딩 / 네이밍 / 마케팅" | **Aphrodite** | branding-marketing |
| "웹사이트 / 앱 만들어" | **Daedalus** | (Arachne·Talos·Iris·Helios·Nike) |
| "프로젝트 현황 / 일정" | **Chronos** | workspace-management |
| "새 프로젝트 만들어" | workspace-manager | — |
| "리소스 동기화" | — | `sync-tools.cmd` |

> 에이전트 체계 상세: [`projects/P0000-000_AI활용/CLAUDE.md`](projects/P0000-000_AI활용/CLAUDE.md)
> 전체 라우팅표: [`_core/REGISTRY.md`](_core/REGISTRY.md)

### 3. 컨설팅 품질 기준
- 전문적·공식적 톤
- 모든 주장에 근거(데이터·이론·사례) 제시
- 검증 프레임워크 활용 (SWOT, BSC, NCS, OKR 등)
- 한국 HR/노동 환경 반영
- 산출물은 **Ralph 루프**로 자동 품질 검증 → 등급 부여

---

## 워크스페이스 구조

```
vrin_AI_hub/
├── _core/                       ← AI 핵심 두뇌 (Single Source of Truth)
│   ├── REGISTRY.md              ← 전체 리소스 카탈로그 (150+)
│   ├── AI_TOOLS_MAP.md          ← AI 도구별 설정 경로
│   ├── SYSTEM_EVOLUTION_LOOP.md ← 자기진화·지속 업데이트 메커니즘
│   ├── skills/ (25개)           ← Tier 2 컨설팅·HR·경영·법률·브랜드
│   ├── agents/ (21개)           ← 그리스신화 9 + 기술/개발 12
│   ├── workflows/ (9개)         ← Ralph + Pygmalion + 레거시 7
│   ├── commands/                ← 워크스페이스 커맨드
│   ├── prompts/                 ← 크로스도구 프롬프트 라이브러리
│   ├── quality-contracts/       ← 산출물 품질 기준
│   └── templates/               ← 프로젝트 템플릿
├── projects/                    ← 활성 프로젝트 (15개: P0000 영구 3 + P2026 12)
├── archive/                     ← 완료 프로젝트
└── outputs/                     ← 최종 산출물 모음 (도메인별 자동 분류)
```

---

## 프로젝트 관리

### 프로젝트 번호 체계
```
P{년도}-{일련번호}_{프로젝트명}

P0000-XXX = 영구·취미·메타 (AI 활용, 학습, 도서, 창작 등)
P{연도}-XXX = 해당 연도 업무 (P2026, P2027, ...)
```

### 생명주기
- **생성**: `new-project.cmd "프로젝트명"` → 자동 폴더·리소스 연결
- **진행**: `projects/P{XX}-XXX_*/` 에서 작업
- **완료**: `projects/` → `archive/` 이동
- **산출물**: 프로젝트 `outputs/`에 저장, 필요 시 루트 `outputs/`에 복사

---

## 스킬 체계 (2-Tier)

- **Tier 1** (전역, 69개): `~/.claude/skills/` — AI/개발/콘텐츠 스킬 (자동 로드)
- **Tier 2** (워크스페이스, 25개): `_core/skills/` — 컨설팅·HR·경영·법률·브랜드 스킬 (프로젝트 배포)
- 상세: [`_core/REGISTRY.md`](_core/REGISTRY.md)

---

## 자기진화 메커니즘 (Ralph + Pygmalion)

이 시스템은 **시간이 갈수록 더 똑똑해지도록** 설계됨:

- **매 산출물**: Ralph 루프 → 품질 검증·등급 부여
- **매주 월요일**: 신규 패턴·스킬 후보 수집
- **매월 말일**: 가이드 vs 실제 정합성 점검
- **매분기**: Pygmalion 진화 사이클 (정리·승격·폐기)

상세: [`_core/SYSTEM_EVOLUTION_LOOP.md`](_core/SYSTEM_EVOLUTION_LOOP.md)

---

## 자주 쓰는 산출물 유형

- 직무분석 보고서 (pptx, xlsx)
- 제안서·발표자료 (pptx)
- 컨설팅 결과보고서 (pptx, pdf)
- 사업계획서 (pptx, docx)
- 훈련과정 로드맵 (pptx, xlsx)
- 데이터 분석 결과 (xlsx)
- 조직진단 보고서 (pptx)
- 경영전략 보고서 (pptx)

---

## 참조 문서

- 운영 가이드: [`WORKSPACE_GUIDE.md`](WORKSPACE_GUIDE.md)
- 리소스 카탈로그: [`_core/REGISTRY.md`](_core/REGISTRY.md)
- AI 도구 맵: [`_core/AI_TOOLS_MAP.md`](_core/AI_TOOLS_MAP.md)
- 멀티디바이스 가이드: [`MULTI_DEVICE_GUIDE.md`](MULTI_DEVICE_GUIDE.md)
- 디바이스 패리티: [`DEVICE_PARITY_CHECKLIST.md`](DEVICE_PARITY_CHECKLIST.md)
- 자기진화 루프: [`_core/SYSTEM_EVOLUTION_LOOP.md`](_core/SYSTEM_EVOLUTION_LOOP.md)
