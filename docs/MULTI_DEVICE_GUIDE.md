# 멀티디바이스 운영 가이드 (v2)

> 노트북(회사/현장) + 데스크탑(집) + 핸드폰(이동)으로 AI 워크스페이스를 통합 활용하기 위한 운영 가이드
>
> **최종 업데이트**: 2026-05-28
> **변경 사항(v2)**: 노트북·데스크탑 **동등 풀-기능 환경** 모델로 재정의

---

## 1. 비전

### "One Brain, Two Equals + One Quick-Hand"

```
                    ☁️ OneDrive + GitHub
                    (하나의 뇌 — 모든 지식·맥락·산출물)
                              │
            ┌─────────────────┼─────────────────┐
            │                 │                 │
            ▼                 ▼                 ▼
        💻 노트북          🖥️ 데스크탑         📱 핸드폰
       (회사/현장)         (집/야간)          (이동 중)
       ════════════       ════════════       ────────────
        풀-기능 주력       풀-기능 주력        빠른 손
        ← 100% 동등 →                       포착·확인·승인
```

### 핵심 원칙
- **노트북 = 데스크탑**: 위치만 다른 동등 환경. 어디서든 같은 품질·속도로 작업
- **핸드폰**: 보조 인터페이스 (메모 입력, 산출물 열람, 진행 추적)
- **OneDrive**: 모든 지식·산출물의 단일 뇌
- **GitHub**: 변경 이력·백업 (주 1~2회 push)
- **각 PC 로컬**: AI 런타임 (`.git`, `.omc`, `.claude`)은 OneDrive 밖 junction

---

## 2. 아키텍처

```
                    ┌─────────────────────────┐
                    │     GitHub (이력/백업)   │
                    │  eykissvrino/project.git │
                    └────────────┬────────────┘
                                 │ 가끔 push/pull
                    ┌────────────▼────────────┐
                    │     OneDrive (실시간)    │
                    │  OneDrive\vrin_AI_hub\    │
                    │                          │
                    │  _core/ ✅ 자동동기화   │
                    │  projects/ ✅ 자동동기화 │
                    │  outputs/ ✅ 자동동기화  │
                    │  CLAUDE.md ✅            │
                    │  WORKSPACE_GUIDE.md ✅   │
                    │  MULTI_DEVICE_GUIDE.md ✅│
                    │                          │
                    │  .git ⛔ junction (제외) │
                    │  .omc ⛔ junction (제외) │
                    │  .claude ⛔ junction     │
                    │                          │
                    │  .desktop-setup/         │
                    │   user-settings-backup/  │
                    │   ← Tier 1 스킬 69개 백업│
                    └──┬──────────┬─────────┬──┘
                       │          │         │
              ┌────────▼───┐ ┌───▼────┐ ┌──▼──────────┐
              │ 💻 노트북  │ │📱 폰   │ │ 🖥️ 데스크탑│
              │ 풀-기능    │ │ Claude │ │ 풀-기능    │
              │ 주력 환경  │ │  앱    │ │ 주력 환경  │
              │            │ │+ Web   │ │            │
              │ .git 로컬  │ │  Project│ │ .git 로컬 │
              │ .omc 로컬  │ │+ Notion │ │ .omc 로컬 │
              │ .claude 로컬│ │+OneDrive│ │ .claude 로컬│
              └────────────┘ └────────┘ └────────────┘
```

### 동기화 방식

| 대상 | 방법 | 속도 |
|------|------|------|
| 문서·스킬·에이전트·산출물 (`_core/`, `projects/`, `outputs/`) | OneDrive 실시간 | 즉시 |
| Git 이력 (커밋·브랜치) | GitHub 수동 push/pull | 주 1~2회 |
| **Tier 1 스킬 (`~/.claude/skills/` 69개)** | `backup-user-settings.cmd` → `.desktop-setup/` → 다른 PC 복원 | 수동 (변경 시) |
| **플러그인·MCP·settings.json** | 위와 동일 — 백업 기반 동기화 | 수동 |
| AI 런타임 (`.git`, `.omc`, `.claude`) | 각 PC 로컬 (동기화 안 함) | — |

