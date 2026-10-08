"""Shared layout parameters (mm). Origin = device center, top view, X right, Y toward back (USB side).
Single source of truth for enclosure + PCB placement (pcb/gen_pcb.py imports this file)."""
W = D = 100.0          # outer footprint
H = 30.0               # body height (excluding knob/wheel)
R_CORNER = 24.0        # plan-view corner radius (soft squircle look)
R_TOP = 7.0            # top edge blend radius (pillow edge)
R_DOME = 300.0         # spherical dome radius of top surface (center highest)
R_BOT = 5.0            # bottom edge fillet
CAP_PROUD = 2.2        # caps protrude above local dome surface
WALL = 2.2
SPLIT_Z = 8.0          # bottom/top shell parting plane
PCB_Z = 11.5           # PCB bottom surface (battery 6.5 + floor 2.2 below)
PCB_T = 1.6
PCB_W = 93.0; PCB_R = 19.0   # legacy (unused)
PCB_INSET = 3.2   # PCB outline = enclosure outline inset by wall 2.2 + 1.0 clearance
CLR = 0.25             # radial clearance cap<->hole (FDM 0.3, molding 0.15)
SCREWS = [(-40, 24), (-38, -34), (42, 12), (28, -12)]  # M2x10 self-tapping (PT/K30x10 for plastic)
TACT_H = 5.5            # CAX TS-1102S-6x6x5.5-160 (LCSC C53431191) 6x6 SMD tact, 5.5 mm tall, 160 gf
# buttons: name, kind, x, y, size (w,h) or diameter
BUTTONS = [   # left-hand layout, all key centres >= 18 mm apart (see docs ergonomics section)
  ("top",   "rect",  -6, 31, (34, 13)),   # pill bar under index+middle finger
  ("tr1",   "round", 20, 36, 11),
  ("tr2",   "round", 38, 25, 11),
  ("br",    "round", 36, -5, 11),
  ("side",  "rect", -34, -20, (18, 13)),  # thumb key, lower-left
  ("tall1", "rect",  18, -26, (12, 22)),  # ring finger
  ("tall2", "rect",  36, -25, (12, 18)),  # pinky
]
KNOB = dict(x=0, y=2, d=32, h=11, ring_d=40)   # EC11E w/ switch, 20 mm D shaft
WHEEL = dict(x=-29.5, y=6, d=24, w=8)            # wheel axis along X, driven by mouse encoder at x=-32.5
LED = dict(x=-16, y=20, d=3)                      # light pipe over WS2812B-2020
USB = dict(x=0, w=9.6, h=3.6)                   # USB-C opening in back wall
BATTERY = (6, -2, 50, 34, 6.5)                  # 603450 LiPo pocket (x,y,l,w,t)

import math
DOME_Y0 = 20.0   # dome apex shifted toward the back -> top slopes down toward the palm (front)
def dome_z(x, y):
    """outer top-surface height at (x,y) (ignoring edge blend)"""
    return H - R_DOME + math.sqrt(R_DOME**2 - x*x - (y-DOME_Y0)**2)

# ---------- ergonomic outline: squircle (superellipse n=4.2) with inward "waist" scallops ----------
# front edge (-Y, palm side) has the deepest waist (3.5 mm), sides 2.0 mm, back 1.5 mm (original shape, not a copy)
WAIST = {"front": 5.0, "back": 2.5, "left": 3.0, "right": 3.0}
SUPER_N = 4.2
def outline_pts(offset=0.0, n=64):
    from shapely.geometry import Polygon
    pts = []
    for i in range(720):
        t = 2*math.pi*i/720; c, s = math.cos(t), math.sin(t)
        x = W/2*math.copysign(abs(c)**(2/SUPER_N), c); y = D/2*math.copysign(abs(s)**(2/SUPER_N), s)
        # waist: smooth cos^6 dip centred on each edge midpoint
        dip = WAIST["right"]*max(c,0)**6 + WAIST["left"]*max(-c,0)**6 + WAIST["back"]*max(s,0)**6 + WAIST["front"]*max(-s,0)**6
        dip_w = lambda v: v  # dip applied along normal direction approx (axis)
        x -= math.copysign(1, c)*(WAIST["right"] if c>0 else WAIST["left"])*(abs(c)**12) if False else 0
        r = math.hypot(x, y); pts.append((x*(r-dip)/r, y*(r-dip)/r))
    poly = Polygon(pts)
    if offset: poly = poly.buffer(-offset, join_style=1, resolution=32)
    xy = list(poly.exterior.coords)[:-1]
    step = max(1, len(xy)//n)
    return [(round(x,4), round(y,4)) for x,y in xy[::step]]

# ---------- 3D-print / FDM parameters ----------
FDM_CLR = 0.25          # cap/knob/wheel sliding clearance per side (0.2-0.3 for 0.4 nozzle)
TOP_STEM_DX = 9.0       # long top bar: two plungers at x = -6 +/- 9
SLEEVE = 1.5            # guide sleeve depth below skin for every cap
PRETRAVEL = 0.15        # gap cap bottom -> tact plunger
WHEEL_AXLE_DZ = 7.2     # mouse-encoder axle height above PCB top (VERIFY with purchased encoder)
WHEEL_PIN = (3.0, 14.0) # steel dowel / printed axle  dia x length (wheel stub side)
INSERT = dict(name="M2 x 4 x OD3.5 brass heat-set insert", hole=3.2, depth=5.0, boss_od=6.6)
SCREW = "M2 x 14 DIN912 socket head (head D3.8)"
# PCB tongues: local PCB extensions so USB-C and power switch reach the inner wall
INNER_GAP = 0.2
TONGUES = {"usb": (-6.5, 6.5), "pwr": (25.5, 39.5)}
PWR_X = 31.0
def inner_y_back(x):
    from shapely.geometry import Polygon, LineString
    poly = Polygon(outline_pts(WALL, 400))
    g = LineString([(x, 0), (x, 80)]).intersection(poly.exterior)
    return max(p.y for p in getattr(g, "geoms", [g]))
def pcb_outline_pts(n=120):
    from shapely.geometry import Polygon, box
    poly = Polygon(outline_pts(PCB_INSET, 400))
    for x0, x1 in TONGUES.values():
        poly = poly.union(box(x0, 30, x1, inner_y_back((x0+x1)/2) - INNER_GAP).intersection(Polygon(outline_pts(WALL + INNER_GAP, 400))))
    poly = poly.buffer(0.5, join_style=1).buffer(-0.5, join_style=1).simplify(0.03)   # round tongue corners
    return [(round(x,4), round(y,4)) for x,y in list(poly.exterior.coords)[:-1]]
