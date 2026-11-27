import re, sys, json, concurrent.futures as cf
sys.path.insert(0, "."); import yts
yts.H["Accept-Language"] = "en-US,en;q=0.9"
def num(s):
    s = s.replace("\xa0", " ").lower().replace(",", "")
    m = re.search(r"(\d[\d.]*)\s*(k|m|b)?\b", s)
    if not m: return 0
    return float(m.group(1)) * {"k": 1e3, "m": 1e6, "b": 1e9}.get(m.group(2), 1)
Q = ["survive 100 days giant insects", "giant insects survival animated", "survive with cockroaches", "parasites explained animated",
     "insects explained", "every parasite explained", "would you survive giant bugs", "100 days survival animated",
     "survive 1 year animated", "day 1 to day 100 survival animation", "trapped for 1 year animated", "what if insects were giant",
     "deadliest insects explained", "creepy bugs explained", "every insect that", "survive in a house infested", "ant colony animated story"]
res = []
with cf.ThreadPoolExecutor(6) as ex:
    for q, r in zip(Q, ex.map(yts.search, Q)):
        for v in r: v["q"] = q; v["v"] = num(v["views"]); res.append(v)
ch = {}
for v in res:
    if v["cid"]: ch.setdefault(v["cid"], []).append(v)
def info(cid):
    try:
        s = json.dumps(yts.initial(yts.get(f"https://www.youtube.com/channel/{cid}")), ensure_ascii=False)
        m = re.search(r'"content": "([^"]*subscriber[^"]*)"', s); n = re.search(r'"content": "([^"]*videos?)"', s)
        return cid, num(m.group(1)) if m else 0, num(n.group(1)) if n else 0
    except Exception: return cid, 0, 0
rows = []
with cf.ThreadPoolExecutor(6) as ex:
    for cid, subs, nv in ex.map(info, list(ch)):
        b = max(ch[cid], key=lambda x: x["v"])
        rows.append((b["v"] / max(subs, 1), subs, nv, b))
print("videos", len(res), "channels", len(rows))
for ratio, subs, nv, b in sorted([r for r in rows if 300 < r[1] < 200000 and r[3]["v"] > 50000], key=lambda r: -r[0])[:30]:
    print(f'{b["channel"][:24]:24} subs={subs:>8,.0f} vids={nv:>5,.0f} best={b["v"]:>11,.0f} x{ratio:6.1f} | {b["title"][:72]} ({b["pub"]}) [{b["q"]}] {b["cid"]}')
