# CONTEXT.md（关于我的共享记忆）

> 所有 bot 共用。换到新的 Grok Bot 账号后，每个 bot 都先读这个文件，再读自己的 `bots/<名字>/CONTEXT.md`。
> 最初由旧号主 bot 在 2026-10-08 导出，之后由每日同步任务维护。时间一律是北京时间（Asia/Shanghai，UTC+8）。
> 写回规则：关于“我”的、所有 bot 都该知道的事写这里；只跟某个 bot 的职责有关的写进它自己的 CONTEXT.md。

## 关于我
- 用中文交流；回答要直接、简短，先给结论。不喜欢绕远路——我说了要用某个方式做（例如“用 Composio 看 GitHub”），就按那个方式做，不要另起炉灶。
- 时区 Asia/Shanghai（UTC+8）。
- 有好几个 Grok Bot 账号，轮换着用，希望换号的成本尽量低（这个仓库就是为此建的）。
- GitHub 账号：`ZMGID`（显示名 ZhiMeng）。个人仓库约 16 公开 + 5 私有，主项目 kivio；还是组织 `dsh-external` 的成员（约 184 个 DSH 相关私有仓库）。
- 邮箱：`ohulercxm8@gmail.com`（**`composio-pg`** / `ca_ZnzYtlTeic0s`）、`zhimeng63@gmail.com`（仅 **`composio-zhimeng`** / `ca_5jGHEthCoWuD`）。另：composio-pg 自 2026-10-14 起还有第二个 Gmail 连接 `ca_JwThbeIld_Jw`（用户决定两个都保留；读 ohulercxm8 时要指定连接）。
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


### AI 编程键盘 + AI 语音脚踏板（2026-10-15 起，新号；**脚踏板 2026-10-19 已废弃**）——文件在盒子 `/workspace/ai-keyboard/`、`/workspace/ai-pedal/`（商业产品设计，暂不进公开仓库，入不入库等用户定）
- (2026-10-15 晚) 我决定做 **AI 相关、拿去卖、门槛低** 的硬件；AI 眼镜这类整机做不了。选定 **AI 编程键盘**（类 AhaKey）：只做**一款**（不分入门/Pro 两档）——4 个键（2U 语音键配卫星轴、批准、打断/拒绝、跳转）+ 小屏 + **内置麦克风**（藏在壳里开孔，不要凸出的杆）+ 自动/逐个批准切换 + 状态灯；有线 + 蓝牙 + 电池；用现成 **ESP32-S3 SuperMini** 开发板，不自己画 PCB。各家 agent（Claude Code、Codex、Cursor）都能用；产品名不能用 Claude/Codex 等商标。
- **(2026-10-19) AI 脚踏板项目已废弃**：老板决定不做，「AI脚踏板」群已解散、成员已移出；`/workspace/ai-pedal/` 原样归档保留（不删不改），没有新指示不再做。下面踏板相关条目只作历史记录。
- (2026-10-16 00:50) 再开 **AI 语音输入脚踏板**（三踏板：语音 / 批准 / 拒绝），交付标准同键盘。（2026-10-19 已废弃）
- **小萌是这两个产品的产品经理**：我只跟小萌谈产品，小萌在群「AI编程键盘」「AI脚踏板」（后者 2026-10-19 已解散）里协调硬件工程师、代码工程师、商品调研、测试工程师，整理后汇报给我。
- 我的硬件偏好：配件选**淘宝上便宜、常见、好买**的通用件，附链接，价格以我核价为准；**成本优先**，能免焊就免焊，焊接明显便宜也可以焊；能 3D 打印的尽量打印（键帽也用 3D 打印、可彩色打印图案，接触面平就行；拨杆用打印件设计、要有小巧思）；按 **FDM** 设计：公差约 0.1 mm、考虑塑料强度、**底面当产品外观面**（多色图标更友好）、配件尺寸留余量；外观要好看；软硬件都参考 GitHub / X 上的同类开源项目。
- 交付标准：可直接打印的模型（STL）、带图淘宝 BOM、可直接刷的固件、刷机与使用教程，做完交测试工程师测。
- 状态（2026-10-16 03:17）：键盘外壳 **v4.1d** 定为样机版并冻结（等我反馈；只追加电池底部浅槽）；固件已编译出可刷整包（未上真板）。踏板外观 **v3.2** 冻结，BOM 与装配文档已出。待我定：固件许可证（Arduino-ESP32 内核 LGPL-2.1，开源固件或提供目标文件）；踏板 9° 倾斜（后端高约 16 mm）还是 5.5°。样机实测项：SuperMini VBUS–5V 是否有二极管、踏板铰链 100 kg 静载。BOM 价格均「待核」，**没有下单、没有付款**。

