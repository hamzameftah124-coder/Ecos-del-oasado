# Worlds for "Frozen Supermarket": frozen city, supermarket interior, walk-in freezer.
import math, random, skia
from gfx import *
from scenes import overlays, anim_x, city_skyline, draw_car

FLOOR = 1000

def kid(c, t, u, ch, y_default):
    x = anim_x(ch, u)
    rot = ch.get("rot", 0)
    if "rot1" in ch: rot = lerp(rot, ch["rot1"], ease_out(clamp(u * ch.get("rspeed", 1.0))))
    y = ch.get("y", y_default)
    if "y1" in ch: y = lerp(y, ch["y1"], ease(u))
    draw_kid(c, ch["who"], x, y, t + ch.get("toff", 0), ch.get("pose", "stand"), ch.get("face", 1), ch.get("expr", "neutral"),
             ch.get("look", (1, 0)), ch.get("scale", 1.0), ch.get("flashlight", False), ch.get("on", True), ch.get("carry"), rot,
             winter=ch.get("winter", 1), goggles=ch.get("goggles", False), shiver=ch.get("shiver", 0.0), frost=ch.get("frost", 0.0))
    if ch.get("breath", True) and rot == 0:
        s = KIDS[ch["who"]]["h"] * ch.get("scale", 1.0)
        mx = x + 40 * s * ch.get("face", 1); my = y - 175 * s
        for i in range(3):
            ph = (t * 0.7 + i / 3 + ch.get("toff", 0)) % 1
            oval(c, mx + ch.get("face", 1) * ph * 120 * s, my - ph * 40 * s, (14 + ph * 40) * s, (10 + ph * 26) * s, "#eef6ff", int(150 * (1 - ph)))

