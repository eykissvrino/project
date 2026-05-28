# 디바이스 패리티 체크리스트

> 노트북과 데스크탑이 **풀-기능 동등 환경**임을 보장하기 위한 점검표.
>
> **목적**: "어느 PC에서든 같은 품질·속도로 작업할 수 있는가?"를 정량 확인
> **빈도**: 주 1회 정기 + PC 전환 직후 + 가이드 문서 변경 후
> **최종 업데이트**: 2026-05-28

---

## 사용법

각 PC에서 아래 점검을 실행하여 결과를 비교. 차이가 발견되면 **부족한 쪽에 복원**.

```
노트북 A 결과   ←→   데스크탑 B 결과
     ▼
   비교 → 차이 있으면 backup-user-settings.cmd로 동기화
```

---

## 1. Tier 1 스킬 (목표: 69개 동일)

### 점검 명령 (양 PC에서 각각 실행)
```cmd
dir /b "%USERPROFILE%\.claude\skills" | find /c /v ""
```
또는 (PowerShell)
```powershell
(Get-ChildItem $env:USERPROFILE\.claude\skills -Directory).Count
```

### 기대 결과
- 노트북: 69
- 데스크탑: 69
- **차이 시 조치**: 스킬 많은 쪽에서 `backup-user-settings.cmd` 실행 → 적은 쪽에서 `setup-desktop.cmd` 또는 수동 xcopy

---

## 2. 플러그인 (목표: mckinsey-pptx + oh-my-claudecode 양쪽 설치)

### 점검 명령
```cmd
dir /b "%USERPROFILE%\.claude\plugins" 2>nul
```

### 기대 결과 (양 PC 동일)
```
blocklist.json
cache (있을 수 있음)
data
install-counts-cache.json
installed_plugins.json
known_marketplaces.json
marketplaces
mckinsey-pptx     ← 필수
oh-my-claudecode  ← 필수
```

### 차이 시 조치
- 노트북에 있고 데스크탑에 없으면: `backup-user-settings.cmd` → `setup-desktop.cmd`
- 새 플러그인 설치 시: Claude Code 내에서 동일 설치 명령 양쪽 실행 + 백업 갱신

---

## 3. settings.json (목표: 내용 동일)

### 점검 명령
```cmd
fc "%USERPROFILE%\.claude\settings.json" "%USERPROFILE%\OneDrive\vrin_AI_hub\.desktop-setup\user-settings-backup\settings.json"
```
또는 (PowerShell)
```powershell
diff (Get-Content $env:USERPROFILE\.claude\settings.json) (Get-Content $env:USERPROFILE\OneDrive\vrin_AI_hub\.desktop-setup\user-settings-backup\settings.json)
```

### 기대 결과
"FC: no differences encountered" 또는 빈 출력

### 차이 시 조치
- 양 PC에 같은 내용이 있어야 함
- 노트북에서 수정했다면: `backup-user-settings.cmd` → 데스크탑 `setup-desktop.cmd`

---

## 4. MCP 서버 (목표: hwp-mcp, notion, figma 등 동일)

### 점검 방법
settings.json의 `mcpServers` 섹션 확인. 양 PC가 같은 MCP 서버 등록 필요.

### 핵심 MCP 목록
| MCP | 양 PC 필수? | 비고 |
|-----|------------|------|
| hwp-mcp | ✅ | 한글 문서 처리 |
| notion | ✅ | Notion 연동 |
| figma | ✅ (있다면) | 디자인 |
| (기타) | ✅ | 노트북에 있는 것은 데스크탑에도 |

### 차이 시 조치
1. 노트북 settings.json 확인
2. 데스크탑에 같은 `mcpServers` 블록 추가
3. 또는 backup-user-settings.cmd → setup-desktop.cmd

---

## 5. OMC (oh-my-claudecode) 버전

### 점검 명령
```cmd
omc --version
```

### 기대 결과
양 PC 동일 버전 (예: v4.14.4)

### 차이 시 조치
```cmd
omc update   :: 양 PC에서 각각 실행
```

---

## 6. Claude Code 인증 (목표: 양 PC 모두 Anthropic 계정 로그인 상태)

### 점검 명령
```cmd
claude --version
```
세션 시작 시 인증 요구 없이 진입 가능해야 함.

### 차이 시 조치
- 인증 미완료 PC에서: `claude` 실행 → 브라우저 로그인 → `eykis.lsj@gmail.com` 사용

---

## 7. OneDrive 동기화 상태

### 점검
- 시스템 트레이 OneDrive 아이콘 → 동기화 완료 표시 (✓)
- `vrin_AI_hub` 폴더 → "항상 이 장치에 유지" 체크됨 (✅ 표시)

