# -*- coding: utf-8 -*-
"""VRIN 신규 프로젝트 생성 — 표준 골격 자동 스캐폴딩.
사용: python scripts/new-project.py "2026-13_고객사_사업명" [컨설팅|연구|사업|개발]
- 템플릿(_core/templates/project-template)을 복사
- 유형이 '개발'이면 03_작업실 제거(코드는 루트), 나머지는 표준 00~05
- _현황.md / README / CLAUDE 에 프로젝트명·유형 치환
"""
import os, io, sys, shutil, datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HUB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(HUB, "_core", "templates", "project-template")

def main():
    if len(sys.argv) < 2:
        print('사용법: python scripts/new-project.py "2026-13_고객사_사업명" [컨설팅|연구|사업|개발]')
        return 1
    name = sys.argv[1].strip().strip('"')
    ptype = sys.argv[2].strip() if len(sys.argv) > 2 else "컨설팅"
    dest = os.path.join(HUB, "projects", name)
    if os.path.exists(dest):
        print(f"⚠️ 이미 존재: {name}")
        return 1
    shutil.copytree(TPL, dest)
    # .gitkeep 정리
    for root, _, files in os.walk(dest):
        for f in files:
            if f == ".gitkeep":
                try: os.remove(os.path.join(root, f))
                except OSError: pass
    # 개발형이면 03_작업실 제거 (코드는 루트)
    if ptype == "개발":
        shutil.rmtree(os.path.join(dest, "03_작업실"), ignore_errors=True)
    # 치환
    today = "2026-06-15"
    repl = {"[프로젝트명]": name, "2026-NN_고객사_사업명": name, "type: 컨설팅": f"type: {ptype}",
            "updated: 2026-06-15": f"updated: {today}"}
    for rel in ["README.md", "CLAUDE.md", os.path.join("00_관리", "_현황.md"),
                os.path.join("00_관리", "_브리프.md"), os.path.join("00_관리", "_스쿼드.md")]:
        fp = os.path.join(dest, rel)
        if os.path.exists(fp):
            txt = io.open(fp, encoding="utf-8").read()
            for a, b in repl.items():
                txt = txt.replace(a, b)
            io.open(fp, "w", encoding="utf-8").write(txt)
    print(f"✅ 생성: projects/{name}  (유형: {ptype})")
    print("   다음: 00_관리/_브리프.md 작성 → @CoS가 스쿼드 차출")
    return 0

if __name__ == "__main__":
    sys.exit(main())
