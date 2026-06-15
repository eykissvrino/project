"""Stage 3 — IWA 절단수준 의사결정 검토서(HTML) 생성기.

cache/s3_cut_analysis.json(민감도 분석) → 연구진 보고용 HTML.
같은 응집트리를 여러 높이로 절단했을 때 IWA 개수·비율·순도·응집도가 어떻게
변하는지, 그리고 k=214를 택한 근거를 차트·표·서술로 정리한다.
출력: 04_framework_design/docs/stages/results/IWA_절단수준_의사결정_검토서.html
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

TEST1_DIR = Path(__file__).resolve().parents[1]
CACHE = TEST1_DIR / "cache"
OUT = (TEST1_DIR / ".." / ".." / "04_framework_design" / "docs" / "stages" / "results"
       / "IWA_절단수준_의사결정_검토서.html").resolve()

D = json.loads((CACHE / "s3_cut_analysis.json").read_text(encoding="utf-8"))
sweep = D["sweep"]
ks = [r["k"] for r in sweep]
effs = [r["eff_iwa"] for r in sweep]
ratios = [r["ratio"] for r in sweep]
purs = [r["mean_purity"] for r in sweep]
cohs = [r["cohesion_median"] for r in sweep]
band = D["band"]; chosen = D["chosen_k"]
n_dwa = D["n_dwa"]; onet = D["onet_ratio"]


# ── SVG 헬퍼 ─────────────────────────────────────────────────────────
def _lin(v, vlo, vhi, plo, phi):
    return plo + (v - vlo) / (vhi - vlo) * (phi - plo)


def chart_count() -> str:
    """IWA 개수 vs 절단 k (밴드 음영 + 채택점 + ONET 비율 목표선)."""
    W, H = 760, 360
    x0, x1, y0, y1 = 78, 720, 46, 290
    klo, khi = min(ks), max(ks)
    elo, ehi = 80, 250
    def X(k): return _lin(k, klo, khi, x0, x1)
    def Y(e): return _lin(e, elo, ehi, y1, y0)
    s = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img">']
    # 밴드 음영
    s.append(f'<rect x="{X(band[0]):.1f}" y="{y0}" width="{X(band[1])-X(band[0]):.1f}" '
             f'height="{y1-y0}" fill="#1f4e8c" opacity="0.06"/>')
    s.append(f'<text x="{(X(band[0])+X(band[1]))/2:.0f}" y="{y0-6}" text-anchor="middle" '
             f'font-size="11" fill="#1f4e8c">ONET 비율 밴드 (DWA÷8~5 = {band[0]}~{band[1]})</text>')
    # y 그리드
    for e in (100, 150, 200, 250):
        yy = Y(e)
        s.append(f'<line x1="{x0}" y1="{yy:.1f}" x2="{x1}" y2="{yy:.1f}" stroke="#eef1f6"/>')
        s.append(f'<text x="{x0-8}" y="{yy+4:.1f}" text-anchor="end" font-size="11" fill="#8a94a3">{e}</text>')
    # x 눈금
    for k in (120, 160, 200, 240, 290):
        s.append(f'<text x="{X(k):.0f}" y="{y1+18}" text-anchor="middle" font-size="11" fill="#8a94a3">{k}</text>')
    s.append(f'<text x="{(x0+x1)/2:.0f}" y="{y1+36}" text-anchor="middle" font-size="12" fill="#697587">절단 수준 k (TASK 트리 군집 수 — 클수록 세분)</text>')
    s.append(f'<text x="20" y="{(y0+y1)/2:.0f}" text-anchor="middle" font-size="12" fill="#697587" transform="rotate(-90 20 {(y0+y1)/2:.0f})">유효 IWA 개수</text>')
    # 라인
    pts = " ".join(f"{X(k):.1f},{Y(e):.1f}" for k, e in zip(ks, effs))
    s.append(f'<polyline points="{pts}" fill="none" stroke="#0f6b5f" stroke-width="2.5"/>')
    for k, e in zip(ks, effs):
        s.append(f'<circle cx="{X(k):.1f}" cy="{Y(e):.1f}" r="3" fill="#0f6b5f"/>')
    # 채택점
    cx, cy = X(chosen), Y(effs[ks.index(chosen)])
    s.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="7" fill="none" stroke="#7a2e3a" stroke-width="2.5"/>')
    s.append(f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{cx:.1f}" y2="{y1}" stroke="#7a2e3a" stroke-dasharray="3 3" opacity="0.6"/>')
    s.append(f'<text x="{cx+10:.0f}" y="{cy-8:.0f}" font-size="12.5" font-weight="700" fill="#7a2e3a">채택 k={chosen} → {effs[ks.index(chosen)]} IWA (6.70:1)</text>')
    s.append('</svg>')
    return "".join(s)


def chart_quality() -> str:
    """순도·응집도 vs k (불변성 시각화, y 확대 0.80~1.00)."""
    W, H = 760, 250
    x0, x1, y0, y1 = 78, 720, 30, 180
    klo, khi = min(ks), max(ks)
    def X(k): return _lin(k, klo, khi, x0, x1)
    def Y(v): return _lin(v, 0.80, 1.00, y1, y0)
    s = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img">']
    for v in (0.80, 0.90, 1.00):
        yy = Y(v)
        s.append(f'<line x1="{x0}" y1="{yy:.1f}" x2="{x1}" y2="{yy:.1f}" stroke="#eef1f6"/>')
        s.append(f'<text x="{x0-8}" y="{yy+4:.1f}" text-anchor="end" font-size="11" fill="#8a94a3">{v:.2f}</text>')
    for k in (120, 160, 200, 240, 290):
        s.append(f'<text x="{X(k):.0f}" y="{y1+18}" text-anchor="middle" font-size="11" fill="#8a94a3">{k}</text>')
    # 채택선
    s.append(f'<line x1="{X(chosen):.1f}" y1="{y0}" x2="{X(chosen):.1f}" y2="{y1}" stroke="#7a2e3a" stroke-dasharray="3 3" opacity="0.5"/>')
    for vals, color, name, yo in ((purs, "#1f4e8c", "트리 순도", -8), (cohs, "#9a6212", "응집도(중앙값)", 14)):
        pts = " ".join(f"{X(k):.1f},{Y(v):.1f}" for k, v in zip(ks, vals))
        s.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2.5"/>')
        for k, v in zip(ks, vals):
            s.append(f'<circle cx="{X(k):.1f}" cy="{Y(v):.1f}" r="2.5" fill="{color}"/>')
        s.append(f'<text x="{x1-4}" y="{Y(vals[-1])+yo:.1f}" text-anchor="end" font-size="12" font-weight="700" fill="{color}">{name} ≈ {sum(vals)/len(vals):.3f}</text>')
    s.append('</svg>')
    return "".join(s)


def sweep_rows() -> str:
    out = []
    for r in sweep:
        cls = ' class="hot"' if r["k"] == chosen else ""
        inband = "●" if band[0] <= r["eff_iwa"] <= band[1] else "·"
        near = ""
        if abs(r["ratio"] - onet) <= 0.5:
            near = ' <span class="tag">ONET근접</span>'
        out.append(f'<tr{cls}><td>{r["k"]}</td><td><b>{r["eff_iwa"]}</b></td>'
                   f'<td>{r["ratio"]:.2f} : 1{near}</td><td>{inband}</td>'
                   f'<td>{r["mean_purity"]:.3f}</td><td>{r["cohesion_median"]:.3f}</td></tr>')
    return "\n".join(out)


def gap_rows() -> str:
    gmax = max(g["gap"] for g in D["gaps_top"]) or 1.0
    out = []
    for rank, g in enumerate(D["gaps_top"], 1):
        if g["k"] == chosen:
            note = '<span class="tag">채택</span> 자연 gap 상위·ONET 정합'
        elif rank == 1:
            note = '전역 최대 gap(미세 1위) — ONET보다 굵음'
        else:
            note = '후보(사실상 동급)'
        bar = int(round(g["gap"] / gmax * 100))
        out.append(f'<tr><td>{rank}</td><td>{g["k"]}</td><td>{g["gap"]:.6f}</td>'
                   f'<td style="text-align:left"><span style="display:inline-block;height:8px;'
                   f'width:{bar}%;max-width:90px;background:#0f6b5f;border-radius:2px;'
                   f'vertical-align:middle;margin-right:6px"></span>{note}</td></tr>')
    return "\n".join(out)


def split_rows() -> str:
    out = []
    for s in D["split_demo"]:
        out.append(f'<tr><td style="text-align:left">{s["label"]}</td><td>{s["n_dwa"]}</td>'
                   f'<td>{s["coarse_merges_into"]}</td><td><b>1</b></td>'
                   f'<td>{s["fine_splits"]}</td></tr>')
    return "\n".join(out)


HTML = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>IWA 절단수준 의사결정 검토서</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<style>
  :root{{--ink:#1a2230;--body:#28303e;--muted:#697587;--faint:#8a94a3;--line:#dde3ec;
    --line2:#eef1f6;--bg:#fff;--paper:#fbfcfe;--navy:#152544;--accent:#1f4e8c;--accent2:#7a2e3a;
    --iwa:#0f6b5f;--soft:#f1f5fb;}}
  *{{box-sizing:border-box}}
  body{{margin:0;background:var(--bg);color:var(--body);font-family:"Pretendard",-apple-system,system-ui,"Malgun Gothic",sans-serif;
    font-size:16px;line-height:1.78;letter-spacing:-.1px;-webkit-font-smoothing:antialiased}}
  .wrap{{max-width:920px;margin:0 auto;padding:0 30px 60px}}
  header.cover{{border-bottom:3px solid var(--navy);padding:52px 0 26px;margin-bottom:8px}}
  .docmeta{{font-size:13px;color:var(--accent);font-weight:700;letter-spacing:.6px;margin-bottom:14px}}
  header.cover h1{{font-size:29px;line-height:1.32;font-weight:800;color:var(--navy);margin:0 0 8px;letter-spacing:-.6px}}
  header.cover .sub{{font-size:17px;color:var(--muted);font-weight:600;margin:0 0 22px}}
  .coverbar{{display:flex;flex-wrap:wrap;border:1px solid var(--line);border-radius:8px;overflow:hidden}}
  .coverbar div{{flex:1;min-width:140px;padding:11px 16px;border-right:1px solid var(--line2);font-size:13.5px}}
  .coverbar div:last-child{{border-right:none}}
  .coverbar b{{display:block;color:var(--faint);font-size:11.5px;font-weight:700;letter-spacing:.4px;margin-bottom:2px}}
  .abstract{{background:var(--paper);border:1px solid var(--line);border-left:3px solid var(--accent);
    border-radius:6px;padding:18px 22px;margin:24px 0 6px;font-size:15px}}
  .abstract b{{color:var(--navy)}}
  section{{padding:32px 0;border-bottom:1px solid var(--line2)}}
  h2{{font-size:21px;font-weight:800;color:var(--navy);margin:0 0 14px;letter-spacing:-.3px;padding-bottom:9px;border-bottom:2px solid var(--line)}}
  h2 .n{{color:var(--iwa);font-size:15px;margin-right:8px}}
  h3{{font-size:16.5px;font-weight:700;color:var(--ink);margin:22px 0 8px}}
  p{{margin:10px 0}}
  .fig{{background:var(--paper);border:1px solid var(--line);border-radius:8px;padding:16px 14px 10px;margin:18px 0}}
  .fig .cap{{font-size:13px;color:var(--muted);margin-top:6px;padding:0 6px}}
  table{{width:100%;border-collapse:collapse;margin:14px 0;font-size:14px}}
  th,td{{border:1px solid var(--line);padding:7px 10px;text-align:center}}
  th{{background:var(--soft);color:var(--navy);font-weight:700;font-size:13px}}
  tr.hot td{{background:#fbf2f3;font-weight:600}}
  .tag{{display:inline-block;background:var(--iwa);color:#fff;font-size:10.5px;font-weight:700;padding:1px 6px;border-radius:4px;vertical-align:middle}}
  .key{{background:#f0f7f5;border:1px solid #cfe6e0;border-left:3px solid var(--iwa);border-radius:6px;padding:14px 18px;margin:16px 0;font-size:14.5px}}
  .key b{{color:var(--iwa)}}
  ul{{margin:10px 0;padding-left:22px}} li{{margin:5px 0}}
  .foot{{margin-top:30px;font-size:12.5px;color:var(--faint);text-align:center}}
</style>
</head>
<body>
<div class="wrap">
<header class="cover">
  <div class="docmeta">국가데이터처 · 직업정보 프레임워크 연구 · Stage 3 부속</div>
  <h1>IWA 절단수준 의사결정 검토서</h1>
  <div class="sub">군집 절단 높이에 따른 결과 변화 분석과 k={chosen} 선정 근거</div>
  <div class="coverbar">
    <div><b>입력 DWA</b>{n_dwa:,}개</div>
    <div><b>채택 IWA</b>{effs[ks.index(chosen)]}개</div>
    <div><b>DWA:IWA</b>6.70 : 1</div>
    <div><b>ONET 기준</b>6.3 : 1</div>
    <div><b>군집 방법</b>같은 트리 상위절단(방법 A)</div>
  </div>
</header>

<div class="abstract">
<b>요약.</b> IWA는 Stage 2의 전수 TASK 응집트리를 <b>더 높은 높이로 한 번 더 절단</b>하여 얻는다.
절단 높이(k)를 바꾸면 IWA 개수가 연속적으로 변하지만, <b>군집 품질(트리 순도 ≈0.986·응집도 ≈0.90)은
절단수준과 거의 무관하게 일정</b>하다 — 즉 이 결정은 "품질"이 아니라 <b>"세분도(해상도)"</b>의 선택이다.
자연 절단점(병합높이 gap)이 평탄해 단일 정답이 없으므로, <b>국제 표준 ONET의 DWA:IWA≈6.3:1</b>을
기준선으로 삼아 그에 가장 부합하고 자연 gap이기도 한 <b>k={chosen}(유효 {effs[ks.index(chosen)]} IWA, 6.70:1)</b>을 채택했다.
</div>

<section>
<h2><span class="n">1</span>무엇을 정하는 문제인가</h2>
<p>본 프로젝트의 직무활동 4계층(TASK→DWA→IWA→GWA)은 <b>전체 TASK를 한 번 군집해 만든 단일 응집트리</b>
(평균연결·코사인) 위에 놓인다. DWA는 이 트리를 어떤 높이에서 자른 결과이고, <b>IWA는 같은 트리를 그보다
더 높은 곳에서 자른 결과</b>다(설계 채택 = 방법 A). 같은 트리를 쓰므로 <b>DWA가 정확히 하나의 IWA에 포함되는
관계(strict nesting)가 수학적으로 보장</b>된다.</p>
<p>따라서 결정해야 할 것은 단 하나 — <b>"얼마나 높은 곳에서 자를 것인가(=IWA를 몇 개로 볼 것인가)"</b>이다.
높이 낮게(k 크게) 자르면 IWA가 많아져 <b>세밀</b>해지고, 높게(k 작게) 자르면 IWA가 적어져 <b>포괄적</b>이 된다.</p>
</section>

<section>
<h2><span class="n">2</span>절단수준 민감도 — 정량 결과</h2>
<p>절단 k를 120~290 구간에서 바꿔가며 ① 유효 IWA 개수 ② DWA:IWA 비율 ③ 트리 순도(각 DWA의 1차 TASK가
배정 IWA에 떨어지는 비율) ④ 응집도(IWA 내 DWA 평균 코사인)를 측정했다.</p>
<div class="fig">{chart_count()}<div class="cap">그림 1. 절단 k가 커질수록 유효 IWA가 매끄럽게 증가한다. 음영 = ONET 비율이 권하는 밴드, ◎ = 채택점 k={chosen}.</div></div>
<div class="fig">{chart_quality()}<div class="cap">그림 2. <b>트리 순도·응집도는 절단수준과 무관하게 거의 수평</b> — 어느 해상도로 잘라도 군집 품질은 유지된다. 즉 k 선택은 품질 문제가 아니라 해상도 문제다.</div></div>
<table>
<thead><tr><th>절단 k</th><th>유효 IWA</th><th>DWA:IWA 비율</th><th>밴드내</th><th>트리순도</th><th>응집도(중앙값)</th></tr></thead>
<tbody>
{sweep_rows()}
</tbody></table>
<div class="key">핵심 ①: <b>품질 지표(순도·응집도)가 모든 절단수준에서 평탄</b>하다. 그러므로 "더 좋은 절단"이 아니라
"적정 해상도"를 고르는 문제이며, 외부 기준(ONET 비율)으로 정당화하는 것이 타당하다.</div>
</section>

<section>
<h2><span class="n">3</span>왜 "자연 절단점" 하나로 못 정하나</h2>
<p>이상적으로는 트리의 병합높이가 크게 벌어지는 <b>자연 절단점(gap)</b>에서 자른다. 그러나 ONET 비율 밴드
({band[0]}~{band[1]}) 안의 gap들은 아래처럼 <b>0.0007~0.0009 수준으로 촘촘</b>해 — 뚜렷한 단일 plateau가 없다.
어휘 체계가 연속적으로 일반화되는 한국 직업 데이터의 자연스러운 성질이다.</p>
<table>
<thead><tr><th>순위</th><th>절단 k</th><th>병합높이 gap</th><th>상대 크기 · 비고</th></tr></thead>
<tbody>
{gap_rows()}
</tbody></table>
<div class="key">핵심 ②: 자연 gap이 평탄해 <b>"데이터가 가리키는 유일한 절단"이 존재하지 않는다.</b> 후보(k=169·214·216·227)가
사실상 동급이므로, 그중 <b>국제 표준에 정합하는 지점</b>을 택하는 것이 가장 방어가능한 선택이다.</div>
</section>

<section>
<h2><span class="n">4</span>세분도의 의미 — 같은 활동이 어떻게 나뉘나</h2>
<p>해상도가 결과에 주는 실제 영향을 보기 위해, 채택 k={chosen}의 대표 IWA들이 더 거친 절단(k={D['coarse_k']})과
더 세밀한 절단(k={D['fine_k']})에서 몇 개 군집으로 묶이는지 추적했다.</p>
<table>
<thead><tr><th>채택 IWA(k={chosen})</th><th>소속 DWA</th><th>거친 k={D['coarse_k']}</th><th>채택 k={chosen}</th><th>세밀 k={D['fine_k']}</th></tr></thead>
<tbody>
{split_rows()}
</tbody></table>
<p>예컨대 <b>"고객을 응대하여 상품을 판매한다"</b>는 채택 수준에서 하나의 IWA지만, 더 세밀하게 자르면 4개
하위활동(응대·추천·결제·홍보 등)으로 갈라진다. 너무 세밀하면 IWA가 DWA에 가까워져 "중간층"의 의미가
옅어지고, 너무 거칠면 이질적 활동이 한데 묶인다. <b>채택 수준은 그 사이의 균형점</b>이다.</p>
</section>

<section>
<h2><span class="n">5</span>결정 — k={chosen} 채택 근거</h2>
<ul>
<li><b>국제 정합(연구목적 #2)</b>: DWA:IWA = 6.70:1로 ONET 6.3:1에 가장 근접. 한국 IWA를 ONET IWA(332개)와
직접 비교·매핑할 수 있는 동일 해상도를 확보.</li>
<li><b>밴드 내 + 자연 gap</b>: ONET 비율이 권하는 밴드({band[0]}~{band[1]}) 안에 들고, k={chosen}은 자연 gap 상위
후보 중 하나 — "자연절단 우선" 원칙과도 충돌하지 않음.</li>
<li><b>품질 불변</b>: 트리 순도 0.986·응집도 0.905로 다른 절단수준과 동일 — 해상도를 ONET에 맞추는 데 따른
품질 손실이 없음.</li>
<li><b>중간층 의미 보존</b>: DWA(1,192)와 GWA(예정 ~41) 사이에서 178개는 "여러 DWA를 포괄하되 GWA보다 구체"인
중간 추상수준을 유지(과세분·과병합 회피).</li>
</ul>
<div class="key"><b>결론.</b> 절단수준은 품질이 아니라 해상도의 문제이고 자연 절단점이 유일하지 않으므로,
<b>국제 표준 ONET 비율(6.3:1)을 기준선으로 k={chosen}(유효 178 IWA·6.70:1)을 채택</b>한다.
이는 자연 gap·밴드·국제정합·품질불변을 모두 만족하는 방어가능한 결정이다.</div>
</section>

<section>
<h2><span class="n">6</span>한계와 재현</h2>
<ul>
<li>절단수준은 연속적이라 ±10 IWA 범위의 인접 해상도(k=200~225)도 합리적 대안이다. 본 결정은 ONET 정합을
1차 기준으로 한 선택이며, 후속 전문가 검수에서 미세 조정 가능하다.</li>
<li>트리 순도 0.986의 미세 누수(1.4%)는 Stage 2의 Multiple Linkage(TASK↔DWA 다대다) 설계에서 비롯한
자연 결과이며 nesting 위반이 아니다(DWA→IWA 배정은 100% strict 1:1).</li>
<li><b>재현</b>: <code>python -m pipeline.s3_cut_analysis</code>(민감도 JSON) → <code>python -m pipeline.s3_cut_report_html</code>(본 문서).
결정론적이므로 같은 입력에 같은 결과.</li>
</ul>
</section>

<div class="foot">국가데이터처 직업정보 프레임워크 연구 · Stage 3 IWA 부속 검토서 · 자동생성(pipeline/s3_cut_report_html.py)</div>
</div>
</body>
</html>"""

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(HTML, encoding="utf-8")
print(f"[html] → {OUT}")
