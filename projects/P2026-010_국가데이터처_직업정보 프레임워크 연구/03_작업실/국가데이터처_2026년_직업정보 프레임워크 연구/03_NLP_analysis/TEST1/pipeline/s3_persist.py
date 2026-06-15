"""Stage 3 — 적재: IWA 명명결과 → 7조항(+R4경고) 검증 → iwa / dwa_to_iwa DB(트랜잭션·멱등).

설계 §④-5·6, ⑦. 입력:
    cache/s3_clusters.json     (IWA 메타: n_dwa·n_task·n_jobs·mean_cosine)
    cache/s3_dwa_to_iwa.json   (dwa_id → iwa_id, strict 1:1)
    cache/s3_results/b*.json   (Opus 명명: [{iwa_id,label,definition}])

검증: iwa_rules.check_iwa() — R4(광의 일반어)는 경고로 완화, 나머지 7조항 게이트.
재개: 결과 없는 IWA는 skip(부분 적재 가능 — 첫 배치 검수용). PYTHONUTF8=1 권장.
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

from pipeline import iwa_rules

TEST1_DIR = Path(__file__).resolve().parents[1]
CACHE = TEST1_DIR / "cache"
CLUSTERS_JSON = CACHE / "s3_clusters.json"
MAP_JSON = CACHE / "s3_dwa_to_iwa.json"
RES_DIR = CACHE / "s3_results"


def load_all_results() -> dict[str, dict]:
    """명명 결과 적재. 배치(b*.json: list) + 개별(I_*.json: dict) 모두 지원."""
    out: dict[str, dict] = {}
    if not RES_DIR.exists():
        return out
    for p in sorted(RES_DIR.glob("*.json")):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            print(f"[warn] 파싱 실패 skip: {p.name}")
            continue
        recs = data if isinstance(data, list) else [data]
        for r in recs:
            if isinstance(r, dict) and r.get("iwa_id") and (r.get("label") or "").strip():
                out[r["iwa_id"]] = r
    return out


def pending(clusters: list[dict] | None = None) -> list[str]:
    if clusters is None:
        clusters = json.loads(CLUSTERS_JSON.read_text(encoding="utf-8"))
    got = load_all_results()
    return [c["iwa_id"] for c in clusters if c["iwa_id"] not in got]


def run(force: bool = False) -> dict:
    from pipeline import db
    clusters = json.loads(CLUSTERS_JSON.read_text(encoding="utf-8"))
    dwa_to_iwa = json.loads(MAP_JSON.read_text(encoding="utf-8"))
    by_id = {c["iwa_id"]: c for c in clusters}

    got = load_all_results()
    named, missing, labels = {}, [], []
    for c in clusters:
        r = got.get(c["iwa_id"])
        if r and (r.get("label") or "").strip():
            named[c["iwa_id"]] = r
            labels.append(r["label"].strip())
        else:
            missing.append(c["iwa_id"])

    batch = iwa_rules.check_batch_iwa(labels)
    print(f"[validate] 명명 {len(named)}/{len(clusters)} · "
          f"7조항 준수율(R4제외) {batch['pass_rate']:.2%} "
          f"(게이트≥0.90: {'PASS' if batch['gate_passed'] else 'FAIL'}) · "
          f"R4완화 {batch['r4_relaxed_count']}건")
    if missing:
        print(f"[validate] 미명명 {len(missing)}건 → 적재 보류(부분): {missing[:8]}"
              f"{'…' if len(missing) > 8 else ''}")

    named_ids = set(named.keys())
    con = db.get_con()
    con.execute("BEGIN")
    try:
        if force:
            con.execute("DELETE FROM dwa_to_iwa")
            con.execute("DELETE FROM iwa")
        n_iwa = 0
        for iwa_id, r in named.items():
            c = by_id[iwa_id]
            chk = iwa_rules.check_iwa(r["label"])
            label = iwa_rules.normalize_label(r["label"])
            con.execute("DELETE FROM iwa WHERE iwa_id=?", [iwa_id])
            con.execute(
                """INSERT INTO iwa
                   (iwa_id, label, definition, n_dwa, n_task, n_jobs,
                    mean_cosine, eight_rules_passed) VALUES (?,?,?,?,?,?,?,?)""",
                [iwa_id, label, (r.get("definition") or "").strip(),
                 c["n_dwa"], c["n_task"], c["n_jobs"], c["mean_cosine"],
                 bool(chk["passed"])])
            n_iwa += 1
        # dwa_to_iwa: 명명된 IWA에 속한 DWA만(멱등 전체 재적재)
        con.execute("DELETE FROM dwa_to_iwa")
        n_link = 0
        for dwa_id, iwa_id in dwa_to_iwa.items():
            if iwa_id in named_ids:
                con.execute("INSERT INTO dwa_to_iwa (dwa_id, iwa_id) VALUES (?,?)",
                            [dwa_id, iwa_id])
                n_link += 1
        con.execute("COMMIT")
    except Exception:
        con.execute("ROLLBACK")
        raise

    n_pass = con.execute("SELECT COUNT(*) FROM iwa WHERE eight_rules_passed").fetchone()[0]
    # nesting 검증: 모든 적재 DWA가 정확히 1 IWA
    dup = con.execute("SELECT COUNT(*) FROM (SELECT dwa_id FROM dwa_to_iwa "
                      "GROUP BY dwa_id HAVING COUNT(*)>1)").fetchone()[0]
    con.close()
    print(f"[persist] iwa {n_iwa} (7조항통과 {n_pass}) · dwa_to_iwa {n_link} · "
          f"중복배정 DWA {dup}(0이어야 strict)")
    return {"iwa": n_iwa, "links": n_link, "rules_pass": n_pass,
            "pass_rate": batch["pass_rate"], "r4_relaxed": batch["r4_relaxed_count"],
            "missing": len(missing), "dup_dwa": dup}


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", nargs="?", default="run", choices=["run", "pending"])
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    if a.cmd == "pending":
        ps = pending()
        print(f"미명명 {len(ps)}건")
        for x in ps:
            print(" ", x)
    else:
        run(force=a.force)
