"""Stage 4b — 상향식 GWA 적재 + Excel + 결과해설서(자기완결 실험).

기존 Stage4(gwa/iwa_to_gwa)는 건드리지 않는다. 신규 테이블(CREATE IF NOT EXISTS):
    kr_domain_bottomup, kr_gwa_bottomup, iwa_to_kr_gwa
입력: cache/s4b_clusters.json + s4b_domain_result.json + s4b_gwa_result.json + s4b_summary.json
산출: outputs/S4b_상향식GWA도출.xlsx + 04_framework_design/docs/stages/results/Stage4b_상향식GWA_결과해설서.md
PYTHONUTF8=1 권장.
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

import numpy as np
import pandas as pd

TEST1_DIR = Path(__file__).resolve().parents[1]
CACHE = TEST1_DIR / "cache"
OUTPUTS = TEST1_DIR / "outputs"
RESULTS = (TEST1_DIR / ".." / ".." / "04_framework_design" / "docs"
           / "stages" / "results").resolve()

CLUSTERS = CACHE / "s4b_clusters.json"
DOM_RES = CACHE / "s4b_domain_result.json"
GWA_RES = CACHE / "s4b_gwa_result.json"
SUMMARY = CACHE / "s4b_summary.json"
IWA_CENT = CACHE / "s4_iwa_centroids.npy"
IWA_IDS = CACHE / "s4_iwa_ids.json"
GWA_EMB = CACHE / "s4_gwa_emb.npy"
GWA_ORDER = CACHE / "s4_gwa_order.json"
TRANSLATION = CACHE / "s4_translation.json"
ONET_DOMAIN = {"4.A.1": "정보 입력", "4.A.2": "정신 과정",
               "4.A.3": "작업 산출", "4.A.4": "타인과의 상호작용"}


def _onet_domain(gid: str) -> str:
    for p, n in ONET_DOMAIN.items():
        if gid.startswith(p):
            return n
    return "기타"


def _onet_reverse(con) -> list[dict]:
    """역방향 비교: ONET 41 각각 → 최근접 KR-GWA + 표출 여부.

    표출(emergent) = 그 ONET GWA가 어떤 KR-GWA의 '최근접'으로 지목됨(우리 체계에 독립 범주로 자생).
    미표출 = 어떤 KR-GWA의 최근접으로도 지목되지 않음(ONET엔 있으나 우리 상향식엔 독립 GWA로 없음).
    """
    iwa_emb = np.load(IWA_CENT)
    iwa_ids = json.loads(IWA_IDS.read_text(encoding="utf-8"))
    rowof = {i: k for k, i in enumerate(iwa_ids)}
    gwa_emb = np.load(GWA_EMB)
    order = json.loads(GWA_ORDER.read_text(encoding="utf-8"))
    trans = {t["onet_gwa_id"]: t for t in
             json.loads(TRANSLATION.read_text(encoding="utf-8"))}
    m = con.execute("SELECT iwa_id, kr_gwa_id FROM iwa_to_kr_gwa").fetchall()
    names = {r[0]: r[1] for r in
             con.execute("SELECT kr_gwa_id, label_kr FROM kr_gwa_bottomup").fetchall()}
    matched = {r[0] for r in
               con.execute("SELECT DISTINCT nearest_onet FROM kr_gwa_bottomup").fetchall()}
    from collections import defaultdict
    mem = defaultdict(list)
    for iid, kg in m:
        mem[kg].append(iid)
    kg_ids = sorted(mem)
    cents = []
    for kg in kg_ids:
        v = iwa_emb[[rowof[i] for i in mem[kg]]].mean(0)
        cents.append(v / (np.linalg.norm(v) or 1.0))
    C = np.vstack(cents)
    sim = gwa_emb @ C.T                       # (41 × k)
    out = []
    for j, gid in enumerate(order):
        b = int(np.argmax(sim[j])); cos = float(sim[j][b])
        out.append({
            "onet_gwa_id": gid, "label_kr": trans[gid]["label_kr"],
            "onet_label_en": trans[gid]["onet_label_en"],
            "domain": _onet_domain(gid),
            "emergent": gid in matched,
            "nearest_kr": names[kg_ids[b]], "nearest_cos": round(cos, 3)})
    return out

SCHEMA = """
CREATE TABLE IF NOT EXISTS kr_domain_bottomup (
    domain_id VARCHAR PRIMARY KEY, label_kr VARCHAR, definition VARCHAR,
    n_iwa INTEGER, nearest_onet_domain VARCHAR, nearest_cosine DOUBLE);