- 状态（2026-10-17 凌晨）：键盘外观被我否掉 v4 后重做 **v5 系列**——键帽露出 5.5 mm、楔形外壳（前沿 18 mm）、**切换用 EC11 + 3D 打印旋钮帽，长按 F16 做备用**（我 10-16 定）、旋钮在右上、状态灯用**旋钮外圈光环**（方案 B，我 10-16 选）、屏幕按 0.96 寸 SSD1306 实际尺寸和真实固件界面画；固件 1.1.0（旋钮 / 长按切换、模式存闪存、USB + 蓝牙，未上真板）。踏板铰链验收线定 3 倍 100 kg，样件实测，不过就换已做好的 Φ10 销轴版。给老板的产品介绍：**要写成申报书式正式文档，不要 PPT 风格**（10-17 凌晨已出 24 页申报书 PDF + Word 和完整资料包）。仍待我定：固件许可证、首发配色、踏板默认按键、零件核价谁做；公差试件需我自己打印。
- 状态（2026-10-19 17:00）：我宣布 **键盘第一版收尾**——最终外壳 **v5.8 B 光环版**（测试复核通过）、固件 1.1.0；产品图和全套文件（打印模型、带图 BOM、接线/组装文档、介绍与申报书、固件、测试记录）已打包给我。样机还没下单，蓝牙配对、光环漏光、公差件等待实测。
- 我的要求：效果图 / 渲染必须按真实元件尺寸和真实固件界面画，不要随手放占位内容。

## 分工（2026-10-08，2026-10-19 更新）

