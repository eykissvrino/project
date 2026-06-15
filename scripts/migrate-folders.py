# -*- coding: utf-8 -*-
"""VRIN 프로젝트 폴더 표준 마이그레이션 (비파괴 — 이동만, 삭제 없음)
- 단순형: 00~05 표준 적용 + data→01, docs→02, outputs→04, loose 산출물→04, loose .md→03
- 개발형(package.json 등): 00_관리만 + 코드 보존
- 자체 번호체계: 00_관리만 추가, 기존 번호폴더 보존 (수동 매핑 대기)
실행: python scripts/migrate-folders.py
"""
import os, re, io, sys, shutil

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HUB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJ = os.path.join(HUB, "projects")
STD = ["00_관리", "01_입력자료", "02_지식리서치", "03_작업실", "04_산출물", "05_보관"]
SKIP = {".git", ".claude", ".agent", ".next", "node_modules", ".omc", ".fonts", ".vscode", "dist", "build", "__pycache__", "site"}
KEEP = {"readme.md", "claude.md", "agents.md", ".gitignore", ".gitkeep"}
DELIV = {".pptx", ".ppt", ".docx", ".doc", ".pdf", ".xlsx", ".xls", ".hwp", ".hwpx", ".epub", ".zip"}
STUB = """---
project: {name}
client: ""
type: 컨설팅
phase: 1
status: green
lead: "@CoS"
squad: []
progress: 0
next: 현황 설정 필요
due: ""
updated: 2026-06-15
---
# 현황 메모
VRIN 표준 폴더 적용됨. 실제 현황(phase·status·squad·lead)으로 갱신 필요.
"""

def ensure(p):
    if not os.path.isdir(p):
        os.makedirs(p, exist_ok=True)

def is_self_numbered(name):
    return bool(re.match(r"^\d{1,2}_", name)) and name not in STD

log = []
for proj in sorted(os.listdir(PROJ)):
    pp = os.path.join(PROJ, proj)
    if not os.path.isdir(pp) or proj in ("_완료", "TEST"):
        continue
    items = os.listdir(pp)
    dev = ("package.json" in items) or ("node_modules" in items) or ("app" in items and "components" in items)
    self_num = any(is_self_numbered(x) and os.path.isdir(os.path.join(pp, x)) for x in items)

    ensure(os.path.join(pp, "00_관리"))
    hyun = os.path.join(pp, "00_관리", "_현황.md")
    ch = False
    if not os.path.exists(hyun):
        io.open(hyun, "w", encoding="utf-8").write(STUB.format(name=proj))
        ch = True

    if dev:
        log.append(("DEV", proj, "00_관리+_현황만 (코드 보존)", ch)); continue
    if self_num:
        log.append(("자체번호", proj, "00_관리+_현황 추가 · 기존 번호체계 보존 (수동매핑 대기)", ch)); continue

    for d in STD:
        ensure(os.path.join(pp, d))
    moved = []
    for old, new in (("data", "01_입력자료"), ("docs", "02_지식리서치"), ("outputs", "04_산출물")):
        op = os.path.join(pp, old)
        if os.path.isdir(op):
            for it in os.listdir(op):
                src, dst = os.path.join(op, it), os.path.join(pp, new, it)
                if not os.path.exists(dst):
                    shutil.move(src, dst)
            try:
                os.rmdir(op); moved.append(f"{old}/→{new}")
            except OSError:
                moved.append(f"{old}/→{new}(잔여)")
    for it in list(os.listdir(pp)):
        ip = os.path.join(pp, it)
        if not os.path.isfile(ip) or it.startswith(".") or it.lower() in KEEP:
            continue
        ext = os.path.splitext(it)[1].lower()
        if ext in DELIV:
            dst = os.path.join(pp, "04_산출물", it)
            if not os.path.exists(dst):
                shutil.move(ip, dst); moved.append(f"{it[:24]}→04")
        elif ext == ".md":
            dst = os.path.join(pp, "03_작업실", it)
            if not os.path.exists(dst):
                shutil.move(ip, dst); moved.append(f"{it[:24]}→03")
    log.append(("표준적용", proj, ", ".join(moved) or "폴더 생성", ch))

print("=" * 60)
for typ, proj, act, ch in log:
    print(f"[{typ}] {proj}")
    print(f"    {act}" + ("  (+_현황 생성)" if ch else ""))
print("=" * 60)
print(f"총 {len(log)}개 프로젝트 처리")
