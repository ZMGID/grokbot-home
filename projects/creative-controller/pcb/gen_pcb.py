import pcbnew, math, uuid, sys
from design import parts, FP
from sexp import get_symbol, pins as sympins
sys.path.insert(0, "../mechanical"); from params import PCB_W, PCB_R, SCREWS, WHEEL, outline_pts, PCB_INSET
NS = uuid.UUID("6b1f0c2e-0000-4000-8000-00000000c0de")
uid = lambda s: str(uuid.uuid5(NS, s))
CX, CY = 100.0, 100.0
mm = pcbnew.FromMM
V = lambda x, y: pcbnew.VECTOR2I(mm(CX + x), mm(CY - y))
b = pcbnew.BOARD()
ds = b.GetDesignSettings()
nc = ds.m_NetSettings.GetDefaultNetclass()
nc.SetTrackWidth(mm(0.25)); nc.SetClearance(mm(0.15)); nc.SetViaDiameter(mm(0.6)); nc.SetViaDrill(mm(0.3))
ds.SetCopperLayerCount(2); ds.m_MinThroughDrill = mm(0.2); ds.m_HoleToHoleMin = mm(0.2)
nets = {}
def net(n):
    if n not in nets:
        ni = pcbnew.NETINFO_ITEM(b, "/" + n); b.Add(ni); nets[n] = ni
    return nets[n]
for p in parts:
    lib, name = p["fp"].split(":")
    path = FP + lib + ".pretty" if lib != "CreativeDial" else "CreativeDial.pretty"
    f = pcbnew.FootprintLoad(path, name)
    f.SetReference(p["ref"]); f.SetValue(p["value"])
    x, y, r = p["pos"]
    f.SetPosition(V(x, y)); f.SetOrientationDegrees(r)
    f.SetPath(pcbnew.KIID_PATH("/" + uid(p["ref"])))
    f.SetFPIDAsString(p["fp"])
    try:
        fld = pcbnew.PCB_FIELD(f, f.GetNextFieldId(), "LCSC"); fld.SetText(p["lcsc"]); fld.SetVisible(False); f.AddField(fld)
    except Exception as e: print("field", e)
    for pad in f.Pads():   # JLC 2-layer min drill 0.3 mm: enlarge EP thermal vias of the module footprint (0.2 -> 0.3)
        if pad.HasHole() and pad.GetDrillSize().x < mm(0.3):
            pad.SetDrillSize(pcbnew.VECTOR2I(mm(0.3), mm(0.3)))
            if pad.GetSize(pcbnew.F_Cu).x < mm(0.6): pad.SetSize(pcbnew.F_Cu, pcbnew.VECTOR2I(mm(0.6), mm(0.6)))
    for pad in f.Pads():
        n = p["pins"].get(pad.GetNumber())
        if n and not n.startswith("NC"): pad.SetNet(net(n))
        elif pad.GetNumber():
            lib_, nm_ = p["sym"].split(":"); pn = {q["num"]: q["name"] for q in sympins(get_symbol(lib_, nm_))}
            if pad.GetNumber() in pn:
                u = f"unconnected-({p['ref']}-{pn[pad.GetNumber()]}-Pad{pad.GetNumber()})"
                ni = pcbnew.NETINFO_ITEM(b, u); b.Add(ni); pad.SetNet(ni)
    if "_0402_" in p["fp"] or "_0603_" in p["fp"] or "_0805_" in p["fp"]:   # small silk refs -> fewer silk overlaps
        f.Reference().SetTextSize(pcbnew.VECTOR2I(mm(0.8), mm(0.8))); f.Reference().SetTextThickness(mm(0.12))
    b.Add(f)
# mounting holes
for i, (x, y) in enumerate(SCREWS):
    f = pcbnew.FootprintLoad(FP + "MountingHole.pretty", "MountingHole_2.2mm_M2")
    f.SetReference(f"H{i+1}"); f.SetPosition(V(x, y)); f.SetAttributes(f.GetAttributes() | pcbnew.FP_EXCLUDE_FROM_BOM | pcbnew.FP_BOARD_ONLY); b.Add(f)
# outline: rounded square
def seg(a, c):
    s = pcbnew.PCB_SHAPE(b); s.SetShape(pcbnew.SHAPE_T_SEGMENT); s.SetStart(a); s.SetEnd(c); s.SetLayer(pcbnew.Edge_Cuts); s.SetWidth(mm(0.1)); b.Add(s)