- **小萌**（主 bot / 经理；原名 Grok Bot，slug `grok-bot`，2026-10-08 改名；2026-10-15 起兼 AI 编程键盘 / 脚踏板（脚踏板 2026-10-19 已废弃）的产品经理，2026-10-19 起兼 AI 陪伴小机器人的产品经理）：分派任务、用 CreateAgent **创建新 bot**；工作日「巡检各 bot」(11:17/15:17)；另有 cloudpotato 来信提醒与 Gmail webhook「gmail-new-mail」。早晚「今日计划 / 今日总结」已移交**事务秘书**。时区 Asia/Hong_Kong（UTC+8）。
- **小枳**：调研（AI / 工具 / 技术规范 / 产品方案）与虾皮（Shopee）选品；活一般由小萌派，只走 Composio。
- **仓库管家**：维护公开仓库 `ZMGID/grokbot-home`，每天 03:14（北京时间）跑同步。
- **代码工程师**：盯 `ZMGID/Dsivio`（主）与 `ZMGID/kivio` 的 CI / 开着的 PR，修代码并开修复 PR；GitHub 只走 composio-pg。**10/16 用户叫停后，没有用户或小萌的明确指令不动 Dsivio / kivio。** 另负责 AI 编程键盘、AI 陪伴小机器人（基于 xiaozhi-esp32）的固件与电脑端软件；AI 脚踏板 2026-10-19 已废弃，`/workspace/ai-pedal/` 只归档（2026-10-19 线上 description 已由小萌更新）。
- **搭建运维**：公司官网、飞书及其他系统/工具的搭建与维护（飞书日常可用 lark-cli；搭建配置仍归本 bot）。
- **事务秘书**（原名「邮件秘书」，2026-10-08 改名）：非技术事务（邮件、账号与订阅、周报/文档、提醒、比价等）+ 工作日早晚「今日计划」(08:53) 与「今日总结」(17:47)。**邮件/消息只写草稿，从不直接发送。**
- **硬件工程师**：**2026-10-15 起**主力做 AI 编程键盘的结构、外壳、接线、BOM（AI 脚踏板 2026-10-19 已废弃，文件归档不动）；**不做 AI 陪伴小机器人**（2026-10-19 线上 description 已由小萌更新）；创作控制器项目（`projects/creative-controller/`）**(2026-10-08) 已停止**。
- **测试工程师**（2026-10-15 小萌新建，仅新号）：AI 编程键盘（ESP32-S3）/ AI 陪伴小机器人（2026-10-19 加入）的测试计划（AI 脚踏板 2026-10-19 已废弃，不再测试）、方案与交付物评审、缺陷单跟踪、样机实测与回归、出货验收与认证提醒。
- **结构工程师**（2026-10-19 小萌新建，仅新号）：AI 陪伴小机器人的外观造型、3D 建模、渲染图、运动机构、可 FDM 打印的 STL/STEP；外观先给小萌过目再给我确认。
- **电子工程师**（2026-10-19 小萌新建，仅新号）：AI 陪伴小机器人的主控与模块选型（优先现成 ESP32-S3 开发板）、电源与充电、引脚表、接线图、带图淘宝 BOM；下单前先问我。
- **AI 陪伴小机器人**（2026-10-19 立项，新号）：协作群「AI陪伴机器人」（小萌、结构工程师、电子工程师、代码工程师、商品调研、测试工程师；小萌任产品经理），资料在盒子 `/workspace/ai-robot/`，不进公开仓库。
  - 状态（2026-10-19 晚）：头 Ø50、整机高 ≤80；我嫌 S 版底座 Ø76 太大，第一版求简单继续用 T7 主板；结构返工后小萌定 **底座 Ø70 + 402535 小电池**，插电为主、插 USB 时舵机走 USB 供电；BE70 详图已过小萌审核、渲染给我看了。样件清单 23 项，**没有下单**，买不买等我定。固件 v0.3.4 只编译通过、没上实物。
- **财务管家**（2026-10-09 小萌创建）：记账、订阅与固定支出、预算、报销对账、财务材料起草；**只记录，从不付款/转账/下单**。明文账本 `/workspace/finance/`；加密备份 `secrets/finance.tgz.enc`（换号按 BOOTSTRAP 解密恢复）。

（2026-10-08 用户已删除 **dr eggbot**；原先「设计并创建 bot」改由主 bot **小萌**自己做。）

