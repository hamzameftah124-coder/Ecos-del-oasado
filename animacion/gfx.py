# Drawing primitives, characters and props (cartoon style) using skia
import skia, math, random

FONT_BLACK = skia.Typeface.MakeFromFile("/usr/share/fonts/opentype/montserrat/Montserrat-Black.otf")
FONT_BOLD = skia.Typeface.MakeFromFile("/usr/share/fonts/opentype/montserrat/Montserrat-ExtraBold.otf")

def col(h, a=255):
    h = h.lstrip("#")
    return skia.ColorSetARGB(int(a), int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

def P(color="#000000", a=255, stroke=0, cap=True, blur=0):
    p = skia.Paint(AntiAlias=True)
    p.setColor(col(color, a) if isinstance(color, str) else color)
    if stroke:
        p.setStyle(skia.Paint.kStroke_Style)
        p.setStrokeWidth(stroke)
        if cap:
            p.setStrokeCap(skia.Paint.kRound_Cap)
            p.setStrokeJoin(skia.Paint.kRound_Join)
    if blur:
        p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    return p

def lerp(a, b, u): return a + (b - a) * u
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(u):
    u = clamp(u); return u * u * (3 - 2 * u)
def ease_out(u):
    u = clamp(u); return 1 - (1 - u) ** 3
def back_out(u):
    u = clamp(u); c = 1.70158
    return 1 + (c + 1) * (u - 1) ** 3 + c * (u - 1) ** 2
def mixc(c1, c2, u):
    c1 = c1.lstrip("#"); c2 = c2.lstrip("#")
    r = [int(lerp(int(c1[i:i+2], 16), int(c2[i:i+2], 16), clamp(u))) for i in (0, 2, 4)]
    return "#%02x%02x%02x" % tuple(r)

OUTLINE = "#1d1a22"

def rect(c, x, y, w, h, color, a=255, r=0, stroke=0):
    p = P(color, a, stroke)
    rr = skia.Rect.MakeXYWH(x, y, w, h)
    if r: c.drawRRect(skia.RRect.MakeRectXY(rr, r, r), p)
    else: c.drawRect(rr, p)

def rect_o(c, x, y, w, h, color, r=0, ow=6, a=255):
    rect(c, x, y, w, h, color, a, r)
    rect(c, x, y, w, h, OUTLINE, a, r, stroke=ow)

def circle(c, x, y, r, color, a=255, stroke=0):
    c.drawCircle(x, y, r, P(color, a, stroke))

def oval(c, x, y, rx, ry, color, a=255, stroke=0):
    c.drawOval(skia.Rect.MakeLTRB(x - rx, y - ry, x + rx, y + ry), P(color, a, stroke))

def line(c, x0, y0, x1, y1, color, w, a=255):
    c.drawLine(x0, y0, x1, y1, P(color, a, w))

def poly(c, pts, color, a=255, stroke=0, close=True):
    path = skia.Path(); path.moveTo(*pts[0])
    for q in pts[1:]: path.lineTo(*q)
    if close: path.close()
    c.drawPath(path, P(color, a, stroke))

def lin_grad(c, x, y, w, h, c0, c1, vertical=True, a0=255, a1=255):
    p = skia.Paint(AntiAlias=True)
    pts = [skia.Point(x, y), skia.Point(x, y + h)] if vertical else [skia.Point(x, y), skia.Point(x + w, y)]
    p.setShader(skia.GradientShader.MakeLinear(pts, [col(c0, a0), col(c1, a1)]))
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), p)

def radial(c, x, y, r, c0, a0, c1="#000000", a1=0):
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeRadial(skia.Point(x, y), max(r, 1), [col(c0, a0), col(c1, a1)]))
    c.drawCircle(x, y, r, p)

def text(c, s, x, y, size, color="#ffffff", font=None, align="center", a=255, stroke=0, stroke_color="#000000"):
    f = skia.Font(font or FONT_BLACK, size)
    w = f.measureText(s)
    if align == "center": x -= w / 2
    elif align == "right": x -= w
    if stroke:
        c.drawString(s, x, y, f, P(stroke_color, a, stroke))
    c.drawString(s, x, y, f, P(color, a))
    return w

