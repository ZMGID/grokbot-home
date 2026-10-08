# 仓库管家的定时任务

## 1. 每日同步到 grokbot-home（daily-grokbot-sync）

- **触发**：每天 03:14（北京时间）。cron：`CRON_TZ=Asia/Shanghai 14 3 * * *`
- **状态**：本账号已于 2026-10-08 由仓库管家创建。新号上按下面的提示词重建。
- **详细步骤**：见 `scripts/sync.md`，脚本 `scripts/sync.sh`。
- **保存的提示词（重建时用 UpdateRoutine 创建）**：

```text
每日同步 grokbot-home：把本账号所有 bot 的新记忆、设定、技能和连接器清单同步到公开仓库 ZMGID/grokbot-home（本地 /workspace/grokbot-home）。仓库是公开的：密钥只以加密形式存在 secrets/*.enc（用 scripts/secret-crypt.py 加解密，口令在环境变量 GROKBOT_HOME_PASSPHRASE），任何明文密钥、口令、验证码、密码、一次性授权链接都绝不能进仓库。旧的私有仓库 ZMGID/grokbot-home-private-old 不要再往里推。详细做法以仓库里的 scripts/sync.md 为准，先读它。
1) 确保 /workspace/grokbot-home 是最新的，origin 指向 ZMGID/grokbot-home（git pull --rebase；目录不存在就用 gh 克隆）。
2) 对 bots/agent-map.json 里的每个 bot（包括我自己 仓库管家，以及本账号新出现、还没登记的 bot）：读它自上次同步以来的对话记录和 /home/box/agent-data/agents/<id>/ 下的 profile.json、settings.json、memory/，把新的持久事实、项目进展、决定、偏好写成带日期的要点合并进 bots/<slug>/CONTEXT.md；设定变化写进 profile.md，定时任务变化写进 routines.md；关于用户本人、所有 bot 都该知道的写进根目录 CONTEXT.md。新 bot 要建 bots/<slug>/ 并登记到 agent-map.json、index.json、bots/README.md。因为仓库公开，写进去的内容要当作谁都能看到。
3) 用当前连接器状态更新 connectors/README.md（只写名字、id、地址、步骤）；用户技能由 sync.sh 从 /home/box/agent-data/workflows/ 复制到 skills/。
4) 运行 bash scripts/sync.sh：它会校验 remote 和分支，先做密钥扫描（scripts/secret-scan.sh），不通过就中止、不提交；通过且有变化才 commit + push。绝不绕过、放宽或改白名单来让扫描通过。
5) 结果发给这个聊天里的用户：没有变化就不发任何消息；有变化发一行中文说明（改了哪些 bot / 文件）；密钥扫描失败、拉取或推送失败等出错时，说清原因（只说文件名和行号，不贴可疑内容）。
```

如果每日同步要读别的 bot 的对话记录，需要有 ReadTranscript 工具（cursor 命名空间）。没有的话退而求其次：读 `/home/box/agent-data/agents/<id>/memory/` 和 `/home/box/agent-data/search-index.db` 的 `messages` 表（只读，先复制到 /tmp 再打开）。
