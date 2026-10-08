"""Single-source netlist + placement for CreativeDial main board.
pos = (x, y, rot) in DEVICE coords (mm, origin = enclosure center, +Y = back/USB side), top side.
pins = {symbol pin number: net}. Pins not listed are no-connect."""
import sys; sys.path.insert(0, "../mechanical")
from params import BUTTONS, KNOB, WHEEL, LED, SCREWS, outline_pts, PCB_INSET, pcb_outline_pts, TOP_STEM_DX, PWR_X
from shapely.geometry import Polygon, LineString
_PCB_POLY = Polygon(pcb_outline_pts())
def edge_y(x, back=True):
    ls = LineString([(x,-80),(x,80)]).intersection(_PCB_POLY.exterior)
    ys = [p.y for p in getattr(ls,'geoms',[ls])]
    return max(ys) if back else min(ys)
FP = "/usr/share/kicad/footprints/"
R0402 = ("Device:R", "Resistor_SMD:R_0402_1005Metric")
C0402 = ("Device:C", "Capacitor_SMD:C_0402_1005Metric")
C0603 = ("Device:C", "Capacitor_SMD:C_0603_1608Metric")
TACT = ("Switch:SW_Push", "Button_Switch_SMD:SW_SPST_PTS645")   # 6x6 SMD gull-wing
TACT_SMALL = ("Switch:SW_Push", "Button_Switch_SMD:SW_SPST_TL3342")
TACT_LCSC = "C53431191"  # CAX TS-1102S-6x6x5.5-160 (6x6x5.5 mm, 160 gf) for user keys
TACT_SMALL_LCSC = "C318884"   # XKB TS-1187A-B-A-B, 5.1x5.1x1.5 mm, 160 gf (verified on LCSC 2026-10)
parts = []
def P(ref, sym_fp, value, lcsc, pos, pins, note=""):
    parts.append(dict(ref=ref, sym=sym_fp[0], fp=sym_fp[1], value=value, lcsc=lcsc, pos=pos, pins=pins, note=note))

# --- MCU ---
ESP = {"1":"GND","40":"GND","41":"GND","2":"+3V3","3":"EN","27":"BOOT",
       "4":"K_TOP","5":"K_SIDE","6":"K_TR1","7":"K_TR2","8":"K_TALL1","9":"K_TALL2","10":"K_BR","11":"K_KNOB","12":"K_WHEEL",
       "17":"ENC1_A","18":"ENC1_B","19":"ENC2_A","20":"ENC2_B","25":"LED_IO","39":"VBAT_SENSE","38":"CHG_STAT","21":"VBUS_SENSE",
       "13":"USB_DN","14":"USB_DP"}
P("U1", ("RF_Module:ESP32-S3-WROOM-1","RF_Module:ESP32-S3-WROOM-1"), "ESP32-S3-WROOM-1-N16R8", "C2913202", (0,-28.5,180), ESP,
  "antenna toward front edge; keep copper out of antenna area")
P("C1", C0603, "10uF", "C19702", (11,-24,90), {"1":"+3V3","2":"GND"})
P("C2", C0402, "100nF", "C1525", (11,-28,90), {"1":"+3V3","2":"GND"})
P("C15", ("Device:C","Capacitor_SMD:C_0805_2012Metric"), "22uF", "C45783", (11,-32,90), {"1":"+3V3","2":"GND"}, "Espressif: >=22uF bulk on 3V3 near module (RF TX bursts)")
P("R1", R0402, "10k", "C25744", (-11,-22,90), {"1":"+3V3","2":"EN"})
P("C3", C0402, "1uF", "C52923", (-11,-26,90), {"1":"EN","2":"GND"})
P("SW10", TACT_SMALL, "RESET", TACT_SMALL_LCSC, (-6,-12,0), {"1":"EN","2":"GND"})
P("SW11", TACT_SMALL, "BOOT", TACT_SMALL_LCSC, (3,-12,0), {"1":"BOOT","2":"GND"})
P("R2", R0402, "10k", "C25744", (-11,-18,90), {"1":"+3V3","2":"BOOT"})
# --- USB-C + ESD ---
P("J1", ("Connector:USB_C_Receptacle_USB2.0_16P","Connector_USB:USB_C_Receptacle_HRO_TYPE-C-31-M-12"), "TYPE-C-31-M-12", "C165948", (0, edge_y(0)-3.5, 180),
  {"A1":"GND","A12":"GND","B1":"GND","B12":"GND","S1":"GND","A4":"VBUS","A9":"VBUS","B4":"VBUS","B9":"VBUS",
   "A5":"CC1","B5":"CC2","A7":"USB_DN","B7":"USB_DN","A6":"USB_DP","B6":"USB_DP"})
