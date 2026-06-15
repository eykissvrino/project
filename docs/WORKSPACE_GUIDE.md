# 워크스페이스 운영 가이드

> AI 도구(Claude Code, Claude Desktop, Claude Web, Antigravity, Gemini 등)가 이 워크스페이스에서 작업할 때 반드시 참조해야 하는 규칙입니다.
>
> **최종 업데이트**: 2026-05-28

---

## 1. 비전 — "One Brain, Two Equals + One Quick-Hand"

```
                  ☁️ OneDrive + GitHub
                 (하나의 뇌 — 모든 지식·맥락·산출물)
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
    💻 노트북          🖥️ 데스크탑         📱 핸드폰
   (회사/현장)         (집/야간)          (이동 중)
   ════════════       ════════════       ────────────
   풀-기능 주력         풀-기능 주력       빠른 손
   ← 100% 동등 →                        포착·확인·승인
```

**노트북 = 데스크탑** (물리적 위치만 다름, 기능 동등). 핸드폰은 보조.
디바이스 패리티 보장: [`DEVICE_PARITY_CHECKLIST.md`](DEVICE_PARITY_CHECKLIST.md)

---

## 2. 워크스페이스 구조

```
vrin_AI_hub/  (OneDrive 동기화 영역)
├── CLAUDE.md                    ← AI가 최초 읽는 전역 컨텍스트
├── WORKSPACE_GUIDE.md           ← 이 문서 (운영 규칙)
├── MULTI_DEVICE_GUIDE.md        ← 3-디바이스 운영
├── DEVICE_PARITY_CHECKLIST.md   ← 노트북·데스크탑 동등성 점검
├── new-project.cmd / .sh        ← 새 프로젝트 생성
├── sync-tools.cmd               ← ★ _core → 활성 프로젝트 배포
├── backup-user-settings.cmd     ← Tier 1 스킬·플러그인·설정 백업
│
├── _core/                       ← 모든 프로젝트 공용 리소스 (Single Source of Truth)
│   ├── REGISTRY.md              ← ★ 전체 리소스 마스터 카탈로그 (150+)
│   ├── AI_TOOLS_MAP.md          ← AI 도구 설정 맵
│   ├── SYSTEM_EVOLUTION_LOOP.md ← ★ 자기진화·지속 업데이트 메커니즘
│   ├── skills/ (25개)           ← Tier 2 컨설팅·HR·경영·법률·브랜드 스킬
│   ├── agents/ (21개)           ← 그리스신화 9 + 기술/개발 12
│   ├── workflows/ (9개)         ← Ralph + Pygmalion + 레거시 7
│   ├── commands/                ← 워크스페이스 커맨드
│   ├── quality-contracts/       ← 산출물 품질 기준
│   ├── prompts/                 ← 크로스도구 프롬프트 라이브러리
│   │   ├── common/
│   │   ├── claude-web/          ← Claude Web Projects용 (핸드폰)
│   │   └── cowork/              ← Claude Desktop용
│   └── templates/               ← 프로젝트 템플릿
│
├── projects/                    ← 활성 프로젝트 (15개)
│   ├── P0000-XXX_*              ← 영구·취미·메타
│   └── P{연도}-XXX_*            ← 연도별 업무
│
├── archive/                     ← 완료 프로젝트
└── outputs/                     ← 최종 산출물 모음
```

### 로컬 (OneDrive 외부, 각 PC별)
```
~/  (홈)
├── .claude/                     ← Claude Code 유저 설정 + Tier 1 스킬 69개
├── .git-repos/vrin_AI_hub/      ← Git 내부 데이터 (junction 대상)
├── .omc-local/vrin_AI_hub/      ← OMC 런타임 (junction)
└── .claude-local/vrin_AI_hub/   ← Claude 워크스페이스 캐시 (junction)
```

---

## 3. 프로젝트 번호 체계 (명문화)

### 형식
```
P{년도}-{일련번호}_{프로젝트명}
```

### 범주

| 범주 | 코드 패턴 | 용도 |
|------|----------|------|
| **영구·메타** | `P0000-XXX` | 연도 무관. AI 활용, 학습, 도서, 취미 등 장기 |
| **연도별 업무** | `P{연도}-XXX` | 해당 연도 사업·컨설팅 프로젝트 (P2026, P2027, ...) |

### 규칙
- 일련번호는 `new-project.cmd` / `.sh` 사용 시 자동 부여
- 프로젝트명에 공백 대신 언더스코어(`_`) 또는 한글 그대로
- 연도가 바뀌면 P{새연도}-001부터 재시작
- **P0000**은 연도 무관이므로 일련번호만 누적 (P0000-001, 002, ...)

### 예시
| 코드 | 의미 |
|------|------|
| `P0000-000_AI활용` | AI 도구·체계 관리 메타 프로젝트 |
| `P0000-001_월인가술빚는날` | 개인 창작/취미 |
| `P0000-002_Book` | 도서 집필/학습 |
| `P2026-001_장애인_B2B사업` | 2026년 첫 번째 업무 프로젝트 |
| `P2026-012_HRM_임금성과평가` | 2026년 12번째 업무 프로젝트 |

