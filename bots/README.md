# bots/

每个 bot 一个文件夹：

- `profile.md`：名字、头衔、description（CreateAgent 用）、头像形状/颜色、设置
- `CONTEXT.md`：这个 bot 自己的记忆和项目状态（新 bot 建好后第一件事就是读它）
- `routines.md`：它的定时任务（或 none）

| 文件夹 | 名字 | 角色 | 主 bot | 定时任务 |
|---|---|---|---|---|
| `grok-bot/` | Grok Bot | 主 bot，分派任务 | ✅ | 无（每日同步已移交给仓库管家） |
| `xiaozhi/` | 小枳 | 中文通用助手：调研、代码审查、GitHub/邮件巡检 | | 无 |
| `dr-eggbot/` | dr eggbot | 设计并创建高质量 Grok Bot | | 2 个（暂停） |
| `仓库管家/` | 仓库管家 | 维护本仓库、跑每日同步 | | 每日 03:14 同步 |

机器可读清单：`index.json`。新增 bot 时同时更新这张表和 `index.json`。

旧号上还有一个空的 “New Bot”（2026-08 创建，没有设定、没有对话），判断不是在用的 bot，没有迁移。