def measure(s, size, font=None):
    return skia.Font(font or FONT_BLACK, size).measureText(s)

# ------------------------------------------------------------------ characters
KIDS = {
    "J": dict(h=1.0, jacket="#3f8a5f", jacket2="#2f6a48", pants="#2b3950", skin="#f2c59c", hair="#3a271c", shoe="#1f1f26"),
    "L": dict(h=0.84, jacket="#ea8034", jacket2="#c9652a", pants="#36506b", skin="#f6cfa6", hair="#9a6233", shoe="#2a2324"),
}

def limb(c, x0, y0, x1, y1, x2, y2, color, w):
    path = skia.Path(); path.moveTo(x0, y0); path.quadTo(x1, y1, x2, y2)
    c.drawPath(path, P(OUTLINE, 255, w + 7))
    c.drawPath(path, P(color, 255, w))

def draw_kid(c, who, x, y, t=0.0, pose="stand", face=1, expr="neutral", look=(1, 0), scale=1.0,
             flashlight=False, light_on=True, carry=None, rot=0.0, alpha=255):
    k = KIDS[who]; s = k["h"] * scale
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s * face, s)
    ph = t * 7.0
    bob = 0; legA = legB = 0; armA = armB = 0; lean = 0; crouch = 0
    if pose == "walk":
        legA = math.sin(ph) * 28; legB = -legA; armA = -math.sin(ph) * 30; armB = -armA; bob = abs(math.sin(ph)) * -6
    elif pose == "run":
        ph = t * 11; legA = math.sin(ph) * 45; legB = -legA; armA = -math.sin(ph) * 50; armB = -armA; bob = abs(math.sin(ph)) * -10; lean = 10
    elif pose == "sneak":
        ph = t * 2.2; legA = math.sin(ph) * 16; legB = -legA; bob = abs(math.sin(ph)) * -3; lean = 4
    elif pose == "crouch":
        crouch = 60
    elif pose == "sit":
        crouch = 95
    elif pose == "push":
        ph = t * 3; legA = math.sin(ph) * 14; legB = -legA; lean = 22
    elif pose == "idle":
        bob = math.sin(t * 2) * 2
    c.translate(0, bob)
    hip_y = -150 + crouch
    # legs
    for i, lg in enumerate((legA, legB)):
        col_p = k["pants"] if i == 0 else mixc(k["pants"], "#000000", 0.15)
        if pose == "sit":
            limb(c, -10 + i * 16, hip_y, 40, hip_y + 10, 70 + i * 10, -6, col_p, 30)
            oval(c, 80 + i * 10, -10, 22, 13, k["shoe"])
        elif pose == "lie":
            pass
        else:
            kx = lg * 0.5 + (crouch * 0.6)
            fx = lg
            limb(c, -6 + i * 12, hip_y, kx - 4 + i * 12, (hip_y) / 2 - crouch * 0.1, fx - 4 + i * 12, -12, col_p, 30)
            oval(c, fx + 6 + i * 12, -10, 25, 13, k["shoe"])
            c.drawOval(skia.Rect.MakeLTRB(fx - 19 + i * 12, -23, fx + 31 + i * 12, 3), P(OUTLINE, 255, 5))
    c.save(); c.translate(0, hip_y); c.rotate(lean)
    # back arm
    def arm(angle, front, carry_mode=None):
        sx, sy = 4, -120
        if carry_mode == "forward":
            ex, ey = 70, -95; mx, my = 40, -85
        elif carry_mode == "up":
            ex, ey = 30 + (8 if front else -8), -235; mx, my = 30, -180
        elif carry_mode == "chin":
            ex, ey = 34, -150; mx, my = 60, -90
        elif carry_mode == "hold":
            ex, ey = 55, -80; mx, my = 50, -60
        elif carry_mode == "tight":
            ex, ey = 10, -45; mx, my = 14, -80
        else:
            a = math.radians(angle)
            ex, ey = sx + math.sin(a) * 105, sy + math.cos(a) * 105
            mx, my = sx + math.sin(a) * 50 + 6, sy + math.cos(a) * 50
        colr = k["jacket"] if front else k["jacket2"]
        limb(c, sx, sy, mx, my, ex, ey, colr, 26)
        circle(c, ex, ey, 14, OUTLINE); circle(c, ex, ey, 11, k["skin"])
        return ex, ey
    am = None
    if pose in ("push",): am = "forward"
    if pose == "scared": am = "up"
    if pose == "think": am = "chin"
    if carry == "bottles": am = "hold"
    if pose == "sneak": am = "tight"
    arm(armB, False, am if am not in ("chin",) else None)
    # torso
    path = skia.Path()
    path.moveTo(-34, 0); path.lineTo(-38, -120); path.quadTo(-36, -150, 0, -152); path.quadTo(36, -150, 38, -120); path.lineTo(34, 0); path.close()
    c.drawPath(path, P(k["jacket"])); c.drawPath(path, P(OUTLINE, 255, 7))
    if who == "L":
        poly(c, [(-20, -150), (0, -120), (20, -150)], k["jacket2"])  # hood
        line(c, 8, -120, 8, -70, "#fbe1c4", 4)
    else:
        line(c, 0, -148, 0, -6, k["jacket2"], 5)
        rect(c, -30, -62, 20, 18, k["jacket2"], r=4)
    # head
    hy = -205
    circle(c, 4, hy, 66, OUTLINE); circle(c, 4, hy, 60, k["skin"])
    # hair
    hp = skia.Path()
    if who == "J":
        hp.moveTo(-58, hy - 4); hp.quadTo(-60, hy - 76, 10, hy - 70); hp.quadTo(70, hy - 66, 64, hy - 12)
        hp.quadTo(40, hy - 44, 0, hy - 38); hp.quadTo(-30, hy - 30, -58, hy - 4); hp.close()
    else:
        hp.moveTo(-58, hy + 4); hp.lineTo(-66, hy - 40); hp.lineTo(-40, hy - 50); hp.lineTo(-38, hy - 78); hp.lineTo(-6, hy - 64)
        hp.lineTo(14, hy - 84); hp.lineTo(30, hy - 62); hp.lineTo(62, hy - 66); hp.lineTo(56, hy - 32); hp.lineTo(68, hy - 10)
        hp.quadTo(30, hy - 40, -10, hy - 34); hp.quadTo(-40, hy - 26, -58, hy + 4); hp.close()
    c.drawPath(hp, P(k["hair"])); c.drawPath(hp, P(OUTLINE, 255, 6))
    # ear
    circle(c, -46, hy + 6, 13, k["skin"]); circle(c, -46, hy + 6, 13, OUTLINE, stroke=5)
    # eyes
    lx, ly = look
    blink = (math.fmod(t + (0.7 if who == "L" else 0.0), 3.3) < 0.12)
    big = 1.35 if expr in ("scared", "shock") else 1.0
    for ex in (14, 44):
        if blink and expr not in ("scared", "shock"):
            line(c, ex - 9, hy - 6, ex + 9, hy - 6, OUTLINE, 5)
        else:
            oval(c, ex, hy - 8, 11 * big, 14 * big, "#ffffff"); oval(c, ex, hy - 8, 11 * big, 14 * big, OUTLINE, stroke=4)
            circle(c, ex + lx * 4, hy - 8 + ly * 5, 6, OUTLINE)
            circle(c, ex + lx * 4 + 2, hy - 11 + ly * 5, 2, "#ffffff")
    # brows
    if expr in ("worried", "scared", "sad"):
        line(c, 4, hy - 34, 22, hy - 28, OUTLINE, 5); line(c, 52, hy - 34, 36, hy - 28, OUTLINE, 5)
    elif expr in ("determined", "angry"):
        line(c, 4, hy - 34, 22, hy - 26, OUTLINE, 6); line(c, 54, hy - 34, 36, hy - 26, OUTLINE, 6)
    elif expr == "happy":
        line(c, 6, hy - 32, 22, hy - 36, OUTLINE, 5); line(c, 36, hy - 36, 52, hy - 32, OUTLINE, 5)
    # mouth
    my = hy + 28
    if expr in ("scared", "shock"):
        oval(c, 30, my + 2, 10, 14, "#5a1f22"); oval(c, 30, my + 2, 10, 14, OUTLINE, stroke=4)
    elif expr == "happy":
        path = skia.Path(); path.moveTo(16, my - 4); path.quadTo(30, my + 16, 46, my - 4); path.close()
        c.drawPath(path, P("#7a2a2a")); c.drawPath(path, P(OUTLINE, 255, 4))
    elif expr in ("sad", "worried"):
        path = skia.Path(); path.moveTo(18, my + 6); path.quadTo(30, my - 4, 42, my + 6); c.drawPath(path, P(OUTLINE, 255, 5))
    elif expr == "whisper":
        oval(c, 32, my, 6, 5, "#5a1f22")
    else:
        line(c, 20, my, 40, my, OUTLINE, 5)
    if expr in ("hungry", "sad"):
        pass
    # front arm
    front_mode = am
    ex, ey = arm(armA, True, front_mode)
    if flashlight:
        c.save(); c.translate(ex, ey); c.rotate(-8)
        rect(c, -6, -12, 52, 24, "#3c4250", r=6); rect(c, -6, -12, 52, 24, OUTLINE, r=6, stroke=4)
        rect(c, 44, -16, 14, 32, "#c9ced8", r=4)
        if light_on: circle(c, 60, 0, 10, "#fff6c8")
        c.restore()
    if carry == "bottles":
        for i in range(3):
            rect(c, ex - 30 + i * 22, ey - 70, 20, 62, "#6fb7e9", 200, r=7); rect(c, ex - 30 + i * 22, ey - 70, 20, 62, OUTLINE, r=7, stroke=3)
            rect(c, ex - 25 + i * 22, ey - 80, 10, 12, "#2f74c0", r=2)
    if carry == "can":
        rect(c, ex - 20, ey - 50, 40, 46, "#d8473a", r=5); rect(c, ex - 20, ey - 50, 40, 46, OUTLINE, r=5, stroke=4)
        rect(c, ex - 20, ey - 36, 40, 14, "#f3e2c0")
    c.restore()
    c.restore()

