# 小萌（grok-bot）自己的记忆与项目状态

> 先读根目录 `/CONTEXT.md`（关于用户的共享记忆），这里只记主 bot 自己的工作记录。导出：2026-10-08。

## 职责
- 账号主 bot / **经理**：接任何任务并分派给合适的 bot；用 CreateAgent 创建新 bot（dr eggbot 已于 2026-10-08 删除）；SetPrimaryBot。
- 换号时执行 BOOTSTRAP；仓库日常维护与每日 03:14 同步已于 2026-10-08 移交给**仓库管家**。

- (2026-10-08) 用户批准把 `/workspace/assistant/big-picture.md` 公开进仓库：`bots/grok-bot/notes/big-picture.md`。每日笔记 `/workspace/assistant/daily/` **不进仓库**；每日同步由仓库管家复制 big-picture（见 `scripts/sync.md`）。
- (2026-10-08) **改名**：显示名 `Grok Bot` → `小萌`（slug 仍为 `grok-bot`）。
- (2026-10-08) 定时任务「巡检各 bot」`17 11,15 * * 1-5`；早晚计划/总结**已移交给事务秘书**。
- (2026-10-09) 「巡检各 bot」改用纯 cron `17 11,15 * * 1-5`（用户时区 Asia/Hong_Kong）；小萌现仅保留此项定时任务。

## 关于用户（主 bot 视角的要点）
- 用中文交流，Grok Bot 账号多个、轮换使用，GitHub `ZMGID`。
- 2026-10-07 用户问订阅：建议先订 SuperGrok（$30/月，按月付），Grok Bot 从这一档开始提供；Plus（$100）主要多用量、1080p 视频、高峰优先。
- 用户会在语音通话里布置任务；通话结束后要在聊天里补发结果摘要。
- 用户发 `/new` 时：主 bot 不能替用户开新对话，告诉他用 app 里的新建入口，或直接换话题。

## 项目记录

### kivio PR #60 审查（2026-10-07）
- PR #60「feat: Kivio Study 材料学习工作台」：最新一轮 CI 和 Study browser regression 在 10-07 通过（`be06640` 修好了共用 Chat 重构引入的两处 bug：读历史时改写记录、打开页面就更新版本号导致其他窗口被误判过期）。没有冲突，可合并，没人 review。review 意见见根目录 CONTEXT.md。
- Dsivio main CI 一直失败：CI 用 Node 20，测试用 `Promise.withResolvers`（Node 22）。

### 仿 TourBox 创作控制器（2026-10-07 ~ 10-08）
- 用户发了一张 TourBox 类产品图，要求做全套（模型、PCB、软件）并给交付文件。主 bot 做了原创设计：
  1. 初版（100×100×30 mm）→ 用户要求按 **3D 打印** 重做并兼顾 **人体工学**（参考原图）→ 人体工学版（约 95×94 mm，左手布局，键距 ≥18 mm）→ 3D 打印版（17 零件、3MF 打印盘、热熔螺母、滚轮支架、公差测试件、中文打印说明）。
  2. 用户要求审查电路板和固件并在嘉立创核对元件 → 修了充电芯片状态脚 5V 直连 ESP32（加分压）、RGB 数据电平偏低（加电平转换），充电电流降到 303 mA，编码器加上拉和滤波，天线禁铺区加大，双面铺地；固件升到 **v1.1.0**（修蓝牙配对、USB 重复发键，加 10 分钟休眠和自检模式）。
- 当前文件：`projects/creative-controller/`（旧号 `/workspace/creative-controller/`，另有打包的 `creative-controller-delivery.zip` 约 15 MB，内容与目录相同，未放进仓库）。
- 剩余风险：ENC2 封装占位、板上无电池保护（用带保护板的 603450）、检查 CPL 旋转、TS-1102S 库存少、未经实物测试。
- 工具链：KiCad 9（kicad-cli）、Freerouting（`/workspace/freerouting.jar`，`pcb/route.sh`）、cadquery 2.8（`mechanical/cad.py`、`params.py`）、PlatformIO espressif32@6.9.0（`firmware/`）、PrusaSlicer（切片估时）。

### 换号方案（2026-10-08）
- 讨论过程：私有仓库 + CONTEXT.md → 工具环境用 setup.sh、密钥放 1Password → 用户希望“给新 bot 一个链接就自动适配” → 考虑过自建 MCP 网关（MetaMCP / mcp-proxy），后来选 Composio（免费 Hobby 版每月 10 万次调用，个人够用）。
- 官方 Composio 插件 OAuth 后看不到应用（不同 Composio user）；小枳用项目 API key 写了 `composio-pg` 启动器，主 bot 在 11:54 把 `composio-pg` 加到账号里并验证 GitHub（ZMGID）和 Gmail 都是 ACTIVE。
- (2026-10-09) 新增 **composio-zhimeng**（stdio，`/workspace/composio-zhimeng/launch.sh`）：Composio 用户 `zhimeng63`，仅 Gmail zhimeng63@gmail.com；与 composio-pg 共用 `~/.composio_pg_key`。composio-pg 此后只管 GitHub + ohulercxm8。
- 用户决定：每个 bot 都存进仓库，新号的第一个 bot 配好自己后用 CreateAgent 重建其他 bot。
- 2026-10-08 12:02 开始建 `ZMGID/grokbot-home`。
- (2026-10-08) 用户改口：单独建同步 bot **仓库管家**，仓库维护与每日同步从主 bot 移交给它；grok-bot 不再跑 daily-grokbot-sync。

