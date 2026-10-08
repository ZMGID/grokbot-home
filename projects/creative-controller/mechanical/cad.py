import cadquery as cq, os
from params import *
os.makedirs("out", exist_ok=True)
pcb_top = PCB_Z + PCB_T

def fcut(a, b, tol=1e-3):
    """robust boolean cut (fuzzy tolerance + heal); spline/sphere geometry needs it"""
    r = a.val().cut(b.val(), tol=tol).fix()
    return cq.Workplane(obj=r)
def funion(a, b, tol=1e-3):
    return cq.Workplane(obj=a.val().fuse(b.val(), tol=tol).fix())

def oplan(offset, h, n=64):
    """extruded ergonomic outline (spline through outline_pts), inset by offset"""
    return cq.Workplane("XY").spline(outline_pts(offset, n), periodic=True).close().extrude(h)

def plan(w, d, r, h):
    return cq.Workplane("XY").rect(w, d).extrude(h).edges("|Z").fillet(r)

# ---------- outer body: squircle plan + spherical dome top + pillow edge blend ----------
def dome_solid(offset):
    """solid bounded by plan rounded-square (inset by offset), bottom z=offset, spherical top (lowered by offset)"""
    blk = oplan(offset, H + 20).translate((0, 0, offset))
    sph = cq.Workplane("XY").sphere(R_DOME - offset).translate((0, DOME_Y0, H - R_DOME))
    return blk.intersect(sph)
body = dome_solid(0)
try:
    body = body.faces(">Z").edges().fillet(R_TOP)
except Exception as e: print("top blend fallback", e); body = body.faces(">Z").edges().fillet(4)
body = body.faces("<Z").edges().chamfer(1.6)          # 45 deg chamfer on bed edge (no elephant-foot overhang)
inner = dome_solid(WALL)
try:
    inner = inner.faces(">Z").edges().fillet(R_TOP - WALL)
except Exception as e: print("inner blend fallback", e); inner = inner.faces(">Z").edges().fillet(2)
inner = inner.faces("<Z").edges().chamfer(1.2)         # 45 deg internal floor/wall transition
shell = cq.Workplane(obj=body.cut(inner).val().fix())

C = FDM_CLR
def cap_profile(k, s_, grow=0.0):
    """2D cap footprint (round or rounded-rect / pill) grown by 'grow'"""
    if k == "round": return cq.Workplane("XY").circle(s_/2 + grow)
    w, h = s_[0] + 2*grow, s_[1] + 2*grow
    r = min(min(s_)/2 - 0.6 + grow, min(w, h)/2 - 0.05)
    return cq.Workplane("XY").sketch().rect(w, h).vertices().fillet(r).finalize()
def cap_prism(k, s_, grow, h, z):
    return cap_profile(k, s_, grow).extrude(h).translate((0, 0, z))

top = shell.intersect(cq.Workplane("XY").box(200,200,100,centered=(True,True,False)).translate((0,0,SPLIT_Z)))
bot = shell.intersect(cq.Workplane("XY").box(200,200,SPLIT_Z,centered=(True,True,False)))

# ---- guide sleeves (hang from inner skin) + cap holes ----
for n,k,x,y,s_ in BUTTONS:
    zs = dome_z(x, y); sk = zs - WALL
    sleeve = cap_prism(k, s_, C + 1.2, SLEEVE + 3, sk - SLEEVE).translate((x, y, 0)).intersect(inner.translate((0,0,0.2)))
    top = funion(top, sleeve)
for n,k,x,y,s_ in BUTTONS:
    top = fcut(top, cap_prism(k, s_, C, 60, -10).translate((x, y, 0)))
