"""JLCPCB BOM + CPL from design.py and the KiCad position export.
Part data (stock / price / Basic-Extended / package / link) is pulled LIVE from the JLCPCB parts library API
(tools/jlc_lookup.py) and cached in fab/jlc_parts.json together with the query timestamp."""
import csv, collections, json, re, time, os, sys
from design import parts
sys.path.insert(0, "tools"); from jlc_lookup import q
HAND = ("Rotary", "CreativeDial")          # THT / non-JLC parts: hand-solder, not in CPL
# KiCad -> JLC rotation corrections (KiCad 9 footprints, IPC zero orientation). These follow the commonly used
# kicad-jlcpcb-tools / JLCKicadTools tables and MUST be confirmed in the JLC 3D placement preview (see docs).
ROT = [(r"^SOT-23", 180), (r"^USB_C_Receptacle_HRO_TYPE-C-31-M-12", 180), (r"^JST_PH_S2B-PH-SM4-TB", 180)]
cache_f = "fab/jlc_parts.json"
cache = json.load(open(cache_f)) if os.path.exists(cache_f) else {}
groups = collections.OrderedDict()
names = {}
for p in parts:   # group by (LCSC, footprint) so identical parts are ONE JLC BOM line (e.g. all 6x6 key switches)
    k = (p["lcsc"] or p["value"], p["fp"]); names.setdefault(k, []).append(p["value"]); groups.setdefault(k, []).append(p["ref"])
def _label(k):
    vs = list(dict.fromkeys(names[k])); return vs[0] if len(vs) == 1 else k[0] + " (" + "/".join(vs) + ")"
groups = collections.OrderedDict(((_label(k), k[1], k[0] if k[0].startswith("C") and k[0][1:].isdigit() else ""), v) for k, v in groups.items())
for (_, _, l) in groups:
    if l and l not in cache:
        r = [x for x in q(l) if x["code"] == l]
        cache[l] = dict(r[0], checked=time.strftime("%Y-%m-%d %H:%M")) if r else {"code": l, "notfound": True}
json.dump(cache, open(cache_f, "w"), indent=1, ensure_ascii=False)
tot = 0; nb = set()
with open("fab/BOM_JLCPCB.csv", "w", newline="") as f, open("fab/BOM_detailed.csv", "w", newline="", encoding="utf-8-sig") as g:
    w = csv.writer(f); w.writerow(["Comment", "Designator", "Footprint", "LCSC Part #"])
    w2 = csv.writer(g); w2.writerow(["Comment", "Designator", "Qty", "KiCad footprint", "LCSC", "MPN (JLC)", "JLC package", "Stock", "Type",
                                     "Unit USD (1+)", "Ext USD", "Assembly", "Checked", "Link"])
    for (v, fp, l), refs in groups.items():
        hand = fp.startswith(HAND)
        if not hand: w.writerow([v, ",".join(refs), fp.split(":")[1], l])
        c = cache.get(l, {})
        u = c.get("price") or 0; tot += u * len(refs)
        if c.get("lib") == "Extended": nb.add(l)
        w2.writerow([v, ",".join(refs), len(refs), fp.split(":")[1], l or "NOT ON LCSC - source Kailh/TTC mouse encoder (Taobao)",
                     c.get("model", ""), c.get("pkg", ""), c.get("stock", ""), c.get("lib", ""), u, round(u * len(refs), 4),
                     "hand-solder (THT)" if hand else "JLC SMT", c.get("checked", ""), c.get("url", "")])
    w2.writerow(["TOTAL parts (1+ price, excl. PCB/SMT/extended-part fees)", "", "", "", "", "", "", "", f"{len(nb)} extended types", "", round(tot, 2)])
fpmap = {p["ref"]: p["fp"].split(":")[1] for p in parts}
rows = list(csv.DictReader(open("fab/pos_raw.csv")))
with open("fab/CPL_JLCPCB.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["Designator", "Mid X", "Mid Y", "Layer", "Rotation"])
    for r in rows:
        ref = r["Ref"]
        if ref not in fpmap or fpmap[ref].startswith(("RotaryEncoder", "MouseEncoder")): continue
        rot = float(r["Rot"]) + sum(d for pat, d in ROT if re.search(pat, fpmap[ref]))
        w.writerow([ref, r["PosX"] + "mm", r["PosY"] + "mm", "Top", f"{rot % 360:g}"])
print("BOM lines", len(groups), "parts total USD", round(tot, 2), "extended types", len(nb))
