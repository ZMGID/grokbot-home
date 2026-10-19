# 大局（2026-10-08 初始化，2026-10-16 18:00 更新）
## 身份
跨境电商小公司唯一的 AI 经理兼 agent 开发。主项目 Dsivio（ZMGID/Dsivio），另管 kivio、官网、各种搭建、飞书等杂事。
## 进行中
- Dsivio：10/16 无提交、无新 Release，main 仍 `4cbd843`（CI 绿），PR #6 仍冲突（最后更新 10/14），官网仍 v1.1.2（10/16 核实）。以下为 10/15：10/15 main 推 5 个提交（吉祥物/composer、市场 catalog、CI 可移植断言与 Windows 主线程栈）；最新 main CI（`4cbd843`）全绿（quality / windows-rust / runtime-launchers-windows，已核实）——自 10/12 以来首次转绿。PR #6 仍 OPEN，相对 main 冲突（领先 12、落后 5），未合。官网已显示 v1.1.2（10/15 核实）。干净 Windows 实测、IM 真机联调第 10 天未做。以下为 10/14 状态：10/14 一次推上 main 12 个提交（Monid+GeckoAPI 工具网关、平台竞品调研插件、agent 重试统一+Windows 稳定、markdown 货币修复、去掉 macOS Vision OCR、Impeccable 设计工具），带 [skip ci]；v1.1.2 于 10/14 18:26 正式发布。
- kivio：10/16 main 12 个提交（WebDAV 手动备份/恢复、聊天停止与插话、UI、模型价格、CI 缓存），**v3.1.4 已发**（17:05），最新 `46e5cfe` CI 全绿（中途 88cc822 红过已修）。issue #27（WebDAV）仍 OPEN 待回复关闭。bot 分支领先 10、落后 **56**，本周零提交。以下为 10/15：10/15 main 约 11 个提交（CSP 放行 ClawHub、备份保留用户文件、侧栏更新图标、去掉旧 connectors、skills 缓存/重载、rustls #66、运行时扫描性能）；#62/#63/#65/#67 已关；#66 已合。最新 `ac721f4` CI 仍在跑（未核实最终）；上一轮完整绿是 `19b71b6`。bot 分支 codex/bot-development 领先 10、落后 43，bot 模式/Rust SDK 仍无新提交。开着的 PR #61/#60/#15/#8 均与 main 冲突。Release 仍停在 v3.1.2（10/12）。
- 官网（10/15 17:58 核实：页面显示 v1.1.2）（https://eastforceglobal.com/dsivio/，自己服务器上的 nginx 静态站）：由搭建运维负责。
- 飞书：10/16 bot 身份 ready，用户 token 仍缺失，第 6 天。运营选品群、公司手册知识库、审批精简、多维表格未做。
- grokbot-home 迁移仓库：已公开，密钥加密，仓库管家负责同步、演练和审计。
- bot 体系：10/8 搭好（代码工程师、搭建运维、事务秘书、硬件工程师（备用）、小枳、仓库管家）。
- 创作控制器（类 TourBox）：只是测试，已停止，不再跟进。
## 风险 / 注意
- Dsivio IM 改动曾直接推 main；后续改动建议走 PR。PR #6 分叉悬挂，需 rebase 或关闭。
- 环境配置未在干净 Windows 上验收；IM 真机联调未做（第 10 天）。
- grokbot-home-private-old 仍存在（10/10 核实，含明文 Composio 密钥），密钥轮换未核实。
- 10/10 凌晨有 Devin 获得 ChatGPT 套餐额度授权、X 账号验证码和密码重置邮件，待用户确认是否本人操作。
- 小米 MiMo V2.5 系列 10/21 10:00 下线，如有使用需迁到 V2.6。
- vm-01 号池为空、请求 503（搭建运维汇报）；工作经费余额不足、11/8 续费可能不够（金额见财务账本；财务管家汇报）。
- grokbot-home 加密口令只有 6 位数字（用户已知情并选择保留）。
- kivio bot 模式分支落后 main 越来越多（10/16：领先 10、落后 56，整周零提交），合并成本在涨。
- Shopee 巴西店待发货与退款时效（店铺邮箱即 composio-pg 第二个 Gmail 连接；两笔退款申请 10/16、10/17 截止，处理状态未核实；10/16 有 4 个退货争议因证据不足被驳回，可补证据二次申诉）。
- composio-pg 当前默认读到的是第二个 Gmail 连接（`ca_JwThbeIld_Jw`，非 ohulercxm8）；ohulercxm8 不在连接器上（用户尚未最终确认邮箱策略）。
- 10/15 zhimeng63：Bybit 异常地区登录通知；GitHub 给 dsivio-marketplace 新增公钥——待用户确认是否本人。
- 飞书 CLI 用户身份连续第 6 天不可用（用户 token 缺失；bot 身份 10/16 已 ready）。
- 10/13–14 起若干账号安全邮件（Meta/Facebook、Reason Machines、sub2api、Cursor App、Bybit）仍待用户确认。

