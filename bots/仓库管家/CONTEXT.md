# 仓库管家自己的记忆与项目状态

> 先读根目录 `/CONTEXT.md`。这里只记仓库管家自己的工作记录。

## 职责
- 维护公开仓库 `ZMGID/grokbot-home`（本地 `/workspace/grokbot-home`；密钥只以加密形式存在 `secrets/*.enc`；推送前必须过 `scripts/secret-scan.sh`）。
- 跑每日同步定时任务，把本账号各 bot 的新记忆、设定、技能、连接器清单和恢复用加密包写回仓库（`pack-bundles.sh` → `secrets/*.enc`）。

## 记录
- (2026-10-08) 用户创建本 bot（agent id `5eed9f49-92c0-49b7-8327-2128e99b910b`）。
- (2026-10-08) 用户要求主 bot（Grok Bot）把本仓库的维护（含每日同步）移交给仓库管家；仓库管家已接手。
- (2026-10-08) 在本账号创建定时任务「每日同步 grokbot-home」，cron `CRON_TZ=Asia/Shanghai 14 3 * * *`（每天 03:14 北京时间）。详细做法见 `scripts/sync.md`，脚本 `scripts/sync.sh`。
- (2026-10-08) 每周「换号演练与安全审计」已创建，cron `CRON_TZ=Asia/Shanghai 12 15 * * 0`（周日 15:12）。

## 规矩
- 公开仓库，密钥只以加密形式存在 `secrets/*.enc`（`scripts/secret-crypt.py`，口令在环境变量 `GROKBOT_HOME_PASSPHRASE`）。明文密钥、口令、验证码、密码、一次性授权链接绝不进仓库；推送前必须跑密钥扫描，不干净就中止。旧仓 `ZMGID/grokbot-home-private-old` 不要再往里推。
- 没有变化就不发消息；有变化发一行中文说明改了哪些 bot / 文件。
- 出错时说清原因（只说文件名和行号，不贴可疑内容）。
- (2026-10-09) 每日同步 03:14：合并小枳 IM Gateway 调研与 Dsivio/官网进展进 CONTEXT；刷新 `bots/grok-bot/notes/big-picture.md`；跳过空白 New Bot；connectors 核对（composio-pg ACTIVE；GetMcpServerStatus 不可用，改用命名空间目录）。

- (2026-10-10) 每日同步 03:14：记录小萌领取的 Grok Bot 邮箱 cloudpotato（不可转移）及其来信提醒任务、新仓库 ZMGID/brake-game；合并各 bot 10-09 午后以来进展；第二个空白 New Bot（`52d1b935-…`）暂不登记。

- (2026-10-11) 每日同步 03:22：记录用户近期三条主线与 Monid 想法（根 CONTEXT）、小萌与小枳 10-10 晚进展（Rust 框架调研、kivio 复查）；刷新 big-picture；两个空白 New Bot 已从账号消失，新空白 “Grok Bot”（`04d9635a-…`）暂不登记；GetMcpServerStatus 仍不可用，改用命名空间目录核对连接器。
- (2026-10-11) 新号起不用 gh / git push：推送改走 composio-pg 的 Composio GitHub（ZMGID）。原因：本 Composio 项目会把 GitHub access token 打码，gh 登录用不了。做法见 `scripts/sync.md`。
- (2026-10-11) 账本改为每次 sync 重打包加密进 `secrets/finance.tgz.enc`（`enc-bin`）；明文 `/workspace/finance/` 仍不进工作树。财务管家 memory 有内容时另写 `secrets/财务管家-memory.tgz.enc`。BOOTSTRAP 换号时用 `dec-bin` 恢复。
- (2026-10-12) 用户确认规矩「明文不进、加密包必进」。每日同步与周日演练提示词已更新：sync 必跑 `pack-bundles.sh`；演练对每个 `secrets/*.enc` 做 decrypt-check（只看文件名/格式，不落明文到仓库）。
- (2026-10-12) 用户明确表示口令**不换**，且不想再被提醒：以后同步、演练、汇报里都不要再建议换口令（只在用户主动提起时再谈）。
- (2026-10-13) 新号盒子上 `/workspace/assistant/daily/` 只剩 10-12，lark-cli 用户登录文件也不在，重新打包的 `daily`、`box-secrets` 包会比仓库里的旧包少文件，所以这两个包没覆盖仓库里的完整版。`pack-bundles.sh` 修了一处：会话里没有 COMPOSIO_API_KEY 等环境变量时沿用 box 上的 `~/.grokbot-home/secrets.env`，不再把它从包里丢掉。各 bot 的 raw/profile.json 快照仍不提交（新号头像被重置，描述多了一句 bootstrap 提示）。
- (2026-10-12) 旧号上本 bot 的 description 03:22 改版（重打包加密包、演练逐包解密、口令不换不再提醒），profile.md 与周日演练原文 10-13 补齐。
- (2026-10-13) 发现新旧两个账号的仓库管家都在 03:14 跑每日同步、都往本仓库推（新号 03:35 先推，旧号随后 rebase）。两边各有一个小萌在改 big-picture，会互相覆盖；旧号这次保留了新号推上来的 big-picture 与 box-secrets 包，只补进旧号独有的内容（10-12 每日笔记加密包、迁移清单、飞书 20069 故障、本 bot 设定）。哪个账号为准、旧号的定时任务要不要停，等用户或小萌定。

