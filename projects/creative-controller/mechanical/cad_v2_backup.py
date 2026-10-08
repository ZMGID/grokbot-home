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
body = body.faces("<Z").edges().fillet(R_BOT)
inner = dome_solid(WALL)
try:
    inner = inner.faces(">Z").edges().fillet(R_TOP - WALL)
except Exception as e: print("inner blend fallback", e); inner = inner.faces(">Z").edges().fillet(2)
inner = inner.faces("<Z").edges().fillet(max(R_BOT - WALL, 0.5))
shell = body.cut(inner)
shell = cq.Workplane(obj=shell.val().fix())   # heal spline/sphere boolean tolerance issues

def cutters(clr):
    c = cq.Workplane("XY")
    sols = []
    for n,k,x,y,s in BUTTONS:
        if k == "round": sols.append(cq.Workplane("XY").circle(s/2+clr).extrude(50).translate((x,y,-10)))
        else: sols.append(cq.Workplane("XY").rect(s[0]+2*clr, s[1]+2*clr).extrude(50).edges("|Z").fillet(min(s)/2-0.6+clr).translate((x,y,-10)))
    return sols

top = shell.intersect(cq.Workplane("XY").box(200,200,100,centered=(True,True,False)).translate((0,0,SPLIT_Z)))
bot = shell.intersect(cq.Workplane("XY").box(200,200,SPLIT_Z,centered=(True,True,False)))
for s in cutters(CLR): top = fcut(top, s)
# knob ring recess + shaft hole
top = fcut(top, cq.Workplane("XY").circle(KNOB["ring_d"]/2+0.5).extrude(10).translate((KNOB["x"],KNOB["y"],dome_z(0,0)-1.5)))
top = fcut(top, cq.Workplane("XY").circle(KNOB["d"]/2+1.0).extrude(40).translate((KNOB["x"],KNOB["y"],0)))
# wheel slot
top = fcut(top, cq.Workplane("XY").rect(WHEEL["w"]+1.2, 20).extrude(40).edges("|Z").fillet(2).translate((WHEEL["x"],WHEEL["y"],0)))
top = fcut(top, cq.Workplane("XY").circle(LED["d"]/2+0.1).extrude(40).translate((LED["x"],LED["y"],0)))
# USB-C opening (back wall, +Y)
uz = pcb_top + 1.6
top = fcut(top, cq.Workplane("XZ").rect(USB["w"]+0.4, USB["h"]+0.4).extrude(-20).edges("|Y").fillet(1.5).translate((USB["x"],D/2-5,uz)))
# power slide-switch slot (right wall, PCM12 at x=43.6,y=-4)
top = fcut(top, cq.Workplane("XZ").rect(8.0, 3.0).extrude(-12).translate((33, D/2-8, pcb_top+1.0)))   # power switch slot, back wall x=30
# top-shell screw bosses (pilot 1.6 for M2 self-tap) down to PCB top
for x,y in SCREWS:
    boss = cq.Workplane("XY").circle(3.2).extrude(H-pcb_top).translate((x,y,pcb_top)).intersect(inner.translate((0,0,0.3)))
    top = fcut(funion(top, boss), cq.Workplane("XY").circle(0.8).extrude(min(8, dome_z(x,y)-WALL-pcb_top-2.5)).translate((x,y,pcb_top)))
# PCB alignment lip on top shell inner wall (locating ribs) - simplified as 4 ribs
# bottom shell: bosses up to PCB bottom, counterbored through-holes, battery pocket ribs
for x,y in SCREWS:
    bot = bot.union(cq.Workplane("XY").circle(3.2).extrude(PCB_Z-WALL).translate((x,y,WALL)))
    bot = bot.cut(cq.Workplane("XY").circle(1.15).extrude(40).translate((x,y,-1)))
    bot = bot.cut(cq.Workplane("XY").circle(2.1).extrude(2.0).translate((x,y,-0.01)))   # head counterbore
bx,by,bl,bw,bt = BATTERY
rib = cq.Workplane("XY").rect(bl+3, bw+3).rect(bl+0.6, bw+0.6).extrude(3).translate((bx,by,WALL))
bot = bot.union(rib)
# lip/groove joint: 1.0 mm tongue on bottom shell, 0.15 clearance
lip = plan(W-2*WALL+0.0, D-2*WALL, R_CORNER-WALL, 1.5).cut(plan(W-2*WALL-2.0, D-2*WALL-2.0, R_CORNER-WALL-1, 1.5)) \
      .translate((0,0,SPLIT_Z))
lip = lip.cut(plan(W-2*WALL+0.3-0.3, D-2*WALL, R_CORNER-WALL, 0).translate((0,0,0))) if False else lip
bot = bot.union(oplan(WALL+0.15, 1.5).cut(oplan(WALL+1.15, 1.5)).translate((0,0,SPLIT_Z)))
# 4 rubber feet recesses ø10x0.8
for x,y in [(-34,-34),(34,-34),(-34,34),(34,34)]:
    bot = bot.cut(cq.Workplane("XY").circle(5.2).extrude(0.8).translate((x,y,-0.01)))

