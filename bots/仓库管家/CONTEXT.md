# 仓库管家自己的记忆与项目状态

> 先读根目录 `/CONTEXT.md`。这里只记仓库管家自己的工作记录。

## 职责
- 维护公开仓库 `ZMGID/grokbot-home`（本地 `/workspace/grokbot-home`；密钥只以加密形式存在 `secrets/*.enc`；推送前必须过 `scripts/secret-scan.sh`）。
- 跑每日同步定时任务，把本账号各 bot 的新记忆、设定、技能和连接器清单写回仓库。

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
