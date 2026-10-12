# grokbot-home 迁移清单（2026-10-12 18:40 核对）

公开仓库：https://github.com/ZMGID/grokbot-home  
最新同步提交：f9f52f5（2026-10-12 03:20 Asia/Shanghai）

## 已加密进仓库（换号可解密恢复）

| 文件 | 内容 |
|---|---|
| `secrets/COMPOSIO_API_KEY.enc` | 用户贴过的 Composio 项目 key |
| `secrets/COMPOSIO_API_KEY.box-current.enc` | box 上实际在用的 Composio key（备用） |
| `secrets/box-secrets.tgz.enc` | `~/.composio_pg_key`；`~/.lark-cli/` + `~/.local/share/lark-cli/`（app cli_aa430b6809f85d0c）；`~/.config/gh/`；`~/.gitconfig`；`~/.ssh/{config,known_hosts}`；`~/servers/`（eastforce）；`/workspace/gmail-listener/webhook_url.local`；`~/.grokbot-home/secrets.env`（COMPOSIO_API_KEY / GMAIL_WEBHOOK_KEY，不含口令） |
| `secrets/daily.tgz.enc` | `/workspace/assistant/daily/` |
| `secrets/feishu-cli.tgz.enc` | `/workspace/feishu-cli/` |
| `secrets/finance.tgz.enc` | `/workspace/finance/` 账本 |

bots/（小萌、小枳、事务秘书、仓库管家、代码工程师、搭建运维、硬件工程师、财务管家）、connectors/composio-pg + composio-zhimeng、BOOTSTRAP.md、agent-map 均在仓库明文配置侧。

## 本机现场（2026-10-12 18:38）

- Composio key 文件在；gh 已登录 ZMGID（gist, read:org, repo）
- gmail-listener 目录与 `webhook_url.local` 在
- lark-cli：auth status 显示 bot ready / user missing，但 `im +chat-list` 实测报错 20069「应用未启用」（与晚报一致）
- `ZMGID/grokbot-home-private-old` 仍存在（private）

## 换号仍需要你动手的（无法只靠解密）

1. 一次 masked 填入 `GROKBOT_HOME_PASSPHRASE`（解密全部 `.enc`）
2. 飞书：开发者后台启用应用 `cli_aa430b6809f85d0c`；用户身份再 `lark-cli auth login` 扫码（约 7 天不用会过期）
3. 新号重建例程 `gmail-new-mail` 后，换新 webhook URL/KEY，写回 `webhook_url.local` 与 secrets.env，再 sync
4. Composio：`composio-pg`（ohulercxm8 + GitHub）、`composio-zhimeng`（zhimeng63）若未 ACTIVE，各点一次授权
5. 平台侧 secret：新号可再 masked 提供 `COMPOSIO_API_KEY`、`GMAIL_WEBHOOK_KEY`（比只靠解密更稳）
6. 可选：删除 `ZMGID/grokbot-home-private-old`（含历史明文 Composio key）

恢复步骤以仓库内 `BOOTSTRAP.md` Step 0 为准。
