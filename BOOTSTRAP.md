# BOOTSTRAP — self-setup for a fresh Grok Bot

> **You are a Grok Bot on a brand-new account.** The user (GitHub `ZMGID`) rotates between several Grok Bot accounts and just gave you this repo's link.
> Follow this file top to bottom to (1) configure yourself, (2) recreate every other bot, (3) verify, and (4) keep the repo up to date.
>
> 中文说明：你是新号上的 Grok Bot。用户把这个仓库链接发给你，意思是“按这里把你自己和其他 bot 都配好”。照下面的步骤一步步做。

**Ground rules / 规则**

- Talk to the user in **Chinese**, short and direct. Times in **Asia/Shanghai (UTC+8)**. 用中文、简短、北京时间。
- **Never put a secret in the repo, in chat, or in a log.** Secrets come only from a masked secret prompt (or 1Password). Never `cat` a key file. 密钥绝不进仓库/聊天/日志。
- Things that need the user: the Composio API key (masked), and only if Step 0 (b) fails the `gh` device code. No official connector auth clicks. Batch these. 需要用户的主要是填一次 Composio key；设备码仅作备用。尽量一次问完。
- Do the steps in order; if a step fails, note it, continue with the rest, and report it in the final checklist. 某步失败就记下来继续，最后汇报。
- The box (`/workspace`, `/home/box`) is shared by all bots on this account, so files you set up are visible to the bots you create.
- Send the user a one-line progress update after each major step (connectors, bots, self-check), not a wall of text.

---

## Step 0 — Composio key + private-repo access / 先拿 Composio key，再进私有仓库

This repo is **private**. Official GitHub / Origin connectors are **not** used (2026-10-08 rule: all apps only via Composio `composio-pg`). You must get the Composio API key **before** you can read BOOTSTRAP from the repo. The `composio-pg` launcher files live *inside* this private repo — so Step 0 bootstraps them **inline** (same content as `connectors/composio-pg/`), then uses Composio's GitHub (ZMGID) to authenticate `gh` and clone.

Do **(a) → (b) → (c)** in order. Never print the key or any access token. Never `cat` key files.

### (a) Composio API key → `~/.composio_pg_key`

1. If `test -s /home/box/.composio_pg_key` already succeeds, skip to (b).
2. Otherwise send a **secret-request** (SendToUser type `secret-request`, masked) with a Chinese label, e.g.
   「Composio 项目 API key（控制台 → 项目设置 → API Keys），用于 composio-pg；写入 ~/.composio_pg_key」。
   The value must land in `/home/box/.composio_pg_key`, then `chmod 600 /home/box/.composio_pg_key`.
3. Fallback if the secret prompt cannot write a file: ask the user to open **your desktop terminal** and type
   `read -rsp 'Composio key: ' K && umask 077 && printf %s "$K" > ~/.composio_pg_key && unset K`
   (they type it; you never see it). Never ask them to paste the key in chat.

### (b) Bootstrap composio-pg inline + clone via Composio GitHub

The launcher is tiny; write it without cloning the repo:

```bash
# uv if missing
command -v uv >/dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

mkdir -p /workspace/composio-pg
cat > /workspace/composio-pg/launch.py << 'PY'
import os, sys
from composio import Composio
key = open("/home/box/.composio_pg_key").read().strip()
s = Composio(api_key=key).create(user_id="pg-test-5be86c3e-d220-4538-ab6d-ae22d538dfde")
os.execvp("npx", ["npx", "-y", "mcp-remote", s.mcp.url, "--transport", "http-only", "--header", "x-api-key:" + key])
PY
cat > /workspace/composio-pg/launch.sh << 'SH'
#!/bin/bash
exec /workspace/composio-pg/.venv/bin/python /workspace/composio-pg/launch.py
SH
chmod 700 /workspace/composio-pg/launch.sh
chmod 600 /workspace/composio-pg/launch.py

cd /workspace/composio-pg
[ -x .venv/bin/python ] || uv venv -q .venv
uv pip install -q --python .venv/bin/python "composio==0.25.0" || uv pip install -q --python .venv/bin/python composio
npx -y mcp-remote --help >/dev/null 2>&1 || true
```

Smoke-test (never print stderr — mcp-remote logs `x-api-key` in clear text):

```bash
timeout 40 /workspace/composio-pg/launch.sh </dev/null >/dev/null 2>/tmp/cpg.err
grep -c "Proxy established successfully" /tmp/cpg.err
rm -f /tmp/cpg.err
```

