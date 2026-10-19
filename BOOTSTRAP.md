# BOOTSTRAP — self-setup for a fresh Grok Bot

> **You are a Grok Bot on a brand-new account.** The user (GitHub `ZMGID`) rotates between several Grok Bot accounts and just gave you this repo's link (public repo: `https://github.com/ZMGID/grokbot-home`).
> Follow this file top to bottom to (1) configure yourself, (2) recreate every other bot, (3) verify, and (4) keep the repo up to date.
>
> 中文说明：你是新号上的 Grok Bot。用户把这个仓库链接发给你，意思是“按这里把你自己和其他 bot 都配好”。照下面的步骤一步步做。

**Ground rules / 规则**

- Talk to the user in **Chinese**, short and direct. Times in **Asia/Shanghai (UTC+8)**. 用中文、简短、北京时间。
- **Never put a secret in the repo, in chat, or in a log.** Secrets come only from a masked secret prompt (or 1Password). Never `cat` a key file. 密钥绝不进仓库/聊天/日志。
- Things that need the user: the repo passphrase `GROKBOT_HOME_PASSPHRASE` once (masked secret-request). Only if something fails: the Composio API key itself (masked), (pushes go through Composio GitHub, no `gh` login — Step 1). No official connector auth clicks. Batch these. 需要用户做的只有在密码框里填一次仓库口令；Composio key 和设备码仅作备用。尽量一次问完。
- Do the steps in order; if a step fails, note it, continue with the rest, and report it in the final checklist. 某步失败就记下来继续，最后汇报。
- The box (`/workspace`, `/home/box`) is shared by all bots on this account, so files you set up are visible to the bots you create.
- Send the user a one-line progress update after each major step (connectors, bots, self-check), not a wall of text.

---

## Step 0 — Clone, passphrase, Composio key, composio-pg + composio-zhimeng / 克隆 → 口令 → 解密 key → 装两个 Composio MCP

This repo is **public**: clone it anonymously, no GitHub login needed. The Composio API key is in the repo **only encrypted** (`secrets/*.enc`); the user gives you the passphrase through a masked secret-request. Official GitHub / Origin connectors are **not** used (all apps via Composio stdio MCPs: `composio-pg` + `composio-zhimeng`). Never print the key, the passphrase, or any token. Never `cat` key files.
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

### (b+) Restore finance ledgers from encrypted backup / 解密恢复账本

After `GROKBOT_HOME_PASSPHRASE` is set, restore `/workspace/finance/` if missing or empty (plaintext ledgers stay on the box only; never `git add` them):

```bash
cd /workspace/grokbot-home
if [[ ! -d /workspace/finance ]] || [[ -z "$(ls -A /workspace/finance 2>/dev/null)" ]]; then
  umask 077
  TMP=$(mktemp /tmp/finance.XXXXXX.tgz)
  python3 scripts/secret-crypt.py dec-bin secrets/finance.tgz.enc "$TMP"
  tar -C /workspace -xzf "$TMP"
  shred -u "$TMP" 2>/dev/null || rm -f "$TMP"
  echo "finance restored to /workspace/finance/"
else
  echo "finance already present; skip restore (do not overwrite live books without asking)"
fi
```

若还有 `secrets/财务管家-memory.tgz.enc`，可同样用 `dec-bin` 解到临时目录后按需合并进该 bot 的 `memory/`（勿提交明文）。细节见 `secrets/README.md`。

### (b++) Restore ALL encrypted box bundles / 一次性恢复全部加密包（2026-10-12 起）

`scripts/pack-bundles.sh`（每次 sync 自动跑）把恢复所需的密钥/私密文件打成 GBH1 加密包。`box-secrets` 包内路径**相对于 `/`**（如 `home/box/.composio_pg_key`）；`daily`/`feishu-cli`/`finance` 包内路径**相对于 `/workspace`**：