CREATE TABLE IF NOT EXISTS kr_gwa_bottomup (
    kr_gwa_id VARCHAR PRIMARY KEY, label_kr VARCHAR, definition VARCHAR,
    domain_id VARCHAR, n_iwa INTEGER, cohesion DOUBLE,
    nearest_onet VARCHAR, nearest_onet_label VARCHAR,
    nearest_onet_domain VARCHAR, nearest_cosine DOUBLE);
CREATE TABLE IF NOT EXISTS iwa_to_kr_gwa (
    iwa_id VARCHAR PRIMARY KEY, kr_gwa_id VARCHAR);
"""


def _load():
    c = json.loads(CLUSTERS.read_text(encoding="utf-8"))
    dom_names = {x["domain_id"]: x for x in json.loads(DOM_RES.read_text(encoding="utf-8"))}
    gwa_names = {x["kr_gwa_id"]: x for x in json.loads(GWA_RES.read_text(encoding="utf-8"))}
    summary = json.loads(SUMMARY.read_text(encoding="utf-8")) if SUMMARY.exists() else {}
    return c, dom_names, gwa_names, summary


def persist():
    from pipeline import gwa_rules, db
    c, dom_names, gwa_names, _ = _load()
    con = db.get_con()
    con.execute("BEGIN")
    try:
        for stmt in SCHEMA.strip().split(";"):
            if stmt.strip():
                con.execute(stmt)
        con.execute("DELETE FROM kr_domain_bottomup")
        con.execute("DELETE FROM kr_gwa_bottomup")
        con.execute("DELETE FROM iwa_to_kr_gwa")
        for d in c["domains"]:
            nm = dom_names.get(d["domain_id"], {})
            con.execute("INSERT INTO kr_domain_bottomup VALUES (?,?,?,?,?,?)",
                        [d["domain_id"], gwa_rules.normalize_label(nm.get("label_kr", d["domain_id"])),
                         nm.get("definition_kr", ""), d["n_iwa"],
                         d["nearest_onet_domain"], d["nearest_cosine"]])
        for g in c["gwas"]:
            nm = gwa_names.get(g["kr_gwa_id"], {})
            con.execute("INSERT INTO kr_gwa_bottomup VALUES (?,?,?,?,?,?,?,?,?,?)",
                        [g["kr_gwa_id"], gwa_rules.normalize_label(nm.get("label_kr", g["kr_gwa_id"])),
                         nm.get("definition_kr", ""), g["domain_id"], g["n_iwa"],
                         g["cohesion"], g["nearest_onet"], g["nearest_onet_label"],
                         g["nearest_onet_domain"], g["nearest_cosine"]])
            for iwa_id in g["member_iwa_ids"]:
                con.execute("INSERT INTO iwa_to_kr_gwa VALUES (?,?)", [iwa_id, g["kr_gwa_id"]])
        con.execute("COMMIT")
    except Exception:
        con.execute("ROLLBACK"); raise
    nd = con.execute("SELECT COUNT(*) FROM kr_domain_bottomup").fetchone()[0]
    ng = con.execute("SELECT COUNT(*) FROM kr_gwa_bottomup").fetchone()[0]
    nm = con.execute("SELECT COUNT(*) FROM iwa_to_kr_gwa").fetchone()[0]
    dup = con.execute("SELECT COUNT(*) FROM (SELECT iwa_id FROM iwa_to_kr_gwa "
                      "GROUP BY iwa_id HAVING COUNT(*)<>1)").fetchone()[0]
    con.close()
    print(f"[persist] kr_domain {nd} · kr_gwa {ng} · iwa_to_kr_gwa {nm} · 중복 {dup}")
    return {"domains": nd, "gwa": ng, "map": nm, "dup": dup}


# ── Excel ────────────────────────────────────────────────────────────
_MAX_W = 60


def _write_xlsx(path, sheets):
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(path, engine="openpyxl") as xw:
        for name, df in sheets.items():
            df.to_excel(xw, sheet_name=name, index=False)
            ws = xw.sheets[name]
            for i, col in enumerate(df.columns, 1):
                lens = sorted(len(str(v)) for v in df[col].tolist()
                              if v is not None and not (isinstance(v, float) and pd.isna(v)))
                body = lens[int(len(lens) * 0.9)] if lens else 10
                ws.column_dimensions[ws.cell(row=1, column=i).column_letter].width = \
                    min(max(len(str(col)), body) + 2, _MAX_W)
    print(f"[export] {path.relative_to(TEST1_DIR)} ({sum(len(d) for d in sheets.values())} rows)")


def _data_dict():
    rows = [
        ("(개요)", "—", "Stage 4b: 우리가 도출한 TASK→DWA→IWA에서 출발해 ONET 41 GWA와 '닮은 형태'가 나오도록 명시적 기준을 적용한 순수 상향식 GWA. 기존 Stage4(ONET 채택 트랙1)와 별개 실험.", ""),
        ("(기준)", "ONET-유사화 6기준", "①군집단위=IWA벡터(TASK트리 아님) ②Ward(분산최소·균형, 사슬효과 제거) ③입도=ONET비율 정합 참조 ④2계층=도메인4→GWA(nested) ⑤균형 모니터 ⑥ONET 정합도 검증.", ""),
        ("영역(도메인)", "label_kr/nearest_onet_domain", "상향식 자생 4대 영역(명사형 대범주) + 최근접 ONET 영역", ""),
        ("KR-GWA", "label_kr/domain_id/n_iwa/cohesion", "자생 GWA(명사형) · 소속 영역 · 소속 IWA수 · 응집도(멤버-중심 평균코사인)", ""),
        ("KR-GWA", "nearest_onet/cosine", "각 KR-GWA ↔ 최근접 ONET GWA(한국어)·코사인(구성타당도)", ""),
        ("GWA별IWA", "—", "KR-GWA → 소속 IWA 역추적 펼침", ""),
        ("ONET비교(우리→ONET)", "—", "각 KR-GWA가 ONET 41 중 무엇과 가장 가까운지(우리→ONET 방향)", ""),
        ("★미매칭ONET(우리에없음)", "—", "ONET GWA 중 우리 상향식 KR-GWA로 표출되지 않은 것만 추린 전용 목록. '매칭'=그 ONET이 어떤 KR-GWA의 최근접으로 지목됨. 미매칭=어디에도 안 지목됨(우리 체계에 독립 범주로 없음). '흡수된 우리GWA'=가장 가깝지만 그 우리GWA의 본 정체성은 다른 ONET이라 매칭 실패.", ""),
        ("ONET전체대조", "—", "ONET 41 전체를 매칭(○)/미매칭(✗)으로 표기한 대조표(미매칭이 위로 정렬)", ""),
        ("커버리지", "—", "도메인·GWA 수·균형·ONET 정합 요약", ""),
    ]
    return pd.DataFrame(rows, columns=["시트", "컬럼", "설명", "표기값/예시"])


def export():
    from pipeline import db
    con = db.get_con(read_only=True)
    df_dom = con.execute("""
        SELECT domain_id "영역코드", label_kr "영역명(자생)", definition 정의,
               n_iwa "소속IWA수", nearest_onet_domain "최근접ONET영역",
               ROUND(nearest_cosine,3) "최근접cos"
        FROM kr_domain_bottomup ORDER BY n_iwa DESC""").df()
    df_gwa = con.execute("""
        SELECT g.kr_gwa_id "GWA코드", g.label_kr "KR-GWA명(자생)",
               d.label_kr "소속영역", g.n_iwa "소속IWA수", ROUND(g.cohesion,3) 응집도,
               g.nearest_onet_label "최근접ONET-GWA", g.nearest_onet_domain "ONET영역",
               ROUND(g.nearest_cosine,3) "최근접cos", g.definition 정의
        FROM kr_gwa_bottomup g LEFT JOIN kr_domain_bottomup d ON g.domain_id=d.domain_id
        ORDER BY g.n_iwa DESC, g.kr_gwa_id""").df()
    df_mem = con.execute("""
        SELECT m.kr_gwa_id "GWA코드", g.label_kr "KR-GWA명", i.label "IWA정식명",
               i.n_dwa "IWA소속DWA", i.n_task "IWA소속TASK", i.n_jobs "IWA소속직업"
        FROM iwa_to_kr_gwa m JOIN kr_gwa_bottomup g ON m.kr_gwa_id=g.kr_gwa_id
        JOIN iwa i ON m.iwa_id=i.iwa_id
        ORDER BY m.kr_gwa_id, i.n_dwa DESC""").df()
    df_cmp = con.execute("""
        SELECT label_kr "KR-GWA명(자생)", nearest_onet_label "최근접ONET-GWA",
               nearest_onet_domain "ONET영역", ROUND(nearest_cosine,3) "최근접cos",
               CASE WHEN nearest_cosine>=0.55 THEN '강매칭'
                    WHEN nearest_cosine>=0.45 THEN '약매칭' ELSE '한국특이후보' END 판정
        FROM kr_gwa_bottomup ORDER BY nearest_cosine DESC""").df()

    # 역방향: ONET 41 각각의 매칭/미매칭 (ONET엔 있는데 우리엔 없는 것)
    rev = _onet_reverse(con)
    n_emg = sum(1 for r in rev if r["emergent"])
    DOM_ORDER = {"정보 입력": 0, "정신 과정": 1, "작업 산출": 2, "타인과의 상호작용": 3}

    # (A) ★우리 KR-GWA와 매칭 안 된 ONET GWA만 — 전용 시트
    miss = [r for r in rev if not r["emergent"]]
    df_miss = pd.DataFrame([{
        "ONET코드": r["onet_gwa_id"], "ONET영역": r["domain"],
        "매칭안된 ONET-GWA(한국어)": r["label_kr"], "ONET원문(영문)": r["onet_label_en"],
        "가장 가깝지만 매칭실패→흡수된 우리GWA": r["nearest_kr"], "최근접cos": r["nearest_cos"],
    } for r in sorted(miss, key=lambda x: (DOM_ORDER.get(x["domain"], 9), -x["nearest_cos"]))])

    # (B) ONET 41 전체 대조(매칭여부 첫 컬럼)
    df_onet = pd.DataFrame([{
        "매칭여부": "○ 매칭" if r["emergent"] else "✗ 미매칭(우리에없음)",
        "ONET코드": r["onet_gwa_id"], "ONET영역": r["domain"],
        "ONET-GWA(한국어)": r["label_kr"], "ONET원문": r["onet_label_en"],
        "최근접 우리GWA": r["nearest_kr"], "최근접cos": r["nearest_cos"],
    } for r in sorted(rev, key=lambda x: (x["emergent"], DOM_ORDER.get(x["domain"], 9)))])

    n_gwa = int(con.execute("SELECT COUNT(*) FROM kr_gwa_bottomup").fetchone()[0])
    n_map = int(con.execute("SELECT COUNT(*) FROM iwa_to_kr_gwa").fetchone()[0])
    matched = int(con.execute("SELECT COUNT(DISTINCT nearest_onet) FROM kr_gwa_bottomup").fetchone()[0])
    matched_s = int(con.execute("SELECT COUNT(DISTINCT nearest_onet) FROM kr_gwa_bottomup WHERE nearest_cosine>=0.55").fetchone()[0])
    sizes = [r[0] for r in con.execute("SELECT n_iwa FROM kr_gwa_bottomup").fetchall()]
    coh = [r[0] for r in con.execute("SELECT cohesion FROM kr_gwa_bottomup").fetchall()]
    import statistics
    con.close()
    cov = pd.DataFrame([
        {"지표": "자생 영역(도메인)", "값": len(df_dom)},
        {"지표": "자생 KR-GWA", "값": n_gwa},
        {"지표": "IWA→KR-GWA 매핑", "값": f"{n_map} (strict 1:1)"},
        {"지표": "IWA당 GWA(입도)", "값": round(178 / n_gwa, 2)},
        {"지표": "최대/최소 군집(IWA)", "값": f"{max(sizes)} / {min(sizes)}"},
        {"지표": "단일 IWA 군집", "값": sum(1 for s in sizes if s == 1)},
        {"지표": "응집도 중앙값", "값": round(statistics.median(coh), 3) if coh else 0},
        {"지표": "ONET 41 표출/미표출", "값": f"표출 {n_emg} · 미표출 {41-n_emg} (distinct)"},
        {"지표": "해석", "값": "Ward+IWA단위로 균형 잡힌 ONET형 41범주 자생. 단 ONET 41 중 19개만 우리 체계에 독립 GWA로 표출되고 22개는 미표출(주로 추상 인지·관리·대인 활동→소수 범주에 흡수)."},
    ])

    path = OUTPUTS / "S4b_상향식GWA도출.xlsx"
    _write_xlsx(path, {"데이터사전": _data_dict(), "영역(도메인)": df_dom,
                       "KR-GWA": df_gwa, "GWA별IWA": df_mem,
                       "ONET비교(우리→ONET)": df_cmp,
                       "★미매칭ONET(우리에없음)": df_miss,
                       "ONET전체대조": df_onet, "커버리지": cov})
    return path


# ── 결과해설서 ────────────────────────────────────────────────────────
def report():
    from pipeline import db
    import statistics
    c, dom_names, gwa_names, summary = _load()
    con = db.get_con(read_only=True)
    doms = con.execute("""SELECT label_kr, n_iwa, nearest_onet_domain, ROUND(nearest_cosine,3)
        FROM kr_domain_bottomup ORDER BY n_iwa DESC""").fetchall()
    top = con.execute("""SELECT g.label_kr, d.label_kr, g.n_iwa, g.nearest_onet_label, ROUND(g.nearest_cosine,3)
        FROM kr_gwa_bottomup g LEFT JOIN kr_domain_bottomup d ON g.domain_id=d.domain_id
        ORDER BY g.n_iwa DESC LIMIT 15""").fetchall()
    n_gwa = con.execute("SELECT COUNT(*) FROM kr_gwa_bottomup").fetchone()[0]
    matched = con.execute("SELECT COUNT(DISTINCT nearest_onet) FROM kr_gwa_bottomup").fetchone()[0]
    matched_s = con.execute("SELECT COUNT(DISTINCT nearest_onet) FROM kr_gwa_bottomup WHERE nearest_cosine>=0.55").fetchone()[0]
    coss = [r[0] for r in con.execute("SELECT nearest_cosine FROM kr_gwa_bottomup").fetchall()]
    sizes = [r[0] for r in con.execute("SELECT n_iwa FROM kr_gwa_bottomup").fetchall()]
    coh = [r[0] for r in con.execute("SELECT cohesion FROM kr_gwa_bottomup").fetchall()]
    uniq = con.execute("SELECT label_kr, nearest_onet_label, ROUND(nearest_cosine,3) "
                       "FROM kr_gwa_bottomup WHERE nearest_cosine<0.45 ORDER BY nearest_cosine LIMIT 8").fetchall()
    rev = _onet_reverse(con)
    con.close()
    missing = [r for r in rev if not r["emergent"]]
    from collections import Counter as _C
    miss_dom = _C(r["domain"] for r in missing)

    L = []; A = L.append
    A("# Stage 4b (순수 상향식 GWA 도출) — ONET-유사 형태 실험 결과")
    A("")
    A("> **연구진 보고용** · 자동생성: `pipeline/s4b_persist.py report`  ")
    A("> 별도 실험: 기존 Stage4(트랙1=ONET 41 채택)와 무관. 우리가 도출한 TASK→DWA→**IWA에서 출발해 ONET과 닮은 형태의 GWA가 자생하도록 기준을 설계·적용**한 상향식 결과.  ")
    A("> 산출 엑셀: `outputs/S4b_상향식GWA도출.xlsx`")
    A("")
    A("---")
    A("")
    A("## 1. 무엇을 했나 — 기준(criteria) 설계")
    A("")
    A("이전 1차 상향식(트랙2)은 16,168 TASK 트리를 자연절단해 **2개 거대군집**으로 무너졌다(average linkage 사슬효과·상위 거대가지 지배). 이를 극복하고 **ONET 41 GWA와 닮은 형태**(균형 잡힌 ~40 일반범주·4대 영역·명사형)가 나오도록 다음 기준을 세웠다:")
    A("")
    A("| # | 기준 | 근거 |")
    A("|---|---|---|")
    A("| 1 | **군집 단위 = IWA 대표벡터(178)** | GWA는 IWA 한 단계 위 → TASK 트리가 아니라 IWA 단위 군집(거대가지 지배 제거) |")
    A("| 2 | **Ward(분산최소) 연결** | average의 사슬효과(한 덩어리 흡수) 제거 → ONET처럼 균형 잡힌 범주 |")
    A("| 3 | **추상 입도 = ONET 비율 참조** | ONET IWA:GWA≈8:1. 본 산출은 ONET '개수' 정합(k=41) 채택 |")
    A("| 4 | **2계층 = 도메인 4 → GWA(nested)** | 같은 Ward 트리의 4-절단과 41-절단 → GWA ⊂ 정확히 1 영역(ONET 형태 재현) |")
    A("| 5 | **균형 모니터** | 과대군집 점검(ONET GWA는 비교적 균형) |")
    A("| 6 | **ONET 정합도 검증** | 각 KR-GWA↔최근접 ONET cosine·매칭 개수(구성타당도) |")
    A("")
    A("## 2. 결과 한눈에")
    A("")
    A(f"- **자생 영역(도메인)**: 4개 · **자생 KR-GWA**: **{n_gwa}개** (IWA 178 → strict 1:1 nesting)")
    A(f"- **균형**: 최대 군집 {max(sizes)} IWA({max(sizes)/178*100:.1f}%) · 최소 {min(sizes)} · 단일 {sum(1 for s in sizes if s==1)}개 · 응집도 중앙값 {statistics.median(coh):.3f}")
    A(f"  → 이전 트랙2(한 군집 50 IWA·자연절단 2개)와 달리 **ONET처럼 균형 잡힌 {n_gwa}범주** 도출")
    A(f"- **ONET 41 정합**: distinct **{matched}/41** 매칭(강매칭 cos≥0.55 **{matched_s}**) · 평균 최근접 cos {statistics.mean(coss):.3f}")
    A("")
    A("## 3. 자생한 4대 영역 — ONET과의 대비 (핵심 발견)")
    A("")
    A("| 자생 영역(상향식) | 소속 IWA | 최근접 ONET 영역 | cos |")
    A("|---|---|---|---|")
    for lbl, n, od, cos in doms:
        A(f"| {lbl} | {n} | {od} | {cos} |")
    A("")
    A("> **핵심**: 상향식으로 자생한 4대 영역은 O*NET의 **인지기능 축**(정보입력·정신과정·작업산출·타인상호작용)이 아니라 **직업유형 축**(생산·대인서비스·사무·운송)으로 갈렸다. 즉 KSCO 직업설명에서 데이터가 스스로 묶이는 1차 축은 \"무슨 일을 하는가(직능유형)\"이지 \"어떤 인지기능인가\"가 아니다. O*NET의 4대 영역은 데이터 자생이 아니라 **직무분석 이론(PAQ)이 부과한 설계 축**임을 재확인한다.")
    A("")
    A("## 4. 자생 KR-GWA — 규모 상위 15")
    A("")
    A("| KR-GWA(자생) | 소속영역 | IWA | 최근접 ONET-GWA | cos |")
    A("|---|---|---|---|---|")
    for lbl, dom, n, onl, cos in top:
        A(f"| {lbl} | {dom} | {n} | {onl} | {cos} |")
    A("")
    A("## 5. ONET과의 정합 — 양방향 가설 검증")
    A("")
    A("### 5-1. 우리 → ONET (자생 KR-GWA가 ONET 어디에 닿나)")
    A(f"- 자생 {n_gwa}개 KR-GWA가 가리키는 ONET GWA는 **{matched}/41 distinct**(강매칭 {matched_s}). 다수 KR-GWA가 같은 ONET을 가리켜(예: 생산계열 다수→'물체 취급 및 이동') distinct는 {matched}개로 수렴.")
    A("")
    A(f"### 5-2. ONET → 우리 (★ONET엔 있으나 우리 상향식엔 없는 GWA)")
    A(f"- ONET 41 중 **표출 {41-len(missing)}개 · 미표출 {len(missing)}개**. '미표출'=어떤 KR-GWA의 최근접으로도 지목되지 않은 것(우리 체계에 독립 범주로 자생하지 않음).")
    A(f"- **미표출 {len(missing)}개의 영역 분포**: " + " · ".join(f"{d} {c}" for d, c in miss_dom.most_common()))
    A("")
    A("| ONET 영역 | ONET GWA(우리엔 없음) | 가장 가깝게 흡수된 우리 KR-GWA | cos |")
    A("|---|---|---|---|")
    for r in sorted(missing, key=lambda x: (x["domain"], -x["nearest_cos"])):
        A(f"| {r['domain']} | {r['label_kr']} | {r['nearest_kr']} | {r['nearest_cos']} |")
    A("")
    A("- **해석(핵심)**: 미표출은 **정신 과정·타인과의 상호작용(추상 인지·관리·대인 활동)에 집중**된다 — 의사결정·전략수립·자문·설득·팀 구축·행정 등. 우리 상향식은 **물리적·생산적 활동은 잘게 쪼개 표출**하지만, ONET이 별도 GWA로 두는 추상 활동은 **'사업 기획 및 조직 운영 관리'·'조직·기관 지휘 및 총괄 관리' 같은 소수 범주로 뭉뚱그려 흡수**한다.")
    A("- 이는 **KSCO 직업설명이 인지·관리·대인 활동을 ONET만큼 세분해 기술하지 않는다**는 원천 데이터 특성의 반영이다(직무분석가가 분해한 ONET vs 분류 정의 중심의 KSCO). 곧, *형태(균형 41범주)는 닮게 만들 수 있으나, ONET의 추상활동 분해 깊이까지 데이터로 자생시키긴 어렵다*가 정직한 결론.")
    if uniq:
        A("")
        A("### 5-3. 한국 특이 후보(우리 KR-GWA 중 최근접 ONET cos<0.45)")
        A("")
        A("| KR-GWA(자생) | 최근접 ONET | cos |")
        A("|---|---|---|")
        for lbl, onl, cos in uniq:
            A(f"| {lbl} | {onl} | {cos} |")
    A("")
    A("## 6. 정직한 한계")
    A(f"- **단일 IWA 군집 {sum(1 for s in sizes if s==1)}개**: k=41 개수 정합을 위해 절단을 높이면 고유 IWA가 단독 GWA가 된다(입도 비용). ONET 비율 정합(k≈22)을 택하면 단일군집이 줄지만 ONET 개수와 멀어진다 — 형태(개수) vs 입도의 trade-off.")
    A("- **ONET 임베딩 기준의 cosine**: 최근접 ONET은 한국어 번역본 임베딩 기준이라 번역 어휘 영향을 받는다(참고치).")
    A("- 본 결과는 **방법 실험**이다. 정본 GWA 체계는 Stage4 트랙1(ONET 41 채택)이며, 본 4b는 \"상향식으로도 ONET형 범주가 자생하는가\"의 구성타당도 근거로 병기한다.")
    A("")
    RESULTS.mkdir(parents=True, exist_ok=True)
    path = RESULTS / "Stage4b_상향식GWA_결과해설서.md"
    path.write_text("\n".join(L), encoding="utf-8")
    print(f"[report] → {path}")
    return path


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    if cmd in ("persist", "all"):
        persist()
    if cmd in ("export", "all"):
        export()
    if cmd in ("report", "all"):
        report()
