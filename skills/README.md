# skills/

**目前没有用户自建技能。** 旧号 `/home/box/agent-data/workflows/` 是空的（2026-10-08 检查）。

以后自建了技能：每个技能一个子文件夹（`skills/<slug>/SKILL.md`，可带 `references/`、`scripts/`），每日同步会自动从
`/home/box/agent-data/workflows/` 收进来。新号导入时把 `skills/<slug>/` 整个复制到 `/home/box/agent-data/workflows/<slug>/`
（或用 `skill-authoring` 托管技能的方式创建同名技能），然后确认它出现在技能列表里。

## 不放在这里、需要重装的

| 名称 | 类型 | 怎么恢复 |
|---|---|---|
| pstack | 插件（plugin id `9717366`，cursor-public），含 architect、tdd、swarm、arena、interrogate、technical-writing 等约 40 个技能 | `InstallPlugin 9717366` |
| Composio 插件技能（composio-mcp、composio-activity-summary） | 随 Composio 插件（`32661537`）安装 | 装插件即可（可选） |
| 托管技能（add-connector、routines、export-bot-template、sign-in……） | 平台自带 | 不用管 |