| 包 | 内容 |
|---|---|
| `secrets/box-secrets.tgz.enc` | `~/.composio_pg_key`；`~/.lark-cli/config.json` + `~/.local/share/lark-cli/`（飞书 app `cli_aa430b6809f85d0c` 的 app secret + 用户 token + master.key）；`~/.config/gh/`（gh 登录）；`~/.gitconfig`；`~/.ssh/config`、`known_hosts`；`~/servers/`（eastforce 服务器资料 + ssh 私钥）；`/workspace/gmail-listener/webhook_url.local`；`~/.grokbot-home/secrets.env`（`COMPOSIO_API_KEY`、`GMAIL_WEBHOOK_KEY` 的值，**不含**口令） |
| `secrets/daily.tgz.enc` | `/workspace/assistant/daily/` |
| `secrets/feishu-cli.tgz.enc` | `/workspace/feishu-cli/`（README、chats、approvals、survey、日志） |
| `secrets/finance.tgz.enc` | `/workspace/finance/`（同 (b+)） |

口令就绪后（never print values）：

```bash
cd /workspace/grokbot-home
umask 077
T=$(mktemp -d /tmp/gbh-restore.XXXXXX)
for b in box-secrets daily feishu-cli finance; do
  [ -f secrets/$b.tgz.enc ] || continue
  python3 scripts/secret-crypt.py dec-bin secrets/$b.tgz.enc "$T/$b.tgz" || { echo "!! $b 解密失败"; continue; }
  tar -tzf "$T/$b.tgz" > "$T/$b.list"              # 想先看清单可以 less 这个文件（只有路径）
  if [ $b = box-secrets ]; then DEST=/; else DEST=/workspace; fi
  tar -C $DEST -xzpf "$T/$b.tgz" --no-overwrite-dir   # 同名文件会被覆盖；finance 若已有活账本，先备份再解
  echo "restored $b ($(wc -l < "$T/$b.list") entries)"
done
find "$T" -type f -exec shred -u {} +; rm -rf "$T"
# 权限
chmod 600 ~/.composio_pg_key ~/.grokbot-home/secrets.env ~/.config/gh/hosts.yml ~/.lark-cli/config.json 2>/dev/null
chmod 700 ~/.ssh ~/.lark-cli ~/.local/share/lark-cli ~/servers ~/servers/* ~/.grokbot-home 2>/dev/null
find ~/.local/share/lark-cli ~/servers ~/.ssh -type f -exec chmod 600 {} + 2>/dev/null
chmod 600 /workspace/gmail-listener/webhook_url.local 2>/dev/null
```

恢复后检查（只看状态，不打印 token）：

```bash
export PATH="$HOME/.local/bin:$PATH"
gh auth status 2>&1 | grep -E 'Logged in|Token scopes|X '      # 可选：推送不靠 gh（Step 1），过期/被撤销就不用管，不要让用户重新 gh auth login
lark-cli auth status 2>&1 | sed -E 's/[A-Za-z0-9_-]{24,}/<redacted>/g'   # 用户 token 约 7 天不用就过期 → lark-cli auth login（扫码）
ssh -o BatchMode=yes -o ConnectTimeout=8 eastforce true && echo "eastforce ssh ok"
```

`~/.grokbot-home/secrets.env` 里是 `export COMPOSIO_API_KEY=…` / `export GMAIL_WEBHOOK_KEY=…`。新号上优先让用户用 masked secret-request 重新提供这两个 env（平台 secret 最可靠）；临时启动 listener 可以 `set -a; . ~/.grokbot-home/secrets.env; set +a` 后再跑 `start.sh`。**注意：webhook URL/KEY 属于旧号的 gmail-new-mail 例程；新号重建例程后 URL 和 key 都会变，要把新值写回 `webhook_url.local` / env，再跑一次 sync 让加密包更新。**

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

### (d) Install composio-zhimeng (zhimeng63 Gmail) + AddMcpServer

