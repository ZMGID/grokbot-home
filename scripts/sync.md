# 每日同步任务说明（daily-grokbot-sync）

- **谁跑**：**仓库管家**（2026-10-08 用户改口：单独建同步 bot，由仓库管家跑每日同步；原先「不单独建同步 bot、由主 bot 跑」已作废）。
- **什么时候**：每天约 03:14（北京时间），cron `CRON_TZ=Asia/Shanghai 14 3 * * *`。提示词见 `bots/仓库管家/routines.md`。
- **原则**：有变化才提交推送，没变化不打扰用户；推送前必须通过密钥扫描；任何密钥、验证码、密码、一次性授权链接都不进仓库。

## 每次运行做什么

1. **拉最新**：`cd /workspace/grokbot-home && git pull --rebase`（目录不存在就 `git clone https://github.com/ZMGID/grokbot-home /workspace/grokbot-home`；仓库公开，克隆不需要登录，但**推送需要 `gh` 以 ZMGID 登录**，见 BOOTSTRAP Step 1）。
2. **收集每个 bot 的新记忆**（仓库管家自己做，需要“读懂”）：
   - 本账号所有 bot：`/home/box/agent-data/agents/<id>/`（id ↔ slug 见 `bots/agent-map.json`；出现新的 bot 就新建 `bots/<slug>/` 并加进 `agent-map.json`、`index.json`、`bots/README.md`）。
   - 读上次同步以后的对话：优先用 ReadTranscript（cursor 命名空间，`agent_id`，用 `before` 往前翻页）；没有这个工具时，只读地复制
     `/home/box/agent-data/search-index.db*` 到 `/tmp`，查 `messages` 表（`agent_id`、`timestamp_ms`、`body`）。
   - 把新的**持久**信息合并进 `bots/<slug>/CONTEXT.md`：项目进展、决定、用户新偏好、待办状态变化。写成要点，带日期，不贴大段原文。
   - 关于用户本人、所有 bot 都需要知道的 → 根目录 `CONTEXT.md`。
   - 设定变化（名字、description、头像）→ `profile.md`；定时任务新增/修改/暂停 → `routines.md`。
   - **主 bot（小萌 / slug grok-bot）笔记**：把 `/workspace/assistant/big-picture.md` 复制到 `bots/grok-bot/notes/big-picture.md`；如有需要把 `/workspace/assistant/routines.md` 的定时任务内容同步进 `bots/grok-bot/routines.md`。**绝不**把 `/workspace/assistant/daily/` 拷进仓库。
   - **财务管家账本**：`/workspace/finance/` **绝不**拷进仓库，也不在 CONTEXT/commit message 里摘录金额、账号、卡号、流水。与 daily/ 同级禁忌。
3. **运行 `bash scripts/sync.sh`**，它负责机械部分：
   - 按 `bots/agent-map.json` 把每个 bot 的 `profile.json`、`settings.json`（去掉 serverId）、`memory/`、自定义头像复制到 `bots/<slug>/raw/`；**例外：`财务管家` 跳过 `memory/`**（可能含金额/流水）；
   - 把 `/home/box/agent-data/workflows/` 下的用户技能复制到 `skills/`；
   - 生成 `scripts/env-snapshot.md`（工具环境快照，发现 setup.sh 漏装的东西就顺手补进 setup.sh）；
   - `git add -A` 后运行 `scripts/secret-scan.sh`（gitleaks 工作区 + 历史；rg 模式扫描所有将提交的文件，含隐藏文件；确认 `~/.composio_pg_key`、两份 `secrets/*.enc` 的明文、口令 `GROKBOT_HOME_PASSPHRASE` 都没出现在文件和未推送提交里；`secrets/` 下只能有 `GBH1` 加密文件；**任何已跟踪的 `finance/`、`assistant/daily/` 路径或账本类文件名一律失败**）——**不干净就撤销暂存、中止，不提交**；
   - 没有变化就退出；有变化就 `git commit -m "sync: <时间> Asia/Shanghai"` 并 `git push origin HEAD:main`（被拒会 pull --rebase 后重试一次）。脚本开头会确认 remote 是 `ZMGID/grokbot-home`、分支是 `main`。
4. **连接器清单**：用 GetMcpServerStatus 看当前连接器，和 `connectors/README.md` 对比；有新增/删除/状态变化就更新清单（只写名字、id、地址、步骤）。
5. **汇报**：
   - 没有变化：不发消息。
   - 有变化：在**仓库管家**的聊天里给用户发一行中文摘要（例如“已同步：小枳 CONTEXT +3 条，connectors 新增 Notion”）。
   - 密钥扫描失败 / 推送失败：在聊天里说明原因（只说文件名和行号，不贴内容）。

## 手动跑

```bash
cd /workspace/grokbot-home
bash scripts/sync.sh --dry-run   # 收集文件 + 扫描，显示会提交什么，不提交（收集到的文件留在工作区）
bash scripts/sync.sh             # 正式同步
bash scripts/secret-scan.sh      # 只做密钥扫描
```

## 注意
- 别的 bot 在新号上的 agent id 和旧号不同：BOOTSTRAP 第 6 步建完 bot 后要把新 id 写进 `bots/agent-map.json` 并提交，否则 raw 快照会跳过。
- 不要把 `/home/box/agent-data/` 下的 `box-secrets.json`、`host-secrets.json`、`gateway.json`、`store.db`、`conversation-blobs.db` 复制进仓库。
- 不要把 `/workspace/finance/` 或 `/workspace/assistant/daily/` 复制进仓库；`.gitignore` 已忽略；扫描脚本会拦。
- 不要把 `/workspace/gmail-listener/` 的 `venv/`、`*.log`、`seen.txt`、`forwarded_ids.txt`、`failed.jsonl` 或 `~/.lark-cli/`、`~/.local/share/lark-cli/`、`feishu-cli/survey/` 复制进仓库。只同步 `services/` 里已备份的安全文件。
- 环境变量 `GMAIL_WEBHOOK_KEY` / Composio API key 的**值**永不进仓库（变量名可以写在文档里）。
