# Scene library. World scenes draw in world units (camera applied by renderer).
# Screen scenes draw in screen space and get the safe content rect.
import math, random, skia
from gfx import *

FLOOR = 1000

# --------------------------------------------------------------------------- helpers
def anim_x(d, u):
    x0 = d.get("x", 0); x1 = d.get("x1", x0)
    return lerp(x0, x1, ease(u) if d.get("ease", True) else u)

def overlays(c, t, u, p):
    for o in p.get("fx", []):
        k = o[0]
        if k == "rings":  # sound rings
            _, x, y = o[:3]; colr = o[3] if len(o) > 3 else "#ffe28a"
            for i in range(3):
                ph = (t * 1.6 + i / 3) % 1
                c.drawCircle(x, y, 30 + ph * 220, P(colr, int(200 * (1 - ph)), 8))
        elif k == "smell":
            _, x, y = o
            for i in range(3):
                path = skia.Path(); yy = y - ((t * 60 + i * 70) % 210)
                path.moveTo(x - 60 + i * 60, yy + 100)
                for j in range(4):
                    path.quadTo(x - 60 + i * 60 + (30 if j % 2 else -30), yy + 75 - j * 50, x - 60 + i * 60, yy + 50 - j * 50)
                c.drawPath(path, P("#b5d36a", 170, 10))
        elif k == "highlight":
            _, x, y, r = o
            pulse = 1 + 0.06 * math.sin(t * 8)
            c.drawCircle(x, y, r * pulse * ease_out(u * 4), P("#ffd400", 230, 12))
        elif k == "question":
            _, x, y = o
            text(c, "?", x, y + math.sin(t * 4) * 8, 150, "#ffd400", stroke=14, stroke_color=OUTLINE)
        elif k == "exclaim":
            _, x, y = o
            sc = back_out(clamp(t * 4))
            text(c, "!", x, y, 170 * sc, "#ff5a3c", stroke=14, stroke_color=OUTLINE)
        elif k == "sweat":
            _, x, y = o
            yy = y + (t * 80) % 60
            path = skia.Path(); path.moveTo(x, yy - 24); path.quadTo(x + 16, yy, x, yy + 6); path.quadTo(x - 16, yy, x, yy - 24)
            c.drawPath(path, P("#8fd3ff")); c.drawPath(path, P(OUTLINE, 255, 4))
        elif k == "zzz":
            _, x, y = o
            for i in range(3):
                ph = (t * 0.6 + i / 3) % 1
                text(c, "z", x + ph * 80, y - ph * 160, 50 + i * 10, "#dfe7ff", a=int(255 * (1 - ph)), stroke=8, stroke_color=OUTLINE)
        elif k == "thought":  # thought bubble with cans
            _, x, y = o
            sc = back_out(clamp(t * 3))
            c.save(); c.translate(x, y); c.scale(sc, sc)
            for i, (dx, dy, r) in enumerate(((-90, 120, 14), (-60, 80, 22))):
                circle(c, dx, dy, r, "#ffffff"); circle(c, dx, dy, r, OUTLINE, stroke=5)
            oval(c, 60, -40, 190, 120, "#ffffff"); oval(c, 60, -40, 190, 120, OUTLINE, stroke=6)
            for i in range(3):
                draw_can(c, -40 + i * 90, 10 + math.sin(t * 5 + i) * 6, 0.8, ["#d8473a", "#3d8bd9", "#e0a52a"][i])
            c.restore()
        elif k == "dust":
            _, x, y, w = o
            rnd = random.Random(3)
            for i in range(40):
                px = x + rnd.uniform(0, w); py = y + rnd.uniform(-300, 0) - (t * rnd.uniform(10, 40)) % 300
                circle(c, px, py, rnd.uniform(3, 8), "#c8c0b0", 90)
        elif k == "speed":
            _, x, y = o
            for i in range(7):
                yy = y - 140 + i * 40
                line(c, x - 600, yy, x - 150 - (i % 3) * 60, yy, "#ffffff", 8, 150)
        elif k == "tic_marks":
            _, x, y = o
            for i in range(3):
                ph = (t * 3 + i * 0.33) % 1
                xx = x + (i - 1) * 90; a = int(255 * (1 - ph))
                line(c, xx - 20, y - 30 - ph * 40, xx + 20, y - 50 - ph * 40, "#fff2a8", 9, a)
                line(c, xx - 10, y - 70 - ph * 40, xx + 24, y - 60 - ph * 40, "#fff2a8", 9, a)
        elif k == "heart_house":
            _, x, y = o
            sc = back_out(clamp(t * 2.5))
            c.save(); c.translate(x, y); c.scale(sc, sc)
            poly(c, [(-90, 0), (0, -80), (90, 0)], "#ffcc4d"); poly(c, [(-90, 0), (0, -80), (90, 0)], OUTLINE, stroke=8)
            rect(c, -70, 0, 140, 110, "#ffe08a"); rect(c, -70, 0, 140, 110, OUTLINE, stroke=8)
            circle(c, 0, 50, 26, "#ff6b6b")
            c.restore()
        elif k == "bubbles":
            _, x, y, w = o
            rnd = random.Random(4)
            for i in range(26):
                bx = x + rnd.uniform(0, w) + math.sin(t * 2 + i) * 14
                by = y - ((t * rnd.uniform(40, 90) + rnd.uniform(0, 700)) % 700)
                c.drawCircle(bx, by, rnd.uniform(8, 22), P("#bfe8ff", 170, 4))
        elif k == "wind":
            _, x, y = o
            for i in range(6):
                ph = (t * 1.4 + i / 6) % 1
                xx = x + ph * 1400; yy = y + i * 50 + math.sin(t * 4 + i) * 20
                path = skia.Path(); path.moveTo(xx, yy); path.quadTo(xx + 120, yy - 40, xx + 260, yy)
                c.drawPath(path, P("#dfe9f2", int(200 * (1 - ph)), 8))
        elif k == "drip":
            _, x, y = o
            for i in range(2):
                ph = (t * 1.2 + i * 0.5) % 1
                yy = y + ph * 260
                path = skia.Path(); path.moveTo(x, yy - 16); path.quadTo(x + 10, yy, x, yy + 4); path.quadTo(x - 10, yy, x, yy - 16)
                c.drawPath(path, P("#7fd0ff", int(255 * (1 - ph * 0.5))))

