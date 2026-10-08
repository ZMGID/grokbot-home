#!/usr/bin/env python3
"""CreativeDial 配置工具 / config tool (cross-platform: Windows / macOS / Linux, Python 3.9+, Tkinter + pyserial).
Edit per-application button mappings and push them to the device over USB serial (JSON lines).
CLI:  python creativedial_config.py --list-ports | --export Photoshop out.json | --push Krita [--port COM5] | --selftest
GUI:  python creativedial_config.py
"""
import json, sys, os, time, argparse, copy
try:
    import serial, serial.tools.list_ports
except ImportError:
    serial = None

CONTROLS = [("top","顶部长键"),("side","侧键"),("tr1","右上圆键1"),("tr2","右上圆键2"),("br","右侧圆键"),
            ("tall1","右下长键1"),("tall2","右下长键2"),("knob_press","旋钮按下"),("wheel_press","滚轮按下")]
ROTARY = [("knob.cw","旋钮 顺时针"),("knob.ccw","旋钮 逆时针"),("wheel.up","滚轮 上"),("wheel.down","滚轮 下")]
EVENTS = [("single","单击"),("double","双击"),("long","长按")]

def _base(win=True):
    c = "ctrl" if win else "cmd"
    return c
PROFILES = {
 "Photoshop": {"top.single":"e","top.double":"ctrl+z","top.long":"hold:space","side.single":"ctrl+z","side.double":"ctrl+shift+z",
   "tr1.single":"i","tr2.single":"b","br.single":"ctrl+0","br.double":"ctrl+shift+n","tall1.single":"hold:space","tall2.single":"hold:alt",
   "knob_press.single":"0","wheel_press.single":"u","knob.cw":"]","knob.ccw":"[","wheel.up":"ctrl+=","wheel.down":"ctrl+-",
   "side+knob.cw":"r","side+knob.ccw":"shift+r","tr1+knob.cw":".","tr1+knob.ccw":",","top+wheel.up":"shift+]","top+wheel.down":"shift+["},
 "Clip Studio Paint": {"top.single":"e","side.single":"ctrl+z","side.double":"ctrl+y","tr1.single":"i","tr2.single":"b",
   "br.single":"ctrl+0","br.double":"ctrl+shift+n","tall1.single":"hold:space","tall2.single":"hold:alt","knob_press.single":"tab",
   "wheel_press.single":"u","knob.cw":"]","knob.ccw":"[","wheel.up":"ctrl+=","wheel.down":"ctrl+-","side+knob.cw":"-","side+knob.ccw":"="},
 "Krita": {"top.single":"e","side.single":"ctrl+z","side.double":"ctrl+shift+z","tr1.single":"p","tr2.single":"b","br.single":"5",
   "br.double":"ins","tall1.single":"hold:space","tall2.single":"hold:ctrl","knob_press.single":"tab","wheel_press.single":"u",
   "knob.cw":"]","knob.ccw":"[","wheel.up":"=","wheel.down":"-","side+knob.cw":"ctrl+]","side+knob.ccw":"ctrl+[","tr1+knob.cw":"o","tr1+knob.ccw":"i"},
 "Procreate-like (iPad/BLE, e.g. Procreate via keyboard shortcuts)": {"top.single":"e","side.single":"cmd+z","side.double":"cmd+shift+z",
   "tr2.single":"b","tr1.single":"s","br.single":"cmd+0","knob.cw":"]","knob.ccw":"[","wheel.up":"cmd+=","wheel.down":"cmd+-",
   "tall1.single":"cmd+shift+n","tall2.single":"hold:space"},
}
VALID_TOKENS = set("ctrl shift alt cmd win gui space enter esc tab del backspace up down left right ins home end pgup pgdn".split()) | {f"f{i}" for i in range(1,13)}
def validate_action(a):
    if not a: return True
    a = a.lower()
    if a.startswith("hold:"): a = a[5:]
    if a.startswith("consumer:"): return True
    toks = [t for t in a.replace("++","+=").split("+") if t]
    return all(t in VALID_TOKENS or len(t)==1 for t in toks)

class Device:
    def __init__(self, port=None):
        if serial is None: raise RuntimeError("pip install pyserial")
        self.port = port or self.find()
        if not self.port: raise RuntimeError("未找到设备 / device not found")
        self.s = serial.Serial(self.port, 115200, timeout=1)
    @staticmethod
    def find():
        for p in serial.tools.list_ports.comports():
            if (p.vid == 0x303A) or "CreativeDial" in (p.description or "") + (p.product or ""): return p.device
        return None
    def cmd(self, obj, timeout=2.0):
        self.s.reset_input_buffer(); self.s.write((json.dumps(obj, ensure_ascii=False)+"\n").encode())
        end = time.time()+timeout
        while time.time() < end:
            line = self.s.readline().decode(errors="ignore").strip()
            if line.startswith("{") and '"ok"' in line: return json.loads(line)
        raise TimeoutError("device timeout")
    def push(self, name, mapping): return self.cmd({"cmd":"set","config":{"name":name,"map":mapping}})

def make_config(name):
    m = {k:v for k,v in PROFILES[name].items() if v}
    bad = [f"{k}={v}" for k,v in m.items() if not validate_action(v)]
    if bad: raise ValueError("invalid actions: " + ", ".join(bad))
    return {"name": name, "map": m}

