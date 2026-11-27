# Fact boards + day card for the frozen episode (English)
import math, random, skia
from gfx import *
from screens import paper_bg, header, fit, label, check, cross, scene_daycard

def bar(c, x, y, w, h, frac, colr, txt, tcol="#2b2f3a"):
    rect(c, x, y, w, h, "#e7d9b8", r=14); rect(c, x, y, w * clamp(frac), h, colr, r=14); rect(c, x, y, w, h, OUTLINE, r=14, stroke=5)
    text(c, txt, x + 20, y + h * 0.68, h * 0.5, tcol, font=FONT_BOLD, align="left")

def f_frostbite(c, W, H, t, u, p, R):
    paper_bg(c, W, H, t); header(c, W, R, "TIME UNTIL SKIN FREEZES", t)
    c.save(); fit(c, R)
    rows = [("-28°C", 1.0, "30 min", "#4aa8e8"), ("-40°C", 0.45, "10 min", "#6c8fe0"), ("-48°C", 0.22, "5 min", "#e0a52a"), ("-55°C", 0.08, "under 2 min", "#e0523a")]
    for i, (tt, fr, lab, colr) in enumerate(rows):
        k = ease(clamp((t - 0.3 - i * 0.45) / 0.6))
        text(c, tt, 160, 150 + i * 140, 50, colr, align="right")
        bar(c, 190, 105 + i * 140, 760, 70, fr * k, colr, lab if k > 0.3 else "", "#2b2f3a")
    text(c, "with wind, uncovered skin", 500, 690, 36, "#6b5a3a", font=FONT_BOLD)
    c.restore()

def f_water(c, W, H, t, u, p, R):
    paper_bg(c, W, H, t); header(c, W, R, "WATER STEALS HEAT", t)
    c.save(); fit(c, R)
    for i, (lab, n, colr) in enumerate((("AIR", 1, "#9fc8ff"), ("WATER", 25, "#2a6fb0"))):
        x = 250 + i * 500
        rect(c, x - 180, 120, 360, 440, colr, 90 if i == 0 else 150, r=30); rect(c, x - 180, 120, 360, 440, OUTLINE, r=30, stroke=6)
        circle(c, x, 260, 50, "#f2c59c"); circle(c, x, 260, 50, OUTLINE, stroke=5); rect(c, x - 45, 310, 90, 150, "#d2452f", r=20)
        k = ease(clamp((t - 0.4 - i * 0.6) / 0.8))
        for a in range(min(int(n * k), 25) if i else (1 if k > 0 else 0)):
            ang = a / 25 * math.tau + t
            line(c, x + math.cos(ang) * 90, 330 + math.sin(ang) * 120, x + math.cos(ang) * 150, 330 + math.sin(ang) * 170, "#e0523a", 6)
        text(c, lab, x, 620, 54, "#2b2f3a")
        text(c, f"{n}x", x, 200, 70, "#e0523a" if i else "#2b2f3a")
    c.restore()

def f_layers(c, W, H, t, u, p, R):
    paper_bg(c, W, H, t); header(c, W, R, "COTTON KILLS", t)
    c.save(); fit(c, R)
    for i, (lab, colr) in enumerate((("COTTON", "#c9c2b0"), ("WOOL + LAYERS", "#7a5a9a"))):
        x = 250 + i * 500
        poly(c, [(x - 150, 160), (x + 150, 160), (x + 190, 520), (x - 190, 520)], colr); poly(c, [(x - 150, 160), (x + 150, 160), (x + 190, 520), (x - 190, 520)], OUTLINE, stroke=6)
        if i == 0:
            for k in range(10):
                yy = 200 + ((t * 80 + k * 37) % 300)
                path = skia.Path(); xx = x - 120 + k * 26; path.moveTo(xx, yy - 18); path.quadTo(xx + 10, yy, xx, yy + 5); path.quadTo(xx - 10, yy, xx, yy - 18)
                c.drawPath(path, P("#3d8bd9"))
            text(c, "WET = COLD", x, 600, 40, "#e0523a")
            cross(c, x + 150, 160, clamp((t - 0.5) * 3), 40)
        else:
            rnd = random.Random(2)
            for k in range(26): c.drawCircle(x + rnd.uniform(-150, 150), rnd.uniform(190, 500), rnd.uniform(10, 20), P("#ffffff", 200, 4))
            text(c, "TRAPPED AIR = WARM", x, 600, 40, "#2a6fb0")
            check(c, x + 150, 160, clamp((t - 1.0) * 3), 40)
        text(c, lab, x, 120, 44, "#2b2f3a")
    c.restore()

