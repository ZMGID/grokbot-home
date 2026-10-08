import trimesh, numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from params import *
import os; os.makedirs("drawings", exist_ok=True)
C = dict(top_shell="#f4a7c0", bottom_shell="#e88fb0", knob="#fbe3ec", knob_ring="#c9c9c9", scroll_wheel="#fbe3ec",
         light_pipe="#ffffff", pcb_placeholder="#1f7a3a")
names = ["bottom_shell","pcb_placeholder","top_shell","knob","knob_ring","scroll_wheel","light_pipe"] + [f"cap_{b[0]}" for b in BUTTONS]
meshes = {n: trimesh.load(f"out/{n}.stl") for n in names}
def render(fname, explode=0.0, elev=28, azim=-60, title="", hide=()):
    fig = plt.figure(figsize=(9,8)); ax = fig.add_subplot(111, projection="3d")
    light = np.array([0.3,-0.5,0.8]); light /= np.linalg.norm(light)
    P=[]; FC=[]
    for n,m in meshes.items():
        if n in hide: continue
        dz = {"bottom_shell":-1.5,"pcb_placeholder":-0.6,"top_shell":0.6}.get(n, 1.6 if n!="light_pipe" else 1.0)*explode
        v = m.vertices + [0,0,dz]
        base = np.array(matplotlib.colors.to_rgb(C.get(n, "#ffd1e0")))
        sh = (0.5 + 0.5*np.clip(m.face_normals@light, 0, 1))[:,None]*base
        P.append(v[m.faces]); FC.append(np.clip(sh,0,1))
    pc = Poly3DCollection(np.concatenate(P), facecolors=np.concatenate(FC), edgecolors="none", linewidths=0, antialiased=False)
    ax.add_collection3d(pc)
    ax.set_xlim(-55,55); ax.set_ylim(-55,55); ax.set_zlim(-40 if explode else -20, 70 if explode else 50)
    ax.set_box_aspect((1,1,1.1 if explode else 0.65)); ax.view_init(elev, azim); ax.set_axis_off()
    ax.set_title(title); plt.tight_layout(); plt.savefig(f"drawings/{fname}", dpi=130); plt.close()

# ---- dimensioned 2D drawing (top + front section) ----
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle
fig, (a1, a2) = plt.subplots(1, 2, figsize=(16, 8.5), gridspec_kw=dict(width_ratios=[1.1, 1]))
def dim(ax, p1, p2, off, text, vert=False):
    (x1,y1),(x2,y2) = p1,p2
    if vert:
        ax.annotate("", (x1+off,y1), (x2+off,y2), arrowprops=dict(arrowstyle="<->", lw=0.8))
        ax.text(x1+off+1.5, (y1+y2)/2, text, rotation=90, va="center", fontsize=8)
        ax.plot([x1,x1+off],[y1,y1],"k-",lw=0.3); ax.plot([x2,x2+off],[y2,y2],"k-",lw=0.3)
    else:
        ax.annotate("", (x1,y1+off), (x2,y2+off), arrowprops=dict(arrowstyle="<->", lw=0.8))
        ax.text((x1+x2)/2, y1+off+1.2, text, ha="center", fontsize=8)
        ax.plot([x1,x1],[y1,y1+off],"k-",lw=0.3); ax.plot([x2,x2],[y2,y2+off],"k-",lw=0.3)
from matplotlib.patches import Polygon as MPoly
a1.add_patch(MPoly(outline_pts(0,300), fc="#fde4ee", ec="k")); a1.add_patch(MPoly(outline_pts(PCB_INSET,300), fc="none", ec="g", ls=":")); a1.text(-20,-38,"PCB outline (inset 3.2)",color="g",fontsize=6)
for n,k,x,y,s in BUTTONS:
    if k=="round": a1.add_patch(Circle((x,y), s/2, fc="w", ec="k")); a1.text(x,y,n,ha="center",va="center",fontsize=6); a1.text(x+s/2+0.5,y-s/2-2,f"Ø{s} @({x},{y})",fontsize=6)
    else:
        a1.add_patch(FancyBboxPatch((x-s[0]/2+2,y-s[1]/2+2), s[0]-4, s[1]-4, boxstyle="round,pad=2", fc="w", ec="k"))
        a1.text(x,y,f"{n}\n{s[0]}x{s[1]}\n@({x},{y})",ha="center",va="center",fontsize=6)