# knob ring recess + shaft hole
kz = dome_z(KNOB["x"], KNOB["y"])
top = fcut(top, cq.Workplane("XY").circle(KNOB["ring_d"]/2 + C).extrude(10).translate((KNOB["x"],KNOB["y"],kz-1.5)))
top = fcut(top, cq.Workplane("XY").circle(KNOB["d"]/2 + 1.0).extrude(40).translate((KNOB["x"],KNOB["y"],0)))
# wheel slot
top = fcut(top, cq.Workplane("XY").rect(WHEEL["w"] + 2*0.6, 22).extrude(40).edges("|Z").fillet(2).translate((WHEEL["x"],WHEEL["y"],0)))
# LED light-pipe hole (3.0 pipe + 0.15/side) with retention counterbore underneath skin
lz = dome_z(LED["x"], LED["y"])
top = fcut(top, cq.Workplane("XY").circle(1.65).extrude(40).translate((LED["x"],LED["y"],0)))
# ---- USB-C: socket face sits at inner wall; outside counterbore leaves 0.8 mm wall -> plug overmold seats (<=1 mm) ----
uz = pcb_top + 1.63
ywall = inner_y_back(0)
top = fcut(top, cq.Workplane("XZ").rect(USB["w"] + 0.4, USB["h"] + 0.4).extrude(-20).edges("|Y").fillet(1.5).translate((USB["x"], ywall - 5, uz)))
top = fcut(top, cq.Workplane("XZ").rect(13.0, 7.5).extrude(-10).edges("|Y").fillet(2.5).translate((USB["x"], ywall + 0.8, uz)))
# ---- power switch: through slot for printed slider extender (PCM12 at x=PWR_X, actuator toward back wall) ----
pz = pcb_top + 0.75
ypw = inner_y_back(PWR_X)
top = fcut(top, cq.Workplane("XZ").rect(6.5, 3.6).extrude(-12).translate((PWR_X + 0.75, ypw - 2, pz)))
top = fcut(top, cq.Workplane("XZ").rect(11.0, 6.0).extrude(-6).edges("|Y").fillet(2.0).translate((PWR_X + 0.75, ypw + 1.2, pz + 0.6)))  # finger scoop
# ---- heat-set insert bosses (top shell) ----
for x,y in SCREWS:
    boss = cq.Workplane("XY").circle(INSERT["boss_od"]/2).extrude(H - pcb_top).translate((x, y, pcb_top)).intersect(inner.translate((0,0,0.3)))
    top = funion(top, boss)
    depth = min(INSERT["depth"], dome_z(x, y) - WALL - pcb_top - 0.8)
    top = fcut(top, cq.Workplane("XY").circle(INSERT["hole"]/2).extrude(depth).translate((x, y, pcb_top - 0.01)))
    top = fcut(top, cq.Workplane("XY").circle(INSERT["hole"]/2 + 0.4).extrude(0.6).faces("<Z").chamfer(0.39).translate((x, y, pcb_top - 0.01)) if False else
               cq.Workplane("XY").circle(INSERT["hole"]/2 + 0.3).extrude(0.4).translate((x, y, pcb_top - 0.01)))   # lead-in
# ---- scroll-wheel bearing lug (integral to top shell, open U-slot so the wheel pin drops in from below) ----
wz = pcb_top + WHEEL_AXLE_DZ
lug_x0 = WHEEL["x"] - WHEEL["w"]/2 - 0.7 - 2.4
lug = cq.Workplane("XY").box(2.4, 9.0, 40, centered=(False, True, False)).translate((lug_x0, WHEEL["y"], wz - 3.5)).intersect(inner.translate((0,0,0.3)))
slot_w = WHEEL_PIN[0] + 0.3
slot = (cq.Workplane("YZ").polyline([(-slot_w/2, -10), (slot_w/2, -10), (slot_w/2, 0.9), (0, 0.9 + slot_w/2), (-slot_w/2, 0.9)]).close()
        .extrude(4).translate((lug_x0 - 0.8, WHEEL["y"], wz)))     # teardrop roof (45 deg), 0.9 mm press travel
top = fcut(funion(top, lug), slot)

# ---- bottom shell: insert-screw through holes, counterbores, battery rib, lip, feet ----
for x,y in SCREWS:
    bot = funion(bot, cq.Workplane("XY").circle(INSERT["boss_od"]/2).extrude(PCB_Z - WALL).translate((x, y, WALL)))
    bot = fcut(bot, cq.Workplane("XY").circle(1.2).extrude(40).translate((x, y, -1)))
    bot = fcut(bot, cq.Workplane("XY").circle(2.2).extrude(2.4).translate((x, y, -0.01)))      # M2 socket head counterbore
bx,by,bl,bw,bt = BATTERY
bot = funion(bot, cq.Workplane("XY").rect(bl+3, bw+3).rect(bl+0.6, bw+0.6).extrude(3).translate((bx, by, WALL)))
bot = funion(bot, oplan(WALL + 0.15, 1.5).cut(oplan(WALL + 1.15, 1.5)).translate((0, 0, SPLIT_Z)))
for x,y in [(-32,-30),(32,-30),(-32,32),(32,32)]:
    bot = fcut(bot, cq.Workplane("XY").circle(5.2).extrude(0.8).translate((x, y, -0.01)))