def snowfall(c, t, x0, x1, y0, y1, amount=1.0, wind=1.0, seed=1):
    rnd = random.Random(seed)
    n = int(160 * amount)
    for i in range(n):
        sx = rnd.uniform(x0, x1); sp = rnd.uniform(120, 320); r = rnd.uniform(3, 9)
        yy = y0 + ((rnd.uniform(0, 1) * (y1 - y0) + t * sp) % (y1 - y0))
        xx = sx + (t * sp * 0.6 * wind) % (x1 - x0) - (x1 - x0) * ((sx + t * sp * 0.6 * wind - x0) // (x1 - x0)) * 0
        xx = x0 + ((sx - x0 + t * sp * 0.6 * wind) % (x1 - x0))
        circle(c, xx, yy, r, "#ffffff", int(rnd.uniform(120, 230)))

def icicles(c, x0, x1, y, seed=3, scale=1.0):
    rnd = random.Random(seed)
    x = x0
    while x < x1:
        L = rnd.uniform(20, 90) * scale; w = rnd.uniform(8, 18) * scale
        poly(c, [(x, y), (x + w, y), (x + w / 2, y + L)], "#dff3ff", 230)
        x += w + rnd.uniform(4, 30) * scale

def frost_edges(c, x, y, w, h, amt):
    if amt <= 0: return
    p = skia.Paint(AntiAlias=True)
    for (cx, cy) in ((x, y), (x + w, y), (x, y + h), (x + w, y + h)):
        radial(c, cx, cy, 700, "#e6f4ff", int(140 * amt))

# ------------------------------------------------------------------ frozen city exterior
FCAM = {"wide": (1600, 600, 2800, 1300), "sign": (650, 470, 760, 640), "market": (2350, 650, 1300, 1000), "street": (1200, 820, 1600, 800),
        "station": (4300, 620, 1600, 1100), "steps": (4300, 960, 1200, 520), "walk": (1300, 780, 1300, 900), "doors": (2350, 760, 800, 700),
        "cars": (900, 900, 1200, 560), "sky": (1800, 250, 2400, 1000)}

def draw_fcity(c, t, u, p):
    white = p.get("mood") == "white"
    if white:
        lin_grad(c, -3000, -1500, 10000, 2600, "#c9d6e2", "#eef3f7")
    else:
        lin_grad(c, -3000, -1500, 10000, 2600, "#0c1424", "#33476a")
    city_skyline(c, t, 820, day=white, seed=11)
    # snow caps + icicles on skyline
    # street with deep snow
    rect(c, -3000, 820, 10000, 1200, "#dfe8f1" if white else "#9fb0c6")
    for k in range(18):
        oval(c, -1000 + k * 380, 840, 260, 40, "#eef4fa" if white else "#b4c3d6")
    # gas station thermometer sign
    rect(c, 430, 250, 440, 260, "#1b1f27", r=16); rect(c, 430, 250, 440, 260, OUTLINE, r=16, stroke=8)
    rect(c, 640, 510, 20, 330, "#3a3f4a")
    temp = p.get("sign", "-60°C")
    text(c, temp, 650, 425, 130, "#ff5a3c" if not white else "#ffb43c", font=FONT_BLACK)
    # buried cars
    for cx, col_ in ((800, "#c4544a"), (1350, "#4a78b8"), (3200, "#5d8f5a")):
        draw_car(c, cx, 960, 0.9, col_, door_open=False)
        oval(c, cx, 930, 260, 120, "#eef4fa" if white else "#c8d5e4")
        rect(c, cx - 260, 930, 520, 120, "#eef4fa" if white else "#c8d5e4")
    # supermarket facade
    if p.get("market", True):
        mx = 1800
        rect(c, mx, 300, 1100, 540, "#6d7884"); rect(c, mx, 300, 1100, 540, OUTLINE, stroke=8)
        rect(c, mx + 200, 220, 700, 110, "#c0392b", r=12); rect(c, mx + 200, 220, 700, 110, OUTLINE, r=12, stroke=7)
        text(c, "MARKET", mx + 550, 305, 84, "#ffffff")
        icicles(c, mx, mx + 1100, 300, 9, 1.4)
        lit = p.get("market_light", True) and not white
        rect(c, mx + 350, 480, 400, 360, "#ffe9a8" if lit else "#1b2230")
        rect(c, mx + 350, 480, 400, 360, OUTLINE, stroke=8); line(c, mx + 550, 480, mx + 550, 840, OUTLINE, 8)
        for wx in (mx + 60, mx + 830):
            rect(c, wx, 480, 220, 250, "#1b2230"); rect(c, wx, 480, 220, 250, OUTLINE, stroke=7)
        rect(c, mx, 780, 1100, 70, "#eef4fa" if white else "#c8d5e4")
        if lit: radial(c, mx + 550, 660, 600, "#ffe28a", 80)
    # train station
    if p.get("station"):
        sx = 3700
        rect(c, sx, 260, 1200, 580, "#7a5a48"); rect(c, sx, 260, 1200, 580, OUTLINE, stroke=8)
        poly(c, [(sx - 60, 270), (sx + 600, 60), (sx + 1260, 270)], "#5a3a30"); poly(c, [(sx - 60, 270), (sx + 600, 60), (sx + 1260, 270)], OUTLINE, stroke=8)
        circle(c, sx + 600, 190, 60, "#f4efe4"); circle(c, sx + 600, 190, 60, OUTLINE, stroke=6)
        rect(c, sx + 950, 0, 90, 200, "#4a3a34"); rect(c, sx + 950, 0, 90, 200, OUTLINE, stroke=6)
        for k in range(5):
            ph = (t * 0.25 + k / 5) % 1
            circle(c, sx + 995 + ph * 120, -ph * 400, 40 + ph * 90, "#d8dde4", int(170 * (1 - ph)))
        for k in range(4):
            wx = sx + 90 + k * 280
            rect(c, wx, 420, 180, 230, "#ffd77a"); rect(c, wx, 420, 180, 230, OUTLINE, stroke=7)
            radial(c, wx + 90, 535, 260, "#ffd77a", 70)
        rect(c, sx + 520, 600, 160, 240, "#2a1c18"); rect(c, sx + 520, 600, 160, 240, OUTLINE, stroke=7)
        rect(c, sx - 200, 820, 1600, 80, "#eef4fa" if white else "#c8d5e4")
    if p.get("collapsed"):
        sx = 3700
        for k in range(14):
            rnd = random.Random(k)
            x = sx + rnd.uniform(-100, 1250); y = 820 - rnd.uniform(0, 300)
            poly(c, [(x, y), (x + rnd.uniform(80, 220), y + 30), (x + 150, 840), (x - 40, 840)], rnd.choice(["#eef4fa", "#7a5a48", "#5a3a30", "#7a838e"]))
    if p.get("rails"):
        for yy in (900, 960):
            line(c, -3000, yy, 7000, yy, "#3a3f4a", 12)
        for x in range(-1000, 6000, 90): rect(c, x, 890, 30, 80, "#5a4a3a")
    if p.get("metro"):
        mx = 2200
        rect(c, mx, 700, 500, 140, "#2a3038"); rect(c, mx, 700, 500, 140, OUTLINE, stroke=8)
        rect(c, mx + 60, 740, 380, 100, "#0a0c10")
        rect(c, mx + 180, 560, 140, 140, "#c0392b", r=20); text(c, "M", mx + 250, 670, 110, "#ffffff")
        rnd = random.Random(9)
        for k in range(120):
            x = mx + 250 + (rnd.random() - 0.5) * 1600 * rnd.random(); y = 860 + rnd.uniform(0, 160)
            oval(c, x, y, 13, 6, "#7d8ea4", 200)
    if p.get("prints"):
        rnd = random.Random(4)
        for k in range(160):
            x = 3800 + rnd.uniform(0, 1000) - (rnd.random() ** 2) * 1800; y = 880 + rnd.uniform(0, 150)
            oval(c, x, y, 13, 6, "#7d8ea4", 200)
    for ch in p.get("chars", []):
        kid(c, t, u, ch, 950)
    overlays(c, t, u, p)
    if p.get("snow", 1.0) > 0:
        snowfall(c, t, -1500, 6500, -800, 1400, p.get("snow", 1.0) * (0.6 if white else 1.4), p.get("wind", 1.5))
    if p.get("whiteout"):
        rect(c, -5000, -5000, 15000, 15000, "#f2f6fa", int(255 * p["whiteout"]))
        snowfall(c, t + 3, -1500, 6500, -800, 1400, 2.0, 3.0, 7)
    if not white:
        darkness(c, 0, 0, p.get("dark", 0.25), [("glow", 2350, 660, 800, 0.8)] + p.get("lights", []))

# ------------------------------------------------------------------ supermarket interior
MCAM = {"wide": (2000, 650, 3400, 1300), "entrance": (330, 700, 1000, 900), "doors": (300, 720, 720, 720), "thermo": (560, 600, 420, 420),
        "aisle7": (1250, 720, 1100, 900), "aisle9": (1850, 720, 1100, 900), "aisle12": (2450, 720, 1100, 900), "clothes": (2950, 740, 900, 820),
        "staff": (3340, 760, 760, 720), "handle": (3405, 735, 300, 300), "freezer": (3720, 720, 940, 860), "floor7": (1250, 880, 1000, 560),
        "window": (820, 520, 760, 640), "mid": (1800, 700, 1800, 1050), "back": (3400, 700, 1500, 1000)}

ITEMS = ["#d8473a", "#3d8bd9", "#e0a52a", "#4caf6e", "#9b6be0", "#ef7d3a"]

def shelf_unit(c, x, y, w, h, seed, label=None, frost=0.0):
    rect(c, x, y - h, w, h, "#c9ced6"); rect(c, x, y - h, w, h, OUTLINE, stroke=6)
    rnd = random.Random(seed)
    for r in range(4):
        sy = y - h + 40 + r * (h - 60) / 4
        rect(c, x + 10, sy + (h - 60) / 4 - 14, w - 20, 14, "#8f98a2")
        xx = x + 22
        while xx < x + w - 50:
            kind = rnd.random(); colr = rnd.choice(ITEMS)
            ih = (h - 60) / 4 - 26
            if kind < 0.45:
                rect(c, xx, sy + (h - 60) / 4 - 14 - ih * 0.7, 34, ih * 0.7, colr, r=5); rect(c, xx, sy + (h - 60) / 4 - 14 - ih * 0.7, 34, ih * 0.7, OUTLINE, r=5, stroke=3); xx += 40
            elif kind < 0.75:
                rect(c, xx, sy + (h - 60) / 4 - 14 - ih * 0.9, 26, ih * 0.9, "#79c2ee", 220, r=8); rect(c, xx, sy + (h - 60) / 4 - 14 - ih * 0.9, 26, ih * 0.9, OUTLINE, r=8, stroke=3); xx += 32
            else:
                rect(c, xx, sy + (h - 60) / 4 - 14 - ih * 0.85, 48, ih * 0.85, colr, r=10); rect(c, xx, sy + (h - 60) / 4 - 14 - ih * 0.85, 48, ih * 0.85, OUTLINE, r=10, stroke=3); xx += 54
    if frost > 0:
        rect(c, x, y - h, w, h, "#e6f4ff", int(90 * frost))
        icicles(c, x, x + w, y - h, seed, 0.8)
    if label:
        line(c, x + w / 2, 120, x + w / 2, y - h - 90, "#5b616b", 5)
        rect(c, x + w / 2 - 70, y - h - 100, 140, 70, "#2f6db0", r=10); rect(c, x + w / 2 - 70, y - h - 100, 140, 70, OUTLINE, r=10, stroke=5)
        text(c, label, x + w / 2, y - h - 46, 48, "#ffffff")

def draw_market(c, t, u, p):
    fr = p.get("frost", 0.5)
    lin_grad(c, -3000, -800, 10000, 1800, "#4a5560", "#36404a")
    rect(c, -3000, -800, 10000, 900, "#252b31"); rect(c, -3000, 90, 10000, 30, "#1b2024")
    for x in range(0, 4000, 300): rect(c, x + 40, 100, 220, 16, "#e8f0f6" if p.get("lights_on") else "#5d666e", r=6)
    rect(c, -3000, FLOOR, 10000, 1500, "#5a5f66")
    for x in range(-200, 4200, 140):
        line(c, x, FLOOR, x - 80, FLOOR + 600, "#4c5157", 3)
    line(c, -3000, FLOOR, 7000, FLOOR, OUTLINE, 8)
    # entrance + sliding doors with snow outside
    lin_grad(c, 100, 460, 400, 540, "#9fb6d0", "#d9e6f2")
    snowfall(c, t, 100, 500, 460, 1000, 0.5, 1.2, 2)
    op = p.get("door_open", 0.25)
    if isinstance(op, (list, tuple)): op = lerp(op[0], op[1], ease(u))
    for i, sgn in enumerate((-1, 1)):
        px = 300 + sgn * (100 + op * 160) - 100
        rect(c, px, 460, 200, 540, "#cfe6f4", 120); rect(c, px, 460, 200, 540, OUTLINE, stroke=6)
    rect(c, 90, 440, 420, 560, OUTLINE, stroke=10)
    frost_edges(c, 100, 460, 400, 540, fr)
    # entrance thermometer
    rect(c, 530, 480, 60, 240, "#f4f4f4", r=30); rect(c, 530, 480, 60, 240, OUTLINE, r=30, stroke=5)
    circle(c, 560, 700, 30, "#e0523a"); rect(c, 552, 540, 16, 160, "#e0523a")
    # broken high window with snow drift
    lin_grad(c, 700, 330, 260, 200, "#8aa4c2", "#c9d9ea")
    snowfall(c, t, 700, 960, 330, 980, 0.35, 0.6, 3)
    rect(c, 700, 330, 260, 200, OUTLINE, stroke=8); poly(c, [(700, 330), (800, 330), (720, 420)], "#5c6670")
    oval(c, 830, 1000, 230, 60, "#eef4fa")
    # checkout
    rect(c, 600, 790, 300, 210, "#a35a3a"); rect(c, 600, 790, 300, 210, OUTLINE, stroke=6); rect(c, 590, 770, 320, 30, "#3a3f4a")
    # shelves
    shelf_unit(c, 1000, FLOOR, 500, 520, 1, "7", fr)
    shelf_unit(c, 1600, FLOOR, 500, 520, 2, "9", fr)
    shelf_unit(c, 2200, FLOOR, 500, 520, 3, "12", fr)
    # clothes rack
    line(c, 2800, 560, 3150, 560, "#8f98a2", 10)
    for k, colr in enumerate(["#2f6db0", "#c0392b", "#3a8a5a", "#e8b33a", "#6a4a8a"]):
        x = 2820 + k * 66
        poly(c, [(x, 570), (x + 56, 570), (x + 62, 820), (x - 6, 820)], colr); poly(c, [(x, 570), (x + 56, 570), (x + 62, 820), (x - 6, 820)], OUTLINE, stroke=4)
    line(c, 2810, 560, 2810, 1000, "#8f98a2", 8); line(c, 3140, 560, 3140, 1000, "#8f98a2", 8)
    # staff metal door
    rect(c, 3250, 560, 180, 440, "#8a939e"); rect(c, 3250, 560, 180, 440, OUTLINE, stroke=7)
    rect(c, 3390, 715, 30, 40, "#c9ced6", r=6); rect(c, 3390, 715, 30, 40, OUTLINE, r=6, stroke=4)
    if p.get("handle_ice"): circle(c, 3405, 735, 28, "#dff3ff", 200)
    # walk-in freezer door
    fo = p.get("freezer_open", 0.0)
    if isinstance(fo, (list, tuple)): fo = lerp(fo[0], fo[1], ease(u))
    rect(c, 3520, 470, 400, 530, "#0e1218")
    rect(c, 3520, 470, 400 * (1 - 0.8 * fo), 530, "#b9c2cc", r=8); rect(c, 3520, 470, 400 * (1 - 0.8 * fo), 530, OUTLINE, r=8, stroke=8)
    if fo < 0.5:
        rect(c, 3860 - 400 * 0.8 * fo, 690, 36, 110, "#5d666e", r=8)
    if fo > 0: radial(c, 3720, 740, 300, "#cfe8ff", int(90 * fo))
    rect(c, 3500, 450, 440, 550, OUTLINE, stroke=10)
    frost_edges(c, -200, -200, 4400, 1400, fr * 0.6)
    icicles(c, -200, 4200, 120, 5, 1.0 * fr)
    for ch in p.get("chars", []):
        kid(c, t, u, ch, FLOOR)
    if p.get("stove"):
        sx, sy = p["stove"]
        rect(c, sx - 50, sy - 40, 100, 40, "#3a3f4a", r=6);
        for k in range(3):
            fl = 20 + 8 * math.sin(t * 20 + k)
            poly(c, [(sx - 30 + k * 30, sy - 40), (sx - 18 + k * 30, sy - 40 - fl), (sx - 6 + k * 30, sy - 40)], "#5ab0ff")
        if p.get("pot"): rect(c, sx - 60, sy - 110, 120, 70, "#9aa3ad", r=10)
    overlays(c, t, u, p)
    amt = p.get("dark", 0.55)
    lights = [("rect", 100, 460, 400, 540, 0.7), ("glow", 300, 760, 700, 0.5), ("rect", 700, 330, 260, 200, 0.6)]
    for ch in p.get("chars", []):
        if ch.get("flashlight") and ch.get("on", True):
            x = anim_x(ch, u)
            ox, oy = flashlight_origin(ch["who"], x, ch.get("y", FLOOR), ch.get("face", 1), ch.get("scale", 1.0))
            ang = ch.get("beam", 0 if ch.get("face", 1) > 0 else 180)
            lights.append(("cone", ox, oy, ang, 1300, 38, 0.95))
    if p.get("stove"): lights.append(("glow", p["stove"][0], p["stove"][1] - 60, 520, 0.85))
    lights += p.get("lights", [])
    darkness(c, 0, 0, amt, lights, color="#040814")
    if p.get("stove"): radial(c, p["stove"][0], p["stove"][1] - 60, 420, "#ffb36a", 50)
    if fr > 0.3:
        rect(c, -5000, -5000, 15000, 15000, "#9fc8ff", int(28 * fr))

# ------------------------------------------------------------------ walk-in freezer interior
ZCAM = {"wide": (800, 660, 1700, 1000), "bed": (780, 860, 1000, 620), "stove": (1180, 860, 700, 520), "door": (1450, 700, 760, 820),
        "thermo": (1300, 520, 420, 420), "shelves": (300, 700, 800, 800), "faces": (760, 860, 600, 420)}

def sleeping_bag(c, x, y, w, colr="#3a5fc0"):
    rect(c, x, y - 130, w, 130, colr, r=50); rect(c, x, y - 130, w, 130, OUTLINE, r=50, stroke=6)
    line(c, x + 30, y - 65, x + w - 30, y - 65, mixc(colr, "#000000", 0.3), 5)

def draw_freezer(c, t, u, p):
    lin_grad(c, -3000, -800, 8000, 1800, "#9aa7b4", "#6e7a86")
    for x in range(-200, 1800, 90): line(c, x, -800, x, FLOOR, "#7f8b97", 6)
    rect(c, -3000, -800, 8000, 900, "#5d6670")
    rect(c, -3000, FLOOR, 8000, 1500, "#4a525b"); line(c, -3000, FLOOR, 6000, FLOOR, OUTLINE, 8)
    icicles(c, -200, 1800, 100, 8, 1.0)
    # shelves with boxes
    for sy in (420, 640, 860):
        rect(c, 40, sy, 480, 20, "#c9ced6"); rect(c, 40, sy, 480, 20, OUTLINE, stroke=5)
        rnd = random.Random(sy)
        for k in range(4):
            bw = rnd.uniform(80, 110)
            rect(c, 60 + k * 115, sy - 110, bw, 110, "#c9a46a"); rect(c, 60 + k * 115, sy - 110, bw, 110, OUTLINE, stroke=4)
            rect(c, 60 + k * 115, sy - 110, bw, 20, "#e6f4ff", 160)
    # thermometer
    rect(c, 1270, 400, 60, 240, "#f4f4f4", r=30); rect(c, 1270, 400, 60, 240, OUTLINE, r=30, stroke=5)
    circle(c, 1300, 620, 30, "#3d8bd9"); rect(c, 1292, 500, 16, 120, "#3d8bd9")
    # cardboard floor + mattress
    rect(c, 480, FLOOR - 20, 700, 20, "#b08a5a")
    rect(c, 520, FLOOR - 70, 620, 50, "#e8e2d2", r=14); rect(c, 520, FLOOR - 70, 620, 50, OUTLINE, r=14, stroke=5)
    # door
    fo = p.get("door", 0.0)
    if isinstance(fo, (list, tuple)): fo = lerp(fo[0], fo[1], ease(u))
    rect(c, 1400, 380, 220, 620, "#2c3440")
    if fo > 0: lin_grad(c, 1400, 380, 220 * fo, 620, "#58667a", "#3a4452")
    rect(c, 1400 + 220 * fo, 380, 220 * (1 - fo) + 4, 620, "#b9c2cc"); rect(c, 1400, 380, 220, 620, OUTLINE, stroke=8)
    for ch in p.get("chars", []):
        kid(c, t, u, ch, FLOOR - 60)
    if p.get("bag"):
        sleeping_bag(c, 520, FLOOR - 40, 600, "#3a5fc0")
    if p.get("stove"):
        sx, sy = 1180, FLOOR - 20
        rect(c, sx - 60, sy - 50, 120, 50, "#3a3f4a", r=8); rect(c, sx - 60, sy - 50, 120, 50, OUTLINE, r=8, stroke=5)
        for k in range(3):
            fl = 26 + 10 * math.sin(t * 20 + k)
            poly(c, [(sx - 36 + k * 36, sy - 50), (sx - 22 + k * 36, sy - 50 - fl), (sx - 8 + k * 36, sy - 50)], "#5ab0ff")
        if p.get("pot"):
            rect(c, sx - 70, sy - 130, 140, 80, "#9aa3ad", r=12); rect(c, sx - 70, sy - 130, 140, 80, OUTLINE, r=12, stroke=5)
            for k in range(3):
                ph = (t * 0.6 + k / 3) % 1
                circle(c, sx - 30 + k * 30, sy - 150 - ph * 120, 14 + ph * 20, "#f4f8ff", int(150 * (1 - ph)))
    if p.get("radio"):
        rect(c, 980, FLOOR - 170, 180, 110, "#7a5a3a", r=16); rect(c, 980, FLOOR - 170, 180, 110, OUTLINE, r=16, stroke=5)
        circle(c, 1030, FLOOR - 115, 30, "#3b2e26"); line(c, 1140, FLOOR - 170, 1190, FLOOR - 260, OUTLINE, 6)
    co = p.get("co", 0)
    if co:
        for k in range(6):
            ph = (t * 0.05 + k / 6) % 1
            oval(c, -200 + ph * 2200, 300 + k * 110 + math.sin(t + k) * 30, 700, 110, "#8a8f98", int(90 * co))
    overlays(c, t, u, p)
    lights = [("glow", 800, 600, 1100, 0.7)]
    if p.get("stove"): lights.append(("glow", 1180, FLOOR - 120, 650, 0.9))
    if fo > 0: lights.append(("rect", 1400, 380, 220 * fo, 620, 0.5))
    darkness(c, 0, 0, p.get("dark", 0.45), lights, color="#050a16")
    if p.get("stove"): radial(c, 1180, FLOOR - 100, 500, "#ffb36a", 40)
    if p.get("blur"):
        rect(c, -5000, -5000, 15000, 15000, "#303540", int(80 * p["blur"] * (0.6 + 0.4 * math.sin(t * 2))))

WORLDS2 = {"fcity": (draw_fcity, FCAM), "market": (draw_market, MCAM), "freezer": (draw_freezer, ZCAM)}
