# skills/

**现有用户自建技能**（2026-10-15 核对，新号 `/home/box/agent-data/workflows/`）：

| 技能 | 目录 | 谁用 | 说明 |
|---|---|---|---|
| TikTok巴西站竞品调研 | `skills/tiktok/` | 商品调研 | 2026-10-14 建。按供应商商品图逐 SKU 查 TikTok Shop 巴西站竞品价格和销量，出带图 xlsx。需环境变量 `GECKOAPI_KEY`（值不进仓库）。`SKILL.md` 由每日同步自动收；它引用的 `scripts/`（解包、列 SKU、Gecko 搜索、生成表格）2026-10-15 从盒子 `/workspace/tk-br-research-skill-v2/scripts/` 手动补进来。含供货价的 `examples/`、`reference/` 表格和 SKU 模板不进公开仓库（只在给用户的压缩包里）。模板表头：`sku,name,cost,case,image_path,keyword,comp_price,sold,result,link`。 |

旧号 `/home/box/agent-data/workflows/` 是空的（2026-10-08 检查）。

以后自建了技能：每个技能一个子文件夹（`skills/<slug>/SKILL.md`，可带 `references/`、`scripts/`），每日同步会自动从
`/home/box/agent-data/workflows/` 收进来。新号导入时把 `skills/<slug>/` 整个复制到 `/home/box/agent-data/workflows/<slug>/`
（或用 `skill-authoring` 托管技能的方式创建同名技能），然后确认它出现在技能列表里。

## 不放在这里、需要重装的

| 名称 | 类型 | 怎么恢复 |
|---|---|---|
| pstack | 插件（plugin id `9717366`，cursor-public），含 architect、tdd、swarm、arena 等约 40 个技能 | **可选**（原为 dr eggbot 安装）；需要时 `InstallPlugin 9717366` |
| Composio 插件技能（composio-mcp、composio-activity-summary） | 随官方 Composio 插件（`32661537`） | **不需要**（2026-10-08 起不装该插件；应用走 composio-pg） |
| 托管技能（add-connector、routines、export-bot-template、sign-in……） | 平台自带 | 不用管 |