## 换号方案（2026-10-08 已确认）
- 所有东西放进 GitHub 仓库 `ZMGID/grokbot-home`（2026-10-08 起改为**公开**，旧私有仓库改名为 `grokbot-home-private-old`）：共享记忆（本文件）、每个 bot 的设定/记忆/定时任务（`bots/`）、连接器清单和启动脚本（`connectors/`）、技能（`skills/`）、工具环境脚本（`setup.sh`）、项目文件（`projects/`）。
- 新号流程：打开一个 Grok Bot，对它说「按 https://github.com/ZMGID/grokbot-home 配置你自己」。它按 `BOOTSTRAP.md` 配好自己，再用 CreateAgent 把其他 bot 全部建出来。
- **明文密钥/账本永远不进仓库**。加密进 `secrets/*.enc`（Composio key 用 `enc`/`dec`；账本 tar 用 `enc-bin`/`dec-bin`，见 `secrets/finance.tgz.enc`）。解密口令 `GROKBOT_HOME_PASSPHRASE` 只通过 bot 的密码框（secret prompt）提供。
- (2026-10-12) 用户要求仓库包含**恢复所需的全部东西，含密钥**，但只能加密：`scripts/pack-bundles.sh`（sync 每次自动跑、内容没变不重新加密）生成 `secrets/box-secrets.tgz.enc`（Composio key、飞书 lark-cli app secret 与 token、gh 登录、ssh 配置与 eastforce 服务器资料/私钥、gmail webhook URL、`COMPOSIO_API_KEY`/`GMAIL_WEBHOOK_KEY` 的值）、`secrets/daily.tgz.enc`（`/workspace/assistant/daily/`）、`secrets/feishu-cli.tgz.enc`（`/workspace/feishu-cli/` 全部）、`secrets/finance.tgz.enc`。无密钥的 `/workspace/assistant/`（routines、big-picture、ideas）明文放 `workspace/assistant/`，`/workspace/brake-game/` 放 `projects/brake-game/`。恢复步骤见 BOOTSTRAP Step 0 (b++)。
- 仓库公开 + 口令较短（用户 2026-10-12 决定不换，别再提醒；换法见 `secrets/README.md`，仅在用户主动要求时用）。
- Composio 连接走两个自定义 stdio MCP（共用 `~/.composio_pg_key`；**一个 Composio 连接器对应一个 Gmail**）：
  - **`composio-pg`**（用户 `pg-test-5be86c3e-d220-4538-ab6d-ae22d538dfde`）：GitHub ZMGID（`ca_1g4u93YydZsp`）+ Gmail `ohulercxm8@gmail.com`（`ca_ZnzYtlTeic0s`）。**不含** zhimeng63。
  - **`composio-zhimeng`**（用户 `zhimeng63`）：仅 Gmail `zhimeng63@gmail.com`（`ca_5jGHEthCoWuD`）。
  - (2026-10-09) 经用户同意，已从 composio-pg 删除旧的 zhimeng63 连接 **`ca_2rJjmKh8j1q0`**。新号/重建时**不要**再在 composio-pg（pg-test 用户）下给 zhimeng63 授权；只通过 composio-zhimeng 授权。
- (2026-10-08) **应用连接只走 Composio**：不要再装官方 GitHub（`cursor-github`）、Origin、Finance、Composio 插件（32661537）。
- **飞书例外（2026-10-10）**：Composio 无飞书 toolkit → 用官方 **lark-cli** 1.0.97（`npm i -g @larksuite/cli --prefix ~/.local`，brand `feishu`，app `cli_aa430b6809f85d0c`）。配置/token 在 `~/.lark-cli/` 与 `~/.local/share/lark-cli/`（明文不进仓库，加密在 `secrets/box-secrets.tgz.enc`）。换号后先解包试 `lark-cli auth status`，用户 token 约 7 天不用会过期；不行再 `lark-cli config init --new --brand feishu` 与 `lark-cli auth login`（用户扫码）。常用群见 `services/feishu-cli/chats.md`（全员群 / bot 通知群）。
- (2026-10-12) 晚上起 lark-cli 报「应用未启用」（错误 20069），bot 和用户身份都不通、用户 token 已被清：需要用户在飞书开发者后台重新启用应用并重新 `lark-cli auth login` 扫码。修好前早晚报的飞书部分会缺。
- **Gmail 来信监听（2026-10-10）**：盒子 `/workspace/gmail-listener/`（脚本备份在 `services/gmail-listener/`）经 Composio 触发器推送到小萌 webhook 例程 `gmail-new-mail`。密钥环境变量名 `GMAIL_WEBHOOK_KEY`（**值不进仓库**）。盒子无 systemd，**重启或换号后须手动** `/workspace/gmail-listener/start.sh`。另有 cloudpotato@mail.grokbot.com 邮箱触发例程。
- 同步方式：由专门 bot **仓库管家**每天约 03:14（北京时间）跑定时任务，把各 bot 的新记忆和设定同步进仓库，有变化才推送，推送前做密钥扫描。（2026-10-08 用户改口：原先「不单独建同步 bot、由主 bot 跑」已作废，移交给仓库管家。）
- 新号流程：匿名克隆 → 密码框填一次仓库口令 → 解密 Composio key、装 `composio-pg` + `composio-zhimeng` → 重建各 bot。`gh` 登录只在推送时需要。
- 不做公开分享模板（export-bot-template 只能生成公开模板，不用）。

