"""KSCO 8차 권위 원천(HWPX) 직접 파서 — 위계 + 정의 + 주요업무 + 예시.

기존 DB(텍스트 깨짐·위계 명칭 누락)를 대체하기 위해, 통계청 공식 HWPX 2종을 직접 파싱한다.
  ① 분류 항목표 HWPX  → 권위 코드→명칭 (대>중>소>세>세세 전체)
  ② 해설서 HWPX        → 코드별 정의·▍주요 업무·▍직업 예시·▍제외

해설서 entry 구조(파악됨):
  "{코드}{직업명}"(붙어있는 헤더 문단) → 정의 문단 → ▍주요 업무(·불릿) → ▍직업 예시(·불릿) → ▍제 외
헤더는 항목표의 (코드,명칭)을 이어붙인 문자열과 정확히 일치할 때만 인정(예: "24911"+"119 구조대원").
"""
from __future__ import annotations

import re
import zipfile
from pathlib import Path

# ── 원천 경로 ────────────────────────────────────────────────────────
REF_DIR = (Path(__file__).resolve().parents[3] / "01_data_collection"
           / "00_external_references" / "직업정보 관련 참고자료_국내"
           / "한국표준직업분류_2024년 고시_8차")
ITEM_TABLE_HWPX = REF_DIR / "제8차+한국표준직업분류+개정+분류+항목표.hwpx"
HANDBOOK_HWPX = REF_DIR / "1. (해설서) 제8차 한국표준직업분류(2차 정오표 반영)_최종_20250722023539 (1).hwpx"

# 대분류(1자리) 권위 명칭 — KSCO 8차 10개 대군 (총설 기준 상수)
MAJOR_NAMES = {
    "1": "관리자",
    "2": "전문가 및 관련 종사자",
    "3": "사무 종사자",
    "4": "서비스 종사자",
    "5": "판매 종사자",
    "6": "농림·어업 숙련 종사자",
    "7": "기능원 및 관련 기능 종사자",
    "8": "장치·기계 조작 및 조립 종사자",
    "9": "단순노무 종사자",
    "A": "군인",
}

_CODE_RE = re.compile(r"^(?:\d{2,5}|A0\d{0,3}|A0)$")  # 11~99999, A0~A0900


# ── HWPX 저수준 추출 ─────────────────────────────────────────────────
def _clean(s: str) -> str:
    s = re.sub(r"<[^>]+>", "", s)
    return (s.replace("&amp;", "&").replace("&lt;", "<")
             .replace("&gt;", ">").replace("&quot;", '"').strip())


def _paras(xml: str) -> list[str]:
    """문단(<hp:p>)별 텍스트 리스트(빈 문단 제외)."""
    out = []
    for pm in re.finditer(r"<hp:p\b.*?</hp:p>", xml, re.S):
        txts = re.findall(r"<hp:t>(.*?)</hp:t>", pm.group(0), re.S)
        line = _clean("".join(txts))
        if line:
            out.append(line)
    return out


def _table_rows(xml: str) -> list[list[str]]:
    """모든 표의 행 → 셀텍스트 리스트."""
    rows = []
    for tr in re.finditer(r"<hp:tr\b.*?</hp:tr>", xml, re.S):
        cells = []
        for tc in re.finditer(r"<hp:tc\b.*?</hp:tc>", tr.group(0), re.S):
            txts = re.findall(r"<hp:t>(.*?)</hp:t>", tc.group(0), re.S)
            cells.append(_clean("".join(txts)))
        if cells:
            rows.append(cells)
    return rows


def _read_sections(path: Path) -> list[str]:
    z = zipfile.ZipFile(path)
    secs = sorted(n for n in z.namelist() if re.match(r"Contents/section\d+\.xml", n))
    return [z.read(s).decode("utf-8", "replace") for s in secs]


# ── ① 항목표 → 코드→명칭 ────────────────────────────────────────────
def load_hierarchy(path: Path = ITEM_TABLE_HWPX) -> dict[str, str]:
    """분류 항목표 → {코드: 명칭} (2~5자리 + A0…)."""
    code2name: dict[str, str] = {}
    for xml in _read_sections(path):
        for row in _table_rows(xml):
            if len(row) >= 2:
                code, name = row[0].strip(), row[1].strip()
                if _CODE_RE.match(code) and name:
                    code2name[code] = name
    return code2name


def level_of(code: str) -> int:
    """코드 길이 = 분류 수준(2=중,3=소,4=세,5=세세). A0110=5."""
    return len(code)


def lineage(code: str, code2name: dict[str, str]) -> dict:
    """세세분류(5자리) → 대>중>소>세>세세 코드·명칭."""
    major = code[0]
    return {
        "major_code": major, "major_name": MAJOR_NAMES.get(major, ""),
        "mid_code": code[:2], "mid_name": code2name.get(code[:2], ""),
        "minor_code": code[:3], "minor_name": code2name.get(code[:3], ""),
        "broad_code": code[:4], "broad_name": code2name.get(code[:4], ""),
        "unit_code": code, "unit_name": code2name.get(code, ""),
    }