### 왜 이렇게 하는가
- **OneDrive + .git = 충돌 위험** → Junction으로 OneDrive 밖 분리
- **OneDrive 주문형 파일 = AI 느림** → "항상 이 장치에 유지" 설정 필수
- **각 PC 독립 실행** → 동시 사용 가능
- **양 PC 풀-기능 동등** → 디바이스 패리티 체크리스트로 보장

---

## 3. 디바이스별 역할

### 💻 노트북 (회사/현장)
- **풀-기능 주력 환경** (데스크탑과 100% 동등)
- 회사 업무, 현장 컨설팅, 출장, 미팅 후 즉시 작업
- Claude Code + 모든 Tier 1·Tier 2 스킬 + 모든 에이전트 + 모든 MCP
- **심층 분석·대량 산출물·장시간 작업 모두 가능**

### 🖥️ 데스크탑 (집/야간)
- **풀-기능 주력 환경** (노트북과 100% 동등)
- 집에서 야간/주말 작업, 멀티 모니터·대용량 처리 강점
- 노트북에서 시작한 작업을 끊김 없이 이어 받음

### 📱 핸드폰 (이동 중) — 보조
- Claude 앱: 빠른 질문, 아이디어 메모, 브레인스토밍
- Claude Web Projects (브라우저): `_core/prompts/claude-web/` 프롬프트 활용
- Notion 앱: 메모·할일·아이디어 기록
- OneDrive 앱: 산출물 PDF·PPT 열람·공유
- GitHub Mobile: 커밋·산출물 확인
- **한계**: PPTX·DOCX 직접 생성 불가, OMC 멀티에이전트 미지원

---

## 4. 일상 워크플로우

### 기본 루틴 (OneDrive 자동 동기화)
```
아침 (회사):
  노트북 켜기 → OneDrive 동기화 확인 → 바로 작업 시작

이동 (출장/외부):
  핸드폰으로 메모·아이디어 → Notion 또는 Claude Web Project
  → 다음 PC 접속 시 자동으로 컨텍스트 연결

저녁 (집):
  데스크탑 켜기 → OneDrive 동기화 확인 → 노트북 작업 이어서

※ git push/pull 없이도 OneDrive가 알아서 양쪽 최신 상태 유지
```

### Git 백업 루틴 (주 1~2회 권장)
```bash
cd OneDrive\vrin_AI_hub
git add -A
git commit -m "주간 백업 + 변경 요약"
git push origin main
```
Git은 **안전 백업·버전 이력** 용도. 일상 동기화는 OneDrive가 처리.

### 동시 사용 시나리오
```
✅ 가능: 노트북에서 P2026-001 작업 + 데스크탑에서 P2026-003 작업
✅ 가능: 노트북에서 보고서 작성 + 데스크탑에서 데이터 분석
✅ 가능: 하나 끝내고 다른 PC에서 이어서 작업

⚠️ 주의: 양쪽에서 정확히 같은 파일을 동시 수정
   → OneDrive가 "파일명 (Desktop).ext" 충돌본 생성
   → 데이터 손실 없음, 나중에 하나 골라서 정리
```

---

## 5. 리소스 업데이트 흐름

### 자동 동기화 (OneDrive)
어느 PC에서든 수정하면 다른 PC에 자동 반영:

| 리소스 | 위치 | 반영 |
|--------|------|------|
| Tier 2 스킬 (25개) | `_core/skills/` | 즉시 |
| 에이전트 (21개) | `_core/agents/` | 즉시 |
| 워크플로우 (9개) | `_core/workflows/` | 즉시 |
| 가이드 문서 | `WORKSPACE_GUIDE.md`, `CLAUDE.md` 등 | 즉시 |
| 프로젝트 CLAUDE.md | 각 프로젝트 루트 | 즉시 |
| 산출물 | `projects/*/outputs/` | 즉시 |

### 수동 배포 (sync-tools.cmd)
`_core/` 수정 후, 각 프로젝트의 `.claude/agents/` 등에 반영:
```cmd
cd OneDrive\vrin_AI_hub
sync-tools.cmd
```
**양쪽 PC에서 각각 실행** (각자의 활성 프로젝트에 배포).