def f_metal(c, W, H, t, u, p, R):
    paper_bg(c, W, H, t); header(c, W, R, "FROZEN METAL GRABS SKIN", t)
    c.save(); fit(c, R)
    rect(c, 420, 120, 160, 480, "#9aa3ad", r=20); rect(c, 420, 120, 160, 480, OUTLINE, r=20, stroke=6)
    k = ease(clamp(t / 1.2))
    hx = lerp(150, 330, k)
    rect(c, hx - 120, 300, 220, 120, "#f2c59c", r=50); rect(c, hx - 120, 300, 220, 120, OUTLINE, r=50, stroke=6)
    if k >= 1:
        rnd = random.Random(1)
        for i in range(14):
            yy = 300 + rnd.uniform(0, 120); xx = 410 + rnd.uniform(-10, 14)
            line(c, xx - 12, yy, xx + 12, yy, "#7fd0ff", 5); line(c, xx, yy - 12, xx, yy + 12, "#7fd0ff", 5)
        text(c, "MOISTURE FREEZES", 760, 330, 40, "#2a6fb0"); text(c, "= ICE GLUE", 760, 390, 40, "#2a6fb0")
    text(c, "-40°C", 500, 680, 54, "#e0523a")
    c.restore()

def f_calories(c, W, H, t, u, p, R):
    paper_bg(c, W, H, t); header(c, W, R, "THE COLD EATS CALORIES", t)
    c.save(); fit(c, R)
    k1 = ease(clamp((t - 0.3) / 0.8)); k2 = ease(clamp((t - 0.9) / 1.2))
    text(c, "NORMAL DAY", 60, 220, 44, "#2b2f3a", font=FONT_BOLD, align="left"); bar(c, 60, 250, 880, 90, 0.5 * k1, "#4caf6e", "~2,500 kcal")
    text(c, "EXTREME COLD", 60, 450, 44, "#e0523a", font=FONT_BOLD, align="left"); bar(c, 60, 480, 880, 90, 1.0 * k2, "#e0523a", "up to 2x", "#ffffff" if k2 > 0.4 else "#2b2f3a")
    c.restore()

def f_freezer(c, W, H, t, u, p, R):
    paper_bg(c, W, H, t); header(c, W, R, "THE WARMEST ROOM", t)
    c.save(); fit(c, R)
    for i, (lab, temp, fr, colr) in enumerate((("STREET", "-60°C", 0.05, "#2a4fb0"), ("STORE", "-35°C", 0.35, "#3d8bd9"), ("FREEZER", "-18°C", 0.62, "#e0a52a"))):
        x = 180 + i * 320; k = ease(clamp((t - 0.3 - i * 0.5) / 0.7))
        rect(c, x - 40, 140, 80, 380, "#ffffff", r=40); rect(c, x - 40, 140, 80, 380, OUTLINE, r=40, stroke=6)
        circle(c, x, 520, 55, colr); circle(c, x, 520, 55, OUTLINE, stroke=6)
        hh = 340 * fr * k; rect(c, x - 18, 500 - hh, 36, hh + 10, colr, r=14)
        text(c, temp, x, 120, 50, colr); text(c, lab, x, 650, 42, "#2b2f3a")
    if t > 2.0:
        check(c, 820, 200, clamp((t - 2.0) * 3), 40)
    c.restore()

