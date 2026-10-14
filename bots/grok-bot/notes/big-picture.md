# 大局（2026-10-08 初始化，2026-10-14 17:58 更新）
## 身份
跨境电商小公司唯一的 AI 经理兼 agent 开发。主项目 Dsivio（ZMGID/Dsivio），另管 kivio、官网、各种搭建、飞书等杂事。
## 进行中
- Dsivio：10/14 一次推上 main 12 个提交（Monid+GeckoAPI 工具网关、平台竞品调研插件、agent 重试统一+Windows 稳定、markdown 货币修复、去掉 macOS Vision OCR、Impeccable 设计工具），最后一个是「release: prepare v1.1.2 [skip ci]」，main 这批提交没跑 CI；v1.1.2 草稿，Release 构建 17:58 仍在跑未核实。PR #6（fix/ci-windows-rust）修 Windows CI，前 3 次红、第 4 次在跑。干净 Windows 实测、IM 真机联调第 8 天未做。以下为 10/13 状态：10/13 无提交、无 PR、无 CI，main 仍红；干净 Windows 实测、IM 真机联调第 6 天未做。以下为 10/12 状态：10/12 14:21 发布 v1.1.1（7 个 Windows 运行时/CI 修复，Release CI 绿，已核实）；main CI windows-rust 连续 4 次红。干净 Windows 实测、IM 真机联调仍未做（第 4 天）。以下为更早状态：10/10 17:07 本地 main 与远端合并后直接推上 main（925d3b6，含飞书+企微 IM 集成、离线电脑控制工具和当天 5 个 IM/UI/定时任务修复），main CI 绿（已核实）；未走 PR。干净 Windows 实测、IM 真机联调仍未做。以下为 10/9 状态：10/8 发布 v1.1.0。10/9 合并 PR #1（Node 22）、#5、#3、#4（内置 Python/Node 运行时 + 国内镜像），#2 关闭，无 open PR。main CI 10/9 15:21 首次转绿，但合 #3/#4 后的 CI 被取消，最新提交 2c32892 未核实。Mac 本地 main 有 5 个未推送提交（含飞书+企微 IM 集成、离线电脑控制工具），与远端分叉（多 5 少 17），另有 16 个未提交改动（插件出表用内置环境）。干净 Windows 实测未做。
- kivio：10/14 12:27 合并 PR #64（修 models catalog/retry 后的 CI），main CI 全绿（5b0c96f，已核实）；当天无其他提交。bot 分支 codex/bot-development 仍停在 10/12，落后 main 31；Rust SDK 未见；issue #61/#62/#63/#65 都 0 回复（#65：v3.1.2 技能商店 CSP 没放行 clawhub.ai）。以下为 10/13 状态：10/13 合并 PR #58、#59，上下文超限恢复（对应 #62，但 issue 仍 open 无回复）、翻译器 18 语言、CUA 改 Skill+CLI 进 main；下午修 Windows CI，a3c0e6b quality 转绿、windows-rust 仍红，17:38 cb94497 在跑未核实。bot 模式在分支 codex/bot-development（10/11–10/12 共 10 个提交，10/13 无新提交，落后 main 26 个）；Rust SDK 标准未见动静；PR #61 仍等批 CI。以下为 10/12 状态：10/12 发布 v3.1.2（凌晨+上午共 14 个修复提交，Release CI 绿，已核实）；main CI windows-rust 红。外部 PR #61（模型库远程更新）等批 CI 和 review；新 issue #62（超上下文后永久 400 的死锁，质量高）。10/10 定的 bot 模式+版本检查、Rust SDK 标准两大目标 10/12 在 GitHub 上无动静。以下为更早状态：10/9 上午 7 个修复提交，main CI 绿（10/9 13:59）。PR #60「Kivio Study 材料学习工作台」草稿，10/7 后无进展；#15、#8 老 PR 挂着。
- 官网（10/14 17:58 核实：页面仍是 v1.1.0，落后 v1.1.1，v1.1.2 在打）（https://eastforceglobal.com/dsivio/，自己服务器上的 nginx 静态站）：10/8 已上线 v1.1.0 页面，安装包放在自己服务器上的 /dsivio/downloads/v1.1.0/。由搭建运维负责。
- 飞书：10/14 仍报 20069「应用未启用」、用户 token 缺失，第 3 天。10/13 仍不通（用户 token 缺失，应用「未启用」），第 2 天。10/12 晚 lark-cli 报「应用未启用」（错误 20069），bot 和用户身份都不通，用户 token 已被清，需要用户重新启用应用并重新授权。10/10 用 lark-cli 接好（王枳萌身份），建了全员群和 bot 通知群；运营选品群、公司手册知识库、审批精简、多维表格未做。
- grokbot-home 迁移仓库：已公开，密钥加密，仓库管家负责同步、演练和审计。
- bot 体系：10/8 搭好（代码工程师、搭建运维、事务秘书、硬件工程师（备用）、小枳、仓库管家）。
- 创作控制器（类 TourBox）：只是测试，已停止，不再跟进。
## 风险 / 注意
- Dsivio IM 改动已直接推 main 且 CI 绿，但没经过 review；后续改动建议走 PR。
- 环境配置未在干净 Windows 上验收。
- grokbot-home-private-old 仍存在（10/10 核实，含明文 Composio 密钥），密钥轮换未核实。
- 10/10 凌晨有 Devin 获得 ChatGPT 套餐额度授权、X 账号验证码和密码重置邮件，待用户确认是否本人操作。
- 小米 MiMo V2.5 系列 10/21 10:00 下线，如有使用需迁到 V2.6。
- vm-01 号池为空、请求 503（搭建运维汇报）；工作经费余额约 769 元，11/8 续费不足（财务管家汇报）。
- grokbot-home 加密口令只有 6 位数字（用户已知情并选择保留）。
- 两个仓库 main 的 windows-rust 都红（10/12），release 分支绿，main 信号失效。
- zhimeng63 的 Bybit 10/12 00:41、09:43 两笔内部转账（金额见财务账本）（iOS），待用户确认。
- 10/13 zhimeng63：Bybit 受限地区登录通知、Bybit Pay 收到一笔 USDT（金额见财务账本）、GitHub 第三方 OAuth 应用 sub2api 获授权、Google Pay 新增卡片，待用户确认是否本人。
- kivio bot 模式分支落后 main 越来越多，合并成本在涨。（10/13 18:40 核实：codex/bot-development 领先 10、落后 26，分支改了 269 个文件，main 那 26 个提交改了 229 个，两边重叠 109 个文件，集中在 chat/agent、chat/model、chat/commands、external_agents/session、settings。rebase 不是小活，建议改成把 main 合进分支一次解决冲突，或交给云端 agent 先做。另：kivio main cb94497 CI 仍红，quality 绿、windows-rust 红。）
- Dsivio main 自 10/12 无绿 CI，10/14 的 12 个提交跳过 CI 直接推 main，v1.1.2 在未验证的 main 上打包。
- 10/14 起 composio-pg 的 Gmail 连接变成 qq290657442@gmail.com（QQ 290657442@qq.com 转发进来，含 Shopee 巴西店 valebaibai 订单和赵远洪的 12306 通知），ohulercxm8 不再被读，待用户确认是否有意。
- 10/13 晚 zhimeng63 出现 Facebook 新账号、Meta 登录码和找回码，Reason Machines OAuth 授权，GitHub App Cursor 第 3 次申请权限，待用户确认。

