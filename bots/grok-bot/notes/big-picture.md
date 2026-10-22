# 大局（2026-10-08 初始化，2026-10-21 18:10 更新）
## 身份
跨境电商小公司唯一的 AI 经理兼 agent 开发。主项目 Dsivio（ZMGID/Dsivio），另管 kivio、官网、各种搭建、飞书等杂事。
## 进行中
- Dsivio：10/21 无提交，main `4cbd843` CI 绿，PR #6 仍冲突（最后更新 10/14），官网 v1.1.2（10/21 核实）。以下为 10/20：10/20 无提交，main `4cbd843` CI 绿，PR #6 仍冲突（最后更新 10/14），官网 v1.1.2（10/20 核实）。以下为 10/19：10/19 无提交，main 仍 `4cbd843`（CI 绿），PR #6 仍冲突，官网 v1.1.2（10/19 核实）。以下为 10/16：10/16 无提交、无新 Release，main 仍 `4cbd843`（CI 绿），PR #6 仍冲突（最后更新 10/14），官网仍 v1.1.2（10/16 核实）。以下为 10/15：10/15 main 推 5 个提交（吉祥物/composer、市场 catalog、CI 可移植断言与 Windows 主线程栈）；最新 main CI（`4cbd843`）全绿（quality / windows-rust / runtime-launchers-windows，已核实）——自 10/12 以来首次转绿。PR #6 仍 OPEN，相对 main 冲突（领先 12、落后 5），未合。官网已显示 v1.1.2（10/15 核实）。干净 Windows 实测、IM 真机联调第 10 天未做。以下为 10/14 状态：10/14 一次推上 main 12 个提交（Monid+GeckoAPI 工具网关、平台竞品调研插件、agent 重试统一+Windows 稳定、markdown 货币修复、去掉 macOS Vision OCR、Impeccable 设计工具），带 [skip ci]；v1.1.2 于 10/14 18:26 正式发布。
- kivio：10/21 上午 5 个提交（Study 可选包、扩展市场、WebDAV CI、证书依赖、发版准备），**v3.1.5 已发**（约 11:35）；最新 tip `f4af3f0`（CI 取消无失败），上一绿 `f083330`；#27 已关；开着的 PR #61/#15/#8；bot 分支领先 10、落后 **106**；main 仍有 `mimo-v2.5-pro`（各 8 处，已核实）。以下为 10/20：10/20 零提交；Release 仍 v3.1.4（#68 修复第二天未发版），#27 仍 OPEN，bot 分支领先 10、落后 59；main 仍有 `mimo-v2.5-pro` 引用。以下为 10/19：10/19 修 #68（PR #69 合并、issue 关）+ `03c5279` 修 ZIP 安全告警，main CI 绿；修复未发版（仍 v3.1.4）；#27 仍 OPEN 未回复；bot 分支领先 10、落后 **59**。以下为 10/16：10/16 main 12 个提交（WebDAV 手动备份/恢复、聊天停止与插话、UI、模型价格、CI 缓存），**v3.1.4 已发**（17:05），最新 `46e5cfe` CI 全绿（中途 88cc822 红过已修）。issue #27（WebDAV）仍 OPEN 待回复关闭。bot 分支领先 10、落后 **56**，本周零提交。以下为 10/15：10/15 main 约 11 个提交（CSP 放行 ClawHub、备份保留用户文件、侧栏更新图标、去掉旧 connectors、skills 缓存/重载、rustls #66、运行时扫描性能）；#62/#63/#65/#67 已关；#66 已合。最新 `ac721f4` CI 仍在跑（未核实最终）；上一轮完整绿是 `19b71b6`。bot 分支 codex/bot-development 领先 10、落后 43，bot 模式/Rust SDK 仍无新提交。开着的 PR #61/#60/#15/#8 均与 main 冲突。Release 仍停在 v3.1.2（10/12）。
- 官网（10/21 核实：页面显示 v1.1.2）（https://eastforceglobal.com/dsivio/，自己服务器上的 nginx 静态站）：由搭建运维负责。
- 飞书：10/21 用户 token 仍缺失（第 9 个工作日）。以下为 10/20：用户 token 仍缺失（第 8 个工作日）。以下为 10/19：10/19 用户 token 仍缺失（10/16 起算已第 7 个工作日）。以下为 10/16：bot 身份 ready，用户 token 仍缺失，第 6 天。运营选品群、公司手册知识库、审批精简、多维表格未做。
- grokbot-home 迁移仓库：已公开，密钥加密，仓库管家负责同步、演练和审计。
- bot 体系：10/8 搭好（代码工程师、搭建运维、事务秘书、硬件工程师（备用）、小枳、仓库管家）。
- 硬件（新号）：10/20 陪伴机器人定版 BE70r3（头 Ø50、底座 Ø70、高约 80），键盘外壳定稿 v5.8 B、固件 1.1.0，两者都未下单打样；新号补了测试工程师测试重点。依据 grokbot-home 同步记录，未核实。10/21 白天巡检未见新硬件产出。以下为 10/19：10/19 AI 脚踏板废弃（群解散、文件归档）；AI 陪伴小机器人立项（xiaozhi-esp32，小萌任产品经理，新建结构工程师、电子工程师和「AI陪伴机器人」群）；AI 编程键盘继续。依据 grokbot-home 同步记录，产出未核实。
- 创作控制器（类 TourBox）：只是测试，已停止，不再跟进。
## 风险 / 注意
- Dsivio IM 改动曾直接推 main；后续改动建议走 PR。PR #6 分叉悬挂，需 rebase 或关闭。
- 环境配置未在干净 Windows 上验收；IM 真机联调未做（第 10 天）。
- grokbot-home-private-old 仍存在（10/10 核实，含明文 Composio 密钥），密钥轮换未核实。
- 10/10 凌晨有 Devin 获得 ChatGPT 套餐额度授权、X 账号验证码和密码重置邮件，待用户确认是否本人操作。
- 小米 MiMo V2.5 系列已于 10/21 10:00 下线；两个仓库 main 仍引用 `mimo-v2.5-pro`（10/21 晚核实各 8 处），选到会报错，需尽快迁到 V2.6 或下掉预设。
- vm-01 号池为空、请求 503（搭建运维汇报）；工作经费余额不足、11/8 续费可能不够（金额见财务账本；财务管家汇报）。
- grokbot-home 加密口令只有 6 位数字（用户已知情并选择保留）。
- kivio bot 模式分支落后 main 越来越多（10/21：领先 10、落后 106，连续第二周零提交），合并成本在涨。
- 主线变多：kivio 主目标、Dsivio 收尾、AI 编程键盘、AI 陪伴机器人四线并行，主目标持续没时间。
- Shopee 巴西店待发货与退款时效（店铺邮箱即 composio-pg 当前 Gmail 连接；10/21 未读邮件很多，含大量待发货；两笔免退货退款已批；螃蟹玩具 4 款断货；有一条圣保罗 Face ID 登录待确认；订单号见每日笔记）。
- composio-pg 当前 Gmail 是 Shopee 店铺那个邮箱（非 ohulercxm8）；ohulercxm8 现可通过 user-Composio 读取（10/21 核实）；邮箱策略仍待用户最终确认。
- 10/15 zhimeng63：Bybit 异常地区登录通知；GitHub 给 dsivio-marketplace 新增公钥——待用户确认是否本人。
- 飞书 CLI 用户身份连续第 9 个工作日不可用（用户 token 缺失；bot 身份 ready）。
- 10/20 zhimeng63：Notion 美国新设备登录、GitHub 新授权 Instabox / Freebuff、Google 登录 agentmail.to、Cursor 授权、Figma 登录——待用户确认是否本人。
- 10/13–14 起若干账号安全邮件（Meta/Facebook、Reason Machines、sub2api、Cursor App、Bybit）仍待用户确认。
- 10/21 GreenCloud 紧急内核维护：约 22:00 上海时间起，预计 15–40 分钟，影响 web-api-relay-ca（邮件称无需用户操作）；维护后需确认服务是否恢复。
- 10/20–21 ohulercxm8：Composio 授权、Windows 新登录、OpenAI 东京登录——待确认是否本人。

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