### 차이 시 조치
- 폴더 우클릭 → "항상 이 장치에 유지"
- OneDrive 일시 중지 해제

---

## 8. Junction 무결성

### 점검 명령 (양 PC에서)
```cmd
cd OneDrive\vrin_AI_hub
fsutil reparsepoint query .git
fsutil reparsepoint query .omc
fsutil reparsepoint query .claude
```

### 기대 결과
3개 모두 "태그 값: Mount Point" 출력

### 차이 시 조치
- junction 재생성: `rmdir .git && mklink /J .git "%USERPROFILE%\.git-repos\vrin_AI_hub"`

---

## 9. 활성 프로젝트 수

### 점검 명령
```cmd
dir /b /a:d projects 2>nul | find /c /v ""
```

### 기대 결과
양 PC 동일 (현재 15개). OneDrive가 자동 동기화하므로 차이 시 OneDrive 미완료.

---

## 10. _core/ 리소스 동기화

### 점검 명령
```cmd
dir /b _core\skills | find /c /v ""   :: 기대 25
dir /b _core\agents | find /c /v ""   :: 기대 21
dir /b _core\workflows | find /c /v "" :: 기대 9
```

### 차이 시 조치
- OneDrive 동기화 대기
- 다 받았는지 폴더 우클릭 → "항상 이 장치에 유지"

---

## 빠른 점검 스크립트 (참고)

> 향후 자동화 가능: `check-parity.cmd` 같은 스크립트로 위 10개 항목 일괄 점검

```cmd
:: 향후 만들 점검 스크립트 골격
@echo off
echo === Tier 1 스킬 ===
dir /b "%USERPROFILE%\.claude\skills" | find /c /v ""
echo === _core/skills ===
dir /b _core\skills | find /c /v ""
echo === _core/agents ===
dir /b _core\agents | find /c /v ""
echo === Junction ===
fsutil reparsepoint query .git >nul 2>&1 && echo .git OK || echo .git FAIL
fsutil reparsepoint query .omc >nul 2>&1 && echo .omc OK || echo .omc FAIL
fsutil reparsepoint query .claude >nul 2>&1 && echo .claude OK || echo .claude FAIL
```

---

## 패리티 점검 결과 기록

> 매주 월요일 1회 기록 권장

| 날짜 | 노트북 점검 | 데스크탑 점검 | 차이 발견 | 조치 |
|------|------------|--------------|----------|------|
| 2026-05-28 | (셋업 전) | (셋업 진행) | — | setup-desktop.cmd 실행 |
| | | | | |
| | | | | |

---

## 11. 변경 시 즉시 실행할 작업

| 변경 종류 | 조치 (소스 PC) | 조치 (대상 PC) |
|----------|---------------|---------------|
| Tier 1 스킬 추가/수정 | `backup-user-settings.cmd` | `setup-desktop.cmd` 또는 수동 복원 |
| 플러그인 설치 | `backup-user-settings.cmd` | `setup-desktop.cmd` |
| settings.json 수정 | `backup-user-settings.cmd` | `setup-desktop.cmd` |
| MCP 서버 추가 | settings.json 수정 + backup | 양쪽 동기화 |
| OMC 버전업 | `omc update` | `omc update` |
| Tier 2 스킬·에이전트·워크플로우 | OneDrive가 자동 | (자동) |
| 가이드 문서 | OneDrive가 자동 + git push | (자동) |

---

## 12. 트러블슈팅

### "노트북엔 있는 스킬이 데스크탑에 없다"
1. 노트북에서: `cd OneDrive\vrin_AI_hub && backup-user-settings.cmd`
2. `git add .desktop-setup/ && git commit -m "user settings update" && git push`
3. 데스크탑에서: `git pull`
4. 데스크탑에서: `setup-desktop.cmd` (또는 `xcopy` 수동 복원)

### "MCP 서버 작동 안 함"
1. 양 PC의 `~/.claude/settings.json`의 `mcpServers` 비교
2. 동일하게 맞춤
3. Claude Code 재시작

### "OMC 명령이 한쪽에만 있음"
- `/oh-my-claudecode:omc-setup` 양 PC에서 각각 실행

---

## 13. 참조

- 멀티디바이스: [`MULTI_DEVICE_GUIDE.md`](MULTI_DEVICE_GUIDE.md)
- AI 도구 맵: [`_core/AI_TOOLS_MAP.md`](_core/AI_TOOLS_MAP.md)
- 자기진화 루프: [`_core/SYSTEM_EVOLUTION_LOOP.md`](_core/SYSTEM_EVOLUTION_LOOP.md)