def arc(cx, cy, r, a0):
    s = pcbnew.PCB_SHAPE(b); s.SetShape(pcbnew.SHAPE_T_ARC); s.SetLayer(pcbnew.Edge_Cuts); s.SetWidth(mm(0.1))
    pt = lambda a: V(cx + r*math.cos(math.radians(a)), cy + r*math.sin(math.radians(a)))
    s.SetArcGeometry(pt(a0), pt(a0+45), pt(a0+90)); b.Add(s)
def rrect(cx, cy, w, h, r):
    hw, hh = w/2, h/2
    seg(V(cx-hw+r, cy+hh), V(cx+hw-r, cy+hh)); seg(V(cx-hw+r, cy-hh), V(cx+hw-r, cy-hh))
    seg(V(cx-hw, cy-hh+r), V(cx-hw, cy+hh-r)); seg(V(cx+hw, cy-hh+r), V(cx+hw, cy+hh-r))
    arc(cx+hw-r, cy+hh-r, r, 0); arc(cx-hw+r, cy+hh-r, r, 90); arc(cx-hw+r, cy-hh+r, r, 180); arc(cx+hw-r, cy-hh+r, r, 270)
from params import pcb_outline_pts
OUT = pcb_outline_pts()
for i in range(len(OUT)):
    seg(V(*OUT[i]), V(*OUT[(i+1) % len(OUT)]))
rrect(WHEEL["x"], WHEEL["y"], 9.6, 22, 2)    # wheel clearance slot
# GND pours both sides + antenna keepout (front edge, under module antenna)
def zone(layer, pts, netname=None, keepout=False):
    z = pcbnew.ZONE(b); z.SetLayer(layer)
    o = z.Outline(); o.NewOutline()
    for x, y in pts: o.Append(V(x, y))
    if keepout:
        z.SetIsRuleArea(True); z.SetDoNotAllowCopperPour(True); z.SetDoNotAllowTracks(True); z.SetDoNotAllowVias(True)
        z.SetDoNotAllowPads(False); z.SetDoNotAllowFootprints(False)
        z.SetLayerSet(pcbnew.LSET.AllCuMask())
    else:
        z.SetNet(net(netname)); z.SetLocalClearance(mm(0.3)); z.SetMinThickness(mm(0.25))
        z.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL)
    b.Add(z)
h = PCB_W/2
if "--zones" in sys.argv:
    for L in (pcbnew.F_Cu, pcbnew.B_Cu): zone(L, [(-h,-h),(h,-h),(h,h),(-h,h)], "GND")
# edge keepout ring (0.6 mm) so the autorouter stays >= 0.5 mm from the board edge
z = pcbnew.ZONE(b); z.SetLayer(pcbnew.F_Cu); o = z.Outline(); o.NewOutline()
for x, y in OUT: o.Append(mm(CX + x), mm(CY - y))
o.NewHole()
from shapely.geometry import Polygon as _P
for x, y in list(_P(OUT).buffer(-0.6, join_style=1).exterior.coords)[:-1]: o.Append(mm(CX + x), mm(CY - y), 0, 0)
z.SetIsRuleArea(True); z.SetDoNotAllowCopperPour(False); z.SetDoNotAllowTracks(True); z.SetDoNotAllowVias(True)
z.SetDoNotAllowPads(False); z.SetDoNotAllowFootprints(False); z.SetLayerSet(pcbnew.LSET.AllCuMask()); b.Add(z)
ey = -edge_y(0, back=False) if False else None
from design import edge_y
fy = edge_y(0, back=False)
zone(pcbnew.F_Cu, [(-20,fy-1),(20,fy-1),(20,-35),(-20,-35)], keepout=True)   # Espressif: no copper (any layer) under/beside PCB antenna
_wx, _wy = WHEEL["x"], WHEEL["y"]   # track keepout around the wheel slot (edge clearance)
zone(pcbnew.F_Cu, [(_wx-5.5,_wy-11.7),(_wx+5.5,_wy-11.7),(_wx+5.5,_wy+11.7),(_wx-5.5,_wy+11.7)], keepout=True)
b.SetFileName("creative-controller.kicad_pcb")
pcbnew.SaveBoard("creative-controller.kicad_pcb", b)
print("footprints", len(b.GetFootprints()), "nets", len(nets))
