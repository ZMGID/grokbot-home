> 仓库副本（2026-10-10）。**不**备份 `~/.lark-cli/`、`~/.local/share/lark-cli/`、`/workspace/feishu-cli/survey/`、二维码/日志、消息正文。
> 飞书是 **Composio-only 规矩的例外**：Composio 无飞书 toolkit，故用官方 `lark-cli`。

# Feishu (飞书) CLI on this box

## What's installed
- Official CLI: **lark-cli** (npm `@larksuite/cli`, repo https://github.com/larksuite/cli, MIT), version **1.0.97**
- Installed with `npm install -g @larksuite/cli@latest` (user prefix, no sudo)
  - Launcher: `/home/box/.local/bin/lark-cli` (Node wrapper) -> Go binary `/home/box/.local/lib/node_modules/@larksuite/cli/bin/lark-cli`
  - `~/.local/bin` is NOT on the default PATH; it was appended to `~/.bashrc`. In non-login shells use the full path or `export PATH="$HOME/.local/bin:$PATH"`.
- Brand: `feishu` (China mainland, open.feishu.cn). Use `--brand lark` only for Lark international.
- Update: `lark-cli update` or `npm install -g @larksuite/cli@latest`.
- Optional agent skills (not installed): `npx skills add larksuite/cli -y -g`; skills are also readable via `lark-cli skills list/read`.

## Auth model (two layers)
1. **App credentials** (App ID + App Secret of a Feishu self-built app 自建应用) — `lark-cli config init`.
   - `lark-cli config init --new` (what we ran): prints a QR + URL `https://open.feishu.cn/page/cli?user_code=...`; the user
     opens it while logged into Feishu and the platform creates/configures an app for the CLI automatically. Code valid ~10 min.
   - Or bring an existing app: `printf '%s' "$FEISHU_APP_SECRET" | lark-cli config init --app-id "$FEISHU_APP_ID" --app-secret-stdin --brand feishu`
   - Env override also supported: `LARKSUITE_CLI_APP_ID`, `LARKSUITE_CLI_APP_SECRET`, `LARKSUITE_CLI_BRAND`.
   - This alone enables **bot identity** (`--as bot`, tenant_access_token).
2. **User OAuth** (device flow) — `lark-cli auth login --recommend` (or `--domain im,docs,base,approval`, `--scope ...`).
   - Agent mode: `lark-cli auth login --domain ... --no-wait --json` -> returns verification URL + device code; later
     `lark-cli auth login --device-code <CODE>` to finish. Enables `--as user`.
   - Check: `lark-cli auth status`, `lark-cli auth scopes`, `lark-cli doctor`.

## Where config/secrets live
- Config dir: `~/.lark-cli/` (override `LARKSUITE_CLI_CONFIG_DIR`). `lark-cli config show` to inspect.
- Secrets/tokens (Linux, no OS keychain): AES-encrypted files under `~/.local/share/lark-cli/` with a local `master.key`
  (override `LARKSUITE_CLI_DATA_DIR`). Anyone with box access can use them — the box is shared by all bots.

## MCP
- lark-cli itself has no MCP server mode. Official separate MCP server: npm `@larksuiteoapi/lark-mcp` (v0.5.1),
  run via `npx -y @larksuiteoapi/lark-mcp mcp -a <APP_ID> -s <APP_SECRET>` (check its --help; not installed).

## Logs
- `/workspace/feishu-cli/config-init.log` — output of the background `config init --new` run.

## Group chats
- See `chats.md`: 全员群 = oc_1bfe10631cc60ae750bbc378376f3c4d; bot 通知群 = oc_ba1ec97d712cc401cabc3a09c610dcbb (bot cli_aa430b6809f85d0c is a member).
