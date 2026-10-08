import trimesh, numpy as np, os, sys
from raster import render
from params import BUTTONS
os.makedirs("drawings", exist_ok=True)
PINK=(0.96,0.66,0.76); PINK2=(0.92,0.58,0.69); CAP=(0.99,0.88,0.92); GREY=(0.80,0.80,0.83); PCB=(0.12,0.45,0.25)
parts = [("bottom_shell",PINK2,0.15),("top_shell",PINK,0.25),("knob",CAP,0.35),("knob_ring",GREY,0.6),("scroll_wheel",CAP,0.3),("light_pipe",(1,1,1),0.5)]+[(f"cap_{b[0]}",CAP,0.3) for b in BUTTONS]
M = {n: trimesh.load(f"out/{n}.stl") for n,_,_ in parts}; M["pcb"] = trimesh.load("out/pcb_placeholder.stl")
def items(explode=0, hide=()):
    out=[]
    for n,c,s in parts+[("pcb",PCB,0.2)]:
        if n in hide: continue
        m = M[n].copy()
        dz = {"bottom_shell":-1.6,"pcb":-0.7,"top_shell":0.5}.get(n,1.5)*explode
        m.apply_translation((0,0,dz)); out.append((m,c,s))
    return out
which = sys.argv[1:] or ["hero","top","exploded","internal"]
if "hero" in which: render(items(), "drawings/render_assembly.png", eye=(150,-200,170), target=(0,0,12))
if "top" in which: render(items(), "drawings/render_top.png", eye=(0,-30,330), target=(0,0,10), fov=22)
if "exploded" in which: render(items(18), "drawings/render_exploded.png", eye=(170,-230,150), target=(0,0,10), fov=34)
if "internal" in which: render(items(hide=("top_shell",)+tuple(f"cap_{b[0]}" for b in BUTTONS)), "drawings/render_internal.png", eye=(150,-200,170), target=(0,0,8))
print("rendered", which)
