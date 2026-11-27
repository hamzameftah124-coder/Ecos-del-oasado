import math, random, skia
from gfx import *
from screens import paper_bg, header, fit, label, check, cross
from screens2 import bar

def f_snowload(c, W, H, t, u, p, R):
    paper_bg(c, W, H, t); header(c, W, R, "HOW HEAVY IS SNOW?", t)
    c.save(); fit(c, R)
    for i, (lab, kg, colr, fr) in enumerate((("FRESH SNOW", "~100 kg", "#e8f2fa", 0.25), ("PACKED SNOW", "400+ kg", "#bcd2e6", 1.0))):
        x = 250 + i * 500; k = back_out(clamp((t - 0.3 - i * 0.6) * 2.5))
        c.save(); c.translate(x, 380); c.scale(k, k)
        poly(c, [(-130, -80), (60, -80), (130, -20), (130, 170), (-60, 170), (-130, 110)], colr)
        poly(c, [(-130, -80), (60, -80), (130, -20), (130, 170), (-60, 170), (-130, 110)], OUTLINE, stroke=6)
        line(c, -130, -80, -60, -20, OUTLINE, 5); line(c, -60, -20, 130, -20, OUTLINE, 5); line(c, -60, -20, -60, 170, OUTLINE, 5)
        c.restore()
        text(c, "1 m³", x, 230, 40, "#6b5a3a", font=FONT_BOLD)
        text(c, kg, x, 620, 58, "#e0523a" if i else "#2a6fb0")
        text(c, lab, x, 680, 36, "#2b2f3a", font=FONT_BOLD)
    c.restore()

def f_insulation(c, W, H, t, u, p, R):
    paper_bg(c, W, H, t); header(c, W, R, "SNOW IS 90% AIR", t)
    c.save(); fit(c, R)
    c.drawOval(skia.Rect.MakeLTRB(180, 220, 820, 700), P("#e6eef6")); c.drawOval(skia.Rect.MakeLTRB(180, 220, 820, 700), P(OUTLINE, 255, 7))
    c.drawOval(skia.Rect.MakeLTRB(330, 400, 670, 700), P("#f6e6c8")); c.drawOval(skia.Rect.MakeLTRB(330, 400, 670, 700), P(OUTLINE, 255, 5))
    rect(c, 60, 600, 880, 100, "#e8e0d0")
    rnd = random.Random(3)
    for k in range(40):
        a = rnd.uniform(0, math.tau); r = rnd.uniform(200, 300)
        x = 500 + math.cos(a) * r * 1.0; y = 460 + math.sin(a) * r * 0.75
        if y < 600: c.drawCircle(x, y, rnd.uniform(6, 12), P("#9fc8ff", 220, 3))
    k = clamp((t - 0.6) * 2)
    text(c, "-40°C", 120, 200, 64, "#2a4fb0", a=int(255 * k))
    text(c, "≈ 0°C", 500, 560, 64, "#e0523a", a=int(255 * clamp((t - 1.2) * 2)))
    c.restore()

def f_airhole(c, W, H, t, u, p, R):
    paper_bg(c, W, H, t); header(c, W, R, "ALWAYS MAKE AN AIR HOLE", t)
    c.save(); fit(c, R)
    c.drawOval(skia.Rect.MakeLTRB(200, 200, 800, 700), P("#e6eef6")); c.drawOval(skia.Rect.MakeLTRB(200, 200, 800, 700), P(OUTLINE, 255, 7))
    rect(c, 60, 600, 880, 100, "#e8e0d0")
    rect(c, 490, 200, 20, 120, "#3a5170")
    for k in range(4):
        ph = (t * 0.8 + k / 4) % 1
        text(c, "CO₂", 500 + math.sin(k) * 40, 520 - ph * 420, 34, "#7a8a9a", font=FONT_BOLD, a=int(255 * (1 - ph)))
    check(c, 600, 190, clamp((t - 0.8) * 3), 40)
    c.restore()

