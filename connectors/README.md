# 连接器清单（connectors manifest）

> 导出时间：2026-10-09（北京时间）更新（新增 composio-zhimeng）。
> 连接器装在 **账号** 上，不是装在某个 bot 上：新号上第一个 bot 装好以后，后面用 CreateAgent 建的 bot 都能直接用。
> 本文件只记名字、ID、地址和步骤，**不含任何密钥**。
>
> **规矩**：所有应用连接只走 Composio 自定义 stdio MCP。**不要**再装官方 GitHub / Origin / Finance / Composio 插件。
> - **`composio-pg`**：用户 `pg-test-…` → GitHub ZMGID（`ca_1g4u93YydZsp`）+ Gmail ohulercxm8（`ca_ZnzYtlTeic0s`）——**一个连接器一个 Gmail**
> - **`composio-zhimeng`**：用户 `zhimeng63` → Gmail zhimeng63（`ca_5jGHEthCoWuD`）only（共用 `/home/box/.composio_pg_key`）
> - 旧 composio-pg 上的 zhimeng63 连接 **`ca_2rJjmKh8j1q0` 已删除**（2026-10-09，用户同意）；新号勿在 pg-test 下重建 zhimeng63

| # | 连接器 | 类型 | 怎么装 | 需要用户做什么 | 必需？ |
|---|---|---|---|---|---|
| 1 | **composio-pg**（`user-composio-pg`） | 自定义 **stdio** MCP（跑在 box 上） | 见下文「composio-pg」；BOOTSTRAP Step 0 从本目录安装启动器 | 在密码框里填一次仓库口令 `GROKBOT_HOME_PASSPHRASE`（用来解密 `secrets/*.enc` 里的 Composio key） | ✅ 必需 |
| 2 | **composio-zhimeng**（`user-composio-zhimeng`） | 自定义 **stdio** MCP（跑在 box 上） | 见下文「composio-zhimeng」；与 composio-pg 共用 key 与 venv | 无（口令已在装 composio-pg 时填过）；若 zhimeng63 Gmail 未授权则在 Composio 里给用户 `zhimeng63` 授权 | ✅ 必需 |
| 3 | **GitHub**（`cursor-github`） | 官方连接器 | — | — | ❌ 不需要（GitHub 走 composio-pg） |
| 4 | **Origin**（`cursor-origin`） | 官方连接器 | — | — | ❌ 不需要 |
| 5 | **Composio 插件**（`user-Composio`，plugin id `32661537`） | 插件市场 OAuth 版 | — | — | ❌ 不需要（它看到的是另一个 Composio user） |
| 6 | **Finance**（`user-Finance-xai`，plugin id `63408931`） | 插件市场 | — | — | ❌ 不需要 |

另外两样不是「应用连接器」但要记得：

- **pstack 插件**（plugin id **`9717366`**，cursor-public）：写代码类 bot 用的工作流技能包（architect、tdd、swarm、arena……）。**可选**（原为 dr eggbot 安装；该 bot 已于 2026-10-08 删除）。这是技能插件，不是应用连接；需要时再 `InstallPlugin 9717366`。
- **`x` 工具命名空间**（X/Twitter 搜索、新闻）：平台自带，不需要安装；新号若没有就忽略。
- **`gh` 命令行**：不是连接器。仓库公开，克隆不需要登录；只有推送（写回、每日同步）才需要。新号上用 Composio 里 GitHub（ZMGID）的 access token 做 `gh auth login --with-token`（见 BOOTSTRAP Step 1）；失败再退回设备码登录。

## composio-pg（自定义 stdio MCP）——GitHub + ohulercxm8 Gmail

**它是什么**：box 上的一个小启动器。读取 `~/.composio_pg_key`（Composio 项目 API key），用 Composio SDK 给用户
`pg-test-5be86c3e-d220-4538-ab6d-ae22d538dfde` 创建一个会话，再用 `npx mcp-remote` 把会话的 MCP 地址桥接成 stdio。

**这个 Composio 用户下现有的连接**（2026-10-09 核对；**勿**再挂 zhimeng63）：

| 应用 | 账号 | connected account |
|---|---|---|
| GitHub | ZMGID（ZhiMeng） | `ca_1g4u93YydZsp` |
| Gmail | ohulercxm8@gmail.com | `ca_ZnzYtlTeic0s` |

~~旧~~：曾有 Gmail zhimeng63@gmail.com / `ca_2rJjmKh8j1q0`，已于 2026-10-09 经用户同意从 composio-pg 删除。新号重建时**不要**在 pg-test 用户下再授权 zhimeng63——只走 composio-zhimeng。

Composio 项目 ID：`pr_lh5-8poHU4QB`（只有这一个项目）。

**文件**：`connectors/composio-pg/launch.py`、`launch.sh`（不含密钥）。BOOTSTRAP Step 0 (c) 把它们装到 `/workspace/composio-pg/`；`launch.sh` 依赖 `/workspace/composio-pg/.venv`（装有 `composio==0.25.0`），以及 node/npx（`npx -y mcp-remote`）。

**安装步骤**：