### Tier 1 스킬·플러그인·MCP 동기화 (수동, 가장 중요)

양 PC 패리티 유지를 위해 **변경 시 즉시 백업**:

```cmd
:: 변경한 PC에서 백업 갱신
cd OneDrive\vrin_AI_hub
backup-user-settings.cmd
git add .desktop-setup/
git commit -m "user settings backup"
git push

:: 다른 PC에서 복원
cd OneDrive\vrin_AI_hub
git pull
:: setup-desktop.cmd 또는 수동 복원
```

상세 점검: [`DEVICE_PARITY_CHECKLIST.md`](DEVICE_PARITY_CHECKLIST.md)

---

## 6. 핸드폰 활용 (상세)

### Claude Web Projects 세팅 (가장 강력한 모바일 활용)

핸드폰 브라우저에서 **컨설팅 보조 AI**를 그대로 사용 가능:

1. claude.ai 로그인
2. Projects → "New Project"
3. 프로젝트 인스트럭션에 다음 파일 내용 복사:
   - HR 컨설팅: `_core/prompts/claude-web/hr-consulting-project.md`
   - 사업개발: `_core/prompts/claude-web/business-development-project.md`
4. 대화 시작 → 프로젝트별 맥락·역할이 유지됨

### 핸드폰 → 데스크탑 워크플로우

```
📱 출장 중 미팅
  ↓
Notion에 회의 핵심 메모 입력 (또는 Claude 앱에 받아쓰기)
  ↓
🖥️ 집/회사 도착
  ↓
Claude Code: "오늘 미팅 메모를 회의록 양식으로 정리해줘"
  ↓
프로젝트 docs/ 에 자동 저장 + 후속 작업 자동 제안
```

### 모바일 인박스 패턴 (추천)

`projects/INBOX/` 폴더를 만들어 핸드폰에서 던진 메모·아이디어를 한 곳에 모음:
- OneDrive 모바일 앱에서 `vrin_AI_hub/projects/INBOX/` 접근
- 음성 메모·텍스트·사진 업로드
- 데스크탑에서 정기적으로 분류·처리 (workspace-manager 활용)

### 함께 쓰면 좋은 앱

| 앱 | 용도 |
|----|------|
| **Claude** | 빠른 질문, 브레인스토밍 |
| **Claude Web (브라우저)** | Projects 기능으로 컨설팅 보조 |
| **Notion** | 메모, 할일, 아이디어 |
| **OneDrive** | 산출물 PDF·PPT 열람·공유 |
| **GitHub Mobile** | 커밋·이력 확인 |

---

## 7. 문제 해결

### OneDrive

| 증상 | 원인 | 해결 |
|------|------|------|
| Claude Code가 파일을 못 읽음 | 주문형 파일 (☁️) | 폴더 우클릭 → "항상 이 장치에 유지" |
| "파일명 (Desktop).ext" 생성 | 양쪽 동시 수정 | 원본 남기고 충돌본 삭제 |
| 동기화 안 됨 | OneDrive 일시중지 | 시스템 트레이 OneDrive 아이콘 확인 |
| 파일이 "동기화 보류 중" | 다른 앱에서 열림 | 해당 앱 닫기 |

### Git

| 증상 | 원인 | 해결 |
|------|------|------|
| `git status` 에러 | junction 깨짐 | `setup-desktop.cmd` 재실행 |
| push 충돌 | 양쪽 각각 커밋 | `git pull --rebase` 후 `git push` |
| Git이 느림 | .git이 OneDrive 안 | junction 확인 `fsutil reparsepoint query .git` |

### Claude Code

| 증상 | 원인 | 해결 |
|------|------|------|
| 스킬이 안 보임 | sync-tools.cmd 미실행 | `sync-tools.cmd` 실행 |
| 에이전트 못 찾음 | 프로젝트에 미배포 | `sync-tools.cmd` 실행 |
| OMC 작동 안 함 | 플러그인 미설치 | `/oh-my-claudecode:omc-setup` |
| "인증 필요" | 새 PC 첫 실행 | `claude` 실행 → 브라우저 로그인 |
| **노트북에는 있는 스킬이 데스크탑에 없음** | Tier 1 백업 미동기화 | `backup-user-settings.cmd` (소스 PC) + `setup-desktop.cmd` (대상 PC) |