# --------------------------------------------------------------------------- KITCHEN world
KCAM = {
    "wide": (1750, 640, 2700, 1300), "door": (300, 740, 900, 820), "table": (790, 780, 1000, 820),
    "stoves": (1560, 700, 1200, 900), "gap": (1410, 700, 560, 560), "gap_close": (1410, 760, 330, 330),
    "fridge": (2290, 700, 1000, 900), "hole": (2470, 900, 560, 420), "table2": (2900, 760, 1000, 820),
    "sacks": (3440, 800, 820, 720), "window": (2875, 420, 760, 520), "vent": (1560, 300, 1000, 620),
    "floor": (1100, 960, 900, 420), "left": (700, 700, 1500, 1000), "right": (2700, 700, 1600, 1000),
    "mid": (1500, 700, 1700, 1050), "under_table": (790, 900, 700, 420),
}

def kitchen_bg(c, p, t):
    # back wall
    lin_grad(c, -3000, -800, 10000, 1800, "#53636a", "#3d4a50")
    rnd = random.Random(11)
    for x in range(-200, 4200, 120):
        for y in range(200, 1000, 120):
            rect(c, x + 3, y + 3, 114, 114, "#5f7077" if (x // 120 + y // 120) % 2 else "#58686f", 255, r=6)
    for _ in range(40):
        oval(c, rnd.uniform(0, 3800), rnd.uniform(250, 980), rnd.uniform(20, 70), rnd.uniform(10, 40), "#3a453f", 70)
    rect(c, -3000, 120, 10000, 60, "#465358")
    # ceiling
    rect(c, -3000, -800, 10000, 900, "#2d3438"); rect(c, -3000, 90, 10000, 30, "#20262a")
    # floor
    rect(c, -3000, FLOOR, 10000, 1500, "#3f362f")
    for x in range(-200, 4200, 160):
        for i, y in enumerate(range(FLOOR, FLOOR + 600, 80)):
            if (x // 160 + i) % 2: rect(c, x, y, 160, 80, "#4a4038")
    line(c, -3000, FLOOR, 7000, FLOOR, OUTLINE, 8)
    for gx in (900, 1700, 2600):
        oval(c, gx, FLOOR + 50, 130, 22, "#2c2622", 160)
    # window
    wl = p.get("window", "#cfdde6")
    draw_window(c, 2700, 250, 350, 270, light=wl)
    # pantry door on back wall
    d = p.get("door", 0.15)
    if isinstance(d, (list, tuple)): d = lerp(d[0], d[1], ease_out(clamp(t / d[2])) if len(d) > 2 else ease(u))
    draw_door(c, 180, FLOOR, 220, 460, d, color="#7d8792")
    # pipe near fridge
    rect(c, 2430, 100, 34, 520, "#7a8288"); rect(c, 2430, 100, 34, 520, OUTLINE, stroke=5)
    poly(c, [(2430, 620), (2464, 620), (2470, 640), (2440, 650), (2426, 636)], "#7a8288")
    # hole behind fridge
    path = skia.Path(); path.moveTo(2400, FLOOR); path.lineTo(2400, FLOOR - 80); path.quadTo(2460, FLOOR - 140, 2520, FLOOR - 80); path.lineTo(2520, FLOOR); path.close()
    c.drawPath(path, P("#0a0a0d")); c.drawPath(path, P(OUTLINE, 255, 6))
    # vent duct over stoves
    vent_open = p.get("vent_open", False)
    rect(c, 1300, 140, 520, 160, "#8b949c", r=10); rect(c, 1300, 140, 520, 160, OUTLINE, r=10, stroke=6)
    rect(c, 1360, 180, 400, 100, "#15171b", r=6)
    if not vent_open:
        for i in range(8): line(c, 1375 + i * 52, 186, 1375 + i * 52, 274, "#a8b0b8", 8)
    else:
        c.save(); c.translate(1400, 330); c.rotate(28)
        rect(c, 0, 0, 400, 30, "#a8b0b8", r=4); c.restore()
    # extractor hood under vent
    poly(c, [(1240, 300), (1880, 300), (1960, 420), (1160, 420)], "#6e7780"); poly(c, [(1240, 300), (1880, 300), (1960, 420), (1160, 420)], OUTLINE, stroke=6)

def _draw_r(c, t, u, r):
    rx = anim_x(r, u)
    al = r.get("alpha", 255)
    if "alpha1" in r: al = int(lerp(al, r["alpha1"], ease(u)))
    fl = r.get("flat", 0)
    if "flat1" in r: fl = lerp(fl, r["flat1"], ease(u))
    y = r.get("y", FLOOR)
    if "y1" in r: y = lerp(y, r["y1"], ease(u))
    if r.get("ant_only"):
        draw_roach(c, rx, y, t, r.get("face", 1), r.get("scale", 0.9), fl, False, True, 0, r.get("amp", 1), r.get("rz", 0), r.get("glow", True), 255, scary=not r.get("calm"))
        return
    draw_roach(c, rx, y, t, r.get("face", 1), r.get("scale", 0.9), fl, r.get("walk", False), False, r.get("shake", 0), r.get("amp", 1),
               r.get("rz", 0), True, al, r.get("speed", 1), False, al, scary=not r.get("calm"))

def kid_from(c, t, u, ch, y_default):
    x = anim_x(ch, u)
    rot = ch.get("rot", 0)
    if "rot1" in ch: rot = lerp(rot, ch["rot1"], ease_out(clamp(u * ch.get("rspeed", 1.0))))
    y = ch.get("y", y_default)
    if "y1" in ch: y = lerp(y, ch["y1"], ease(u))
    draw_kid(c, ch["who"], x, y, t + ch.get("toff", 0), ch.get("pose", "stand"), ch.get("face", 1), ch.get("expr", "neutral"),
             ch.get("look", (1, 0)), ch.get("scale", 1.0), ch.get("flashlight", False), ch.get("on", True), ch.get("carry"), rot)

def draw_kitchen(c, t, u, p):
    kitchen_bg(c, p, t)
    if p.get("drip", True):
        overlays(c, t, u, {"fx": [("drip", 2447, 650)]})
    # stoves
    for i in range(3):
        draw_stove(c, 1150 + i * 280, FLOOR, 240, 300)
    # gap antennae
    if "gap_ant" in p:
        g = p["gap_ant"]; L = lerp(g.get("l0", 0.2), g.get("l1", 1), ease(u))
        # draw from behind stoves: clip region above stove top/inside gap
        draw_antennae_from(c, 1410, FLOOR - 250, t, 1, 0.8, L, g.get("amp", 1.0))
        if g.get("one", False):
            pass
    # redraw gap edges (stove sides) so antenna roots look inside the gap
    for gx in (1390, 1670):
        rect(c, gx, FLOOR - 300, 40, 300, "#0c0d10")
    # table 1 + pots
    draw_table(c, 520, FLOOR, 520, 240)
    pots = p.get("pots", "hang")
    line(c, 540, 130, 1060, 130, "#5b616b", 10)
    for i, px in enumerate((600, 760, 920)):
        if pots == "hang":
            draw_pot(c, px, 270, 0.8, math.sin(t * 1.5 + i) * 2)
        elif pots == "swing":
            draw_pot(c, px, 270, 0.8, math.sin(t * 9 + i) * 18)
        elif pots == "fall":
            fu = clamp(u * 1.6 - i * 0.15)
            yy = 270 + (fu ** 2) * 700; ang = fu * 160 * (1 if i % 2 else -1)
            draw_pot(c, px + fu * 60 * (i - 1), min(yy, FLOOR - 60), 0.8, ang)
        elif pots == "floor":
            draw_pot(c, px + (i - 1) * 80, FLOOR - 50, 0.8, [150, -110, 175][i])
    r = p.get("roach")
    if r and r.get("behind"): _draw_r(c, t, u, r)
    # fridge
    draw_fridge(c, 2100, FLOOR, 280, 640)
    # table 2, bowl
    draw_table(c, 2650, FLOOR, 500, 240)
    if p.get("bowl"): draw_bowl(c, 2900, FLOOR - 240, 1.0, p.get("water", 1.0))
    # sacks
    for i, sx in enumerate((3380, 3520, 3450)):
        draw_sack(c, sx, FLOOR if i < 2 else FLOOR - 110, 1.0, ["#c9a46a", "#b9945d", "#d4b07a"][i])
    # floor marks
    if p.get("marks"):
        rnd = random.Random(5)
        for i in range(16):
            x0 = 300 + i * 190 + rnd.uniform(-40, 40); y0 = FLOOR + 30 + rnd.uniform(0, 160)
            for j in range(3):
                line(c, x0 + j * 14, y0 + j * 8, x0 + 70 + j * 14, y0 - 6 + j * 8, "#c9c0ae", 4, 200)
    # cart
    cart = p.get("cart")
    if cart is not None:
        cx = cart if isinstance(cart, (int, float)) else lerp(cart[0], cart[1], ease(u))
        draw_cart(c, cx, FLOOR, 1.0, p.get("cart_tilt", 0))
    # mess
    if p.get("mess"):
        rnd = random.Random(9)
        for i in range(10):
            draw_can(c, 400 + rnd.uniform(0, 3000), FLOOR + rnd.uniform(10, 80), 0.7, rnd.choice(["#d8473a", "#3d8bd9", "#e0a52a"]))
    # flashlight object on floor etc
    fl = p.get("flash_obj")
    if fl: draw_flashlight_obj(c, *fl)
    # roach
    r = p.get("roach")
    if r and not r.get("hidden") and not r.get("behind"): _draw_r(c, t, u, r)
    fly = p.get("fly")
    if fly:
        k = clamp(t / fly[4])
        fx = lerp(fly[0], fly[2], k); fy = lerp(fly[1], fly[3], k) - math.sin(k * math.pi) * 300
        draw_flashlight_obj(c, fx, fy, t * 900, 1.2, 0, True)
    # characters
    for ch in p.get("chars", []):
        kid_from(c, t, u, ch, FLOOR)
    # table front (for hiding under) - draw front legs again
    if p.get("table_front"):
        rect(c, 520, FLOOR - 240, 520, 30, "#a9b2bd", r=6); rect(c, 520, FLOOR - 240, 520, 30, OUTLINE, r=6, stroke=6)
        for lx in (544, 992): rect(c, lx, FLOOR - 210, 24, 210, "#8a939e")
    overlays(c, t, u, p)
    # lighting
    light = p.get("light", "dim")
    amt = {"dim": 0.45, "dark": 0.74, "black": 0.92, "day": 0.15, "morning": 0.28}.get(light, light if isinstance(light, (int, float)) else 0.5)
    if "light_u" in p:  # animated light change (a0,a1)
        a0, a1 = p["light_u"]; amt = lerp(a0, a1, ease(u))
    lights = [("rect", 2700, 250, 350, 270, 0.9), ("glow", 2875, 700, 900, 0.55 if light != "black" else 0.15)]
    for ch in p.get("chars", []):
        if ch.get("flashlight") and ch.get("on", True):
            x = anim_x(ch, u)
            ox, oy = flashlight_origin(ch["who"], x, ch.get("y", FLOOR), ch.get("face", 1), ch.get("scale", 1.0))
            ang = ch.get("beam", 0 if ch.get("face", 1) > 0 else 180)
            if "beam1" in ch: ang = lerp(ang, ch["beam1"], ease(u))
            if ch.get("sweep"): ang += math.sin(t * 2.2) * ch["sweep"]
            flick = 1.0
            if ch.get("flicker"):
                flick = 1.0 if (math.sin(t * 40) > -0.2 and t < ch["flicker"]) else 0.0
            if flick:
                lights.append(("cone", ox, oy, ang, 1300, 38, 0.95))
                ch["_beam"] = (ox, oy, ang)
    if "gap_ant" in p:
        lights.append(("glow", 1410, FLOOR - 450, 520, 0.75))
    if r and not r.get("hidden"):
        lights.append(("glow", anim_x(r, u) + 150 * r.get("face", 1), r.get("y", FLOOR) - 150, 650, 0.55))
    for L in p.get("lights", []):
        if p.get("flicker") and (int(t * 9) % 3 == 0 or t > 1.0): continue
        lights.append(L)
    darkness(c, 0, 0, amt, lights)
    for ch in p.get("chars", []):
        if "_beam" in ch:
            ox, oy, ang = ch.pop("_beam")
            light_beam(c, ox, oy, ang, 1300, 38, 60)

# --------------------------------------------------------------------------- PANTRY world (interior)
PCAM = {"wide": (800, 650, 1700, 1050), "shelves": (700, 520, 1200, 820), "sit": (760, 820, 900, 560),
        "door": (1380, 700, 800, 800), "leo": (900, 760, 700, 640)}

def draw_pantry(c, t, u, p):
    lin_grad(c, -3000, -800, 8000, 1800, "#4b4038", "#3a302a")
    rect(c, -3000, FLOOR, 8000, 1500, "#30282a")
    line(c, -3000, FLOOR, 6000, FLOOR, OUTLINE, 8)
    for sy in (330, 560, 790):
        rect(c, 150, sy, 1000, 26, "#8a6a48"); rect(c, 150, sy, 1000, 26, OUTLINE, stroke=5)
        rnd = random.Random(sy)
        for i in range(9):
            kind = rnd.random()
            x = 200 + i * 105
            if kind < 0.55: draw_can(c, x, sy, 0.85, rnd.choice(["#d8473a", "#3d8bd9", "#e0a52a", "#4caf6e"]))
            elif kind < 0.85: draw_bottle(c, x, sy, 0.9)
            else: draw_sack(c, x, sy, 0.55)
    # door on right (inside)
    draw_door(c, 1300, FLOOR, 220, 460, p.get("door", 0.0), color="#6f7984", inner="#20242a")
    if p.get("latch_fallen"):
        rect(c, 1350, FLOOR - 20, 60, 16, "#c9b25a", r=4)
    for ch in p.get("chars", []):
        kid_from(c, t, u, ch, FLOOR)
    if p.get("eat"):
        draw_can(c, 760, FLOOR - 10, 1.0, "#d8473a", tomato=True)
    overlays(c, t, u, p)
    amt = p.get("dark", 0.45)
    lights = [("glow", 800, 500, 900, 0.7)]
    if p.get("flash") and t < p.get("flash_until", 1e9):
        lights.append(("cone", p["flash"][0], p["flash"][1], p["flash"][2], 1200, 40, 0.9))
    elif p.get("flash_until"):
        amt = max(amt, 0.86)
    darkness(c, 0, 0, amt, lights)

# --------------------------------------------------------------------------- STREET / CITY world (night)
SCAM = {"wide": (1600, 560, 2800, 1300), "restaurant": (2400, 600, 1300, 1000), "door": (2400, 700, 800, 700),
        "cars": (900, 820, 1300, 700), "sky": (1600, 200, 2400, 1000), "walk": (1200, 760, 1300, 900),
        "sign": (2300, 950, 700, 420), "glass": (2140, 700, 650, 600), "street": (1300, 800, 1900, 900)}

def city_skyline(c, t, base=820, day=False, seed=4, lights_on=False):
    rnd = random.Random(seed)
    x = -2000
    while x < 6000:
        w = rnd.uniform(160, 340); h = rnd.uniform(300, 900)
        colr = rnd.choice(["#4a4a58", "#5a4c4c", "#3e4656"]) if not day else rnd.choice(["#8ea3b8", "#a89890", "#9aa6b4"])
        rect(c, x, base - h, w, h + 400, colr); rect(c, x, base - h, w, h + 400, OUTLINE, stroke=5)
        for wy in range(int(base - h + 30), base - 40, 60):
            for wx in range(int(x + 20), int(x + w - 30), 50):
                lit = rnd.random() < (0.03 if lights_on else 0.0)
                rect(c, wx, wy, 26, 34, "#ffe28a" if lit else ("#2c3a50" if not day else "#c4d6e4"), r=3); rect(c, wx, wy, 26, 34, OUTLINE, r=3, stroke=3)
        x += w + rnd.uniform(10, 40)

def draw_car(c, x, y, s=1.0, color="#c4544a", door_open=True, face=1):
    c.save(); c.translate(x, y); c.scale(s * face, s)
    path = skia.Path(); path.moveTo(-220, -40); path.lineTo(-210, -110); path.lineTo(-120, -120); path.lineTo(-70, -190); path.lineTo(90, -190)
    path.lineTo(150, -120); path.lineTo(220, -110); path.lineTo(230, -40); path.close()
    c.drawPath(path, P(color)); c.drawPath(path, P(OUTLINE, 255, 7))
    poly(c, [(-55, -175), (10, -175), (10, -125), (-100, -125)], "#9fc3d8"); poly(c, [(25, -175), (82, -175), (125, -125), (25, -125)], "#9fc3d8")
    for wx in (-130, 140):
        circle(c, wx, -40, 44, "#22252b"); circle(c, wx, -40, 18, "#9aa1a8")
    if door_open:
        poly(c, [(10, -180), (-40, -240), (-60, -110), (5, -60)], mixc(color, "#000000", 0.2)); poly(c, [(10, -180), (-40, -240), (-60, -110), (5, -60)], OUTLINE, stroke=6)
    c.restore()

def draw_street(c, t, u, p):
    lin_grad(c, -3000, -1500, 9000, 2400, "#1c1e2c", "#6a4e4c")
    radial(c, 1600, 700, 1500, "#b07a68", 70)
    rnd = random.Random(2)
    for _ in range(80):
        circle(c, rnd.uniform(-1000, 4500), rnd.uniform(-800, 300), rnd.uniform(1.5, 4), "#ffffff", int(rnd.uniform(80, 220)))
    circle(c, 3000, 0, 90, "#f4efd8"); radial(c, 3000, 0, 300, "#f4efd8", 60)
    city_skyline(c, t, 820)
    # sidewalk & road
    rect(c, -3000, 820, 9000, 80, "#4a4d58"); rect(c, -3000, 900, 9000, 900, "#2c2e36")
    for x in range(-1000, 5000, 300): rect(c, x, 1080, 160, 18, "#c9c08a")
    if p.get("cars", True):
        draw_car(c, 700, 1000, 1.0, "#c4544a"); draw_car(c, 1350, 1060, 0.9, "#4a78b8", face=-1)
    # restaurant
    if p.get("restaurant", True):
        rx = 1850
        rect(c, rx, 220, 1100, 600, "#5a4a3e"); rect(c, rx, 220, 1100, 600, OUTLINE, stroke=8)
        rect(c, rx - 20, 200, 1140, 50, "#3b2e26")
        # broken windows
        for wx in (rx + 60, rx + 720):
            rect(c, wx, 400, 320, 330, "#14181f"); rect(c, wx, 400, 320, 330, OUTLINE, stroke=8)
            for k in range(5):
                a = k * 1.2
                line(c, wx + 160, 560, wx + 160 + math.cos(a) * 170, 560 + math.sin(a) * 170, "#b9d3e0", 4)
            poly(c, [(wx, 400), (wx + 120, 400), (wx, 520)], "#7fa6ba", 140)
        # bar door metal at back (through door)
        rect(c, rx + 440, 430, 230, 390, "#1a1c22"); rect(c, rx + 440, 430, 230, 390, OUTLINE, stroke=8)
        # inside: bar + metal door ajar with light line
        rect(c, rx + 470, 690, 170, 40, "#6b4a30")
        rect(c, rx + 520, 520, 90, 170, "#7d8792"); line(c, rx + 612, 522, rx + 612, 688, "#ffd98a", 6)
        # fallen sign (fork & knife icon, no text)
        c.save(); c.translate(rx + 420, 860); c.rotate(-12)
        rect(c, -200, -70, 400, 120, "#b9473b", r=14); rect(c, -200, -70, 400, 120, OUTLINE, r=14, stroke=7)
        line(c, -40, -40, -40, 20, "#f3e2c0", 12); line(c, 40, -40, 40, 20, "#f3e2c0", 12); circle(c, 0, -10, 26, "#f3e2c0", stroke=10)
        c.restore()
        # glass shards on ground
        for k in range(14):
            poly(c, [(rx + 100 + k * 60, 880), (rx + 120 + k * 60, 860), (rx + 140 + k * 60, 884)], "#a8cfe0", 200)
    for ch in p.get("chars", []):
        x = anim_x(ch, u)
        draw_kid(c, ch["who"], x, ch.get("y", 900), t + ch.get("toff", 0), ch.get("pose", "stand"), ch.get("face", 1), ch.get("expr", "neutral"),
                 ch.get("look", (1, 0)), ch.get("scale", 0.9), ch.get("flashlight", False), ch.get("on", True), ch.get("carry"), ch.get("rot", 0))
    # shadows that buzz/crawl
    if p.get("shadows"):
        for k in range(5):
            sx = (k * 600 + t * 120 * (1 if k % 2 else -1)) % 3200 - 200
            oval(c, sx, 300 + k * 90, 40, 14, "#000000", 160)
            for w in (-1, 1):
                oval(c, sx + w * 30, 290 + k * 90 + math.sin(t * 50) * 6, 30, 10, "#000000", 120)
    overlays(c, t, u, p)
    darkness(c, 0, 0, p.get("dark", 0.25), [("glow", 3000, 0, 700, 0.6)] + p.get("lights", []))

# --------------------------------------------------------------------------- CITY empty (wide, day-gray)
def draw_city(c, t, u, p):
    mood = p.get("mood", "night")
    if mood == "morning":
        lin_grad(c, -3000, -1500, 9000, 2400, "#f6c48a", "#9fd0ee")
        circle(c, 2400, 150, 120, "#fff4c4"); radial(c, 2400, 150, 500, "#fff4c4", 120)
    else:
        lin_grad(c, -3000, -1500, 9000, 2400, "#262836", "#7d6062")
        radial(c, 1500, 650, 1600, "#c08a74", 80)
        for k in range(3): oval(c, 1500, 120 + k * 160, 3000, 60, "#3a3440", 70)
    city_skyline(c, t, 820, day=(mood == "morning"), seed=p.get("seed", 4))
    rect(c, -3000, 820, 9000, 900, "#3a3d47" if mood != "morning" else "#7d8592")
    for x in range(-1000, 5000, 300): rect(c, x, 1000, 160, 18, "#c9c08a")
    if p.get("cars", True):
        draw_car(c, 600, 980, 0.9, "#c4544a"); draw_car(c, 1500, 1020, 0.9, "#5d8f5a", face=-1); draw_car(c, 2500, 990, 0.9, "#c9a43c")
    if p.get("paper"):
        for k in range(3):
            xx = (t * 200 + k * 700) % 3000
            poly(c, [(xx, 900 - k * 30), (xx + 40, 880 - k * 30), (xx + 50, 920 - k * 30), (xx + 8, 930 - k * 30)], "#e8e2d0")
    for ch in p.get("chars", []):
        x = anim_x(ch, u)
        draw_kid(c, ch["who"], x, ch.get("y", 950), t + ch.get("toff", 0), ch.get("pose", "stand"), ch.get("face", 1), ch.get("expr", "neutral"),
                 ch.get("look", (1, 0)), ch.get("scale", 0.9), ch.get("flashlight", False), ch.get("on", True), ch.get("carry"), ch.get("rot", 0))
    if p.get("peek"):  # tiny eyes in a dark window
        for (ex, ey) in ((1180, 420), (2210, 560)):
            bl = 1 if (t % 2.2) > 0.15 else 0.1
            oval(c, ex, ey, 10, 12 * bl, "#ffffff"); oval(c, ex + 26, ey, 10, 12 * bl, "#ffffff")
    overlays(c, t, u, p)
    if mood != "morning": darkness(c, 0, 0, p.get("dark", 0.2), [])

CCAM = {"wide": (1500, 600, 2600, 1200), "street": (1400, 820, 1500, 700), "cars": (1000, 880, 1200, 520),
        "windows": (1500, 480, 1300, 700), "sky": (2000, 300, 1600, 900), "roof": (1500, 700, 1900, 1100)}

# --------------------------------------------------------------------------- GARDEN flashback (mosquito)
def draw_garden(c, t, u, p):
    lin_grad(c, -3000, -1500, 9000, 2400, "#24314a", "#3d5a4e")
    rect(c, -3000, 850, 9000, 900, "#2f5a3a")
    # house
    rect(c, 1500, 380, 600, 470, "#c9b48a"); rect(c, 1500, 380, 600, 470, OUTLINE, stroke=8)
    poly(c, [(1450, 390), (1800, 150), (2150, 390)], "#9a4a3a"); poly(c, [(1450, 390), (1800, 150), (2150, 390)], OUTLINE, stroke=8)
    rect(c, 1740, 640, 120, 210, "#5a3a2a")
    for gx in range(-400, 3600, 70):
        line(c, gx, 850, gx + 10, 800 + (gx * 7) % 30, "#3f7a4a", 8)
    # running kids
    for ch in p.get("chars", []):
        x = anim_x(ch, u)
        draw_kid(c, ch["who"], x, 880, t + ch.get("toff", 0), "run", ch.get("face", 1), "scared", (1, 0), 0.9)
    # giant mosquito (cartoon)
    mx = lerp(p.get("mx0", 1300), p.get("mx1", 1600), ease(u)); my = 380 + math.sin(t * 5) * 30
    c.save(); c.translate(mx, my); c.scale(-1, 1)
    for k in (-1, 1):
        oval(c, 30, -60 + k * 10 + math.sin(t * 60) * 20 * k, 140, 40, "#d8ecf5", 150)
    oval(c, 0, 0, 160, 50, "#5a5f6e"); oval(c, -40, 6, 110, 40, "#a3121c"); oval(c, -60, -6, 50, 12, "#e0464e", 160); oval(c, 0, 0, 160, 50, OUTLINE, stroke=7)
    for i in range(4): line(c, -110 + i * 50, -40, -110 + i * 50, 40, "#3b3f4a", 6)
    circle(c, 190, -10, 50, "#4a4e5c"); circle(c, 190, -10, 50, OUTLINE, stroke=6)
    radial(c, 210, -22, 60, "#ff2a1a", 140); oval(c, 210, -22, 22, 26, "#ffd23a"); oval(c, 214, -22, 5, 18, OUTLINE)
    line(c, 230, 10, 400, 70, OUTLINE, 9)
    dl = (t * 60) % 60
    line(c, 400, 70, 400, 80 + dl, "#b0121c", 8); circle(c, 400, 84 + dl, 8, "#b0121c")
    for i in range(3):
        line(c, -40 + i * 60, 40, -90 + i * 70, 200, OUTLINE, 7)
    c.restore()
    overlays(c, t, u, p)
    # sepia flashback tint
    rect(c, -5000, -5000, 15000, 15000, "#c49a5a", 55)

GCAM = {"wide": (1600, 560, 2400, 1100), "chase": (1300, 640, 1500, 900), "mosq": (1500, 420, 900, 700)}

# --------------------------------------------------------------------------- RADIO (close prop)
def draw_radio(c, t, u, p):
    lin_grad(c, -3000, -3000, 9000, 9000, "#1e2433", "#121620")
    rect(c, 400, 400, 900, 520, "#7a5a3a", r=40); rect(c, 400, 400, 900, 520, OUTLINE, r=40, stroke=10)
    circle(c, 640, 660, 160, "#3b2e26"); circle(c, 640, 660, 160, OUTLINE, stroke=8)
    for i in range(6): line(c, 520, 560 + i * 40, 760, 560 + i * 40, "#5a4a3a", 8)
    rect(c, 860, 500, 360, 120, "#e8d8a8", r=10); rect(c, 860, 500, 360, 120, OUTLINE, r=10, stroke=6)
    nx = 880 + (math.sin(t * 1.3) * 0.5 + 0.5) * 320
    line(c, nx, 510, nx, 610, "#d94a3a", 6)
    circle(c, 960, 760, 50, "#c9b27a"); circle(c, 1120, 760, 50, "#c9b27a")
    line(c, 1250, 400, 1400, 120, OUTLINE, 10)
    # static waves crossed
    rnd = random.Random(int(t * 12))
    for i in range(30):
        x = 1400 + rnd.uniform(-200, 200); y = 300 + rnd.uniform(-150, 150)
        line(c, x, y, x + rnd.uniform(-30, 30), y + rnd.uniform(-30, 30), "#9fb0c8", 4, 150)
    overlays(c, t, u, p)

RCAM = {"wide": (850, 600, 1400, 1000), "close": (900, 620, 900, 700)}

# --------------------------------------------------------------------------- DUCT (crawl)
def draw_duct(c, t, u, p):
    rect(c, -3000, -3000, 9000, 9000, "#0b0c10")
    cx, cy = 1000, 600
    end = p.get("end", 0.3)
    for i in range(14, 0, -1):
        k = i / 14; s = 0.12 + k * 1.2
        z = (k + t * 0.15) % 1
        s = 0.1 + z * 1.4
        rect(c, cx - 700 * s, cy - 450 * s, 1400 * s, 900 * s, "#5a636b", int(60 + 120 * z), stroke=10 * s + 2)
    radial(c, cx, cy, 260, "#fff3c8", int(255 * end))
    rect(c, cx - 70, cy - 45, 140, 90, "#fff6d8", int(255 * end))
    for ch in p.get("chars", []):
        x = anim_x(ch, u)
        c.save(); c.translate(x, 1050); c.rotate(-90 * 0)
        draw_kid(c, ch["who"], 0, 0, t + ch.get("toff", 0), "sneak", 1, ch.get("expr", "determined"), (0, -1), ch.get("scale", 1.0), rot=0)
        c.restore()
    darkness(c, 0, 0, 0.35, [("glow", cx, cy, 900, 0.8)])

DCAM = {"wide": (1000, 700, 1600, 1100), "light": (1000, 600, 800, 600)}

# --------------------------------------------------------------------------- ROOF (morning)
def draw_roof(c, t, u, p):
    draw_city(c, t, u, {"mood": "morning", "cars": True, "seed": 8})
    rect(c, -3000, 1000, 9000, 900, "#6a5a52"); rect(c, -3000, 1000, 9000, 30, "#4a3e38")
    rect(c, 300, 820, 200, 180, "#7d8792"); rect(c, 300, 820, 200, 180, OUTLINE, stroke=6)  # vent exit
    # fire escape at right edge
    if p.get("ladder"):
        for yy in range(1000, 1800, 60): line(c, 2600, yy, 2760, yy, "#3b3f4a", 10)
        line(c, 2600, 1000, 2600, 1800, OUTLINE, 12); line(c, 2760, 1000, 2760, 1800, OUTLINE, 12)
    for ch in p.get("chars", []):
        x = anim_x(ch, u)
        y = ch.get("y", 1000); y1 = ch.get("y1", y); yy = lerp(y, y1, ease(u))
        draw_kid(c, ch["who"], x, yy, t + ch.get("toff", 0), ch.get("pose", "stand"), ch.get("face", 1), ch.get("expr", "neutral"),
                 ch.get("look", (1, 0)), ch.get("scale", 1.0), carry=ch.get("carry"))
    overlays(c, t, u, p)
    if p.get("birds"):
        for k in range(4):
            bx = (t * 160 + k * 300) % 3000; by = 200 + k * 50 + math.sin(t * 3 + k) * 20
            path = skia.Path(); path.moveTo(bx - 30, by); path.quadTo(bx - 15, by - 20 * abs(math.sin(t * 8 + k)), bx, by); path.quadTo(bx + 15, by - 20 * abs(math.sin(t * 8 + k)), bx + 30, by)
            c.drawPath(path, P(OUTLINE, 255, 6))

FCAM = {"wide": (1500, 650, 2400, 1150), "kids": (900, 760, 1000, 800), "city": (1700, 500, 2000, 900),
        "ladder": (2500, 1000, 1100, 1000)}

WORLDS = {"kitchen": (draw_kitchen, KCAM), "pantry": (draw_pantry, PCAM), "street": (draw_street, SCAM),
          "city": (draw_city, CCAM), "garden": (draw_garden, GCAM), "radio": (draw_radio, RCAM),
          "duct": (draw_duct, DCAM), "roof": (draw_roof, FCAM)}
