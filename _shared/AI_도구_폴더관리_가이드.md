# AI 도구 활용 시 폴더 관리 가이드

> 이석주님의 현재 폴더 상태를 분석하고, Claude Code + Antigravity 환경에 최적화된 관리 방안을 정리했습니다.

---

## 1. 현재 상태 진단

### 발견된 문제점

**OneDrive 루트에 파일 100+개가 분류 없이 존재**
- pptx 47개, xlsx 25개, pdf 24개 등이 플랫하게 나열
- 같은 문서의 버전 파일이 v1, v2, v3... 으로 계속 쌓여 있음 (예: 한국화학융합시험연구원 제안서가 v1.1~v5.1까지 7개)
- 업무 프로젝트별 구분이 없음

**AI 도구 설정 폴더가 프로젝트마다 중복 생성**
- 홈 폴더: `.claude`, `.agents`, `.antigravity`, `.gemini`
- `Antigravity/` 안: `.agent`, `.agents`, `.claude`
- `project/` 안: `.agent`, `.agents`, `.claude`
- `project/claude-code-harness/` 안: `.claude` (agents, commands, skills 포함)
- 총 4곳에 걸쳐 AI 설정이 흩어져 있음

**OneDrive/문서 폴더도 혼잡**
- 업무 파일, 개인 파일, 게임 폴더(League of Legends, My Games), 앱 데이터(UPDF, Zoom, CyberLink)가 뒤섞여 있음
- github 토큰 등 민감 정보가 텍스트 파일로 저장되어 있음

---

## 2. OneDrive 파일 정리 방안

### 권장 폴더 구조

```
OneDrive/
├── 01_컨설팅_프로젝트/
│   ├── 2023_산업전환_대한상의/
│   ├── 2023_DX아카데미/
│   ├── 2023_일터혁신_씨씨앤아이/
│   ├── 2024_국가임상시험지원재단/
│   ├── 2024_SK오션플랜트/
│   ├── 2024_한국화학융합시험연구원/
│   ├── 2024_부산과기대_DX직업전환/
│   ├── 2024_대우경영_장애인직무개발/
│   ├── 2024_대우경영_직무디자인/
│   ├── 2024_한국전자기술연구원/
│   ├── 2024_간호인력_역량체계/
│   └── 2025_일터혁신_진테크/
│
├── 02_내부업무/
│   ├── 실적_보고/          ← 본부 실적, 분기별 정리
│   ├── 지출_경비/          ← 지출결의서, 품의서
│   └── NCS_가이드북/       ← NCS 관련 연구/가이드
│
├── 03_제안서_템플릿/       ← 범용 양식, 재사용 자료
│
├── 04_학습_연구/
│   ├── HR애널리틱스/
│   ├── 통계/
│   └── 프롬프트엔지니어링/
│
├── 05_개인/
│   ├── 인감_서류/
│   └── 기타/
│
├── 문서/                   ← 기존 유지 (OneDrive 시스템 폴더)
├── 사진/
└── 첨부 파일/
```

### 정리 원칙

1. **연도_프로젝트명** 형식으로 폴더 생성 → 같은 프로젝트의 모든 버전 파일을 한 폴더에
2. 최종본만 루트에 두고, 중간 버전은 하위 `_archive/` 폴더로 이동
3. 프로젝트 완료 후에는 폴더 앞에 `[완료]` 접두사 추가

### 버전 관리 팁

현재 같은 파일의 v1~v5가 동일 폴더에 있어 혼란스럽습니다.

- **진행 중 프로젝트**: `최종본.pptx` + `_archive/` 폴더에 이전 버전 보관
- **완료된 프로젝트**: 최종본만 남기고 나머지는 `_archive/`로
- 파일명 규칙: `[기관명]_프로젝트명_최종.확장자` 또는 `[기관명]_프로젝트명_v날짜.확장자`

---

## 3. AI 도구 폴더 정리

### 현재 중복 현황

| 위치 | .claude | .agents | .agent | 비고 |
|------|---------|---------|--------|------|
| `~/` (홈) | O | O | - | Claude Code 전역 설정 |
| `~/Antigravity/` | O | O | O | Antigravity 프로젝트 |
| `~/project/` | O | O | O | 사업 기획 프로젝트 |
| `~/project/claude-code-harness/` | O | - | - | Claude Code harness |

### 정리 전략

**원칙: AI 도구 설정 폴더는 "프로젝트 루트"에만 두기**

#### Claude Code (`.claude`, `.claude.json`)

Claude Code는 작업 디렉토리 기준으로 설정을 찾습니다. 따라서:

- **홈 폴더의 `.claude.json`**: 전역 설정으로 유지 (건드리지 않기)
- **홈 폴더의 `.claude/`**: 전역 캐시/히스토리 → 유지
- **각 프로젝트 안의 `.claude/`**: 해당 프로젝트 전용 설정 → 프로젝트와 함께 관리
- 불필요한 프로젝트를 삭제하면 안의 `.claude/`도 함께 정리됨

