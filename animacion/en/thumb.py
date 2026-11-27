import skia, sys
from gfx import *
from scenes import draw_kitchen
W, H = 1280, 720
s = skia.Surface(W, H)
with s as c:
    c.clear(col("#000000"))
    c.save()
    sc = 1.35
    c.translate(W / 2, H / 2); c.scale(sc * 0.62, sc * 0.62); c.translate(-1330, -700)
    p = dict(light="dark", pots="floor", roach=dict(x=1700, face=-1, scale=1.05, rz=0.9, amp=0.6),
             chars=[dict(who="L", x=700, face=1, expr="scared", flashlight=True, beam=-4, look=(1, 0), scale=1.15)])
    draw_kitchen(c, 0.7, 0.5, p)
    c.restore()
    # vignette
    pnt = skia.Paint(); pnt.setShader(skia.GradientShader.MakeRadial(skia.Point(W * 0.62, H * 0.5), 900, [col("#000000", 0), col("#000000", 200)]))
    c.drawRect(skia.Rect.MakeWH(W, H), pnt)
    # red glow behind text
    radial(c, 1000, 150, 420, "#ff2a1a", 70)
    text(c, "DON'T", 1245, 150, 150, "#ffffff", align="right", stroke=24, stroke_color="#000000")
    text(c, "MOVE.", 1245, 290, 150, "#ffd400", align="right", stroke=24, stroke_color="#000000")
    rect(c, 770, 320, 475, 96, "#d8211c", r=20)
    text(c, "IT FEELS YOU", 1007, 388, 56, "#ffffff")
s.makeImageSnapshot().save(sys.argv[1])
