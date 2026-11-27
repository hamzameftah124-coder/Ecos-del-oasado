import json, re
from story2 import build
C = "C"
_W = json.load(open("work/align.json"))["words"]
_paras = []; _start = True
for i, w in enumerate(_W):
    if _start: _paras.append(w["para"]); _start = False
    nxt = _W[i + 1] if i + 1 < len(_W) else None
    if re.search(r"[.?!:]$", w["w"]) or (w["w"].endswith("…") and nxt and nxt["w"][0].isupper()) or not nxt or nxt["para"] != w["para"]:
        _start = True
SB = build(_paras)
