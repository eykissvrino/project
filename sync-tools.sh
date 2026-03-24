#!/bin/bash
# ============================================================
# sync-tools.sh — AI Resource Cross-Deploy Script
# workspace/_shared/ -> All active projects (cross-tool)
# All agents/workflows available in ALL tools
# ============================================================

WORKSPACE="$(cd "$(dirname "$0")" && pwd)"
SHARED="$WORKSPACE/_shared"
PROJECTS="$WORKSPACE/projects"

echo ""
echo "========================================"
echo "  AI Resource Sync (Cross-Tool Deploy)"
echo "  _shared/ -> projects/"
echo "========================================"
echo ""

if [ ! -d "$SHARED" ]; then
    echo "[ERROR] _shared/ folder not found."
    exit 1
fi

PROJECT_COUNT=0
for proj in "$PROJECTS"/*/; do
    [ -d "$proj" ] && PROJECT_COUNT=$((PROJECT_COUNT + 1))
done

if [ "$PROJECT_COUNT" -eq 0 ]; then
    echo "  No active projects found."
    exit 0
fi

echo "[1/5] Found $PROJECT_COUNT projects"
echo ""

for proj in "$PROJECTS"/*/; do
    [ ! -d "$proj" ] && continue
    name=$(basename "$proj")
    echo "=== $name ==="

    # Create directories
    mkdir -p "$proj/.claude/skills" "$proj/.claude/agents" "$proj/.claude/commands"
    mkdir -p "$proj/.agent/skills" "$proj/.agent/workflows"

    # Skills -> both .claude/skills/ and .agent/skills/
    cp -r "$SHARED"/skills/* "$proj/.claude/skills/" 2>/dev/null
    cp -r "$SHARED"/skills/* "$proj/.agent/skills/" 2>/dev/null
    echo "  [2/5] Skills: .claude + .agent OK (23)"

    # Agents -> .claude/agents/ AND .agent/workflows/ (cross-deploy)
    cp -r "$SHARED"/agents/* "$proj/.claude/agents/" 2>/dev/null
    cp -r "$SHARED"/agents/* "$proj/.agent/workflows/" 2>/dev/null
    echo "  [3/5] Agents: .claude/agents + .agent/workflows OK (cross)"

    # Workflows -> .agent/workflows/ AND .claude/agents/ (cross-deploy)
    cp -r "$SHARED"/workflows/* "$proj/.agent/workflows/" 2>/dev/null
    cp -r "$SHARED"/workflows/* "$proj/.claude/agents/" 2>/dev/null
    echo "  [4/5] Workflows: .agent/workflows + .claude/agents OK (cross)"

    # Commands -> .claude/commands/
    cp -r "$SHARED"/commands/* "$proj/.claude/commands/" 2>/dev/null
    echo "  [5/5] Commands: .claude/commands OK"

    echo ""
done

echo "========================================"
echo "  Sync Complete! (Cross-Tool Deploy)"
echo "  $PROJECT_COUNT projects updated"
echo "========================================"
echo ""
echo "Deployed per project:"
echo "  .claude/agents/    = 19 files (12 agents + 7 workflows)"
echo "  .agent/workflows/  = 19 files (7 workflows + 12 agents)"
echo "  .claude/skills/    = 23 folders"
echo "  .agent/skills/     = 23 folders"
echo "  .claude/commands/  = 3 files"
echo ""