def f_co(c, W, H, t, u, p, R):
    paper_bg(c, W, H, t); header(c, W, R, "CARBON MONOXIDE", t)
    c.save(); fit(c, R)
    for k in range(5):
        ph = (t * 0.3 + k / 5) % 1
        oval(c, 500 + math.sin(k * 2 + t) * 200, 380 - ph * 200, 160 + ph * 120, 60 + ph * 30, "#8a8f98", int(120 * (1 - ph)))
    items = [("NO COLOR", 200), ("NO SMELL", 500), ("NO SOUND", 800)]
    for i, (lab, x) in enumerate(items):
        kk = clamp((t - 0.4 - i * 0.4) * 3)
        if kk <= 0: continue
        circle(c, x, 260, 80, "#ffffff"); circle(c, x, 260, 80, OUTLINE, stroke=6)
        if i == 0: oval(c, x, 260, 46, 26, "#2b2f3a", stroke=8); circle(c, x, 260, 12, "#2b2f3a")
        elif i == 1: poly(c, [(x, 210), (x - 20, 290), (x + 20, 290)], "#f2c59c"); poly(c, [(x, 210), (x - 20, 290), (x + 20, 290)], OUTLINE, stroke=6)
        else: poly(c, [(x - 40, 240), (x - 15, 240), (x + 15, 215), (x + 15, 305), (x - 15, 280), (x - 40, 280)], "#2b2f3a")
        line(c, x - 60, 200, x + 60, 320, "#e0523a", 10)
        label(c, lab, x, 390, 40)
    steps = ["HEADACHE", "SLEEPY", "UNCONSCIOUS"]
    for i, s in enumerate(steps):
        kk = clamp((t - 1.8 - i * 0.5) * 3)
        if kk <= 0: continue
        rect(c, 80 + i * 300, 480, 260, 90, ["#e0a52a", "#ef7d3a", "#e0523a"][i], r=18)
        text(c, s, 210 + i * 300, 540, 36, "#ffffff")
        if i < 2: text(c, "→", 355 + i * 300, 545, 50, "#2b2f3a")
    c.restore()

def f_snow(c, W, H, t, u, p, R):
    paper_bg(c, W, H, t); header(c, W, R, "NEVER EAT SNOW", t)
    c.save(); fit(c, R)
    # left: snow into mouth (X)
    circle(c, 250, 320, 120, "#f2c59c"); circle(c, 250, 320, 120, OUTLINE, stroke=6); oval(c, 290, 360, 30, 20, "#5a1f22")
    for k in range(6): circle(c, 340 + k * 14, 370 - k * 10, 10, "#ffffff"); 
    text(c, "LOSES BODY HEAT", 250, 520, 36, "#e0523a"); cross(c, 360, 200, clamp((t - 0.5) * 3), 42)
    # right: pot melting
    rect(c, 640, 280, 240, 140, "#9aa3ad", r=20); rect(c, 640, 280, 240, 140, OUTLINE, r=20, stroke=6)
    for k in range(3):
        fl = 30 + 10 * math.sin(t * 15 + k); poly(c, [(690 + k * 70, 440), (705 + k * 70, 440 - fl + 60), (720 + k * 70, 440)], "#5ab0ff")
    for k in range(3):
        ph = (t * 0.6 + k / 3) % 1; circle(c, 700 + k * 60, 260 - ph * 120, 16 + ph * 20, "#dfe8f1", int(160 * (1 - ph)))
    text(c, "MELT IT FIRST", 760, 520, 36, "#2a6fb0"); check(c, 880, 220, clamp((t - 1.2) * 3), 42)
    c.restore()

def f_hypo(c, W, H, t, u, p, R):
    paper_bg(c, W, H, t); header(c, W, R, "WHEN SHIVERING STOPS", t)
    c.save(); fit(c, R)
    rect(c, 120, 80, 90, 520, "#ffffff", r=45); rect(c, 120, 80, 90, 520, OUTLINE, r=45, stroke=6)
    circle(c, 165, 600, 70, "#e0523a"); circle(c, 165, 600, 70, OUTLINE, stroke=6)
    rows = [("37°C", "NORMAL", 0.95, "#4caf6e"), ("35°C", "SHIVERING", 0.72, "#e0a52a"), ("32°C", "SHIVERING STOPS", 0.45, "#e0523a"), ("28°C", "UNCONSCIOUS", 0.2, "#7a1f2a")]
    T = clamp((t - 0.3) / 2.6)
    level = lerp(0.95, 0.45, ease(T))
    hh = 460 * level; rect(c, 145, 560 - hh, 40, hh + 20, "#e0523a", r=18)
    for i, (tt, lab, lv, colr) in enumerate(rows):
        y = 560 - 460 * lv
        kk = clamp((t - 0.3 - i * 0.6) * 3)
        if kk <= 0: continue
        line(c, 215, y, 290, y, colr, 8)
        text(c, tt, 310, y + 18, 50, colr, align="left")
        text(c, lab, 470, y + 16, 44, colr if i == 2 else "#2b2f3a", font=FONT_BOLD, align="left")
    c.restore()

