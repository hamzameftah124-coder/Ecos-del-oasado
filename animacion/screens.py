# Screen-space scenes: roulette, title cards, fact boards (infographics), end card.
import math, random, skia
from gfx import *

def paper_bg(c, W, H, t):
    lin_grad(c, 0, 0, W, H, "#f4e7c8", "#e9d6ab")
    for y in range(0, H, 48): line(c, 0, y, W, y, "#d9c290", 2, 160)
    for x in range(0, W, 48): line(c, x, 0, x, H, "#e2cfa0", 1, 120)
    rect(c, 0, 0, W, H, "#7a5a2a", 30, stroke=40)

def header(c, W, R, s, t, size=None):
    size = size or 62
    y = R["y"] - size * 0.45
    sc = back_out(clamp(t * 4))
    c.save(); c.translate(W / 2, y); c.scale(sc, sc)
    w = measure(s, size) + 60
    rect(c, -w / 2, -size * 0.95, w, size * 1.3, "#2b2f3a", r=18)
    text(c, s, 0, 0, size, "#ffd400")
    c.restore()

H_GLOBAL = [1920]

def fit(c, R, dw=1000, dh=700):
    s = min(R["w"] / dw, R["h"] / dh)
    c.translate(R["x"] + (R["w"] - dw * s) / 2, R["y"] + (R["h"] - dh * s) / 2)
    c.scale(s, s)

def label(c, s, x, y, size=44, color="#2b2f3a", a=255):
    text(c, s, x, y, size, color, font=FONT_BOLD, a=a)

def check(c, x, y, u, size=40):
    if u <= 0: return
    sc = back_out(clamp(u))
    c.save(); c.translate(x, y); c.scale(sc, sc)
    circle(c, 0, 0, size, "#4caf6e"); circle(c, 0, 0, size, OUTLINE, stroke=5)
    poly(c, [(-18, 0), (-5, 14), (20, -14)], "#ffffff", stroke=9, close=False)
    c.restore()

def cross(c, x, y, u, size=40):
    if u <= 0: return
    sc = back_out(clamp(u))
    c.save(); c.translate(x, y); c.scale(sc, sc)
    circle(c, 0, 0, size, "#e0523a"); circle(c, 0, 0, size, OUTLINE, stroke=5)
    line(c, -14, -14, 14, 14, "#ffffff", 9); line(c, 14, -14, -14, 14, "#ffffff", 9)
    c.restore()

# ----------------------------------------------------------------------------- roulette
ROUL = [("mosquito", "#5aa9e6"), ("cucaracha", "#e0523a"), ("araña", "#9b6be0"), ("hormiga", "#4caf6e"),
        ("avispa", "#f2b632"), ("escorpión", "#e07a3a"), ("ciempiés", "#3fb6b0"), ("polilla", "#d86aa8")]

def icon_bug(c, kind, s=1.0, t=0.0):
    c.save(); c.scale(s, s)
    if kind == "cucaracha":
        c.save(); c.scale(0.16, 0.16); c.translate(0, 60); draw_roach(c, -20, 0, t, 1, 1.0); c.restore()
    elif kind == "mosquito":
        oval(c, 0, 0, 34, 10, "#3b3f4a"); circle(c, 34, -4, 10, "#3b3f4a"); line(c, 40, 0, 70, 14, OUTLINE, 4)
        oval(c, -4, -18, 26, 9, "#d8ecf5"); oval(c, 6, -16, 24, 8, "#d8ecf5")
    elif kind == "araña":
        circle(c, 0, 0, 22, "#2b2b33"); circle(c, 22, -6, 12, "#2b2b33")
        for k in range(4):
            for sgn in (-1, 1): line(c, 0, 0, -10 + k * 12, sgn * 38, "#2b2b33", 5)
    elif kind == "hormiga":
        for i, r in enumerate((12, 9, 15)): circle(c, -26 + i * 24, 0, r, "#3a2a22")
        for i in range(3): line(c, -6 + i * 8, 0, -16 + i * 14, 24, "#3a2a22", 4)
    elif kind == "avispa":
        oval(c, 0, 0, 30, 18, "#f2c232"); line(c, -8, -16, -8, 16, OUTLINE, 6); line(c, 8, -16, 8, 16, OUTLINE, 6); circle(c, 32, -2, 10, OUTLINE)
        oval(c, -2, -22, 20, 9, "#d8ecf5")
    elif kind == "escorpión":
        oval(c, 0, 10, 26, 12, "#a2562a"); path = skia.Path(); path.moveTo(-24, 8); path.quadTo(-60, -40, -14, -36)
        c.drawPath(path, P("#a2562a", 255, 10)); circle(c, 30, 2, 10, "#a2562a")
    elif kind == "ciempiés":
        for i in range(6): circle(c, -40 + i * 16, math.sin(i) * 4, 9, "#7a3a2a"); line(c, -40 + i * 16, 0, -40 + i * 16, 18, "#7a3a2a", 3)
    else:
        oval(c, 0, 0, 14, 22, "#a89070"); oval(c, -20, -6, 22, 16, "#d8c8a8"); oval(c, 20, -6, 22, 16, "#d8c8a8")
    c.restore()