`1` = OK. Then `AddMcpServer` name **`composio-pg`**, command **`/workspace/composio-pg/launch.sh`** (no args, no env).

Authenticate `gh` with the GitHub OAuth token already held by Composio (user `pg-test-5be86c3e-d220-4538-ab6d-ae22d538dfde`, toolkit `github` = ZMGID). Pipe the token — do not echo or write it to a tracked file:

```bash
# logs in gh as ZMGID using Composio's stored GitHub token; token never printed
/workspace/composio-pg/.venv/bin/python - <<'PY' | gh auth login --with-token
from composio import Composio
key = open("/home/box/.composio_pg_key").read().strip()
client = Composio(api_key=key)
for acc in client.connected_accounts.list(user_ids=["pg-test-5be86c3e-d220-4538-ab6d-ae22d538dfde"]).items:
    d = acc.model_dump() if hasattr(acc, "model_dump") else acc
    toolkit = (d.get("toolkit") or {}).get("slug") if isinstance(d, dict) else None
    if toolkit == "github" and d.get("status") == "ACTIVE":
        tok = (d.get("data") or {}).get("access_token")
        if tok:
            print(tok, end="")
            break
else:
    raise SystemExit("no ACTIVE github connected account")
PY
gh auth setup-git
gh auth status   # should show ZMGID; OK to show login name, never the token
```

Then go to Step 1 to clone.

### (c) Fallback — `gh auth login` device code

Only if (b)'s token login fails: run `gh auth login --hostname github.com --git-protocol https --web` in the background, send the user the one-time code + `https://github.com/login/device`（中文：「请打开这个链接输入验证码，授权 ZMGID」）, wait until it finishes, then Step 1. This is a handoff, not a secret. Do **not** install the official GitHub connector as a substitute.

## Step 1 — Clone / 克隆

```bash
gh repo clone ZMGID/grokbot-home /workspace/grokbot-home 2>/dev/null || (cd /workspace/grokbot-home && git pull --rebase)
cd /workspace/grokbot-home
git config user.name ZMGID
git config user.email 214914950+ZMGID@users.noreply.github.com
gh auth setup-git
```

Then read: `README.md`, `CONTEXT.md` (shared user memory), `connectors/README.md`, `bots/README.md`, `bots/index.json`.

## Step 2 — Tool environment / 工具环境

```bash
cd /workspace/grokbot-home
nohup bash setup.sh > /tmp/setup.log 2>&1 &
```

- Idempotent; heavy installs (KiCad 9, LibreOffice, PrusaSlicer, cadquery, PlatformIO ESP32 toolchain) can take 10–20 min — run in background, keep going with Step 3, check `/tmp/setup.log` later (the summary at the end lists anything that failed).
- `bash setup.sh --light` skips the heavy CAD/EDA packages if the user only needs the basics.
- It also refreshes the `composio-pg` launcher from the repo into `/workspace/composio-pg/` and rebuilds its venv. Step 0 already bootstrapped it inline; this keeps files in sync with `connectors/composio-pg/`. If the inline copy is missing for any reason, run:
  ```bash
  mkdir -p /workspace/composio-pg && cd /workspace/composio-pg
  install -m 700 /workspace/grokbot-home/connectors/composio-pg/launch.sh .
  install -m 600 /workspace/grokbot-home/connectors/composio-pg/launch.py .
  [ -x .venv/bin/python ] || uv venv -q .venv
  uv pip install -q --python .venv/bin/python "composio==0.25.0" || uv pip install -q --python .venv/bin/python composio
  npx -y mcp-remote --help >/dev/null 2>&1 || true
  ```
  (No `uv`? `curl -LsSf https://astral.sh/uv/install.sh | sh`.)

## Step 3 — Connectors / 连接器

Follow `connectors/README.md`. **Rule (2026-10-08): all app connections only through Composio (`composio-pg`).** Do **not** install or authenticate official GitHub (`cursor-github`), Origin, Finance (63408931), or the Composio OAuth plugin (32661537). New apps are added inside Composio for user `pg-test-5be86c3e-d220-4538-ab6d-ae22d538dfde`, never as separate connectors.

| Item | Action | User does |
|---|---|---|
| **composio-pg** | Already done in Step 0 if key + AddMcpServer succeeded; otherwise finish Step 0 (a)(b) | type Composio API key once (masked) |
| pstack plugin, **plugin id 9717366** | `InstallPlugin` (skills for dr eggbot — not an app connection) | nothing |
| Official GitHub / Origin / Finance / Composio plugin 32661537 | **skip** | nothing |

