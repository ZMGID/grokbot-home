#!/usr/bin/env python3
"""GeckoAPI 搜 TikTok Shop 巴西站。每次调用约 5 积分，余额查询免费。
用法:
  gecko_search.py --credits                       # 只查余额（免费）
  gecko_search.py -k "pincel kabuki" -o raw/      # 单/多个关键词 (-k 可重复)
  gecko_search.py --csv skus.csv -o raw/          # CSV 需含 sku,keyword 列；已有结果的自动跳过
需要环境变量 GECKOAPI_KEY。脚本绝不打印 key。"""
import argparse, csv, json, os, re, sys, time
import requests
API = 'https://api.geckoapi.com.br/v1'

def headers():
    k = os.environ.get('GECKOAPI_KEY')
    if not k: sys.exit('缺少环境变量 GECKOAPI_KEY')
    return {'Authorization': f'Bearer {k}', 'Content-Type': 'application/json'}

def credits():
    try:
        r = requests.get(f'{API}/me/credits', headers=headers(), timeout=30)
        return r.json() if r.ok else f'HTTP {r.status_code}'
    except Exception as e:
        return f'错误: {e}'

def search(kw, page=1, platform='tiktok.com'):
    body = {'target': platform, 'type': 'plp', 'keyword': kw, 'region': 'BR', 'page': page}
    for attempt in range(2):  # 5xx 会退款，重试一次
        r = requests.post(f'{API}/extract', headers=headers(), json=body, timeout=180)
        if r.status_code < 500: break
        print(f'  HTTP {r.status_code}，{"重试" if attempt == 0 else "放弃"}', file=sys.stderr); time.sleep(3)
    try: return r.status_code, r.json()
    except Exception: return r.status_code, {'error': r.text[:500]}

def summary(data):
    items = (data.get('data') or {}).get('items') or []
    for it in items[:10]:
        print(f"   R${it.get('price')}  销量:{it.get('soldCount') or it.get('soldCountText') or '-'}  "
              f"{(it.get('name') or '')[:60]}  https://shop.tiktok.com/br/pdp/{it.get('productId')}")
    return len(items)

def safe(s): return re.sub(r'[^\w\-]+', '_', s)[:80]

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument('-k', '--keyword', action='append', default=[])
ap.add_argument('--csv'); ap.add_argument('-o', '--out', default='raw')
ap.add_argument('--page', type=int, default=1)
ap.add_argument('--credits', action='store_true', help='只查余额')
ap.add_argument('--force', action='store_true', help='已有结果也重新搜')
a = ap.parse_args()
print('积分(前):', credits())
if a.credits: sys.exit(0)
jobs = [(safe(k), k) for k in a.keyword]
if a.csv:
    with open(a.csv, encoding='utf-8-sig') as fp:
        jobs += [(safe(r['sku']), r['keyword']) for r in csv.DictReader(fp) if r.get('keyword')]
os.makedirs(a.out, exist_ok=True)
for name, kw in jobs:
    path = os.path.join(a.out, f'{name}.json')
    if os.path.exists(path) and not a.force:
        print(f'[跳过] {name} 已有'); continue
    print(f'[搜索] {name}: {kw}')
    code, data = search(kw, a.page)
    data['_keyword'] = kw
    json.dump(data, open(path, 'w'), ensure_ascii=False, indent=1)
    print(f'  HTTP {code}，{summary(data) if code < 400 else 0} 条')
print('积分(后):', credits())
