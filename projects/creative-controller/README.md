# CreativeDial delivery package (Rev A1, 2026-10-08)
中文完整说明见 docs/README.md；设计审查报告（问题清单、修复、料号核验表、上电调试清单）见 **docs/审查报告.md**。

- Mechanical: mechanical/ (print-ready STL in print/)
- PCB (KiCad 9): pcb/ — regenerate with `cd pcb && ./route.sh && ./export.sh`; JLCPCB outputs in pcb/fab/
  (gerbers zip, BOM_JLCPCB.csv, CPL_JLCPCB.csv, BOM_detailed.csv with LCSC stock/price/Basic-Extended/links, ERC/DRC reports)
- Firmware: firmware/ (PlatformIO, Arduino-ESP32); prebuilt merged image firmware/bin/creativedial-esp32s3-merged.bin @0x0.
  Hardware self-test: hold TOP key while plugging in USB (or send `{"cmd":"selftest","on":true}`), watch serial at 115200.
- Config app: software/

Status: ERC 0 errors / DRC 0 errors (silkscreen warnings only), firmware builds cleanly. Not yet prototyped — see docs/审查报告.md §6 for remaining risks
(ENC2 mouse-encoder footprint is a placeholder; confirm CPL rotations in JLC preview; battery must have its own protection PCM).