## 本周方向
- 10/8 约一半时间投入 bot 和迁移基础设施；之后应回到 Dsivio 质量（CI 变绿）。

- 10/8 记录：Dsivio 新方向：① 环境配置优化（同事电脑装环境太费时间，已开 PR #2/#3/#4，10/9 用户手工继续优化，当天最重要）；② IM Gateway（接入消息平台），参考 Hermes。

- 10/9 记录：环境配置 PR 全部合入，IM 网关本地第一版完成（未推送）。下周初：推送 + main CI 转绿 → 干净 Windows 验收 → IM 真机联调。

- 10/10 记录：IM 网关推上 main 并转绿。下个工作日：干净 Windows 验收 → IM 真机联调 → 安全收尾。

- 10/12 记录：本周主攻 kivio bot 模式+版本检查、Rust SDK 标准；周一实际全花在两个项目的修复发版上，主目标未起步。

- 10/13 记录：上午 kivio 质量提升有效，下午又花在 Windows CI；周二过完 bot 模式和 Rust SDK 标准都没新提交，本周方向开始偏。

- 10/14 记录：白天主要在 Dsivio（12 个提交、v1.1.2 发版准备、Windows CI），kivio 只修绿了 CI；周三过完 bot 模式和 Rust SDK 仍零提交，本周方向明显偏离，需要用户明确是继续追 kivio 还是转向 Dsivio。

- 10/15 记录：Dsivio main CI 终于转绿，kivio 质量/issue 推进明显，但 bot 模式和 Rust SDK 周四仍零提交、分支落后 43；工程时间花得值，本周主目标仍未落地。周五需二选一：硬推 bot 分支，或正式挪到下周。

- 10/16 记录（周五 / 本周回顾）：kivio 发 v3.1.4 并加 WebDAV 备份，Dsivio 当天无提交。本周 kivio 56 提交、3 个版本，Dsivio 29 提交、2 个版本、main 转绿；但 bot 模式和 Rust SDK 整周零提交，分支落后 56。下周需要给主目标留整块时间，或正式改目标。

## 新号补充（新号 10-19 17:55 晚报版的独有内容，已去敏）
- （10/19 晚报核实）Dsivio 当天无提交，官网仍 v1.1.2，PR #6 仍冲突未合。kivio #68 已由 PR #69 修复合并，另合 ZIP 依赖安全修复（CI 成功），**v3.1.5 未发**，Release 仍 v3.1.4，待发版并回复 issue。
- AI 编程键盘：10/19 17:00 用户宣布第一版收尾（外壳 v5.8 B 光环版、固件 1.1.0），全套文件已打包交用户；样机未下单。AI 脚踏板：10/19 11:38 老板废弃，群与仓库已标记，文件归档不动。
- AI 陪伴小机器人：10/19 立项（小萌任产品经理），T7-S3 + 1.28 寸 GC9A01。底座先后经历 S 版 Ø76（老板嫌大）、NT 版 Ø70.6（电池建模错误作废）；19:02 定 **Ø70 + 402535 小电池**，详图已过小萌审核；固件到 v0.3.4（未实测）；样件清单未下单。
- 商品调研：10/19 交了枕头表定价和 ABC Space 清单的 TikTok 巴西竞品表（定价公式见商品调研 CONTEXT）。
- 风险：Shopee 退款、退货和发错货连续两个工作日没人处理（详见每日笔记）；kivio 修了没发版；机器人应先定电池和体积再画壳；zhimeng 那个 Gmail 有新的设备登录提醒待用户确认，Copilot 审查额度已用完；composio-pg 的 Gmail 当前连的不是记忆里的那个邮箱；小米 MiMo V2.5 系列 10/21 下线；工作经费见账本。
- 本周方向：10/19（周一）原定先还欠账（Shopee、PR #6、kivio #68），实际只修了 kivio #68，大部分时间给了陪伴机器人；周二建议先 Shopee 后台，再 kivio v3.1.5，再机器人样件拍板。
- 仍待：账号安全确认（Bybit / GitHub OAuth / Meta / Monid / X↔Grok）；飞书应用未启用、用户 OAuth 缺；Mac mini 不在已注册电脑；grokbot-home 新旧账号以谁为准仍等用户定。