# ── ② 해설서 → 코드별 정의·주요업무·예시·제외 ───────────────────────
_MARK = re.compile(r"^▍\s*(.+?)\s*$")


def _norm_header(s: str) -> str:
    """헤더 비교용 정규화: 공백 제거 + 가운뎃점 변형 통일.
    해설서 헤더는 '코드명칭'(붙임) 또는 '코드 명칭'(공백) 혼재 → 공백 무시.
    """
    s = re.sub(r"\s+", "", s)
    for ch in "‧∙•・·":
        s = s.replace(ch, "·")
    return s


def _ws(s: str) -> str:
    """다중 공백·개행 → 단일 공백 (justified 텍스트의 큰 간격 정규화)."""
    return " ".join(str(s).split())


def _marker_kind(line: str) -> str | None:
    """블록 마커 판정. ▍ 유무 무관(해설서엔 '▍직업 예시'·'직업 예시' 혼재)."""
    key = re.sub(r"\s+", "", line.lstrip("▍ ").strip())
    if key in ("주요업무", "수행직무"):
        return "tasks"
    if key in ("직업예시", "예시"):
        return "examples"
    if key in ("제외", "제외직업"):
        return "excl"
    if key == "자격요건":
        return "qual"
    if key in ("참고", "분류시유의사항"):
        return "other"
    return None


def parse_handbook(code2name: dict[str, str], path: Path = HANDBOOK_HWPX) -> dict[str, dict]:
    """해설서 → {코드: {정의, 주요업무[], 예시[], 제외[]}}.

    헤더 = '코드'+'명칭' 정확 일치 문단에서 노드 시작, 다음 헤더 전까지 수집.
    """
    # 헤더(정규화) → 코드. 공백/가운뎃점 변형 무시.
    header2code = {_norm_header(f"{c}{n}"): c for c, n in code2name.items()}
    nodes: dict[str, dict] = {}

    all_paras: list[str] = []
    for xml in _read_sections(path):
        all_paras.extend(_paras(xml))

    cur = None          # 현재 코드
    section = "def"     # def | tasks | examples | excl | qual | other
    for line in all_paras:
        code = header2code.get(_norm_header(line))
        if code is not None:
            cur = code
            nodes[cur] = {"정의": [], "주요업무": [], "예시": [], "제외": []}
            section = "def"
            continue
        if cur is None:
            continue
        kind = _marker_kind(line)
        if kind:
            section = {"tasks": "tasks", "examples": "examples",
                       "excl": "excl", "qual": "other", "other": "other"}[kind]
            continue
        # 구성 안내문(비-리프 노드) → 정의에서 제외
        if re.match(r"^이 (대분류|중분류|소분류|세분류)의 직업은 다음의", line):
            section = "other"
            continue
        node = nodes[cur]
        if section == "def":
            node["정의"].append(line)
        elif section == "tasks":
            node["주요업무"].append(line)
        elif section == "examples":
            node["예시"].append(line)
        elif section == "excl":
            node["제외"].append(line)
        # other(자격요건·참고·구성 등)는 버림

    # 리스트 정리: 정의는 join+공백정규화, 불릿은 재구성+중복제거
    for c, nd in nodes.items():
        nd["정의"] = _ws(" ".join(nd["정의"]))
        nd["주요업무"] = _dedup(_bullets_from_lines(nd["주요업무"]))
        nd["예시"] = _dedup(_bullets_from_lines(nd["예시"]))
        nd["제외"] = _dedup(_bullets_from_lines(nd["제외"]))
    return nodes


# '·'를 불릿 구분자로 인식: 줄 시작 또는 공백 뒤의 '·'에서만 분할.
# 단어 사이 병렬점(예: '심의·의결', '감사·조사')은 분할하지 않음.
_BULLET_SPLIT = re.compile(r"(?:^|(?<=\s))·\s*")


def _bullets_from_lines(lines: list[str]) -> list[str]:
    """문단 리스트 → 불릿 항목. 줄바꿈으로 이어진 불릿은 이전 항목에 연결."""
    items: list[str] = []
    for ln in lines:
        starts_bullet = bool(re.match(r"^\s*·", ln))
        segs = [_ws(s) for s in _BULLET_SPLIT.split(ln)]
        for j, seg in enumerate(segs):
            if not seg:
                continue
            if j == 0 and not starts_bullet and items:
                items[-1] = _ws(items[-1] + " " + seg)   # 이전 불릿의 연속(줄바꿈)
            else:
                items.append(seg)
    return items


def _dedup(items: list[str]) -> list[str]:
    seen, out = set(), []
    for it in items:
        if it not in seen:
            seen.add(it)
            out.append(it)
    return out


