"""Stage 4c — 연역적 한국형 GWA 적재 + Excel + 결과해설서.

입력 cache: s4c_gwa_design.json(설계) · s4c_map_res*.json(Opus 매핑) · s4c_cos.json ·
            s4c_kr_emb.npy/s4c_kr_order.json · s4_gwa_emb.npy(ONET 비교) · s4_translation.json
DB(CREATE IF NOT EXISTS): kr_gwa_deductive, iwa_to_kr_gwa_deductive (기존 미훼손)
산출: outputs/S4c_연역적GWA도출.xlsx · results/Stage4c_연역적GWA_결과해설서.md
PYTHONUTF8=1 권장.
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
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

DESIGN = CACHE / "s4c_gwa_design.json"
COS_LOOKUP = CACHE / "s4c_cos.json"
KR_EMB = CACHE / "s4c_kr_emb.npy"
KR_ORDER = CACHE / "s4c_kr_order.json"
MAP_JSON = CACHE / "s4c_iwa_to_kr.json"
GWA_EMB = CACHE / "s4_gwa_emb.npy"
GWA_ORDER = CACHE / "s4_gwa_order.json"
TRANSLATION = CACHE / "s4_translation.json"

SCHEMA = """
CREATE TABLE IF NOT EXISTS kr_gwa_deductive (
    gwa_id VARCHAR PRIMARY KEY, label_kr VARCHAR, definition VARCHAR,
    domain_id VARCHAR, domain_label VARCHAR, basis VARCHAR, rationale VARCHAR,
    n_iwa INTEGER, nearest_onet VARCHAR, nearest_onet_label VARCHAR, nearest_cosine DOUBLE);
CREATE TABLE IF NOT EXISTS iwa_to_kr_gwa_deductive (
    iwa_id VARCHAR PRIMARY KEY, gwa_id VARCHAR, cosine DOUBLE);
