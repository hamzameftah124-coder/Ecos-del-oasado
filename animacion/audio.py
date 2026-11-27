# Synthesized music + SFX, mixed under the voice. Outputs per-part and full mixes.
import json, re, numpy as np, soundfile as sf, librosa
from scipy.signal import butter, sosfilt

SR = 44100
TL = json.load(open("work/timeline.json"))
OFFS = TL["offs"]; DURS = TL["durs"]; TOTAL = TL["total"]
TAIL = 1.5
N = int((TOTAL + TAIL) * SR)
rng = np.random.default_rng(7)

def bp(x, lo, hi, order=2):
    sos = butter(order, [lo, hi], btype="band", fs=SR, output="sos"); return sosfilt(sos, x)
def lp(x, f, order=2):
    sos = butter(order, f, btype="low", fs=SR, output="sos"); return sosfilt(sos, x)
def hp(x, f, order=2):
    sos = butter(order, f, btype="high", fs=SR, output="sos"); return sosfilt(sos, x)
def env(n, a=0.005, d=0.2):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)
def noise(sec): return rng.standard_normal(int(sec * SR))
def tone(f, sec, kind="sine"):
    t = np.arange(int(sec * SR)) / SR
    if kind == "sine": return np.sin(2 * np.pi * f * t)
    if kind == "tri": return 2 / np.pi * np.arcsin(np.sin(2 * np.pi * f * t))
    if kind == "saw": return 2 * (t * f % 1) - 1

# ---------------------------------------------------------------- voice
voice = np.zeros(N)
for i, p in enumerate(["p1", "p2", "p3"]):
    y, _ = librosa.load(f"work/{p}.wav", sr=SR)
    s = int(round(OFFS[i] * SR)); voice[s:s + len(y)] += y[: N - s]
voice /= np.max(np.abs(voice)) + 1e-9; voice *= 0.89

# ---------------------------------------------------------------- music
def midi(m): return 440 * 2 ** ((m - 69) / 12)
def pluck(f, sec=0.9, bright=0.5):
    n = int(sec * SR); per = max(2, int(SR / f))
    buf = rng.uniform(-1, 1, per); out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % per]
        buf[i % per] = 0.5 * (buf[i % per] + buf[(i + 1) % per]) * (0.993 + 0.004 * bright)
    return out * env(n, 0.002, sec * 0.5)

pl_cache = {}
def pl(m):
    if m not in pl_cache: pl_cache[m] = pluck(midi(m))
    return pl_cache[m]

def pad(freqs, sec, cutoff=900):
    t = np.arange(int(sec * SR)) / SR
    x = np.zeros_like(t)
    for f in freqs:
        for det in (-0.25, 0.25):
            x += np.sin(2 * np.pi * (f + det) * t) * 0.5 + 0.25 * np.sin(2 * np.pi * 2 * (f + det) * t)
    x = lp(x, cutoff)
    a = np.minimum(1, t / 0.6) * np.minimum(1, (sec - t) / 0.6)
    return x * a / max(1, len(freqs))

# sections: (start, end, mood)
sections = [(0, 5.5, "intro"), (5.5, 35.3, "somber"), (35.3, 126.0, "curious"), (126.0, 233.0, "tense"),
            (233.0, 260.0, "action"), (260.0, 280.4, "curious"), (280.4, 306.0, "action"), (306.0, 405.0, "tense"),
            (405.0, 427.0, "tense"), (427.0, 526.5, "curious"), (526.5, 556.6, "action"), (556.6, 644.8, "somber"),
            (644.8, 677.0, "hope"), (677.0, 691.4, "curious"), (691.4, TOTAL + TAIL, "hope")]
PROG = {"somber": [[57, 60, 64], [53, 57, 60], [50, 53, 57], [52, 56, 59]],         # Am F Dm E
        "curious": [[57, 60, 64], [55, 59, 62], [53, 57, 60], [52, 56, 59]],        # Am G F E
        "tense": [[57, 60, 63], [57, 60, 63], [56, 59, 62], [56, 60, 63]],          # dim-ish
        "action": [[57, 60, 64], [58, 62, 65], [57, 60, 64], [56, 60, 63]],
        "hope": [[60, 64, 67], [55, 59, 62], [57, 60, 64], [53, 57, 60]],           # C G Am F
        "intro": [[57, 61, 64], [57, 61, 64], [57, 61, 64], [57, 61, 64]]}