def _norm_name(s: str) -> str:
    return re.sub(r"[\s·‧∙•・]", "", s)


def parse_major_definitions(path: Path = HANDBOOK_HWPX) -> dict[str, str]:
    """대분류(1자리) 정의 — 해설서 요약 트리플('대분류 N'+명칭+정의)에서 추출."""
    paras: list[str] = []
    for xml in _read_sections(path):
        paras.extend(_paras(xml))
    out: dict[str, str] = {}
    for i, line in enumerate(paras):
        m = re.fullmatch(r"대분류 ?([1-9A])", line)
        if not m or i + 2 >= len(paras):
            continue
        code = m.group(1)
        if code in out:
            continue
        name, deff = paras[i + 1].strip(), paras[i + 2].strip()
        if (_norm_name(name) == _norm_name(MAJOR_NAMES.get(code, "·"))
                and not deff.startswith(("◦", "이 대분류", "("))
                and len(deff) > 20):
            out[code] = deff
    return out


# ── 결합: 전체 노드(1~5수준) ────────────────────────────────────────
def build_nodes() -> tuple[dict[str, str], dict[str, dict]]:
    """모든 분류 노드(중·소·세·세세) → 코드·수준·명칭·부모·정의·주요업무·예시·제외.

    Returns: (code2name, {code: node_dict})
    """
    code2name = load_hierarchy()
    parsed = parse_handbook(code2name)
    major_defs = parse_major_definitions()
    out: dict[str, dict] = {}
    # 대분류(L1) 노드 — 명칭(상수) + 정의(해설서)
    for mcode, mname in MAJOR_NAMES.items():
        out[mcode] = {
            "code": mcode, "level": 1, "name": mname, "parent_code": "",
            "major_code": mcode, "major_name": mname,
            "definition": major_defs.get(mcode, ""),
            "main_tasks": [], "examples": [], "exclusions": [],
        }
    for code, name in code2name.items():
        nd = parsed.get(code, {})
        out[code] = {
            "code": code, "level": level_of(code), "name": name,
            "parent_code": code[:-1],   # A0110→A011, 28120→2812, 11→1
            "major_code": code[0], "major_name": MAJOR_NAMES.get(code[0], ""),
            "definition": nd.get("정의", ""),
            "main_tasks": nd.get("주요업무", []),
            "examples": nd.get("예시", []),
            "exclusions": nd.get("제외", []),
        }
    return code2name, out


# ── 결합: 세세분류 1,270 레코드 ──────────────────────────────────────
def build_records() -> list[dict]:
    code2name = load_hierarchy()
    nodes = parse_handbook(code2name)
    recs = []
    for code in sorted(c for c in code2name if level_of(c) == 5):
        lin = lineage(code, code2name)
        own = nodes.get(code, {})
        parent = nodes.get(code[:4], {})
        # 주요업무 상속: 자기 것 우선, 없으면 부모 세분류
        main_tasks = own.get("주요업무") or parent.get("주요업무") or []
        tasks_src = "self" if own.get("주요업무") else ("parent" if parent.get("주요업무") else "none")
        recs.append({
            **lin,
            "definition": own.get("정의", ""),
            "parent_definition": parent.get("정의", ""),
            "main_tasks": main_tasks,
            "main_tasks_source": tasks_src,
            "examples": own.get("예시", []),
            "exclusions": own.get("제외", []),
        })
    return recs


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    c2n = load_hierarchy()
    bylv = {}
    for c in c2n:
        bylv[level_of(c)] = bylv.get(level_of(c), 0) + 1
    print("항목표 코드 수준별:", dict(sorted(bylv.items())))
    nodes = parse_handbook(c2n)
    leaves = [c for c in c2n if level_of(c) == 5]
    matched = [c for c in leaves if c in nodes]
    print(f"세세분류: {len(leaves)} / 해설서 헤더매칭: {len(matched)}")
    recs = build_records()
    with_def = sum(1 for r in recs if r["definition"])
    with_tasks = sum(1 for r in recs if r["main_tasks"])
    self_t = sum(1 for r in recs if r["main_tasks_source"] == "self")
    par_t = sum(1 for r in recs if r["main_tasks_source"] == "parent")
    print(f"정의 보유: {with_def}/{len(recs)} · 주요업무 보유: {with_tasks} (self {self_t}/parent {par_t})")
    # 샘플
    for code in ["28120", "28151", "27111", "24911", "89905"]:
        r = next((x for x in recs if x["unit_code"] == code), None)
        if r:
            print(f"\n[{code}] {r['major_name']}>{r['mid_name']}>{r['minor_name']}>{r['broad_name']}>{r['unit_name']}")
            print(f"   정의: {r['definition'][:70]}")
            print(f"   주요업무({r['main_tasks_source']},{len(r['main_tasks'])}): {r['main_tasks'][:2]}")
            print(f"   예시: {r['examples'][:3]}")