P("R3", R0402, "5.1k", "C25905", (-7,38,90), {"1":"CC1","2":"GND"})
P("R4", R0402, "5.1k", "C25905", (7,38,90), {"1":"CC2","2":"GND"})
P("U2", ("Power_Protection:USBLC6-2SC6","Package_TO_SOT_SMD:SOT-23-6"), "USBLC6-2SC6", "C7519", (-6,29,0),
  {"1":"USB_DP","6":"USB_DP","3":"USB_DN","4":"USB_DN","5":"VBUS","2":"GND"})
# --- power path, charger, LDO ---
P("D1", ("Device:D_Schottky","Diode_SMD:D_SOD-123"), "B5819W", "C8598", (12,22,0), {"2":"VBUS","1":"VSYS"})
P("Q1", ("Transistor_FET:AO3401A","Package_TO_SOT_SMD:SOT-23"), "AO3401A", "C15127", (12,17,0), {"1":"VBUS","2":"VSYS","3":"VBAT_SW"},
  "P-FET ideal-diode power path: USB present -> FET off, battery isolated")
P("R5", R0402, "100k", "C25741", (16,14,0), {"1":"VBUS","2":"GND"})
P("U3", ("Battery_Management:MCP73831-2-OT","Package_TO_SOT_SMD:SOT-23-5"), "MCP73831T-2ACI/OT", "C424093", (18,26,0),
  {"4":"VBUS","2":"GND","3":"VBAT","5":"PROG","1":"STAT"})
P("R6", R0402, "3.3k", "C25890", (22,22,90), {"1":"PROG","2":"GND"}, "Ichg = 1000/3.3k = 303 mA: keeps USB draw < 500 mA and MCP73831 SOT-23-5 dissipation < 0.4 W")
P("C4", C0603, "10uF", "C19702", (13,27,90), {"1":"VBUS","2":"GND"})
P("C5", C0603, "10uF", "C19702", (23,28,90), {"1":"VBAT","2":"GND"})
P("R7", R0402, "15k", "C25756", (22,18,90), {"1":"STAT","2":"CHG_STAT"}, "MCP73831 STAT drives HIGH to VDD(5V): divider 15k/22k -> <=3.2V into GPIO2")
P("R10", R0402, "22k", "C25768", (25,18,90), {"1":"CHG_STAT","2":"GND"})
P("R11", R0402, "22k", "C25768", (19,10,90), {"1":"VBUS","2":"VBUS_SENSE"}, "USB present detect: 5V*39/61 = 3.2V on GPIO13")
P("R12", R0402, "39k", "C25783", (22,10,90), {"1":"VBUS_SENSE","2":"GND"})
P("SW12", ("Switch:SW_SPDT","Button_Switch_SMD:SW_SPDT_PCM12"), "PCM12SMTR", "C221841", (PWR_X, edge_y(PWR_X)-3.4, 180), {"2":"VBAT_SW","1":"VBAT","3":"NC_SW"},
  "power switch on back edge x=33 (enclosure slot modelled)")
P("J2", ("Connector_Generic:Conn_01x02","Connector_JST:JST_PH_S2B-PH-SM4-TB_1x02-1MP_P2.00mm_Horizontal"), "LiPo 3.7V", "C295747", (-20,-6,90),
  {"1":"VBAT","2":"GND"})
P("U4", ("Regulator_Linear:AP2112K-3.3","Package_TO_SOT_SMD:SOT-23-5"), "AP2112K-3.3TRG1", "C51118", (4,15,0),
  {"1":"VSYS","3":"VSYS","2":"GND","5":"+3V3"})
