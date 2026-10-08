"""Create print-ready (bed-oriented) STLs, tolerance test piece, 3MF plates, and an overhang report."""
import cadquery as cq, trimesh, numpy as np, os, json
from params import *
os.makedirs("../print", exist_ok=True)
pcb_top = PCB_Z + PCB_T

# ---------- tolerance test piece ----------
def tol_piece():
    base = cq.Workplane("XY").box(96, 34, 4, centered=(False, False, False)).edges("|Z").fillet(3).faces("<Z").edges().chamfer(0.5)
    feats = []
    # cap-hole clearance holes: dia 11 + 2c
    for i, c in enumerate([0.15, 0.20, 0.25, 0.30]):
        base = base.cut(cq.Workplane("XY").circle(5.5 + c).extrude(10).translate((8 + i*14, 8, -1)))
    # D-shaft bores (EC11): R/flat combos
    for i, (r, f) in enumerate([(3.05, 1.55), (3.10, 1.60), (3.15, 1.65)]):
        b = cq.Workplane("XY").circle(r).extrude(10).cut(cq.Workplane("XY").rect(8, 8).extrude(10).translate((0, 4 + f, 0)))
        base = base.cut(b.translate((64 + i*11, 8, -1)))
    # heat-set insert pilot holes in bosses
    for i, d in enumerate([3.0, 3.1, 3.2, 3.3]):
        x = 8 + i*12
        base = base.union(cq.Workplane("XY").circle(3.3).extrude(6).translate((x, 25, 4)))
        base = base.cut(cq.Workplane("XY").circle(d/2).extrude(6).translate((x, 25, 4.01)))
    # horizontal teardrop hole (3.3) for wheel pin in a vertical tab
    tab = cq.Workplane("XY").box(10, 3, 9, centered=(False, True, False)).translate((58, 25, 4))
    hole = cq.Workplane("XZ").circle(1.65).extrude(4).union(cq.Workplane("XZ").polyline([(-1.167, 1.167), (0, 2.333), (1.167, 1.167)]).close().extrude(4))
    base = base.union(tab).cut(hole.translate((63, 27, 9)))
    # square drive socket test (mouse encoder 2.0 sq): 2.0 / 2.05 / 2.1
    for i, a in enumerate([2.0, 2.05, 2.1]):
        base = base.cut(cq.Workplane("XY").rect(a, a).extrude(10).translate((74 + i*8, 25, -1)))
    # engraved labels
    try:
        for i, c in enumerate(["15", "20", "25", "30"]):
            base = base.cut(cq.Workplane("XY").text(c, 3.0, 0.6, kind="bold").translate((8 + i*14, 16.5, 3.5)))
    except Exception as e: print("text skipped", e)
    return base
def tol_pegs():
    p = cq.Workplane("XY").box(60, 12, 2, centered=(False, False, False)).edges("|Z").fillet(2)
    for i in range(4):   # 4 identical cap-diameter pegs (11.0) to test against holes
        p = p.union(cq.Workplane("XY").circle(5.5).extrude(6).faces(">Z").edges().chamfer(0.4).translate((7 + i*15, 6, 2)))
    p = p.union(cq.Workplane("XY").rect(1.95, 1.95).extrude(6).translate((56, 6, 2)))   # printed square drive sample
    return p
cq.exporters.export(tol_piece(), "../print/tolerance_test_plate.stl", tolerance=0.02, angularTolerance=0.1)
cq.exporters.export(tol_pegs(), "../print/tolerance_test_pegs.stl", tolerance=0.02, angularTolerance=0.1)
cq.exporters.export(tol_piece(), "out/tolerance_test_plate.step"); cq.exporters.export(tol_pegs(), "out/tolerance_test_pegs.step")

# ---------- bed orientation for each part ----------
def on_bed(m):
    m = m.copy(); m.merge_vertices(digits_vertex=3); m.update_faces(m.nondegenerate_faces()); m.remove_unreferenced_vertices()
    trimesh.repair.fill_holes(m); trimesh.repair.fix_normals(m)
    b = m.bounds; m.apply_translation([-(b[0][0]+b[1][0])/2, -(b[0][1]+b[1][1])/2, -b[0][2]]); return m
