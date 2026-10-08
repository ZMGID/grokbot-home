# 连接器清单（connectors manifest）

> 导出时间：2026-10-08（北京时间），来源：旧号上主 bot 的连接器状态 + box 上的插件缓存。
> 连接器装在 **账号** 上，不是装在某个 bot 上：新号上第一个 bot 装好以后，后面用 CreateAgent 建的 bot 都能直接用。
> 本文件只记名字、ID、地址和步骤，**不含任何密钥**。

| # | 连接器 | 类型 | 怎么装 | 需要用户做什么 | 必需？ |
|---|---|---|---|---|---|
| 1 | **GitHub**（工具命名空间 `cursor-github`） | Grok Bot / Cursor 官方连接器 | `SearchPlugins "GitHub"` → `InstallPlugin`（若已内置则 `GetMcpServerStatus` 看状态，needsAuth 时 `AuthenticateMcpServer`） | 点一次授权卡片，GitHub 账号选 **ZMGID** | ✅ 必需 |
| 2 | **Origin**（`cursor-origin`） | Cursor 官方（Cursor 自己的代码托管） | 新号通常自带；没有就 `SearchPlugins "Origin"` | 一般无需操作，needsAuth 时点授权 | 可选 |
| 3 | **Composio 插件**（`user-Composio`，MCP 地址 `https://connect.composio.dev/mcp`） | 插件市场插件，**plugin id `32661537`**（cursor-public） | `InstallPlugin` id `32661537` | OAuth 登录 Composio 一次 | 可选 |
| 4 | **composio-pg**（`user-composio-pg`） | 自定义 **stdio** MCP（跑在 box 上） | 见下文「composio-pg」 | 在密码框里填一次 Composio **项目 API key** | ✅ 必需（GitHub/Gmail 都走它） |
| 5 | **Finance**（`user-Finance-xai`，`https://connectors-gateway.grok.com/gateway/v1/finance/mcp`） | 插件市场插件，**plugin id `63408931`** | `InstallPlugin` id `63408931` | 旧号上一直是 needsAuth，没登录过 | 可选（可跳过） |

另外两样不是连接器但要记得：

- **pstack 插件**（plugin id **`9717366`**，cursor-public）：写代码类 bot 用的工作流技能包（architect、tdd、swarm、arena……）。dr eggbot 在旧号上装过。新号上 `InstallPlugin 9717366` 重装即可，技能不在本仓库里。
- **`x` 工具命名空间**（X/Twitter 搜索、新闻）：旧号上出现过，属于平台自带工具，不需要安装；新号若没有就忽略。
- **`gh` 命令行**：不是连接器，但很多事靠它。新号 box 上要 `gh auth login --web`，把设备码给用户确认（见 BOOTSTRAP 第 0 步）。

## 1. GitHub（官方）

- 装好后用 `GetMcpServerStatus` 确认 `connected`。
- 自检：调用 `cursor-github` 的 `get_me`，login 应为 `ZMGID`。

## 3. Composio 插件（官方 OAuth 版）——注意它看不到我的应用

- 旧号上装过，OAuth 登录的是我的 Composio 账号本身，查询时用的是 **登录账号自己的 user**，
  而我的 GitHub / Gmail 授权都挂在开发者项目里的 **测试用户 `pg-test-5be86c3e-d220-4538-ab6d-ae22d538dfde`** 下面，
  所以这个插件里 **看不到任何应用（全是 0 个连接）**。
- 结论：要用 GitHub/Gmail 就走下面的 `composio-pg`。这个插件装不装都行；装了也**不要**在里面重新生成授权链接（我明确说过不要重新授权一套）。

## 4. composio-pg（自定义 stdio MCP）

**它是什么**：box 上的一个小启动器。读取 `~/.composio_pg_key`（Composio 项目 API key），用 Composio SDK 给用户
`pg-test-5be86c3e-d220-4538-ab6d-ae22d538dfde` 创建一个会话，再用 `npx mcp-remote` 把会话的 MCP 地址桥接成 stdio。

**这个 Composio 用户下现有的连接**（2026-10-08 核对，均为 ACTIVE）：

| 应用 | 账号 |
|---|---|
| GitHub | ZMGID（ZhiMeng） |
| Gmail | ohulercxm8@gmail.com |
| Gmail | zhimeng63@gmail.com |

Composio 项目 ID：`pr_lh5-8poHU4QB`（只有这一个项目）。

**文件**：`connectors/composio-pg/launch.py`、`launch.sh`（不含密钥，密钥只从 `/home/box/.composio_pg_key` 读取）。

**安装步骤**（BOOTSTRAP 第 3 步会照做）：

1. `bash setup.sh` 已经做了：
   - 把 `launch.sh`、`launch.py` 复制到 `/workspace/composio-pg/`；
   - `cd /workspace/composio-pg && uv venv .venv && uv pip install --python .venv/bin/python composio==0.25.0`（旧号用的版本；装不上就装最新版）；
   - 预热 `npx -y mcp-remote`（旧号缓存的是 mcp-remote ^0.14.3）。
2. 用 **secret-request（密码框，掩码输入）** 向用户要 Composio 项目 API key（Composio 控制台 → 项目设置 → API Keys）。
   值写入 `/home/box/.composio_pg_key`，然后 `chmod 600 /home/box/.composio_pg_key`。**绝不能**让用户把 key 贴进聊天，也不要 `cat` 出来。
   - 备选（若密码框不能落到文件）：请用户打开 bot 的桌面终端，自己执行
     `read -rsp 'Composio key: ' K && umask 077 && printf %s "$K" > ~/.composio_pg_key && unset K`
3. 冒烟测试（**不要**打印 stderr：mcp-remote 会在日志里明文打印 `Using custom headers: x-api-key:<key>`）：
   `timeout 40 /workspace/composio-pg/launch.sh </dev/null >/dev/null 2>/tmp/cpg.err; grep -c "Proxy established successfully" /tmp/cpg.err`
   ——输出 `1` 即成功（约 6 秒后连上，40 秒超时退出是正常的）。输出 `0` 时只用 `grep -iE "error|401|403" /tmp/cpg.err | grep -vi x-api-key` 看原因。看完一定 `rm -f /tmp/cpg.err`。
4. `AddMcpServer`：name **`composio-pg`**，command **`/workspace/composio-pg/launch.sh`**，无 args、无 env（密钥不经过 MCP 配置）。
   这个服务器会出现在账号下所有 bot 里。
5. 自检：调用 `user-composio-pg` 的 `COMPOSIO_MANAGE_CONNECTIONS`，参数 `{"toolkits":["github","gmail"]}`（**不要** `reinitiate_all`），
   应返回 `All connections are active`，GitHub login 为 ZMGID。第二个 Gmail（zhimeng63）在同一用户下，用 `COMPOSIO_SEARCH_TOOLS`/读邮件工具时可选账号。

**用户偏好**：我要求“GitHub 通过 Composio（com）来看”，所以查 GitHub 动态、通知时优先用 composio-pg 里的 GitHub；
写操作（PR、评论）可以用官方 GitHub 连接器或 `gh`。

**换号/轮换 key**：如果 Composio key 换了，只需重写 `~/.composio_pg_key` 并 `RestartMcpServers`，不用改仓库。

## 5. Finance

- 旧号状态：installed，needsAuth，从没登录。我没提过要用。新号上可以不装；装了就让它保持 needsAuth，等我需要时再授权。
