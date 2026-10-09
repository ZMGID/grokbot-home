# BOOTSTRAP — self-setup for a fresh Grok Bot

> **You are a Grok Bot on a brand-new account.** The user (GitHub `ZMGID`) rotates between several Grok Bot accounts and just gave you this repo's link (public repo: `https://github.com/ZMGID/grokbot-home`).
> Follow this file top to bottom to (1) configure yourself, (2) recreate every other bot, (3) verify, and (4) keep the repo up to date.
>
> 中文说明：你是新号上的 Grok Bot。用户把这个仓库链接发给你，意思是“按这里把你自己和其他 bot 都配好”。照下面的步骤一步步做。

**Ground rules / 规则**

- Talk to the user in **Chinese**, short and direct. Times in **Asia/Shanghai (UTC+8)**. 用中文、简短、北京时间。
- **Never put a secret in the repo, in chat, or in a log.** Secrets come only from a masked secret prompt (or 1Password). Never `cat` a key file. 密钥绝不进仓库/聊天/日志。
- Things that need the user: the repo passphrase `GROKBOT_HOME_PASSPHRASE` once (masked secret-request). Only if something fails: the Composio API key itself (masked), or a `gh` device code for push access. No official connector auth clicks. Batch these. 需要用户做的只有在密码框里填一次仓库口令；Composio key 和设备码仅作备用。尽量一次问完。
- Do the steps in order; if a step fails, note it, continue with the rest, and report it in the final checklist. 某步失败就记下来继续，最后汇报。
- The box (`/workspace`, `/home/box`) is shared by all bots on this account, so files you set up are visible to the bots you create.
- Send the user a one-line progress update after each major step (connectors, bots, self-check), not a wall of text.

---

## Step 0 — Clone, passphrase, Composio key, composio-pg / 克隆 → 口令 → 解密 key → 装 composio-pg

This repo is **public**: clone it anonymously, no GitHub login needed. The Composio API key is in the repo **only encrypted** (`secrets/*.enc`); the user gives you the passphrase through a masked secret-request. Official GitHub / Origin connectors are **not** used (2026-10-08 rule: all apps only via Composio `composio-pg`). Never print the key, the passphrase, or any token. Never `cat` key files.
仓库是公开的，匿名克隆即可；Composio key 只以加密形式放在 `secrets/`，口令用密码框向用户要。

### (a) Anonymous clone / 匿名克隆

```bash
GIT_TERMINAL_PROMPT=0 git -c credential.helper= clone https://github.com/ZMGID/grokbot-home /workspace/grokbot-home \
  || (cd /workspace/grokbot-home && git pull --rebase)
cd /workspace/grokbot-home
git config user.name ZMGID
git config user.email 214914950+ZMGID@users.noreply.github.com
```

Then read: `README.md`, `CONTEXT.md` (shared user memory), `connectors/README.md`, `bots/README.md`, `bots/index.json`.

### (b) Passphrase → decrypt the Composio key to `~/.composio_pg_key`

1. If `test -s /home/box/.composio_pg_key` already succeeds, skip to (c).
2. Check whether the passphrase is already in the environment (never echo it): `[ -n "$GROKBOT_HOME_PASSPHRASE" ] && echo set || echo missing`.
   If missing, send a **secret-request** (SendToUser type `secret-request`, masked) named **`GROKBOT_HOME_PASSPHRASE`** with a Chinese label, e.g.
   「grokbot-home 仓库的解密口令（GROKBOT_HOME_PASSPHRASE），用来解密 Composio key」. It shows up as an env var in **new** box shells; if the current shell still says `missing`, start a fresh shell (e.g. `bash -lc '…'`). Never ask for it in chat.
3. Decrypt (needs ~1 GiB RAM, a few seconds; prints nothing on success, only a short error on a wrong passphrase):
   ```bash
   cd /workspace/grokbot-home
   python3 scripts/secret-crypt.py dec secrets/COMPOSIO_API_KEY.enc /home/box/.composio_pg_key && chmod 600 /home/box/.composio_pg_key
   ```
   `secrets/COMPOSIO_API_KEY.enc` = the key the user pasted; `secrets/COMPOSIO_API_KEY.box-current.enc` = the key composio-pg was last running on. If the smoke test in (c) fails, decrypt `.box-current.enc` to the same path and retest.
4. Fallback only if decryption fails (wrong passphrase twice / files missing): ask for the Composio project API key itself with a masked secret-request
   「Composio 项目 API key（控制台 → 项目设置 → API Keys），用于 composio-pg；写入 ~/.composio_pg_key」, or have the user type it in **your desktop terminal**:
   `read -rsp 'Composio key: ' K && umask 077 && printf %s "$K" > ~/.composio_pg_key && unset K`. Never in chat.