1. 用 **secret-request（密码框，掩码输入）** 向用户要仓库口令 `GROKBOT_HOME_PASSPHRASE`，然后解密 key：
   `python3 scripts/secret-crypt.py dec secrets/COMPOSIO_API_KEY.enc /home/box/.composio_pg_key && chmod 600 /home/box/.composio_pg_key`
   （冒烟测试不通过就改用 `secrets/COMPOSIO_API_KEY.box-current.enc`）。**绝不能**让用户把口令或 key 贴进聊天，也不要 `cat` 出来。
   - 解密失败时的备选：用密码框直接要 Composio 项目 API key（Composio 控制台 → 项目设置 → API Keys），或请用户在 bot 桌面终端执行
     `read -rsp 'Composio key: ' K && umask 077 && printf %s "$K" > ~/.composio_pg_key && unset K`
2. 装启动器（也可以直接跑 `setup.sh`，它做同样的事）：
   ```bash
   mkdir -p /workspace/composio-pg && cd /workspace/composio-pg
   install -m 700 /workspace/grokbot-home/connectors/composio-pg/launch.sh .
   install -m 600 /workspace/grokbot-home/connectors/composio-pg/launch.py .
   [ -x .venv/bin/python ] || uv venv -q .venv
   uv pip install -q --python .venv/bin/python "composio==0.25.0" || uv pip install -q --python .venv/bin/python composio
   npx -y mcp-remote --help >/dev/null 2>&1 || true
   ```
3. 冒烟测试（**不要**打印 stderr：mcp-remote 会在日志里明文打印 `x-api-key`）：
   `timeout 40 /workspace/composio-pg/launch.sh </dev/null >/dev/null 2>/tmp/cpg.err; grep -c "Proxy established successfully" /tmp/cpg.err; rm -f /tmp/cpg.err`
   ——输出 `1` 即成功。
4. `AddMcpServer`：name **`composio-pg`**，command **`/workspace/composio-pg/launch.sh`**，无 args、无 env。
5. 自检：`user-composio-pg` → `COMPOSIO_MANAGE_CONNECTIONS`，参数 `{"toolkits":["github","gmail"]}`（**不要** `reinitiate_all`），
   应返回 `All connections are active`，GitHub login 为 ZMGID，Gmail 为 ohulercxm8@gmail.com。

**新应用（给 pg-test 用户）**：只在 Composio 控制台给测试用户 `pg-test-5be86c3e-d220-4538-ab6d-ae22d538dfde` 授权新 toolkit，然后通过 composio-pg 使用。**不要**再装官方连接器。

**换号/轮换 key**：重写 `~/.composio_pg_key` 并 `RestartMcpServers`（两个 MCP 都会用到同一 key）；然后重新加密写回仓库（`python3 scripts/secret-crypt.py enc /home/box/.composio_pg_key secrets/COMPOSIO_API_KEY.enc`，见 `secrets/README.md`），跑 `scripts/secret-scan.sh` 再推送。

## composio-zhimeng（自定义 stdio MCP）——zhimeng63 Gmail only

**它是什么**：与 composio-pg 同类的启动器，但 Composio 用户为 **`zhimeng63`**，toolkit 仅 **gmail**。读取同一份 `~/.composio_pg_key`；`launch.sh` 复用 `/workspace/composio-pg/.venv/bin/python`。

**连接**（2026-10-09 核对）：

| 应用 | 账号 | connected account |
|---|---|---|
| Gmail | zhimeng63@gmail.com | `ca_5jGHEthCoWuD`（ACTIVE，已验证可读） |

**文件**：`connectors/composio-zhimeng/launch.py`、`launch.sh`（不含密钥；key 只从路径读取）。`setup.sh` / BOOTSTRAP Step 0 (d) 装到 `/workspace/composio-zhimeng/`。

**安装步骤**（在 composio-pg 装好且 `~/.composio_pg_key` 已就位之后）：

1. ```bash
   mkdir -p /workspace/composio-zhimeng
   install -m 700 /workspace/grokbot-home/connectors/composio-zhimeng/launch.sh /workspace/composio-zhimeng/
   install -m 600 /workspace/grokbot-home/connectors/composio-zhimeng/launch.py /workspace/composio-zhimeng/
   ```
2. 冒烟测试（同样**不要**打印 stderr）：
   `timeout 40 /workspace/composio-zhimeng/launch.sh </dev/null >/dev/null 2>/tmp/czm.err; grep -c "Proxy established successfully" /tmp/czm.err; rm -f /tmp/czm.err`
3. `AddMcpServer`：name **`composio-zhimeng`**，command **`/workspace/composio-zhimeng/launch.sh`**，无 args、无 env（在 composio-pg 之后添加）。
4. 自检：`user-composio-zhimeng` → `COMPOSIO_MANAGE_CONNECTIONS` `{"toolkits":["gmail"]}`（**不要** `reinitiate_all`）→ active；再读一封 zhimeng63 邮件确认。
5. 若新号上缺少 zhimeng63 的 Gmail 连接：用 `COMPOSIO_MANAGE_CONNECTIONS` 给 Composio 用户 **`zhimeng63`** 重新授权 Gmail（**不要**用 pg-test / composio-pg；旧 `ca_2rJjmKh8j1q0` 已删，勿重建到 composio-pg）。

## Grok Bot 自带邮箱（不是连接器，2026-10-10）
- `cloudpotato@mail.grokbot.com`：Grok Bot 原生邮箱，由小萌在当前账号领取。**绑在当前账号上，不能转移，换号即丢失**；新号若需要，只能用 ListEmailInboxes / ClaimEmailInbox 另领一个新地址（地址会不同），并相应改写「cloudpotato 来信提醒」任务。只用于临时注册、验证码等可丢弃用途。