P("C6", C0603, "10uF", "C19702", (-1,16,90), {"1":"VSYS","2":"GND"})
P("C7", C0603, "10uF", "C19702", (9,11,90), {"1":"+3V3","2":"GND"})
P("R8", R0402, "100k", "C25741", (14,-13,90), {"1":"VBAT_SW","2":"VBAT_SENSE"})
P("R9", R0402, "100k", "C25741", (17,-13,90), {"1":"VBAT_SENSE","2":"GND"})
P("C8", C0402, "100nF", "C1525", (20,-13,90), {"1":"VBAT_SENSE","2":"GND"})
# --- LED ---
P("D2", ("LED:WS2812B","LED_SMD:LED_WS2812B_PLCC4_5.0x5.0mm_P3.2mm"), "WS2812B-B", "C2761795", (LED["x"],LED["y"],0),
  {"1":"VSYS","3":"GND","4":"LED_DIN"}, "VDD=VSYS; DIN driven by U5 level shifter at VSYS level")
P("U5", ("74xGxx:74LVC1G34","Package_TO_SOT_SMD:SOT-23-5"), "SN74LV1T34DBVR", "C100024", (-8,21.5,0), {"2":"LED_IO","3":"GND","4":"LED_DIN","5":"VSYS","1":"NC_U5"},
  "single-supply level shifter: VIH~1.35V at VCC 3.3-5V, output = VSYS level -> fixes WS2812B VIH=0.7*VDD issue")
P("C10", C0402, "100nF", "C1525", (-5,21.5,90), {"1":"VSYS","2":"GND"})
P("C9", C0402, "100nF", "C1525", (LED["x"]+5,LED["y"],90), {"1":"VSYS","2":"GND"})
# --- encoder pull-ups + RC (10k/10nF, tau=100us) ---
for j,(net_,x,y) in enumerate([("ENC1_A",8,-7),("ENC1_B",10,-7),("ENC2_A",-12,13),("ENC2_B",-10,13)]):
    P(f"R{13+j}", R0402, "10k", "C25744", (x,y,90), {"1":"+3V3","2":net_})
    P(f"C{11+j}", C0402, "10nF", "C15195", (x+4.5,y,90), {"1":net_,"2":"GND"})
# --- keys ---
key_net = {"top":"K_TOP","side":"K_SIDE","tr1":"K_TR1","tr2":"K_TR2","tall1":"K_TALL1","tall2":"K_TALL2","br":"K_BR"}
i = 1
for n,k,x,y,s in BUTTONS:
    locs = [(x-TOP_STEM_DX,y),(x+TOP_STEM_DX,y)] if n=="top" else [(x,y)]
    for lx,ly in locs:
        P(f"SW{i}", TACT, f"KEY_{n.upper()}", TACT_LCSC, (lx,ly,0), {"1":key_net[n],"2":"GND"}); i += 1
# i == 9 now; wheel press switch beneath wheel pivot
P("SW9", TACT, "KEY_WHEEL", TACT_LCSC, (-40, WHEEL["y"], 90), {"1":"K_WHEEL","2":"GND"})
# --- encoders ---
P("ENC1", ("Device:RotaryEncoder_Switch","Rotary_Encoder:RotaryEncoder_Alps_EC11E-Switch_Vertical_H20mm"), "EC11E w/ switch 20mm D-shaft", "C255515",
  (KNOB["x"]-7.5,KNOB["y"]+2.5,0), {"A":"ENC1_A","B":"ENC1_B","C":"GND","S1":"K_KNOB","S2":"GND"}, "THT - hand/wave solder")
P("ENC2", ("Device:RotaryEncoder","CreativeDial:MouseEncoder_11mm_3pin"), "Mouse wheel encoder 11mm (Kailh/TTC)", "",
  (WHEEL["x"]+9.0, WHEEL["y"], 90), {"A":"ENC2_A","C":"GND","B":"ENC2_B"},
  "PLACEHOLDER footprint: replace with exact mouse-encoder footprint after sourcing (pitch ~2.5mm)")
