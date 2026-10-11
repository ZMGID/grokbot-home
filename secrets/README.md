# secrets/

这里只放**加密后**的密钥/敏感数据，明文永远不进仓库（`.gitignore` 已拦截）。

- `COMPOSIO_API_KEY.enc`：用户贴给 bot 的 Composio 项目 API Key，用 `scripts/secret-crypt.py enc` 加密（scrypt N=2^20 + AES-256-CBC，文件头 `GBH1`）。文本模式。
- `COMPOSIO_API_KEY.box-current.enc`：旧号 box 上 `~/.composio_pg_key` 里实际在用的 key（和上面那份不同）。BOOTSTRAP 先用 `.enc`，composio-pg 连不上再用这份。
- `finance.tgz.enc`：`/workspace/finance/` 整树（README、csv、inbox/）的 gzip tar，用 `enc-bin` / `dec-bin` 加解密（二进制模式，解密时不做 ASCII 可打印检查）。**明文账本只存在于 box 的 `/workspace/finance/`，永不进 git。**
- （可选）`财务管家-memory.tgz.enc`：若 财务管家 的 `memory/` 有内容，每日同步会单独打成加密包；空则跳过。
- `box-secrets.tgz.enc`（2026-10-12）：box 上恢复所需的密钥文件，包内路径相对于 `/`：`home/box/.composio_pg_key`、`home/box/.lark-cli/config.json`、`home/box/.local/share/lark-cli/`（飞书 app secret、用户 token、master.key）、`home/box/.config/gh/`、`home/box/.gitconfig`、`home/box/.ssh/{config,known_hosts}`、`home/box/servers/`（eastforce 资料 + ssh 私钥）、`workspace/gmail-listener/webhook_url.local`、`home/box/.grokbot-home/secrets.env`（`COMPOSIO_API_KEY`、`GMAIL_WEBHOOK_KEY` 的 export 行；**不含**口令）。`enc-bin`。
- `daily.tgz.enc`：`/workspace/assistant/daily/`（包内相对 `/workspace`）。`enc-bin`。
- `feishu-cli.tgz.enc`：`/workspace/feishu-cli/` 全部（chats/approvals/survey/日志；包内相对 `/workspace`）。`enc-bin`。
- 以上四个 tgz 包（含 finance）都由 `scripts/pack-bundles.sh` 生成，`scripts/sync.sh` 每次调用；tar 固定排序/属主/mtime（mtime 统一为 1970），解密比对内容没变就不重新加密。恢复步骤见 `BOOTSTRAP.md` Step 0 (b++)。
- **仓库是公开的**：任何人都能下载这些 `.enc` 文件离线猜口令，所以口令要足够长（建议 4 个以上随机词或 16+ 位随机字符）。
- 解密需要用户的口令，放在环境变量 `GROKBOT_HOME_PASSPHRASE`（用 secret-request 向用户要，不要让用户贴在聊天里）。

## Composio key

```bash
python3 scripts/secret-crypt.py dec secrets/COMPOSIO_API_KEY.enc /home/box/.composio_pg_key
```

（口令错误时只报一行错误，不会写文件，也不会打印任何密钥材料。）

密钥轮换后：把新值写进 `~/.composio_pg_key`，再

```bash
python3 scripts/secret-crypt.py enc /home/box/.composio_pg_key secrets/COMPOSIO_API_KEY.enc
```

再 `bash scripts/secret-scan.sh` 后提交推送。

## 恢复账本（新 box / 换号）

口令已写入环境变量后：

```bash
cd /workspace/grokbot-home
umask 077
TMP=$(mktemp /tmp/finance.XXXXXX.tgz)
python3 scripts/secret-crypt.py dec-bin secrets/finance.tgz.enc "$TMP"
mkdir -p /workspace
tar -C /workspace -xzf "$TMP"
shred -u "$TMP" 2>/dev/null || rm -f "$TMP"
# 此时 /workspace/finance/ 已恢复；明文只留在 box，不要 git add
```

每日同步（`scripts/sync.sh`）会重新打包并 `enc-bin` 覆盖 `secrets/finance.tgz.enc`，使账本变更进入加密备份。

## 模式说明

| 模式 | 用途 |
|---|---|
| `enc` / `dec` | 文本密钥（Composio key 等）；`dec` 拒绝非 ASCII 可打印输出 |
| `enc-bin` / `dec-bin` | 二进制包（box-secrets / daily / feishu-cli / finance tarball）；`dec-bin` 跳过可打印检查 |

换口令：先用旧口令把各 `.enc` 解密到 `/tmp`（`umask 077`；二进制用 `dec-bin`），换成新口令的环境变量后重新 `enc`/`enc-bin`，删掉 `/tmp` 里的明文。
