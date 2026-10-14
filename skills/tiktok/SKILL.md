---
name: TikTok巴西站竞品调研
description: 用户发来供应商商品图（zip/rar/PDF），需要按 SKU 在 TikTok Shop 巴西站查竞品价格和销量并输出带图 Excel 表时使用。
---
# TikTok 巴西站竞品调研

## 适用场景
用户给出供应商目录图片（压缩包或 PDF），每张图上有 SKU（如 LUX761-439）、批发价（`/un` 单价，`/dz` 为一打需 ÷12）、整箱数（`cx:...`）。要为每个 SKU 在 TikTok Shop 巴西站找同款/类似款，记录竞品价格、销量，输出带图片的 xlsx。

## 环境准备
- 系统: `unzip`、`unrar-free`、`poppler-utils`（pdftoppm）
- Python: `pip install requests openpyxl pillow`
- 环境变量: `export GECKOAPI_KEY=...`（GeckoAPI 后台获取；任何时候都不要打印、写入文件或贴到聊天里）

## 步骤
1. **解包**: `scripts/unpack.sh 资料.rar imgs/`（RAR5 用 7z 会失败，用 unrar-free；PDF 用 pdftoppm 转 PNG）。
2. **列 SKU**: `scripts/list_skus.py imgs/ --csv skus.csv`。`761450(2).jpg` 是变体，基础编码去掉 `(n)`，优先主图。
3. **看图填表**: 逐张读主图，填 `name`（中文品名）、`cost`（R$，/dz ÷12）、`case`（cx 数）、`keyword`（葡萄牙语搜索词）。看不清的标注"待确认"，不要编造。
4. **先报预算**: 一个 SKU 一次搜索约 5 积分。开跑前告诉用户 SKU 数和预计积分，并查余额 `scripts/gecko_search.py --credits`（免费）。
5. **搜索**: `scripts/gecko_search.py --csv skus.csv -o raw/`。每 SKU 只搜第 1 页（翻页同样扣 5 积分）。已有结果自动跳过，可断点续跑。
6. **挑竞品**: 读 `raw/<sku>.json` 的 `data.items[]`（productId, name, sellerName, price, regularPrice, soldCount, soldCountText），按下方匹配规则选 1 个，回填 `comp_price, sold, result, link`（链接 `https://shop.tiktok.com/br/pdp/<productId>`）。
7. **出表**: `scripts/build_xlsx.py skus.csv 结果.xlsx`。售价/保本价/利润列留空，等用户给公式。
8. **汇报**: 用户中文，简短说 SKU 数、积分消耗与剩余、红旗项、同款少的情况。

## 关键词技巧（葡萄牙语，品牌/品类 + 关键属性 + 规格）
- 香水: `perfume <品牌> <品名> 15ml`，如 `perfume adoree habibi`
- 化妆刷: `pincel maquiagem`, `kit pincel 10 peças`, `pincel kabuki`, `pincel leque`, `pincel esfumar sombra`, `pincel chanfrado sobrancelha`
- 假睫毛: `cílios postiços`, `cílios tufinho`（簇状）, `cílios fio a fio`, `kit cílios bond selante`
- 收纳: `organizador maquiagem acrílico`, `porta pincel`, `copo organizador cristal`, `limpador elétrico de pincel`
- 清洁/美容仪: `rolo de jade`, `rolo gelo facial`, `massageador pescoço`, `máscara facial silicone`, `escova limpeza facial`
- 服装: `saia longa plissada`, `vestido longo plissado sem manga`
- 搜不到时去掉品牌，换成通用品类词；不要多次翻页。

## 匹配规则
- **同款**: 外观/规格/件数基本一致（同品牌同品名最佳）。
- **同款类**: 同品类、同形态（如都是 10 支套刷），包装不同。
- **类似**: 只有相近品类；套装 vs 单品不一致时一律算类似。
- 优先: 规格一致 > 销量高 > 价格合理；有销量的优先于无销量；广告位稍降权。
- 结果列写法: `同款52销量，价格19.9` / `类似14销量，价格19.91，参考同品牌多款链接` / `未找到合适竞品`。

## 红旗规则（写进结果列，用【】标注并在汇报中点名）
- 竞品价 < 成本 → 【竞品低于成本】，风险高
- 竞品价 < 1.5×成本 → 【空间紧】
- 销量很高（≥1000）且价格低 → 市场红海，需谨慎；销量高且价格 ≥2×成本 → 机会款
- 没有销量数据 → 注明"无销量"，必要时可单查详情（另扣 5 积分）

## 费用与坑
- GeckoAPI `POST https://api.geckoapi.com.br/v1/extract`，body `{"target":"tiktok.com","type":"plp","keyword":"...","region":"BR","page":1}`，约 5 积分/次，一页固定 10 条，无批量接口；`GET /v1/me/credits` 免费。
- 5xx 会退款，502 重试一次即可。
- Monid 的 TikHub/MrScraper 不支持巴西站（实测返回美国站），不要用。
- 巴西站很多商品没有销量字段，属正常。
- Excel 图片必须用 `TwoCellAnchor(editAs='oneCell')`（从 A 列第 r 行到 B 列第 r+1 行），行高约 110、A 列宽约 22；OneCellAnchor 在 WPS 里不显示。
- 同一压缩包可能重复发送，先核对是否已做过，避免重复扣积分。
- 用户喊停时立即停止脚本，报告已扣积分。