BPM = {"somber": 80, "curious": 96, "tense": 88, "action": 132, "hope": 92, "intro": 120}
music = np.zeros(N)
for s0, s1, mood in sections:
    beat = 60 / BPM[mood]; bar = beat * 4
    t = s0; k = 0
    while t < s1 - 0.05:
        chord = PROG[mood][k % 4]
        L = min(bar, s1 - t)
        i0 = int(t * SR)
        if mood != "intro":
            pd = pad([midi(m - 12) for m in chord], L + 0.3, 700 if mood in ("tense", "somber") else 1100)
            music[i0:i0 + len(pd)] += pd[: N - i0] * (0.22 if mood != "action" else 0.16)
            # bass
            b = tone(midi(chord[0] - 24), L, "tri") * env(int(L * SR), 0.01, L * 0.6)
            music[i0:i0 + len(b)] += b[: N - i0] * 0.18
        # plucked arpeggio
        steps = 8 if mood in ("curious", "hope", "action", "intro") else 4
        for j in range(steps):
            tj = t + j * bar / steps
            if tj >= s1: break
            if mood == "tense" and j % 2: continue
            m = chord[[0, 1, 2, 1, 0, 2, 1, 2][j % 8]] + (12 if mood in ("hope", "intro") else 0)
            x = pl(m); i = int(tj * SR)
            music[i:i + len(x)] += x[: max(0, N - i)] * (0.20 if mood != "tense" else 0.14)
        # percussion
        if mood in ("action", "tense", "intro"):
            for j in range(4):
                tj = t + j * beat
                if tj >= s1: break
                i = int(tj * SR)
                kick = tone(55, 0.25) * env(int(0.25 * SR), 0.002, 0.08)
                music[i:i + len(kick)] += kick[: N - i] * (0.35 if mood == "action" else 0.2)
                if mood == "action":
                    hh = hp(noise(0.05), 6000) * env(int(0.05 * SR), 0.001, 0.015)
                    ih = int((tj + beat / 2) * SR)
                    music[ih:ih + len(hh)] += hh[: max(0, N - ih)] * 0.08
        t += bar; k += 1
music = lp(music, 5000)
# fades at part edges so each part starts/ends cleanly
def fade_env():
    e = np.ones(N)
    for o in OFFS[1:]:
        i = int(o * SR); w = int(0.25 * SR)
        e[i - w:i] *= np.linspace(1, 0.2, w); e[i:i + w] *= np.linspace(0.2, 1, w)
    w = int(TAIL * SR); e[-w:] *= np.linspace(1, 0, w)
    return e
music *= fade_env()

# ---------------------------------------------------------------- SFX
W = [(s, " ".join(ws)) for s, ws in zip(TL["sent_t"], TL["sents"])]
A = json.load(open("work/align.json"))["words"]
def word_time(pattern, nth=0, after=0.0):
    """time of the first word of the nth match of a phrase (case-insensitive) after `after`."""
    toks = [re.sub(r"[^\wáéíóúñü]", "", w["w"].lower()) for w in A]
    pat = pattern.lower().split(); hits = []
    for i in range(len(toks) - len(pat) + 1):
        if toks[i:i + len(pat)] == pat and A[i]["s"] >= after: hits.append(i)
    i = hits[nth]; return A[i]["s"], A[i + len(pat) - 1]["e"]

sfx = np.zeros(N)
def put(x, t, g=1.0):
    i = int(t * SR)
    if i >= N: return
    sfx[i:i + len(x)] += x[: N - i] * g

def s_click(): return hp(noise(0.03), 2000) * env(int(0.03 * SR), 0.0005, 0.006)
def s_tick(): return bp(noise(0.04), 2500, 7000) * env(int(0.04 * SR), 0.0005, 0.008) * 1.5
def s_ding():
    n = 1.2; return (tone(1320, n) + 0.5 * tone(1980, n) + 0.3 * tone(2640, n)) * env(int(n * SR), 0.002, 0.35) * 0.4
def s_buzz(sec=1.3):
    t = np.arange(int(sec * SR)) / SR; f = 520 + 40 * np.sin(2 * np.pi * 5 * t)
    x = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.3
    return lp(x, 3000) * np.minimum(1, t / 0.15) * np.minimum(1, (sec - t) / 0.3)
def s_static(sec=1.0):
    t = np.arange(int(sec * SR)) / SR
    return bp(noise(sec), 800, 6000) * 0.25 * np.minimum(1, (sec - t) / 0.3) * (0.6 + 0.4 * (np.sin(2 * np.pi * 9 * t) > 0))
def s_glass():
    out = np.zeros(int(0.9 * SR))
    for k in range(9):
        x = bp(noise(0.12), 3000, 9000) * env(int(0.12 * SR), 0.001, 0.03)
        i = int(rng.uniform(0, 0.6) * SR); out[i:i + len(x)] += x * rng.uniform(0.4, 1)
    return out * 0.6