# ---------- button caps: printed upright on their contact face, every downward face is 45 deg ----------
caps = {}
z0 = pcb_top + TACT_H + PRETRAVEL
for n,k,x,y,s_ in BUTTONS:
    zs = dome_z(x, y); top_z = zs + CAP_PROUD
    fl_top = zs - WALL - SLEEVE            # flange stops against sleeve bottom
    body_c = cap_prism(k, s_, 0, top_z - fl_top, fl_top).faces(">Z").edges().fillet(1.2)
    body_c = body_c.cut(cq.Workplane("XY").sphere(40).translate((0, 0, top_z + 40 - 0.5)))   # finger dish
    # flange: 0.6 vertical + 45 deg chamfer underneath
    fl = cap_prism(k, s_, 1.0, 0.6, fl_top - 0.6)
    fl = fl.union(cap_profile(k, s_, 1.0).extrude(1.0, taper=45).rotate((0,0,0),(1,0,0),180).translate((0, 0, fl_top - 0.6)))
    c = body_c.union(fl)
    # 45 deg taper toward the plunger(s), then straight post to z0
    fb = fl_top - 1.6; avail = fb - z0
    half_min = (s_/2 if k == "round" else min(s_)/2)
    tap_h = max(0.0, min(avail, half_min - 1.75))
    prof = cap_profile(k, s_, 0)
    tap = prof.extrude(tap_h, taper=45).rotate((0,0,0),(1,0,0),180).translate((0, 0, fb)) if tap_h > 0.05 else None
    if tap is not None: c = c.union(tap)
    rest = avail - tap_h
    if rest > 0.05:
        if k == "round": post = cq.Workplane("XY").circle(half_min - tap_h).extrude(rest)
        else: post = cap_profile(k, s_, -tap_h).extrude(rest)
        c = c.union(post.translate((0, 0, z0)))
    caps[n] = c.translate((x, y, 0))
    print(f"cap {n}: taper {tap_h:.1f} post {max(rest,0):.1f} plunger gap {PRETRAVEL}")

# ---------- knob: printed bore-down, D-shaft fit tuned for FDM ----------
kx, ky = KNOB["x"], KNOB["y"]
knob = cq.Workplane("XY").circle(KNOB["d"]/2).extrude(KNOB["h"]).faces(">Z").edges().fillet(1.5).faces("<Z").edges().chamfer(0.6)
knob = knob.cut(cq.Workplane("XY").circle(KNOB["d"]/2 - 2).extrude(0.6).translate((0, 0, KNOB["h"] - 0.6)))
for i in range(36):
    knob = knob.cut(cq.Workplane("XY").rect(1.0, 1.0).extrude(KNOB["h"] - 2.2).rotate((0,0,0),(0,0,1),45).translate((KNOB["d"]/2, 0, 0.6)).rotate((0,0,0),(0,0,1),i*10))
SH_R, SH_FLAT = 3.1, 1.6          # EC11 6.0 mm shaft, 4.5 mm D -> printed bore 6.2 / 4.7 (tune with test piece)
bore = cq.Workplane("XY").circle(SH_R).extrude(9).cut(cq.Workplane("XY").rect(8, 8).extrude(9).translate((0, 4 + SH_FLAT, 0)))
bore = bore.union(cq.Workplane("XY").circle(SH_R + 0.5).extrude(0.5, taper=45))   # entry chamfer
knob = knob.cut(bore).cut(cq.Workplane("XY").rect(0.8, 6).extrude(7).translate((0, -SH_R - 2.5, 0)))   # flex slit opposite flat
ring = cq.Workplane("XY").circle(KNOB["ring_d"]/2 - 0.0).circle(KNOB["d"]/2 + 0.6).extrude(1.2)
knob = knob.translate((kx, ky, kz - 0.5)); ring = ring.translate((kx, ky, kz - 1.5))

