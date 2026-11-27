import json, numpy as np, soundfile as sf
SR = 44100
paras = [p.strip() for p in open("en/script_en.txt").read().split("\n\n") if p.strip()]
GAP = 0.32; LEAD = 0.06; TAIL = 0.12; MAXPAUSE = 0.55
out = []; words = []; t = 0.0; mism = 0
for i, p in enumerate(paras):
    a, _ = sf.read(f"en/tts/p{i:03d}.wav")
    ws = json.load(open(f"en/tts/p{i:03d}.json"))
    toks = p.split()
    if len(ws) != len(toks):
        mism += 1
        s0 = ws[0][1]; s1 = ws[-1][2]; L = sum(len(x) + 1 for x in toks); acc = 0; ws2 = []
        for x in toks:
            a0 = s0 + (s1 - s0) * acc / L; acc += len(x) + 1; ws2.append([x, a0, s0 + (s1 - s0) * acc / L])
        ws = ws2
    # build kept segments: lead, words with capped pauses, tail
    segs = []  # (src_start, src_end)
    cur0 = max(0, ws[0][1] - LEAD)
    newt = []  # mapping per word
    pos = 0.0  # output time within paragraph
    for k, (w, s, e) in enumerate(ws):
        if k == 0:
            seg_start = cur0
        else:
            pe = ws[k - 1][2]; gap = s - pe
            if gap > MAXPAUSE:
                # cut: keep pe .. pe+MAXPAUSE/2 and s-MAXPAUSE/2 .. s
                segs.append((seg_start, pe + MAXPAUSE / 2)); pos += (pe + MAXPAUSE / 2) - seg_start
                seg_start = s - MAXPAUSE / 2
        # word time in output = pos + (s - seg_start)
        newt.append((pos + (s - seg_start), pos + (e - seg_start)))
    end = min(len(a) / SR, ws[-1][2] + TAIL)
    segs.append((seg_start, end))
    pieces = [a[int(x * SR):int(y * SR)] for x, y in segs]
    pa = np.concatenate(pieces)
    # tiny fades at cut points
    for tok, (s, e) in zip(toks, newt):
        words.append({"w": tok, "para": i, "s": t + s, "e": t + e})
    out.append(pa); t += len(pa) / SR
    if i < len(paras) - 1:
        out.append(np.zeros(int(GAP * SR))); t += GAP
v = np.concatenate(out)
sf.write("en/voice_en.wav", v, SR)
json.dump({"words": words, "offs": [0.0], "durs": [len(v) / SR]}, open("en/align_en.json", "w"))
print("dur", round(len(v) / SR, 2), "words", len(words), "mismatch", mism)
