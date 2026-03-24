# OhMyOpenAgent (OhMyOpenCode) - 아키텍처 분석

**저장소**: https://github.com/code-yeongyu/oh-my-openagent  
**버전**: 3.11.0  
**타입**: OpenCode 플러그인 (다중 에이전트 오케스트레이션 프레임워크)  
**언어**: TypeScript (Bun 런타임)  
**규모**: 1,427개 파일, ~40,000 LOC

---

## 핵심 요약

OhMyOpenAgent는 **단일 AI 에이전트를 조직화된 개발팀으로 변환**하는 다중 모델 오케스트레이션 프레임워크입니다.

**핵심 혁신**: 하나의 에이전트가 모든 것을 하는 대신, **의도 기반 위임(intent-based delegation)**을 사용하여 작업을 분류하고 전문가에게 자동으로 라우팅합니다.

---

## 아키텍처 개요

### 3계층 시스템

```
┌─────────────────────────────────────────────────────────────┐
│ 계획 계층 (Planning Layer)                                   │
│ ├─ Prometheus: 전략 계획가 (인터뷰 모드)                     │
│ ├─ Metis: 갭 분석가                                         │
│ └─ Momus: 계획 검토자                                       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 오케스트레이션 계층 (Orchestration Layer)                    │
│ ├─ Atlas: 지휘자 (작업 분배)                                │
│ ├─ 계획 읽기                                                │
│ ├─ 작업 분석                                                │
│ ├─ 학습 축적                                                │
│ └─ 결과 검증                                                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 워커 계층 (Worker Layer)                                     │
│ ├─ Sisyphus: 메인 오케스트레이터                            │
│ ├─ Hephaestus: 자율 심화 작업자 (GPT 네이티브)             │
│ ├─ Oracle: 아키텍처 컨설턴트                               │
│ ├─ Librarian: 문서/OSS 검색                                │
│ ├─ Explore: 빠른 코드베이스 grep                           │
│ ├─ Sisyphus-Junior: 작업 실행자                            │
│ ├─ Multimodal-Looker: 비전/스크린샷 분석                   │
│ └─ [커스텀 에이전트]                                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 핵심 컴포넌트

### 1. 에이전트 (11개 내장)

| 에이전트 | 목적 | 모델 | 비용 |
|---------|------|------|------|
| **Sisyphus** | 메인 오케스트레이터 | Claude Opus 4.6 / Kimi K2.5 | 높음 |
| **Hephaestus** | 자율 심화 작업 | GPT-5.3 Codex | 높음 |
| **Prometheus** | 전략 계획 | Claude Opus 4.6 | 높음 |
| **Atlas** | 작업 분배 | Claude Sonnet 4.6 | 높음 |
| **Oracle** | 아키텍처 컨설팅 | GPT-5.4 | 높음 |
| **Librarian** | 문서/OSS 검색 | Gemini 3 Flash | 낮음 |
| **Explore** | 코드베이스 grep | Grok Code Fast | 낮음 |
| **Metis** | 갭 분석 | Claude Opus 4.6 | 높음 |
| **Momus** | 계획 검토 | GPT-5.4 | 높음 |
| **Multimodal-Looker** | 비전 분석 | Claude Vision | 높음 |
| **Sisyphus-Junior** | 작업 실행 | Claude Sonnet 4.6 | 높음 |

### 2. 도구 (26개)

**코드 조작:**
- `hashline-edit` — 해시 앵커 편집 (안전한 변경)
- `ast-grep` — 패턴 인식 코드 검색/재작성
- `lsp` — IDE 수준의 도구 (rename, goto-def, find-refs)
- `glob` — 파일 패턴 매칭
- `grep` — 콘텐츠 검색

**실행:**
- `interactive-bash` — 대화형 터미널 (Tmux)
- `background-task` — 병렬 에이전트 실행
- `task` — 작업 생성/관리

**에이전트 제어:**
- `delegate-task` — 전문가에게 작업 라우팅
- `call-omo-agent` — 직접 에이전트 호출
- `slashcommand` — 슬래시 명령 실행

### 3. 기능 (19개 모듈)

**핵심 오케스트레이션:**
- `background-agent` — 병렬 에이전트 실행
- `boulder-state` — Sisyphus 루프 상태 추적
- `run-continuation-state` — 연속 모드 상태

**스킬 & 명령:**
- `builtin-skills` — 7개 내장 스킬 (git-master, playwright, frontend-ui-ux 등)
- `builtin-commands` — 슬래시 명령 (ultrawork, start-work, init-deep 등)
- `opencode-skill-loader` — .opencode/skills/ 에서 스킬 로드

**통합:**
- `claude-code-agent-loader` — Claude Code 에이전트 로드
- `claude-code-command-loader` — Claude Code 명령 로드
- `claude-code-mcp-loader` — Claude Code MCP 로드
- `skill-mcp-manager` — 스킬 임베디드 MCP 관리

### 4. 훅 (48개 - 3계층 시스템)

**계층 1: 핵심 훅 (39개)**
- 세션 라이프사이클 (created, deleted, idle, error)
- 채팅 메시지 처리
- 도구 실행 가드 (파일 가드, 라벨 트렁케이터)
- 컨텍스트 주입 및 변환

**계층 2: 연속 훅 (7개)**
- 작업 연속 추적
- Todo 보존
- 컴팩션 컨텍스트 주입

**계층 3: 스킬 훅 (2개)**
- 스킬 특정 라이프사이클 훅

### 5. 설정 시스템

**3계층 설정:**
```
프로젝트 (.opencode/oh-my-opencode.jsonc)
    ↓
