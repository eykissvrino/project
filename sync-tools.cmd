@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: ============================================================
:: sync-tools.cmd — AI 리소스 동기화 스크립트
:: workspace/_shared/ → 모든 활성 프로젝트에 교차 배포
::
:: 핵심 원칙: 모든 에이전트/워크플로우가 모든 도구에서 사용 가능
::   agents/   → .claude/agents/ (Claude Code/OpenCode)
::   agents/   → .agent/workflows/ (Antigravity) ← 교차 배포
::   workflows/→ .agent/workflows/ (Antigravity)
::   workflows/→ .claude/agents/ (Claude Code/OpenCode) ← 교차 배포
:: ============================================================

echo.
echo ========================================
echo   AI 리소스 동기화 도구 (크로스도구)
echo   workspace/_shared/ → projects/
echo   모든 에이전트가 모든 도구에서 사용 가능
echo ========================================
echo.

set "WORKSPACE=%~dp0"
set "SHARED=%WORKSPACE%_shared"
set "PROJECTS=%WORKSPACE%projects"

:: 공유 리소스 존재 확인
if not exist "%SHARED%" (
    echo [오류] _shared/ 폴더를 찾을 수 없습니다.
    exit /b 1
)

:: 활성 프로젝트 목록
echo [1/5] 활성 프로젝트 탐색 중...
set "PROJECT_COUNT=0"
for /d %%P in ("%PROJECTS%\*") do (
    set /a PROJECT_COUNT+=1
    echo   발견: %%~nxP
)

if %PROJECT_COUNT%==0 (
    echo   활성 프로젝트가 없습니다.
    echo.
    echo 완료.
    exit /b 0
)

echo   총 %PROJECT_COUNT%개 프로젝트 발견
echo.

:: 스킬 배포 (양쪽 모두)
echo [2/5] 스킬 배포 중...
for /d %%P in ("%PROJECTS%\*") do (
    set "TARGET=%%P"

    :: Claude Code / OpenCode 스킬 배포
    if not exist "!TARGET!\.claude\skills" mkdir "!TARGET!\.claude\skills"
    xcopy "%SHARED%\skills\*" "!TARGET!\.claude\skills\" /E /I /Y /Q >nul 2>&1

    :: Antigravity 스킬 배포
    if not exist "!TARGET!\.agent\skills" mkdir "!TARGET!\.agent\skills"
    xcopy "%SHARED%\skills\*" "!TARGET!\.agent\skills\" /E /I /Y /Q >nul 2>&1

    echo   %%~nxP: 스킬 배포 완료 (.claude + .agent)
)
echo.

:: 에이전트 교차 배포 (Claude Code + Antigravity 양쪽)
echo [3/5] 에이전트 교차 배포 중...
for /d %%P in ("%PROJECTS%\*") do (
    set "TARGET=%%P"

    :: Claude Code / OpenCode 에이전트 배포
    if not exist "!TARGET!\.claude\agents" mkdir "!TARGET!\.claude\agents"
    xcopy "%SHARED%\agents\*" "!TARGET!\.claude\agents\" /E /I /Y /Q >nul 2>&1

    :: ★ Antigravity에도 에이전트 배포 (교차 배포)
    if not exist "!TARGET!\.agent\workflows" mkdir "!TARGET!\.agent\workflows"
    xcopy "%SHARED%\agents\*" "!TARGET!\.agent\workflows\" /E /I /Y /Q >nul 2>&1

    echo   %%~nxP: 에이전트 교차 배포 완료 (.claude/agents + .agent/workflows)
)
echo.

:: 워크플로우 교차 배포 (Antigravity + Claude Code 양쪽)
echo [4/5] 워크플로우 교차 배포 중...
for /d %%P in ("%PROJECTS%\*") do (
    set "TARGET=%%P"

    :: Antigravity 워크플로우 배포
    xcopy "%SHARED%\workflows\*" "!TARGET!\.agent\workflows\" /E /I /Y /Q >nul 2>&1

    :: ★ Claude Code / OpenCode에도 워크플로우 배포 (교차 배포)
    xcopy "%SHARED%\workflows\*" "!TARGET!\.claude\agents\" /E /I /Y /Q >nul 2>&1

    echo   %%~nxP: 워크플로우 교차 배포 완료 (.agent/workflows + .claude/agents)
)
echo.

:: 커맨드 배포
echo [5/5] 커맨드 배포 중...
for /d %%P in ("%PROJECTS%\*") do (
    set "TARGET=%%P"

    if not exist "!TARGET!\.claude\commands" mkdir "!TARGET!\.claude\commands"
    xcopy "%SHARED%\commands\*" "!TARGET!\.claude\commands\" /E /I /Y /Q >nul 2>&1

    echo   %%~nxP: 커맨드 배포 완료
)

echo.
echo ========================================
echo   동기화 완료! (크로스도구 교차 배포)
echo   %PROJECT_COUNT%개 프로젝트에 배포됨
echo ========================================
echo.
echo 배포 내용 (모든 도구에서 사용 가능):
echo   - 스킬 (23개):     _shared/skills/     → .claude/skills/ + .agent/skills/
echo   - 에이전트 (12개):  _shared/agents/     → .claude/agents/ + .agent/workflows/
echo   - 워크플로우 (7개): _shared/workflows/  → .agent/workflows/ + .claude/agents/
echo   - 커맨드 (3개):     _shared/commands/   → .claude/commands/
echo.
echo 결과: 프로젝트 내 .claude/agents/에 19개, .agent/workflows/에 19개 배포
echo.

endlocal