### Junction 확인
```cmd
cd OneDrive\vrin_AI_hub
fsutil reparsepoint query .git
fsutil reparsepoint query .omc
fsutil reparsepoint query .claude
```
정상이면 "태그 값: Mount Point" 출력.

---

## 8. 초기 설정 체크리스트

### 노트북 (1회 — 이미 완료)
- [x] migrate-to-onedrive.cmd 실행
- [x] OneDrive "항상 이 장치에 유지"
- [x] backup-user-settings.cmd 실행 → `.desktop-setup/` 백업 생성

### 데스크탑 (이번에 진행)
- [ ] OneDrive 로그인 + workspace 동기화 완료
- [ ] workspace 폴더 → "항상 이 장치에 유지"
- [ ] Git, Node.js, Python 설치 (이미 완료)
- [ ] **setup-desktop.cmd 실행** (Git junction·Tier 1 스킬·플러그인·settings.json 일괄 복원)
- [ ] Claude Code 설치: `npm install -g @anthropic-ai/claude-code`
- [ ] Claude Code 인증: `cd OneDrive\vrin_AI_hub && claude`
- [ ] OMC 설치: `/oh-my-claudecode:omc-setup`
- [ ] **디바이스 패리티 점검**: [`DEVICE_PARITY_CHECKLIST.md`](DEVICE_PARITY_CHECKLIST.md)

### 핸드폰
- [ ] Claude 앱 설치 + Anthropic 로그인
- [ ] Claude Web (브라우저) Projects 5개 세팅
- [ ] Notion 앱 + OneDrive 앱 + GitHub Mobile 설치·로그인

---

## 9. 정기 점검 (자기진화 연동)

| 주기 | 작업 | 도구 |
|------|------|------|
| 매주 월요일 | 양 PC 패리티 점검 | DEVICE_PARITY_CHECKLIST 빠른 체크 |
| 매주 | Git push (백업) | `git add -A && git commit && git push` |
| 매월 말일 | 가이드 vs 실제 정합성 | workspace-manager |
| 매분기 | Tier 1 스킬·플러그인 정리 | backup-user-settings.cmd 갱신 |
| 연 1회 | archive/ 외부 백업 | 외장 디스크 등 |

자기진화 메커니즘 전체: [`_core/SYSTEM_EVOLUTION_LOOP.md`](_core/SYSTEM_EVOLUTION_LOOP.md)

---

## 10. 파일 목록

| 파일 | 용도 | 실행 시점 |
|------|------|----------|
| `migrate-to-onedrive.cmd` | 노트북 → OneDrive 이전 | 1회 (이미 완료) |
| `setup-desktop.cmd` | 데스크탑 초기 셋업 (자동 일괄 복원) | 1회 (이번 진행) |
| `backup-user-settings.cmd` | Tier 1 스킬·플러그인 백업 갱신 | 변경 시마다 |
| `sync-tools.cmd` | _core → 프로젝트 배포 | _core/ 수정 시 |
| `new-project.cmd` / `.sh` | 새 프로젝트 생성 | 신규 프로젝트 시 |
| `MULTI_DEVICE_GUIDE.md` | 이 문서 | 참고 |
| `DEVICE_PARITY_CHECKLIST.md` | 양 PC 동등성 점검표 | 주 1회 + PC 전환 시 |

---

## 11. 참조

- 전체 운영: [`WORKSPACE_GUIDE.md`](WORKSPACE_GUIDE.md)
- 리소스 카탈로그: [`_core/REGISTRY.md`](_core/REGISTRY.md)
- AI 도구 맵: [`_core/AI_TOOLS_MAP.md`](_core/AI_TOOLS_MAP.md)
- 자기진화 루프: [`_core/SYSTEM_EVOLUTION_LOOP.md`](_core/SYSTEM_EVOLUTION_LOOP.md)
- 디바이스 패리티: [`DEVICE_PARITY_CHECKLIST.md`](DEVICE_PARITY_CHECKLIST.md)
