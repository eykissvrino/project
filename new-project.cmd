@echo off
chcp 65001 >nul
REM ============================================
REM 새 프로젝트 생성 스크립트 (Windows용)
REM 사용법: new-project.cmd "프로젝트명"
REM 코드 형식: P년도-일련번호_프로젝트명
REM 예시 결과: P2026-002_한화연_산업전환진단
REM ============================================

set "WORKSPACE=%~dp0"
set "TEMPLATE=%WORKSPACE%_shared\templates\project-template"

if "%~1"=="" (
    echo 사용법: new-project.cmd "프로젝트명"
    echo 예시:  new-project.cmd "한화연_산업전환진단"
    echo.
    echo 결과:  P2026-002_한화연_산업전환진단 (번호 자동 부여)
    exit /b 1
)

set "PROJECT_NAME=%~1"

REM 현재 연도 가져오기
for /f "tokens=1 delims=/" %%a in ('date /t') do set "YEAR=%%a"
REM Windows 날짜 형식에 따라 조정
if "%YEAR:~0,2%"=="20" (set "YEAR=%YEAR:~0,4%") else (for /f "tokens=3 delims=/" %%a in ('date /t') do set "YEAR=%%a")

REM 올해 프로젝트 중 가장 큰 번호 찾기
set "MAX_NUM=0"
for /d %%d in ("%WORKSPACE%projects\P%YEAR%-*") do (
    for /f "tokens=2 delims=-_" %%n in ("%%~nxd") do (
        set /a "NUM=%%n" 2>nul
        if !NUM! gtr !MAX_NUM! set "MAX_NUM=!NUM!"
    )
)
setlocal enabledelayedexpansion
set /a "NEXT_NUM=!MAX_NUM!+1"
set "PADDED=00!NEXT_NUM!"
set "PADDED=!PADDED:~-3!"
set "PROJECT_CODE=P%YEAR%-!PADDED!"
set "FULL_NAME=!PROJECT_CODE!_%PROJECT_NAME%"
set "PROJECT_DIR=%WORKSPACE%projects\!FULL_NAME!"

if exist "!PROJECT_DIR!" (
    echo 오류: '!FULL_NAME!' 프로젝트가 이미 존재합니다.
    exit /b 1
)

REM 템플릿 복사
xcopy "%TEMPLATE%" "!PROJECT_DIR!" /E /I /Q >nul

REM 공유 스킬을 프로젝트에 복사
xcopy "%WORKSPACE%_shared\skills" "!PROJECT_DIR!\.claude\skills" /E /I /Q >nul 2>nul
xcopy "%WORKSPACE%_shared\skills" "!PROJECT_DIR!\.agent\skills" /E /I /Q >nul 2>nul

REM 공유 에이전트 복사
if not exist "!PROJECT_DIR!\.claude\agents" mkdir "!PROJECT_DIR!\.claude\agents"
copy "%WORKSPACE%_shared\agents\*.md" "!PROJECT_DIR!\.claude\agents\" /Y >nul 2>nul

REM 공유 커맨드 복사
copy "%WORKSPACE%_shared\commands\*.md" "!PROJECT_DIR!\.claude\commands\" /Y >nul 2>nul

REM 공유 워크플로우 복사
if not exist "!PROJECT_DIR!\.agent\workflows" mkdir "!PROJECT_DIR!\.agent\workflows"
copy "%WORKSPACE%_shared\workflows\*.md" "!PROJECT_DIR!\.agent\workflows\" /Y >nul 2>nul

echo.
echo ■ 프로젝트 생성: !FULL_NAME!
echo.
echo   .claude\skills\     -- 공유 스킬 포함
echo   .claude\agents\     -- 공유 에이전트 포함
echo   .agent\skills\      -- 공유 스킬 포함
echo   .agent\workflows\   -- 공유 워크플로우 포함
echo   docs\               -- 작업 메모
echo   data\               -- 원시 데이터
echo   outputs\            -- 최종 산출물
echo.
echo 다음: CLAUDE.md 편집 후 claude 또는 antigravity 실행
endlocal
