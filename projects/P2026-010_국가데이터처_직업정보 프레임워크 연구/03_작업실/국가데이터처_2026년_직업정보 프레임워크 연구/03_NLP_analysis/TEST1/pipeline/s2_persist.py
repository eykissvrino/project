"""Stage 2 — 적재: 명명결과 → 8조항 검증 → dwa / task_to_dwa DB(트랜잭션·멱등).

설계 §④-7·8, ⑦, ⑨. 입력:
    cache/s2_clusters.json  (군집 메타: cluster_size·n_jobs·mean_cosine·cross_family)
    cache/s2_links.json     (task_to_dwa: link_order 1~3)
    cache/s2_results/{dwa_id}.json  (Opus 명명: label·definition)

검증: dwa_rules.check_dwa() 하드조항 통과 → eight_rules_passed. 준수율 §⑦ ≥0.90 게이트.
재개: 결과 없는 DWA는 skip(+ 해당 links 보류). PYTHONUTF8=1 권장.
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

from pipeline import dwa_rules

TEST1_DIR = Path(__file__).resolve().parents[1]
CACHE = TEST1_DIR / "cache"
CLUSTERS_JSON = CACHE / "s2_clusters.json"
LINKS_JSON = CACHE / "s2_links.json"
RES_DIR = CACHE / "s2_results"


def load_all_results() -> dict[str, dict]:
    """명명 결과 적재. 배치묶음(b*.json: list) + 개별(D_*.json: dict) 모두 지원."""
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
            if isinstance(r, dict) and r.get("dwa_id") and (r.get("label") or "").strip():
                out[r["dwa_id"]] = r          # 동일 id 중복 시 후자 우선
    return out


def pending(clusters: list[dict] | None = None) -> list[str]:
    """명명 결과가 아직 없는(또는 깨진) dwa_id 목록 — 워크플로 재개용."""
    if clusters is None:
        clusters = json.loads(CLUSTERS_JSON.read_text(encoding="utf-8"))
    got = load_all_results()
    return [c["dwa_id"] for c in clusters if c["dwa_id"] not in got]


def run(force: bool = False) -> dict:
    from pipeline import db
    clusters = json.loads(CLUSTERS_JSON.read_text(encoding="utf-8"))
    links = json.loads(LINKS_JSON.read_text(encoding="utf-8"))
    by_id = {c["dwa_id"]: c for c in clusters}

    got = load_all_results()
    named, missing, labels = {}, [], []
    for c in clusters:
        r = got.get(c["dwa_id"])
        if r and (r.get("label") or "").strip():
            named[c["dwa_id"]] = r
            labels.append(r["label"].strip())
        else:
            missing.append(c["dwa_id"])

    batch = dwa_rules.check_batch(labels)
    print(f"[validate] 명명 {len(named)}/{len(clusters)} · "
          f"8조항 준수율 {batch['pass_rate']:.2%} (게이트≥0.90: "
          f"{'PASS' if batch['gate_passed'] else 'FAIL'})")
    if missing:
        print(f"[validate] 미명명 {len(missing)}건 → 적재 보류: {missing[:8]}"
              f"{'…' if len(missing) > 8 else ''}")

    con = db.get_con()
    con.execute("BEGIN")
    try:
        if force:
            con.execute("DELETE FROM task_to_dwa")
            con.execute("DELETE FROM dwa")
        n_dwa = 0
        for dwa_id, r in named.items():
            c = by_id[dwa_id]
            chk = dwa_rules.check_dwa(r["label"])
            label = dwa_rules.normalize_label(r["label"])
            con.execute("DELETE FROM dwa WHERE dwa_id=?", [dwa_id])
            con.execute(
                """INSERT INTO dwa
                   (dwa_id, label, definition, cluster_size, n_jobs, mean_cosine,
                    eight_rules_passed, is_cross_family) VALUES (?,?,?,?,?,?,?,?)""",
                [dwa_id, label, (r.get("definition") or "").strip(),
                 c["cluster_size"], c["n_jobs"], c["mean_cosine"],
                 bool(chk["passed"]), bool(c.get("is_cross_family", False))])
            n_dwa += 1
        # task_to_dwa: 적재된 dwa만(멱등 전체 재적재)
        named_ids = set(named.keys())
        con.execute("DELETE FROM task_to_dwa")
        n_link = 0
        for l in links:
            if l["dwa_id"] in named_ids:
                con.execute(
                    "INSERT INTO task_to_dwa (task_id, dwa_id, link_order) "
                    "VALUES (?,?,?)", [l["task_id"], l["dwa_id"], l["link_order"]])
                n_link += 1
        con.execute("COMMIT")
    except Exception:
        con.execute("ROLLBACK")
        raise

    n_pass = con.execute("SELECT COUNT(*) FROM dwa WHERE eight_rules_passed").fetchone()[0]
    n_cf = con.execute("SELECT COUNT(*) FROM dwa WHERE is_cross_family").fetchone()[0]
    con.close()
    print(f"[persist] dwa {n_dwa} (8조항통과 {n_pass}) · task_to_dwa {n_link} · "
          f"cross-family {n_cf}")
    return {"dwa": n_dwa, "links": n_link, "rules_pass": n_pass,
            "cross_family": n_cf, "pass_rate": batch["pass_rate"], "missing": missing}


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
