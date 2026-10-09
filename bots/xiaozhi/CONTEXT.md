# 小枳自己的记忆与项目状态

> 先读根目录 `/CONTEXT.md`。这里是小枳的记忆（旧号 memory/profile.md、memory/log/ 和对话记录整理，2026-10-08 导出；description 于 2026-10-09 由小萌写入线上）。

## 职责（与线上 description 一致）
- 调研：AI / 工具 / 技术规范 / 产品方案，写成可开工要点或文档。
- 虾皮（Shopee）选品：品类、竞品、价格和素材相关调研与整理。
- 需要时用 composio-pg（GitHub / ohulercxm8）与 composio-zhimeng（zhimeng63 Gmail）只读查询；做完简短汇报用户并抄送小萌。
- 不做：分派/新建 bot、Dsivio/kivio 代码与 CI、官网/飞书搭建、事务与早晚报、硬件、grokbot-home。

## 关于用户（小枳记住的）
- (2026-08-21) 用户在共用电脑上拉了 Kivio Desktop（github.com/ZMGID/kivio），本地路径 `/workspace/kivio`，main 分支，当时在做 Linux 适配（ONNX Runtime linux 包、非 macOS overlay 窗口销毁、区域截图 `exclude_self_pid` 参数）。
- (2026-08-21) 常用本地 CLI：Claude Code、Codex、Pi、OpenCode、DSH。
- (2026-08-26) GitHub `ZMGID`（ZhiMeng），个人仓库 15 个（10-08 通过 Composio 看是公开 16 + 私有 5），主项目 kivio；组织 dsh-external 成员（约 184 个 DSH 插件私有仓库）。
- (2026-08-26) 个人其余仓库：私有 wetware、nabai、obsidian-personal-data、Contin；公开 claude-desktop-assistant、Longtxt、ev-charging-optimization、File-Auto-Copy-Tool、openai-gemini；fork claude-tap-kivio、latex-arxiv-SKILL、hermes-agent。近期在改 fkmem（Pi 的运行时记忆）。
- (2026-08-31) 评估别人仓库时更看重 git 时间线与 AI 痕迹，不看功能清单。
- (2026-10-08) 两个 Gmail：ohulercxm8@gmail.com、zhimeng63@gmail.com。邮件里的要点：Anthropic 10-03 以“地区不支持”封了 Claude 账号，申诉和 $88.99 Max 订阅退款都被拒（10-04），已申请数据导出；zhimeng63 有一封 Shopee 巴西邮箱确认（10-07 23:41）还没点。
- (2026-10-08) 用户在 Composio 控制台只有一个项目（`pr_lh5-8poHU4QB`）。曾把“MCP 需要 API 密钥”开关关掉过——已提醒他重新打开。

## 项目与工作记录

### kivio 本地 CLI 适配审查（2026-08-21）
- 已对接 10 个本地 CLI：Claude、Codex、Cursor、OpenCode、Gemini、Kimi、Pi、Hermes、Grok、dsh。
- 协议五路：Claude 走 stream-json，Codex 走 app-server，Pi 走自有 RPC，dsh 走 SDK JSON-RPC，其余（Cursor/OpenCode/Gemini/Kimi/Hermes/Grok）走 ACP。能运行中注入（steer）的只有 Codex、Pi、dsh；能原生 follow-up 的只有 Pi、dsh。
- 当时最高优先级缺口：Grok 0.2.103→1.0.5（默认 Grok 4.6）；Gemini `--experimental-acp` 转正为 `--acp`；dsh-acp 仍不可用（SDK 路径正确，但 rc.8 SQLite 不兼容）。其次：Claude 2.1.220→2.1.238（5 系默认去掉 Todo 工具，未设 `CLAUDE_CODE_ENABLE_TODO_TOOLS`）、Codex 0.149 steer 强制 `expectedTurnId`、Cursor 需接 ask_question/create_plan 且静态模型表已旧；ACP v2 草案不要切。
- 常用五个细查：Claude 2.1.238；Codex 0.149（精选 gpt-5.6 与 live model/list 不一致、initialize 无 experimentalApi）；Pi 0.84.2（steer/follow_up 已接，get_available_thinking_levels 未调）；OpenCode 1.18.20（仍 ACP v1 session/load，兜底模型旧）；DSH 0.1.1-rc.2（SDK+bridge 正确，Kivio 自管 JSON 会话不受 rc.8 SQLite 影响）。
- 结论只做了总结，没改代码。

### 招聘评估：GitHub 用户 biheto（2026-08-31）
- ValuSee 与 DevAgent-Studio（2026-08-08 改名）是同一份 AI 赶出来的毕业作品集：账号 2024-08 注册、到 2026-06 无提交，公开活动从 2026-07-09 开始；作者时间被 GIT_AUTHOR_DATE 整点回填；7 月做治理平台、8 月改成购物产品；8 月 9 日一天 47 个 feat/merge；172 星含牛客求 star，watcher 为 0。
- 给老板的口径：当会用 AI 赶 demo 的实习生面试，不当开源作者；star、两个独立平台、Langflow contributor 都从汇报里拿掉。

### agent 插件/skill 打包调研（2026-09-02）
- 现在的做法是“插件为安装单位，里面多个小 skill 为触发单位”：插件根有 `.claude-plugin/plugin.json`，`skills/<一件事>/SKILL.md`，MCP 用根目录 `.mcp.json`，hooks 也放根上。示例：anthropics/claude-plugins-official 的 plugin-dev（7 个 skill）。
- 加载差异：Claude Code 启动只注入 name+description 目录，匹配或 `/` 调用后把整份 SKILL.md 贴进对话并常驻（references/scripts 不自动进）；Codex 只注入「name: description (file: 绝对路径)」一行，正文不自动灌，插件须写入 marketplace.json。
- Claude Code 插件还能带 commands、agents、hooks、LSP、monitors、themes、workflows、output styles、channels、bin、settings/userConfig/dependencies；Codex 目前只有 skill、MCP、`.app.json`、hooks、assets。