Reuses the same `~/.composio_pg_key` and `/workspace/composio-pg/.venv` (no second key file).

```bash
mkdir -p /workspace/composio-zhimeng
install -m 700 /workspace/grokbot-home/connectors/composio-zhimeng/launch.sh /workspace/composio-zhimeng/
install -m 600 /workspace/grokbot-home/connectors/composio-zhimeng/launch.py /workspace/composio-zhimeng/
timeout 40 /workspace/composio-zhimeng/launch.sh </dev/null >/dev/null 2>/tmp/czm.err
grep -c "Proxy established successfully" /tmp/czm.err
rm -f /tmp/czm.err
```

`1` = OK. Then `AddMcpServer` name **`composio-zhimeng`**, command **`/workspace/composio-zhimeng/launch.sh`** (no args, no env) — **after** composio-pg. Verify Gmail read via `user-composio-zhimeng`. If the zhimeng63 Gmail connection is missing on a new account, re-auth with `COMPOSIO_MANAGE_CONNECTIONS` for Composio user **`zhimeng63`** (toolkit gmail), not the pg-test user.

### (e) Gmail listener + webhook key + Feishu lark-cli

**Gmail webhook（小萌例程 gmail-new-mail）**
1. Recreate 小萌's webhook routine **gmail-new-mail** (folder `gmail-new-mail`; prompt in `bots/grok-bot/routines.md`).
2. Ask the user (masked secret-request) for **`GMAIL_WEBHOOK_KEY`** — put it only in the process environment, never in the repo or chat. Env var **name** may be documented; **value** must not.
3. Write the new webhook URL into `/workspace/gmail-listener/webhook_url.local` (`chmod 600`) **or** set env `GMAIL_WEBHOOK_URL`. Never commit `webhook_url.local` in plaintext (旧号的 URL 已随 `box-secrets.tgz.enc` 恢复；新号例程 URL 会变，要覆盖它)。
4. Recreate Composio triggers `GMAIL_NEW_GMAIL_MESSAGE` per user if needed: ohulercxm8 on **composio-pg**, zhimeng63 on **composio-zhimeng** (never put zhimeng63 under pg-test).
5. Restore scripts from `services/gmail-listener/` (`listener.py`, `run_loop.sh`, `start.sh`, `stop.sh`) into `/workspace/gmail-listener/`, build venv if needed, then run `/workspace/gmail-listener/start.sh`.
6. After **every box restart**, run `start.sh` again (no systemd on the box).

**Feishu（lark-cli；Composio 无飞书）**
1. `setup.sh` installs `@larksuite/cli` to `~/.local` (`export PATH="$HOME/.local/bin:$PATH"`).
2. After account switch: `lark-cli config init --new --brand feishu` then `lark-cli auth login` — **user scans QR**.
3. **先试恢复的凭据**：(b++) 已把 `~/.lark-cli/config.json`、`~/.local/share/lark-cli/`（app secret + 用户 token）和 `/workspace/feishu-cli/` 解回来。跑 `lark-cli auth status`：有效就不用重新配置；app secret 有效但用户 token 过期 → 只需 `lark-cli auth login`（扫码一次）；都不行才走第 2 步全量重配。
4. 明文 `~/.lark-cli/`、`~/.local/share/lark-cli/`、`/workspace/feishu-cli/{survey,chats,approvals}/` 永不进仓库（只以加密包存在）。Group ids: `services/feishu-cli/chats.md`.

## Step 1 — Push access (only for write-back / daily sync) / 推送权限（只有写回和每日同步需要）