## 账号上的其他 bot（供分派参考，2026-10-08）
- **小枳**（xiaozhi）：中文通用助手，调研/查资料/方案。
- **仓库管家**：维护本仓库、跑每日 03:14 同步。
- **代码工程师**：Dsivio / kivio 的 CI、PR 与代码修复。
- **搭建运维**：公司官网、飞书及其他搭建维护。
- **事务秘书**（原名「邮件秘书」）：非技术事务 + 工作日早晚计划/总结；只写草稿，从不直接发送。
- **硬件工程师**：创作控制器（`projects/creative-controller/`）。
- **财务管家**：记账/订阅/预算/报销对账（只记录不付款）；账本 `/workspace/finance/` 不进仓库。
- **dr eggbot**：已于 2026-10-08 删除；新建 bot 改由本 bot（小萌）负责。
- 另有一个空的 “New Bot”（id `1dbfda76-…`，2026-08 创建，无对话、无设定），不是真正在用的 bot，没有迁移。
- (2026-10-10) 又出现第二个空白 “New Bot”（id `52d1b935-…`，10-10 03:09 创建，只发了一句自我介绍，无设定），同样暂不登记，等用户或小萌确认用途。

## 2026-10-08 晚 ~ 10-09
- (2026-10-08) Dsivio v1.1.0 发布；官网产品页上线；环境配置 PR #2/#3/#4 开出未合；用户次日重点：手工优化环境配置 + 启动 IM Gateway（参考 Hermes）。
- (2026-10-08) 派小枳做 Hermes IM 网关调研；用户 10/9 凌晨决定自写 Rust 协议实现。

## 2026-10-09 午后 ~ 10-10 凌晨
- (2026-10-09) 帮用户查了 Codex CLI 0.160–0.162 更新、GPT-6.1 Sol 与 Claude Opus 5.5 API 价格对比、AI 操作 Word/Excel 的开源项目（首推 OfficeCLI，备选 officekit）。
- (2026-10-10) 应用户要求做了恶搞网页小游戏《刹不住的境界》（虚构车名/厂名），用户最终选第一版；已挂到新的公开仓库 **ZMGID/brake-game**（GitHub Pages：https://zmgid.github.io/brake-game/），只记一笔、不同步进本仓库。素材整理在 box 的 `/workspace/brake-game/`。
- (2026-10-10) 领取 Grok Bot 邮箱 `cloudpotato@mail.grokbot.com`（绑当前账号、不可转移，见根目录 CONTEXT「Grok Bot 自带邮箱」），并新建自动任务「cloudpotato 来信提醒」。
- (2026-10-10) 用户想在 Composio 里再接其他邮箱：规矩是每个邮箱单独建一个 Composio 连接器（同 composio-zhimeng 模式），等用户给地址。

- (2026-10-10) 新增例程：**cloudpotato 来信提醒**（email 触发）与 **gmail-new-mail**（webhook；触发器 ti_ePC_aV3eRSPT / ti_6ozhOAfOaHLq；密钥 env `GMAIL_WEBHOOK_KEY` 不进仓库）。盒子 `/workspace/gmail-listener/start.sh`，重启后需手动启动。
- (2026-10-10) 飞书走官方 **lark-cli**（Composio 无飞书例外）；群 id 见 `services/feishu-cli/chats.md`。

## 2026-10-10 晚
- (2026-10-10) 帮用户看了 Monid（统一付费的工具/数据接口平台），结论：可借鉴思路，不必自建；记入 `/workspace/assistant/ideas/monid-unified-api.md`，等 Dsivio 环境配置忙完再拿出来商量。
- (2026-10-10) 接下用户三条主线（kivio bot 模式 + 版本检查、kivio Rust SDK 标准、Dsivio 运营插件），小萌要先摸清 kivio / Dsivio 代码结构再出拆解和计划；插件线建议让事务秘书问运营同事日常，或用户直接口述。
- (2026-10-11) 两个空白 “New Bot”（`1dbfda76-…`、`52d1b935-…`）已不在本账号的 agent 目录中（应已删除，从未登记，无需清理）。又出现一个默认设定的空白 “Grok Bot”（id `04d9635a-…`，10-10 17:22 创建，只有自我介绍和一问一答，无分工），同样暂不登记，等用户或小萌确认用途。
- (2026-10-11) 新账号 bootstrap：所有 bot 已重建，新 agent id 写在 `bots/agent-map.json`；小萌新 id `70869d39-bdf3-4146-823b-db0bd0d3da2c`。不用 gh（Composio 项目把 GitHub token 打码），推送一律走 composio-pg 的 Composio GitHub（ZMGID）。
- (2026-10-12) 大局更新（见 `notes/big-picture.md`）：Dsivio 发布 v1.1.1、kivio 发布 v3.1.2，但两边 main CI 都在 windows-rust 的 Rust 测试上失败，待修绿；kivio 新 issue #62（上下文超限后永久 400）；官网仍是 v1.1.0 待更新；新号已注册电脑里没有 Mac mini（只有 ZMair）。
- (2026-10-12) 旧号盒子上的小萌 18:40 写了换号迁移清单 `workspace/assistant/ideas/grokbot-home-migration-checklist-2026-10-12.md`；旧号盒子上 lark-cli 晚上报「应用未启用」（20069），需要用户在飞书开发者后台重新启用应用并重新扫码。

