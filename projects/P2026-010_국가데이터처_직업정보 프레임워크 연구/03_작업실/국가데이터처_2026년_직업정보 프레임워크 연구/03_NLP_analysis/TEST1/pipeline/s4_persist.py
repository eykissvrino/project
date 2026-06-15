"""Stage 4 — 적재: GWA 도출 결과 → gwa / iwa_to_gwa / gwa_bottomup DB(트랜잭션·멱등).

설계 §③·④·⑦. 입력(cache):
    s4_translation.json        ONET 41 GWA 한국어(label_kr·definition_kr·domain) — 트랙1 GWA 어휘
    s4_iwa_to_gwa.json         IWA→GWA 임베딩 prior 매핑(폴백)
    s4_iwa_gwa_cos.json        IWA→{gwa_id: cosine}(전 41, 정확한 cosine 기록용)
    s4_map_result.json         Opus zero-shot 전수 분류(정본) → method='llm'
    s4_bottomup.json           트랙2 한국형 GWA 군집(nearest_onet·cosine)
    s4_bottomup_result.json    (선택) 트랙2 GWA Opus 명명(label_kr)

매핑 정본 = Opus 분류(s4_map_result). 없는 IWA만 임베딩 prior 폴백.
검증: gwa_rules.check_gwa(명사형) — 게이트 아닌 보고지표. nesting: 모든 IWA→정확히 1 GWA.
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

from pipeline import gwa_rules

TEST1_DIR = Path(__file__).resolve().parents[1]
CACHE = TEST1_DIR / "cache"
TRANSLATION = CACHE / "s4_translation.json"
MAP_JSON = CACHE / "s4_iwa_to_gwa.json"
COS_LOOKUP = CACHE / "s4_iwa_gwa_cos.json"
MAP_RES = CACHE / "s4_map_result.json"
BOTTOMUP = CACHE / "s4_bottomup.json"
BU_RESULT = CACHE / "s4_bottomup_result.json"

KR_UNIQUE_COS = 0.55


def run(force: bool = False) -> dict:
    from pipeline import db
    if not TRANSLATION.exists():
        raise SystemExit(f"번역결과 없음: {TRANSLATION}")
    if not MAP_JSON.exists():
        raise SystemExit(f"매핑결과 없음: {MAP_JSON} — s4_cluster map 먼저")

    translation = json.loads(TRANSLATION.read_text(encoding="utf-8"))
    mapping = json.loads(MAP_JSON.read_text(encoding="utf-8"))
    cos_lookup = json.loads(COS_LOOKUP.read_text(encoding="utf-8")) \
        if COS_LOOKUP.exists() else {}
    valid_gids = {t["onet_gwa_id"] for t in translation}

    # Opus 전수 분류(정본) 적용 — cosine 은 룩업으로 정확히 재기록
    n_llm = 0
    if MAP_RES.exists():
        for r in json.loads(MAP_RES.read_text(encoding="utf-8")):
            iid = r.get("iwa_id"); gid = r.get("gwa_id")
            if iid in mapping and gid in valid_gids:
                mapping[iid]["gwa_id"] = gid
                mapping[iid]["method"] = "llm"
                mapping[iid]["llm_kr_unique"] = bool(r.get("is_kr_unique", False))
                if iid in cos_lookup and gid in cos_lookup[iid]:
                    mapping[iid]["cosine"] = cos_lookup[iid][gid]
                n_llm += 1
    else:
        print("[persist][warn] s4_map_result.json 없음 — 임베딩 prior로 적재(품질 낮음)")

    # GWA 명사형 검증(보고)
    g_labels = [t["label_kr"] for t in translation]
    gbatch = gwa_rules.check_batch_gwa(g_labels)
    print(f"[validate] GWA {len(translation)} · 명사형 준수율 {gbatch['pass_rate']:.2%} "
          f"({'PASS' if gbatch['gate_passed'] else 'CHECK'})")

    con = db.get_con()
    con.execute("BEGIN")
    try:
        if force:
            con.execute("DELETE FROM iwa_to_gwa")
            con.execute("DELETE FROM gwa")
            con.execute("DELETE FROM gwa_bottomup")

        # 1) gwa (트랙1: ONET 41 채택). gwa_id = onet_gwa_id.
        n_gwa = 0
        for t in translation:
            gid = t["onet_gwa_id"]
            con.execute("DELETE FROM gwa WHERE gwa_id=?", [gid])
            con.execute(
                """INSERT INTO gwa
                   (gwa_id, label_kr, onet_gwa_id, onet_label_en, domain,
                    is_kr_unique, source) VALUES (?,?,?,?,?,?,?)""",
                [gid, gwa_rules.normalize_label(t["label_kr"]), gid,
                 t.get("onet_label_en", ""), t.get("domain", ""),
                 False, "ONET_adopt"])
            n_gwa += 1

        # 2) iwa_to_gwa (strict 1:1)
        con.execute("DELETE FROM iwa_to_gwa")
        n_map, bad = 0, 0
        for iwa_id, m in mapping.items():
            gid = m["gwa_id"]
            if gid not in valid_gids:
                bad += 1
                continue
            con.execute(
                "INSERT INTO iwa_to_gwa (iwa_id, gwa_id, cosine, method) VALUES (?,?,?,?)",
                [iwa_id, gid, float(m.get("cosine", 0.0)), m.get("method", "mapped")])
            n_map += 1

        # 3) gwa_bottomup (트랙2 탐색)
        n_bu = 0
        if BOTTOMUP.exists():
            bu = json.loads(BOTTOMUP.read_text(encoding="utf-8"))
            names = {}
            if BU_RESULT.exists():
                for r in json.loads(BU_RESULT.read_text(encoding="utf-8")):
                    if r.get("kr_gwa_id"):
                        names[r["kr_gwa_id"]] = r.get("label_kr", "")
            con.execute("DELETE FROM gwa_bottomup")
            for c in bu:
                kid = c["kr_gwa_id"]
                label = gwa_rules.normalize_label(
                    names.get(kid) or c.get("nearest_onet_label", kid))
                con.execute(
                    """INSERT INTO gwa_bottomup
                       (kr_gwa_id, label_kr, n_iwa, nearest_onet, cosine)
                       VALUES (?,?,?,?,?)""",
                    [kid, label, int(c["n_iwa"]), c["nearest_onet"],
                     float(c["nearest_cosine"])])
                n_bu += 1
        con.execute("COMMIT")
    except Exception:
        con.execute("ROLLBACK")
        raise

    # 무결성 검증
    n_iwa = con.execute("SELECT COUNT(*) FROM iwa").fetchone()[0]
    dup = con.execute("SELECT COUNT(*) FROM (SELECT iwa_id FROM iwa_to_gwa "
                      "GROUP BY iwa_id HAVING COUNT(*)>1)").fetchone()[0]
    orphan = con.execute("SELECT COUNT(*) FROM iwa i LEFT JOIN iwa_to_gwa m "
                         "ON i.iwa_id=m.iwa_id WHERE m.gwa_id IS NULL").fetchone()[0]
    used = con.execute("SELECT COUNT(DISTINCT gwa_id) FROM iwa_to_gwa").fetchone()[0]
    n_weak = sum(1 for m in mapping.values() if m.get("weak"))
    con.close()

    print(f"[persist] gwa {n_gwa}(ONET채택) · iwa_to_gwa {n_map}/{n_iwa} "
          f"(애매→LLM {n_llm}, 무효gwa {bad}) · gwa_bottomup {n_bu}")
    print(f"[nesting] 중복배정 IWA {dup}(0=strict) · 고아 IWA {orphan} · "
          f"사용 GWA {used}/{n_gwa} · weak매핑(<{KR_UNIQUE_COS}) {n_weak}")
    return {"gwa": n_gwa, "iwa_to_gwa": n_map, "gwa_bottomup": n_bu,
            "dup_iwa": dup, "orphan_iwa": orphan, "used_gwa": used,
            "llm_resolved": n_llm, "weak": n_weak,
            "noun_pass_rate": gbatch["pass_rate"]}


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", nargs="?", default="run", choices=["run"])
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    run(force=a.force)