Confirm with `GetMcpServerStatus` that `composio-pg` is connected (tools appear as `user-composio-pg` / `COMPOSIO_*` on your next turn). Self-check GitHub + Gmail with `COMPOSIO_MANAGE_CONNECTIONS` `{"toolkits":["github","gmail"]}` (never `reinitiate_all`) → “All connections are active”, GitHub ZMGID.

Composio user: `pg-test-5be86c3e-d220-4538-ab6d-ae22d538dfde` (project `pr_lh5-8poHU4QB`), holding GitHub (ZMGID), Gmail ohulercxm8@gmail.com, Gmail zhimeng63@gmail.com. Nothing to re-authorize unless a new app is needed (add it in Composio console).

## Step 4 — Skills / 技能

- `skills/` currently has **no user skills** (see `skills/README.md`). For any `skills/<slug>/` that appears later: copy it to `/home/box/agent-data/workflows/<slug>/` (or create it with the `skill-authoring` skill using the same name and body), then confirm it is listed.
- Reinstall the **pstack** plugin (`InstallPlugin 9717366`) if not done in Step 3.
- Managed skills (add-connector, routines, …) come with the platform — nothing to do.

## Step 5 — Apply your own profile (primary bot) / 设置你自己

Primary = `bots/index.json` → `"primary": "grok-bot"`. Read `bots/grok-bot/profile.md`, `bots/grok-bot/CONTEXT.md`.

1. `update_state` target `profile`, action `set`: **name** `Grok Bot`, **description** = the exact English text in `bots/grok-bot/profile.md`, title empty.
2. Avatar: no custom image (default shape `blob`, color `black`). If a `bots/grok-bot/avatar.*` file ever exists, set it with `update_state` target `avatar`.
3. If you are not the primary bot, ask the user once whether to make you primary, then `SetPrimaryBot`.
4. Save the important facts from `/CONTEXT.md` + `bots/grok-bot/CONTEXT.md` into your memory (`update_state` target `memory`): user writes Chinese, rotates accounts, GitHub ZMGID, repo `ZMGID/grokbot-home` is the source of truth, secrets never in repo, Composio via `composio-pg`.
5. If the bot the user opened is **not** the Grok Bot primary (e.g. they opened a bot with another name), still act as the bootstrapper: apply `grok-bot`'s profile only if the user agrees; otherwise create `grok-bot` in Step 6 like the others.

## Step 6 — Recreate every other bot / 用 CreateAgent 重建其他 bot

For **each** folder in `bots/` except the primary (today: `xiaozhi`, `dr-eggbot`, `仓库管家`; also any new folder listed in `bots/index.json`):

1. Read `bots/<slug>/profile.md`.
2. Call **CreateAgent** with:
   - **name**: exactly as in profile.md (`小枳`, `dr eggbot`, `仓库管家`)
   - **title**: as in profile.md (currently empty)
   - **description / instructions**: the text block in profile.md (xiaozhi's is reconstructed; dr eggbot's is the original English text — keep it verbatim), **plus** this line appended:
     `On your first turn, read /workspace/grokbot-home/CONTEXT.md and /workspace/grokbot-home/bots/<slug>/CONTEXT.md, save the key facts to your memory, then recreate your routines from bots/<slug>/routines.md.`
     （中文可写成：“第一次启动先读 /workspace/grokbot-home/CONTEXT.md 和 bots/<slug>/CONTEXT.md，把要点存进自己的记忆，再按 bots/<slug>/routines.md 重建定时任务。”）
   - avatar: default shape/color from profile.md if CreateAgent accepts it; set an image only if `bots/<slug>/avatar.*` exists.
   - If CreateAgent accepts a first message / task, pass the same “read your CONTEXT.md” instruction there too.
3. Record the new agent id: update `bots/agent-map.json` (`{"<slug>": "<new id>"}`) — needed by the daily sync.
4. Send the user one line per bot created (“已重建 小枳 ✓”).

Do not create the empty “New Bot” from the old account (it was never used).

## Step 7 — Routines / 定时任务

Routines belong to the bot that creates them, so:

