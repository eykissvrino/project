"""Stage 3 — IWA 절단수준 민감도 분석(의사결정 검토서용 데이터 산출).

같은 TASK 응집트리를 여러 높이로 절단했을 때 IWA 개수·DWA:IWA 비율·트리순도·
응집도가 어떻게 변하는지, 그리고 군집 세분도가 어떻게 달라지는지를 정량화한다.
출력: cache/s3_cut_analysis.json (의사결정 HTML이 읽음).
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
from scipy.cluster.hierarchy import fcluster

TEST1_DIR = Path(__file__).resolve().parents[1]
CACHE = TEST1_DIR / "cache"

from pipeline.s2_cluster import EMB_PATH, LINK_PATH

emb = np.load(EMB_PATH)
Z = np.load(LINK_PATH)
ids = json.loads((CACHE / "embedding_ids.json").read_text(encoding="utf-8"))
n = len(ids)
idx_of = {t: i for i, t in enumerate(ids)}
heights = Z[:, 2]

links = json.loads((CACHE / "s2_links.json").read_text(encoding="utf-8"))
prim = defaultdict(list)
for l in links:
    if l.get("link_order") == 1:
        prim[l["dwa_id"]].append(l["task_id"])
n_dwa = len(prim)
k_dwa = json.loads((CACHE / "s2_summary.json").read_text(encoding="utf-8"))["k_cut"]
raw = fcluster(Z, t=k_dwa, criterion="maxclust")

# DWA centroid(1차 TASK 평균, 정규화) — cohesion 계산용
dwa_cent = {}
for d, tids in prim.items():
    rows = [idx_of[t] for t in tids if t in idx_of]
    if not rows:
        continue
    c = emb[rows].mean(axis=0)
    dwa_cent[d] = c / (np.linalg.norm(c) or 1.0)


def map_at(k: int):
    lab = fcluster(Z, t=k, criterion="maxclust")
    tmp = defaultdict(set)
    for i in range(n):
        tmp[int(raw[i])].add(int(lab[i]))
    raw2iwa = {}
    for r, s in tmp.items():
        raw2iwa[r] = (next(iter(s)) if len(s) == 1
                      else Counter(int(lab[i]) for i in range(n) if raw[i] == r).most_common(1)[0][0])
    d2i, purs = {}, []
    for d, tids in prim.items():
        rs = [int(raw[idx_of[t]]) for t in tids if t in idx_of]
        if not rs:
            continue
        dom = Counter(rs).most_common(1)[0][0]
        iw = raw2iwa[dom]
        d2i[d] = iw
        same = sum(1 for r in rs if raw2iwa[r] == iw)
        purs.append(same / len(rs))
    # cohesion: IWA별 소속 DWA centroid 평균 코사인
    members = defaultdict(list)
    for d, iw in d2i.items():
        members[iw].append(d)
    cohs = []
    for iw, ds in members.items():
        mv = np.vstack([dwa_cent[d] for d in ds if d in dwa_cent])
        ic = mv.mean(axis=0)
        ic = ic / (np.linalg.norm(ic) or 1.0)
        cohs.append(float((mv @ ic).mean()))
    eff = len(members)
    return d2i, {
        "k": k, "eff_iwa": eff, "ratio": round(n_dwa / eff, 2),
        "mean_purity": round(float(np.mean(purs)), 4),
        "cohesion_median": round(float(np.median(cohs)), 4),
    }


# 1) 스윕
SWEEP_K = [120, 135, 149, 160, 169, 180, 188, 200, 214, 225, 238, 260, 290]
sweep, maps = [], {}
for k in SWEEP_K:
    d2i, row = map_at(k)
    sweep.append(row)
    maps[k] = d2i
    print(f"k={k:4d} eff={row['eff_iwa']:4d} ratio={row['ratio']:5.2f} "
          f"pur={row['mean_purity']:.3f} coh={row['cohesion_median']:.3f}")

# 2) 자연 gap 곡선(밴드 내 상위)
band_lo, band_hi = n_dwa // 8, n_dwa // 5
gaps = []
for k in range(band_lo, band_hi + 1):
    i = n - 1 - k
    if 0 <= i < len(heights) - 1:
        gaps.append({"k": k, "gap": round(float(heights[i + 1] - heights[i]), 6)})
gaps_top = sorted(gaps, key=lambda x: -x["gap"])[:8]

# 3) 세분도 변화 예시: 채택 k=214의 최대 IWA들이 coarse(149)서 병합 / fine(290)서 분할
CHOSEN, COARSE, FINE = 214, 149, 290
d2i_c = maps[CHOSEN]
mem_c = defaultdict(list)
for d, iw in d2i_c.items():
    mem_c[iw].append(d)
top_iwa = sorted(mem_c.items(), key=lambda kv: -len(kv[1]))[:6]
# 라벨(있으면)
iwa_label = {}
try:
    from pipeline import db
    con = db.get_con(read_only=True)
    for r in con.execute("SELECT iwa_id,label FROM iwa").fetchall():
        iwa_label[r[0]] = r[1]
    # iwa_id(I_xxxx)는 cluster fcluster label과 다름 → s3_dwa_to_iwa로 역매핑
    map_named = json.loads((CACHE / "s3_dwa_to_iwa.json").read_text(encoding="utf-8"))
    con.close()
except Exception:
    map_named = {}

split_demo = []
d2i_fine = maps[FINE]
d2i_coarse = maps[COARSE]
for iw, ds in top_iwa:
    # 이 DWA들이 fine에서 몇 개 IWA로 쪼개지나 / coarse에서 몇 개로 합쳐지나
    fine_groups = len(set(d2i_fine[d] for d in ds if d in d2i_fine))
    coarse_groups = len(set(d2i_coarse[d] for d in ds if d in d2i_coarse))
    # 대표 라벨: 이 DWA들의 명명된 IWA(채택본) 라벨
    named_ids = Counter(map_named.get(d) for d in ds if d in map_named)
    lbl = iwa_label.get(named_ids.most_common(1)[0][0]) if named_ids else f"(군집 {iw})"
    split_demo.append({"label": lbl, "n_dwa": len(ds),
                       "fine_splits": fine_groups, "coarse_merges_into": coarse_groups})

out = {
    "n_dwa": n_dwa, "n_task": n, "band": [band_lo, band_hi],
    "onet_ratio": 6.3, "chosen_k": CHOSEN, "chosen_eff_iwa": maps[CHOSEN] and sweep[SWEEP_K.index(CHOSEN)]["eff_iwa"],
    "sweep": sweep, "gaps_top": gaps_top,
    "split_demo": split_demo, "coarse_k": COARSE, "fine_k": FINE,
}
(CACHE / "s3_cut_analysis.json").write_text(json.dumps(out, ensure_ascii=False, indent=2),
                                            encoding="utf-8")
print("\n[saved] cache/s3_cut_analysis.json")
print("split_demo:")
for s in split_demo:
    print(f"  '{s['label']}' DWA{s['n_dwa']} → fine{FINE}서 {s['fine_splits']}분할 / coarse{COARSE}서 {s['coarse_merges_into']}군집")