- 10/19 记录（周一）：上午修完 kivio #68 和 ZIP 安全告警，之后 GitHub 无动静（Mac 未连接，本地情况未知）；bot 模式和 Rust SDK 第二周仍零提交、落后 59；硬件砍脚踏板、立项陪伴机器人。Shopee 售后处理情况仍未核实。建议本周尽快对主目标做去留决定。

- 10/20 记录（周二）：两个仓库全天零提交，早上 5 件计划能核实的都没落地（Shopee、kivio v3.1.5、bot 模式定调、MiMo 迁移、PR #6）；可见动静是陪伴机器人定版 BE70r3 和几个新工具注册。Mac 未连接。主目标第二周周二仍未起步，四线并行排不下，需要用户明天定去留；MiMo 10/21 10:00 下线最急。

- 10/21 记录（周三）：kivio 发 v3.1.5（扩展市场 + Study 拆包等），计划 5 件只做成发版这一件；MiMo 已下线但预设未迁；bot 分支落后拉到 106；Dsivio 仍静；Shopee 邮件继续堆。本周过半，主目标仍零进展，需要尽快定去留。

## 新号补充（新号 10-22 17:55 晚报版的独有内容，已去敏）
- （10/22 晚报核实）**kivio v3.1.6 已发布**（10/22 01:09 北京时间，tip `2fb4bb18`，输入法回车、笔记行号配色修复）；open PR #8/#15/#61。Dsivio 10/22 上午 4 个提交（Pi 子代理、媒体工具），tip `103a5ca2` macOS 过、Windows 被取消，前两次 Windows 失败；PR #6 仍 CONFLICTING/DIRTY；官网仍 v1.1.2（curl 核实）。
- AI 编程键盘：样机未下单，当天无新核实。陪伴机器人：保持暂停采购，无新活。商品调研：无今日新表（巡检旁证）。
- 风险：Shopee 第六个工作日未处理（新增待发货、一笔钱包调整被拒，详见每日笔记）；Dsivio Windows CI 连续失败；Temu 卖家邮箱验证码邮件需确认是否本人；一个域名 30 天后到期（自动续费）；composio-pg 的 Gmail 当前连的不是记忆里的那个邮箱；Mac mini 不在已注册电脑，ZMair/BF 离线；vm-01 号池与工作经费未重核（见账本）。
- 本周方向：10/22（周四）kivio 再发 v3.1.6，Dsivio 回到加新功能；Shopee / 账号确认 / PR #6 仍没清。周五建议：Shopee → Dsivio Windows CI + PR #6 → 账号确认。
- 仍待：账号安全确认（Shopee Face ID、GitHub 第三方授权、Notion 新设备登录、Google 登录提醒、AgentMail 测试及更早的 Bybit/Meta/Monid 等）；飞书应用未启用、用户 OAuth 缺；grokbot-home 新旧账号以谁为准仍等用户定。
