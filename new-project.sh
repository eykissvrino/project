#!/bin/bash
# ============================================
# 새 프로젝트 생성 스크립트
# 사용법: ./new-project.sh "프로젝트명"
# 코드 형식: P년도-일련번호_프로젝트명
# 예시 결과: P2026-002_한화연_산업전환진단
# ============================================

WORKSPACE="$(cd "$(dirname "$0")" && pwd)"
TEMPLATE="$WORKSPACE/_shared/templates/project-template"

if [ -z "$1" ]; then
    echo "사용법: ./new-project.sh \"프로젝트명\""
    echo "예시:  ./new-project.sh \"한화연_산업전환진단\""
    echo ""
    echo "결과:  P2026-002_한화연_산업전환진단 (번호 자동 부여)"
    exit 1
fi

PROJECT_NAME="$1"
YEAR=$(date +%Y)

# 올해 프로젝트 중 가장 큰 번호 찾기
MAX_NUM=0
for d in "$WORKSPACE/projects/P${YEAR}-"*/; do
    if [ -d "$d" ]; then
        NUM=$(basename "$d" | grep -oP "P${YEAR}-\K\d+")
        if [ -n "$NUM" ] && [ "$NUM" -gt "$MAX_NUM" ] 2>/dev/null; then
            MAX_NUM=$NUM
        fi
    fi
done

NEXT_NUM=$((MAX_NUM + 1))
PADDED=$(printf "%03d" $NEXT_NUM)
PROJECT_CODE="P${YEAR}-${PADDED}"
FULL_NAME="${PROJECT_CODE}_${PROJECT_NAME}"
PROJECT_DIR="$WORKSPACE/projects/$FULL_NAME"

if [ -d "$PROJECT_DIR" ]; then
    echo "오류: '$FULL_NAME' 프로젝트가 이미 존재합니다."
    exit 1
fi

# 템플릿 복사
cp -r "$TEMPLATE" "$PROJECT_DIR"

# CLAUDE.md에 프로젝트명 적용
sed -i "s/\[프로젝트명\]/$FULL_NAME/g" "$PROJECT_DIR/CLAUDE.md"

# 공유 스킬 → .claude/skills/ 링크
for skill_dir in "$WORKSPACE/_shared/skills/"*/; do
    skill_name=$(basename "$skill_dir")
    ln -sf "$skill_dir" "$PROJECT_DIR/.claude/skills/$skill_name"
done

# 공유 에이전트 → 교차 배포 (.claude/agents/ + .agent/workflows/)
mkdir -p "$PROJECT_DIR/.claude/agents"
mkdir -p "$PROJECT_DIR/.agent/workflows"
for agent_file in "$WORKSPACE/_shared/agents/"*.md; do
    ln -sf "$agent_file" "$PROJECT_DIR/.claude/agents/$(basename "$agent_file")"
    ln -sf "$agent_file" "$PROJECT_DIR/.agent/workflows/$(basename "$agent_file")"
done

# 공유 커맨드 → .claude/commands/ 링크
for cmd_file in "$WORKSPACE/_shared/commands/"*.md; do
    ln -sf "$cmd_file" "$PROJECT_DIR/.claude/commands/$(basename "$cmd_file")"
done

# 공유 워크플로우 → 교차 배포 (.agent/workflows/ + .claude/agents/)
for wf_file in "$WORKSPACE/_shared/workflows/"*.md; do
    ln -sf "$wf_file" "$PROJECT_DIR/.agent/workflows/$(basename "$wf_file")"
    ln -sf "$wf_file" "$PROJECT_DIR/.claude/agents/$(basename "$wf_file")"
done

# 공유 스킬 → .agent/skills/ 링크
for skill_dir in "$WORKSPACE/_shared/skills/"*/; do
    skill_name=$(basename "$skill_dir")
    ln -sf "$skill_dir" "$PROJECT_DIR/.agent/skills/$skill_name"
done

echo "✓ 프로젝트 생성: $FULL_NAME"
echo ""
echo "  .claude/skills/     → 공유 스킬 링크됨"
echo "  .claude/agents/     → 에이전트+워크플로우 19개 (교차 배포)"
echo "  .agent/skills/      → 공유 스킬 링크됨"
echo "  .agent/workflows/   → 워크플로우+에이전트 19개 (교차 배포)"
echo "  docs/               ← 작업 메모"
echo "  data/               ← 원시 데이터"
echo "  outputs/            ← 최종 산출물"
echo ""
echo "다음: CLAUDE.md 편집 후 claude 또는 antigravity 실행"
