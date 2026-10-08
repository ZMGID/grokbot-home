"""Set JLCPCB 2-layer design rules + net classes in the KiCad project (DRC and Freerouting DSN read these)."""
import json
P = "creative-controller.kicad_pro"
d = json.load(open(P))
r = d["board"]["design_settings"]["rules"]
r.update(min_clearance=0.127, min_track_width=0.127, min_via_diameter=0.45, min_via_annular_width=0.13,
         min_through_hole_diameter=0.3, min_hole_to_hole=0.5, min_hole_clearance=0.25, min_copper_edge_clearance=0.3)
base = dict(d["net_settings"]["classes"][0]); base.update(clearance=0.2)   # 0.2 mm also keeps via holes >= 0.5 mm apart (JLC hole-to-hole)
def cls(name, **kw):
    c = dict(base); c.update(name=name, priority=len(d["net_settings"]["classes"])); c.update(kw); return c
d["net_settings"]["classes"] = [base,
    cls("Power", track_width=0.4, clearance=0.2, via_diameter=0.8, via_drill=0.4),
    cls("VBUS", track_width=0.35, clearance=0.2, via_diameter=0.8, via_drill=0.4),
    cls("USB", track_width=0.25, clearance=0.2, diff_pair_width=0.25, diff_pair_gap=0.2)]
d["net_settings"]["netclass_patterns"] = [{"netclass": "Power", "pattern": f"/{n}"} for n in ["VSYS","VBAT","VBAT_SW","+3V3"]] + [{"netclass": "VBUS", "pattern": "/VBUS"}] + \
    [{"netclass": "USB", "pattern": "/USB_D*"}]
json.dump(d, open(P, "w"), indent=2)
print("patched", P)
