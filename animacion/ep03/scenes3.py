# Worlds for Part 2: station interior (roof collapse), snow cave, metro (crowd).
import math, random, skia
from gfx import *
from scenes import overlays, anim_x
from scenes2 import kid, snowfall, icicles, draw_fcity

FLOOR = 1000
PCOLS = ["#7a4a8a", "#3a7a6a", "#a0603a", "#4a5a9a", "#8a3a3a", "#5a7a3a", "#9a8a3a", "#3a6a9a"]

def person(c, x, y, colr, s=1.0, t=0.0, face=1, hat="#2b2f3a", sit=False, kidsize=False):
    c.save(); c.translate(x, y); c.scale(s * face * (0.8 if kidsize else 1.0), s * (0.8 if kidsize else 1.0))
    bob = math.sin(t * 2 + x) * 2
    if not sit:
        line(c, -12, -150, -14, -10, OUTLINE, 30); line(c, 12, -150, 14, -10, OUTLINE, 30)
        line(c, -12, -150, -14, -10, "#2b3442", 22); line(c, 12, -150, 14, -10, "#2b3442", 22)
        body_y = -150
    else:
        line(c, -10, -60, 50, -20, OUTLINE, 30); line(c, -10, -60, 50, -20, "#2b3442", 22)
        body_y = -60
    path = skia.Path(); path.moveTo(-42, body_y + 10); path.lineTo(-46, body_y - 120 + bob); path.quadTo(0, body_y - 150 + bob, 46, body_y - 120 + bob); path.lineTo(42, body_y + 10); path.close()
    c.drawPath(path, P(colr)); c.drawPath(path, P(OUTLINE, 255, 6))
    hy = body_y - 175 + bob
    circle(c, 0, hy, 46, OUTLINE); circle(c, 0, hy, 41, "#e8b996")
    bp = skia.Path(); bp.moveTo(-46, hy - 4); bp.quadTo(-44, hy - 60, 0, hy - 60); bp.quadTo(44, hy - 60, 46, hy - 4); bp.close()
    c.drawPath(bp, P(hat)); c.drawPath(bp, P(OUTLINE, 255, 5))
    circle(c, 14, hy + 4, 5, OUTLINE); circle(c, 30, hy + 4, 5, OUTLINE)
    c.restore()