## 本周方向
- 10/8 约一半时间投入 bot 和迁移基础设施；之后应回到 Dsivio 质量（CI 变绿）。

- 10/8 记录：Dsivio 新方向：① 环境配置优化（同事电脑装环境太费时间，已开 PR #2/#3/#4，10/9 用户手工继续优化，当天最重要）；② IM Gateway（接入消息平台），参考 Hermes。

- 10/9 记录：环境配置 PR 全部合入，IM 网关本地第一版完成（未推送）。下周初：推送 + main CI 转绿 → 干净 Windows 验收 → IM 真机联调。

- 10/10 记录：IM 网关推上 main 并转绿。下个工作日：干净 Windows 验收 → IM 真机联调 → 安全收尾。

- 10/12 记录：本周主攻 kivio bot 模式+版本检查、Rust SDK 标准；周一实际全花在两个项目的修复发版上，主目标未起步。

- 10/13 记录：上午 kivio 质量提升有效，下午又花在 Windows CI；周二过完 bot 模式和 Rust SDK 标准都没新提交，本周方向开始偏。

- 10/14 记录：白天主要在 Dsivio（12 个提交、v1.1.2 发版准备、Windows CI），kivio 只修绿了 CI；周三过完 bot 模式和 Rust SDK 仍零提交，本周方向明显偏离，需要用户明确是继续追 kivio 还是转向 Dsivio。
