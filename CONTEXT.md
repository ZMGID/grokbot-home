# CONTEXT.md（关于我的共享记忆）

> 所有 bot 共用。换到新的 Grok Bot 账号后，每个 bot 都先读这个文件，再读自己的 `bots/<名字>/CONTEXT.md`。
> 最初由旧号主 bot 在 2026-10-08 导出，之后由每日同步任务维护。时间一律是北京时间（Asia/Shanghai，UTC+8）。
> 写回规则：关于“我”的、所有 bot 都该知道的事写这里；只跟某个 bot 的职责有关的写进它自己的 CONTEXT.md。

## 关于我
- 用中文交流；回答要直接、简短，先给结论。不喜欢绕远路——我说了要用某个方式做（例如“用 Composio 看 GitHub”），就按那个方式做，不要另起炉灶。
- 时区 Asia/Shanghai（UTC+8）。
- 有好几个 Grok Bot 账号，轮换着用，希望换号的成本尽量低（这个仓库就是为此建的）。
- GitHub 账号：`ZMGID`（显示名 ZhiMeng）。个人仓库约 16 公开 + 5 私有，主项目 kivio；还是组织 `dsh-external` 的成员（约 184 个 DSH 相关私有仓库）。
- 邮箱：`ohulercxm8@gmail.com`（仅 **`composio-pg`** / `ca_ZnzYtlTeic0s`）、`zhimeng63@gmail.com`（仅 **`composio-zhimeng`** / `ca_5jGHEthCoWuD`）。
- 常用本地 CLI：Claude Code、Codex、Pi、OpenCode、DSH。
- 评估别人的仓库时更看重 git 时间线和 AI 痕迹，不看功能清单。
- 在做虾皮（Shopee）巴西站选品调研，打算用 agent + Playwright + Shopdora（虾多拉）插件做自动化，而不是紫鸟浏览器（详见 `bots/xiaozhi/CONTEXT.md`）。
- 订阅建议（2026-10-07）：主要用 Grok Bot，建议先订 SuperGrok（$30/月，按月付），不够再升 Plus。

## 项目

### kivio（ZMGID/kivio）
- Tauri 2 + React/Vite/TS 前端 + Rust 后端的桌面 AI 助手，约 585 star。另有仓库 `Dsivio`、`dsivio-plugins`、`dsvideo-plugin`、`fkmem`（Pi 的运行时记忆）。
- **PR #60「feat: Kivio Study 材料学习工作台」**（分支 `feat/kivio-study-cloud`，草稿状态）：2026-10-07 20:48 的提交 `be06640` 修好了 Study browser regression；之后（10-07 20:49 那一轮）CI 和 Study browser regression **全部通过**，没有冲突，还没人 review；live check-mode 验收未过，10/7 后无进展。
- PR #60 的 review 意见：PR 太大（102 个文件、8000+ 行），建议把共用 Chat 的重构拆成单独 PR；迁移旧数据时判断冲突是直接比较两段 JSON 文本，字段顺序一变就可能误判；浏览器测试运行时联网下载真实 PDF，可能随机失败，建议缓存；Rust 测试 `antigravity.rs:497` 有一个不稳定的 OAuth 回调端口检测；工作流里 Node 20 的 actions 已弃用；ChatPanel 测试少一个 mock。
- kivio `main` 9-24 到 10-06 也有 CI 失败（最近一次 10-06 14:05），原因还没细查。
- 其他老 PR：#15「修复 external-agent 会话恢复」（7 月停着）、#8「Linux AppImage 适配基线」（6 月草稿）。

