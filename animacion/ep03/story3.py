F_ = 1000
def J(x, **k): d = dict(who="J", x=x, winter=2, goggles=True); d.update(k); return d
def L(x, **k): d = dict(who="L", x=x, winter=2, goggles=True); d.update(k); return d
def Jf(x, **k): d = dict(who="J", x=x, winter=1); d.update(k); return d
def Lf(x, **k): d = dict(who="L", x=x, winter=1); d.update(k); return d
def W(sc, cam, **p): return dict(sc=sc, cam=cam, p=p)
def F(cam, **p): return dict(sc="fcity", cam=cam, p=p)
def ST(cam, **p): return dict(sc="station", cam=cam, p=p)
def CV(cam, **p): return dict(sc="cave", cam=cam, p=p)
def MT(cam, **p): return dict(sc="metro", cam=cam, p=p)
def S(name, nosub=False, **p): return dict(sc=name, cam=None, p=p, nosub=nosub)
def box(cx, cy, w, h): return (cx, cy, w, h)
def D(n, temp): return S("dayT", nosub=True, day=n, temp=temp)

PARAS = [
 # 0 cold open: snow weight
 [ST("roof", bend=0.6, rshake=0.5, dust=True), ST("wide", bend=0.3), S("f_snowload"), F("station", station=True, market=False, mood="white", prints=True, chars=[J(3600, expr="scared"), L(3720, expr="scared")])],
 # 1 recap
 [F("sign", sign="-60°C"), W("freezer", "bed", dark=0.5, bag=True, chars=[Jf(650, pose="sit"), Lf(850, pose="sit", face=-1)]), W("freezer", box(1000, 820, 600, 460), dark=0.4, radio=True, chars=[Lf(900, pose="sit", face=1, expr="shock")]),
  F("steps", mood="white", station=True, prints=True, fx=[("highlight", 4200, 940, 300)])],
 # 2 nobody going in
 [F("station", mood="white", station=True, prints=True, chars=[J(3600, expr="scared"), L(3720, expr="scared")])],
 [D(30, "-50°C")],
 # 4 inside station, warm, abandoned
 [ST("doors", chars=[J(3100, x1=2900, pose="walk", face=-1, expr="happy"), L(3240, x1=3040, pose="walk", face=-1, expr="happy")]), ST("barrel"), ST("bench"), ST("bear")],
 # 5 nobody here
 [ST("wide", chars=[J(2700, face=-1, expr="worried"), L(2850, face=-1, expr="worried")])],
 # 6 Leo eats, groan
 [ST(box(1450, 820, 700, 600), chars=[Lf(1400, pose="sit", expr="happy", carry="can")]), ST("mid", chars=[Jf(1700, x1=1800, pose="walk", expr="worried")], rshake=0.3), ST(box(1800, 740, 600, 600), chars=[Jf(1800, expr="worried", look=(0, -1))], rshake=0.6, fx=[("rings", 1800, 200, "#ffd77a")])],
 # 7 beams bending
 [ST(box(1800, 740, 600, 600), chars=[Jf(1800, expr="shock", look=(0, -1))]), ST("roof", bend=(0.3, 0.7), rshake=0.4), ST("roof", bend=0.8, rshake=0.8, dust=True)],
 # 8 science snow load
 [S("f_snowload"), ST("roof", bend=0.85, rshake=0.6, dust=True), S("f_snowload")],
 # 9 that's why
 [ST("wide", bend=0.9, rshake=0.8, dust=True, chars=[Jf(1800, expr="scared", look=(0, -1)), Lf(1400, pose="sit", expr="neutral", carry="can")])],
 # 10 crack, dust, grabs Leo
 [ST("roof", bend=1.0, rshake=1.2, dust=True, shake=0.6), ST(box(1500, 780, 700, 640), bend=1.0, dust=True, shake=0.5, chars=[Jf(1600, pose="run", face=-1, expr="scared"), Lf(1420, expr="shock")])],
 # 11 run, collapse
 [ST("mid", bend=1.0, dust=True, shake=1.0, chars=[Jf(1700, x1=2900, pose="run", expr="scared"), Lf(1550, x1=2750, pose="run", expr="scared", toff=0.3)]), ST("wide", collapse=True, bend=1.0, shake=1.5),
  F("station", mood="white", station=False, collapsed=True, snow=1.5, shake=1.0, chars=[J(3300, x1=3100, pose="run", face=-1), L(3150, x1=2950, pose="run", face=-1)])],
 # 12 silence, gone
 [F("station", mood="white", collapsed=True, snow=0.6, chars=[J(3000, face=1, expr="shock"), L(2880, face=1, expr="shock")])],
 [D(30, "-45°C")],
 # 14 getting dark, no shelter
 [F("wide", dark=0.45, snow=1.2, chars=[J(1400, expr="worried"), L(1260, expr="scared", shiver=0.8)], market=False), F(box(1330, 700, 700, 700), dark=0.4, chars=[J(1400, expr="worried"), L(1260, expr="scared", shiver=1.0)], market=False)],
 # 15 Javier digs
 [CV("dig", build=(0.1, 0.4), dug=0, chars=[J(450, pose="crouch", expr="determined")]), CV("dig", build=0.4, dug=0, chars=[L(300, expr="shock")])],
 # 16 snow insulation science
 [S("f_insulation"), CV("wide", build=0.7, dug=0), S("f_insulation")],
 # 17 mound, tunnel, hole
 [CV("wide", build=(0.6, 1.0), dug=0, chars=[J(300, pose="push", expr="determined")]), CV("wide", build=1.0, dug=(0.2, 1.0)), CV("hole", build=1.0, dug=1.0, hole=True)],
 # 18 air hole science
 [CV("hole", build=1.0, dug=1.0, hole=True), S("f_airhole")],
 # 19 candle, warms up
 [CV("inside", build=1.0, dug=1.0, hole=True, candle=True, chars=[Jf(840, pose="sit", scale=0.8), Lf(1060, pose="sit", face=-1, scale=0.8)]), CV("wide", build=1.0, dug=1.0, hole=True, candle=True, chars=[Jf(840, pose="sit", scale=0.8), Lf(1060, pose="sit", face=-1, scale=0.8)])],
 # 20 stop shaking
 [CV("inside", build=1.0, dug=1.0, hole=True, candle=True, chars=[Jf(840, pose="sit", scale=0.8, expr="happy"), Lf(1060, pose="sit", face=-1, scale=0.8, expr="happy")])],
 [D(31, "-48°C")],
 # 22 follow footprints
 [F("steps", mood="white", collapsed=True, prints=True, snow=1.2), F("walk", mood="white", snow=1.8, wind=3, chars=[J(1100, x1=1400, pose="walk"), L(950, x1=1250, pose="walk", toff=0.3)])],
 # 23 whiteout
 [F("walk", mood="white", whiteout=0.6, snow=2.0, chars=[J(1250, pose="walk", expr="scared"), L(1100, pose="walk", expr="scared")]), F("wide", mood="white", whiteout=0.85, snow=2.0), F("walk", mood="white", whiteout=0.75, chars=[J(1250, expr="worried", look=(-1, 0)), L(1100, expr="scared")])],
 # 24 walking in circles science
 [S("f_circles"), F("walk", mood="white", whiteout=0.8, chars=[J(1250, x1=1100, pose="walk", face=-1), L(1100, x1=950, pose="walk", face=-1)]), S("f_circles")],
 # 25 hold backpack, rails
 [F("walk", mood="white", whiteout=0.6, chars=[J(1250, expr="determined"), L(1120, expr="worried")]), F("street", mood="white", whiteout=0.5, rails=True), F("walk", mood="white", whiteout=0.5, rails=True, chars=[J(1100, x1=1500, pose="walk", expr="determined"), L(970, x1=1370, pose="walk")])],
 [D(32, "-46°C")],
 # 27 Leo limping, second shelter, boots off
 [F("walk", mood="white", rails=True, chars=[L(1200, x1=1400, pose="sneak", expr="sad"), J(1350, x1=1550, pose="walk")]), CV("inside", build=1.0, dug=1.0, candle=True, chars=[Jf(840, pose="sit", scale=0.8, expr="worried"), Lf(1060, pose="sit", face=-1, scale=0.8, expr="sad")])],
 # 28 white waxy toes
 [CV(box(1060, 900, 360, 260), build=1.0, dug=1.0, candle=True, chars=[Lf(1060, pose="sit", face=-1, scale=0.8, expr="scared")], fx=[("highlight", 1130, 990, 70)])],
 # 29 frostbite rules
 [S("f_frost"), CV("inside", build=1.0, dug=1.0, candle=True, chars=[Jf(840, pose="sit", scale=0.8, expr="worried"), Lf(1060, pose="sit", face=-1, scale=0.8, expr="scared")]), S("f_frost")],
 # 30 feet on stomach
 [CV("inside", build=1.0, dug=1.0, candle=True, chars=[Jf(880, pose="crouch", scale=0.8, expr="determined"), Lf(1060, pose="sit", face=-1, scale=0.8, expr="sad")])],
 # 31 pain is back
 [CV("inside", build=1.0, dug=1.0, candle=True, shake=0.4, chars=[Lf(1060, pose="sit", face=-1, scale=0.8, expr="shock")], fx=[("exclaim", 1090, 760)]), CV("inside", build=1.0, dug=1.0, candle=True, chars=[Jf(840, pose="sit", scale=0.8, expr="happy"), Lf(1060, pose="sit", face=-1, scale=0.8, expr="sad")])],
 [D(33, "-44°C")],
 # 33 metro entrance
 [F("wide", mood="white", rails=True, market=False, metro=True, snow=0.6), F(box(2450, 760, 900, 700), mood="white", market=False, metro=True, chars=[J(2000, expr="shock"), L(1880, expr="shock")])],
 # 34 down the stairs, warmer
 [MT("stairs", dark=0.6, crowd=0, chars=[J(300, x1=420, pose="walk", y=700, y1=900), L(200, x1=320, pose="walk", y=640, y1=850)]), MT("stairs", dark=0.5, crowd=0, chars=[J(480, pose="walk", expr="neutral"), L(360, pose="walk", expr="neutral")])],
 # 35 ground warmer science
 [S("f_ground"), S("f_ground")],
 # 36 light, people
 [MT("wide", dark=0.35), MT("crowd", dark=0.3), MT("wall", dark=0.35), MT("brothers", dark=0.35, chars=[J(900, expr="shock"), L(1050, face=-1, expr="happy")])],
 # 37 woman with blankets
 [MT("woman", dark=0.3, woman=1350, gap=1300, chars=[J(1000, expr="neutral"), L(1130, expr="shock")]), MT("woman", dark=0.3, woman=1300, gap=1300, chars=[L(1130, expr="happy")])],
 # 38 Leo crying, Javier sits
 [MT("brothers", dark=0.35, chars=[Jf(900, pose="sit", expr="sad"), Lf(1050, face=-1, expr="sad")]), MT(box(900, 840, 520, 460), dark=0.35, chars=[Jf(900, pose="sit", expr="happy")])],
 # 39 they made it
 [MT("wide", dark=0.3, chars=[Jf(900, pose="sit", expr="happy"), Lf(1050, pose="sit", face=-1, expr="happy")])],
 [D(35, "-41°C")],
 # 41 shouting, radio
 [MT("radio", dark=0.35, radio_table=True, fx=[("rings", 2450, 800, "#ffe28a")]), MT("crowd", dark=0.35, radio_table=True, shake=0.2)],
 # 42 warm air coming
 [MT("radio", dark=0.35, radio_table=True, fx=[("rings", 2450, 800, "#ffe28a")]), S("f_thaw")],
 # 43 people cheer
 [MT("crowd", dark=0.3, chars=[Lf(1500, expr="happy", y=980, y1=940)]), MT("brothers", dark=0.3, chars=[Lf(1050, face=-1, expr="happy")])],
 # 44 Javier not smiling, looks at walls/snow
 [MT(box(900, 800, 520, 520), dark=0.35, chars=[Jf(900, expr="worried", look=(1, -1))]), MT("wall", dark=0.35), F("wide", mood="white", market=False, metro=True, snow=0.3)],
 # 45 doing the math
 [MT(box(900, 800, 520, 520), dark=0.4, chars=[Jf(900, pose="think", expr="worried")], fx=[("question", 1000, 520)])],
 # 46 snow melts, water
 [S("f_thaw"), MT("wall", dark=0.4, water=0.4)],
 # 47 down
 [MT("wall", dark=0.45, water=0.8)],
 # 48 into tunnels
 [MT("wide", dark=0.45, water=1.0, shake=0.3, chars=[Jf(900, expr="scared"), Lf(1050, face=-1, expr="scared")])],
 # 49 tbc
 [S("tbc", nosub=True)],
 # 50 comments
 [S("endcard")],
]

HUD = [(3, 30, "-50°C"), (13, 30, "-45°C"), (21, 31, "-48°C"), (26, 32, "-46°C"), (32, 33, "-44°C"), (40, 35, "-41°C"), (49, None, None)]

def build(sent_paras):
    import copy
    SB = {}; by_para = {}
    for k, pi in enumerate(sent_paras): by_para.setdefault(pi, []).append(k)
    for pi, ks in by_para.items():
        specs = PARAS[pi]; m = len(ks); n = len(specs)
        hud = None
        for fp, d, tmp in HUD:
            if pi >= fp: hud = (d, tmp) if d else None
        for j, k in enumerate(ks):
            idx = min(n - 1, j * n // m)
            if j > 0 and (j * n // m) == ((j - 1) * n // m):
                SB[k] = "C"; continue
            sp = copy.deepcopy(specs[idx])
            if hud and not sp["sc"].startswith("day"): sp["p"]["hud"] = hud
            SB[k] = sp
    return SB
