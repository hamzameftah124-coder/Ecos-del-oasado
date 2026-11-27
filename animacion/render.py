import json, math, sys, subprocess, bisect, numpy as np, skia
from gfx import *
from scenes import WORLDS
from screens import SCREENS

TL = json.load(open("work/timeline.json"))
SHOTS = TL["shots"]; SUBS = TL["subs"]
STARTS = [s["t0"] for s in SHOTS]; SUBST = [g["t0"] for g in SUBS]
FPS = 30

def fmt_dims(fmt):
    return (1080, 1920) if fmt == "v" else (1920, 1080)

def shot_at(T):
    i = max(0, bisect.bisect_right(STARTS, T) - 1)
    return SHOTS[i]

def resolve_box(cams, c):
    if isinstance(c, str): return cams[c]
    return tuple(c)

def cam_boxes(sh, cams):
    cam = sh["cam"]
    if isinstance(cam, list) and len(cam) == 2 and not isinstance(cam[0], (int, float)):
        return resolve_box(cams, cam[0]), resolve_box(cams, cam[1])
    b = resolve_box(cams, cam)
    return b, (b[0], b[1], b[2] * 0.93, b[3] * 0.93)

def subtitle(c, W, H, T, fmt):
    i = bisect.bisect_right(SUBST, T) - 1
    if i < 0: return
    g = SUBS[i]
    if not (g["t0"] <= T < g["t1"]): return
    size = 86 if fmt == "v" else 74
    words = [w["w"].upper() for w in g["words"]]
    sp = measure(" ", size)
    widths = [measure(w, size) for w in words]
    tot = sum(widths) + sp * (len(words) - 1)
    maxw = W - 100
    if tot > maxw:
        k = maxw / tot; size *= k; widths = [w * k for w in widths]; sp *= k; tot = maxw
    y = H * (0.75 if fmt == "v" else 0.885)
    pop = back_out(clamp((T - g["t0"]) / 0.14))
    c.save(); c.translate(W / 2, y); c.scale(0.85 + 0.15 * pop, 0.85 + 0.15 * pop)
    x = -tot / 2
    cur = 0
    for j, w in enumerate(g["words"]):
        if T >= w["s"] - 0.03: cur = j
    for j, w in enumerate(words):
        colr = "#ffd400" if j == cur else "#ffffff"
        f = skia.Font(FONT_BLACK, size)
        sh = P("#000000", 120, size * 0.22, blur=6)
        c.drawString(w, x + 4, 6, f, sh)
        c.drawString(w, x, 0, f, P(OUTLINE, 255, size * 0.2))
        c.drawString(w, x, 0, f, P(colr))
        x += widths[j] + sp
    c.restore()

def content_rect(W, H, fmt):
    if fmt == "v": return dict(x=70, y=H * 0.22, w=W - 140, h=H * 0.42)
    return dict(x=200, y=H * 0.22, w=W - 400, h=H * 0.54)

def draw_content(c, W, H, T, fmt):
    sh = shot_at(T)
    t = T - sh["t0"]; d = max(sh["t1"] - sh["t0"], 1e-3); u = clamp(t / d)
    p = dict(sh["p"])
    sc = sh["sc"]
    shake = p.get("shake", 0)
    c.save()
    if sc in WORLDS:
        fn, cams = WORLDS[sc]
        b0, b1 = cam_boxes(sh, cams)
        uu = u
        if "piece" in sh:
            j, n = sh["piece"]; uu = (j + u) / n
        e = ease(uu)
        cx, cy, bw, bh = [lerp(a, b, e) for a, b in zip(b0, b1)]
        if sh.get("var"):
            bw *= 0.78; bh *= 0.78
        if fmt == "v": bw = max(min(bw, bh * 0.78), bw * 0.58)
        s = min(W / bw, H / bh)
        sx = math.sin(T * 47) * shake * 14 + math.sin(T * 13) * shake * 8
        sy = math.cos(T * 41) * shake * 12
        c.translate(W / 2 + sx, H / 2 + sy); c.scale(s, s); c.translate(-cx, -cy)
        fn(c, t, u, p)
    else:
        fn = SCREENS[sc]
        R = content_rect(W, H, fmt)
        tt = t
        if "t0" in p: tt = T - p["t0"]
        p["_T"] = T
        if sh.get("var"):
            c.translate(W / 2, H * 0.45); c.scale(1.07, 1.07); c.translate(-W / 2, -H * 0.45)
        fn(c, W, H, tt, u, p, R)
    c.restore()
    # vignette
    p2 = skia.Paint(AntiAlias=True)
    p2.setShader(skia.GradientShader.MakeRadial(skia.Point(W / 2, H / 2), max(W, H) * 0.75, [col("#000000", 0), col("#000000", 0), col("#000000", 120)], [0.0, 0.6, 1.0]))
    c.drawRect(skia.Rect.MakeWH(W, H), p2)
    if not sh.get("nosub"):
        subtitle(c, W, H, T, fmt)

def draw_frame(c, T, fmt):
    if fmt == "v":
        c.clear(col("#000000"))
        draw_content(c, 1080, 1920, T, "v")
    else:
        # YouTube: picture slightly reduced with a margin so the whole frame stays visible
        c.clear(col("#0c0e13"))
        m = 0.88
        W, H = 1920, 1080
        c.save()
        c.translate(W * (1 - m) / 2, H * (1 - m) / 2); c.scale(m, m)
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeWH(W, H), 28, 28)
        c.drawRRect(rr.makeOffset(0, 10) if hasattr(rr, "makeOffset") else rr, P("#000000", 160, blur=20))
        c.clipRRect(rr, True)
        draw_content(c, W, H, T, "h")
        c.restore()
        c.save(); c.translate(W * (1 - m) / 2, H * (1 - m) / 2); c.scale(m, m)
        c.drawRRect(rr, P("#2b3040", 255, 6))
        c.restore()

def render_range(fmt, t_start, t_end, out):
    W, H = fmt_dims(fmt)
    surf = skia.Surface(W, H)
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", "-r", str(FPS), out], stdin=subprocess.PIPE)
    f0 = round(t_start * FPS); f1 = round(t_end * FPS)
    for f in range(f0, f1):
        T = f / FPS
        with surf as c:
            draw_frame(c, T, fmt)
        img = surf.makeImageSnapshot()
        arr = img.toarray(colorType=skia.kRGBA_8888_ColorType)
        ff.stdin.write(arr.tobytes())
    ff.stdin.close(); ff.wait()

def still(fmt, T, path, scale=1.0):
    W, H = fmt_dims(fmt)
    surf = skia.Surface(int(W * scale), int(H * scale))
    with surf as c:
        c.scale(scale, scale)
        draw_frame(c, T, fmt)
    surf.makeImageSnapshot().save(path)

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "range":
        render_range(sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), sys.argv[5])
    elif mode == "still":
        still(sys.argv[2], float(sys.argv[3]), sys.argv[4], float(sys.argv[5]) if len(sys.argv) > 5 else 1.0)