P = {}
P["top_shell"] = on_bed(trimesh.load("out/top_shell.stl"))           # open side down, parting plane on bed
P["bottom_shell"] = on_bed(trimesh.load("out/bottom_shell.stl"))     # outer bottom on bed
for n in [b[0] for b in BUTTONS]:
    P[f"cap_{n}"] = on_bed(trimesh.load(f"out/cap_{n}.stl"))       # as used: contact face on bed, dish up
P["knob"] = on_bed(trimesh.load("out/knob.stl"))                    # bore down
P["knob_ring"] = on_bed(trimesh.load("out/knob_ring.stl"))
P["scroll_wheel"] = on_bed(trimesh.load("out/_wheel_print.stl"))    # flat face down, square drive up
lp = trimesh.load("out/light_pipe.stl"); P["light_pipe_clearPETG"] = on_bed(lp)
ext = trimesh.load("out/pwr_slider_ext.stl")
ext.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1,0,0]))   # pocket opening on bed
P["pwr_slider_ext"] = on_bed(ext)
pin = trimesh.load("out/wheel_pin.stl"); pin.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [0,1,0]))
P["wheel_pin_optional"] = on_bed(pin)                               # vertical; steel dowel 3x14 preferred
for n, m in P.items(): m.export(f"../print/{n}.stl")

# ---------- overhang report: downward faces steeper than 45 deg not touching the bed ----------
rep = {}
for n, m in list(P.items()) + [("tolerance_test_plate", trimesh.load("../print/tolerance_test_plate.stl")), ("tolerance_test_pegs", trimesh.load("../print/tolerance_test_pegs.stl"))]:
    nz = m.face_normals[:, 2]; cz = m.triangles_center[:, 2]
    th = np.degrees(np.arccos(np.clip(-nz, -1, 1)))      # downward face angle from horizontal
    br = (cz > 0.3) & (th <= 2.0); sl = (cz > 0.3) & (th > 2.0) & (th < 43.0)   # 2 deg tessellation tolerance
    rep[n] = dict(bridge_area_mm2=round(float(m.area_faces[br].sum()), 1), overhang_steeper_than_45deg_mm2=round(float(m.area_faces[sl].sum()), 1), bbox=[round(v, 1) for v in m.extents], volume_cm3=round(m.volume/1000, 2), watertight=bool(m.is_watertight))
json.dump(rep, open("../print/overhang_report.json", "w"), indent=1)
for n, r in rep.items(): print(f"{n:24s} bridge {r['bridge_area_mm2']:7.1f}  overhang>45 {r['overhang_steeper_than_45deg_mm2']:7.1f} mm2  bbox {r['bbox']}  watertight {r['watertight']}")

# ---------- 3MF plates (256x256 / 220x220 beds) ----------
def plate(names, fname, spacing=6, bed=220):
    scene = trimesh.Scene(); x = y = 0; rowh = 0
    for n in names:
        m = P[n].copy() if n in P else trimesh.load(f"../print/{n}.stl")
        e = m.extents
        if x + e[0] > bed: x = 0; y += rowh + spacing; rowh = 0
        m.apply_translation([x + e[0]/2 - bed/2 + 5, y + e[1]/2 - bed/2 + 5, 0]); scene.add_geometry(m, geom_name=n)
        x += e[0] + spacing; rowh = max(rowh, e[1])
    open(fname, "wb").write(trimesh.exchange.threemf.export_3MF(scene))
    print("3MF", fname, "max y used", y + rowh)
plate(["top_shell", "bottom_shell"], "../print/plate1_shells.3mf")
plate([f"cap_{b[0]}" for b in BUTTONS] + ["knob", "knob_ring", "scroll_wheel", "pwr_slider_ext", "wheel_pin_optional"], "../print/plate2_controls.3mf")
plate(["tolerance_test_plate", "tolerance_test_pegs"], "../print/plate0_tolerance_test.3mf")