def scene_roulette(c, W, H, t, u, p, R):
    lin_grad(c, 0, 0, W, H, "#0d0e14", "#1c1a24")
    radial(c, W / 2, H * 0.42, max(W, H) * 0.6, "#5a2a2a", 90)
    for i in range(24):
        a = i / 24 * math.tau + t * 0.3
        line(c, W / 2, H / 2, W / 2 + math.cos(a) * 2000, H / 2 + math.sin(a) * 2000, "#ffffff", 30, 5)
    cx, cy = W / 2, H * (0.40 if H > W else 0.47)
    r = min(W, H) * (0.40 if H > W else 0.36)
    # spin: decelerate to land on cucaracha (index 1) under pointer at top
    n = len(ROUL); seg = math.tau / n
    total = p.get("dur", 4.3)
    k = clamp(t / total)
    target = -math.pi / 2 - (1 + 0.5) * seg + 6 * math.tau  # angle so that segment 1 center is at top
    ang = target * (1 - (1 - k) ** 3)
    circle(c, cx, cy + 14, r + 30, "#000000", 90)
    circle(c, cx, cy, r + 26, "#f2c232"); circle(c, cx, cy, r + 26, OUTLINE, stroke=10)
    for i, (name, colr) in enumerate(ROUL):
        a0 = ang + i * seg
        path = skia.Path(); path.moveTo(cx, cy)
        path.arcTo(skia.Rect.MakeLTRB(cx - r, cy - r, cx + r, cy + r), math.degrees(a0), math.degrees(seg), False); path.close()
        c.drawPath(path, P(colr)); c.drawPath(path, P(OUTLINE, 255, 6))
        am = a0 + seg / 2
        c.save(); c.translate(cx + math.cos(am) * r * 0.66, cy + math.sin(am) * r * 0.66); c.rotate(math.degrees(am) + 90)
        icon_bug(c, name, r / 260, t)
        c.restore()
    circle(c, cx, cy, r * 0.16, "#2b2f3a"); circle(c, cx, cy, r * 0.16, OUTLINE, stroke=8); circle(c, cx, cy, r * 0.06, "#f2c232")
    # bulbs
    for i in range(16):
        a = i / 16 * math.tau
        on = (int(t * 8) + i) % 2 == 0
        circle(c, cx + math.cos(a) * (r + 13), cy + math.sin(a) * (r + 13), 9, "#fff6c8" if on else "#a07a2a")
    # pointer
    poly(c, [(cx - 40, cy - r - 70), (cx + 40, cy - r - 70), (cx, cy - r + 20)], "#ffffff"); poly(c, [(cx - 40, cy - r - 70), (cx + 40, cy - r - 70), (cx, cy - r + 20)], OUTLINE, stroke=8)
    if t > total:
        # winner flash + big icon + label at top (subtitle hidden while label shows)
        k2 = clamp((t - total) * 3)
        rect(c, 0, 0, W, H, "#ffffff", int(120 * (1 - k2)))
        sc = back_out(k2)
        c.save(); c.translate(W / 2, cy + r + (190 if H > W else 120)); c.scale(sc, sc)
        text(c, "¡CUCARACHA!", 0, 0, 120 if H > W else 110, "#ffd400", stroke=22, stroke_color=OUTLINE)
        c.restore()