def fire_barrel(c, x, y, t, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    rect(c, -55, -140, 110, 140, "#5a5048", r=8); rect(c, -55, -140, 110, 140, OUTLINE, r=8, stroke=6)
    for yy in (-110, -50): line(c, -55, yy, 55, yy, "#3a342e", 6)
    for k in range(5):
        fl = 50 + 25 * math.sin(t * 9 + k * 1.7)
        poly(c, [(-45 + k * 22, -140), (-34 + k * 22, -140 - fl), (-23 + k * 22, -140)], ["#ffb33a", "#ff7a2a", "#ffd65a"][k % 3])
    c.restore()

# ------------------------------------------------------------------ station interior
SCAM = {"wide": (1700, 600, 3400, 1300), "bench": (650, 820, 1000, 700), "bear": (1500, 930, 520, 360), "roof": (1700, 260, 2400, 900),
        "mid": (1700, 700, 1600, 1000), "doors": (3150, 740, 900, 820), "barrel": (1100, 820, 760, 620), "leo": (900, 780, 640, 600)}

def draw_station(c, t, u, p):
    lin_grad(c, -3000, -800, 10000, 1800, "#6a4a3e", "#4a3430")
    for x in range(-200, 4000, 160):
        for y in range(200, 1000, 60):
            rect(c, x + (80 if (y // 60) % 2 else 0), y, 150, 52, "#7a5444", 200)
    for k in range(4):
        wx = 300 + k * 850
        rect(c, wx, 300, 400, 380, "#1a2230"); poly(c, [(wx, 300), (wx + 200, 200), (wx + 400, 300)], "#1a2230")
        rect(c, wx, 300, 400, 380, OUTLINE, stroke=10)
        snowfall(c, t, wx, wx + 400, 200, 680, 0.25, 1.5, k)
    rect(c, -3000, FLOOR, 10000, 1500, "#4a4440"); line(c, -3000, FLOOR, 7000, FLOOR, OUTLINE, 8)
    # roof trusses that bend
    bend = p.get("bend", 0.0)
    if isinstance(bend, (list, tuple)): bend = lerp(bend[0], bend[1], ease(u))
    shake = p.get("rshake", 0.0)
    for k in range(5):
        x0 = -100 + k * 800
        sag = bend * 160 + math.sin(t * 30 + k) * shake * 8
        path = skia.Path(); path.moveTo(x0, 170); path.quadTo(x0 + 400, 170 + sag * 2, x0 + 800, 170)
        c.drawPath(path, P(OUTLINE, 255, 50)); c.drawPath(path, P("#8a939e", 255, 38))
        for j in range(1, 8):
            xx = x0 + j * 100; yy = 170 + sag * 2 * (1 - ((j - 4) / 4) ** 2)
            line(c, xx, yy, xx + 50, 40, OUTLINE, 18); line(c, xx, yy, xx + 50, 40, "#8a939e", 12)
    rect(c, -3000, -800, 10000, 830, "#2a2f38"); rect(c, -3000, 0, 10000, 40, "#dfe8f1", 220)
    if bend > 0.5:
        rnd = random.Random(3)
        for k in range(8):
            x = rnd.uniform(200, 3200)
            poly(c, [(x, 40), (x + 20, 90), (x - 10, 140), (x + 15, 200)], OUTLINE, stroke=5, close=False)
    if p.get("dust"):
        rnd = random.Random(int(t * 3))
        for k in range(30):
            x = rnd.uniform(0, 3400); y = 60 + ((t * 300 + rnd.uniform(0, 900)) % 900)
            circle(c, x, y, rnd.uniform(3, 8), "#d8d0c4", 160)
    # benches with blankets, barrels, cans, teddy
    for bx in (300, 1800):
        rect(c, bx, 860, 560, 30, "#8a5a3a", r=6); rect(c, bx + 20, 890, 20, 110, "#5a3a2a"); rect(c, bx + 520, 890, 20, 110, "#5a3a2a")
        rect(c, bx + 40, 820, 220, 50, "#b04a4a", r=14); rect(c, bx + 300, 825, 200, 45, "#4a6ab0", r=14)
    fire_barrel(c, 1150, FLOOR, t); fire_barrel(c, 2600, FLOOR, t + 1)
    for k in range(4): draw_can(c, 1350 + k * 70, FLOOR - 5 + (k % 2) * 8, 0.6, ["#d8473a", "#3d8bd9", "#e0a52a", "#4caf6e"][k])
    # teddy bear
    tx, ty = 1520, FLOOR - 10
    oval(c, tx, ty - 40, 40, 45, "#a0703a"); circle(c, tx, ty - 105, 32, "#a0703a"); circle(c, tx - 26, ty - 130, 12, "#a0703a"); circle(c, tx + 26, ty - 130, 12, "#a0703a")
    circle(c, tx - 10, ty - 108, 5, OUTLINE); circle(c, tx + 10, ty - 108, 5, OUTLINE)
    # exit doors
    rect(c, 3000, 520, 320, 480, "#3a2c26"); rect(c, 3000, 520, 320, 480, OUTLINE, stroke=8)
    lin_grad(c, 3010, 530, 300, 460, "#c9d6e2", "#eef3f7", a0=160, a1=160)
    for ch in p.get("chars", []):
        kid(c, t, u, ch, FLOOR)
    # collapse
    col_ = p.get("collapse")
    if col_:
        k = clamp(u * 1.4)
        rnd = random.Random(8)
        for i in range(18):
            x = rnd.uniform(0, 3000); y = -100 + (k ** 2) * rnd.uniform(800, 1300)
            poly(c, [(x, y), (x + rnd.uniform(60, 160), y + 20), (x + 120, y + rnd.uniform(60, 140)), (x - 20, y + 80)], rnd.choice(["#eef4fa", "#7a838e", "#dfe8f1"]))
        rect(c, -5000, -5000, 15000, 15000, "#ffffff", int(230 * clamp((u - 0.6) * 3)))
    overlays(c, t, u, p)
    lights = [("glow", 1150, 820, 700, 0.9), ("glow", 2600, 820, 700, 0.9), ("rect", 3010, 530, 300, 460, 0.6)]
    darkness(c, 0, 0, p.get("dark", 0.35), lights, color="#0a0608")
    radial(c, 1150, 830, 500, "#ffb36a", 50); radial(c, 2600, 830, 500, "#ffb36a", 50)

# ------------------------------------------------------------------ snow cave cross-section
CCAM = {"wide": (900, 680, 1700, 1000), "inside": (950, 830, 760, 520), "hole": (950, 470, 560, 420), "dig": (700, 800, 900, 640)}

def draw_cave(c, t, u, p):
    lin_grad(c, -3000, -1500, 8000, 2400, "#0a1222", "#22324e")
    rnd = random.Random(2)
    for _ in range(60): circle(c, rnd.uniform(-500, 2500), rnd.uniform(-300, 500), rnd.uniform(1, 3), "#ffffff", 180)
    rect(c, -3000, FLOOR, 8000, 1500, "#c8d5e4")
    b = p.get("build", 1.0)
    if isinstance(b, (list, tuple)): b = lerp(b[0], b[1], ease(u))
    # mound
    R = 520 * b
    c.drawOval(skia.Rect.MakeLTRB(950 - R * 1.1, FLOOR - R * 0.9, 950 + R * 1.1, FLOOR + R * 0.9), P("#e6eef6"))
    c.drawOval(skia.Rect.MakeLTRB(950 - R * 1.1, FLOOR - R * 0.9, 950 + R * 1.1, FLOOR + R * 0.9), P(OUTLINE, 255, 8))
    rect(c, -3000, FLOOR, 8000, 1500, "#c8d5e4")
    dug = p.get("dug", 1.0)
    if isinstance(dug, (list, tuple)): dug = lerp(dug[0], dug[1], ease(u))
    if b > 0.9 and dug > 0:
        # chamber cross-section + tunnel
        r2 = 330 * dug
        c.drawOval(skia.Rect.MakeLTRB(950 - r2, FLOOR - r2 * 0.75, 950 + r2, FLOOR + 40), P("#3a5170"))
        c.drawOval(skia.Rect.MakeLTRB(950 - r2, FLOOR - r2 * 0.75, 950 + r2, FLOOR + 40), P(OUTLINE, 255, 6))
        rect(c, 950 - r2 - 400 * dug, FLOOR - 90, 400 * dug + 20, 90, "#3a5170"); line(c, 950 - r2 - 400 * dug, FLOOR - 90, 950 - r2, FLOOR - 90, OUTLINE, 6)
        rect(c, 600, FLOOR - 10, 700, 20, "#b08a5a")
    if p.get("hole"):
        rect(c, 940, FLOOR - 420 * 0.9 - 40, 20, 200, "#3a5170")
        for i in range(3):
            ph = (t * 0.6 + i / 3) % 1
            oval(c, 950 + ph * 30, FLOOR - 470 - ph * 120, 16 + ph * 26, 10 + ph * 18, "#eef6ff", int(150 * (1 - ph)))
    for ch in p.get("chars", []):
        kid(c, t, u, ch, FLOOR)
    if p.get("candle"):
        rect(c, 935, FLOOR - 70, 30, 60, "#f4efe4"); poly(c, [(943, FLOOR - 70), (950, FLOOR - 100 - 6 * math.sin(t * 12)), (957, FLOOR - 70)], "#ffc84a")
    overlays(c, t, u, p)
    snowfall(c, t, -800, 2600, -400, 1000, p.get("snow", 0.5), 2.0)
    lights = [("glow", 950, FLOOR - 100, 500, 0.85)] if p.get("candle") else []
    darkness(c, 0, 0, p.get("dark", 0.35), lights, color="#050a16")
    if p.get("candle"): radial(c, 950, FLOOR - 90, 330, "#ffc84a", 60)

# ------------------------------------------------------------------ metro platform with survivors
MCAM3 = {"wide": (1700, 650, 3200, 1200), "crowd": (1500, 780, 1400, 900), "radio": (2450, 800, 900, 700), "brothers": (1000, 800, 820, 700),
         "wall": (2900, 560, 1000, 900), "stairs": (330, 650, 900, 900), "woman": (1250, 780, 700, 640)}

def draw_metro(c, t, u, p):
    lin_grad(c, -3000, -800, 10000, 1800, "#5a6a6e", "#3e4a4e")
    for x in range(-200, 4000, 80):
        for y in range(160, 860, 40):
            rect(c, x + 2, y + 2, 76, 36, "#d8dcd2" if (x // 80 + y // 40) % 7 else "#c9a43c", 70, r=3)
    rect(c, -3000, -800, 10000, 900, "#2a3034")
    # tunnel mouth
    path = skia.Path(); path.moveTo(3050, FLOOR); path.lineTo(3050, 500); path.quadTo(3300, 300, 3550, 500); path.lineTo(3550, FLOOR); path.close()
    c.drawPath(path, P("#07090b")); c.drawPath(path, P(OUTLINE, 255, 8))
    # stairs at left
    for k in range(8): rect(c, 100 + k * 50, 400 + k * 75, 400, 75, "#8a9096"); rect(c, 100 + k * 50, 400 + k * 75, 400, 75, OUTLINE, stroke=4)
    rect(c, -3000, FLOOR, 10000, 1500, "#6e6a62"); rect(c, -3000, FLOOR + 160, 10000, 40, "#e0c040")
    line(c, -3000, FLOOR, 7000, FLOOR, OUTLINE, 8)
    # water creeping
    w = p.get("water", 0)
    if w:
        for k in range(12):
            x = 600 + k * 260
            ph = (t * 0.8 + k * 0.13) % 1
            line(c, x, 160, x + math.sin(k) * 10, 160 + ph * 700, "#7fc8ff", 6, int(200 * w))
        rect(c, -3000, FLOOR - 30 * w, 10000, 40 * w, "#5aa8e8", int(160 * w))
    # camp: blankets, tents, barrels
    for k, x in enumerate((700, 1500, 2300)):
        poly(c, [(x - 160, FLOOR), (x, FLOOR - 220), (x + 160, FLOOR)], PCOLS[k + 2]); poly(c, [(x - 160, FLOOR), (x, FLOOR - 220), (x + 160, FLOOR)], OUTLINE, stroke=6)
    fire_barrel(c, 1100, FLOOR, t, 0.9); fire_barrel(c, 1950, FLOOR, t + 2, 0.9); fire_barrel(c, 2750, FLOOR, t + 1, 0.9)
    if p.get("radio_table"):
        rect(c, 2300, 860, 300, 20, "#8a5a3a"); rect(c, 2320, 880, 16, 120, "#5a3a2a"); rect(c, 2564, 880, 16, 120, "#5a3a2a")
        rect(c, 2380, 780, 140, 80, "#7a5a3a", r=12); rect(c, 2380, 780, 140, 80, OUTLINE, r=12, stroke=5)
    rnd = random.Random(6)
    crowd = p.get("crowd", 1.0)
    for k in range(int(26 * crowd)):
        x = 500 + rnd.uniform(0, 2500); sz = rnd.uniform(0.6, 0.85)
        if abs(x - p.get("gap", -999)) < 250: continue
        person(c, x, FLOOR - rnd.uniform(0, 10), rnd.choice(PCOLS), sz, t + k, rnd.choice((-1, 1)), rnd.choice(["#2b2f3a", "#c0392b", "#e8b33a", "#3a5fc0"]),
               sit=rnd.random() < 0.4, kidsize=rnd.random() < 0.2)
    if p.get("woman"):
        wx = p["woman"]; person(c, wx, FLOOR, "#8a4aa0", 1.0, t, -1, "#e8e2d2")
    for ch in p.get("chars", []):
        kid(c, t, u, ch, FLOOR)
    overlays(c, t, u, p)
    lights = [("glow", 1100, 830, 650, 0.9), ("glow", 1950, 830, 650, 0.9), ("glow", 2750, 830, 650, 0.9), ("glow", 330, 400, 500, 0.5)]
    darkness(c, 0, 0, p.get("dark", 0.4), lights, color="#06080c")
    for x in (1100, 1950, 2750): radial(c, x, 840, 460, "#ffb36a", 45)

WORLDS3 = {"station": (draw_station, SCAM), "cave": (draw_cave, CCAM), "metro": (draw_metro, MCAM3)}