## Grok Bot 自带邮箱（2026-10-10）
- (2026-10-10) 小萌为用户领了 Grok Bot 邮箱 **`cloudpotato@mail.grokbot.com`**。它绑定在**当前 Grok Bot 账号**上，**无法转移，换号后会丢失**，新号上也不能重新领回同一个地址（每个账号只能领一个，领了不能改）。
- 用途只限可丢弃的事：注册测试账号、收验证码、不重要的往来邮件。重要账号、账单一律留在用户自己的 Gmail。
- 小萌有一个只读的「cloudpotato 来信提醒」自动任务（来信即提醒用户，不回复、不删信），见 `bots/grok-bot/routines.md`。换号后该任务需按新号上的邮箱重建或删除。

## 近期重点（2026-10-14 晚）
- (2026-10-14) kivio：PR #64 修好 CI 并合入 main（`5b0c96f`），quality + windows-rust 都绿；#62、#63 仍开，新开 #65（技能商店 CSP 没放行）；PR #8/#15/#60/#61 仍挂着。
- (2026-10-14) Dsivio：当天约 12 笔提交（Windows/重试修复、竞品调研插件、Monid/Gecko 网关等），在 `e665f4c` 准备 v1.1.2（skip ci），Release 当晚未打完；修 windows-rust 的 PR #6 仍未全绿；官网仍 v1.1.0，别对外说已发 1.1.2。
- (2026-10-14) 飞书：应用已恢复、机器人身份通，只差用户本人扫码登录。
- (2026-10-14) composio-pg 新增了第二个 Gmail 连接（非 ohulercxm8），读信默认会落到它；用户决定两个都保留。要读 ohulercxm8 时注意指定连接。GitHub 仍是 ZMGID。
- (2026-10-14) 商品调研跑完收纳、假睫毛、化妆刷几批巴西 TikTok Shop 竞品表，并存成技能 `skills/tiktok/`（TikTok巴西站竞品调研）。
- (2026-10-14) 新旧两个 Grok Bot 账号以哪个为准、旧号定时任务停不停，用户仍未定；账号安全邮件（交易所、GitHub 第三方授权、Meta、Monid 新设备）仍待用户确认。

## 近期重点（2026-10-16 晚，旧号）
- (2026-10-16) kivio 发 v3.1.4（加手动 WebDAV 备份/恢复），main CI 全绿；Dsivio 当天无提交，PR #6 仍冲突。
- (2026-10-16) 本周两个主目标（kivio bot 模式、Rust SDK）整周零提交，bot 分支落后 main 56；下周要么留整块时间，要么正式改目标。
- (2026-10-16) 飞书 CLI bot 身份已 ready，用户身份仍要我在飞书里重新授权（`lark-cli auth login`）；Shopee 退货争议被驳回 4 个，补证据可二次申诉。

## 近期重点（2026-10-17 凌晨，新号）
- (2026-10-16) kivio 连发到 **v3.1.4**（CI / 打包都绿）；Dsivio main 仍绿，PR #6 仍 dirty 未处理；官网仍 v1.1.2。
- (2026-10-16) Shopee 巴西店有两笔「包裹未送达」退款分别在 10-16、10-17 截止，到晚上仍未处理；发货与退货还有积压。
- (2026-10-16 08:01) 我决定：grokbot-home 公开历史里误推的 `6766d7d` 先不强推清掉，box 上的 gh 登录也先保留（推送仍只走 Composio）。
- (2026-10-16) 键盘 / 踏板进展见上方「项目」；商品调研按我给的三张参考图做了 TikTok + Shopee 巴西两边的调研表。