def scene_luck(c, W, H, t, u, p, R):
    # two brothers silhouettes on hill under moon, slow push
    lin_grad(c, 0, 0, W, H, "#1c1e2c", "#6a4e4c")
    rnd = random.Random(1)
    for _ in range(90): circle(c, rnd.uniform(0, W), rnd.uniform(0, H * 0.6), rnd.uniform(1, 3), "#ffffff", int(rnd.uniform(80, 230)))
    s = 1 + u * 0.08
    c.save(); c.translate(W / 2, H * 0.62); c.scale(s, s)
    circle(c, 0, -H * 0.18, min(W, H) * 0.22, "#f4efd8"); radial(c, 0, -H * 0.18, min(W, H) * 0.5, "#f4efd8", 60)
    oval(c, 0, 260, W * 0.9, 300, "#1b1f2e")
    k = min(W, H) / 1080
    draw_kid(c, "J", -90 * k, 0, t, "idle", -1, "worried", (-1, 0), 1.25 * k)
    draw_kid(c, "L", 90 * k, 0, t + 0.5, "idle", -1, "worried", (-1, 0), 1.25 * k)
    c.restore()

def scene_daycard(c, W, H, t, u, p, R):
    lin_grad(c, 0, 0, W, H, "#141824", "#232a3d")
    n = p["day"]
    k = back_out(clamp(t * 3))
    cx, cy = W / 2, H * (0.42 if H > W else 0.48)
    s = min(W, H) / 1080
    c.save(); c.translate(cx, cy); c.rotate(-4 + 2 * math.sin(t)); c.scale(k * s, k * s)
    rect(c, -260, -300, 520, 600, "#f4efe4", r=30); rect(c, -260, -300, 520, 600, OUTLINE, r=30, stroke=10)
    rect(c, -260, -300, 520, 140, "#e0523a", r=30); rect(c, -260, -200, 520, 40, "#e0523a")
    text(c, "DÍA", 0, -200, 90, "#ffffff")
    text(c, str(n), 0, 170, 300, "#2b2f3a")
    for i in (-1, 1): circle(c, i * 140, -300, 24, "#2b2f3a")
    c.restore()
    # torn previous page flying
    if t < 0.6:
        c.save(); c.translate(cx + t * 1500, cy - t * 600); c.rotate(t * 90); c.scale(s, s)
        rect(c, -260, -300, 520, 600, "#f4efe4", int(255 * (1 - t / 0.6)), r=30)
        text(c, str(n - 1), 0, 170, 300, "#2b2f3a", a=int(255 * (1 - t / 0.6)))
        c.restore()

# ----------------------------------------------------------------------------- facts
def fact_habitat(c, W, H, t, u, p, R):
    paper_bg(c, W, H, t); header(c, W, R, "SU LUGAR FAVORITO", t)
    c.save(); fit(c, R)
    c.save(); c.translate(430, 560); c.scale(0.55, 0.55); draw_roach(c, -20, 0, t, 1, 1.0, walking=False, ant_amp=0.5); c.restore()
    items = [("OSCURO", 170, 150, "moon"), ("CÁLIDO", 500, 110, "heat"), ("HÚMEDO", 830, 150, "drop")]
    for i, (s, x, y, ic) in enumerate(items):
        k = clamp((t - 0.4 - i * 0.7) * 3)
        if k <= 0: continue
        sc = back_out(k)
        c.save(); c.translate(x, y); c.scale(sc, sc)
        circle(c, 0, 0, 90, "#ffffff"); circle(c, 0, 0, 90, OUTLINE, stroke=6)
        if ic == "moon":
            circle(c, 0, 0, 50, "#2b2f3a"); circle(c, 20, -14, 44, "#ffffff")
        elif ic == "heat":
            rect(c, -14, -56, 28, 90, "#ffffff", r=14); rect(c, -14, -56, 28, 90, OUTLINE, r=14, stroke=5)
            circle(c, 0, 40, 26, "#e0523a"); rect(c, -6, -30, 12, 70, "#e0523a")
        else:
            path = skia.Path(); path.moveTo(0, -56); path.quadTo(46, 10, 0, 50); path.quadTo(-46, 10, 0, -56)
            c.drawPath(path, P("#4aa8e8")); c.drawPath(path, P(OUTLINE, 255, 5))
        c.restore()
        label(c, s, x, y + 140, 44, a=int(255 * k))
        check(c, x + 70, y - 60, clamp((t - 0.7 - i * 0.7) * 3), 30)
    c.restore()