Setup itself needs **no** GitHub login. Pushing (Step 6 `agent-map.json`, Step 9 write-back, 仓库管家's daily sync) is needed only for writes.

**Decision 2026-10-11: do not use `gh` / `git push`.** All GitHub writes to `ZMGID/grokbot-home` go through the Composio GitHub toolkit on `user-composio-pg` (ZMGID): find tools with `COMPOSIO_SEARCH_TOOLS` (single file: create/update file contents; multi-file: create blobs → tree → commit → update ref `heads/main`). Reason: this Composio project masks the GitHub access token (the API returns an 8-char placeholder), so `gh auth login --with-token` gets HTTP 401, and the device-code flow is not used. Before writing, check remote `main` has not moved past local HEAD in the touched files; afterwards `git fetch` anonymously and `git reset --hard origin/main` only after `git diff origin/main` shows the remote has exactly your changes.

（2026-10-11 起不再用 gh：推送一律走 composio-pg 的 Composio GitHub（ZMGID）。原因：本 Composio 项目会把 GitHub access token 打码，gh 登录用不了。不装官方 GitHub 连接器。）

## Step 2 — Tool environment / 工具环境

```bash
cd /workspace/grokbot-home
nohup bash setup.sh > /tmp/setup.log 2>&1 &
```

- Idempotent; heavy installs (KiCad 9, LibreOffice, PrusaSlicer, cadquery, PlatformIO ESP32 toolchain) can take 10–20 min — run in background, keep going with Step 3, check `/tmp/setup.log` later (the summary at the end lists anything that failed).
- `bash setup.sh --light` skips the heavy CAD/EDA packages if the user only needs the basics.
- It also refreshes `composio-pg` and `composio-zhimeng` launchers from the repo (same as Step 0 (c)(d)); rebuilds composio-pg venv if needed. zhimeng launcher reuses that venv and `~/.composio_pg_key`.

## Step 3 — Connectors / 连接器

Follow `connectors/README.md`. **Rule: app connections through Composio stdio MCPs (`composio-pg` + `composio-zhimeng`), plus Feishu via official lark-cli (exception).** Do **not** install official GitHub (`cursor-github`), Origin, Finance (63408931), or the Composio OAuth plugin (32661537).

| Item | Action | User does |
|---|---|---|
| **composio-pg** | Step 0 (b)(c); AddMcpServer `/workspace/composio-pg/launch.sh` | type the repo passphrase once (masked) |
| **composio-zhimeng** | Step 0 (d) after composio-pg; AddMcpServer `/workspace/composio-zhimeng/launch.sh` | nothing if zhimeng63 Gmail already ACTIVE; else re-auth for user `zhimeng63` |
| **gmail-listener + webhook** | Step 0 (e): recreate triggers; secret-prompt `GMAIL_WEBHOOK_KEY`; `start.sh` | provide webhook key (masked); after box restart expect agent to start listener |
| **飞书 lark-cli** | Step 0 (e): install via setup.sh; `config init` + `auth login` | scan QR twice |
| pstack plugin, **plugin id 9717366** | optional `InstallPlugin` | nothing |
| Official GitHub / Origin / Finance / Composio plugin 32661537 | **skip** | nothing |

Confirm `GetMcpServerStatus`: both `composio-pg` and `composio-zhimeng` connected.
- `user-composio-pg` → `COMPOSIO_MANAGE_CONNECTIONS` `{"toolkits":["github","gmail"]}` (never `reinitiate_all`) → GitHub ZMGID + Gmail ohulercxm8@gmail.com.
- `user-composio-zhimeng` → `COMPOSIO_MANAGE_CONNECTIONS` `{"toolkits":["gmail"]}` → Gmail zhimeng63@gmail.com; fetch 1 recent mail to verify.
If zhimeng63 Gmail is missing: re-auth via `COMPOSIO_MANAGE_CONNECTIONS` for Composio user **`zhimeng63`**.

## Step 4 — Skills / 技能

- `skills/` currently has **one user skill**: `skills/tiktok/`（TikTok巴西站竞品调研，商品调研 用；needs env `GECKOAPI_KEY`, value never in the repo — see `skills/README.md`). For every `skills/<slug>/` (now and later): copy the whole folder (incl. `scripts/`) to `/home/box/agent-data/workflows/<slug>/` (or create it with the `skill-authoring` skill using the same name and body), then confirm it is listed.
- **pstack** plugin (`InstallPlugin 9717366`) is **optional**（可选，原为 dr eggbot 安装）. Install only if a coding bot needs those skills.
- Managed skills (add-connector, routines, …) come with the platform — nothing to do.

