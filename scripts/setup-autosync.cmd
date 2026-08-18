@echo off
chcp 65001 >nul
REM ============================================================
REM setup-autosync.cmd — 매일 자동 커밋·푸시 등록 (더블클릭 실행)
REM
REM   setup-autosync.cmd           매일 18:00 로 등록
REM   setup-autosync.cmd 21:30     시각 지정해서 등록
REM   setup-autosync.cmd /status   상태·최근 로그 확인
REM   setup-autosync.cmd /remove   자동 동기화 해제
REM ============================================================

if /i "%~1"=="/remove" goto :remove
if /i "%~1"=="/status" goto :status
if "%~1"=="" goto :install
goto :installat

:install
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup-autosync.ps1"
goto :end

:installat
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup-autosync.ps1" -Time "%~1"
goto :end

:status
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup-autosync.ps1" -Status
goto :end

:remove
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup-autosync.ps1" -Remove
goto :end

:end
echo.
pause