사용자 (~/.config/opencode/oh-my-opencode.jsonc)
    ↓
기본값 (내장)
```

**설정 스키마 (Zod v4):**
- 14개 오버라이드 가능한 에이전트
- 8개 내장 카테고리 + 커스텀
- 6개 disabled_* 배열
- 19개 기능별 설정

### 6. 스킬 시스템

**스킬이란?**
- 도메인 튜닝된 시스템 지시사항
- 임베디드 MCP 서버 (온디맨드, 스코프됨)
- 스코프된 권한
- 에이전트 간 재사용 가능

**내장 스킬 (7개):**
1. `git-master` — 원자적 커밋, 리베이스 수술, 히스토리 고고학
2. `playwright` — 브라우저 자동화
3. `frontend-ui-ux` — 디자인 우선 UI 개발
4. `dev-browser` — 개발 브라우저 통합
5. `playwright-cli` — CLI 기반 브라우저 자동화
6. `dev-browser-cli` — CLI 기반 개발 브라우저

### 7. MCP 시스템 (3계층)

| 계층 | 소스 | 메커니즘 |
|------|------|---------|
| **내장** | src/mcp/ | 3개 원격 HTTP: websearch, context7, grep_app |
| **Claude Code** | .mcp.json | ${VAR} 환경 변수 확장 |
| **스킬 임베디드** | SKILL.md YAML | SkillMcpManager로 관리 |

---

## 설계 패턴 & 철학

### 1. 의도 기반 위임 (Intent-Based Delegation)

모델 이름으로 라우팅하는 대신, **의도로 분류**하고 전문가에게 자동 라우팅:

```
사용자 요청
    ↓
[의도 게이트] — 사용자가 실제로 원하는 것은?
    ↓
[카테고리 분류] — visual-engineering? deep? quick? ultrabrain?
    ↓
