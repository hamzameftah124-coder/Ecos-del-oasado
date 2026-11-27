import json, sys, base64, urllib.request, numpy as np, soundfile as sf
TEXT = "Day twenty. The last can is gone. And then, from somewhere in the dark kitchen, they hear it. Tick. Tick. Tick. Something is coming."
def tts(voice, model, out):
    body = json.dumps({"model_id": model, "transcript": TEXT, "voice": {"mode": "id", "id": voice}, "language": "en",
                       "output_format": {"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100}, "add_timestamps": True}).encode()
    req = urllib.request.Request("https://api.cartesia.ai/tts/sse", data=body, method="POST",
        headers={"Cartesia-Version": "2025-04-16", "Authorization": "Bearer dummy", "Content-Type": "application/json"})
    pcm = b""; words = []
    with urllib.request.urlopen(req, timeout=120) as r:
        for raw in r:
            line = raw.decode().strip()
            if not line.startswith("data:"): continue
            ev = json.loads(line[5:])
            if ev.get("type") == "chunk" and ev.get("data"): pcm += base64.b64decode(ev["data"])
            elif ev.get("type") == "timestamps":
                wt = ev["word_timestamps"]; words += list(zip(wt["words"], wt["start"], wt["end"]))
            elif ev.get("type") == "error": print("ERR", ev); return
    a = np.frombuffer(pcm, dtype=np.float32)
    sf.write(out, a, 44100)
    print(out, round(len(a) / 44100, 2), "s,", len(words), "palabras:", words[:4], "...", words[-2:])
for name, vid in [("damon", "dbfa416f-d5c3-4006-854b-235ef6bdf4fd"), ("darius", "23112795-d54e-4560-9568-791a87c30201"), ("adrian", "e2d48e7b-cd73-4c4c-bc1e-f232580e8709")]:
    try: tts(vid, sys.argv[1], f"voz/{name}.wav")
    except Exception as e: print(name, "fallo:", e, getattr(e, "read", lambda: b"")()[:300])
