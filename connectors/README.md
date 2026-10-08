# 连接器清单（connectors manifest）

> 导出时间：2026-10-08（北京时间），来源：旧号上主 bot 的连接器状态 + box 上的插件缓存。
> 连接器装在 **账号** 上，不是装在某个 bot 上：新号上第一个 bot 装好以后，后面用 CreateAgent 建的 bot 都能直接用。
> 本文件只记名字、ID、地址和步骤，**不含任何密钥**。
>
> **规矩（2026-10-08）**：所有应用连接只走 Composio（自定义 `composio-pg`，Composio 用户 `pg-test-5be86c3e-d220-4538-ab6d-ae22d538dfde`）。不要再装官方 GitHub / Origin / Finance / Composio 插件。新应用一律在 Composio 控制台里给该测试用户授权，再通过 composio-pg 使用。

| # | 连接器 | 类型 | 怎么装 | 需要用户做什么 | 必需？ |
|---|---|---|---|---|---|
| 1 | **composio-pg**（`user-composio-pg`） | 自定义 **stdio** MCP（跑在 box 上） | 见下文「composio-pg」；BOOTSTRAP Step 0 会先内联写出启动器 | 在密码框里填一次 Composio **项目 API key** | ✅ 必需（唯一的应用连接通道） |
| 2 | **GitHub**（`cursor-github`） | 官方连接器 | — | — | ❌ 不需要（GitHub 走 composio-pg） |
| 3 | **Origin**（`cursor-origin`） | 官方连接器 | — | — | ❌ 不需要 |
| 4 | **Composio 插件**（`user-Composio`，plugin id `32661537`） | 插件市场 OAuth 版 | — | — | ❌ 不需要（它看到的是另一个 Composio user，看不到我们的应用） |
| 5 | **Finance**（plugin id `63408931`） | 插件市场 | — | — | ❌ 不需要 |

另外两样不是「应用连接器」但要记得：

- **pstack 插件**（plugin id **`9717366`**，cursor-public）：写代码类 bot 用的工作流技能包（architect、tdd、swarm、arena……）。dr eggbot 需要它。这是技能插件，不是应用连接；新号上 `InstallPlugin 9717366` 即可。
- **`x` 工具命名空间**（X/Twitter 搜索、新闻）：平台自带，不需要安装；新号若没有就忽略。
- **`gh` 命令行**：不是连接器。新号上用 Composio 里 GitHub（ZMGID）的 access token 做 `gh auth login --with-token`（见 BOOTSTRAP Step 0）；失败再退回设备码登录。

## composio-pg（自定义 stdio MCP）——唯一必需的应用连接

**它是什么**：box 上的一个小启动器。读取 `~/.composio_pg_key`（Composio 项目 API key），用 Composio SDK 给用户
`pg-test-5be86c3e-d220-4538-ab6d-ae22d538dfde` 创建一个会话，再用 `npx mcp-remote` 把会话的 MCP 地址桥接成 stdio。

**这个 Composio 用户下现有的连接**（2026-10-08 核对，均为 ACTIVE）：

| 应用 | 账号 |
|---|---|
| GitHub | ZMGID（ZhiMeng） |
| Gmail | ohulercxm8@gmail.com |
| Gmail | zhimeng63@gmail.com |

Composio 项目 ID：`pr_lh5-8poHU4QB`（只有这一个项目）。

**文件**：`connectors/composio-pg/launch.py`、`launch.sh`（不含密钥）。仓库私有时 Step 0 会先按 BOOTSTRAP 里的内联片段写出这两份文件，不必先克隆仓库。

**安装步骤**：

1. 用 **secret-request（密码框，掩码输入）** 向用户要 Composio 项目 API key（Composio 控制台 → 项目设置 → API Keys）。
   值写入 `/home/box/.composio_pg_key`，然后 `chmod 600`。**绝不能**让用户把 key 贴进聊天，也不要 `cat` 出来。
   - 备选：请用户在 bot 桌面终端执行
     `read -rsp 'Composio key: ' K && umask 077 && printf %s "$K" > ~/.composio_pg_key && unset K`
2. 写出启动器（若 `/workspace/composio-pg/launch.sh` 还不存在，用 BOOTSTRAP Step 0 的内联内容；仓库克隆后也可用 `setup.sh` / 复制 `connectors/composio-pg/`）：
   ```bash
   mkdir -p /workspace/composio-pg && cd /workspace/composio-pg
   # launch.py / launch.sh 见 BOOTSTRAP Step 0（与 connectors/composio-pg/ 相同）
   [ -x .venv/bin/python ] || uv venv -q .venv
   uv pip install -q --python .venv/bin/python "composio==0.25.0" || uv pip install -q --python .venv/bin/python composio
   npx -y mcp-remote --help >/dev/null 2>&1 || true
   ```
3. 冒烟测试（**不要**打印 stderr：mcp-remote 会在日志里明文打印 `x-api-key`）：
   `timeout 40 /workspace/composio-pg/launch.sh </dev/null >/dev/null 2>/tmp/cpg.err; grep -c "Proxy established successfully" /tmp/cpg.err; rm -f /tmp/cpg.err`
   ——输出 `1` 即成功。
4. `AddMcpServer`：name **`composio-pg`**，command **`/workspace/composio-pg/launch.sh`**，无 args、无 env。
5. 自检：`user-composio-pg` → `COMPOSIO_MANAGE_CONNECTIONS`，参数 `{"toolkits":["github","gmail"]}`（**不要** `reinitiate_all`），
   应返回 `All connections are active`，GitHub login 为 ZMGID。

**新应用**：只在 Composio 控制台给测试用户 `pg-test-5be86c3e-d220-4538-ab6d-ae22d538dfde` 授权新 toolkit，然后通过 composio-pg 使用。**不要**再装官方连接器。

**换号/轮换 key**：重写 `~/.composio_pg_key` 并 `RestartMcpServers`，不用改仓库。
