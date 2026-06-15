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