def s_creak(sec=0.9, f0=180):
    t = np.arange(int(sec * SR)) / SR; f = f0 + 60 * np.sin(2 * np.pi * 0.8 * t)
    ph = np.cumsum(f) / SR
    x = ((ph * 1) % 1 < 0.08).astype(float) * 1.0
    x = bp(x, 300, 2500)
    return x * 0.5 * np.minimum(1, t / 0.05) * np.minimum(1, (sec - t) / 0.2)
def s_clink():
    n = 0.5; return (tone(2200, n) + 0.6 * tone(3300, n)) * env(int(n * SR), 0.001, 0.08) * 0.3
def s_can_open():
    x = bp(noise(0.25), 1500, 8000) * env(int(0.25 * SR), 0.001, 0.05)
    return np.concatenate([s_click() * 2, x]) * 0.7
def s_whoosh(sec=0.5):
    t = np.arange(int(sec * SR)) / SR
    return bp(noise(sec), 400, 3000) * np.sin(np.pi * t / sec) ** 2 * 0.6
def s_squeak():
    sec = 0.3; t = np.arange(int(sec * SR)) / SR
    return tone(1, sec) * 0 + np.sin(2 * np.pi * np.cumsum(1800 - 2400 * t) / SR) * env(int(sec * SR), 0.005, 0.12) * 0.25
def s_clang():
    n = 1.0
    return (tone(620, n) + 0.7 * tone(1490, n) + 0.5 * tone(2380, n) + bp(noise(n), 2000, 6000) * env(int(n * SR), 0.0005, 0.02) * 3) * env(int(n * SR), 0.001, 0.25) * 0.35
def s_crack():
    x = hp(noise(0.12), 1000) * env(int(0.12 * SR), 0.0005, 0.02); return x * 0.9
def s_wind(sec=1.6):
    t = np.arange(int(sec * SR)) / SR
    return bp(noise(sec), 300, 1500) * np.sin(np.pi * t / sec) * 0.5
def s_slam():
    n = 0.8; x = lp(noise(n), 300) * env(int(n * SR), 0.001, 0.12) * 2.5 + tone(70, n) * env(int(n * SR), 0.001, 0.2) * 0.8
    return x * 0.8
def s_rumble(sec=1.4):
    t = np.arange(int(sec * SR)) / SR
    return lp(noise(sec), 120) * 3 * np.minimum(1, t / 0.05) * np.exp(-t / 0.6)
def s_knock():
    n = 0.12; return lp(noise(n), 900) * env(int(n * SR), 0.0005, 0.02) * 1.6
def s_drip():
    n = 0.2; t = np.arange(int(n * SR)) / SR
    return np.sin(2 * np.pi * np.cumsum(900 + 1400 * t / n) / SR) * env(int(n * SR), 0.001, 0.04) * 0.35
def s_cart(sec=1.2):
    t = np.arange(int(sec * SR)) / SR
    x = bp(noise(sec), 150, 900) * (0.6 + 0.4 * np.sin(2 * np.pi * 14 * t)) * np.minimum(1, t / 0.1) * np.minimum(1, (sec - t) / 0.2)
    return x * 0.6
def s_step():
    n = 0.12; return lp(noise(n), 500) * env(int(n * SR), 0.002, 0.03) * 0.9
def s_latch():
    return np.concatenate([s_click() * 2, np.zeros(int(0.06 * SR)), s_click() * 3])
def s_crash():
    out = np.zeros(int(1.6 * SR))
    for k in range(5):
        x = s_clang(); i = int(rng.uniform(0, 0.6) * SR); out[i:i + len(x)] += x[: len(out) - i] * rng.uniform(0.5, 1)
    return out * 0.8
def s_birds(sec=2.0):
    out = np.zeros(int(sec * SR))
    for k in range(5):
        n = 0.15; t = np.arange(int(n * SR)) / SR
        x = np.sin(2 * np.pi * np.cumsum(3000 + 1500 * np.sin(2 * np.pi * 30 * t)) / SR) * env(int(n * SR), 0.005, 0.05) * 0.15
        i = int(rng.uniform(0.1, sec - 0.3) * SR); out[i:i + len(x)] += x
    return out + s_wind(sec) * 0.3
def s_spin(sec=4.3):
    out = np.zeros(int((sec + 0.2) * SR)); t = 0.0; gap = 0.05
    while t < sec:
        x = s_tick(); i = int(t * SR); out[i:i + len(x)] += x[: len(out) - i]
        t += gap; gap *= 1.06
    return out

