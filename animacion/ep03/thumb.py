import skia, sys
from gfx import *
from scenes3 import draw_station
W, H = 1280, 720
s = skia.Surface(W, H)
with s as c:
    c.clear(col("#000000"))
    c.save(); c.translate(W / 2, H / 2); c.scale(0.62, 0.62); c.translate(-1500, -560)
    draw_station(c, 1.0, 0.45, dict(bend=1.0, dust=True, collapse=True, dark=0.2,
        chars=[dict(who="J", x=1650, pose="run", expr="scared", winter=1, scale=1.25), dict(who="L", x=1420, pose="run", expr="scared", winter=1, scale=1.25, toff=0.3)]))
    c.restore()
    rect(c, 0, 0, W, H, "#000000", 40)
    radial(c, 1000, 520, 420, "#ff2a1a", 70)
    text(c, "IT'S", 1240, 470, 120, "#ffffff", align="right", stroke=22, stroke_color="#000000")
    text(c, "FALLING", 1240, 600, 130, "#ffd400", align="right", stroke=24, stroke_color="#000000")
    rect(c, 40, 40, 270, 96, "#d8211c", r=20); text(c, "PART 2", 175, 110, 64, "#ffffff")
s.makeImageSnapshot().save(sys.argv[1])