"""


def _merge_map(valid_ids: set) -> dict:
    """s4c_map_res*.json 병합 → {iwa_id: gwa_id}. 없으면 임베딩 prior 폴백."""
    out = {}
    files = sorted(CACHE.glob("s4c_map_res*.json"))
    for p in files:
        try:
            for r in json.loads(p.read_text(encoding="utf-8")):
                iid, gid = r.get("iwa_id"), r.get("gwa_id")
                if iid and gid in valid_ids and iid not in out:
                    out[iid] = gid
        except Exception:
            print(f"[warn] 파싱 실패 skip: {p.name}")
    return out


def persist():
    from pipeline import db, gwa_rules
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    gwa = design["gwa"]
    domains = {d["domain_id"]: d.get("label_kr", d.get("label", d["domain_id"]))
               for d in design["domains"]}
    valid_ids = {g["gwa_id"] for g in gwa}
    cos = json.loads(COS_LOOKUP.read_text(encoding="utf-8")) if COS_LOOKUP.exists() else {}

    mapres = _merge_map(valid_ids)
    prior = json.loads(MAP_JSON.read_text(encoding="utf-8")) if MAP_JSON.exists() else {}
    final = {}
    n_llm = 0
    for iid in prior:
        if iid in mapres:
            final[iid] = mapres[iid]; n_llm += 1
        else:
            final[iid] = prior[iid]["gwa_id"]
    if not mapres:
        print("[persist][warn] s4c_map_res*.json 없음 — 임베딩 prior 폴백 적재")

    # 각 KR-GWA 최근접 ONET(구성타당도)
    kr_emb = np.load(KR_EMB); kr_order = json.loads(KR_ORDER.read_text(encoding="utf-8"))
    gwa_emb = np.load(GWA_EMB); on_order = json.loads(GWA_ORDER.read_text(encoding="utf-8"))
    trans = {t["onet_gwa_id"]: t for t in json.loads(TRANSLATION.read_text(encoding="utf-8"))}
    krrow = {g: i for i, g in enumerate(kr_order)}
    near = {}
    sim = kr_emb @ gwa_emb.T
    for g in gwa:
        j = int(np.argmax(sim[krrow[g["gwa_id"]]]))
        near[g["gwa_id"]] = (on_order[j], trans[on_order[j]]["label_kr"],
                             round(float(sim[krrow[g["gwa_id"]]][j]), 4))

    cnt = Counter(final.values())
    con = db.get_con()
    con.execute("BEGIN")
    try:
        for s in SCHEMA.strip().split(";"):
            if s.strip():
                con.execute(s)
        con.execute("DELETE FROM kr_gwa_deductive")
        con.execute("DELETE FROM iwa_to_kr_gwa_deductive")
        for g in gwa:
            gid = g["gwa_id"]; on = near[gid]
            con.execute("INSERT INTO kr_gwa_deductive VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                        [gid, gwa_rules.normalize_label(g["label_kr"]),
                         g.get("definition_kr", ""), g["domain_id"],
                         domains.get(g["domain_id"], g["domain_id"]),
                         g.get("basis", ""), g.get("rationale", ""),
                         int(cnt.get(gid, 0)), on[0], on[1], on[2]])
        for iid, gid in final.items():
            c = cos.get(iid, {}).get(gid, 0.0)
            con.execute("INSERT INTO iwa_to_kr_gwa_deductive VALUES (?,?,?)",
                        [iid, gid, float(c)])
        con.execute("COMMIT")
    except Exception:
        con.execute("ROLLBACK"); raise
    ng = con.execute("SELECT COUNT(*) FROM kr_gwa_deductive").fetchone()[0]
    nm = con.execute("SELECT COUNT(*) FROM iwa_to_kr_gwa_deductive").fetchone()[0]
    dup = con.execute("SELECT COUNT(*) FROM (SELECT iwa_id FROM iwa_to_kr_gwa_deductive "
                      "GROUP BY iwa_id HAVING COUNT(*)<>1)").fetchone()[0]
    empty = con.execute("SELECT COUNT(*) FROM kr_gwa_deductive WHERE n_iwa=0").fetchone()[0]
    con.close()
    basis = Counter(g.get("basis", "") for g in gwa)
    print(f"[persist] kr_gwa_deductive {ng} · iwa_to_kr {nm} · 중복 {dup} · "
          f"빈GWA(이론만) {empty} · LLM매핑 {n_llm}")
    print(f"  basis 분포: {dict(basis)}")
    return {"gwa": ng, "map": nm, "dup": dup, "empty": empty}


# ── Excel ────────────────────────────────────────────────────────────
_MAX_W = 64


def _xlsx(path, sheets):
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


def _criteria_sheet():
    rows = [
        ("이론 베이스", "Worker-oriented Job Analysis (PAQ, McCormick 1972)", "직업을 산업·직무가 아닌 작업자의 일반 행동요소로 기술. 모든 GWA는 여러 직업에 공통 적용되는 일반 행동단위."),
        ("이론 베이스", "정보처리 모델 (Information-Processing)", "일을 입력→처리→산출→상호작용으로 봄. 4대 영역을 이론 천장으로 고정(국제 비교가능성)."),
        ("이론 베이스", "분류학 원칙 (Fleishman & Quaintance 1984)", "상호배타성·포괄성·추상수준 동질성."),
        ("이론 베이스", "O*NET GWA Writing 형식", "명사형 일반범주명, 한 GWA=한 일반활동유형."),
        ("설계 기준", "C1 영역별 활동공간 이론규정", "각 영역이 이론상 어떤 활동유형으로 구성되는지 먼저 규정."),
        ("설계 기준", "C2 데이터 근거(grounded)", "178 IWA를 근거로 공통 일반활동을 GWA 후보로 묶음(개별 IWA 복사 금지)."),
        ("설계 기준", "C3 이론 보강(★)", "이론상 필요하나 데이터에 얇은 활동(의사결정·전략수립 등)도 범주로 포함, basis=theory 표시."),
        ("설계 기준", "C4 MECE·추상수준 정제", "중복 통합·과구체 병합·과광범 분할로 일반성 수준 통일."),
        ("설계 기준", "C5 입도", "총 약 30~45개(ONET 41 비교가능 입도), 개수 강제 안 함."),
        ("설계 기준", "C6 한국 맥락", "KSCO 두꺼운 영역은 더 세분, 희박하면 통합. ONET은 기준선."),
        ("basis 태그", "data / theory / mixed", "data=KSCO 데이터에 두텁게 근거 / theory=이론보강(데이터 얇음→측정 필요) / mixed=혼합."),
    ]
    return pd.DataFrame(rows, columns=["구분", "항목", "내용"])


def export():
    from pipeline import db
    con = db.get_con(read_only=True)
    df_dom = con.execute("""
        SELECT domain_label "영역", COUNT(*) "GWA수", SUM(n_iwa) "소속IWA합"
        FROM kr_gwa_deductive GROUP BY domain_id, domain_label
        ORDER BY SUM(n_iwa) DESC""").df()
    df_gwa = con.execute("""
        SELECT gwa_id "코드", domain_label "영역", label_kr "한국형GWA",
               basis "근거(data/theory)", n_iwa "소속IWA수",
               nearest_onet_label "최근접ONET", ROUND(nearest_cosine,3) "ONETcos",
               definition "정의", rationale "설계근거"
        FROM kr_gwa_deductive ORDER BY domain_id, n_iwa DESC""").df()
    df_mem = con.execute("""
        SELECT m.gwa_id "코드", g.label_kr "한국형GWA", i.label "IWA정식명",
               i.n_dwa "IWA소속DWA", i.n_jobs "IWA소속직업", ROUND(m.cosine,3) cos
        FROM iwa_to_kr_gwa_deductive m JOIN kr_gwa_deductive g ON m.gwa_id=g.gwa_id
        JOIN iwa i ON m.iwa_id=i.iwa_id ORDER BY m.gwa_id, i.n_dwa DESC""").df()
    df_empty = con.execute("""
        SELECT gwa_id "코드", domain_label "영역", label_kr "한국형GWA(데이터 미표출)",
               basis 근거, nearest_onet_label "최근접ONET", definition 정의
        FROM kr_gwa_deductive WHERE n_iwa=0 ORDER BY domain_id""").df()
    ng = int(con.execute("SELECT COUNT(*) FROM kr_gwa_deductive").fetchone()[0])
    nm = int(con.execute("SELECT COUNT(*) FROM iwa_to_kr_gwa_deductive").fetchone()[0])
    empty = int(con.execute("SELECT COUNT(*) FROM kr_gwa_deductive WHERE n_iwa=0").fetchone()[0])
    basis = dict(con.execute("SELECT basis,COUNT(*) FROM kr_gwa_deductive GROUP BY basis").fetchall())
    matched = int(con.execute("SELECT COUNT(DISTINCT nearest_onet) FROM kr_gwa_deductive").fetchone()[0])
    con.close()
    cov = pd.DataFrame([
        {"지표": "한국형 GWA 수", "값": ng},
        {"지표": "영역", "값": "4 (정보입력·정신과정·작업산출·타인상호작용)"},
        {"지표": "IWA→GWA 매핑", "값": f"{nm} (strict 1:1)"},
        {"지표": "basis 분포", "값": str(basis)},
        {"지표": "빈 GWA(데이터 미표출=측정 필요)", "값": empty},
        {"지표": "ONET 41 최근접 distinct", "값": f"{matched}/41"},
        {"지표": "방법", "값": "ONET 방법 복제(이론 우선·데이터 근거·연역 설계). ONET 41 목록 미사용."},
    ])
    path = OUTPUTS / "S4c_연역적GWA도출.xlsx"
    sheets = {"데이터사전·설계기준": _criteria_sheet(), "영역요약": df_dom,
              "한국형GWA": df_gwa, "GWA별IWA": df_mem}
    if len(df_empty):
        sheets["★이론보강GWA(데이터미표출)"] = df_empty
    sheets["커버리지"] = cov
    _xlsx(path, sheets)
    return path


def report():
    from pipeline import db
    import statistics as st
    con = db.get_con(read_only=True)
    ng = con.execute("SELECT COUNT(*) FROM kr_gwa_deductive").fetchone()[0]
    nm = con.execute("SELECT COUNT(*) FROM iwa_to_kr_gwa_deductive").fetchone()[0]
    dup = con.execute("SELECT COUNT(*) FROM (SELECT iwa_id FROM iwa_to_kr_gwa_deductive GROUP BY iwa_id HAVING COUNT(*)<>1)").fetchone()[0]
    empty = con.execute("SELECT COUNT(*) FROM kr_gwa_deductive WHERE n_iwa=0").fetchone()[0]
    basis = dict(con.execute("SELECT basis,COUNT(*) FROM kr_gwa_deductive GROUP BY basis").fetchall())
    matched = con.execute("SELECT COUNT(DISTINCT nearest_onet) FROM kr_gwa_deductive").fetchone()[0]
    doms = con.execute("""SELECT domain_label, COUNT(*), SUM(n_iwa)
        FROM kr_gwa_deductive GROUP BY domain_id, domain_label ORDER BY SUM(n_iwa) DESC""").fetchall()
    bydom = {}
    for did, dl in con.execute("SELECT DISTINCT domain_id, domain_label FROM kr_gwa_deductive").fetchall():
        bydom[dl] = con.execute("""SELECT label_kr, basis, n_iwa, nearest_onet_label, ROUND(nearest_cosine,2)
            FROM kr_gwa_deductive WHERE domain_id=? ORDER BY n_iwa DESC""", [did]).fetchall()
    emptyrows = con.execute("""SELECT domain_label, label_kr, basis, nearest_onet_label
        FROM kr_gwa_deductive WHERE n_iwa=0 ORDER BY domain_id""").fetchall()
    con.close()

    L = []; A = L.append
    A("# Stage 4c (연역적 한국형 GWA) — ONET 방법 복제, ONET 41 미사용")
    A("")
    A("> **연구진 보고용** · 자동생성: `pipeline/s4c_persist.py report`  ")
    A("> 별도 산출: Stage4 트랙1(ONET 채택)·4b(순수 상향식)와 무관. **O*NET이 GWA를 만든 *방법*을 그대로 복제**하되, **O*NET의 41개 목록은 쓰지 않고** 우리 TASK→DWA→IWA 데이터+이론으로 한국형 GWA를 연역 설계.  ")
    A("> 산출 엑셀: `outputs/S4c_연역적GWA도출.xlsx`")
    A("")
    A("---")
    A("")
    A("## 1. 방법 — ONET을 베끼지 않고 ONET처럼 만들기")
    A("")
    A("O*NET GWA의 3개 층을 분리하면: **(a) 조직 프레임**(정보처리 4영역) · **(b) 방법**(이론 우선→데이터 검증) · **(c) 41개 목록**. 본 단계는 **(a)+(b)를 채택하고 (c)는 자체 생산**한다.")
    A("")
    A("| 층 | O*NET | Stage 4(트랙1) | Stage 4b | **Stage 4c(본 단계)** |")
    A("|---|---|---|---|---|")
    A("| 프레임 | 정보처리 4영역 | (ONET 그대로) | 데이터 자생(직종축) | **정보처리 4영역 채택(이론)** |")
    A("| 방법 | 연역+검증 | 채택·매핑 | 순수 상향식 | **연역 설계+데이터 검증** |")
    A("| 내용 | ONET 41 | ONET 41 수입 | 데이터 군집 | **자체 설계(데이터+이론)** |")
    A("")
    A("**Opus(I/O 전문가 패널 대리)의 설계 기준**(프롬프트 `gwa_deductive_design_system.md`에 명문화): "
      "①영역별 활동공간 이론규정 → ②178 IWA 근거 대조(grounded) → ③**이론 보강**(데이터에 얇아도 이론상 필요한 활동은 범주로 포함, `basis=theory`) → ④MECE·추상수준 정제 → ⑤입도 30~45 → ⑥한국 맥락. 이론 베이스=PAQ(worker-oriented)·정보처리 모델·Fleishman 분류학 원칙·ONET 작성형식.")
    A("")
    A("## 2. 결과 한눈에")
    A("")
    A(f"- **한국형 GWA**: **{ng}개** (4영역) · IWA 178 → **strict 1:1 매핑 {nm}**(중복 {dup})")
    A(f"- **basis 분포**: {basis}  ← `theory`/`mixed`는 데이터 추출만으론 안 잡혀 **Stage5 측정으로 채울 범주**")
    A(f"- **데이터 미표출(빈) GWA**: {empty}개 — 이론상 두었으나 KSCO 추출 근거가 없는 범주(아래 4장)")
    A(f"- **ONET 41 최근접 distinct**: {matched}/41 (구성타당도 참고)")
    A("")
    A("## 3. 한국형 GWA 체계 (영역별)")
    A("")
    for dl, ngd, nid in doms:
        A(f"### {dl} — GWA {ngd}개 · 소속 IWA {int(nid) if nid else 0}")
        A("")
        A("| 한국형 GWA | basis | IWA | 최근접 ONET | cos |")
        A("|---|---|---|---|---|")
        for lbl, bs, n, onl, cos in bydom.get(dl, []):
            A(f"| {lbl} | {bs} | {n} | {onl} | {cos} |")
        A("")
    A("## 4. 이론 보강 GWA — 데이터엔 얇지만 체계엔 필요 (★측정 대상)")
    A("")
    if emptyrows:
        A("추출(텍스트)만으론 독립 범주로 안 잡혔으나 worker-oriented 체계 완결성을 위해 둔 범주. **Stage5 직업별 측정(Importance/Level)으로 채워야 완성**된다 — ONET이 평정으로 추상활동을 채운 것과 같은 자리.")
        A("")
        A("| 영역 | 한국형 GWA | basis | 최근접 ONET |")
        A("|---|---|---|---|")
        for dl, lbl, bs, onl in emptyrows:
            A(f"| {dl} | {lbl} | {bs} | {onl} |")
    else:
        A("빈 GWA 없음 — 설계된 모든 범주가 데이터로 1건 이상 채워짐.")
    A("")
    A("## 5. 의의·한계")
    A("- **의의**: ONET 41을 수입하지 않고도 **ONET과 동형의 형태**(정보처리 4영역 × 일반 작업활동 범주)를 **한국 데이터·이론으로 자체 구성**. (a)프레임·(b)방법은 국제 정합, (c)내용은 한국 고유.")
    A("- **한계**: `theory`/`mixed` 범주(추상 인지·관리·대인 활동)는 KSCO 직업설명에 명시되지 않아 데이터 근거가 얇다. ONET도 이를 *추출이 아니라 평정*으로 채웠다 → **본 연역 골격 + Stage5 직업별 측정이 한 세트**여야 ONET 수준 완성.")
    A("- 최근접 ONET cosine은 한국어 번역본 임베딩 기준 참고치(구성타당도 방향성).")
    A("")
    RESULTS.mkdir(parents=True, exist_ok=True)
    p = RESULTS / "Stage4c_연역적GWA_결과해설서.md"
    p.write_text("\n".join(L), encoding="utf-8")
    print(f"[report] → {p}")
    return p


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    if cmd in ("persist", "all"):
        persist()
    if cmd in ("export", "all"):
        export()
    if cmd in ("report", "all"):
        report()
