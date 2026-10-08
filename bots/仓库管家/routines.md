# 仓库管家的定时任务

## 1. 每日同步到 grokbot-home（daily-grokbot-sync）

- **触发**：每天 03:14（北京时间）。cron：`CRON_TZ=Asia/Shanghai 14 3 * * *`
- **状态**：本账号已于 2026-10-08 由仓库管家创建。新号上按下面的提示词重建。
- **详细步骤**：见 `scripts/sync.md`，脚本 `scripts/sync.sh`。
- **保存的提示词（重建时用 UpdateRoutine 创建）**：

```text
每日同步 grokbot-home：把本账号所有 bot 的新记忆、设定、技能和连接器清单同步到公开仓库 ZMGID/grokbot-home（本地 /workspace/grokbot-home），并做漂移检查。仓库是公开的：密钥只以加密形式存在 secrets/*.enc（用 scripts/secret-crypt.py 加解密，口令在环境变量 GROKBOT_HOME_PASSPHRASE），任何明文密钥、口令、验证码、密码、一次性授权链接都绝不能进仓库。旧的私有仓库 ZMGID/grokbot-home-private-old 不要再往里推。详细做法以仓库里的 scripts/sync.md 为准，先读它。
1) 确保 /workspace/grokbot-home 是最新的，origin 指向 ZMGID/grokbot-home（git pull --rebase；目录不存在就用 gh 克隆）。
2) 对 bots/agent-map.json 里的每个 bot（包括我自己 仓库管家，以及本账号新出现、还没登记的 bot）：读它自上次同步以来的对话记录和 /home/box/agent-data/agents/<id>/ 下的 profile.json、settings.json、memory/，把新的持久事实、项目进展、决定、偏好写成带日期的要点合并进 bots/<slug>/CONTEXT.md；设定变化写进 profile.md，定时任务变化写进 routines.md；关于用户本人、所有 bot 都该知道的写进根目录 CONTEXT.md。新 bot 要建 bots/<slug>/ 并登记到 agent-map.json、index.json、bots/README.md。因为仓库公开，写进去的内容要当作谁都能看到。
3) Grok Bot 的笔记：把 /workspace/assistant/big-picture.md 复制到仓库 bots/grok-bot/notes/big-picture.md，/workspace/assistant/routines.md 的定时任务内容同步进 bots/grok-bot/routines.md。/workspace/assistant/daily/ 绝不进仓库。
4) 漂移检查：把线上实际情况和仓库逐项对比并补齐：本账号现有的 bot 名单与 agent-map.json、index.json；每个 bot 的名字、标题、说明与 profile.md；每个 bot 的定时任务与 routines.md（我自己的看当前定时任务状态，别的 bot 读不到原文就在 Grok Bot 应用里发消息问那个 bot 要）；/home/box/agent-data/workflows/ 下的技能与 skills/；当前连接器状态与 connectors/README.md；已删除的 bot 要从仓库和 BOOTSTRAP 里去掉。
5) 运行 bash scripts/sync.sh：它会校验 remote 和分支，先做密钥扫描（scripts/secret-scan.sh），不通过就中止、不提交；通过且有变化才 commit + push。绝不绕过、放宽或改白名单来让扫描通过。
6) 结果发给这个聊天里的用户：没有变化就不发任何消息；有变化发一行中文说明（改了哪些 bot / 文件、补齐了哪些漂移）；密钥扫描失败、拉取或推送失败等出错时，说清原因和需要用户做什么（只说文件名和行号，不贴可疑内容），并在 Grok Bot 应用里发消息抄送给 Grok Bot（id a96070f7-cb92-4f15-bcd4-7b1e700cc676）。
```

如果每日同步要读别的 bot 的对话记录，需要有 ReadTranscript 工具（cursor 命名空间）。没有的话退而求其次：读 `/home/box/agent-data/agents/<id>/memory/` 和 `/home/box/agent-data/search-index.db` 的 `messages` 表（只读，先复制到 /tmp 再打开）。

## 2. 换号演练与安全审计

- **触发**：每周日下午（具体 cron 待用户确认）。建议形态：`CRON_TZ=Asia/Shanghai … * * 0`（周日）。
- **状态**：**待建**（2026-10-08；等用户确认后再用 UpdateRoutine 创建，尚未在本账号建好）。
- **内容概要**（见 profile 职责 3–4）：在 `/tmp` 匿名重克隆公开仓库，按 BOOTSTRAP 走一遍演练（不真建 bot）；解密 `secrets/*.enc` 确认可用；核对各 bot 的 profile/CONTEXT/routines 完整；并对公开仓库历史做密钥扫描。发现断点就修或告诉用户；遗留风险只提醒，不替用户删旧私有仓或改口令。
- **保存的提示词**：待用户确认创建时再写入。
