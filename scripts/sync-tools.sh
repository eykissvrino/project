#!/bin/bash
# ============================================================
# sync-tools.sh — VRIN 리소스 배포 (래퍼)
# 정식 배포 로직은 scripts/sync-agents.py 에 통합됨:
#   _core/agents/v2 + _core/skills + _core/commands
#   → 허브 벤더 폴더(.claude/.agent/.codex) + 전 프로젝트 (커스텀 보존)
# (구 v1 교차배포 로직은 archive/_core-v1-20260615 로 폐기)
# ============================================================
DIR="$(cd "$(dirname "$0")" && pwd)"
python "$DIR/sync-agents.py" 2>/dev/null || python3 "$DIR/sync-agents.py"