### (c) Install composio-pg from the repo + smoke test

```bash
command -v uv >/dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
mkdir -p /workspace/composio-pg && cd /workspace/composio-pg
install -m 700 /workspace/grokbot-home/connectors/composio-pg/launch.sh .
install -m 600 /workspace/grokbot-home/connectors/composio-pg/launch.py .
[ -x .venv/bin/python ] || uv venv -q .venv
uv pip install -q --python .venv/bin/python "composio==0.25.0" || uv pip install -q --python .venv/bin/python composio
npx -y mcp-remote --help >/dev/null 2>&1 || true    # needs node/npx (present on the box; setup.sh installs it otherwise)
```

`launch.sh` runs `/workspace/composio-pg/.venv/bin/python launch.py`, so the venv above is required. Smoke-test (never print stderr — mcp-remote logs `x-api-key` in clear text):

```bash
timeout 40 /workspace/composio-pg/launch.sh </dev/null >/dev/null 2>/tmp/cpg.err
grep -c "Proxy established successfully" /tmp/cpg.err
rm -f /tmp/cpg.err
```

`1` = OK (`0` → try the `.box-current.enc` key from (b)3, then the (b)4 fallback). Then `AddMcpServer` name **`composio-pg`**, command **`/workspace/composio-pg/launch.sh`** (no args, no env).

## Step 1 — Push access (only for write-back / daily sync) / 推送权限（只有写回和每日同步需要）