a1.add_patch(Circle((KNOB["x"],KNOB["y"]), KNOB["ring_d"]/2, fc="#ddd", ec="k")); a1.add_patch(Circle((KNOB["x"],KNOB["y"]), KNOB["d"]/2, fc="w", ec="k"))
a1.text(0,0,f"KNOB Ø{KNOB['d']}\nring Ø{KNOB['ring_d']}\nEC11 @ (0,0)",ha="center",va="center",fontsize=7)
a1.add_patch(Rectangle((WHEEL["x"]-WHEEL["w"]/2, WHEEL["y"]-10), WHEEL["w"], 20, fc="#ccc", ec="k")); a1.text(WHEEL["x"],WHEEL["y"]-13,f"WHEEL Ø{WHEEL['d']}x{WHEEL['w']}",ha="center",fontsize=6)
a1.add_patch(Circle((LED["x"],LED["y"]), 1.5, fc="y", ec="k")); a1.text(2.5,LED["y"],"LED",fontsize=6)
for x,y in SCREWS: a1.add_patch(Circle((x,y),1.1,fc="none",ec="b",ls="--")); a1.text(x-3,y+2.5,"M2",fontsize=6,color="b")
a1.add_patch(Rectangle((-USB["w"]/2, D/2-1), USB["w"], 1.5, fc="k")); a1.text(0,D/2+1,"USB-C (back)",ha="center",fontsize=7)
a1.add_patch(Rectangle((29,D/2-3), 8, 1.5, fc="k")); a1.text(29,D/2+1,"PWR",fontsize=7)
dim(a1,(-W/2,-D/2),(W/2,-D/2),-7,f"{W:.0f}"); dim(a1,(W/2,-D/2),(W/2,D/2),9,f"{D:.0f}",vert=True)
a1.text(-W/2+2,D/2-2,f"squircle n={SUPER_N}, waists F{WAIST['front']}/B{WAIST['back']}/L{WAIST['left']}/R{WAIST['right']} mm",fontsize=6)
a1.set_xlim(-62,65); a1.set_ylim(-62,60); a1.set_aspect("equal"); a1.set_title("TOP VIEW (mm, origin = center)"); a1.grid(alpha=0.2)
# section view from front (YZ at x=0 schematic)
a2.add_patch(Rectangle((-W/2,0), W, SPLIT_Z, fc="#e88fb0", ec="k", alpha=0.6)); a2.text(-W/2+2,2,"BOTTOM SHELL",fontsize=7)
a2.add_patch(Rectangle((-W/2,SPLIT_Z), W, H-SPLIT_Z, fc="#f4a7c0", ec="k", alpha=0.4)); a2.text(-W/2+2,H-5,"TOP SHELL",fontsize=7)
a2.add_patch(Rectangle((-PCB_W/2,PCB_Z), PCB_W, PCB_T, fc="g")); a2.text(-PCB_W/2+30,PCB_Z+2.2,f"PCB 1.6 @ z={PCB_Z}",fontsize=7,color="g")
bx,by,bl,bw,bt = BATTERY; a2.add_patch(Rectangle((bx-bl/2, WALL), bl, bt, fc="#888")); a2.text(bx-bl/2+2,WALL+2,"LiPo 603450",fontsize=7,color="w")
a2.add_patch(Rectangle((-KNOB["d"]/2,H-1), KNOB["d"], KNOB["h"], fc="w", ec="k")); a2.text(-6,H+4,"KNOB",fontsize=7)
a2.add_patch(Rectangle((-3,PCB_Z+PCB_T), 6, 6.5, fc="#999")); a2.text(4,PCB_Z+4,"EC11",fontsize=7)
dim(a2,(-W/2,0),(-W/2,H),-6,f"{H:.0f}",vert=True); dim(a2,(W/2,0),(W/2,H-1+KNOB['h']),5,f"{H-1+KNOB['h']:.0f} (with knob)",vert=True)
dim(a2,(-W/2,0),(-W/2,SPLIT_Z),-12,f"{SPLIT_Z:.0f}",vert=True); dim(a2,(-W/2,0),(-W/2,PCB_Z),-18,f"{PCB_Z:.0f}",vert=True)
a2.text(-W/2,-10,f"Domed top R{R_DOME:.0f}, edge blend R{R_TOP:.0f}, corners R{R_CORNER:.0f} | Wall {WALL} mm | cap-hole clearance {CLR} mm/side | 6x6x5.5 tact, guided stems, FDM clearance 0.25\nTongue/groove 1.5 mm at parting line, 0.15 mm gap | 4x M2x14 DIN912 into M2x4xOD3.5 heat-set inserts",fontsize=7)
a2.set_xlim(-75,65); a2.set_ylim(-15,50); a2.set_aspect("equal"); a2.set_title("FRONT SECTION (schematic, not to scale for internals)")
plt.tight_layout(); plt.savefig("drawings/drawing_dimensions.png", dpi=140); plt.savefig("drawings/drawing_dimensions.pdf"); plt.close()
print("ok")
