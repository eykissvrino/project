@echo off
chcp 65001 >nul
title VRIN 에이전트 관제탑
cd /d "%~dp0"
echo.
echo   VRIN 에이전트 관제탑을 시작합니다...
echo   잠시 후 브라우저가 자동으로 열립니다.
echo   (창을 닫으면 대시보드가 종료됩니다)
echo.
start "" /min cmd /c "timeout /t 2 >nul & start "" http://127.0.0.1:9777"
node server\server.js
echo.
echo   대시보드가 종료되었습니다. 아무 키나 누르세요.
pause >nul
