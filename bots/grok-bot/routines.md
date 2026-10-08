# grok-bot 的定时任务

## 1. 每日同步到 grokbot-home（daily-grokbot-sync）

- **触发**：每天约 03:14（北京时间）。cron：`CRON_TZ=Asia/Shanghai 14 3 * * *`
- **状态**：旧号上已于 2026-10-08 由主 bot 创建。新号上按下面的提示词重建。
- **详细步骤**：见 `scripts/sync.md`，脚本 `scripts/sync.sh`。
- **保存的提示词（重建时用 UpdateRoutine 创建）**：

```text
每日同步 grokbot-home：把本账号所有 bot 的新记忆和设定同步到私有仓库 ZMGID/grokbot-home。
1) 确保 /workspace/grokbot-home 是最新的（git pull --rebase）。
2) 对 bots/ 下每个 bot（以及本账号新出现的 bot）：读它自上次同步以来的对话记录（ReadTranscript）和 /home/box/agent-data/agents/<id>/ 下的 profile.json、settings.json、memory/，把新的持久事实、项目进展、偏好合并进 bots/<名字>/CONTEXT.md，设定变化写进 profile.md，定时任务变化写进 routines.md；关于用户本人、所有 bot 都该知道的写进根目录 CONTEXT.md。不要抄录密钥、验证码、密码、一次性链接。
3) 更新 skills/（/home/box/agent-data/workflows/ 下的用户技能）和 connectors/README.md（当前连接器状态）。
4) 运行 bash scripts/sync.sh：它会做密钥扫描（gitleaks，失败则 rg 兜底），扫描不干净就中止且不推送；干净且有变化才 commit + push。
5) 结果：没有变化就不发消息；有变化只在这个聊天里给用户发一行中文摘要（改了哪些 bot / 文件）；密钥扫描失败或推送失败时在这个聊天里告诉用户原因。
```

如果每日同步要读别的 bot 的对话记录，需要主 bot 有 ReadTranscript 工具（cursor 命名空间）。没有的话退而求其次：读 `/home/box/agent-data/agents/<id>/memory/` 和 `/home/box/agent-data/search-index.db` 的 `messages` 表（只读，先复制到 /tmp 再打开）。