**실천 방법:**
```
# Claude Code를 실행할 때 항상 프로젝트 루트에서 시작
cd ~/project/claude-code-harness
claude

# 홈 디렉토리에서 claude 실행 → 홈에 설정 파일 생성됨 (피하기)
```

#### Antigravity (`.antigravity`, `.agent`, `.agents`)

- `~/.antigravity/`: Antigravity 앱 자체 설정 → 유지
- `~/Antigravity/` 폴더: Antigravity 프로젝트 → 유지하되 내부 정리
- `~/Antigravity/.agent`, `~/Antigravity/.agents`: Antigravity가 자동 생성 → 유지

#### 권장 프로젝트 구조

```
홈 폴더/
├── .claude.json              ← Claude Code 전역 설정 (유지)
├── .claude/                  ← Claude Code 전역 데이터 (유지)
├── .antigravity/             ← Antigravity 앱 설정 (유지)
├── .gemini/                  ← Gemini 설정 (유지)
│
├── projects/                 ← 모든 AI 프로젝트를 여기 아래에 통합
│   ├── claude-code-harness/  ← 기존 project/claude-code-harness 이동
│   ├── antigravity-b2b/      ← 기존 Antigravity/ 내용 이동
│   └── business-plan/        ← 기존 project/ 의 사업 기획 문서들
│
├── OneDrive/                 ← 업무 파일 (위의 정리안 적용)
└── Documents/                ← 시스템 폴더
```

---

## 4. AI 도구 활용 시 베스트 프랙티스

### 4.1 Claude Code 사용 시

**프로젝트별 격리 원칙**
- 항상 프로젝트 폴더로 이동한 후 `claude` 실행
- 홈 디렉토리에서 직접 실행하면 홈에 설정 파일이 생성되어 지저분해짐
- `CLAUDE.md` 파일을 프로젝트 루트에 만들어두면 프로젝트 컨텍스트를 자동 인식

**설정 파일 관리**
- `.claude/settings.json`: 프로젝트별 설정 (MCP 서버, 허용 도구 등)
- `.claude/commands/`: 커스텀 슬래시 명령어
- `.claude/skills/`: 프로젝트 전용 스킬
- 이 파일들은 Git에 포함시켜도 됨 (민감 정보 제외)

**CLAUDE.md 활용**
```markdown
# 프로젝트명

## 개요
이 프로젝트는 ...

## 기술 스택
- Python, FastAPI, Next.js

## 주요 규칙
- 한국어로 커밋 메시지 작성
- 테스트 필수
```

### 4.2 Antigravity 사용 시

- Antigravity는 `.agent/`, `.agents/` 폴더를 프로젝트 루트에 자동 생성
- 이 폴더 안에는 워크플로우 정의, 스킬 등이 포함됨
- 프로젝트를 옮길 때 이 폴더도 함께 이동해야 설정이 유지됨

### 4.3 공통 습관

1. **프로젝트 시작 시**: 전용 폴더를 먼저 만들고, 그 안에서 AI 도구 실행
2. **프로젝트 완료 시**: 결과물은 OneDrive로 복사, 프로젝트 폴더는 아카이브
3. **주기적 정리**: 월 1회 `~/.claude/cache/` 등 캐시 폴더 정리
4. **민감 정보**: `.env`, 토큰, API 키는 절대 OneDrive에 올리지 않기

---

## 5. 즉시 실행 가능한 액션 플랜

### 지금 바로 할 수 있는 것

1. **OneDrive 루트 정리**: 위의 폴더 구조대로 하위 폴더 생성 후 파일 이동
2. **`github_깃허브_개인 액세스 토큰.txt`**: OneDrive/문서에서 즉시 삭제하고 안전한 곳(1Password 등)으로 이동
3. **빈 `cowork/` 폴더**: 사용하지 않으면 삭제

### 이번 주에 할 것

4. **`~/project/`와 `~/Antigravity/` 통합**: 하나의 `~/projects/` 아래로 정리
5. **OneDrive/문서 정리**: 게임 폴더, 앱 데이터를 적절한 위치로 분리

### 습관으로 만들 것

6. 새 프로젝트 시작 시 반드시 전용 폴더 생성 → 그 안에서 AI 도구 실행
7. 완료된 프로젝트는 `[완료]` 접두사 추가 또는 archive 폴더로 이동
8. 월 1회 캐시 정리: `.claude/cache/`, `.claude/debug/` 등

---

## 6. 주의사항

- **`.claude.json` (홈 폴더)**: 절대 삭제하지 마세요. Claude Code 전역 설정입니다.
- **`.antigravity/`**: Antigravity 앱 설정이므로 유지하세요.
- **OneDrive 동기화**: 폴더 이동 시 OneDrive 동기화가 완료된 후 진행하세요.
- **AI 설정 폴더(`.claude/`, `.agent/`)를 OneDrive에 넣지 마세요**: 동기화 충돌이 발생할 수 있습니다.
- **파일 이동 전 백업**: 중요 파일은 이동 전 복사본을 먼저 만들어두세요.