Setup itself needs **no** GitHub login. `gh` must be logged in as ZMGID only to **push** (Step 6 `agent-map.json`, Step 9 write-back, 仓库管家's daily sync). Do this after composio-pg works; if it fails, keep going and list it in the report.

**Preferred:** log `gh` in with the GitHub OAuth token Composio already holds (user `pg-test-5be86c3e-d220-4538-ab6d-ae22d538dfde`, toolkit `github` = ZMGID). Pipe it — never echo it or write it to a file:

```bash
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
gh auth status   # should show ZMGID; OK to show the login name, never the token
```

**Fallback:** `gh auth login --hostname github.com --git-protocol https --web` in the background, send the user the one-time code + `https://github.com/login/device`（「请打开这个链接输入验证码，授权 ZMGID（只用于往仓库推送）」）. This is a handoff, not a secret. Do **not** install the official GitHub connector as a substitute.

## Step 2 — Tool environment / 工具环境

```bash
cd /workspace/grokbot-home
nohup bash setup.sh > /tmp/setup.log 2>&1 &
```

- Idempotent; heavy installs (KiCad 9, LibreOffice, PrusaSlicer, cadquery, PlatformIO ESP32 toolchain) can take 10–20 min — run in background, keep going with Step 3, check `/tmp/setup.log` later (the summary at the end lists anything that failed).
- `bash setup.sh --light` skips the heavy CAD/EDA packages if the user only needs the basics.
- It also refreshes the `composio-pg` launcher from the repo into `/workspace/composio-pg/` and rebuilds its venv if needed (same as Step 0 (c)). If `/workspace/composio-pg` is missing for any reason, run:
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
| **composio-pg** | Already done in Step 0 if decrypt + AddMcpServer succeeded; otherwise finish Step 0 (b)(c) | type the repo passphrase once (masked) |
| pstack plugin, **plugin id 9717366** | optional `InstallPlugin`（可选，原为 dr eggbot 安装；技能插件，不是应用连接） | nothing |
| Official GitHub / Origin / Finance / Composio plugin 32661537 | **skip** | nothing |

Confirm with `GetMcpServerStatus` that `composio-pg` is connected (tools appear as `user-composio-pg` / `COMPOSIO_*` on your next turn). Self-check GitHub + Gmail with `COMPOSIO_MANAGE_CONNECTIONS` `{"toolkits":["github","gmail"]}` (never `reinitiate_all`) → “All connections are active”, GitHub ZMGID.

Composio user: `pg-test-5be86c3e-d220-4538-ab6d-ae22d538dfde` (project `pr_lh5-8poHU4QB`), holding GitHub (ZMGID), Gmail ohulercxm8@gmail.com, Gmail zhimeng63@gmail.com. Nothing to re-authorize unless a new app is needed (add it in Composio console).

## Step 4 — Skills / 技能

- `skills/` currently has **no user skills** (see `skills/README.md`). For any `skills/<slug>/` that appears later: copy it to `/home/box/agent-data/workflows/<slug>/` (or create it with the `skill-authoring` skill using the same name and body), then confirm it is listed.
- **pstack** plugin (`InstallPlugin 9717366`) is **optional**（可选，原为 dr eggbot 安装）. Install only if a coding bot needs those skills.
- Managed skills (add-connector, routines, …) come with the platform — nothing to do.

## Step 5 — Apply your own profile (primary bot) / 设置你自己

Primary = `bots/index.json` → `"primary": "grok-bot"`. Read `bots/grok-bot/profile.md`, `bots/grok-bot/CONTEXT.md`.

1. `update_state` target `profile`, action `set`: **name** `小萌` (formerly `Grok Bot`, renamed 2026-10-08; slug stays `grok-bot`), **description** = the exact English text in `bots/grok-bot/profile.md`, title empty.
2. Avatar: no custom image (default shape `blob`, color `black`). If a `bots/grok-bot/avatar.*` file ever exists, set it with `update_state` target `avatar`.
3. If you are not the primary bot, ask the user once whether to make you primary, then `SetPrimaryBot`.
4. Save the important facts from `/CONTEXT.md` + `bots/grok-bot/CONTEXT.md` into your memory (`update_state` target `memory`): user writes Chinese, rotates accounts, GitHub ZMGID, repo `ZMGID/grokbot-home` (public) is the source of truth, no plaintext secrets in the repo (only `secrets/*.enc`), Composio via `composio-pg`.
5. If the bot the user opened is **not** the primary (`小萌` / slug `grok-bot`), still act as the bootstrapper: apply `grok-bot`'s profile only if the user agrees; otherwise create `grok-bot` in Step 6 like the others.

## Step 6 — Recreate every other bot / 用 CreateAgent 重建其他 bot

For **each** folder in `bots/` except the primary — driven by `bots/index.json`. Current set (2026-10-08): `xiaozhi`（小枳）, `仓库管家`, `代码工程师`, `搭建运维`, `事务秘书`, `硬件工程师`. **Do not** recreate deleted `dr-eggbot`.

1. Read `bots/<slug>/profile.md`.
2. Call **CreateAgent** with:
   - **name**: exactly as in profile.md (`小枳`, `仓库管家`, `代码工程师`, `搭建运维`, `事务秘书`, `硬件工程师`)
   - **title**: as in profile.md (currently empty)
   - **description / instructions**: the text block in profile.md (keep verbatim; xiaozhi's is reconstructed), **plus** this line appended:
     `On your first turn, read /workspace/grokbot-home/CONTEXT.md and /workspace/grokbot-home/bots/<slug>/CONTEXT.md, save the key facts to your memory, then recreate your routines from bots/<slug>/routines.md.`
     （中文可写成：“第一次启动先读 /workspace/grokbot-home/CONTEXT.md 和 bots/<slug>/CONTEXT.md，把要点存进自己的记忆，再按 bots/<slug>/routines.md 重建定时任务。”）
   - avatar: default shape/color from profile.md if CreateAgent accepts it; set an image only if `bots/<slug>/avatar.*` exists.
   - If CreateAgent accepts a first message / task, pass the same “read your CONTEXT.md” instruction there too.
3. Record the new agent id: update `bots/agent-map.json` (`{"<slug>": "<new id>"}`) — needed by the daily sync.
4. Send the user one line per bot created (“已重建 小枳 ✓”).

Do not create the empty “New Bot” from the old account (it was never used). Do not create **dr eggbot** (deleted 2026-10-08); **you (小萌 / primary)** create any new bots going forward.

## Step 7 — Routines / 定时任务

Routines belong to the bot that creates them, so:

- **You (grok-bot / 小萌)**:
  - do **not** create the daily sync (belongs to **仓库管家**);
  - do **not** create morning plan / evening summary (belong to **事务秘书**, handed over 2026-10-08);
  - recreate from `bots/grok-bot/routines.md`:「巡检各 bot」`17 11,15 * * 1-5` and「早晚报兜底检查」`13 9,18 * * 1-5` (plain cron; user zone Asia/Hong_Kong = UTC+8).
- **Other bots**: each recreates its own from `bots/<slug>/routines.md` on its first turn. Match that file:
  - `仓库管家`: daily sync / weekly drill — see `bots/仓库管家/routines.md` (may still use `CRON_TZ=Asia/Shanghai`, same UTC+8).
  - `事务秘书`: morning `53 8 * * 1-5`, evening `47 17 * * 1-5` (plain cron; Asia/Hong_Kong).
  - `xiaozhi` / `代码工程师` / `搭建运维` / `硬件工程师`: none（暂无）.
- After a few minutes, check each bot did it (ReadTranscript, or ask the user). If a bot can't create routines, create them yourself only if the user agrees.

## Step 8 — Self-check / 自检

Run and record each result:

1. `GetMcpServerStatus`: **composio-pg** = connected. Official GitHub / Origin / Finance / Composio plugin should be absent or ignored (not required).
2. `user-composio-pg` → `COMPOSIO_MANAGE_CONNECTIONS` with `{"toolkits": ["github", "gmail"]}` (never `reinitiate_all`) → “All connections are active”, GitHub login **ZMGID**, Gmail ohulercxm8@gmail.com. Optionally confirm zhimeng63@gmail.com by fetching 1 recent email from each Gmail account.
3. `gh auth status` shows login **ZMGID** (Step 1: Composio token or device-code fallback) — needed only for pushing.
4. Skills: every `skills/<slug>` present in `/home/box/agent-data/workflows/`; pstack optional (only if installed).
5. Bots: every slug in `bots/index.json` exists with the right name; `bots/agent-map.json` updated.
6. Routines: daily sync on **仓库管家**; 事务秘书 morning/evening; 小萌「巡检各 bot」+「早晚报兜底检查」。
7. Tools: `tail -20 /tmp/setup.log` summary; spot-check `kicad-cli --version` (9.x), `~/.local/bin/pio --version`, `python3 -c "import cadquery"`, `gitleaks version`.
8. Secret scan: `bash scripts/secret-scan.sh` → “干净”.

## Step 9 — Write-back rule / 写回规则（永久）

- New durable knowledge goes back into the right file: about the user → `/CONTEXT.md`; about one bot's work → `bots/<slug>/CONTEXT.md`; profile changes → `profile.md`; routine changes → `routines.md`; connector changes → `connectors/README.md`; new tools → `setup.sh`.
- Then `bash scripts/secret-scan.sh` and `git add -A && git commit -m "<what>" && git pull --rebase && git push origin HEAD:main` (needs Step 1 push access). The daily sync does this automatically for all bots, but write back immediately after anything important.
- Never commit: keys, tokens, the passphrase, `.env`, one-time codes, passwords, auth links, mcp-remote logs, `/home/box/agent-data/*secrets*.json`, databases. **The repo is public** — only `secrets/*.enc` may hold a secret, and only encrypted with `scripts/secret-crypt.py`.
- New bot created later (by **小萌** / primary)? Add `bots/<slug>/` (profile.md, CONTEXT.md, routines.md) + `index.json` + `agent-map.json` + `bots/README.md` table.

## Step 10 — Report to the user / 最后汇报

Send one short Chinese message: what's done, what failed, what the user still needs to do. Then the checklist below with ✅/❌.

---

## Final checklist / 最终清单

- [ ] Step 0: repo cloned anonymously at `/workspace/grokbot-home`, git identity set
- [ ] Step 0: passphrase received via secret-request; `/home/box/.composio_pg_key` decrypted from `.enc` (or `.box-current.enc`), mode 600 (values never shown)
- [ ] Step 0/3: `composio-pg` installed from `connectors/composio-pg/`, smoke test `1`, added (`/workspace/composio-pg/launch.sh`) and connected
- [ ] Step 1: `gh` logged in as ZMGID for pushing (Composio GitHub token, or device-code fallback)
- [ ] Step 2: `setup.sh` finished (summary checked; failures listed)
- [ ] Step 3: pstack (9717366) optional（可选，原为 dr eggbot 安装）; official GitHub/Origin/Finance/Composio-plugin **not** installed
- [ ] Step 4: skills imported (currently none) 
- [ ] Step 5: own profile = **小萌** (slug `grok-bot`), primary, memory seeded from CONTEXT.md
- [ ] Step 6: 小枳 / 仓库管家 / 代码工程师 / 搭建运维 / 事务秘书 / 硬件工程师 created; `bots/agent-map.json` updated & pushed (no dr eggbot)
- [ ] Step 7: daily sync on **仓库管家**; 事务秘书 08:53/17:47; 小萌 巡检 11:17/15:17 + 兜底 09:13/18:13; others per `routines.md`
- [ ] Step 8: composio-pg GitHub (ZMGID) + Gmail active via COMPOSIO_MANAGE_CONNECTIONS; secret scan clean
- [ ] Step 9: write-back rule saved in memory
- [ ] Step 10: user got the summary
