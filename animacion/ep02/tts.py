import json, base64, urllib.request, numpy as np, soundfile as sf, concurrent.futures as cf, time, os, sys
VOICE = "e2d48e7b-cd73-4c4c-bc1e-f232580e8709"  # Adrian - Explorer
SR = 44100
paras = [p.strip() for p in open("ep2/script.txt").read().split("\n\n") if p.strip()]
os.makedirs("ep2/tts", exist_ok=True)
def tts(i):
    fn = f"ep2/tts/p{i:03d}.json"
    if os.path.exists(fn): return i, "cached"
    body = json.dumps({"model_id": "sonic-3", "transcript": paras[i], "voice": {"mode": "id", "id": VOICE}, "language": "en",
                       "output_format": {"container": "raw", "encoding": "pcm_f32le", "sample_rate": SR}, "add_timestamps": True}).encode()
    for attempt in range(4):
        try:
            req = urllib.request.Request("https://api.cartesia.ai/tts/sse", data=body, method="POST",
                headers={"Cartesia-Version": "2025-04-16", "Authorization": "Bearer dummy", "Content-Type": "application/json"})
            pcm = b""; words = []
            with urllib.request.urlopen(req, timeout=180) as r:
                for raw in r:
                    line = raw.decode().strip()
                    if not line.startswith("data:"): continue
                    ev = json.loads(line[5:])
                    if ev.get("type") == "chunk" and ev.get("data"): pcm += base64.b64decode(ev["data"])
                    elif ev.get("type") == "timestamps":
                        wt = ev["word_timestamps"]; words += [[w, s, e] for w, s, e in zip(wt["words"], wt["start"], wt["end"])]
                    elif ev.get("type") == "error": raise RuntimeError(str(ev))
            a = np.frombuffer(pcm, dtype=np.float32)
            sf.write(f"ep2/tts/p{i:03d}.wav", a, SR)
            json.dump(words, open(fn, "w"))
            return i, "ok"
        except Exception as e:
            time.sleep(2 + attempt * 3); err = e
    return i, f"FAIL {err}"
with cf.ThreadPoolExecutor(3) as ex:
    for i, st in ex.map(tts, range(len(paras))):
        if st != "ok": print(i, st, flush=True)
print("done", len(paras))