### AI 新闻（2026-10-07）
- 给过一次 AI 新闻速览（OpenAI 一次放出数百个数学结果、Apple 论文“单 agent + shell 胜过多 agent 框架”、Google Playground、DeepSeek 融资等）。用户对“单 agent 胜多 agent”与 Kivio 的关联可能感兴趣。

### 虾皮巴西选品调研 → agent 插件方案（2026-10-07 ~ 10-08）
- 用户发来一份 .doc 操作说明：紫鸟浏览器装虾多拉（Shopdora）插件 → 豆包根据产品图生成巴西电商标题 → 虾皮搜索 → View Product Details 看竞品 → 按 Total Sales / GMV / Price 挑三条（销量最高、居中、价格最低且有销量）填调研表。
- 结论：Shopdora 是 Shopee 数据插件，Chrome/Edge 都能装，不需要紫鸟（紫鸟只用于多店铺防关联）。
- 用户想用 agent 直接驱动 Playwright CLI 并做成给 agent 用的插件。小枳的方案：Playwright 用 Chromium 持久化上下文加载扩展（`launchPersistentContext` + `--load-extension`，有头或新版 headless），插件拆成 title / search / pick / report 四个小 skill，抓取逻辑集中在 `scripts/` 或一个小 MCP（如 `search_products(title)`），选品规则写成固定脚本；风险：虾皮反爬、Shopdora 改版导致选择器失效。还没开始搭骨架，等用户说。
- CSV 不支持嵌图片；要看图用 `.xlsx`（openpyxl 嵌图）或飞书表格。

### Composio 接入（2026-10-08，关键）
- 用户在 Composio 控制台给测试用户 `pg-test-5be86c3e-d220-4538-ab6d-ae22d538dfde` 授权了 GitHub 和两个 Gmail；官方 Composio 插件（OAuth）查的是登录账号自己的 user，所以看不到。
- 用户通过密码框给了 Composio 项目 API key（存在 box 的 `/home/box/.composio_pg_key`，权限 600；**key 本身不在仓库**），小枳写了 `/workspace/composio-pg/launch.py` + `launch.sh`（现在在 `connectors/composio-pg/`），测试通过；后来主 bot 把它作为 `composio-pg` 加到账号里。
- 用户要求：**看 GitHub 也通过 Composio（composio-pg）**。通过它看到：Dsivio main CI 从 9-27 起一直挂（Node 20 vs `Promise.withResolvers`）；kivio main 9-24 ~ 10-06 也有 CI 失败（未细查）；PR #60 最后一轮全过；9 月底 kivio 合并/关闭了 agent todo 工具重构、上下文压缩对齐 ZCode、标题大纲原地展开、外部 CLI 会话“回退到这里”等 PR。
- (2026-10-08) 后续：Dsivio **PR #1**（Node 22）已由代码工程师开出且 CI 全绿、未合并；kivio main 红灯原因仍未细查。

### Dsivio IM Gateway 调研（2026-10-08 ~ 10-09）
- 小萌派活：调研 Hermes IM 网关。确认对象是 Nous Research 的 [Hermes Agent](https://github.com/NousResearch/hermes-agent)（Python）；企业微信与飞书均已内置。桌面端无公网，两边都应走长连接。建议先做企业微信智能机器人（协议公开、可纯 Rust、原生流式），飞书第二；MVP 单平台单聊 + 流式/配对码/重连；IM 发起的对话默认拒绝需审批的工具。报告：`/workspace/dsivio-im/hermes-gateway.md`（不进本仓库）。
- (2026-10-09) 用户问有无现成 SDK：飞书官方 `@larksuiteoapi/node-sdk`（含 `createLarkChannel` 长连接等）、企微官方 `@wecom/aibot-node-sdk`（长连接/流式），均为 Node；Rust 仅有不成熟社区实现。用户决定自己写 Rust，要求整理协议实现手册，明早使用（`/workspace/dsivio-im/rust-impl-guide.md`）。

- (2026-10-09) Gmail `zhimeng63@gmail.com` 改走 **composio-zhimeng**；GitHub 与 ohulercxm8 仍走 composio-pg。

## 教训
- 用户正在按某个方式配置时，不要提供另一套方案（例如重新生成授权链接）。先问清楚、照用户的路子走。
- 不能控制用户电脑上的浏览器时，直接说明并请他截图或复制关键值（例如完整 User ID）。

## 2026-10-09 ~ 10-10
- (2026-10-09) Dsivio IM 网关 Rust 实现手册在 box 的 `/workspace/dsivio-im/rust-impl-guide.md`（两个平台的帧格式、心跳、重连、收发、流式和媒体，字段标了出处）。
- (2026-10-10) 用户嫌 AI 生成的页面全是输入框、没设计感，调研 UI 设计类 skill（含 X 上的推荐）：首推 **Impeccable**（`npx impeccable install`，`/impeccable init` 生成 PRODUCT.md/DESIGN.md，会装改后自动检查的 hook），第二 **shadcn 官方 skill**（`npx skills add shadcn/ui`）配 shadcn/lint，第三 Jakub Krehel skills；建议两者一起用，以 shadcn 主题变量作为唯一色值来源。