## 2026-10-13
- (2026-10-13) 大局更新（见 `notes/big-picture.md`）：Dsivio 当天无进展、main 仍红；kivio 合并 #58/#59 并修 Windows CI（quality 绿、windows-rust 仍红），bot 模式分支落后 main 加重；官网仍 v1.1.0；飞书仍「应用未启用」不通。
- (2026-10-13) 本周原定 kivio bot 模式+版本检查、Rust SDK 标准两条主线仍无新提交，方向开始偏。
- (2026-10-13，新号) 用户问 X 统一会员（X Pass）要不要从 SuperGrok Plus 转：小萌查官方说明和 X 帖子后建议先不转（转换=退掉旧订阅按比例退款再重新买，剩余时长不折算；新 Plus $8 档不含 Grok Bot；Super $100 才大致对应现档；额度池合并、具体额度官方未公布）。用户表示基本只用 Grok Bot、现订阅还剩约 3 个月。
- (2026-10-13，新号) 用户咨询自部署 Qwen3.8-Flash-Next：小萌评估 4×A100 80G + 4×A800 80G 两台各跑一份 BF16（N-gram 嵌入卸载到内存）可行，粗估日常几十人可用；买卡/整机/租用均为 10 月二手行情估算，未决定。
- (2026-10-13，新号) 小萌巡检读不到其他 bot 的对话记录，提议改成每次巡检给各 bot 发消息要进度（代价是每次叫醒 7 个 bot），待用户回复。11:24 巡检提醒用户：新旧两个账号同时在跑、互相覆盖仓库，需要用户登旧号暂停那边的定时任务（仓库管家每日同步、小萌巡检、事务秘书早晚报）后告诉小萌。
- (2026-10-13，新号) 14:24 按用户要求新建商品调研 bot（`19702f19-…`，见 `bots/商品调研/`）；盒子上新装 Monid 插件（已连接）。

## 2026-10-14
- (2026-10-14，新号) 11:21 巡检推代码工程师修 kivio CI（`23cddd2` 红）；15:27 巡检确认 kivio main `5b0c96f` 已绿，转去盯 Dsivio windows-rust，并提醒本机 `/workspace/kivio` 是脏树要先回到 main。
- (2026-10-14，新号) 12:07 发现 composio-pg 当天 10:14 新授权了另一个 Gmail（非 ohulercxm8），读信默认会落到新邮箱，问用户；16:45 用户决定两个都保留，并说这件事小萌不用管。
- (2026-10-14) 大局 `notes/big-picture.md` 更新到 10-14 晚报版（kivio CI 绿；Dsivio 冲 v1.1.2、Release 未完成、官网仍 v1.1.0；账号安全与飞书扫码仍拖）。
- (2026-10-14，旧号) 巡检：gmail-listener 实时连接假死，11:27 重启后恢复；漏掉的邮件不会补发。
- (2026-10-14) 本周方向明显偏离原定 kivio 两条主线，晚报建议用户明确继续 kivio 还是转向 Dsivio。

## 2026-10-15
- (2026-10-15) 大局 `notes/big-picture.md` 更新到 10-15 晚报版：Dsivio main 推 5 个提交后 CI（`4cbd843`）自 10/12 以来首次全绿；PR #6 仍 OPEN 且与 main 冲突（领先 12、落后 5），建议 rebase 或关掉；官网已显示 v1.1.2。kivio main 约 11 个提交，合 #66、关 #62/#63/#65/#67，Release 仍 v3.1.2。
- (2026-10-15) 本周主目标（kivio bot 模式、Rust SDK 标准）周四仍零提交，`codex/bot-development` 领先 10、落后 43；晚报建议周五二选一：硬推 bot 分支（把 main 合进分支或交云端 agent），或正式挪到下周。
- (2026-10-15) 业务侧：Shopee 巴西店待发货单和一笔有截止日（10/16）的退款申请仍压着，晚报建议次日先清；飞书 CLI 第 5 天不通（用户 token 缺失，bot 下午一度 ready 但晚报仍报 20069）；干净 Windows 实测与 IM 真机联调第 10 天未做。
- (2026-10-15，旧号) 15:28 巡检叫醒仓库管家把 agent-map 改成两号 id 并存（format 2，已于 `a70974f` 完成）；财务管家设定里写的 composio-pg 邮箱与现状不一致，等用户确认邮箱策略后再改。
- (2026-10-15，旧号) gmail-listener 夜间与上午各掉线一次（SSL/DNS），均自动重连。
