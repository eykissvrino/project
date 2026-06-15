# -*- coding: utf-8 -*-
"""VRIN 에이전트 활성화 — 단일 원본(_core/agents/v2)을 3-벤더로 배포.
- Claude:      .claude/agents/        (Claude Code가 서브에이전트로 로드)
- Antigravity: .agent/agents/
- Codex:       AGENTS.md (= CLAUDE.md 미러, 조직 컨텍스트) + .codex/agents/
실행: python scripts/sync-agents.py
"""
import os, io, sys, shutil, glob

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HUB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(HUB, "_core", "agents", "v2")
DESTS = [os.path.join(HUB, ".claude", "agents"),
         os.path.join(HUB, ".agent", "agents"),
         os.path.join(HUB, ".codex", "agents")]

src_files = sorted(glob.glob(os.path.join(SRC, "*.md")))
n = 0
for dest in DESTS:
    os.makedirs(dest, exist_ok=True)
    for f in src_files:
        shutil.copy2(f, os.path.join(dest, os.path.basename(f)))
    n += 1
    print(f"  → {os.path.relpath(dest, HUB)} : {len(src_files)}개 배포")

# 프로젝트 배포 — 각 projects/*/ 에 v2 에이전트 + 스킬 + 커맨드 배치
#   (추가/갱신만 — 프로젝트 커스텀 에이전트/파일은 삭제하지 않고 보존)
SKILLS = os.path.join(HUB, "_core", "skills")
CMDS = os.path.join(HUB, "_core", "commands")
PROJ = os.path.join(HUB, "projects")

def deploy_dir(src_root, dst_root):
    """src_root 내용을 dst_root 로 복사(덮어쓰기, 기존 추가분 보존)."""
    if not os.path.isdir(src_root):
        return
    os.makedirs(dst_root, exist_ok=True)
    for item in os.listdir(src_root):
        s = os.path.join(src_root, item)
        d = os.path.join(dst_root, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)

def deploy_agents(dst):
    os.makedirs(dst, exist_ok=True)
    for f in src_files:
        shutil.copy2(f, os.path.join(dst, os.path.basename(f)))

proj_count = 0
if os.path.isdir(PROJ):
    for proj in sorted(os.listdir(PROJ)):
        ppath = os.path.join(PROJ, proj)
        if not os.path.isdir(ppath):
            continue
        has_claude = os.path.isdir(os.path.join(ppath, ".claude"))
        has_agent = os.path.isdir(os.path.join(ppath, ".agent"))
        if not (has_claude or has_agent):
            continue
        if has_claude:
            deploy_agents(os.path.join(ppath, ".claude", "agents"))
            deploy_dir(SKILLS, os.path.join(ppath, ".claude", "skills"))
            deploy_dir(CMDS, os.path.join(ppath, ".claude", "commands"))
        if has_agent:
            deploy_agents(os.path.join(ppath, ".agent", "agents"))
            deploy_dir(SKILLS, os.path.join(ppath, ".agent", "skills"))
        proj_count += 1
    print(f"  → projects/*/ : {proj_count}개 프로젝트에 v2 에이전트+스킬+커맨드 배치 (커스텀 보존)")

# Codex용 AGENTS.md = CLAUDE.md 미러 (동일 조직 컨텍스트)
claude_md = os.path.join(HUB, "CLAUDE.md")
agents_md = os.path.join(HUB, "AGENTS.md")
if os.path.exists(claude_md):
    body = io.open(claude_md, encoding="utf-8").read()
    note = "<!-- 자동 생성: CLAUDE.md 미러 (Codex·Antigravity용). 원본은 CLAUDE.md를 수정하고 sync-agents 재실행 -->\n\n"
    io.open(agents_md, "w", encoding="utf-8").write(note + body)
    print("  → AGENTS.md (Codex/Antigravity 조직 컨텍스트) 생성")

print("=" * 50)
print(f"활성화 완료: {len(src_files)}개 에이전트 × {n}개 벤더 폴더 + AGENTS.md")
print("이제 vrin_AI_hub에서 Claude·Codex·Antigravity가 동일 조직을 사용합니다.")