def fact_food(c, W, H, t, u, p, R):
    paper_bg(c, W, H, t); header(c, W, R, "COMEN CASI DE TODO", t)
    c.save(); fit(c, R)
    c.save(); c.translate(500, 420); c.scale(0.5, 0.5); draw_roach(c, -20, 0, t, 1, 1.0, walking=True, speed=0.3); c.restore()
    items = [("RESTOS", 150, 140), ("MIGAS", 850, 140), ("GRASA", 150, 560), ("PAPEL", 850, 560)]
    for i, (s, x, y) in enumerate(items):
        k = clamp((t - 0.2 - i * 0.55) * 3)
        if k <= 0: continue
        sc = back_out(k)
        c.save(); c.translate(x, y); c.scale(sc, sc)
        circle(c, 0, 0, 80, "#ffffff"); circle(c, 0, 0, 80, OUTLINE, stroke=6)
        if s == "RESTOS":
            oval(c, 0, 10, 50, 22, "#e8e2d2"); circle(c, -10, 0, 14, "#d8473a"); circle(c, 14, 4, 12, "#6aa84f")
        elif s == "MIGAS":
            for j in range(6): rect(c, -40 + (j % 3) * 30, -20 + (j // 3) * 30, 18, 16, "#e3b061", r=4)
        elif s == "GRASA":
            path = skia.Path(); path.moveTo(0, -46); path.quadTo(40, 10, 0, 40); path.quadTo(-40, 10, 0, -46)
            c.drawPath(path, P("#d8b13a")); c.drawPath(path, P(OUTLINE, 255, 5))
        else:
            poly(c, [(-36, -44), (24, -44), (40, -28), (40, 46), (-36, 46)], "#ffffff"); poly(c, [(-36, -44), (24, -44), (40, -28), (40, 46), (-36, 46)], OUTLINE, stroke=5)
            for j in range(4): line(c, -24, -20 + j * 16, 26, -20 + j * 16, "#9aa1a8", 4)
        c.restore()
        label(c, s, x, y + 125 if y < 300 else y - 100, 40, a=int(255 * k))
        # dotted arrow to roach
        if k >= 1:
            line(c, x + (80 if x < 500 else -80), y, lerp(x, 500, 0.45), lerp(y, 380, 0.45), "#2b2f3a", 6, 140)
    c.restore()

def fact_paradise(c, W, H, t, u, p, R):
    paper_bg(c, W, H, t); header(c, W, R, "PARA ELLA: UN PARAÍSO", t)
    c.save(); fit(c, R)
    # little kitchen drawing with sparkle + roach with heart eyes
    rect(c, 140, 220, 720, 420, "#cfd8dc", r=20); rect(c, 140, 220, 720, 420, OUTLINE, r=20, stroke=6)
    for i in range(3): draw_stove(c, 190 + i * 210, 620, 180, 220, dust=False)
    c.save(); c.translate(500, 360); c.scale(0.3, 0.3); draw_roach(c, 0, 0, t, 1, 1.0); c.restore()
    for i in range(6):
        a = i / 6 * math.tau + t
        x = 500 + math.cos(a) * 330; y = 360 + math.sin(a) * 160
        sc = 0.6 + 0.4 * math.sin(t * 6 + i)
        poly(c, [(x, y - 30 * sc), (x + 8 * sc, y - 8 * sc), (x + 30 * sc, y), (x + 8 * sc, y + 8 * sc), (x, y + 30 * sc), (x - 8 * sc, y + 8 * sc), (x - 30 * sc, y), (x - 8 * sc, y - 8 * sc)], "#ffd400")
    c.restore()

def fact_flatten(c, W, H, t, u, p, R):
    paper_bg(c, W, H, t); header(c, W, R, "SE APLANA", t)
    c.save(); fit(c, R)
    # two blocks with narrow gap; roach squashes through
    rect(c, 80, 120, 840, 180, "#9aa3ad", r=10); rect(c, 80, 120, 840, 180, OUTLINE, r=10, stroke=6)
    rect(c, 80, 380, 840, 220, "#9aa3ad", r=10); rect(c, 80, 380, 840, 220, OUTLINE, r=10, stroke=6)
    rect(c, 80, 300, 840, 80, "#2b2f3a")
    k = clamp(t / max(p.get("dur", 3), 0.1))
    x = lerp(-150, 900, ease(k))
    flat = clamp(1 - abs(x - 500) / 380) * 0.9 + (0.0)
    flat = 0.75 if 80 < x < 920 else 0.0
    c.save(); c.translate(x, 380); c.scale(0.45, 0.45); draw_roach(c, 0, 0, t, 1, 1.0, flat=flat, walking=True); c.restore()
    # height arrows
    line(c, 960, 300, 960, 380, "#e0523a", 8); poly(c, [(945, 310), (975, 310), (960, 290)], "#e0523a"); poly(c, [(945, 370), (975, 370), (960, 390)], "#e0523a")
    label(c, "¡HUECO MUY FINO!", 500, 680, 44, "#e0523a")
    c.restore()

def fact_nocturnal(c, W, H, t, u, p, R):
    paper_bg(c, W, H, t); header(c, W, R, "HUYEN DE LA LUZ", t)
    c.save(); fit(c, R)
    rect(c, 60, 80, 440, 520, "#ffe9a8", r=24); rect(c, 500, 80, 440, 520, "#2b2f4a", r=24)
    rect(c, 60, 80, 880, 520, OUTLINE, r=24, stroke=6)
    circle(c, 200, 200, 60, "#ffc93c");
    for i in range(8):
        a = i / 8 * math.tau + t
        line(c, 200 + math.cos(a) * 80, 200 + math.sin(a) * 80, 200 + math.cos(a) * 110, 200 + math.sin(a) * 110, "#ffc93c", 8)
    circle(c, 820, 190, 50, "#f4efd8"); circle(c, 845, 175, 45, "#2b2f4a")
    k = clamp(t / max(p.get("dur", 3), 0.1))
    x = lerp(260, 740, ease(k * 1.3))
    c.save(); c.translate(x, 520); c.scale(0.38, 0.38); draw_roach(c, 0, 0, t, 1, 1.0, walking=k < 0.75, speed=2); c.restore()
    label(c, "DÍA", 280, 660, 44); label(c, "NOCHE", 720, 660, 44)
    c.restore()

def fact_cerci(c, W, H, t, u, p, R):
    paper_bg(c, W, H, t); header(c, W, R, "SENSORES DE AIRE", t)
    c.save(); fit(c, R)
    c.save(); c.translate(560, 450); c.scale(0.8, 0.8); draw_roach(c, 0, 0, t, 1, 1.0, show_cerci=True, ant_amp=0.4); c.restore()
    # air waves from left
    for i in range(4):
        ph = (t * 0.8 + i / 4) % 1
        x = lerp(-20, 300, ph)
        path = skia.Path(); path.moveTo(x, 260)
        path.quadTo(x + 40, 340, x, 420); path.quadTo(x - 40, 500, x, 580)
        c.drawPath(path, P("#4aa8e8", int(255 * (1 - ph)), 8))
    if (t % 1.0) > 0.75 or t > 1.6:
        c.drawCircle(340, 395, 60 + 10 * math.sin(t * 10), P("#ffd400", 255, 8))
    label(c, "CERCOS", 340, 250, 44, "#e0523a")
    label(c, "notan cada corriente", 500, 680, 40)
    c.restore()

def fact_reaction(c, W, H, t, u, p, R):
    paper_bg(c, W, H, t); header(c, W, R, "TIEMPO DE REACCIÓN", t)
    c.save(); fit(c, R)
    k1 = ease(clamp((t - 0.3) / 1.2)); k2 = ease(clamp((t - 0.3) / 0.25))
    label(c, "TU PARPADEO", 60, 210, 44);
    rect(c, 60, 240, 880, 90, "#e7d9b8", r=14); rect(c, 60, 240, 880 * k1, 90, "#4aa8e8", r=14); rect(c, 60, 240, 880, 90, OUTLINE, r=14, stroke=5)
    text(c, "100 – 400 ms", 500, 302, 48, "#ffffff" if k1 > 0.6 else "#2b2f3a", font=FONT_BOLD)
    text(c, "CUCARACHA", 60, 440, 44, "#e0523a", font=FONT_BOLD, align="left")
    rect(c, 60, 470, 880, 90, "#e7d9b8", r=14); rect(c, 60, 470, 110 * k2, 90, "#e0523a", r=14); rect(c, 60, 470, 880, 90, OUTLINE, r=14, stroke=5)
    text(c, "menos de 50 ms", 200, 532, 48, "#2b2f3a", font=FONT_BOLD, align="left")
    c.save(); c.translate(130, 470); c.scale(0.12, 0.12); c.restore()
    c.restore()
    for lab in ():
        pass

def fact_water(c, W, H, t, u, p, R):
    paper_bg(c, W, H, t); header(c, W, R, "¿CUÁNTO AGUANTA?", t)
    c.save(); fit(c, R)
    k1 = ease(clamp((t - 0.3) / 1.4)); k2 = ease(clamp((t - 1.2) / 0.5))
    # food icon
    oval(c, 110, 260, 60, 30, "#e8e2d2"); circle(c, 95, 250, 16, "#d8473a"); circle(c, 125, 252, 14, "#6aa84f")
    label(c, "SIN COMER", 500, 200, 44)
    rect(c, 200, 225, 740, 80, "#e7d9b8", r=14); rect(c, 200, 225, 740 * k1, 80, "#4caf6e", r=14); rect(c, 200, 225, 740, 80, OUTLINE, r=14, stroke=5)
    text(c, "SEMANAS", 570, 282, 48, "#ffffff" if k1 > 0.5 else "#2b2f3a")
    path = skia.Path(); path.moveTo(110, 430); path.quadTo(160, 500, 110, 540); path.quadTo(60, 500, 110, 430)
    c.drawPath(path, P("#4aa8e8")); c.drawPath(path, P(OUTLINE, 255, 5))
    label(c, "SIN AGUA", 500, 430, 44, "#e0523a")
    rect(c, 200, 455, 740, 80, "#e7d9b8", r=14); rect(c, 200, 455, 170 * k2, 80, "#e0523a", r=14); rect(c, 200, 455, 740, 80, OUTLINE, r=14, stroke=5)
    text(c, "DÍAS", 400, 512, 48, "#2b2f3a", align="left")
    c.restore()

def fact_plan(c, W, H, t, u, p, R):
    paper_bg(c, W, H, t); header(c, W, R, "EL PLAN", t)
    c.save(); fit(c, R)
    # top-down map
    rect(c, 60, 60, 880, 560, "#efe2c0", r=16); rect(c, 60, 60, 880, 560, OUTLINE, r=16, stroke=6)
    rect(c, 80, 80, 200, 160, "#c9a46a", r=10); label(c, "DESPENSA", 180, 175, 32)
    rect(c, 720, 80, 200, 140, "#d9dde0", r=10); label(c, "NEVERA", 820, 165, 32)
    circle(c, 760, 300, 26, "#4aa8e8")
    rect(c, 700, 440, 220, 150, "#a9b2bd", r=10);
    k = clamp((t - 0.4) / 2.0)
    # roach icon moves from door to bowl
    pos = (lerp(300, 780, ease(k)), lerp(200, 500, ease(k)))
    # path dashed
    for i in range(12):
        f = i / 12
        if f > k: break
        circle(c, lerp(300, 780, f), lerp(200, 500, f), 7, "#e0523a")
    circle(c, 810, 515, 30, "#4aa8e8"); circle(c, 810, 515, 30, OUTLINE, stroke=4)
    for bx in (760, 860): rect(c, bx - 12, 500, 24, 20, "#e3b061", r=4)
    c.save(); c.translate(pos[0], pos[1]); c.scale(0.12, 0.12); draw_roach(c, 0, 80, t, 1, 1.0); c.restore()
    label(c, "AGUA + PAN", 810, 420, 32, "#2a6fb0")
    c.restore()

def fact_recap(c, W, H, t, u, p, R):
    paper_bg(c, W, H, t); header(c, W, R, "LO QUE HIZO", t)
    c.save(); fit(c, R)
    items = [("Se escondió", "hide"), ("Huyó de la luz", "light"), ("Se apartó", "away"), ("Nunca atacó", "noatk")]
    for i, (s, ic) in enumerate(items):
        x = 60 + (i % 2) * 460; y = 60 + (i // 2) * 300
        k = clamp((t - i * 0.5) * 3)
        if k <= 0: continue
        c.save(); c.translate(x, y)
        rect(c, 0, 0, 420, 260, "#ffffff", int(255 * k), r=20); rect(c, 0, 0, 420, 260, OUTLINE, int(255 * k), r=20, stroke=5)
        c.save(); c.translate(150, 170); c.scale(0.18, 0.18)
        draw_roach(c, 0, 0, t, -1 if ic in ("light", "away") else 1, 1.0, flat=0.3 if ic == "hide" else 0)
        c.restore()
        label(c, s, 210, 240, 36, a=int(255 * k))
        check(c, 370, 50, clamp((t - i * 0.5 - 0.25) * 3), 30)
        c.restore()
    c.restore()

def fact_bacteria(c, W, H, t, u, p, R):
    paper_bg(c, W, H, t); header(c, W, R, "BACTERIAS EN LAS PATAS", t)
    c.save(); fit(c, R)
    c.save(); c.translate(330, 470); c.scale(0.55, 0.55); draw_roach(c, 0, 0, t, 1, 1.0); c.restore()
    k = back_out(clamp((t - 0.4) * 2))
    c.save(); c.translate(720, 320); c.scale(k, k)
    circle(c, 0, 0, 200, "#ffffff");
    line(c, -40, -150, 40, 160, "#6b2e14", 40)
    rnd = random.Random(2)
    for i in range(22):
        bx = rnd.uniform(-150, 150); by = rnd.uniform(-150, 150)
        if bx * bx + by * by < 170 ** 2:
            c.save(); c.translate(bx, by); c.rotate(rnd.uniform(0, 180) + t * 30)
            rect(c, -16, -7, 32, 14, ["#6ac46a", "#9b6be0", "#f2b632"][i % 3], r=7)
            c.restore()
    circle(c, 0, 0, 200, OUTLINE, stroke=14)
    c.restore()
    line(c, 250, 440, 560, 470, OUTLINE, 18)  # magnifier handle-ish
    label(c, "¡lávate las manos y limpia la cocina!", 500, 680, 38, "#2a6fb0")
    c.restore()

def scene_endcard(c, W, H, t, u, p, R):
    lin_grad(c, 0, 0, W, H, "#1f2a44", "#3a2a4a")
    s = min(W, H) / 1080
    cx = W / 2; cy = R["y"] + R["h"] * 0.42
    k = back_out(clamp(t * 2.5))
    c.save(); c.translate(cx, cy); c.scale(k * s, k * s)
    rect(c, -380, -230, 760, 400, "#ffffff", r=50); rect(c, -380, -230, 760, 400, OUTLINE, r=50, stroke=10)
    poly(c, [(-200, 160), (-260, 300), (-80, 170)], "#ffffff"); poly(c, [(-200, 168), (-260, 300), (-80, 172)], OUTLINE, stroke=10, close=False)
    for i in range(3):
        circle(c, -140 + i * 140, -30 + math.sin(t * 5 + i) * 12, 34, "#2b2f3a")
    c.restore()
    c.save(); c.translate(cx, cy + 260 * s); c.scale(0.25 * s, 0.25 * s); draw_roach(c, 0, 0, t, 1, 1.0, walking=True, speed=0.5); c.restore()

def scene_split(c, W, H, t, u, p, R, draw_world):
    """split: left pantry (Leo), right kitchen (Javier + antennae)."""
    pass

def scene_clock(c, W, H, t, u, p, R):
    lin_grad(c, 0, 0, W, H, "#1e2433", "#2b3346")
    cx, cy = W / 2, R["y"] + R["h"] * 0.45; r = min(W, R["h"]) * 0.36
    circle(c, cx, cy, r + 20, "#c9a46a"); circle(c, cx, cy, r, "#f4efe4"); circle(c, cx, cy, r, OUTLINE, stroke=12)
    for i in range(12):
        a = i / 12 * math.tau
        line(c, cx + math.cos(a) * r * 0.82, cy + math.sin(a) * r * 0.82, cx + math.cos(a) * r * 0.92, cy + math.sin(a) * r * 0.92, OUTLINE, 10)
    T = p.get("_T", t) - p.get("t0", 0)
    sp = 1 + T * T * 3
    am = -math.pi / 2 + T * sp * 2.5; ah = -math.pi / 2 + T * sp * 0.21
    line(c, cx, cy, cx + math.cos(ah) * r * 0.5, cy + math.sin(ah) * r * 0.5, OUTLINE, 18)
    line(c, cx, cy, cx + math.cos(am) * r * 0.78, cy + math.sin(am) * r * 0.78, "#e0523a", 12)
    circle(c, cx, cy, 18, OUTLINE)

def scene_nosafe(c, W, H, t, u, p, R):
    paper_bg(c, W, H, t); header(c, W, R, "NINGÚN LUGAR SEGURO", t)
    c.save(); fit(c, R)
    T = p.get("_T", t) - p.get("t0", 0)
    marks = p.get("marks", [0.3, 1.8, 2.9])
    for i, (s, x) in enumerate((("PARED", 180), ("ESCONDITE", 500), ("RINCÓN", 820))):
        c.save(); c.translate(x, 330)
        rect(c, -130, -150, 260, 260, "#ffffff", r=20); rect(c, -130, -150, 260, 260, OUTLINE, r=20, stroke=6)
        if i == 0:
            for yy in range(-120, 90, 50):
                for xx in range(-110, 110, 70): rect(c, xx + (25 if (yy // 50) % 2 else 0), yy, 60, 40, "#c9734a", r=4)
        elif i == 1:
            draw_sack(c, 0, 90, 0.9)
        else:
            poly(c, [(-110, -130), (-110, 90), (110, 90)], "#9aa3ad"); poly(c, [(-110, -130), (-110, 90), (110, 90)], OUTLINE, stroke=6)
        c.restore()
        label(c, s, x, 560, 42)
        cross(c, x + 100, 200, clamp((T - marks[i]) * 3), 44)
    c.restore()

SCREENS = {"clock": scene_clock, "nosafe": scene_nosafe, "roulette": scene_roulette, "luck": scene_luck, "daycard": scene_daycard,
           "f_habitat": fact_habitat, "f_food": fact_food, "f_paradise": fact_paradise, "f_flatten": fact_flatten,
           "f_nocturnal": fact_nocturnal, "f_cerci": fact_cerci, "f_reaction": fact_reaction, "f_water": fact_water,
           "f_plan": fact_plan, "f_recap": fact_recap, "f_bacteria": fact_bacteria, "endcard": scene_endcard}