# ---------- scroll wheel: printed flat, square drive shaft into mouse encoder, 3 mm pin into lug ----------
ww = WHEEL["w"]
wh = cq.Workplane("XY").circle(WHEEL["d"]/2).extrude(ww).faces(">Z").edges().fillet(0.8).faces("<Z").edges().chamfer(0.6)
for i in range(24):
    wh = wh.cut(cq.Workplane("XY").rect(1.2, 1.2).extrude(ww + 2).rotate((0,0,0),(0,0,1),45).translate((WHEEL["d"]/2, 0, -1)).rotate((0,0,0),(0,0,1),i*15))
enc_face_gap = (WHEEL["x"] + 9.0 - 3.2) - (WHEEL["x"] + ww/2)
wh = wh.union(cq.Workplane("XY").rect(1.95, 1.95).extrude(enc_face_gap + 4.0).edges("|Z").chamfer(0.2).translate((0, 0, ww)))  # 1.95 sq drive
wh = wh.cut(cq.Workplane("XY").circle(WHEEL_PIN[0]/2 - 0.05).extrude(5.5).translate((0, 0, -0.01)))                           # pin press hole
wheel_print = wh
# assembled: wheel axis along +X (square shaft toward encoder at +X)
wheel = wh.rotate((0,0,0),(0,1,0),90).translate((WHEEL["x"] - ww/2, WHEEL["y"], wz))
pin = cq.Workplane("XY").circle(WHEEL_PIN[0]/2).extrude(WHEEL_PIN[1]).rotate((0,0,0),(0,1,0),-90).translate((WHEEL["x"] - ww/2 + 5.5, WHEEL["y"], wz))

# ---------- light pipe (clear PETG/PMMA rod 3.0) with retention flange ----------
lp_len = lz + 0.3 - (pcb_top + 0.8)
lp = cq.Workplane("XY").circle(1.5).extrude(lp_len).union(cq.Workplane("XY").circle(2.5).extrude(1.0).translate((0, 0, lz - WALL - 1.0 - (pcb_top + 0.8))))
lp = lp.faces("<Z").edges().chamfer(0.3).translate((LED["x"], LED["y"], pcb_top + 0.8))

# ---------- power-switch slider extender (press-fit on PCM12 actuator) ----------
ext = cq.Workplane("XY").box(4.0, 4.0, 3.0).faces(">Y").edges().fillet(0.6)
ext = ext.cut(cq.Workplane("XY").box(1.5, 1.6, 1.6).translate((0, -2.0 + 0.8 - 0.01, 0)))
pwr_ext = ext.translate((PWR_X + 0.75, ypw - 1.85 + 2.0, pz))

top = cq.Workplane(obj=top.val().fix()); bot = cq.Workplane(obj=bot.val().fix())
parts = dict(top_shell=top, bottom_shell=bot, knob=knob, knob_ring=ring, scroll_wheel=wheel, wheel_pin=pin, light_pipe=lp,
             pwr_slider_ext=pwr_ext, **{f"cap_{n}": c for n, c in caps.items()})
asm = cq.Assembly()
for n, p in parts.items():
    cq.exporters.export(p, f"out/{n}.step"); cq.exporters.export(p, f"out/{n}.stl", tolerance=0.03, angularTolerance=0.15)
    asm.add(p, name=n)
from shapely.geometry import Polygon as _P
pcb_pts = pcb_outline_pts()
pcbp = cq.Workplane("XY").polyline(pcb_pts).close().extrude(PCB_T).translate((0, 0, PCB_Z))
for x, y in SCREWS: pcbp = pcbp.cut(cq.Workplane("XY").circle(1.1).extrude(5).translate((x, y, PCB_Z - 1)))
pcbp = pcbp.cut(cq.Workplane("XY").rect(9.6, 22).extrude(5).translate((WHEEL["x"], WHEEL["y"], PCB_Z - 1)))
asm.add(pcbp, name="pcb_placeholder", color=cq.Color(0, 0.5, 0, 1))
asm.save("out/assembly.step")
cq.exporters.export(pcbp, "out/pcb_placeholder.stl")
import pickle
pickle.dump(dict(wheel_print=None), open("out/.meta.pkl", "wb"))
cq.exporters.export(wheel_print, "out/_wheel_print.stl", tolerance=0.03, angularTolerance=0.15)
for n, p in parts.items():
    bb = p.val().BoundingBox(); print(("" if p.val().isValid() else "INVALID ") + f"{n:16s} {bb.xlen:6.1f} x {bb.ylen:6.1f} x {bb.zlen:6.1f}  vol={p.val().Volume()/1000:.1f}cm3")
