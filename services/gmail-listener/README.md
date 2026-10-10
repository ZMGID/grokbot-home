> 仓库副本：备份 `listener.py`、`run_loop.sh`、`start.sh`、`stop.sh`、本 README。
> **永不备份**：`venv/`、`listener.log`、`forwarded_ids.txt`、`seen.txt`、`failed.jsonl`、`supervisor.pid`、`__pycache__/`、`webhook_url.local`（含 webhook URL）。
> 运行时目录：`/workspace/gmail-listener/`。

# gmail-listener

Forwards Composio Gmail trigger events (`GMAIL_NEW_GMAIL_MESSAGE`) to the Grok Bot webhook routine **gmail-new-mail**
using Composio's realtime (Pusher websocket) channel via the Python SDK `composio.triggers.subscribe()`.
No public URL and no Composio webhook subscription needed.

Webhook URL is **not** in the repo. `listener.py` loads it from:
1. env `GMAIL_WEBHOOK_URL`, else
2. file `webhook_url.local` in the same directory (`chmod 600`), else
3. exits with error.

Trigger instances (Composio, labelIds=INBOX, interval=1 min requested):
- `ti_ePC_aV3eRSPT` → `ca_ZnzYtlTeic0s` (ohulercxm8@gmail.com, composio-pg)
- `ti_6ozhOAfOaHLq` → `ca_5jGHEthCoWuD` (zhimeng63@gmail.com, composio-zhimeng)

## Env / local secrets (runtime only; values never in repo)

| Name | Purpose |
|---|---|
| `COMPOSIO_API_KEY` | Composio project API key (same material as `~/.composio_pg_key`) |
| `GMAIL_WEBHOOK_KEY` | Webhook auth key (user supplies via secret prompt on new account) |
| `GMAIL_WEBHOOK_URL` | Full webhook URL (optional if `webhook_url.local` exists) |

## Files

| File | In repo? |
|---|---|
| `listener.py`, `run_loop.sh`, `start.sh`, `stop.sh`, `README.md` | yes |
| `webhook_url.local` | **no** (mode 600 on box) |
| `venv/`, `listener.log`, `forwarded_ids.txt`, `seen.txt`, `failed.jsonl`, `supervisor.pid` | **no** |

## New account / rebuild checklist

1. Recreate 小萌's webhook routine **gmail-new-mail** (folder `gmail-new-mail`; prompt in `bots/grok-bot/routines.md`).
2. User provides the new key into env **`GMAIL_WEBHOOK_KEY`** via secret prompt (never chat / never commit).
3. Write the new webhook URL into `/workspace/gmail-listener/webhook_url.local` (`chmod 600`) **or** set env `GMAIL_WEBHOOK_URL`.
4. Recreate Composio `GMAIL_NEW_GMAIL_MESSAGE` triggers per user if needed (ohulercxm8 → composio-pg; zhimeng63 → composio-zhimeng).
5. Restore scripts from this directory, build venv if missing, run `/workspace/gmail-listener/start.sh`.

## After a box restart

The box has no systemd/cron (PID 1 is tini), so nothing auto-starts. Run:
```bash
/workspace/gmail-listener/start.sh
```
(from a shell that has `COMPOSIO_API_KEY` and `GMAIL_WEBHOOK_KEY` in env, and URL via env or `webhook_url.local`).
Check: `tail listener.log`, `pgrep -af listener.py`. `start.sh` is idempotent.

## Rebuild venv if missing

```bash
cd /workspace/gmail-listener
python3 -m venv venv && ./venv/bin/pip install composio
```
