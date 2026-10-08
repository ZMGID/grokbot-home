# grok-bot 的定时任务

## 1. 每日同步到 grokbot-home（daily-grokbot-sync）——已移交

- **状态**：**已移交给仓库管家**（2026-10-08）。grok-bot 不再跑此任务。
- **规范提示词与重建说明**：见 `bots/仓库管家/routines.md`。
- **详细步骤**：见 `scripts/sync.md`，脚本 `scripts/sync.sh`。

## 2. 工作日早晨计划（含双 Gmail 未读摘要）

- **触发**：工作日 08:53（北京时间）。cron：`CRON_TZ=Asia/Shanghai 53 8 * * 1-5`
- **状态**：本账号已于 2026-10-08 前后由主 bot 使用（见任务说明）。`automations/` 目录为空，未能从本机自动化文件读出保存的提示词。
- **内容（据任务说明）**：工作日早晨计划，包含两个 Gmail 账号的未读摘要。
- **保存的提示词**：未知（本机 `/home/box/agent-data/agents/a96070f7-…/automations/` 无文件；store.db 亦无 routine 正文）。新号重建时需向用户确认完整提示词后再用 UpdateRoutine 创建。

## 3. 工作日晚间总结

- **触发**：工作日 17:47（北京时间）。cron：`CRON_TZ=Asia/Shanghai 47 17 * * 1-5`
- **状态**：同上；`automations/` 为空，提示词未知。
- **内容（据任务说明）**：工作日晚间总结。
- **保存的提示词**：未知。新号重建时需向用户确认完整提示词后再用 UpdateRoutine 创建。
