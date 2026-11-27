import json, re, sys, concurrent.futures as cf
sys.path.insert(0, "."); import yts
yts.H["Accept-Language"] = "en-US,en;q=0.9"
def num(s):
    s = s.replace("\xa0", " ").lower().replace(",", "")
    m = re.search(r"(\d[\d.]*)\s*(k|m|b)?\b", s)
    return float(m.group(1)) * {"k": 1e3, "m": 1e6, "b": 1e9}.get(m.group(2), 1) if m else 0
CH = {"One Year Inside": "UCWif7N1C2ptpoUOLYCB353A", "Your Other Life": "UCZw9yuzRJV5itMb60or5bcg", "Nowhere Safe": "UCThqd5_nd0mraA5UuH992uA",
      "Mr. DoomStick": "UCvo4SkLnD35z_F0a6hFbCtg", "Marrow": "UCgzVBte0O0Iju1ACoNbdINQ", "Nobody Leaves": "UC8ZI36lMpVuYaraDtnNVZig",
      "StickDread": "UCQ2G7eQ_2c9vrQQSnt8n53A", "Headlamp Guy": "UCEwbkI91uCLJnbf9Wf67X9w", "Last Lamp": "UCMFoQOG39LCFojJahQYHHQQ",
      "Sam Survives": "UCwrQuAUBeQaujR9lpAO-nbw", "Thinkdots": "UCIgqKdnxbcAV5rG_3gFjq0g", "Stick It Out": "UCEIa6uIuby6yeTlaC0dP34Q"}
def vids(item):
    name, cid = item
    s = json.dumps(yts.initial(yts.get(f"https://www.youtube.com/channel/{cid}/videos")), ensure_ascii=False)
    cs = re.findall(r'"content": "([^"]{0,160})"', s)
    lens = re.findall(r'"text": "(\d+:\d\d(?::\d\d)?)"', s)
    out = []
    for i in range(len(cs) - 2):
        if re.match(r"^\d+(d|w|mo|h|y) ago$", cs[i + 2]) and re.match(r"^[\d.,]+[KMB]?$", cs[i + 1]):
            out.append((num(cs[i + 1]), cs[i], cs[i + 2]))
    return name, out, lens[:len(out)]
rows = []
with cf.ThreadPoolExecutor(6) as ex:
    for name, out, lens in ex.map(vids, CH.items()):
        print(f"\n## {name} ({len(out)} vídeos)")
        for k, (v, t, p) in enumerate(sorted(out, reverse=True)[:5]):
            print(f"  {v:>10,.0f}  {p:>13}  {t[:90]}")
        rows += [(v, name, t) for v, t, p in out]
json.dump(rows, open("top_en.json", "w"))
