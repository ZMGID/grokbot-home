# CONTEXT.md（关于我的共享记忆）

> 所有 bot 共用。换到新的 Grok Bot 账号后，每个 bot 都先读这个文件，再读自己的 `bots/<名字>/CONTEXT.md`。
> 最初由旧号主 bot 在 2026-10-08 导出，之后由每日同步任务维护。时间一律是北京时间（Asia/Shanghai，UTC+8）。
> 写回规则：关于“我”的、所有 bot 都该知道的事写这里；只跟某个 bot 的职责有关的写进它自己的 CONTEXT.md。

## 关于我
- 用中文交流；回答要直接、简短，先给结论。不喜欢绕远路——我说了要用某个方式做（例如“用 Composio 看 GitHub”），就按那个方式做，不要另起炉灶。
- 时区 Asia/Shanghai（UTC+8）。
- 有好几个 Grok Bot 账号，轮换着用，希望换号的成本尽量低（这个仓库就是为此建的）。
- GitHub 账号：`ZMGID`（显示名 ZhiMeng）。个人仓库约 16 公开 + 5 私有，主项目 kivio；还是组织 `dsh-external` 的成员（约 184 个 DSH 相关私有仓库）。
- 邮箱：`ohulercxm8@gmail.com`、`zhimeng63@gmail.com`（都通过 Composio `composio-pg` 接入）。
- 常用本地 CLI：Claude Code、Codex、Pi、OpenCode、DSH。
- 评估别人的仓库时更看重 git 时间线和 AI 痕迹，不看功能清单。
- 在做虾皮（Shopee）巴西站选品调研，打算用 agent + Playwright + Shopdora（虾多拉）插件做自动化，而不是紫鸟浏览器（详见 `bots/xiaozhi/CONTEXT.md`）。
- 订阅建议（2026-10-07）：主要用 Grok Bot，建议先订 SuperGrok（$30/月，按月付），不够再升 Plus。

## 项目

### kivio（ZMGID/kivio）
- Tauri 2 + React/Vite/TS 前端 + Rust 后端的桌面 AI 助手，约 585 star。另有仓库 `Dsivio`、`dsivio-plugins`、`dsvideo-plugin`、`fkmem`（Pi 的运行时记忆）。
- **PR #60「feat: Kivio Study 材料学习工作台」**（分支 `feat/kivio-study-cloud`，草稿状态）：2026-10-07 20:48 的提交 `be06640` 修好了 Study browser regression；之后（10-07 20:49 那一轮）CI 和 Study browser regression **全部通过**，没有冲突，还没人 review。
- PR #60 的 review 意见：PR 太大（102 个文件、8000+ 行），建议把共用 Chat 的重构拆成单独 PR；迁移旧数据时判断冲突是直接比较两段 JSON 文本，字段顺序一变就可能误判；浏览器测试运行时联网下载真实 PDF，可能随机失败，建议缓存；Rust 测试 `antigravity.rs:497` 有一个不稳定的 OAuth 回调端口检测；工作流里 Node 20 的 actions 已弃用；ChatPanel 测试少一个 mock。
- kivio `main` 9-24 到 10-06 也有 CI 失败（最近一次 10-06 14:05），原因还没细查。
- 其他老 PR：#15「修复 external-agent 会话恢复」（7 月停着）、#8「Linux AppImage 适配基线」（6 月草稿）。

### Dsivio（ZMGID/Dsivio）
- `main` 分支 CI 从 9 月底起每次推送都失败（最近：10-07 22:50 推送「add built-in Ziniao daily report plugin」）。
- 原因：CI 配置 `node-version: 20`，而测试（`ProductArchivePage.test.tsx`、`CopyUploadField.test.tsx`）用了 `Promise.withResolvers`（Node 22 才有）。3231 个前端测试只挂这 2 个，但导致后面的 Rust 测试被跳过。
- 修法：CI 改成 Node 22，或者那两个测试别用 `Promise.withResolvers`。已提议提 PR，我还没回复。

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

- **Grok Bot**（主 bot / 经理）：分派任务给其他 bot，并负责用 CreateAgent **创建新 bot**；工作日早晨计划（含双 Gmail 未读摘要）与晚间总结。
- **小枳**：中文通用助手，调研、查资料、方案与代码仓库审查辅助。
- **仓库管家**：维护公开仓库 `ZMGID/grokbot-home`，每天 03:14（北京时间）跑同步。
- **代码工程师**：盯 `ZMGID/Dsivio`（主）与 `ZMGID/kivio` 的 CI / 开着的 PR，修代码并开修复 PR；GitHub 只走 composio-pg。
- **搭建运维**：公司官网、飞书及其他系统/工具的搭建与维护。
- **邮件秘书**：经 composio-pg 处理两个 Gmail；查信、整理、起草回复与待办跟进。**只写草稿，从不发送。**
- **硬件工程师**：创作控制器项目（`projects/creative-controller/`：外壳、PCB、固件、软件、BOM）。

（2026-10-08 用户已删除 **dr eggbot**；原先「设计并创建 bot」改由 Grok Bot 自己做。）

## 换号方案（2026-10-08 已确认）
- 所有东西放进 GitHub 仓库 `ZMGID/grokbot-home`（2026-10-08 起改为**公开**，旧私有仓库改名为 `grokbot-home-private-old`）：共享记忆（本文件）、每个 bot 的设定/记忆/定时任务（`bots/`）、连接器清单和启动脚本（`connectors/`）、技能（`skills/`）、工具环境脚本（`setup.sh`）、项目文件（`projects/`）。
- 新号流程：打开一个 Grok Bot，对它说「按 https://github.com/ZMGID/grokbot-home 配置你自己」。它按 `BOOTSTRAP.md` 配好自己，再用 CreateAgent 把其他 bot 全部建出来。
- **明文密钥永远不进仓库**。唯一例外：Composio key 用 `scripts/secret-crypt.py` 加密后放 `secrets/*.enc`；解密口令 `GROKBOT_HOME_PASSPHRASE` 只通过 bot 的密码框（secret prompt）提供。
- Composio 的 GitHub / Gmail 连接统一走自定义连接器 **`composio-pg`**（Composio 测试用户 `pg-test-5be86c3e-d220-4538-ab6d-ae22d538dfde`），不在官方 Composio 插件里重新授权。
- (2026-10-08) **应用连接只走 Composio**：不要再装官方 GitHub（`cursor-github`）、Origin、Finance、Composio 插件（32661537）。新应用一律在 Composio 控制台给上述测试用户授权，经 `composio-pg` 使用。
- 同步方式：由专门 bot **仓库管家**每天约 03:14（北京时间）跑定时任务，把各 bot 的新记忆和设定同步进仓库，有变化才推送，推送前做密钥扫描。（2026-10-08 用户改口：原先「不单独建同步 bot、由主 bot 跑」已作废，移交给仓库管家。）
- 新号流程：匿名克隆（公开仓库不需要登录）→ 密码框填一次仓库口令 → bot 解密 Composio key、装 composio-pg → 重建各 bot。`gh` 登录只在推送时需要（优先用 Composio 的 GitHub token，设备码备用）。官方连接器授权不再需要。
- 不做公开分享模板（export-bot-template 只能生成公开模板，不用）。