## Step 5 — Apply your own profile (primary bot) / 设置你自己

Primary = `bots/index.json` → `"primary": "grok-bot"`. Read `bots/grok-bot/profile.md`, `bots/grok-bot/CONTEXT.md`.

1. `update_state` target `profile`, action `set`: **name** `小萌` (formerly `Grok Bot`, renamed 2026-10-08; slug stays `grok-bot`), **description** = the exact English text in `bots/grok-bot/profile.md`, title empty.
2. Avatar: no custom image (default shape `blob`, color `black`). If a `bots/grok-bot/avatar.*` file ever exists, set it with `update_state` target `avatar`.
3. If you are not the primary bot, ask the user once whether to make you primary, then `SetPrimaryBot`.
4. Save the important facts from `/CONTEXT.md` + `bots/grok-bot/CONTEXT.md` into your memory (`update_state` target `memory`): user writes Chinese, rotates accounts, GitHub ZMGID, repo `ZMGID/grokbot-home` (public) is the source of truth, no plaintext secrets in the repo (only `secrets/*.enc`), Composio via `composio-pg` + `composio-zhimeng`.
5. If the bot the user opened is **not** the primary (`小萌` / slug `grok-bot`), still act as the bootstrapper: apply `grok-bot`'s profile only if the user agrees; otherwise create `grok-bot` in Step 6 like the others.

## Step 6 — Recreate every other bot / 用 CreateAgent 重建其他 bot

For **each** folder in `bots/` except the primary — driven by `bots/index.json`. Current set (2026-10-19): `xiaozhi`（小枳）, `仓库管家`, `代码工程师`, `搭建运维`, `事务秘书`, `硬件工程师`, `财务管家`, `商品调研`, `测试工程师`, `结构工程师`, `电子工程师`. **Do not** recreate deleted `dr-eggbot`.

