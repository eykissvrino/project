# -*- coding: utf-8 -*-
"""모든 비개발 프로젝트의 상위 폴더를 VRIN 표준(00~05)으로 재구성.
비표준 상위 폴더는 키워드 매핑으로 표준 폴더 '하위에 둥지(nest)'로 이동 → 원래 라벨/내용 보존.
비파괴(이동만). 개발형(코드)·.hidden·skip 폴더는 건드리지 않음.
실행: python scripts/remap-standard.py
"""
import os, re, io, sys, shutil

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HUB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJ = os.path.join(HUB, "projects")
STD = ["00_관리", "01_입력자료", "02_지식리서치", "03_작업실", "04_산출물", "05_보관"]
SKIP = {".git", ".claude", ".agent", ".next", "node_modules", ".omc", ".fonts", ".vscode",
        "dist", "build", "__pycache__"}
KEEP = {"readme.md", "claude.md", "agents.md", ".gitignore", ".gitkeep"}
DELIV = {".pptx", ".ppt", ".docx", ".doc", ".pdf", ".xlsx", ".xls", ".hwp", ".hwpx", ".epub", ".zip"}
KW = [
    ("04_산출물", ["산출", "최종", "결과물", "deliver", "아카이브", "archive"]),
    ("00_관리", ["회의", "과업", "프로젝트관리", "일정", "행정", "관리", "에이전트", "kickoff"]),
    ("02_지식리서치", ["참고", "지식", "템플릿", "시스템", "레퍼런스", "reference", "자산", "study", "학습", "자료"]),
    ("01_입력자료", ["원본", "입력", "raw", "받은", "업로드", "data"]),
    ("05_보관", ["보관", "폐기", "구버전", "backup", "temp", "tmp"]),
]

def target_for(name):
    for tgt, kws in KW:
        for kw in kws:
            if kw in name or kw in name.lower():
                return tgt
    return "03_작업실"

def ensure(p):
    if not os.path.isdir(p):
        os.makedirs(p, exist_ok=True)

def is_dev(items):
    return ("package.json" in items) or ("node_modules" in items) or ("app" in items and "components" in items)

log = []
for proj in sorted(os.listdir(PROJ)):
    pp = os.path.join(PROJ, proj)
    if not os.path.isdir(pp) or proj in ("_완료", "TEST") or proj.startswith("."):
        continue
    items = os.listdir(pp)
    if is_dev(items):
        log.append((proj, "DEV 건너뜀 (코드 보존)", [])); continue
    for d in STD:
        ensure(os.path.join(pp, d))
    actions = []
    for it in list(os.listdir(pp)):
        ip = os.path.join(pp, it)
        if it in STD or it in SKIP or it.startswith("."):
            continue
        if os.path.isdir(ip):
            tgt = target_for(it)
            dst = os.path.join(pp, tgt, it)
            if not os.path.exists(dst):
                shutil.move(ip, dst); actions.append(f"{it} → {tgt}/")
            else:
                actions.append(f"{it} → {tgt}/ (존재, 건너뜀)")
        elif os.path.isfile(ip):
            if it.lower() in KEEP:
                continue
            ext = os.path.splitext(it)[1].lower()
            tgt = "04_산출물" if ext in DELIV else ("05_보관" if ext in (".tmp", ".bak") else ("03_작업실" if ext == ".md" else None))
            if tgt:
                dst = os.path.join(pp, tgt, it)
                if not os.path.exists(dst):
                    shutil.move(ip, dst); actions.append(f"{it[:22]} → {tgt}/")
    log.append((proj, "재구성" if actions else "이미 표준", actions))

print("=" * 64)
for proj, st, acts in log:
    print(f"[{st}] {proj}")
    for a in acts:
        print(f"    · {a}")
print("=" * 64)
print(f"총 {len(log)}개 처리 — 모든 비개발 프로젝트 상위 = 00~05 표준 통일")
