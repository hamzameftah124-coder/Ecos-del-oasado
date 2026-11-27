import skia, sys, subprocess, math
from gfx import *
W, H, FPS, DUR = 1080, 1920, 30, 2.4
ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                       "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p", sys.argv[1]], stdin=subprocess.PIPE)
surf = skia.Surface(W, H)
for f in range(int(DUR * FPS)):
    t = f / FPS
    with surf as c:
        lin_grad(c, 0, 0, W, H, "#0d0e14", "#2a1418")
        radial(c, W / 2, H * 0.45, 700, "#ff2a1a", 80)
        k = back_out(clamp(t * 3))
        c.save(); c.translate(W / 2, H * 0.40); c.scale(k, k)
        text(c, "FULL STORY", 0, 0, 120, "#ffffff", stroke=20, stroke_color="#000000")
        text(c, "ON THE CHANNEL", 0, 140, 92, "#ffd400", stroke=18, stroke_color="#000000")
        c.restore()
        c.save(); c.translate(W / 2 - 180, H * 0.66); c.scale(0.7, 0.7); draw_roach(c, 0, 0, t, 1, 1.0, walking=True, speed=0.8); c.restore()
    ff.stdin.write(surf.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType).tobytes())
ff.stdin.close(); ff.wait()
