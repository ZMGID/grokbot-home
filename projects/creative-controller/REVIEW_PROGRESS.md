# Review progress (auto notes)
## Done (as of 02:00)
- design.py: +U5 SN74LV1T34DBVR level shifter (LED_IO GPIO48 -> LED_DIN @VSYS), C10; MCP73831 STAT (pushes 5V!) now via 15k/22k divider (R7/R10) to GPIO2;
  VBUS_SENSE 22k/39k (R11/R12) -> GPIO13 (module pin 21); ENC pullups 10k + 10nF (R13-16, C11-14); C15 22uF 0805 on 3V3.
- gen_pcb.py: antenna keepout widened to x±20 (all Cu), module EP vias 0.2->0.3 drill (JLC 2L min), small silk refs 0.8mm.
- tools/patch_pro.py: JLC rules + netclasses Power/USB (run after every SaveBoard). import_route.py: GND pours + stitching vias (168).
- tools/jlc_lookup.py: JLC parts API lookup. All original 20 LCSC codes verified in stock (see make_bom_cpl output / fab/jlc_parts.json).
- make_bom_cpl.py rewritten (live JLC data, BOM_detailed.csv, CPL rotation corrections).
- firmware main.cpp: v1.1.0 VBUS sense, charge logic, battery avg/pct, BLE security order, robust encoder ISR (rest-state), deep sleep ext1, self-test mode. Builds OK.
## Remaining
- Reroute: last freerouting run (-mp 60) left VBUS (USB-C pads) and VBAT (J2) unrouted and froze the box -> rerun with -Xmx3g, power width 0.4/VBUS 0.35.
- DRC 0 errors, export.sh, BOM/CPL, docs/审查报告.md, README, bins, zip.
- 02:06 reroute OK: 0 unconnected, DRC 14 (check)
- 02:15 R6->3.3k (303mA), BOM regrouped, fw low-batt cutoff + USB/BLE dedupe, bins rebuilt. DRC 0 err. Next: docs
- 02:2x exports regenerated; writing docs/审查报告.md
- docs/审查报告.md written
- README/docs updated; next: zip
- 02:2x zip rebuilt. ALL DONE