- **You (grok-bot)**: do **not** create the daily sync. It belongs to **仓库管家** (handed over 2026-10-08).
- **Other bots**: each recreates its own from `bots/<slug>/routines.md` on its first turn (that's why Step 6 tells them to).
  - `仓库管家`: create the daily sync with UpdateRoutine using the prompt in `bots/仓库管家/routines.md`
    — schedule `CRON_TZ=Asia/Shanghai 14 3 * * *` (≈03:14 Beijing time daily). Details: `scripts/sync.md`.
  - `xiaozhi`: none.
  - `dr-eggbot`: two routines — weekday 08:44 bot-friction scan, Monday 08:49 routine-waste audit — **create both, then pause both** (they were paused on the old account).
- After a few minutes, check each bot did it (read their transcript with ReadTranscript, or ask the user to glance at the routines panel). If a bot can't create routines, create them yourself only if the user agrees.

## Step 8 — Self-check / 自检

Run and record each result:

1. `GetMcpServerStatus`: **composio-pg** = connected. Official GitHub / Origin / Finance / Composio plugin should be absent or ignored (not required).
2. `user-composio-pg` → `COMPOSIO_MANAGE_CONNECTIONS` with `{"toolkits": ["github", "gmail"]}` (never `reinitiate_all`) → “All connections are active”, GitHub login **ZMGID**, Gmail ohulercxm8@gmail.com. Optionally confirm zhimeng63@gmail.com by fetching 1 recent email from each Gmail account.
3. `gh auth status` shows login **ZMGID** (from Step 0 Composio token or device-code fallback).
4. Skills: pstack skills listed; every `skills/<slug>` present in `/home/box/agent-data/workflows/`.
5. Bots: every slug in `bots/index.json` exists with the right name; `bots/agent-map.json` updated.
6. Routines: daily sync exists on **仓库管家**; dr eggbot's two exist and are paused; grok-bot has no daily sync.
7. Tools: `tail -20 /tmp/setup.log` summary; spot-check `kicad-cli --version` (9.x), `~/.local/bin/pio --version`, `python3 -c "import cadquery"`, `gitleaks version`.
8. Secret scan: `bash scripts/secret-scan.sh` → “干净”.

## Step 9 — Write-back rule / 写回规则（永久）

- New durable knowledge goes back into the right file: about the user → `/CONTEXT.md`; about one bot's work → `bots/<slug>/CONTEXT.md`; profile changes → `profile.md`; routine changes → `routines.md`; connector changes → `connectors/README.md`; new tools → `setup.sh`.
- Then `bash scripts/secret-scan.sh` and `git add -A && git commit -m "<what>" && git push`. The daily sync does this automatically for all bots, but write back immediately after anything important.
- Never commit: keys, tokens, `.env`, one-time codes, passwords, auth links, `/home/box/agent-data/*secrets*.json`, databases.
- New bot created later (e.g. by dr eggbot)? Add `bots/<slug>/` (profile.md, CONTEXT.md, routines.md) + `index.json` + `agent-map.json` + `bots/README.md` table.

## Step 10 — Report to the user / 最后汇报

Send one short Chinese message: what's done, what failed, what the user still needs to do. Then the checklist below with ✅/❌.

---

## Final checklist / 最终清单

- [ ] Step 0: `/home/box/.composio_pg_key` exists, mode 600 (value never shown)
- [ ] Step 0/3: `composio-pg` added (`/workspace/composio-pg/launch.sh`) and connected
- [ ] Step 0: `gh` logged in as ZMGID (via Composio GitHub token, or device-code fallback)
- [ ] Step 1: repo cloned at `/workspace/grokbot-home`, git identity set
- [ ] Step 2: `setup.sh` finished (summary checked; failures listed)
- [ ] Step 3: pstack (9717366) installed; official GitHub/Origin/Finance/Composio-plugin **not** installed
- [ ] Step 4: skills imported (currently none) 
- [ ] Step 5: own profile = Grok Bot, primary, memory seeded from CONTEXT.md
- [ ] Step 6: 小枳 / dr eggbot / 仓库管家 created; `bots/agent-map.json` updated & pushed
- [ ] Step 7: daily sync routine (03:14 Asia/Shanghai) on **仓库管家** (recreated by 仓库管家 from `bots/仓库管家/routines.md` on its first turn; grok-bot does not create it); dr eggbot's 2 routines created and paused
- [ ] Step 8: composio-pg GitHub (ZMGID) + Gmail active via COMPOSIO_MANAGE_CONNECTIONS; secret scan clean
- [ ] Step 9: write-back rule saved in memory
- [ ] Step 10: user got the summary
