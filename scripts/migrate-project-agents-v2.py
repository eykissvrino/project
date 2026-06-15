# -*- coding: utf-8 -*-
"""
프로젝트 에이전트 v2 마이그레이션
- 모든 projects/*/ 의 .claude/agents, .agent/workflows 에서 v1 잔재 제거
- _core/agents/v2/ 의 43개 v2 에이전트를 각 프로젝트 .claude/agents + .agent/agents 에 배치
- 진짜 프로젝트 커스텀(아래 STALE 목록에 없는 것)은 보존
주의: 이 경로들은 .gitignore 대상(로컬 동기화 복사본). git push 불필요.
"""
import os, shutil, io

HUB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V2_DIR = os.path.join(HUB, "_core", "agents", "v2")
PROJ_DIR = os.path.join(HUB, "projects")
ARCHIVE = os.path.join(HUB, "archive", "project-agents-v1-template-20260615")

GREEK = ["athena","apollo","midas","hera","hermes","themis","aphrodite",
         "daedalus","chronos","pygmalion","ralph-loop"]
BOTS = ["auth-route-debugger","auth-route-tester","auto-error-resolver",
        "code-architecture-reviewer","code-refactor-master","documentation-architect",
        "frontend-error-fixer","plan-reviewer","planner","refactor-planner",
        "web-research-specialist","workspace-manager"]
TEMPLATE = ["agent-01-legal","agent-02-hr","agent-03-job-carving","agent-04-bm",
            "agent-05-research","agent-06-branding","agent-07-cso"]
STALE = set(f + ".md" for f in GREEK + BOTS + TEMPLATE)

V2_FILES = [f for f in os.listdir(V2_DIR) if f.endswith(".md")]

def backup_once():
    """v1 범용 템플릿(agent-0X) 한 벌만 archive 백업 (그리스는 이미 archive에 있음)"""
    if os.path.isdir(ARCHIVE):
        return "백업 생략(이미 존재)"
    os.makedirs(ARCHIVE, exist_ok=True)
    # 첫 발견 프로젝트에서 template + workflows 한 벌 백업
    for proj in sorted(os.listdir(PROJ_DIR)):
        src = os.path.join(PROJ_DIR, proj, ".claude", "agents")
        if os.path.isdir(src):
            for t in TEMPLATE:
                fp = os.path.join(src, t + ".md")
                if os.path.exists(fp):
                    shutil.copy2(fp, os.path.join(ARCHIVE, t + ".md"))
            break
    return "백업 완료: " + ARCHIVE

def process():
    summary = []
    for proj in sorted(os.listdir(PROJ_DIR)):
        ppath = os.path.join(PROJ_DIR, proj)
        if not os.path.isdir(ppath):
            continue
        removed = kept = deployed = 0
        # 1) .claude/agents 정리 + v2 배치
        ca = os.path.join(ppath, ".claude", "agents")
        if os.path.isdir(ca):
            for f in os.listdir(ca):
                if f in STALE:
                    os.remove(os.path.join(ca, f)); removed += 1
                elif f.endswith(".md") and f not in V2_FILES and f != "README.md":
                    kept += 1
            for vf in V2_FILES:
                shutil.copy2(os.path.join(V2_DIR, vf), os.path.join(ca, vf)); deployed += 1
        # 2) .agent/workflows stale 제거
        aw = os.path.join(ppath, ".agent", "workflows")
        wf_removed = 0
        if os.path.isdir(aw):
            for f in os.listdir(aw):
                if f in STALE:
                    os.remove(os.path.join(aw, f)); wf_removed += 1
        # 3) .agent/agents v2 배치 (Antigravity)
        aa = os.path.join(ppath, ".agent", "agents")
        if os.path.isdir(os.path.join(ppath, ".agent")):
            os.makedirs(aa, exist_ok=True)
            for vf in V2_FILES:
                shutil.copy2(os.path.join(V2_DIR, vf), os.path.join(aa, vf))
        summary.append((proj, removed, kept, deployed, wf_removed))
    return summary

if __name__ == "__main__":
    print("[v2 마이그레이션] v2 에이전트 %d개" % len(V2_FILES))
    print(backup_once())
    print("-" * 70)
    print("%-46s rm  keep dep  wf-rm" % "project")
    for proj, r, k, d, w in process():
        print("%-46s %3d %4d %4d %5d" % (proj[:46], r, k, d, w))
