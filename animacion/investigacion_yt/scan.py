import json, re, sys, time, concurrent.futures as cf
sys.path.insert(0, ".")
import yts
QUERIES = [
 "qué pasaría si animado", "sobrevivir animación", "historia animada supervivencia", "insectos gigantes", "animales más peligrosos animado",
 "datos curiosos animales", "historia de terror animada", "misterios sin resolver animado", "cómo funciona explicado animado",
 "historia antigua animada", "cuerpo humano curiosidades animado", "qué pasa si no duermes", "la peor forma de morir en la historia",
 "cómo era vivir en", "sobrevive 24 horas", "ruleta de supervivencia", "parte 1 animación supervivencia", "historias de supervivencia reales animadas",
 "plagas", "parásitos", "criaturas abisales", "el animal más", "biología explicada", "experimentos prohibidos", "civilizaciones perdidas",
 "what if you survived", "animated survival story", "what happens if animated", "worst jobs in history animated", "how people lived in",
 "deep sea creatures explained", "insects explained animated", "parasites explained", "would you survive animated",
]
def run(q):
    try: return q, yts.search(q)
    except Exception as e: return q, []
res = {}
with cf.ThreadPoolExecutor(6) as ex:
    for q, r in ex.map(run, QUERIES): res[q] = r
vids = []
for q, r in res.items():
    for v in r:
        v["q"] = q; vids.append(v)
def num(s):
    s = s.replace("\xa0", " ").lower()
    m = re.search(r"(\d[\d.,]*)\s*(mil|m|k|millones|mill)?\b", s)
    if not m: return 0
    n = float(m.group(1).replace(".", "").replace(",", ".")) if m.group(2) else float(m.group(1).replace(".", "").replace(",", ""))
    mult = {"mil": 1e3, "k": 1e3, "m": 1e6, "millones": 1e6, "mill": 1e6}.get(m.group(2), 1)
    return n * mult
for v in vids: v["v"] = num(v["views"])
chans = {}
for v in vids:
    if v["cid"]: chans.setdefault(v["cid"], []).append(v)
print("videos", len(vids), "channels", len(chans))
def chinfo(cid):
    try:
        h = yts.get(f"https://www.youtube.com/channel/{cid}")
        d = yts.initial(h)
        s = json.dumps(d, ensure_ascii=False)
        subs = re.search(r"\"content\": \"([^\"]*suscriptor[^\"]*)\"", s)
        nv = re.search(r'"content": "([^"]*vídeo[^"]*)"', s)
        return cid, (subs.group(1) if subs else ""), (nv.group(1) if nv else "")
    except Exception as e:
        return cid, "", ""
info = {}
with cf.ThreadPoolExecutor(6) as ex:
    for cid, s, n in ex.map(chinfo, list(chans)): info[cid] = (s, n)
rows = []
for cid, vs in chans.items():
    s, n = info[cid]
    subs = num(s) if s else 0; nvid = num(n) if n else 0
    best = max(vs, key=lambda x: x["v"])
    rows.append(dict(channel=best["channel"], cid=cid, subs=subs, nvid=nvid, best_views=best["v"], best_title=best["title"], pub=best["pub"], q=best["q"], len=best["len"],
                     ratio=best["v"] / max(subs, 1)))
json.dump(rows, open("rows.json", "w"), ensure_ascii=False)
small = [r for r in rows if 0 < r["subs"] <= 150000 and r["best_views"] >= 50000]
small.sort(key=lambda r: -r["ratio"])
for r in small[:45]:
    print(f'{r["channel"][:28]:28} subs={r["subs"]:>9,.0f} vids={r["nvid"]:>5,.0f} best={r["best_views"]:>10,.0f} x{r["ratio"]:5.1f} | {r["best_title"][:70]} ({r["pub"]}, {r["len"]}) [{r["q"]}]')
