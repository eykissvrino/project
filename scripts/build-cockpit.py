# -*- coding: utf-8 -*-
"""VRIN Cockpit 렌더러
projects/*/00_관리/_현황.md 의 프론트매터를 읽어 cockpit.html 생성.
외부 의존성 없음. 실행: python scripts/build-cockpit.py
"""
import glob, os, re, html, io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

HUB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHASES = ["Frame", "Plan", "Produce", "Critique", "Validate", "Deliver", "Learn"]
STATUS = {"green": ("#22c55e", "정상"), "amber": ("#f59e0b", "주의"), "red": ("#ef4444", "지연")}
DEPT_COLOR = {"@STR": "#6366f1", "@HR": "#14b8a6", "@RES": "#0ea5e9", "@PT": "#a855f7",
              "@GTM": "#f59e0b", "@DEL": "#ec4899", "@LEG": "#64748b", "@CoS": "#94a3b8"}


def parse_fm(path):
    try:
        txt = io.open(path, encoding="utf-8").read()
    except Exception:
        return None
    m = re.search(r"^---\s*\n(.*?)\n---", txt, re.S)
    if not m:
        return None
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm


def parse_squad(s):
    if not s:
        return []
    return [x.strip().strip('"').strip("'") for x in re.sub(r"[\[\]]", "", s).split(",") if x.strip()]


def esc(s):
    return html.escape(str(s if s is not None else ""))


def gauge(phase):
    try:
        ph = int(phase)
    except Exception:
        ph = 0
    return "".join("●" if i < ph else "○" for i in range(7)), ph


# 수집
files = sorted(glob.glob(os.path.join(HUB, "projects", "*", "00_관리", "_현황.md")))
projects = []
for f in files:
    fm = parse_fm(f)
    if fm and fm.get("project"):
        projects.append(fm)

total = len(projects)
cnt = {"green": 0, "amber": 0, "red": 0}
dept_use = {}
for p in projects:
    st = p.get("status", "green")
    cnt[st] = cnt.get(st, 0) + 1
    lead = p.get("lead", "")
    if lead:
        dept_use[lead] = dept_use.get(lead, 0) + 1

# 행
rows = ""
for p in sorted(projects, key=lambda x: -(int(x.get("phase", 0) or 0))):
    g, ph = gauge(p.get("phase", 0))
    sc, sl = STATUS.get(p.get("status", "green"), ("#94a3b8", "-"))
    lead = p.get("lead", "")
    lc = DEPT_COLOR.get(lead, "#94a3b8")
    squad = parse_squad(p.get("squad", ""))
    chips = " ".join(f'<span class="chip">{esc(s)}</span>' for s in squad[:6])
    phname = PHASES[ph - 1] if 1 <= ph <= 7 else "-"
    rows += (
        "<tr>"
        f'<td><b>{esc(p.get("project"))}</b><div class="cli">{esc(p.get("client"))} · {esc(p.get("type"))}</div></td>'
        f'<td class="gauge">{g} <span class="pn">{ph}/7 {phname}</span></td>'
        f'<td><span class="lead" style="border-color:{lc};color:{lc}">{esc(lead)}</span> {chips}</td>'
        f'<td><span class="dot" style="background:{sc}"></span>{sl}</td>'
        f'<td>{esc(p.get("next"))}</td>'
        f'<td class="due">{esc(p.get("due"))}</td>'
        "</tr>"
    )
if not rows:
    rows = '<tr><td colspan="6" style="color:#9aa0ac">등록된 _현황.md 없음 — 프로젝트에 00_관리/_현황.md 추가</td></tr>'

dept_bars = ""
for d, n in sorted(dept_use.items(), key=lambda x: -x[1]):
    c = DEPT_COLOR.get(d, "#94a3b8")
    dept_bars += f'<span class="ub"><span class="ubn" style="color:{c}">{esc(d)}</span> <b>{n}</b></span>'
if not dept_bars:
    dept_bars = "-"

CSS = r"""<style>
:root{--bg:#0f1117;--panel:#171a22;--line:#2a2f3a;--txt:#e8eaed;--mut:#9aa0ac}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--txt);font-family:-apple-system,"Segoe UI","Malgun Gothic",sans-serif;padding:26px;line-height:1.45}
h1{font-size:21px;font-weight:800}
.sub{color:var(--mut);font-size:12px;margin:3px 0 18px}
.kpi{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:16px}
.k{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:10px 16px;font-size:13px}
.k b{font-size:20px;display:block}
table{width:100%;border-collapse:collapse;background:var(--panel);border:1px solid var(--line);border-radius:12px;overflow:hidden}
th,td{text-align:left;padding:11px 13px;border-bottom:1px solid var(--line);font-size:13px;vertical-align:top}
th{color:var(--mut);font-size:11px;font-weight:700;letter-spacing:.5px}
tr:last-child td{border-bottom:none}
.cli{color:var(--mut);font-size:11px;margin-top:2px}
.gauge{font-size:13px;letter-spacing:2px;color:#22c55e;white-space:nowrap}
.pn{color:var(--mut);font-size:11px;letter-spacing:0;margin-left:6px}
.lead{border:1px solid;border-radius:6px;padding:1px 6px;font-size:11px;font-weight:700}
.chip{background:#1c2029;border:1px solid var(--line);border-radius:6px;padding:1px 6px;font-size:10.5px;color:var(--mut)}
.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px;vertical-align:middle}
.due{color:var(--mut);font-size:12px;white-space:nowrap}
.util{margin-top:16px;background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:12px 16px;font-size:13px}
.ub{display:inline-block;margin-right:18px}.ubn{font-weight:700}
.foot{color:var(--mut);font-size:11px;margin-top:14px}
.banner{background:#241d12;border:1px solid #d98a3d;border-radius:8px;padding:8px 12px;font-size:12px;margin-bottom:14px;color:#e8c89a}
</style>"""

doc = (
    '<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    "<title>VRIN Cockpit</title>" + CSS + "</head><body>"
    '<h1>📊 VRIN Cockpit <span style="font-size:12px;color:#9aa0ac">— 실시간 수행 현황</span></h1>'
    '<div class="sub">소스: 각 프로젝트 00_관리/_현황.md · 갱신: python scripts/build-cockpit.py</div>'
    '<div class="banner">⚠️ 초기 스냅샷입니다 — 각 프로젝트 <b>_현황.md</b>의 phase·status·progress를 실제 값으로 갱신하면 자동 반영됩니다.</div>'
    '<div class="kpi">'
    f'<div class="k"><b>{total}</b>활성 프로젝트</div>'
    f'<div class="k"><b style="color:#22c55e">{cnt["green"]}</b>🟢 정상</div>'
    f'<div class="k"><b style="color:#f59e0b">{cnt["amber"]}</b>🟡 주의</div>'
    f'<div class="k"><b style="color:#ef4444">{cnt["red"]}</b>🔴 지연</div>'
    "</div>"
    "<table>"
    "<tr><th>프로젝트</th><th>단계 (7-스프린트)</th><th>스쿼드</th><th>상태</th><th>다음 액션</th><th>마감</th></tr>"
    + rows +
    "</table>"
    f'<div class="util"><b>부서 가동률(리드 기준)</b> &nbsp; {dept_bars}</div>'
    f'<div class="foot">VRIN OS v2.1 · 매트릭스 조직 · {total}개 프로젝트</div>'
    "</body></html>"
)

out = os.path.join(HUB, "cockpit.html")
io.open(out, "w", encoding="utf-8").write(doc)
print(f"cockpit.html 생성 완료 — 프로젝트 {total}개")
print(out)