- (2026-10-14) 每日同步 03:26：刷新 big-picture（10-13 晚报版，去掉公开仓不宜出现的具体金额）、补 10-13 每日笔记加密包；agent-map 仍用新号 id（本旧号盒子按名字匹配 raw 快照）；空白默认 Grok Bot `04d9635a-…` 仍不在账号、不登记；连接器核对：composio-pg / composio-zhimeng / Origin / x 可用，cursor-github 与 Finance 为 needsAuth（不用），本账号另有 user-Composio ready。
- (2026-10-14，新号) 每日同步 03:33：旧号已在 03:26–03:30 先推过一次（含 box-secrets 包先缩小后恢复）；新号补登记新 bot「商品调研」（agent-map、index.json、bots/README、BOOTSTRAP），新号空白默认「Grok Bot」`79d40bdd-…` 不登记；连接器清单补 Monid（新号已连接），并把状态行改为新旧两号分开写。
- (2026-10-14，新号) 03:40 同步后问用户以新号还是旧号为准、另一边的同步停不停，截至 10-15 凌晨未回复。新号线上本 bot 的 description 当天改版（推送改写成走 composio-pg 的 GitHub；去掉口令偏短的提醒；去掉首轮 bootstrap 提示），`profile.md` 已补。
- (2026-10-15，新号) 每日同步 03:21：补各 bot 10-14 进展、新技能 `skills/tiktok/`、composio-pg 第二个 Gmail 连接；big-picture 刷新到 10-14 晚版（去掉金额、第三方邮箱地址和口令位数）；但把 box-secrets/daily 包压小了。
- (2026-10-15，旧号) 每日同步 03:24：rebase 到新号 03:21 提交后，恢复完整 box-secrets（16 项）与含 10-14 的 daily 加密包；agent-map 仍保留新号 id（本旧号按名字匹配 raw）；空白默认 Grok Bot 仍不登记；连接器核对见 connectors/README（composio-pg 现有两个 Gmail，用户 10-14 决定都保留）。
- (2026-10-15) `agent-map.json` 改为 format 2：两号 id 并存（键=各号小萌 id）；本号校正后不再被他号扁平 map 覆盖。商品调研仅他号。
- (2026-10-16，旧号) 每日同步 03:14：big-picture 刷新到 10-15 晚版（公开副本去掉第三方邮箱地址与退款单号）；补小萌 10-15 要点与根 CONTEXT「近期重点（10-15 晚）」；本号 8 个 bot 与 agent-map format 2 一致，无新 bot、无技能、连接器状态无变化。本号 search-index 自 10-12 起未再更新，对话改以 memory 与小萌笔记为准。