put(s_spin(), 0.0, 0.8)
put(s_ding(), word_time("cucaracha")[0] - 0.1, 0.8)
put(s_buzz(), word_time("un mosquito")[0], 0.5)
put(s_static(), word_time("radios")[0], 0.6)
put(s_creak(0.7, 140), word_time("puertas abiertas")[0], 0.35)
put(s_glass(), word_time("cristales rotos")[0], 0.7)
put(s_creak(1.0, 200), word_time("puerta metálica")[0], 0.45)
put(s_clink(), word_time("latas", 0, 60)[0], 0.6)
put(s_click(), word_time("con la linterna")[0], 1.0)
put(s_creak(1.1, 120), word_time("la despensa", 0, 95)[0], 0.5)
put(s_can_open(), word_time("una lata de tomate")[0], 0.8)
for nth in range(4):
    try:
        a, b = word_time("tic tic tic", nth)
        for k in range(3): put(s_tick(), a + k * (b - a) / 3, 1.2)
    except IndexError: pass
put(s_click(), word_time("apaga la linterna")[0], 1.2)
put(s_click(), word_time("enciende la linterna")[0], 1.2)
put(s_whoosh(0.5), word_time("sale disparado")[0], 0.9)
put(s_squeak(), word_time("resbala")[0], 0.8)
put(s_whoosh(0.4), word_time("sale volando")[0], 0.7)
put(s_clang(), word_time("rebota")[0], 0.7)
put(s_crack(), word_time("se parte en dos")[0], 1.0)
put(s_click(), word_time("y se apaga")[0], 1.0)
put(s_wind(), word_time("ráfaga de viento")[0], 0.6)
put(s_slam(), word_time("se cierra de golpe")[0], 1.0)
put(s_rumble(), word_time("como un trueno")[0], 0.6)
a = word_time("golpea con suavidad")[0]
for k in range(3): put(s_knock(), a + k * 0.22, 0.8)
a = word_time("que gotea")[0]
for k in range(3): put(s_drip(), a + k * 0.45, 0.6)
put(s_cart(1.2), word_time("mueve un carrito")[0], 0.6)
put(s_cart(1.0), word_time("lo empuja hacia")[0], 0.6)
put(s_latch(), word_time("levanta el pestillo")[0], 1.0)
a = word_time("un paso esperar")[0]; put(s_step(), a, 0.7)
a = word_time("otro paso esperar")[0]; put(s_step(), a, 0.7)
a = word_time("paso a paso")[0]
for k in range(3): put(s_step(), a + k * 0.35, 0.6)
put(s_clang(), word_time("golpea el carrito")[0], 0.7)
put(s_crash(), word_time("las ollas caen")[0], 0.7)
put(s_rumble(1.2), word_time("la cocina entera retumba")[0], 0.6)
put(s_cart(1.3), word_time("lo empuja sin ruido")[0], 0.35)
put(s_clink(), word_time("la rejilla caída")[0], 0.5)
put(s_birds(), word_time("salen al tejado")[0], 0.7)
a = word_time("escalera de incendios")[0]
for k in range(4): put(s_clang() * 0.3, a + k * 0.3, 0.4)

# ---------------------------------------------------------------- mix with ducking
venv = np.abs(voice)
win = int(0.25 * SR)
venv = np.convolve(venv, np.ones(win) / win, mode="same")
venv = venv / (np.max(venv) + 1e-9)
duck = 1 - 0.55 * np.clip(venv * 4, 0, 1)
music_n = music / (np.max(np.abs(music)) + 1e-9)
sfx_n = np.tanh(sfx * 1.5) / np.tanh(1.5)
sfx_n = sfx_n / (np.max(np.abs(sfx_n)) + 1e-9) * 0.45
mix = voice + music_n * 0.2 * duck + sfx_n * (1 - 0.4 * np.clip(venv * 4, 0, 1))
mix = np.tanh(mix * 1.1) / np.tanh(1.1)
peak = np.max(np.abs(mix))
mix = mix / peak * 0.95 if peak > 0.95 else mix
print("peak", peak, "music rms dB", 20 * np.log10(np.sqrt(np.mean((music_n * 0.2 * duck) ** 2))), "voice rms dB", 20 * np.log10(np.sqrt(np.mean(voice ** 2))))
sf.write("work/mix_full.wav", mix, SR, subtype="PCM_16")
for i in range(3):
    a = int(OFFS[i] * SR); b = int((OFFS[i] + DURS[i] + (TAIL if i == 2 else 0)) * SR)
    seg = mix[a:b].copy()
    # small fade-in/out at cut points of the music/sfx only (voice is untouched inside)
    sf.write(f"work/mix_p{i+1}.wav", seg, SR, subtype="PCM_16")
print("ok")
