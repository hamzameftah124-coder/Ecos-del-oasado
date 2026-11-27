import sys, json, skia, traceback
import render
from gfx import *
fmt = sys.argv[1]; out = sys.argv[2]
ids = None if len(sys.argv) < 4 else [int(x) for x in sys.argv[3].split(",")]
SH = render.SHOTS if ids is None else [render.SHOTS[i] for i in ids]
W, H = render.fmt_dims(fmt)
sc = 0.2 if fmt == "h" else 0.16
tw, th = int(W * sc), int(H * sc)
cols = 8 if fmt == "h" else 12
pages = [SH[i:i + (cols * 7 if fmt == "h" else cols * 5)] for i in range(0, len(SH), cols * 7 if fmt == "h" else cols * 5)]
errs = 0
for pi, page in enumerate(pages):
    rows = (len(page) + cols - 1) // cols
    surf = skia.Surface(cols * (tw + 12) + 12, 70 + rows * (th + 52) + 12)
    with surf as c:
        c.clear(col("#1b1e26"))
        text(c, f"Hoja de contactos {'16:9 YouTube' if fmt=='h' else '9:16 vertical'} — página {pi+1}/{len(pages)}", 16, 46, 32, "#ffffff", align="left")
        for k, sh in enumerate(page):
            x = 12 + (k % cols) * (tw + 12); y = 70 + (k // cols) * (th + 52)
            T = sh["t0"] + (sh["t1"] - sh["t0"]) * 0.6
            ts = skia.Surface(tw, th)
            try:
                with ts as c2:
                    c2.scale(sc, sc); render.draw_frame(c2, T, fmt)
                c.drawImage(ts.makeImageSnapshot(), x, y)
            except Exception as e:
                errs += 1; print("ERR shot", sh["id"], sh["sc"], e); traceback.print_exc(limit=2)
                rect(c, x, y, tw, th, "#802020")
            m = int(T // 60); s = T % 60
            text(c, f"#{sh['id']}  {m}:{s:04.1f}  {sh['t1']-sh['t0']:.1f}s", x, y + th + 30, 20, "#cfd6e4", font=FONT_BOLD, align="left")
    surf.makeImageSnapshot().save(f"{out}_{pi+1}.png")
print("pages", len(pages), "errors", errs)
