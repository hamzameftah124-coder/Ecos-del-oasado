import skia, sys
from gfx import *
from scenes2 import draw_market, draw_fcity
W, H = 1280, 720
s = skia.Surface(W, H)
with s as c:
    c.clear(col("#000000"))
    c.save(); c.translate(W / 2, H / 2); c.scale(0.95, 0.95); c.translate(-2350, -560)
    draw_fcity(c, 1.3, 0.5, dict(sign="-60°C", snow=1.6, wind=2.0, dark=0.2))
    c.restore()
    rect(c, 0, 0, W, H, "#0a1a33", 70)
    # big frosty brothers
    c.save(); c.translate(300, 790); c.scale(1.6, 1.6)
    draw_kid(c, "J", -40, 0, 0.3, "stand", 1, "scared", (1, -0.3), 1.0, winter=1, frost=1.0, shiver=0.0)
    draw_kid(c, "L", 110, 30, 0.6, "stand", -1, "scared", (-1, -0.3), 1.0, winter=1, frost=1.0)
    c.restore()
    radial(c, 960, 300, 460, "#7fd0ff", 60)
    text(c, "-60°C", 1240, 250, 190, "#bfe8ff", align="right", stroke=26, stroke_color="#06121f")
    text(c, "30 DAYS", 1240, 410, 140, "#ffffff", align="right", stroke=24, stroke_color="#000000")
    rect(c, 640, 460, 610, 100, "#d8211c", r=20)
    text(c, "IN A SUPERMARKET", 945, 530, 50, "#ffffff")
s.makeImageSnapshot().save(sys.argv[1])