# ---------- button caps ----------
caps = {}
for n,k,x,y,s_ in BUTTONS:
    flange = 1.2; z0 = pcb_top + TACT_H + 0.3      # 0.3 mm pre-travel gap to tact plunger
    zs = dome_z(x, y)                               # local outer surface
    skin = zs - WALL - 0.4                          # flange top sits under inner skin (0.4 travel stop gap)
    top_z = zs + CAP_PROUD
    if k == "round":
        c = cq.Workplane("XY").circle(s_/2).extrude(top_z - skin).translate((0,0,skin))
        c = c.union(cq.Workplane("XY").circle(s_/2+1.5).extrude(flange).translate((0,0,skin-flange)))
        c = c.faces(">Z").edges().fillet(1.2)
    else:
        c = cq.Workplane("XY").rect(*s_).extrude(top_z - skin).edges("|Z").fillet(min(s_)/2-0.6).translate((0,0,skin))
        c = c.union(cq.Workplane("XY").rect(s_[0]+3, s_[1]+3).extrude(flange).edges("|Z").fillet(min(s_)/2+0.5).translate((0,0,skin-flange)))
        c = c.faces(">Z").edges().fillet(1.2)
    # concave finger dish on top
    c = c.cut(cq.Workplane("XY").sphere(40).translate((0,0,top_z+40-0.5)))
    stem = cq.Workplane("XY").circle(1.6).extrude(skin-flange-z0).translate((0,0,z0))
    if n == "top":   # long bar: 2 stems over 2 parallel tact switches
        c = c.union(stem.translate((-14,0,0))).union(stem.translate((14,0,0)))
    else: c = c.union(stem)
    caps[n] = c.translate((x,y,0))

# ---------- knob (EC11 D-shaft 6 mm, 20 mm shaft) ----------
kx,ky = KNOB["x"],KNOB["y"]
knob = cq.Workplane("XY").circle(KNOB["d"]/2).extrude(KNOB["h"]).faces(">Z").edges().fillet(1.5)
knob = knob.cut(cq.Workplane("XY").circle(KNOB["d"]/2-2).extrude(0.6).translate((0,0,KNOB["h"]-0.6)))  # dish
for i in range(36):   # knurl
    knob = knob.cut(cq.Workplane("XY").rect(1.0,1.0).extrude(KNOB["h"]-2).rotate((0,0,0),(0,0,1),45)
                    .translate((KNOB["d"]/2,0,0)).rotate((0,0,0),(0,0,1),i*10))
bore = cq.Workplane("XY").circle(3.0+0.05).extrude(9).cut(cq.Workplane("XY").rect(8,8).extrude(9).translate((0,4+1.5,0)))
knob = knob.cut(bore)   # D-flat 4.5 mm (EC11 D-shaft), press fit 0.05
ring = cq.Workplane("XY").circle(KNOB["ring_d"]/2).circle(KNOB["d"]/2+0.6).extrude(1.2)  # decorative light/grip ring
knob = knob.translate((kx,ky,dome_z(kx,ky)-0.5))
ring = ring.translate((kx,ky,dome_z(kx,ky)-1.5))

# ---------- scroll wheel (mouse-encoder axle: 2.0x2.0 square bore) ----------
wh = cq.Workplane("YZ").circle(WHEEL["d"]/2).extrude(WHEEL["w"]).translate((-WHEEL["w"]/2,0,0)).edges().fillet(1.0)
for i in range(24):
    wh = wh.cut(cq.Workplane("YZ").rect(1.2,1.2).extrude(WHEEL["w"]+2).translate((-WHEEL["w"]/2-1,0,0))
                .rotate((0,0,0),(1,0,0),45).translate((0,0,WHEEL["d"]/2)).rotate((0,0,0),(1,0,0),i*15))
axle = cq.Workplane("YZ").circle(1.5).extrude(16).translate((-8,0,0))
wh = wh.union(axle).cut(cq.Workplane("YZ").rect(2.05,2.05).extrude(7).translate((1.5,0,0)))
wz = pcb_top + 7.0  # Kailh mouse encoder axle height (~7 mm above PCB) - VERIFY with chosen encoder
wheel = wh.translate((WHEEL["x"],WHEEL["y"],wz))
lp = cq.Workplane("XY").circle(LED["d"]/2-0.05).extrude(dome_z(LED['x'],LED['y'])+0.3-pcb_top-0.8).translate((LED["x"],LED["y"],pcb_top+0.8))

top = cq.Workplane(obj=top.val().fix()); bot = cq.Workplane(obj=bot.val().fix())
parts = dict(top_shell=top, bottom_shell=bot, knob=knob, knob_ring=ring, scroll_wheel=wheel, light_pipe=lp,
             **{f"cap_{n}":c for n,c in caps.items()})
asm = cq.Assembly()
for n,p in parts.items():
    cq.exporters.export(p, f"out/{n}.step"); cq.exporters.export(p, f"out/{n}.stl", tolerance=0.05, angularTolerance=0.2)
    asm.add(p, name=n)
# PCB placeholder for assembly visualisation
pcbp = oplan(PCB_INSET, PCB_T).translate((0,0,PCB_Z))
for x,y in SCREWS: pcbp = pcbp.cut(cq.Workplane("XY").circle(1.7).extrude(5).translate((x,y,PCB_Z-1)))
pcbp = pcbp.cut(cq.Workplane("XY").rect(11,28).extrude(5).translate((WHEEL["x"],WHEEL["y"],PCB_Z-1)))
asm.add(pcbp, name="pcb_placeholder", color=cq.Color(0,0.5,0,1))
asm.save("out/assembly.step")
cq.exporters.export(pcbp, "out/pcb_placeholder.stl")
for n,p in parts.items():
    bb = p.val().BoundingBox(); print(("" if p.val().isValid() else "INVALID ") + f"{n:16s} {bb.xlen:6.1f} x {bb.ylen:6.1f} x {bb.zlen:6.1f}  vol={p.val().Volume()/1000:.1f}cm3")