- (2026-10-15，新号) 03:23 每日同步被一张 Auto-review 审批卡卡住，已请用户处理（经小萌早上转告）。
- (2026-10-16，新号) 每日同步 03:33：旧号已在 03:18 先推了一次。新号补登记新 bot「测试工程师」（agent-map 仅他号、index.json、bots/README、BOOTSTRAP），新增「群聊」登记（AI编程键盘、AI脚踏板）；补各 bot 10-15 进展与根 CONTEXT 新项目「AI 编程键盘 + 脚踏板」。**意外**：本 box 上 git 的 GitHub 凭据助手（gh）已可用，`sync.sh` 里的 `git push` 直接推上去了（`6766d7d`），把本号较旧的 big-picture 和缺 3 天的 daily 包也带了上去；随即用 composio-pg 提交恢复这两个文件的完整/去敏版，并把 `sync.sh` 改成不再 `git push`（一律退出码 5 后走 Composio）。各 bot raw/profile.json 这次是本号版本（两号互相覆盖，只差小萌 id 与头像，等用户定主号）。键盘 / 踏板设计文件（约 435 MB，商业产品）没进公开仓库，等用户定。
- (2026-10-17，旧号) 每日同步 03:14：先拉齐他号 10-16 03:33/03:35 的两个提交（测试工程师登记、sync.sh 不再 git push）。big-picture 刷新到 10-16 晚版（公开副本去掉店铺邮箱地址与退款单号）；补小萌 10-16 要点与根 CONTEXT「近期重点（10-16 晚）」；连接器清单记下旧号新出现的 Finance（needsAuth）。本号 8 个 bot 与 agent-map 一致，无新 bot、无用户技能；本号对话 store 读不到新记录（search-index 停在 10-12），以小萌笔记为准。重打包后 box-secrets（缺他号写入的官网 v1.1.2 部署记录）和 feishu-cli（少一个文件）比仓库版旧，按规矩保留仓库版；finance 内容未变不改；gmail-listener `run_loop.sh` 保留他号加了读取 secrets.env 的新版；daily 包新增 10-16。
- (2026-10-16 08:01) 用户决定：公开历史里的 `6766d7d` 先不强推清掉，本盒 gh 登录也先保留；推送仍只走 Composio。
- (2026-10-17，新号) 每日同步 03:2x：rebase 到旧号 03:20 的提交上。按小萌 10-16 11:26 的通知同步硬件工程师、测试工程师新 description 到 `profile.md`；补各 bot 10-16 进展与根 CONTEXT「近期重点（10-17 凌晨，新号）」；big-picture 以旧号 10-16 晚版为主，追加「新号补充」一节（去掉退款单号、邮箱、金额）；daily 加密包改为两号合并（旧包全保留，新号不同的同日笔记存为 `<日期>.新号.md`，规则写进 sync.md）；setup.sh 补装 opencv-python-headless；bot 名单与 agent-map 一致，无新技能，连接器状态与 10-16 相同。
- (2026-10-18，新号) 每日同步 03:2x：10-17 白天本号几乎无对话，只补小萌 10-17 14:27 踏板铰链 Φ10 建议。漂移检查无差异（bot 名单、设定、技能、连接器同 10-17）；本盒 daily 包和 big-picture 没有新内容，保留仓库里合并版，不提交缩小的 daily 包；raw/profile.json 两号版本不同，设定没变就不来回覆盖。
- (2026-10-19，新号) 每日同步 03:1x：10-18 本号没有新对话可读（搜索索引最新仍是 10-17）。漂移检查：bot 名单、设定、技能、连接器均无差异；补齐本 bot `routines.md` 第 1 条，改为新号线上实际保存的每日同步提示词原文（旧号 10-12 版留作参考）。本盒 daily 包和 big-picture 没有新内容，保留仓库里的合并版；raw 快照不改回新号设定。
- (2026-10-19，旧号) 每日同步 03:2x：rebase 到新号 03:20 提交上。本盒 10-18 起没有新对话（搜索索引最新仍是 10-12），各 bot profile/settings 未变。漂移修正：本 bot `routines.md` 第 1 条折叠里的 10-12 版其实是本号（小萌 a96070f7…）线上在用的原文，改正说明并把抄送小萌的 id 改回本号 id；两号提示词不同、都在用。bot 名单、技能、连接器与 10-17 相同；本盒重打的加密包（daily 变小）、big-picture、raw 快照、env-snapshot 保留仓库版。
- (2026-10-20 11:22，新号) 按小萌巡检通知，实时把测试工程师线上新 description（陪伴机器人定版 BE70r3、键盘 v5.8 B / 固件 1.1.0 等）同步进 `bots/测试工程师/`（`4b7de35`，走 Composio）。
- (2026-10-22，新号) 03:14 每日同步因账号额度用尽没跑成，15:2x 补跑：rebase 到旧号 03:19 的 `1b75f6e` 上。本盒搜索索引和各 bot transcript 为空、memory/ 不存在，读不到 10-21 以来的对话，只按小萌 big-picture 补记。big-picture「新号补充」换成 10-21 去敏版。daily 包补上本盒 10-20、10-21（存成 `<日期>.新号.md`，旧包全留）；10-22 当天笔记未完，留到下次。漂移检查无差异。
- (2026-10-23，旧号) 每日同步 03:1x：本盒 10-22 20:16 前后被整体重建（文件时间全是那一刻；`/home/box/agent-data/workflows/` 为空、pip 包变旧、各 bot profile 回到本号版本、composio-pg 的 venv 丢失）。按 setup.sh 第 8 步重建 `/workspace/composio-pg/.venv`（composio 0.25.0）后 composio-pg / composio-zhimeng 恢复连接。工作树里 `projects/creative-controller/mechanical/out/` 被删成未暂存改动，已从 git 还原。daily 包合并加入旧号 10-22（只有早报和巡检），旧包全留；big-picture、raw 快照、env-snapshot、box-secrets/feishu-cli/finance 包、gmail-listener `run_loop.sh` 保留仓库版。连接器与 10-17 旧号状态一致，技能与 bot 名单无变化。
- (2026-10-23，新号) 每日同步 03:2x：rebase 到旧号 03:2x 的 `25b4280` 上。本盒搜索索引和各 bot transcript 仍为空、memory/ 不存在，只按小萌 big-picture 补记。big-picture「新号补充」换成 10-22 去敏版；小萌 CONTEXT 记新号 10-22 晚报；daily 包加入本盒 10-22（`2026-10-22.新号.md`，旧包全留）。漂移检查：bot 名单、设定、技能、定时任务无差异。
- (2026-10-24，旧号) 每日同步 03:1x：本盒搜索索引停在 10-23 03:17、各 bot transcript 和 memory/ 无新内容，只按小萌笔记补记。daily 包合并加入旧号 10-23（旧包全留）；big-picture 换成 10-23 版并去敏（Shopee 邮箱、订单号去掉），「新号补充」保留；小萌 CONTEXT 记旧号 10-23 晚报。raw 快照、env-snapshot、box-secrets/feishu-cli/finance 包（账本内容无变化）、gmail-listener `run_loop.sh` 保留仓库版。bot 名单、技能（本盒 workflows 仍为空）、定时任务无变化。
- (2026-10-24，新号) 每日同步 03:2x：rebase 到旧号 03:2x 的 `876eecc` 上。本盒搜索索引和 transcript 仍为空，只按小萌 big-picture 补记。big-picture「新号补充」换成 10-23 去敏版；小萌 CONTEXT 记新号 10-23 晚报。本盒 10-23 daily 合进加密包这一步又被 Auto-review 拦下，仓库 daily 包保持原样，新号 10-23 笔记暂未备份。漂移检查：bot 名单、设定、技能、定时任务、连接器无差异。
- (2026-10-27，旧号) 每日同步 03:2x：10-24、10-25 无新内容未提交。本次 big-picture 换成 10-26 版并去敏（店铺邮箱、订单号、买家名去掉），「新号补充」保留；小萌 CONTEXT 记旧号 10-26 晚报；daily 包合并加入旧号 10-26（旧包全留）。bot 名单、设定、技能、定时任务、连接器无变化。