def f_circles(c, W, H, t, u, p, R):
    paper_bg(c, W, H, t); header(c, W, R, "LOST IN WHITE, YOU WALK IN CIRCLES", t, size=52)
    c.save(); fit(c, R)
    rect(c, 60, 80, 420, 540, "#f4f8fb", r=16); rect(c, 520, 80, 420, 540, "#f4f8fb", r=16)
    rect(c, 60, 80, 420, 540, OUTLINE, r=16, stroke=5); rect(c, 520, 80, 420, 540, OUTLINE, r=16, stroke=5)
    k = clamp(t / 2.5)
    pts = 60
    for i in range(int(pts * k)):
        a = i / pts * math.tau * 0.9
        x = 270 + math.sin(a) * 140; y = 560 - (1 - math.cos(a)) * 200 * 0.9
        circle(c, x, y, 7, "#e0523a")
    cross(c, 430, 130, clamp((t - 2.2) * 3), 34)
    line(c, 690, 600, 690, 100, "#3a3f4a", 10); line(c, 770, 600, 770, 100, "#3a3f4a", 10)
    for yy in range(110, 600, 50): rect(c, 680, yy, 100, 14, "#5a4a3a")
    for i in range(int(pts * k)):
        circle(c, 730, 580 - i * 8, 7, "#2a6fb0")
    check(c, 890, 130, clamp((t - 2.2) * 3), 34)
    label(c, "NO LANDMARK", 270, 660, 34); label(c, "FOLLOW THE RAILS", 730, 660, 34)
    c.restore()

def f_frost(c, W, H, t, u, p, R):
    paper_bg(c, W, H, t); header(c, W, R, "FROSTBITE: WHAT TO DO", t)
    c.save(); fit(c, R)
    rows = [("RUB IT WITH SNOW", False), ("PUT IT NEXT TO A FIRE", False), ("WARM IT SLOWLY WITH BODY HEAT", True)]
    for i, (s, ok) in enumerate(rows):
        k = clamp((t - 0.3 - i * 0.6) * 3)
        if k <= 0: continue
        y = 150 + i * 170
        rect(c, 80, y, 840, 120, "#ffffff", r=20); rect(c, 80, y, 840, 120, OUTLINE, r=20, stroke=5)
        (check if ok else cross)(c, 150, y + 60, k, 40)
        text(c, s, 220, y + 76, 40, "#2b2f3a", font=FONT_BOLD, align="left")
    c.restore()

def f_ground(c, W, H, t, u, p, R):
    paper_bg(c, W, H, t); header(c, W, R, "UNDERGROUND IS WARMER", t)
    c.save(); fit(c, R)
    rect(c, 60, 60, 880, 120, "#dfe8f1"); text(c, "AIR  -45°C", 500, 140, 50, "#2a4fb0")
    for i, colr in enumerate(("#8a6a4a", "#7a5a3a", "#6a4a2e", "#5a3e26")):
        rect(c, 60, 180 + i * 110, 880, 110, colr)
    k = ease(clamp((t - 0.3) / 1.6))
    rect(c, 440, 180, 120, 440 * k, "#2a3038")
    text(c, "STAYS STABLE ALL YEAR", 500, 560, 40, "#ffd77a", a=int(255 * clamp((t - 1.5) * 2)))
    c.restore()

def f_thaw(c, W, H, t, u, p, R):
    paper_bg(c, W, H, t); header(c, W, R, "+40°C IN 48 HOURS", t)
    c.save(); fit(c, R)
    k = clamp(t / 3.0)
    for i in range(6):
        x = 120 + i * 150
        rect(c, x, 120, 110, 260 * (1 - k), "#eef4fa"); rect(c, x, 120, 110, 260, OUTLINE, stroke=4)
    rect(c, 60, 620 - 260 * k, 880, 260 * k, "#5aa8e8", 200)
    rect(c, 60, 380, 880, 240, OUTLINE, stroke=5)
    text(c, "↓ WATER GOES DOWN ↓", 500, 470, 46, "#e0523a", a=int(255 * clamp((t - 1.5) * 2)))
    c.restore()

SCREENS3 = {"f_snowload": f_snowload, "f_insulation": f_insulation, "f_airhole": f_airhole, "f_circles": f_circles,
            "f_frost": f_frost, "f_ground": f_ground, "f_thaw": f_thaw}
