# grok-bot 自己的记忆与项目状态

> 先读根目录 `/CONTEXT.md`（关于用户的共享记忆），这里只记主 bot 自己的工作记录。导出：2026-10-08。

## 职责
- 账号主 bot，接任何任务并分派给合适的 bot；管理其他 bot（CreateAgent / SetPrimaryBot）。
- 维护 `ZMGID/grokbot-home`：换号时执行 BOOTSTRAP，每天 03:17 同步所有 bot 的记忆和设定。

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
- 用户决定：每个 bot 都存进仓库，新号的第一个 bot 配好自己后用 CreateAgent 重建其他 bot；不建单独的同步 bot，由主 bot 每日同步。
- 2026-10-08 12:02 开始建 `ZMGID/grokbot-home`。

## 旧号上的其他 bot（供分派参考）
- **小枳**（xiaozhi）：中文通用助手，调研/代码审查/GitHub 和邮件巡检/插件方案设计；composio-pg 是它接通的。
- **dr eggbot**（dr-eggbot）：设计并创建高质量 Grok Bot；用户要新 bot 时交给它。
- 另有一个空的 “New Bot”（id `1dbfda76-…`，2026-08 创建，无对话、无设定），不是真正在用的 bot，没有迁移。