### Dsivio（ZMGID/Dsivio）
- (2026-10-08) 发布 **v1.1.0**（内置 Shopee 调研插件、图片搜 SKU 插件）；发版提交带 `[skip ci]`，release 流水线仍用 Node 20；未经完整 CI。
- `main` CI 自 9 月起一直红：CI 用 Node 20，测试用 `Promise.withResolvers`（Node 22）。**PR #1**（CI/release 升 Node 22）CI 全绿未合并，合并前需 Update branch 重跑完整 CI。
- (2026-10-08) 环境配置优化（同事装环境太慢）：**PR #2**（内嵌 WebView2）、**PR #3**（自带 Python/Node + npmmirror）、**PR #4**（自带工具转接与文档改用 dsivio python）均开出、CI 绿、均未合并。合并顺序建议 #3 → #4，#2 独立；用户计划 10/9 手工继续打磨（当天最重要）。
- (2026-10-08) 新方向 **IM Gateway**（接入企业微信/飞书等消息平台），参考 Hermes Agent；调研报告在共享电脑 `/workspace/dsivio-im/`（不进本仓库）。
- 官网产品页：`https://eastforceglobal.com/dsivio/`（自有服务器 nginx 静态站），10/8 已上线 v1.1.0 页面与安装包（由搭建运维负责；飞书仍未接入）。

### 仿 TourBox 创作控制器（原创设计，不是照抄）——文件在 `projects/creative-controller/`
- ESP32-S3 主控，USB-C 有线 + 蓝牙，1000 mAh 电池；**按 FDM 3D 打印设计**的左手人体工学外壳（约 95×94 mm，软圆方形、前低后高）；KiCad 9 PCB（嘉立创打样）；固件 **v1.1.0**；电脑端配置软件（Python）；BOM、打印说明、审查报告。
- 状态：ERC/DRC 0 错误，固件编译通过，26 颗元件都在嘉立创核对过（约 $12.3/板）。**还没打样，也没在真机上测试。**
- 打印：17 个零件 + 3 个 3MF 打印盘，PETG 0.2 mm 约 8.5 小时、90 g；M2 热熔铜螺母 + M2×14 螺丝；先打公差测试件，松紧不对就改 `mechanical/params.py` 里的 `FDM_CLR` 重新导出。
- 剩余风险 / 下单前待办：
  - **ENC2 滚轮编码器封装是占位的**：嘉立创没货，要单独买 Kailh 或 TTC 鼠标滚轮编码器，买到后核对封装。
  - **板上没有电池保护电路**：必须买带保护板的 603450 锂电池。
  - 下单时在嘉立创贴片预览里**逐个检查 CPL 元件旋转方向**（ESP32 模组尤其要看），清单在 `docs/审查报告.md`。
  - 按键开关 **TS-1102S 库存偏少**（约 1000 个，够 110 台左右），要做就早点下单。
  - 按键行程约 0.25 mm，手感可能偏硬（可换 Choc 矮轴）；按滚轮时滚轮会绕编码器轴略倾斜，需实测。
  - PCB 是自动布线（Freerouting），下单前最好请硬件工程师看一遍。
  - 建议先做 2–5 块板，焊好后进自检模式（插电时按住顶部长键）逐键测试。


## 分工（2026-10-08）

- **小萌**（主 bot / 经理；原名 Grok Bot，slug `grok-bot`，2026-10-08 改名）：分派任务、用 CreateAgent **创建新 bot**；工作日仅「巡检各 bot」(11:17/15:17，cron `17 11,15 * * 1-5`)。早晚「今日计划 / 今日总结」已移交**事务秘书**。时区 Asia/Hong_Kong（UTC+8）。
- **小枳**：调研（AI / 工具 / 技术规范 / 产品方案）与虾皮（Shopee）选品；活一般由小萌派，只走 Composio。
- **仓库管家**：维护公开仓库 `ZMGID/grokbot-home`，每天 03:14（北京时间）跑同步。
- **代码工程师**：盯 `ZMGID/Dsivio`（主）与 `ZMGID/kivio` 的 CI / 开着的 PR，修代码并开修复 PR；GitHub 只走 composio-pg。
- **搭建运维**：公司官网、飞书及其他系统/工具的搭建与维护。
- **事务秘书**（原名「邮件秘书」，2026-10-08 改名）：非技术事务（邮件、账号与订阅、周报/文档、提醒、比价等）+ 工作日早晚「今日计划」(08:53) 与「今日总结」(17:47)。**邮件/消息只写草稿，从不直接发送。**
- **硬件工程师**：创作控制器项目（`projects/creative-controller/`）。**(2026-10-08) 项目已暂停、待命**；无用户或小萌新指示不要继续做。
- **财务管家**（2026-10-09 小萌创建）：记账、订阅与固定支出、预算、报销对账、财务材料起草；**只记录，从不付款/转账/下单**。账本在 `/workspace/finance/`。