> 활성 프로젝트 전체 목록: [`_core/REGISTRY.md`](_core/REGISTRY.md) 1번 섹션

---

## 4. 스킬·에이전트 2-Tier 체계

### Tier 1 (유저 레벨, 전역, 69개)
- 위치: `~/.claude/skills/`
- 적용: 모든 프로젝트·모든 디바이스에서 자동 로드
- 성격: AI 도구·개발·콘텐츠 생성
- **양 PC 동기화**: `backup-user-settings.cmd`로 백업 → 다른 PC `setup-desktop.cmd`로 복원

### Tier 2 (워크스페이스 레벨, 25개)
- 위치: `_core/skills/`
- 적용: `sync-tools.cmd` 실행 시 프로젝트 `.claude/skills/`로 복사
- 성격: 컨설팅·HR·경영·법률·브랜드 업무 스킬
- **양 PC 동기화**: OneDrive가 자동

### 신규 스킬 판단

```
이 스킬은 모든 프로젝트에서 항상 필요한가?
  YES → Tier 1 (~/.claude/skills/)
  NO  → Tier 2 (_core/skills/)

컨설팅 업무 전용인가, AI/개발 범용인가?
  컨설팅 → Tier 2
  AI/개발 → Tier 1
```

> 전체 스킬·에이전트 목록: [`_core/REGISTRY.md`](_core/REGISTRY.md)

---

## 5. 그리스신화 에이전트 라우팅

사용자가 한국어로 말하면 AI가 자동 라우팅:

| 사용자 말 | 리드 에이전트 | 적용 스킬 |
|----------|--------------|-----------|
| "전략 수립해줘" | **Athena** | strategic-management |
| "시장조사 해줘" | **Apollo** | data-analysis |
| "직무분석 해줘" | **Hera** | job-analysis, hr-consulting |
| "조직진단 해줘" | **Hera** | org-diagnosis |
| "보고서 써줘" / "제안서 만들어줘" | **Hermes** | consulting-report, proposal, pptx |
| "사업계획서 만들어줘" | **Midas** | business-planning |
| "법률 검토해줘" / "계약서 검토" | **Themis** | legal-consulting |
| "브랜딩 / 네이밍 / 마케팅" | **Aphrodite** | branding-marketing |
| "웹사이트 / 앱 만들어" | **Daedalus** | (Arachne·Talos·Iris·Helios·Nike) |
| "프로젝트 현황 / 일정" | **Chronos** | workspace-management |
| "새 프로젝트 만들어" | workspace-manager | — |

---

## 6. 파일 저장 규칙

### 어디에 저장?
| 파일 유형 | 위치 | 예시 |
|----------|------|------|
| 작업 메모·초안 | `프로젝트/docs/` | 회의록, 분석 메모 |
| 원시 데이터 | `프로젝트/data/` | 설문 원본 |
| 최종 산출물 | `프로젝트/outputs/` | 보고서, 제안서 |
| 통합 산출물 모음 | `outputs/` (루트) | 여러 프로젝트 취합 |

### 파일명 규칙

**산출물**: `[유형]_[기관명]_[내용]_v버전.확장자`
- `결과보고서_한화연_산업전환진단_v2.1.pptx`
- `제안서_진테크_일터혁신_v1.0.pdf`

**작업 문서**: `날짜_내용.확장자`
- `20260528_킥오프회의_회의록.md`

**버전**: `_v1`, `_v2` → 최종 확정 시 `_최종`/`_final`

---

## 7. AI 도구별 작업 방법

### Claude Code (양 PC 주력)
```bash
cd ~/OneDrive/vrin_AI_hub/projects/P2026-001_장애인_B2B사업
claude
```
- Tier 1 스킬 69개 자동 로드
- 프로젝트 내 `.claude/skills/` (Tier 2 배포본) 자동 인식
- `CLAUDE.md` 자동 컨텍스트

### Claude Desktop (Cowork)
- 폴더 선택: `OneDrive/vrin_AI_hub/projects/{해당}` 또는 워크스페이스 루트
- 시스템 프롬프트: `_core/prompts/cowork/general-assistant.md`

### Claude Web (핸드폰·브라우저)
- claude.ai → Projects → New Project
- 인스트럭션: `_core/prompts/claude-web/` 폴더 파일 복사
- 산출물·파일 접근: OneDrive 모바일 앱과 병용

### Antigravity
- 작업 디렉토리: 해당 프로젝트
- `.agent/skills/`, `.agent/workflows/` 자동 인식

---

## 8. 프로젝트 생명주기

```
생성 → 진행 → 완료 → 아카이브
```

### 생성
```cmd
new-project.cmd "기관명_프로젝트명"   :: Windows
./new-project.sh "기관명_프로젝트명"  :: bash
```

