@echo off
chcp 65001 >nul
REM ============================================================
REM sync-tools.cmd — VRIN 리소스 배포 (래퍼)
REM 정식 배포 로직은 scripts\sync-agents.py 에 통합됨:
REM   _core/agents/v2 + _core/skills + _core/commands
REM   → 허브 벤더 폴더(.claude/.agent/.codex) + 전 프로젝트 (커스텀 보존)
REM (구 v1 교차배포 로직은 archive\_core-v1-20260615 로 폐기)
REM ============================================================
python "%~dp0sync-agents.py"