（2026-10-08 用户已删除 **dr eggbot**；原先「设计并创建 bot」改由主 bot **小萌**自己做。）

## 换号方案（2026-10-08 已确认）
- 所有东西放进 GitHub 仓库 `ZMGID/grokbot-home`（2026-10-08 起改为**公开**，旧私有仓库改名为 `grokbot-home-private-old`）：共享记忆（本文件）、每个 bot 的设定/记忆/定时任务（`bots/`）、连接器清单和启动脚本（`connectors/`）、技能（`skills/`）、工具环境脚本（`setup.sh`）、项目文件（`projects/`）。
- 新号流程：打开一个 Grok Bot，对它说「按 https://github.com/ZMGID/grokbot-home 配置你自己」。它按 `BOOTSTRAP.md` 配好自己，再用 CreateAgent 把其他 bot 全部建出来。
- **明文密钥永远不进仓库**。唯一例外：Composio key 用 `scripts/secret-crypt.py` 加密后放 `secrets/*.enc`；解密口令 `GROKBOT_HOME_PASSPHRASE` 只通过 bot 的密码框（secret prompt）提供。
- Composio 连接走两个自定义 stdio MCP（共用 `~/.composio_pg_key`；**一个 Composio 连接器对应一个 Gmail**）：
  - **`composio-pg`**（用户 `pg-test-5be86c3e-d220-4538-ab6d-ae22d538dfde`）：GitHub ZMGID（`ca_1g4u93YydZsp`）+ Gmail `ohulercxm8@gmail.com`（`ca_ZnzYtlTeic0s`）。**不含** zhimeng63。
  - **`composio-zhimeng`**（用户 `zhimeng63`）：仅 Gmail `zhimeng63@gmail.com`（`ca_5jGHEthCoWuD`）。
  - (2026-10-09) 经用户同意，已从 composio-pg 删除旧的 zhimeng63 连接 **`ca_2rJjmKh8j1q0`**。新号/重建时**不要**再在 composio-pg（pg-test 用户）下给 zhimeng63 授权；只通过 composio-zhimeng 授权。
- (2026-10-08) **应用连接只走 Composio**：不要再装官方 GitHub（`cursor-github`）、Origin、Finance、Composio 插件（32661537）。
- 同步方式：由专门 bot **仓库管家**每天约 03:14（北京时间）跑定时任务，把各 bot 的新记忆和设定同步进仓库，有变化才推送，推送前做密钥扫描。（2026-10-08 用户改口：原先「不单独建同步 bot、由主 bot 跑」已作废，移交给仓库管家。）
- 新号流程：匿名克隆 → 密码框填一次仓库口令 → 解密 Composio key、装 `composio-pg` + `composio-zhimeng` → 重建各 bot。`gh` 登录只在推送时需要。
- 不做公开分享模板（export-bot-template 只能生成公开模板，不用）。

## Grok Bot 自带邮箱（2026-10-10）
- (2026-10-10) 小萌为用户领了 Grok Bot 邮箱 **`cloudpotato@mail.grokbot.com`**。它绑定在**当前 Grok Bot 账号**上，**无法转移，换号后会丢失**，新号上也不能重新领回同一个地址（每个账号只能领一个，领了不能改）。
- 用途只限可丢弃的事：注册测试账号、收验证码、不重要的往来邮件。重要账号、账单一律留在用户自己的 Gmail。
- 小萌有一个只读的「cloudpotato 来信提醒」自动任务（来信即提醒用户，不回复、不删信），见 `bots/grok-bot/routines.md`。换号后该任务需按新号上的邮箱重建或删除。
