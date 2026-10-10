> 仓库副本：仅备份 `start.sh` / `stop.sh` / 本 README。**不**备份 `venv/`、`listener.log`、`forwarded_ids.txt`、`seen.txt`、`failed.jsonl`、`listener.py`（可能含邮件主题）。
> 运行时目录：`/workspace/gmail-listener/`。密钥只来自环境变量 `COMPOSIO_API_KEY`、`GMAIL_WEBHOOK_KEY`（值不进仓库）。

# gmail-listener

Forwards Composio Gmail trigger events (GMAIL_NEW_GMAIL_MESSAGE) to the Grok Bot webhook routine
https://api2.cursor.sh/automations/webhook/<REDACTED-set-at-runtime>
using Composio's realtime (Pusher websocket) channel via the Python SDK `composio.triggers.subscribe()`.
No public URL and no Composio webhook subscription needed.

Trigger instances (Composio, labelIds=INBOX, interval=1 min requested):
- ti_ePC_aV3eRSPT -> ca_ZnzYtlTeic0s (ohulercxm8@gmail.com)
- ti_6ozhOAfOaHLq -> ca_5jGHEthCoWuD (zhimeng63@gmail.com)

## Env (required, read at runtime only; never stored here)
COMPOSIO_API_KEY, GMAIL_WEBHOOK_KEY

## Files
- listener.py       subscriber + forwarder (small JSON, no message body)
- run_loop.sh       supervisor loop (restarts listener.py 10s after any exit)
- start.sh          idempotent start (no-op if already running)
- stop.sh           stop everything
- listener.log      log (no secrets, no bodies); "connected and subscribed" = healthy; hourly heartbeat
- forwarded_ids.txt listener-local dedupe of message_ids
- failed.jsonl      events whose POST failed (not auto-retried)
- seen.txt          owned by the routine; listener doesn't touch it
- venv/             Python venv with `composio` SDK

## Forwarded JSON
{"event":"new_mail","account","connected_account_id","message_id","thread_id","subject","sender","timestamp"}
also {"event":"trigger_disabled"|"account_expired", "account","connected_account_id","trigger_id","timestamp"} if Composio emits them on the realtime channel.

## After a box restart
The box has no systemd/cron (PID 1 is tini), so nothing auto-starts. Run:
    /workspace/gmail-listener/start.sh
(from a shell that has COMPOSIO_API_KEY and GMAIL_WEBHOOK_KEY in env). Check: `tail listener.log`, `pgrep -af listener.py`.
Any agent/routine can call start.sh safely; it won't start a second copy.

## Rebuild venv if missing
    python3 -m venv venv && ./venv/bin/pip install composio
