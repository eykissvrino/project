@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
REM ============================================================
REM git-sync.cmd — OneDrive vrin_AI_hub → GitHub 원클릭 동기화
REM
REM 사용법:  scripts\git-sync.cmd  ["커밋 메시지"]
REM   메시지를 안 주면 "chore: 작업 동기화 (YYYY-MM-DD)" 로 자동 생성
REM
REM 하는 일: 진단 → pull --rebase → add → commit → push (재시도 4회)
REM ============================================================

set "WORKSPACE=%USERPROFILE%\OneDrive\vrin_AI_hub"
set "BRANCH=main"

echo ══════════════════════════════════════════════════
echo   VRIN AI Hub — GitHub 동기화
echo ══════════════════════════════════════════════════
echo.

REM ── [1] 워크스페이스 확인 ──────────────────────────
if not exist "%WORKSPACE%" (
    echo   [오류] 워크스페이스를 찾을 수 없습니다:
    echo          %WORKSPACE%
    echo   OneDrive 로그인 / 동기화 상태를 확인해주세요.
    goto :error
)
cd /d "%WORKSPACE%"
echo   워크스페이스: %WORKSPACE%

REM ── [2] Git 연결 진단 ─────────────────────────────
echo.
echo [1/5] Git 연결 확인...
git rev-parse --git-dir >nul 2>&1
if errorlevel 1 (
    echo   [오류] 이 폴더는 Git에 연결되어 있지 않습니다.
    echo          .git junction 이 없거나 깨졌습니다.
    echo.
    echo   해결: scripts\setup-desktop.cmd 를 실행하세요.
    echo         ^(GitHub 이력을 %%USERPROFILE%%\.git-repos 에 복원하고
    echo          .git junction 을 다시 만들어 줍니다^)
    goto :error
)
for /f "delims=" %%B in ('git rev-parse --abbrev-ref HEAD') do set "CURBRANCH=%%B"
echo   OK — 현재 브랜치: !CURBRANCH!

if not "!CURBRANCH!"=="%BRANCH%" (
    echo.
    echo   [주의] 현재 브랜치가 %BRANCH% 가 아닙니다.
    echo          %BRANCH% 로 전환하려면 Y, 현재 브랜치에 그대로 올리려면 N.
    set /p "SWITCH=   %BRANCH% 로 전환할까요? (Y/N): "
    if /i "!SWITCH!"=="Y" (
        git checkout %BRANCH% || goto :error
        set "CURBRANCH=%BRANCH%"
    ) else (
        set "BRANCH=!CURBRANCH!"
    )
)

REM ── [3] 원격 최신 반영 ────────────────────────────
echo.
echo [2/5] GitHub 최신 내용 가져오는 중...
git pull --rebase origin %BRANCH%
if errorlevel 1 (
    echo.
    echo   [주의] pull --rebase 중 충돌이 발생했습니다.
    echo          충돌 파일을 정리한 뒤  git rebase --continue  를 실행하거나,
    echo          되돌리려면  git rebase --abort  를 실행하세요.
    goto :error
)

REM ── [4] 변경사항 확인 + 커밋 ──────────────────────
echo.
echo [3/5] 변경사항 확인...
git add -A
git diff --cached --quiet
if not errorlevel 1 (
    echo   변경된 파일이 없습니다 — 커밋할 것이 없습니다.
    goto :pushcheck
)

for /f %%C in ('git diff --cached --name-only ^| find /c /v ""') do set "NCHANGED=%%C"
echo   변경 파일 !NCHANGED!개:
git diff --cached --stat | more +0
echo.

set "MSG=%~1"
if "%MSG%"=="" (
    for /f "tokens=1-3 delims=-/. " %%a in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd"') do set "TODAY=%%a-%%b-%%c"
    set "MSG=chore: 작업 동기화 (!TODAY!)"
)

echo [4/5] 커밋 중: !MSG!
git commit -m "!MSG!"
if errorlevel 1 goto :error

:pushcheck
REM ── [5] 푸시 (네트워크 오류 시 재시도) ────────────
echo.
echo [5/5] GitHub 에 푸시 중...
set "TRY=0"
:retry
set /a TRY+=1
git push -u origin %BRANCH%
if not errorlevel 1 goto :done

if !TRY! GEQ 5 (
    echo.
    echo   [오류] 푸시 실패 ^(4회 재시도 후^).
    echo          네트워크 또는 GitHub 인증을 확인해주세요.
    goto :error
)
set /a WAIT=2
if !TRY!==2 set /a WAIT=4
if !TRY!==3 set /a WAIT=8
if !TRY!==4 set /a WAIT=16
echo   푸시 실패 — !WAIT!초 후 재시도 ^(!TRY!/4^)...
powershell -NoProfile -Command "Start-Sleep -Seconds !WAIT!" >nul
goto :retry

:done
echo.
echo ══════════════════════════════════════════════════
echo   완료 — GitHub 반영됨
echo   https://github.com/eykissvrino/project
echo ══════════════════════════════════════════════════
echo.
pause
exit /b 0

:error
echo.
echo ══════════════════════════════════════════════════
echo   중단됨 — 위 메시지를 확인해주세요.
echo ══════════════════════════════════════════════════
echo.
pause
exit /b 1