1. Read `bots/<slug>/profile.md`.
2. Call **CreateAgent** with:
   - **name**: exactly as in profile.md (`小枳`, `仓库管家`, `代码工程师`, `搭建运维`, `事务秘书`, `硬件工程师`, `财务管家`, `商品调研`, `测试工程师`, `结构工程师`, `电子工程师`)
   - **title**: as in profile.md (currently empty)
   - **description / instructions**: the text block in profile.md (keep verbatim; xiaozhi's is reconstructed), **plus** this line appended:
     `On your first turn, read /workspace/grokbot-home/CONTEXT.md and /workspace/grokbot-home/bots/<slug>/CONTEXT.md, save the key facts to your memory, then recreate your routines from bots/<slug>/routines.md.`
     （中文可写成：“第一次启动先读 /workspace/grokbot-home/CONTEXT.md 和 bots/<slug>/CONTEXT.md，把要点存进自己的记忆，再按 bots/<slug>/routines.md 重建定时任务。”）
   - avatar: default shape/color from profile.md if CreateAgent accepts it; set an image only if `bots/<slug>/avatar.*` exists.
   - If CreateAgent accepts a first message / task, pass the same “read your CONTEXT.md” instruction there too.
3. Record the new agent id in `bots/agent-map.json` **format 2**: set `bots.<slug>.ids.<this-account-小萌-id> = "<new id>"` (do **not** flatten to a single string — another Grok Bot account may share this repo). Account keys are each account's 小萌 agent id; see top-level `accounts`. Needed by the daily sync.
4. Send the user one line per bot created (“已重建 小枳 ✓”).
5. Group chats (2026-10-15 起): after all bots exist, recreate the project groups listed in `bots/README.md`「群聊」 (「AI编程键盘」「AI脚踏板」, members = 小萌 + 硬件工程师 + 代码工程师 + 商品调研 + 测试工程师；「AI陪伴机器人」(2026-10-19), members = 小萌 + 结构工程师 + 电子工程师 + 代码工程师 + 商品调研 + 测试工程师) only if the user still wants them; group ids are per-account, record nothing secret.

Do not create the empty “New Bot” from the old account (it was never used). Do not create **dr eggbot** (deleted 2026-10-08); **you (小萌 / primary)** create any new bots going forward.

## Step 7 — Routines / 定时任务

Routines belong to the bot that creates them, so:

- **You (grok-bot / 小萌)**:
  - do **not** create the daily sync (belongs to **仓库管家**);
  - do **not** create morning plan / evening summary (belong to **事务秘书**, handed over 2026-10-08);
  - recreate from `bots/grok-bot/routines.md`:「巡检各 bot」`17 11,15 * * 1-5`; email「cloudpotato 来信提醒」; webhook「gmail-new-mail」(needs listener + `GMAIL_WEBHOOK_KEY`).
- **Other bots**: each recreates its own from `bots/<slug>/routines.md` on its first turn. Match that file:
  - `仓库管家`: daily sync / weekly drill — see `bots/仓库管家/routines.md` (may still use `CRON_TZ=Asia/Shanghai`, same UTC+8).
  - `事务秘书`: morning `53 8 * * 1-5`, evening `47 17 * * 1-5` (plain cron; Asia/Hong_Kong).
  - `xiaozhi` / `代码工程师` / `搭建运维` / `硬件工程师` / `财务管家` / `商品调研` / `测试工程师` / `结构工程师` / `电子工程师`: none（暂无；只有过一次性/临时任务，不用重建）.
- After a few minutes, check each bot did it (ReadTranscript, or ask the user). If a bot can't create routines, create them yourself only if the user agrees.

## Step 8 — Self-check / 自检

Run and record each result:

1. `GetMcpServerStatus`: **composio-pg** and **composio-zhimeng** = connected. Official GitHub / Origin / Finance / Composio plugin should be absent or ignored.
2. `user-composio-pg` → `COMPOSIO_MANAGE_CONNECTIONS` `{"toolkits": ["github", "gmail"]}` (never `reinitiate_all`) → GitHub **ZMGID**, Gmail ohulercxm8@gmail.com.
3. `user-composio-zhimeng` → `COMPOSIO_MANAGE_CONNECTIONS` `{"toolkits": ["gmail"]}` → zhimeng63@gmail.com; fetch 1 recent email to verify.
4. Push access: Composio GitHub on `user-composio-pg` is ZMGID (item 2) — `gh` is not used (Step 1, 2026-10-11).
5. Skills: every `skills/<slug>` present in `/home/box/agent-data/workflows/`; pstack optional (only if installed).
6. Bots: every slug in `bots/index.json` exists with the right name; `bots/agent-map.json` updated.
7. Routines: daily sync + weekly drill on **仓库管家**; 事务秘书 morning/evening; 小萌「巡检各 bot」+「cloudpotato 来信提醒」+「gmail-new-mail」（no daily sync / morning / evening on 小萌）。
8. Tools: `tail -20 /tmp/setup.log` summary; spot-check `kicad-cli --version` (9.x), `~/.local/bin/pio --version`, `python3 -c "import cadquery"`, `gitleaks version`.
9. Secret scan: `bash scripts/secret-scan.sh` → “干净”.

## Step 9 — Write-back rule / 写回规则（永久）

- New durable knowledge goes back into the right file: about the user → `/CONTEXT.md`; about one bot's work → `bots/<slug>/CONTEXT.md`; profile changes → `profile.md`; routine changes → `routines.md`; connector changes → `connectors/README.md`; new tools → `setup.sh`.
- Then `bash scripts/secret-scan.sh`, and commit the changed files to `main` through Composio GitHub on `user-composio-pg` (Step 1; no `gh` / `git push` since 2026-10-11), then sync the local copy (`git fetch` + verify `git diff origin/main` + `git reset --hard origin/main`). The daily sync does this automatically for all bots, but write back immediately after anything important.
- Never commit: keys, tokens, the passphrase, `.env`, one-time codes, passwords, auth links, mcp-remote logs, `/home/box/agent-data/*secrets*.json`, databases. **The repo is public** — only `secrets/*.enc` may hold a secret, and only encrypted with `scripts/secret-crypt.py`.
- New bot created later (by **小萌** / primary)? Add `bots/<slug>/` (profile.md, CONTEXT.md, routines.md) + `index.json` + `agent-map.json` (format 2: merge into `bots.<slug>.ids.<本号小萌id>`) + `bots/README.md` table.
- **Finance restore / 账本**：明文 `/workspace/finance/` **永不**进 git（`.gitignore` 已忽略）。迁移备份是加密包 `secrets/finance.tgz.enc`。口令就绪后（Step 0 (b)），按 Step 0 (b+) 与 `secrets/README.md` 解密恢复到 `/workspace/finance/`。每日同步会重新打包并 `enc-bin` 覆盖该文件。`/workspace/assistant/daily/` 明文仍绝不进仓库，只以 `secrets/daily.tgz.enc` 加密备份（2026-10-12 起）；其他 box 密钥见 Step 0 (b++)。`财务管家` 的 plaintext `memory/` 不拷进 `raw/`；有内容时 sync 另加密为 `secrets/财务管家-memory.tgz.enc`。

## Step 10 — Report to the user / 最后汇报

Send one short Chinese message: what's done, what failed, what the user still needs to do. Then the checklist below with ✅/❌.

---

## Final checklist / 最终清单

- [ ] Step 0: repo cloned anonymously at `/workspace/grokbot-home`, git identity set
- [ ] Step 0: passphrase received via secret-request; `/home/box/.composio_pg_key` decrypted from `.enc` (or `.box-current.enc`), mode 600 (values never shown); `/workspace/finance/` restored from `secrets/finance.tgz.enc` if needed
- [ ] Step 0 (b++): `box-secrets` / `daily` / `feishu-cli` 加密包已解到原路径并 chmod；`lark-cli auth status`、`ssh eastforce` 已检查（`gh auth status` 可选，推送不靠 gh）
- [ ] Step 0/3: `composio-pg` + `composio-zhimeng` installed & connected; gmail-listener started; lark-cli auth’d (user QR); `GMAIL_WEBHOOK_KEY` in env only
- [ ] Step 1: push access via Composio GitHub (composio-pg, ZMGID); no `gh`
- [ ] Step 2: `setup.sh` finished (summary checked; failures listed)
- [ ] Step 3: pstack (9717366) optional（可选，原为 dr eggbot 安装）; official GitHub/Origin/Finance/Composio-plugin **not** installed
- [ ] Step 4: skills imported (currently `tiktok`)
- [ ] Step 5: own profile = **小萌** (slug `grok-bot`), primary, memory seeded from CONTEXT.md
- [ ] Step 6: 小枳 / 仓库管家 / 代码工程师 / 搭建运维 / 事务秘书 / 硬件工程师 / 财务管家 / 商品调研 / 测试工程师 / 结构工程师 / 电子工程师 created; `bots/agent-map.json` updated & pushed (no dr eggbot)
- [ ] Step 7: daily sync + weekly drill on **仓库管家**; 事务秘书 08:53/17:47; 小萌 巡检 11:17/15:17 + cloudpotato 邮件 + gmail-new-mail webhook; others per `routines.md`
- [ ] Step 8: composio-pg GitHub+ohulercxm8 + composio-zhimeng zhimeng63 Gmail active; secret scan clean
- [ ] Step 9: write-back rule saved in memory
- [ ] Step 10: user got the summary