[모델 할당] — 최적 모델로 자동 라우팅
```

**카테고리:**
- `visual-engineering` → Gemini (프론트엔드/UI)
- `deep` → GPT-5.3 Codex (자율 연구)
- `quick` → GPT-5.4 Mini (속도)
- `ultrabrain` → GPT-5.4 (어려운 로직)
- `unspecified-high` → Claude Opus (기본값)

### 2. 계획과 실행의 분리

**계획 단계:**
- Prometheus가 사용자 인터뷰
- Metis가 갭 분석
- Momus가 계획 검증
- 출력: `.sisyphus/plans/*.md`

**실행 단계:**
- Atlas가 계획 읽기
- 워커에게 작업 분배
- 학습 축적
- 결과 검증

### 3. 해시 앵커 편집 (Hashline)

"harness problem" 해결 — 에이전트가 본 콘텐츠를 안정적으로 재현할 수 없음:

```
11#VK| function hello() {
22#XJ|   return "world";
33#MB| }
```

에이전트가 콘텐츠가 아닌 해시 태그로 편집. 파일이 변경되면 해시가 일치하지 않음 → 손상 전에 편집 거부.

**영향**: 6.7% → 68.3% 성공률 (Grok Code Fast 1)

### 4. 병렬 백그라운드 에이전트

메인 에이전트가 계속 진행하는 동안 5+ 에이전트를 병렬로 실행:

```
메인 에이전트: "코드베이스를 이해해야 함"
    ↓
[백그라운드] Explore: 패턴 grep
[백그라운드] Librarian: 문서 검색
[백그라운드] Oracle: 아키텍처 검토
    ↓
메인 에이전트: "필요할 때 결과 준비됨"
```

### 5. 스킬 임베디드 MCP

MCP는 보통 컨텍스트 예산을 소비. OmO가 해결:

```
스킬 = 도메인 지시사항 + 임베디드 MCP
    ↓
MCP는 온디맨드로 시작
    ↓
작업으로 스코프됨
    ↓
완료 시 정리
```

### 6. 동적 에이전트 프롬프트 빌딩

Sisyphus 프롬프트는 **동적으로 생성**:
- 사용 가능한 에이전트
- 사용 가능한 도구
- 사용 가능한 스킬
- 사용 가능한 카테고리
- 모델별 최적화

### 7. 모델별 프롬프트 변형

다른 모델은 다른 프롬프트를 받음:

- **Claude**: 완전한 오케스트레이션, 위임 중심
- **GPT-5.4**: 추론 중심, 검증 중심
- **Gemini**: 비전 우선, 창의성 중심
- **Kimi**: Claude 유사, 위임 중심

### 8. 3계층 훅 시스템

```
세션 훅 (23개)
    ↓
도구 가드 훅 (12개)
    ↓
변환 훅 (4개)
    ↓
연속 훅 (7개)
    ↓
스킬 훅 (2개)
```

---

## 개발자 중심 설계

### 1. **CLI 우선 인터페이스**
- 명령: `ultrawork`, `ulw`, `/start-work`, `/init-deep`
- 슬래시 명령으로 에이전트 제어
- 대화형 터미널 (Tmux) 디버깅

### 2. **코드 중심 도구**
- LSP 통합 (IDE 수준의 정밀도)
- AST-Grep (패턴 인식 재작성)
- 해시 앵커 편집 (코드 안전성)
- Git 통합 (원자적 커밋)

### 3. **개발자 워크플로우**
- 리팩토링 모드 (안전성 우선)
- 처음부터 빌드 모드 (발견)
- 아키텍처 컨설팅 (Oracle)
- 디버깅 지원 (대화형 bash)

### 4. **기술 설정**
- JSONC 설정 파일
- Zod 스키마 검증
- 모델 오버라이드 시스템
- 훅 커스터마이제이션

### 5. **개발자 마인드셋**
- "AI slop 없음" 철학
- 코드 품질 강제
- 댓글 검사기 (AI 생성 댓글 없음)
- 원자적 커밋 (규율)

### 6. **개발자를 위한 확장성**
- 설정을 통한 커스텀 에이전트
- 커스텀 스킬 (SKILL.md 형식)
- 커스텀 명령
- 커스텀 MCP
- 깊은 커스터마이제이션을 위한 훅 시스템

---

## 비개발자를 위한 적응 필요 사항

### 1. **인터페이스 계층**
- ❌ CLI 명령 → ✅ 자연어 ("이 작업을 해줘")
- ❌ 슬래시 명령 → ✅ 대화형 트리거
- ❌ 설정 파일 → ✅ UI 기반 설정 마법사
- ❌ 터미널 출력 → ✅ 진행 대시보드

### 2. **용어**
- ❌ "Oracle에 위임" → ✅ "전문가 조언 받기"
- ❌ "ultrawork 실행" → ✅ "이것에 대해 작업 시작"
- ❌ "해시 앵커 편집" → ✅ "안전한 변경"
- ❌ "AST-Grep" → ✅ "패턴 찾기 및 바꾸기"

### 3. **워크플로우 단순화**
- ❌ 계획 → 실행 → 검증 → ✅ 그냥 "해줘"
- ❌ 모델 선택 → ✅ 자동 (숨김)
- ❌ 훅 설정 → ✅ 합리적인 기본값
- ❌ 스킬 생성 → ✅ 가이드 템플릿

### 4. **출력 형식**
- ❌ JSON/YAML 설정 → ✅ 폼/마법사
- ❌ Markdown 계획 → ✅ 시각적 로드맵
- ❌ 터미널 로그 → ✅ 진행 바 + 요약
- ❌ 코드 diff → ✅ 평문 "무엇이 변경되었나"

### 5. **에러 처리**
- ❌ "훅 실행 실패" → ✅ "뭔가 잘못됐어, 다시 시도 중"
- ❌ "모델 사용 불가" → ✅ "백업 옵션 사용 중"
- ❌ "설정 검증 오류" → ✅ "이거 고쳐줄게"

### 6. **스킬/명령 시스템**
- ❌ SKILL.md with YAML → ✅ "새 기능 추가" 마법사
- ❌ MCP 설정 → ✅ "서비스 연결" 플로우
- ❌ 훅 등록 → ✅ 자동 감지

---

## 디렉토리 구조

```
oh-my-openagent/
├── src/
│   ├── index.ts                    # 플러그인 진입점
│   ├── plugin-config.ts            # 설정 로딩 & 병합
│   ├── plugin-interface.ts         