def f_battery(c, W, H, t, u, p, R):
    paper_bg(c, W, H, t); header(c, W, R, "COLD KILLS BATTERIES", t)
    c.save(); fit(c, R)
    for i, (lab, keep, colr) in enumerate((("OUTSIDE  -50°C", 1 - clamp(t / 1.6) * 0.85, "#e0523a"), ("IN YOUR JACKET", 0.95, "#4caf6e"))):
        x = 250 + i * 500
        rect(c, x - 110, 160, 220, 380, "#ffffff", r=24); rect(c, x - 110, 160, 220, 380, OUTLINE, r=24, stroke=8); rect(c, x - 40, 130, 80, 34, OUTLINE, r=8)
        hh = 340 * keep; rect(c, x - 90, 520 - hh, 180, hh, colr, r=14)
        text(c, lab, x, 620, 40, "#2b2f3a")
    c.restore()

def f_route(c, W, H, t, u, p, R):
    paper_bg(c, W, H, t); header(c, W, R, "8 KM AT -50°C", t)
    c.save(); fit(c, R)
    rect(c, 60, 60, 880, 560, "#eef3f7", r=16); rect(c, 60, 60, 880, 560, OUTLINE, r=16, stroke=6)
    for k in range(6): line(c, 60 + k * 170, 60, 60 + k * 170, 620, "#c9d6e2", 4)
    rect(c, 110, 480, 160, 100, "#c0392b", r=10); label(c, "MARKET", 190, 545, 30, "#ffffff")
    rect(c, 720, 90, 180, 110, "#7a5a48", r=10); label(c, "STATION", 810, 158, 30, "#ffffff")
    k = clamp((t - 0.3) / 2.2)
    for i in range(20):
        f = i / 20
        if f > k: break
        circle(c, lerp(270, 720, f), lerp(500, 180, f) + math.sin(f * 9) * 30, 8, "#2a6fb0")
    text(c, "≈ 2 HOURS ON FOOT", 500, 690, 40, "#e0523a")
    c.restore()

def daycard_t(c, W, H, t, u, p, R):
    scene_daycard(c, W, H, t, u, p, R)
    if "temp" in p:
        k = back_out(clamp((t - 0.25) * 3))
        c.save(); c.translate(W / 2, H * (0.42 if H > W else 0.48) + 420 * min(W, H) / 1080); c.scale(k, k)
        text(c, p["temp"], 0, 0, 96 * min(W, H) / 1080, "#7fd0ff", stroke=16, stroke_color="#000000")
        c.restore()

SCREENS2 = {"f_frostbite": f_frostbite, "f_water": f_water, "f_layers": f_layers, "f_metal": f_metal, "f_calories": f_calories,
            "f_freezer": f_freezer, "f_co": f_co, "f_snow": f_snow, "f_hypo": f_hypo, "f_battery": f_battery, "f_route": f_route,
            "dayT": daycard_t}

def tbc(c, W, H, t, u, p, R):
    lin_grad(c, 0, 0, W, H, "#05070c", "#121826")
    k = back_out(clamp(t * 2.5))
    c.save(); c.translate(W / 2, H * 0.47); c.scale(k, k)
    text(c, "TO BE", 0, -10, 130 * min(W, H) / 1080, "#ffffff", stroke=20, stroke_color="#000000")
    text(c, "CONTINUED", 0, 140 * min(W, H) / 1080, 130 * min(W, H) / 1080, "#7fd0ff", stroke=20, stroke_color="#000000")
    c.restore()
SCREENS2["tbc"] = tbc
