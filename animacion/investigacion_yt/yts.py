import json, re, sys, urllib.request, urllib.parse
H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36", "Accept-Language": "es-ES,es;q=0.9"}
def get(url):
    req = urllib.request.Request(url, headers=H)
    return urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
def initial(html):
    m = re.search(r"var ytInitialData = (\{.*?\});</script>", html, re.S)
    return json.loads(m.group(1)) if m else {}
def walk(o, key):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == key: yield v
            yield from walk(v, key)
    elif isinstance(o, list):
        for v in o: yield from walk(v, key)
def txt(x):
    if not x: return ""
    if "simpleText" in x: return x["simpleText"]
    return "".join(r.get("text", "") for r in x.get("runs", []))
def search(q, sp="CAMSBAgEEAE%3D"):
    d = initial(get("https://www.youtube.com/results?search_query=" + urllib.parse.quote(q) + "&sp=" + sp))
    out = []
    for v in walk(d, "videoRenderer"):
        ch = v.get("ownerText", {}).get("runs", [{}])[0]
        out.append(dict(title=txt(v.get("title")), views=txt(v.get("viewCountText")), pub=txt(v.get("publishedTimeText")),
                        len=txt(v.get("lengthText")), channel=ch.get("text"),
                        cid=ch.get("navigationEndpoint", {}).get("browseEndpoint", {}).get("browseId"), vid=v.get("videoId")))
    return out
if __name__ == "__main__":
    for r in search(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "CAMSBAgEEAE%3D")[:15]:
        print(r)
