"""Step 2: import Freerouting session, add GND pours (both layers) + GND stitching vias, fill zones."""
import pcbnew, sys
sys.path.insert(0, "../mechanical"); from params import pcb_outline_pts
from shapely.geometry import Polygon, Point, LineString
from shapely.ops import unary_union
mm = pcbnew.FromMM; MM = lambda v: v / 1e6
b = pcbnew.LoadBoard("creative-controller.kicad_pcb")
print("SES import:", pcbnew.ImportSpecctraSES(b, "route.ses"))
gnd = b.FindNet("/GND")
for L in (pcbnew.F_Cu, pcbnew.B_Cu):
    z = pcbnew.ZONE(b); z.SetLayer(L); o = z.Outline(); o.NewOutline()
    for x, y in pcb_outline_pts(): o.Append(mm(100+x), mm(100-y))
    z.SetNet(gnd); z.SetLocalClearance(mm(0.3)); z.SetMinThickness(mm(0.25)); z.SetPadConnection(pcbnew.ZONE_CONNECTION_FULL)
    z.SetThermalReliefSpokeWidth(mm(0.4)); z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS); b.Add(z)
# ---- GND stitching vias on a 4 mm grid wherever free on BOTH layers ----
VR, CLR = 0.3, 0.35          # via radius (0.6/0.3), clearance to other copper (> 0.3 zone clearance)
obst = []
for t in b.GetTracks():
    if t.GetNetCode() == gnd.GetNetCode() and t.Type() == pcbnew.PCB_TRACE_T: continue
    s, e = t.GetStart(), t.GetEnd(); w = MM(t.GetWidth(pcbnew.F_Cu) if t.Type() == pcbnew.PCB_VIA_T else t.GetWidth()) / 2
    obst.append(LineString([(MM(s.x), MM(s.y)), (MM(e.x), MM(e.y))]).buffer(w + CLR + VR) if s != e else Point(MM(s.x), MM(s.y)).buffer(w + CLR + VR))
for f in b.GetFootprints():
    for p in f.Pads():
        bb = p.GetBoundingBox(); pad = Polygon([(MM(bb.GetLeft()), MM(bb.GetTop())), (MM(bb.GetRight()), MM(bb.GetTop())), (MM(bb.GetRight()), MM(bb.GetBottom())), (MM(bb.GetLeft()), MM(bb.GetBottom()))])
        obst.append(pad.buffer(CLR + VR + (0.3 if p.GetNetCode() != gnd.GetNetCode() else 0.1)))
    cy = f.GetCourtyard(pcbnew.F_CrtYd)   # keep vias out from under parts (paste/tenting, tact switches)
    bb = f.GetBoundingBox(False)
    obst.append(Polygon([(MM(bb.GetLeft()), MM(bb.GetTop())), (MM(bb.GetRight()), MM(bb.GetTop())), (MM(bb.GetRight()), MM(bb.GetBottom())), (MM(bb.GetLeft()), MM(bb.GetBottom()))]).buffer(0.2))
for z in b.Zones():
    if z.GetIsRuleArea():
        ring = lambda o: [(MM(o.CPoint(i).x), MM(o.CPoint(i).y)) for i in range(o.PointCount())]
        ol = z.Outline(); holes = [ring(ol.Hole(0, h)) for h in range(ol.HoleCount(0))]
        obst.append(Polygon(ring(ol.Outline(0)), holes).buffer(VR + 0.5))
O = unary_union(obst)
board = Polygon([(100+x, 100-y) for x, y in pcb_outline_pts()]).buffer(-(VR + 1.0))
n = 0
for gx in range(-48, 49, 4):
    for gy in range(-48, 49, 4):
        P = Point(100 + gx, 100 + gy)
        if board.contains(P) and not O.contains(P):
            v = pcbnew.PCB_VIA(b); v.SetPosition(pcbnew.VECTOR2I(mm(P.x), mm(P.y))); v.SetWidth(mm(0.6)); v.SetDrill(mm(0.3))
            v.SetNet(gnd); b.Add(v); n += 1
print("stitching vias:", n)
pcbnew.ZONE_FILLER(b).Fill(b.Zones())
pcbnew.SaveBoard("creative-controller.kicad_pcb", b)
print("tracks+vias:", len(b.GetTracks()))