## 近期重点（2026-10-16 凌晨，新号）
- (2026-10-15) **任何 PR 合并都要我明确同意**：代码工程师用自己设的轮询例程把 kivio #66 合进了 main（没等我点头），已认错并记下规则；所有 bot 都按这条来，CI 全绿也不能自己合。当天 15:35 我叫代码工程师停手，别再碰 kivio / Dsivio，等我吩咐。
- (2026-10-15 08:40) 搭建运维把官网 Dsivio 换成 v1.1.2 并部署，3 个安装包线上可下载；「新版本」区块的功能介绍还是 1.1.0 那版，要不要重写等我说。
- (2026-10-15 21:13) 小萌按我说的把官网服务器上的 CPA（cli-proxy-api）从 v7.3.13 升到 v8.0.29（升级前整目录备份在服务器上，可回退）；服务器整体健康，HTTPS 证书 12 月下旬到期；有两个端口直接对公网开放，要不要收紧还没定。
- (2026-10-15 晚) 新开 AI 编程键盘 / AI 脚踏板两个产品（见上方「项目」），新建 bot「测试工程师」和两个项目群。

## 近期重点（2026-10-15 晚）
- (2026-10-15) Dsivio：main CI 自 10/12 以来首次全绿（靠当天直接推 main 的 CI 修复，不是合 PR #6）；PR #6 已与 main 冲突，需 rebase 或关闭；官网显示 v1.1.2。
- (2026-10-15) kivio：main 质量/issue 推进明显（#66 合入，#62/#63/#65/#67 关闭）；但 bot 模式与 Rust SDK 本周仍零提交，bot 分支落后 main 43，周五需决定硬推还是挪到下周。
- (2026-10-15) Shopee 巴西店发货与退款时效是当前最紧的业务事项；飞书 CLI 连续第 5 天不可用，需用户在开发者后台重新启用应用并重新授权。

## 近期重点（2026-10-13 晚）
- (2026-10-13) Dsivio：当天无提交/无 PR/无 CI，main 仍红；干净 Windows 验收与 IM 真机联调已连续多日未做；官网产品页仍停在 v1.1.0，落后于已发的 v1.1.1。
- (2026-10-13) kivio：合并 PR #58、#59（含上下文超限恢复对应 #62，但 issue 仍 open）；翻译器与 CUA 相关改动进 main；下午修 Windows CI，quality 转绿、windows-rust 仍红。bot 模式分支 `codex/bot-development` 当天无新提交，落后 main 较多，合并成本上升；Rust SDK 标准仍无动静；外部 PR #61 仍等批 CI。
- (2026-10-13) 飞书 lark-cli 仍不通（应用「未启用」/用户 token 缺失），连续第 2 天；需用户在开发者后台重新启用并扫码授权。
- (2026-10-13) 新旧两个 Grok Bot 账号的仓库管家都在跑每日同步；agent-map 暂保留新号 id，旧号盒子按名字匹配快照，以哪边为准待用户或小萌决定。
- (2026-10-13) 新号上新建「商品调研」bot（单品调研、1688 成本、侵权禁售风险、做不做建议；虾皮日常选品仍归小枳）。用户目前在做巴西 TikTok Shop 选品：供货商香水目录、面膜/美容仪/洗脸刷等 SKU，竞品数据用 GeckoAPI（已买 Developer 套餐），Monid 查不了巴西站。
- (2026-10-13) 用户现在是 SuperGrok Plus（还剩约 3 个月），基本只用 Grok Bot；对 X 统一会员倾向先不转。

## 近期重点（2026-10-10 晚）
- (2026-10-10) 用户定下这几天的三条主线：① kivio（ZMGID/kivio）做 **bot 模式**，并加**版本检查**；② 给 kivio 的 AI 框架定一套 **Rust SDK 标准**；③ 推进 Dsivio：按运营同事日常高频工作写**插件**（先摸清运营日常、列插件候选清单再排序）。前两件用户自评都比较难。
- (2026-10-10) 用户发现 **Monid**（monid.ai）：把各类工具/数据接口集中到一个平台、一个预付余额统一付费（不含大模型；开源的只有 MIT 协议的接口定义和本地引擎）。用户觉得会很有用，待议两个想法：小额试用跑选品数据；借鉴思路给 Dsivio 做「一个 key 通吃」代理。均未决定，笔记在 box 的 `/workspace/assistant/ideas/monid-unified-api.md`。