def flashlight_origin(who, x, y, face=1, scale=1.0):
    s = KIDS[who]["h"] * scale
    return x + 70 * s * face, y + (-150 - 88) * s

# ------------------------------------------------------------------ cockroach
def draw_roach(c, x, y, t=0.0, face=1, scale=1.0, flat=0.0, walking=False, ant_only=False,
               shake=0.0, ant_amp=1.0, ant_raise=0.0, eyes=True, alpha=255, speed=1.0, show_cerci=False, body_alpha=255):
    """x,y = ground point under body center. Body length ~ 520*scale."""
    c.save(); c.translate(x + (math.sin(t * 60) * shake * 6), y); c.scale(scale * face, scale * (1 - 0.55 * flat))
    ph = t * 14 * speed if walking else 0
    body_h = 120
    by = -78  # body center height
    if not ant_only:
        # legs (back layer)
        for i, lx in enumerate((-130, -10, 110)):
            sw = math.sin(ph + i * 2.1) * 22 if walking else 0
            path = skia.Path(); path.moveTo(lx, by + 10); path.lineTo(lx - 40 + sw, by + 30); path.lineTo(lx - 70 + sw, 0)
            c.drawPath(path, P("#3d1a0e", body_alpha, 16));
        # abdomen
        p = skia.Paint(AntiAlias=True)
        p.setShader(skia.GradientShader.MakeLinear([skia.Point(0, by - 70), skia.Point(0, by + 60)], [col("#b0532a", body_alpha), col("#5e2612", body_alpha)]))
        c.drawOval(skia.Rect.MakeLTRB(-250, by - 62, 190, by + 58), p)
        c.drawOval(skia.Rect.MakeLTRB(-250, by - 62, 190, by + 58), P(OUTLINE, body_alpha, 7))
        # wing seam + segments
        line(c, -230, by - 4, 120, by - 10, "#4a1d0d", 4, body_alpha)
        for sx in (-180, -120, -60):
            path = skia.Path(); path.moveTo(sx, by - 50); path.quadTo(sx + 14, by, sx, by + 48)
            c.drawPath(path, P("#6d2c14", body_alpha, 4))
        # shine
        oval(c, -40, by - 38, 120, 12, "#f0a070", 110 if body_alpha == 255 else body_alpha // 2)
        if show_cerci:
            for dy in (-20, 16):
                line(c, -246, by + dy, -300, by + dy * 2.2, "#ffd34d", 12)
                line(c, -246, by + dy, -300, by + dy * 2.2, OUTLINE, 3)
        else:
            for dy in (-16, 14):
                line(c, -246, by + dy, -285, by + dy * 2, "#3d1a0e", 8, body_alpha)
        # pronotum (shield)
        oval(c, 175, by - 6, 70, 56, "#c87a3e", body_alpha); oval(c, 175, by - 6, 70, 56, OUTLINE, body_alpha, stroke=6)
        oval(c, 180, by - 6, 42, 30, "#8a3c18", body_alpha)
        # front legs
        for i, lx in enumerate((-90, 30, 150)):
            sw = math.sin(ph + i * 2.1 + 1.5) * 22 if walking else 0
            path = skia.Path(); path.moveTo(lx, by + 20); path.lineTo(lx + 36 + sw, by + 40); path.lineTo(lx + 62 + sw, 0)
            c.drawPath(path, P(OUTLINE, body_alpha, 22)); c.drawPath(path, P("#6b2e14", body_alpha, 14))
            # little spikes (cartoon)
            line(c, lx + 46 + sw, by + 38, lx + 56 + sw, by + 26, "#6b2e14", 5, body_alpha)
    # head
    hx, hy = 240, by + 8
    if not ant_only:
        oval(c, hx, hy, 40, 34, "#7a3416", body_alpha); oval(c, hx, hy, 40, 34, OUTLINE, body_alpha, stroke=6)
        if eyes:
            for ex, ey in ((hx + 6, hy - 14), (hx + 28, hy - 10)):
                oval(c, ex, ey, 15, 17, "#ffffff", body_alpha); oval(c, ex, ey, 15, 17, OUTLINE, body_alpha, stroke=4)
                circle(c, ex + 5, ey + 2, 7, OUTLINE, body_alpha); circle(c, ex + 7, ey - 1, 2.5, "#ffffff", body_alpha)
    # antennae
    for i, base_a in enumerate((-0.35, -0.05)):
        path = skia.Path(); path.moveTo(hx + 20, hy - 26)
        sway = math.sin(t * 2.6 + i * 1.7) * 0.35 * ant_amp + math.sin(t * 5.3 + i) * 0.1 * ant_amp
        ang = base_a - ant_raise * 0.6 + sway
        L = 430
        mx = hx + 20 + math.cos(ang - 0.5) * L * 0.5; my = hy - 26 + math.sin(ang - 0.5) * L * 0.5
        ex = hx + 20 + math.cos(ang) * L; ey = hy - 26 + math.sin(ang) * L - 60
        path.quadTo(mx, my, ex, ey)
        c.drawPath(path, P(OUTLINE, alpha, 10)); c.drawPath(path, P("#c2672e", alpha, 6))
    c.restore()

def roach_antenna_tips(x, y, t, face=1, scale=1.0, ant_amp=1.0, ant_raise=0.0):
    pts = []
    by = -78; hx, hy = 240, by + 8
    for i, base_a in enumerate((-0.35, -0.05)):
        sway = math.sin(t * 2.6 + i * 1.7) * 0.35 * ant_amp + math.sin(t * 5.3 + i) * 0.1 * ant_amp
        ang = base_a - ant_raise * 0.6 + sway
        ex = hx + 20 + math.cos(ang) * 430; ey = hy - 26 + math.sin(ang) * 430 - 60
        pts.append((x + ex * scale * face, y + ey * scale))
    return pts

def draw_antennae_from(c, x, y, t, face=1, scale=1.0, length=1.0, amp=1.0, alpha=255):
    """Only antennae coming out of a point (for gap reveals)."""
    for i in range(2):
        L = 430 * length
        sway = math.sin(t * 2.4 + i * 1.9) * 0.45 * amp
        ang = -math.pi / 2 + (i - 0.5) * 0.5 + sway
        ex = x + math.cos(ang) * L * face * scale; ey = y + math.sin(ang) * L * scale
        mx = x + math.cos(ang + 0.5 * (1 if i else -1)) * L * 0.5 * scale; my = y + math.sin(ang + 0.4) * L * 0.5 * scale
        path = skia.Path(); path.moveTo(x, y); path.quadTo(mx, my, ex, ey)
        c.drawPath(path, P(OUTLINE, alpha, 11 * scale)); c.drawPath(path, P("#c2672e", alpha, 6 * scale))

# ------------------------------------------------------------------ props
def draw_can(c, x, y, s=1.0, color="#d8473a", open_=False, label="#f3e2c0", tomato=False):
    c.save(); c.translate(x, y); c.scale(s, s)
    rect(c, -30, -80, 60, 80, color, r=6); rect(c, -30, -56, 60, 26, label)
    rect(c, -30, -80, 60, 80, OUTLINE, r=6, stroke=5)
    oval(c, 0, -80, 30, 8, "#cfd3da"); oval(c, 0, -80, 30, 8, OUTLINE, stroke=4)
    if tomato: oval(c, 0, -80, 24, 6, "#c0332a")
    c.restore()

def draw_bottle(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    rect(c, -16, -90, 32, 90, "#79c2ee", 210, r=9); rect(c, -16, -90, 32, 90, OUTLINE, r=9, stroke=4)
    rect(c, -8, -104, 16, 16, "#2f74c0", r=3); rect(c, -16, -60, 32, 18, "#ffffff", 160)
    c.restore()

def draw_sack(c, x, y, s=1.0, color="#c9a46a"):
    c.save(); c.translate(x, y); c.scale(s, s)
    path = skia.Path(); path.moveTo(-60, 0); path.quadTo(-80, -70, -40, -120); path.lineTo(-20, -140); path.lineTo(20, -140)
    path.lineTo(40, -120); path.quadTo(80, -70, 60, 0); path.close()
    c.drawPath(path, P(color)); c.drawPath(path, P(OUTLINE, 255, 6))
    line(c, -24, -124, 24, -124, "#8a6a3a", 6)
    c.restore()

def draw_stove(c, x, y, w=260, h=300, dust=True):
    rect(c, x, y - h, w, h, "#2c2f36", r=8); rect(c, x, y - h, w, h, OUTLINE, r=8, stroke=6)
    rect(c, x + 20, y - h + 80, w - 40, h - 110, "#1e2026", r=6); rect(c, x + 20, y - h + 80, w - 40, h - 110, "#454a55", r=6, stroke=5)
    rect(c, x + 40, y - h + 95, w - 80, 14, "#7b808c", r=7)
    for i in range(3):
        circle(c, x + 50 + i * (w - 100) / 2, y - h + 40, 14, "#6a6f7a"); circle(c, x + 50 + i * (w - 100) / 2, y - h + 40, 14, OUTLINE, stroke=4)
    rect(c, x - 6, y - h - 14, w + 12, 18, "#3b3f49", r=4); rect(c, x - 6, y - h - 14, w + 12, 18, OUTLINE, r=4, stroke=5)
    if dust:
        rnd = random.Random(int(x))
        for _ in range(14):
            circle(c, x + rnd.uniform(10, w - 10), y - h + rnd.uniform(-10, h - 20), rnd.uniform(2, 5), "#9aa0a8", 90)

def draw_table(c, x, y, w=520, h=230, color="#a9b2bd"):
    rect(c, x, y - h, w, 30, color, r=6); rect(c, x, y - h, w, 30, OUTLINE, r=6, stroke=6)
    for lx in (x + 24, x + w - 48):
        rect(c, lx, y - h + 30, 24, h - 30, "#8a939e"); rect(c, lx, y - h + 30, 24, h - 30, OUTLINE, stroke=5)
    rect(c, x + 30, y - 60, w - 60, 10, "#8a939e")

def draw_pot(c, x, y, s=1.0, angle=0.0, color="#9aa3ad"):
    c.save(); c.translate(x, y); c.rotate(angle); c.scale(s, s)
    line(c, 0, -60, 0, 0, "#5b616b", 5)
    path = skia.Path(); path.moveTo(-70, 0); path.lineTo(70, 0); path.quadTo(66, 90, 0, 92); path.quadTo(-66, 90, -70, 0); path.close()
    c.drawPath(path, P(color)); c.drawPath(path, P(OUTLINE, 255, 6))
    line(c, -70, 4, 70, 4, "#c3cad2", 6)
    line(c, 70, 10, 120, -4, OUTLINE, 12); line(c, 70, 10, 120, -4, "#5b616b", 7)
    c.restore()

def draw_fridge(c, x, y, w=280, h=620):
    rect(c, x, y - h, w, h, "#d9dde0", r=24); rect(c, x, y - h, w, h, OUTLINE, r=24, stroke=7)
    line(c, x + 4, y - h + 210, x + w - 4, y - h + 210, OUTLINE, 6)
    rect(c, x + 22, y - h + 110, 18, 80, "#9aa1a8", r=8); rect(c, x + 22, y - h + 250, 18, 120, "#9aa1a8", r=8)
    for i in range(6):
        circle(c, x + 60 + i * 30, y - h + 330 + (i % 3) * 70, 6, "#9e9c8a", 120)

def draw_door(c, x, y, w=180, h=420, open_amt=0.0, color="#7f8994", inner="#0e0f13"):
    rect(c, x, y - h, w, h, inner)
    ww = w * (1 - 0.85 * open_amt)
    rect(c, x, y - h, ww, h, color, r=6); rect(c, x, y - h, ww, h, OUTLINE, r=6, stroke=7)
    if ww > 40:
        rect(c, x + 16, y - h + 30, ww - 32, h - 60, mixc(color, "#000000", 0.12), r=4)
        circle(c, x + ww - 26, y - h / 2, 10, "#d7c37a"); circle(c, x + ww - 26, y - h / 2, 10, OUTLINE, stroke=4)
    rect(c, x - 10, y - h - 10, w + 20, h + 10, OUTLINE, stroke=8)

def draw_cart(c, x, y, s=1.0, tilt=0.0):
    c.save(); c.translate(x, y); c.rotate(tilt); c.scale(s, s)
    for yy in (-210, -90):
        rect(c, -120, yy, 240, 18, "#b8c0c8", r=5); rect(c, -120, yy, 240, 18, OUTLINE, r=5, stroke=5)
    for xx in (-112, 98):
        rect(c, xx, -230, 14, 200, "#8f98a2"); rect(c, xx, -230, 14, 200, OUTLINE, stroke=4)
    line(c, 112, -230, 150, -260, OUTLINE, 12); line(c, 112, -230, 150, -260, "#8f98a2", 7)
    for xx in (-90, 90):
        circle(c, xx, -18, 18, "#2a2d33"); circle(c, xx, -18, 7, "#9aa1a8")
    c.restore()

def draw_bowl(c, x, y, s=1.0, water=1.0, bread=True):
    c.save(); c.translate(x, y); c.scale(s, s)
    path = skia.Path(); path.moveTo(-60, -36); path.lineTo(60, -36); path.quadTo(56, 0, 0, 0); path.quadTo(-56, 0, -60, -36); path.close()
    c.drawPath(path, P("#e8e2d2")); c.drawPath(path, P(OUTLINE, 255, 5))
    if water > 0: oval(c, 0, -36, 56 * water, 8, "#6fc3f0")
    if bread:
        for bx in (-90, 84, 104):
            rect(c, bx - 14, -22, 28, 22, "#e3b061", r=6); rect(c, bx - 14, -22, 28, 22, OUTLINE, r=6, stroke=3)
    c.restore()

def draw_window(c, x, y, w, h, dirt=True, light="#cfe2ee", la=255):
    rect(c, x, y, w, h, light, la);
    if dirt:
        rnd = random.Random(7)
        for _ in range(26):
            circle(c, x + rnd.uniform(0, w), y + rnd.uniform(0, h), rnd.uniform(8, 26), "#6d6a55", 120)
    line(c, x + w / 2, y, x + w / 2, y + h, OUTLINE, 8); line(c, x, y + h / 2, x + w, y + h / 2, OUTLINE, 8)
    rect(c, x, y, w, h, OUTLINE, stroke=10)

def draw_flashlight_obj(c, x, y, angle=0.0, s=1.0, broken=0.0, on=True):
    c.save(); c.translate(x, y); c.rotate(angle); c.scale(s, s)
    if broken > 0:
        c.save(); c.translate(-broken * 60, 0); c.rotate(-broken * 30)
        rect(c, -50, -14, 50, 28, "#3c4250", r=6); rect(c, -50, -14, 50, 28, OUTLINE, r=6, stroke=4); c.restore()
        c.save(); c.translate(broken * 60, 0); c.rotate(broken * 40)
        rect(c, 0, -14, 40, 28, "#3c4250", r=6); rect(c, 36, -18, 14, 36, "#c9ced8", r=4); c.restore()
    else:
        rect(c, -50, -14, 90, 28, "#3c4250", r=6); rect(c, -50, -14, 90, 28, OUTLINE, r=6, stroke=4)
        rect(c, 36, -18, 16, 36, "#c9ced8", r=4)
        if on: circle(c, 54, 0, 10, "#fff6c8")
    c.restore()

# ------------------------------------------------------------------ lighting
def darkness(c, W, H, amount, lights=(), color="#05060c"):
    """lights: list of ('cone', x, y, angle_deg, length, spread_deg, strength) or ('glow', x, y, r, strength)
       or ('rect', x, y, w, h, strength). Coordinates are in current canvas coords (world)."""
    if amount <= 0: return
    c.saveLayer(None, None)
    m = c.getTotalMatrix(); inv = skia.Matrix()
    big = skia.Rect.MakeLTRB(-20000, -20000, 20000, 20000)
    c.drawRect(big, P(color, int(255 * amount)))
    for L in lights:
        p = skia.Paint(AntiAlias=True); p.setBlendMode(skia.BlendMode.kDstOut)
        if L[0] == "cone":
            _, x, y, ang, length, spread, st = L
            p.setShader(skia.GradientShader.MakeRadial(skia.Point(x, y), length, [col("#000000", int(255 * st)), col("#000000", int(200 * st)), col("#000000", 0)], [0.0, 0.6, 1.0]))
            path = skia.Path(); path.moveTo(x, y)
            a0 = math.radians(ang - spread / 2); a1 = math.radians(ang + spread / 2)
            n = 16
            for i in range(n + 1):
                a = a0 + (a1 - a0) * i / n
                path.lineTo(x + math.cos(a) * length, y + math.sin(a) * length)
            path.close()
            p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 18))
            c.drawPath(path, p)
        elif L[0] == "glow":
            _, x, y, r, st = L
            p.setShader(skia.GradientShader.MakeRadial(skia.Point(x, y), r, [col("#000000", int(255 * st)), col("#000000", 0)]))
            c.drawCircle(x, y, r, p)
        elif L[0] == "rect":
            _, x, y, w, h, st = L
            p.setColor(col("#000000", int(255 * st))); p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 40))
            c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), p)
    c.restore()

def light_beam(c, x, y, ang, length, spread, a=70, color="#fff3b0"):
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeRadial(skia.Point(x, y), length, [col(color, a), col(color, 0)]))
    path = skia.Path(); path.moveTo(x, y)
    a0 = math.radians(ang - spread / 2); a1 = math.radians(ang + spread / 2)
    for i in range(13):
        aa = a0 + (a1 - a0) * i / 12
        path.lineTo(x + math.cos(aa) * length, y + math.sin(aa) * length)
    path.close(); c.drawPath(path, p)
