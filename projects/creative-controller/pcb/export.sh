#!/bin/bash
# fabrication outputs for JLCPCB
set -e
rm -rf fab; mkdir -p fab/gerbers
P=creative-controller
kicad-cli pcb export gerbers -o fab/gerbers/ -l F.Cu,B.Cu,F.Paste,B.Paste,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts --no-protel-ext $P.kicad_pcb
kicad-cli pcb export drill -o fab/gerbers/ --format excellon --excellon-separate-th --generate-map --map-format gerberx2 $P.kicad_pcb
(cd fab/gerbers && zip -q ../$P-gerbers-JLCPCB.zip *)
kicad-cli sch export pdf -o fab/schematic.pdf $P.kicad_sch
kicad-cli sch export netlist -o fab/$P.net $P.kicad_sch
kicad-cli pcb export pos -o fab/pos_raw.csv --format csv --units mm --side front $P.kicad_pcb
kicad-cli pcb export pdf -o fab/pcb_top_layers.pdf -l F.Cu,F.SilkS,Edge.Cuts $P.kicad_pcb
kicad-cli pcb export pdf -o fab/pcb_bottom_layers.pdf -l B.Cu,Edge.Cuts $P.kicad_pcb
kicad-cli pcb export step -o fab/$P-pcb.step --subst-models $P.kicad_pcb
kicad-cli pcb render -o fab/pcb_render_top.png --side top -w 1600 --height 1200 --quality high $P.kicad_pcb
kicad-cli pcb render -o fab/pcb_render_bottom.png --side bottom -w 1200 --height 1000 $P.kicad_pcb
python3 make_bom_cpl.py
cp erc.rpt drc.rpt fab/
