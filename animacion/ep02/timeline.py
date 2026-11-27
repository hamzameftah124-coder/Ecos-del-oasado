import json, re, copy, math
from story import SB, C

A = json.load(open("work/align.json"))
W = A["words"]; OFFS = A["offs"]; DURS = A["durs"]
TOTAL = OFFS[-1] + DURS[-1]
PART_CUTS = list(OFFS[1:])

# sentences (same rule as listing)
sents = []; cur = []
for i, w in enumerate(W):
    cur.append(i)
    nxt = W[i + 1] if i + 1 < len(W) else None
    if re.search(r"[.?!:]$", w["w"]) or (w["w"].endswith("…") and nxt and nxt["w"][0].isupper()) or not nxt or nxt["para"] != w["para"]:
        sents.append(cur); cur = []
assert len(sents) == len(SB), (len(sents), len(SB))

def s_start(k): return W[sents[k][0]]["s"]

# cut times
cuts = []
for k in range(len(sents)):
    st = 0.0 if k == 0 else max(s_start(k) - 0.12, W[sents[k - 1][-1]]["e"] + 0.02)
    for pc in PART_CUTS:
        if abs(st - pc) < 1.5 and W[sents[k - 1][-1]]["e"] <= pc <= s_start(k) + 0.05:
            st = pc
    cuts.append(st)
cuts.append(TOTAL)

shots = []
for k in range(len(sents)):
    spec = SB.get(k)
    t0, t1 = cuts[k], cuts[k + 1]
    if spec is None:
        raise SystemExit(f"missing storyboard for sentence {k}")
    if spec == C:
        shots[-1]["t1"] = t1; shots[-1]["sents"].append(k)
        continue
    specs = spec if isinstance(spec, list) else [spec]
    n = len(specs)
    # split boundaries snapped to word starts
    bounds = [t0]
    wstarts = [W[i]["s"] - 0.05 for i in sents[k][1:]]
    for j in range(1, n):
        target = t0 + (t1 - t0) * j / n
        cand = min(wstarts, key=lambda x: abs(x - target)) if wstarts else target
        if cand <= bounds[-1] + 0.4 or abs(cand - target) > 0.9: cand = target
        bounds.append(cand)
    bounds.append(t1)
    for j, sp in enumerate(specs):
        sh = copy.deepcopy(sp)
        sh["t0"] = bounds[j]; sh["t1"] = bounds[j + 1]; sh["sents"] = [k]
        p = sh.setdefault("p", {})
        if "t0" in p:
            if p["t0"] == -1: p["t0"] = bounds[0] if j > 0 else bounds[j]
            elif isinstance(p["t0"], int) and p["t0"] > 0: p["t0"] = cuts[p["t0"]]
        shots.append(sh)

# resolve t0=-1 chained through continuations: screen scene groups share first start
for sh in shots:
    if sh["p"].get("t0") == -1: sh["p"]["t0"] = sh["t0"]

WORLD_SC = {"kitchen", "pantry", "street", "city", "garden", "radio", "duct", "roof"}
for sh in shots:
    if sh["sc"] not in WORLD_SC and "t0" not in sh["p"]:
        sh["p"]["t0"] = sh["t0"]
# split long shots (<= 3.9 s), with camera variation
out = []
for sh in shots:
    d = sh["t1"] - sh["t0"]
    n = max(1, math.ceil(d / 3.9))
    if n == 1:
        out.append(sh); continue
    for j in range(n):
        s2 = copy.deepcopy(sh)
        s2["t0"] = sh["t0"] + d * j / n; s2["t1"] = sh["t0"] + d * (j + 1) / n
        s2["piece"] = [j, n]
        s2["var"] = j % 2
        out.append(s2)
shots = out
# never cross part boundaries
fixed = []
for sh in shots:
    parts = [sh]
    for pc in PART_CUTS:
        nxt = []
        for s in parts:
            if s["t0"] < pc - 0.01 < s["t1"] - 0.02:
                a = copy.deepcopy(s); b = copy.deepcopy(s); a["t1"] = pc; b["t0"] = pc; nxt += [a, b]
            else: nxt.append(s)
        parts = nxt
    fixed += parts
shots = fixed
for i, sh in enumerate(shots): sh["id"] = i

# subtitles: groups of up to 3 words within sentence, balanced
nosub_sents = set()
for sh in shots:
    if sh.get("nosub"): nosub_sents.update(sh["sents"])
groups = []
for k, s in enumerate(sents):
    if k in nosub_sents: continue
    n = len(s); g = math.ceil(n / 3)
    sizes = [n // g + (1 if i < n % g else 0) for i in range(g)]
    idx = 0
    for sz in sizes:
        ws = s[idx:idx + sz]; idx += sz
        groups.append({"words": [{"w": W[i]["w"], "s": W[i]["s"], "e": W[i]["e"]} for i in ws], "t0": W[ws[0]]["s"] - 0.05, "t1": W[ws[-1]]["e"] + 0.15})
for a, b in zip(groups, groups[1:]):
    if b["t0"] - a["t1"] < 0.35: a["t1"] = b["t0"]
    a["t1"] = min(a["t1"], b["t0"])
# do not let a subtitle cross a part boundary
for g in groups:
    for pc in PART_CUTS:
        if g["t0"] < pc < g["t1"]: g["t1"] = pc

json.dump({"shots": shots, "subs": groups, "total": TOTAL, "offs": OFFS, "durs": DURS,
           "sents": [[W[i]["w"] for i in s] for s in sents], "sent_t": [[W[s[0]]["s"], W[s[-1]]["e"]] for s in sents]},
          open("work/timeline.json", "w"), ensure_ascii=False)
ds = [s["t1"] - s["t0"] for s in shots]
print("shots", len(shots), "max", round(max(ds), 2), "min", round(min(ds), 2), "subs", len(groups))
print("short shots:", [(s["id"], round(s["t1"] - s["t0"], 2), s["sents"]) for s in shots if s["t1"] - s["t0"] < 0.6])
