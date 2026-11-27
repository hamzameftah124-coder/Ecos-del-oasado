import json, re, sys, concurrent.futures as cf
sys.path.insert(0, "."); import yts
import re as _re
def num(s):
    s = s.replace("\xa0", " ").lower()
    m = _re.search(r"(\d[\d.,]*)\s*(mil|m|k|millones|mill)?\b", s)
    if not m: return 0
    n = float(m.group(1).replace(".", "").replace(",", ".")) if m.group(2) else float(m.group(1).replace(".", "").replace(",", ""))
    return n * {"mil": 1e3, "k": 1e3, "m": 1e6, "millones": 1e6, "mill": 1e6}.get(m.group(2), 1)
rows = {r["channel"]: r for r in json.load(open("rows.json"))}
names = ["Primer Nivel", "¿Y Si? en Español", "Bajo el Abismo", "WhatIfVerse", "ImaginaX", "¿Y luego qué?", "IMAGINA ESTO", "Marrow",
         "El Laboratorio Natural", "Huellas del Ayer", "España Recordada", "Little Less Hurry", "Outlast History", "Nowhere Safe",
         "IFBEYOND", "Brain on a Stick", "Insane Survival", "The Map Reason", "Causality", "Sky Archives", "AI Abyss", "Mayson Plain"]
def vids(name):
    r = rows.get(name)
    if not r: return name, None
    try:
        h = yts.get(f"https://www.youtube.com/channel/{r['cid']}/videos")
        d = yts.initial(h)
        s = json.dumps(d, ensure_ascii=False)
        cs = re.findall(r'"content": "([^"]{0,140})"', s)
        out = []
        for i in range(len(cs) - 2):
            if re.match(r"^hace ", cs[i + 2]) and re.match(r"^[\d.,]+\s*(K|M|mil)?$", cs[i + 1].replace("\xa0", " ")):
                out.append((cs[i], num(cs[i + 1]), cs[i + 2]))
        return name, (r, out)
    except Exception as e:
        return name, None
with cf.ThreadPoolExecutor(6) as ex:
    for name, res in ex.map(vids, names):
        if not res: print(name, "n/a"); continue
        r, out = res
        vs = sorted([o[1] for o in out], reverse=True)
        med = vs[len(vs)//2] if vs else 0
        oldest = out[-1][2] if out else ""
        print(f"\n## {name} | {r['subs']:,.0f} subs | {len(out)} vídeos visibles | mediana {med:,.0f} | más antiguo visible: {oldest}")
        for o in out[:6]: print(f"   {o[1]:>10,.0f}  {o[2]:>12}  {o[0][:80]}")
