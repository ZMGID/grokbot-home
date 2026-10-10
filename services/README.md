# services/

盒子上的本地服务脚本备份（**不含密钥、不含邮件正文/主题状态文件**）。

| 目录 | 用途 | 运行时路径 | 换号/重启 |
|---|---|---|---|
| `gmail-listener/` | 把 Composio Gmail 新邮件触发推到小萌 webhook 例程 | `/workspace/gmail-listener/` | 手动 `start.sh`；重建触发器 + 用户提供 `GMAIL_WEBHOOK_KEY` |
| `feishu-cli/` | 飞书 lark-cli 说明与两个群 chat_id | CLI 在 `~/.local`；配置在 `~/.lark-cli/`（不进仓库） | `lark-cli config init --new --brand feishu` + `lark-cli auth login`（扫码） |
