#!/bin/bash
# full regeneration: schematic -> placed PCB -> Freerouting autoroute -> zones+stitching -> ERC/DRC
set -e
python3 gen_sch.py
python3 gen_pcb.py
python3 tools/patch_pro.py          # JLC rules + Power/USB net classes (SaveBoard rewrites the .kicad_pro)
python3 -c "import pcbnew; b=pcbnew.LoadBoard('creative-controller.kicad_pcb'); pcbnew.ExportSpecctraDSN(b,'route.dsn')"
timeout 1500 nice xvfb-run -a java -Xmx3g -jar ${FREEROUTING:-/workspace/freerouting.jar} -de route.dsn -do route.ses -mp 30 -oit 5 > freerouting.log 2>&1
python3 import_route.py
python3 tools/patch_pro.py
kicad-cli sch erc -o erc.rpt creative-controller.kicad_sch
kicad-cli pcb drc --schematic-parity -o drc.rpt creative-controller.kicad_pcb