### 진행
- 작업 폴더: `projects/P{연도}-XXX_*/`
- AI는 그리스신화 에이전트로 자동 라우팅
- 산출물 → 프로젝트 `outputs/`, 필요 시 루트 `outputs/`에 복사

### 완료 → 아카이브
- `projects/` → `archive/` 이동
- 새로 만든 스킬·프롬프트가 있으면 `_core/`에 승격 (Pygmalion 사이클)

---

## 9. 새 스킬·에이전트·워크플로우 추가

### 스킬 추가
**Tier 1 (전역 AI/개발)**:
```
~/.claude/skills/{새스킬명}/SKILL.md
```
→ 즉시 전역 사용 가능. 다른 PC에는 `backup-user-settings.cmd` 후 동기화.

**Tier 2 (워크스페이스 컨설팅)**:
```
_core/skills/{새스킬명}/SKILL.md
```
→ `sync-tools.cmd` 실행하면 활성 프로젝트 전체에 배포

### 에이전트 추가
```
_core/agents/{새에이전트}.md
```
→ `sync-tools.cmd`로 프로젝트 `.claude/agents/` + `.agent/workflows/`에 배포

### REGISTRY 갱신
- 새 리소스 추가 → 즉시 `_core/REGISTRY.md` 업데이트
- 분기 점검에서 Pygmalion이 자동 감지 (미등록 리소스 알림)

---

## 10. 자기진화 메커니즘

> 시스템이 **시간이 갈수록 더 똑똑해지도록** 설계됨.
> 상세: [`SYSTEM_EVOLUTION_LOOP.md`](SYSTEM_EVOLUTION_LOOP.md)

| 주기 | 트리거 | 작업 | 책임 |
|------|--------|------|------|
| 매 산출물 | 산출물 완성 | **Ralph 루프** — 품질 검증·등급 부여 | Hermes |
| 매주 (월요일) | 정기 | 신규 패턴·스킬 후보 수집 | 사용자 |
| 매월 (말일) | 정기 | 가이드 vs 실제 정합성 점검 | workspace-manager |
| 매분기 (3·6·9·12월) | 정기 | **Pygmalion 진화 사이클** — 정리·승격 | Pygmalion |
| 연 1회 | 정기 | archive 외부 백업 | 사용자 |

---

## 11. 워크스페이스 매니저 에이전트

전용 에이전트: `_core/agents/workspace-manager.md`

| 요청 | 수행 |
|------|------|
| "새 프로젝트 만들어" | 코드 부여 + 폴더 생성 + 리소스 연결 |
| "프로젝트 상태 보여줘" | 활성/아카이브 현황 |
| "워크스페이스 점검해" | 헬스체크 (가이드 정합성, 디바이스 패리티 등) |
| "산출물 정리해" | 프로젝트 → 전역 outputs 동기화 |
| "스킬 추가해" | 새 스킬 생성 + 전 프로젝트 배포 |
| "리소스 동기화" | sync-tools.cmd 실행 |
| "이 프로젝트 아카이빙해" | archive/ 이동 |

### 산출물 자동 분류
| 유형 | 확장자 | outputs/ 하위 |
|------|--------|--------------|
| 보고서 | .docx, .pdf, .md | documents/ |
| 프레젠테이션 | .pptx | presentations/ |
| 데이터 | .xlsx, .csv | data-analysis/ |
| 웹앱 | .html, 폴더 | web-apps/ |
| 모바일앱 | 폴더 | mobile-apps/ |
| 이미지 | .png, .svg | design/ |

---

## 12. 주의사항

- ❌ **홈 폴더에서 AI 도구 실행 금지** — 반드시 프로젝트 폴더로 이동
- ❌ **OneDrive에 .git/.claude/.omc 저장 금지** — junction으로 분리
- ❌ **민감 정보(API 키, 토큰)는 프로젝트 폴더에 저장 금지** — 1Password 등 별도 관리
- ❌ **archive 파일은 수정하지 말 것** — 필요 시 `projects/`로 복사 후 작업
- ✅ `_core/`는 직접 수정 가능 — 변경 후 REGISTRY 갱신 + sync-tools 실행

---

## 13. 참조

- 리소스 카탈로그: [`_core/REGISTRY.md`](_core/REGISTRY.md)
- AI 도구 맵: [`_core/AI_TOOLS_MAP.md`](_core/AI_TOOLS_MAP.md)
- 자기진화 루프: [`_core/SYSTEM_EVOLUTION_LOOP.md`](_core/SYSTEM_EVOLUTION_LOOP.md)
- 멀티디바이스: [`MULTI_DEVICE_GUIDE.md`](MULTI_DEVICE_GUIDE.md)
- 디바이스 패리티: [`DEVICE_PARITY_CHECKLIST.md`](DEVICE_PARITY_CHECKLIST.md)
- 전역 컨텍스트: [`CLAUDE.md`](CLAUDE.md)
