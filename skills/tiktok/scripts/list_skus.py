#!/usr/bin/env python3
"""列出文件夹中唯一的 SKU 基础编码。761450(2).jpg 视为 761450 的变体，优先主图 761450.jpg。
用法: list_skus.py <图片目录> [--csv out.csv]   (--csv 生成可填写的 skus.csv 骨架)"""
import argparse, csv, re, sys
from pathlib import Path
EXT = {'.jpg', '.jpeg', '.png', '.webp'}
ap = argparse.ArgumentParser(); ap.add_argument('folder'); ap.add_argument('--csv')
a = ap.parse_args()
groups = {}
for f in sorted(Path(a.folder).iterdir()):
    if f.suffix.lower() not in EXT: continue
    m = re.match(r'^(.*?)\s*[\(（](\d+)[\)）]$', f.stem)
    base, var = (m.group(1).strip(), int(m.group(2))) if m else (f.stem.strip(), -1)
    groups.setdefault(base, []).append((var, f))
rows = []
for base in sorted(groups):
    files = sorted(groups[base], key=lambda x: x[0])  # 主图(-1)排最前
    rows.append((base, str(files[0][1].resolve()), len(files)))
    print(f"{base}\t{len(files)}张\t主图={files[0][1].name}")
print(f"共 {len(rows)} 个 SKU，{sum(r[2] for r in rows)} 张图", file=sys.stderr)
if a.csv:
    with open(a.csv, 'w', newline='', encoding='utf-8-sig') as fp:
        w = csv.writer(fp)
        w.writerow(['sku','name','cost','case','image_path','keyword','comp_price','sold','result','link'])
        for base, img, _ in rows: w.writerow([base,'','','',img,'','','','',''])
    print(f"已写骨架 {a.csv}", file=sys.stderr)
