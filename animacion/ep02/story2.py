# Storyboard for "Frozen Supermarket": one list of shot specs per paragraph.
F_ = 1000
def J(x, **k): d = dict(who="J", x=x, winter=1); d.update(k); return d
def L(x, **k): d = dict(who="L", x=x, winter=1); d.update(k); return d
def M(cam, **p): return dict(sc="market", cam=cam, p=p)
def Z(cam, **p): return dict(sc="freezer", cam=cam, p=p)
def F(cam, **p): return dict(sc="fcity", cam=cam, p=p)
def S(name, nosub=False, **p): return dict(sc=name, cam=None, p=p, nosub=nosub)
def box(cx, cy, w, h): return (cx, cy, w, h)
def D(n, temp): return S("dayT", nosub=True, day=n, temp=temp)

BOTH_BED = [J(700, pose="sit", expr="worried"), L(900, pose="sit", face=-1, expr="worried")]

PARAS = [
 # 0 cold open
 [Z("wide", dark=0.5, chars=[J(700, pose="sit", expr="worried", shiver=0.6), L(900, pose="sit", face=-1, expr="scared", shiver=0.6)], bag=False),
  F("wide", dark=0.35, chars=[J(1400, x1=1700, pose="walk", winter=2), L(1250, x1=1550, pose="walk", winter=2, toff=0.3)])],
 # 1 it started on a Tuesday
 [F("sign", mood="white", sign="-5°C", snow=0.2), F("sign", sign="-30°C", snow=0.8), F(("sign", "wide"), sign="-60°C", snow=1.4)],
 # 2 power went out
 [F("walk", chars=[J(900, x1=1300, pose="walk", expr="worried"), L(760, x1=1160, pose="walk", expr="worried", toff=0.3)], market_light=False),
  F(("wide", "sky"), market_light=False, dark=0.5), F("street", market_light=False, wind=3.0, snow=2.0)],
 [D(1, "-60°C")],
 # 4 the air hurts
 [F(box(1300, 700, 700, 700), chars=[L(1300, expr="scared", winter=1, frost=0.4)], wind=2.5), F(box(1300, 640, 500, 500), chars=[L(1300, expr="worried", winter=2, frost=0.8)])],
 # 5 scary part (frostbite)
 [F(box(1300, 700, 700, 700), chars=[J(1300, expr="worried", frost=0.5)]), S("f_frostbite"), F(box(1300, 640, 600, 600), wind=3, chars=[L(1300, expr="scared", frost=0.9, shiver=1)])],
 # 6 a light, supermarket
 [F(("wide", "market")), F("doors", chars=[J(2250, x1=2400, pose="run", expr="determined"), L(2100, x1=2350, pose="run", expr="scared")]), M("doors", door_open=(0.4, 0.0), frost=0.4, chars=[J(380, pose="push", face=-1, expr="determined"), L(560, expr="scared")])],
 # 7 inside: dark aisles, food
 [M("wide", dark=0.7, frost=0.3, chars=[J(700, flashlight=True, beam=5), L(600)]), M("aisle7", dark=0.6, frost=0.3), M("aisle9", dark=0.6, frost=0.3), M(box(1250, 760, 700, 600), dark=0.5, frost=0.3, chars=[L(1250, expr="happy")])],
 # 8 thermometer inside
 [M(box(700, 680, 700, 600), dark=0.55, frost=0.4, chars=[J(780, face=-1, expr="worried", look=(-1, -1))]), M("thermo", dark=0.4, frost=0.5, fx=[("highlight", 560, 640, 120)])],
 [D(2, "-22°C")],
 # 10 wake up, frost on eyelashes
 [M("floor7", dark=0.5, frost=0.6, chars=[J(1150, pose="sit", expr="sad", shiver=0.8), L(1350, pose="sit", face=-1, expr="sad", shiver=0.8)]),
  M(box(1350, 790, 460, 420), dark=0.45, frost=0.7, chars=[L(1350, pose="sit", face=-1, expr="worried", frost=1.0, shiver=1)])],
 # 11 layers
 [M("clothes", dark=0.45, frost=0.5, chars=[J(2900, expr="neutral"), L(3060, expr="neutral", face=-1)]), M(box(2980, 760, 600, 600), dark=0.45, chars=[L(2980, expr="happy", winter=1)])],
 # 12 cotton rule
 [S("f_layers"), S("f_water"), S("f_layers")],
 # 13 Leo stops shaking
 [M(box(2980, 760, 600, 600), dark=0.45, chars=[L(2980, expr="neutral", shiver=1.0)]), M(box(2980, 760, 600, 600), dark=0.45, chars=[L(2980, expr="happy")])],
 [D(3, "-28°C")],
 # 15 staff door, grabs handle
 [M("back", dark=0.55, frost=0.6, chars=[L(2900, x1=3200, pose="walk", expr="neutral")]), M("staff", dark=0.5, frost=0.6, chars=[L(3300, pose="push", expr="neutral", winter=3)]), M("handle", dark=0.4, frost=0.6, handle_ice=True)],
 # 16 hand does not come back
 [M("handle", dark=0.4, handle_ice=True, shake=0.4, chars=[L(3300, pose="push", expr="shock", winter=3)], fx=[("exclaim", 3330, 650)])],
 # 17 metal science
 [S("f_metal"), M("handle", dark=0.4, handle_ice=True, shake=0.3, chars=[L(3300, pose="push", expr="scared", winter=3)]), S("f_metal")],
 # 18 Javier breathes on handle
 [M("staff", dark=0.5, chars=[L(3300, pose="push", expr="scared", winter=3), J(3120, x1=3200, pose="run", expr="worried")]), M("handle", dark=0.4, handle_ice=True, chars=[J(3230, expr="determined")], fx=[("breath_hot", 3360, 735)])],
 # 19 red palm, bandage, gloves
 [M(box(3250, 760, 600, 600), dark=0.45, chars=[L(3200, expr="sad", winter=3), J(3360, face=-1, expr="neutral")]), M(box(3250, 760, 600, 600), dark=0.45, chars=[L(3200, expr="neutral"), J(3360, face=-1, expr="happy")])],
 [D(5, "-35°C")],
 # 21 hungry
 [M("aisle7", dark=0.5, frost=0.7), M(box(1250, 800, 800, 600), dark=0.5, frost=0.7, chars=[J(1150, pose="sit", expr="sad", carry="can"), L(1350, pose="sit", face=-1, expr="sad")])],
 # 22 calories science
 [S("f_calories"), M(box(1250, 800, 800, 600), dark=0.5, frost=0.7, chars=[J(1150, pose="sit", expr="sad", carry="can", shiver=0.8), L(1350, pose="sit", face=-1, expr="sad", shiver=0.8)]), S("f_calories")],
 # 23 idea: sleep in freezer
 [M(box(1250, 760, 700, 600), dark=0.5, frost=0.7, chars=[J(1250, pose="think", expr="neutral")], fx=[("exclaim", 1320, 460)]), M(box(1300, 760, 800, 600), dark=0.5, chars=[L(1200, expr="shock"), J(1400, face=-1, expr="happy")])],
 # 24 walk-in freezer
 [M("freezer", dark=0.5, frost=0.7), M("freezer", dark=0.45, frost=0.7, fx=[("highlight", 3720, 740, 240)])],
 # 25 open door, thermometer -18
 [M("freezer", dark=0.45, freezer_open=(0.0, 0.8), chars=[J(3500, pose="push", expr="determined")]), Z("thermo", dark=0.3, fx=[("highlight", 1300, 560, 110)]), S("f_freezer"), S("f_freezer")],
 # 26 warmest room
 [Z("wide", dark=0.3, door=0.6, chars=[J(1300, x1=1100, pose="walk", face=-1, expr="happy"), L(1450, x1=1250, pose="walk", face=-1, expr="happy")])],
 # 27 drag mattresses, sleep
 [M("back", dark=0.5, chars=[J(3000, x1=3400, pose="push", expr="determined"), L(2850, x1=3250, pose="walk", carry="bottles")]), Z("bed", dark=0.45, bag=True, chars=[J(650, pose="sit"), L(850, pose="sit", face=-1)]), Z("bed", dark=0.6, bag=True, chars=[J(650, pose="sit", expr="neutral"), L(850, pose="sit", face=-1, expr="neutral")], fx=[("zzz", 760, 760)])],
 [D(7, "-18°C")],
 # 29 camping stove
 [Z("wide", dark=0.5, chars=BOTH_BED), M("aisle9", dark=0.5, chars=[L(1850, expr="happy")]), Z("stove", dark=0.45, stove=True, door=(0.4, 0.0), chars=[L(1020, pose="crouch", expr="happy")])],
 # 30 feels amazing, fall asleep
 [Z("stove", dark=0.4, stove=True, pot=True, chars=[L(1000, pose="sit", expr="happy", winter=3)]), Z("wide", dark=0.4, stove=True, pot=True, chars=[J(700, pose="sit", expr="happy", winter=3), L(900, pose="sit", face=-1, expr="happy", winter=3)]),
  Z("wide", dark=0.55, stove=True, co=0.3, chars=[J(700, pose="sit", expr="neutral", winter=3), L(900, pose="sit", face=-1, expr="neutral", winter=3)], fx=[("zzz", 800, 760)])],
 # 31 two hours later: headache
 [Z("faces", dark=0.55, stove=True, co=0.7, blur=0.6, chars=[J(700, pose="sit", expr="worried", winter=3)]), Z("wide", dark=0.55, stove=True, co=0.8, blur=0.8, shake=0.3, chars=[J(700, pose="sit", expr="scared", winter=3), L(900, pose="stand", rot=-90, y=F_ - 60, expr="neutral", winter=3)])],
 # 32 CO science
 [Z("stove", dark=0.5, stove=True, co=0.9), S("f_co"), Z("faces", dark=0.6, stove=True, co=0.9, blur=0.7, chars=[L(850, pose="sit", face=-1, expr="neutral", winter=3)]), S("f_co")],
 # 33 crawls to door, drags Leo
 [Z("door", dark=0.55, co=0.8, blur=0.5, chars=[J(1300, pose="crouch", expr="determined", winter=3)]), Z("door", dark=0.45, co=0.6, door=(0.0, 0.8), chars=[J(1380, pose="push", expr="determined", winter=3)]),
  M("freezer", dark=0.45, freezer_open=0.8, chars=[J(3400, x1=3200, pose="walk", face=-1, expr="determined"), L(3560, x1=3360, rot=-90, y=F_ - 40, expr="neutral")])],
 # 34 Leo coughs
 [M(box(3300, 820, 600, 500), dark=0.45, chars=[L(3300, pose="sit", expr="scared"), J(3450, face=-1, pose="crouch", expr="worried")]), M(box(3300, 820, 600, 500), dark=0.45, chars=[L(3300, pose="sit", expr="sad")])],
 # 35 rule from that day
 [M("freezer", dark=0.45, freezer_open=0.9, stove=(3300, F_), chars=[J(3150, pose="sit", expr="determined")])],
 [D(10, "-33°C")],
 # 37 water runs out, snow
 [M("aisle7", dark=0.5, frost=0.8), M("window", dark=0.45, frost=0.8, chars=[L(830, expr="neutral")]), M(box(830, 700, 500, 500), dark=0.4, frost=0.8, chars=[L(830, expr="happy")])],
 # 38 slap
 [M(box(900, 720, 700, 600), dark=0.4, shake=0.5, chars=[L(830, expr="shock"), J(990, face=-1, expr="angry")])],
 # 39 snow science
 [S("f_snow"), M(box(830, 720, 560, 560), dark=0.4, frost=0.8, chars=[L(830, expr="sad")]), S("f_snow")],
 # 40 melt in pot
 [M("freezer", dark=0.45, freezer_open=0.9, stove=(3300, F_), pot=True, chars=[J(3150, pose="sit"), L(3450, pose="sit", face=-1)]), M(box(3300, 840, 520, 420), dark=0.4, stove=(3300, F_), pot=True)],
 [D(14, "-36°C")],
 # 42 something wrong with Javier
 [Z("wide", dark=0.5, chars=[J(700, expr="sad", look=(0, 1)), L(900, face=-1, expr="worried")]), Z(box(700, 760, 520, 520), dark=0.5, chars=[J(700, expr="neutral", look=(0, 1))])],
 # 43 stopped shivering
 [Z(box(800, 760, 700, 600), dark=0.5, chars=[J(700, expr="neutral"), L(900, face=-1, expr="shock")], fx=[("exclaim", 980, 470)])],
 # 44 hypothermia science
 [Z(box(700, 760, 600, 560), dark=0.5, chars=[J(700, expr="sad")]), S("f_hypo"), Z(box(800, 760, 700, 600), dark=0.5, chars=[J(700, expr="neutral"), L(900, face=-1, expr="worried")]), S("f_hypo"), S("f_hypo")],
 # 45 Leo drags him, sleeping bags
 [Z("wide", dark=0.5, chars=[L(800, pose="push", expr="determined"), J(950, rot=-90, y=F_ - 60)]), Z("bed", dark=0.5, bag=True, chars=[J(650, pose="sit", expr="sad"), L(850, pose="sit", face=-1, expr="determined")])],
 # 46 skin to skin, talks
 [Z("faces", dark=0.55, bag=True, chars=[J(700, pose="sit", expr="sad"), L(850, pose="sit", face=-1, expr="whisper")]), Z("bed", dark=0.6, bag=True, chars=[J(650, pose="sit", expr="sad"), L(850, pose="sit", face=-1, expr="whisper")])],
 # 47 3 am shaking again
 [Z("faces", dark=0.55, bag=True, chars=[J(700, pose="sit", expr="neutral", shiver=1.2), L(850, pose="sit", face=-1, expr="happy")])],
 [D(20, "-31°C")],
 # 49 days blur, batteries
 [M(box(3300, 840, 520, 420), dark=0.45, stove=(3300, F_), pot=True), Z("thermo", dark=0.35), M("thermo", dark=0.4, frost=0.8), M("aisle12", dark=0.65, chars=[L(2450, flashlight=True, on=True, beam=5, expr="neutral")]), S("f_battery")],
 # 50 batteries in jacket
 [M(box(2450, 740, 520, 520), dark=0.55, chars=[L(2450, expr="happy")]), S("f_battery")],
 # 51 building groans
 [M("wide", dark=0.75, frost=0.9, shake=0.3, fx=[("rings", 2000, 400, "#cfe8ff")]), M("mid", dark=0.75, frost=0.9, shake=0.6)],
 [D(25, "-50°C")],
 # 53 radio, static
 [M("aisle12", dark=0.5, chars=[L(2450, expr="neutral")]), Z("wide", dark=0.45, radio=True, chars=[L(900, pose="sit", face=-1, expr="neutral"), J(700, pose="sit")], fx=[("rings", 1070, 820, "#9fd8ff")])],
 # 54 a voice
 [Z(box(1000, 820, 600, 460), dark=0.4, radio=True, chars=[L(900, pose="sit", face=1, expr="shock")], fx=[("rings", 1070, 820, "#ffe28a")])],
 # 55 warming center
 [Z(box(900, 800, 800, 600), dark=0.4, radio=True, chars=[J(760, pose="sit", expr="shock"), L(900, pose="sit", face=-1, expr="happy")]), F("station", station=True, market=False, mood="white", snow=0.6), S("f_route")],
 # 56 8km at -50
 [S("f_route"), F("street", snow=1.6, wind=2.5)],
 # 57 Javier does the math
 [Z(box(800, 760, 700, 600), dark=0.4, chars=[J(760, pose="think", expr="neutral"), L(900, face=-1, expr="worried")]), S("f_frostbite")],
 [D(30, "-31°C")],
 # 59 warmest in a month
 [M("thermo", dark=0.35, frost=0.6, fx=[("highlight", 560, 640, 120)])],
 # 60 dress in layers, goggles
 [M("clothes", dark=0.4, chars=[J(2900, winter=2, goggles=True, expr="determined"), L(3060, face=-1, winter=2, goggles=True, expr="determined")]), M(box(2980, 740, 620, 620), dark=0.4, chars=[L(2980, winter=2, goggles=True)])],
 # 61 walk out into white city
 [M("doors", door_open=(0.0, 0.5), frost=0.6, chars=[J(300, x1=150, pose="walk", face=-1, winter=2, goggles=True), L(420, x1=270, pose="walk", face=-1, winter=2, goggles=True)]),
  F("cars", mood="white", snow=0.5), F("wide", mood="white", snow=0.5, chars=[J(1500, x1=1200, pose="walk", face=-1, winter=2, goggles=True, scale=0.7), L(1620, x1=1320, pose="walk", face=-1, winter=2, goggles=True, scale=0.7)])],
 # 62 walk north
 [F("walk", mood="white", snow=1.0, wind=2.0, chars=[J(1100, x1=1500, pose="walk", winter=2, goggles=True), L(950, x1=1350, pose="walk", winter=2, goggles=True, toff=0.3)])],
 # 63 they see station
 [F(("street", "station"), mood="white", station=True, snow=0.8), F("station", mood="white", station=True, snow=0.6, chars=[J(3500, winter=2, goggles=True, expr="happy"), L(3380, winter=2, goggles=True, expr="happy")])],
 # 64 Leo starts running
 [F("station", mood="white", station=True, snow=0.6, chars=[L(3400, x1=3800, pose="run", winter=2, goggles=True, expr="happy")])],
 # 65 footprints leading away
 [F(box(3700, 760, 700, 600), mood="white", station=True, chars=[J(3600, winter=2, goggles=True, expr="worried"), L(3720, winter=2, goggles=True)]), F("steps", mood="white", station=True, prints=True, snow=0.4),
  F("steps", mood="white", station=True, prints=True, snow=0.4, fx=[("highlight", 4200, 940, 300)])],
 # 66 nobody going in
 [F("station", mood="white", station=True, prints=True, snow=0.5, dark=0.0, chars=[J(3600, winter=2, goggles=True, expr="scared"), L(3720, winter=2, goggles=True, expr="scared")])],
 # 67 to be continued
 [S("tbc", nosub=True)],
 # 68 comments
 [S("endcard")],
]

# HUD per paragraph range: (first_para, day, temp)
HUD = [(3, 1, "-60°C"), (8, 1, "-22°C"), (9, 2, "-24°C"), (14, 3, "-28°C"), (20, 5, "-35°C"), (25, 5, "-18°C"), (28, 7, "-18°C"),
       (36, 10, "-33°C"), (41, 14, "-36°C"), (48, 20, "-31°C"), (52, 25, "-50°C"), (58, 30, "-31°C"), (67, None, None)]

def build(sent_paras):
    """sent_paras: list of paragraph index per sentence -> SB dict sentence->spec"""
    import copy
    SB = {}
    by_para = {}
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