CFG_PATH = os.path.join(os.path.expanduser("~"), ".creativedial_profiles.json")
def load_user():
    if os.path.exists(CFG_PATH):
        try: PROFILES.update(json.load(open(CFG_PATH, encoding="utf-8")))
        except Exception: pass
def save_user(): json.dump(PROFILES, open(CFG_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

def gui():
    import tkinter as tk
    from tkinter import ttk, messagebox
    root = tk.Tk(); root.title("CreativeDial 配置工具"); root.geometry("760x620")
    top = ttk.Frame(root, padding=6); top.pack(fill="x")
    ttk.Label(top, text="应用配置 Profile:").pack(side="left")
    prof = tk.StringVar(value=list(PROFILES)[0])
    cb = ttk.Combobox(top, textvariable=prof, values=list(PROFILES), width=40, state="readonly"); cb.pack(side="left", padx=4)
    port = tk.StringVar(value="auto")
    ports = ["auto"] + ([p.device for p in serial.tools.list_ports.comports()] if serial else [])
    ttk.Label(top, text="端口:").pack(side="left"); ttk.Combobox(top, textvariable=port, values=ports, width=14).pack(side="left")
    nb = ttk.Notebook(root); nb.pack(fill="both", expand=True, padx=6, pady=6)
    entries = {}
    f1 = ttk.Frame(nb, padding=6); nb.add(f1, text="按键")
    ttk.Label(f1, text="控件").grid(row=0, column=0)
    for j,(e,en) in enumerate(EVENTS): ttk.Label(f1, text=en).grid(row=0, column=j+1)
    for i,(c,cn) in enumerate(CONTROLS):
        ttk.Label(f1, text=cn).grid(row=i+1, column=0, sticky="w")
        for j,(e,_) in enumerate(EVENTS):
            v = tk.StringVar(); ttk.Entry(f1, textvariable=v, width=18).grid(row=i+1, column=j+1, padx=2, pady=2); entries[f"{c}.{e}"] = v
    f2 = ttk.Frame(nb, padding=6); nb.add(f2, text="旋钮/滚轮/组合")
    rows = [(k,n) for k,n in ROTARY] + [(f"{h}+{k}", f"按住{hn} + {n}") for h,hn in CONTROLS[:3] for k,n in ROTARY]
    for i,(k,n) in enumerate(rows):
        ttk.Label(f2, text=n).grid(row=i, column=0, sticky="w"); v = tk.StringVar()
        ttk.Entry(f2, textvariable=v, width=24).grid(row=i, column=1, padx=2, pady=1); entries[k] = v
    help_ = ("动作格式: ctrl+z / ctrl+shift+z / [ / space / f5 / hold:space(按住期间保持) / consumer:volup\n"
             "macOS 下用 cmd 代替 ctrl。 组合 = 按住某键时转动旋钮/滚轮。")
    ttk.Label(root, text=help_, foreground="#555").pack(fill="x", padx=8)
    status = tk.StringVar(value="就绪"); ttk.Label(root, textvariable=status, relief="sunken").pack(fill="x", side="bottom")
    def load(*_):
        m = PROFILES[prof.get()]
        for k,v in entries.items(): v.set(m.get(k, ""))
    def collect():
        m = {k:v.get().strip() for k,v in entries.items() if v.get().strip()}
        bad = [k for k,v in m.items() if not validate_action(v)]
        if bad: messagebox.showerror("错误", "无效动作: " + ", ".join(bad)); return None
        PROFILES[prof.get()] = m; save_user(); return m
    def push():
        m = collect()
        if m is None: return
        try:
            d = Device(None if port.get()=="auto" else port.get()); r = d.push(prof.get(), m)
            status.set(f"已写入 {d.port}: {r}")
        except Exception as e: status.set(f"写入失败: {e}")
    def export():
        m = collect()
        if m is None: return
        fn = f"{prof.get().split()[0]}.json"; json.dump({"name":prof.get(),"map":m}, open(fn,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
        status.set(f"已导出 {os.path.abspath(fn)}")
    cb.bind("<<ComboboxSelected>>", load)
    bf = ttk.Frame(root, padding=6); bf.pack(fill="x")
    ttk.Button(bf, text="保存", command=lambda: (collect(), status.set("已保存"))).pack(side="left")
    ttk.Button(bf, text="导出 JSON", command=export).pack(side="left", padx=4)
    ttk.Button(bf, text="写入设备", command=push).pack(side="left")
    load(); root.mainloop()

def main():
    load_user()
    ap = argparse.ArgumentParser()
    ap.add_argument("--list-ports", action="store_true"); ap.add_argument("--export", nargs=2, metavar=("PROFILE","FILE"))
    ap.add_argument("--push", metavar="PROFILE"); ap.add_argument("--port"); ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.list_ports:
        for p in serial.tools.list_ports.comports(): print(p.device, p.description, hex(p.vid or 0))
    elif a.export: json.dump(make_config(a.export[0]), open(a.export[1],"w",encoding="utf-8"), ensure_ascii=False, indent=1); print("wrote", a.export[1])
    elif a.push: print(Device(a.port).push(a.push, make_config(a.push)["map"]))
    elif a.selftest:
        for n in PROFILES: c = make_config(n); assert len(json.dumps(c)) < 4096, "config exceeds firmware 4 KB line buffer"; print("OK", n, len(c["map"]), "mappings")
        assert not validate_action("ctrl+foo") and validate_action("hold:space") and validate_action("ctrl+shift+z")
        print("selftest passed")
    else: gui()
if __name__ == "__main__": main()
