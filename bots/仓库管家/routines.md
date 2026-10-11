# 仓库管家的定时任务

## 1. 每日同步到 grokbot-home（daily-grokbot-sync）

- **触发**：每天 03:14（北京时间）。cron：`CRON_TZ=Asia/Shanghai 14 3 * * *`
- **状态**：本账号在用（2026-10-12 提示词按用户确认的「明文不进、加密包必进」更新）。
- **详细步骤**：见 `scripts/sync.md`，脚本 `scripts/sync.sh`（含 `scripts/pack-bundles.sh`）。
- **保存的提示词（重建时用 UpdateRoutine 创建）**：

```text
每日同步 grokbot-home：把本账号所有 bot 的新记忆、设定、技能、连接器清单和恢复所需材料同步到公开仓库 ZMGID/grokbot-home（本地 /workspace/grokbot-home），并做漂移检查。用户 2026-10-12 确认的规矩：明文不进、加密包必进。所有密钥和敏感数据只以 secrets/*.enc 加密形式入库（scripts/secret-crypt.py，GBH1，口令在环境变量 GROKBOT_HOME_PASSPHRASE），包括 box-secrets.tgz.enc、feishu-cli.tgz.enc、daily.tgz.enc、finance.tgz.enc 和 Composio key；任何明文密钥、口令、验证码、密码、一次性链接、webhook 地址、每日笔记、账本流水都绝不能进仓库。旧的私有仓库 ZMGID/grokbot-home-private-old 不要再往里推。口令现在偏短，用户换口令前不要动它。详细做法以仓库里的 scripts/sync.md 和 BOOTSTRAP.md 为准，先读它们。
1) 确保 /workspace/grokbot-home 是最新的，origin 指向 ZMGID/grokbot-home（git pull --rebase；目录不存在就匿名 git clone）。
2) 对 bots/agent-map.json 里的每个 bot（包括我自己 仓库管家，以及本账号新出现、还没登记的 bot）：读它自上次同步以来的对话记录和 /home/box/agent-data/agents/<id>/ 下的 profile.json、settings.json、memory/，把新的持久事实、项目进展、决定、偏好写成带日期的要点合并进 bots/<slug>/CONTEXT.md；设定变化写进 profile.md，定时任务变化写进 routines.md；关于用户本人、所有 bot 都该知道的写进根目录 CONTEXT.md。新 bot 要建 bots/<slug>/ 并登记到 agent-map.json、index.json、bots/README.md；空白未确认的 bot 先不登记，问小萌或用户。仓库公开，写进去的明文要当作谁都能看到，CONTEXT/摘要里不写金额、账号、密钥。
3) 小萌的笔记：/workspace/assistant/ 下的 routines.md、big-picture.md、ideas/ 以明文进 workspace/assistant/（按 sync.sh 的做法），daily/ 只以 secrets/daily.tgz.enc 加密入库；明文 /workspace/finance/ 只以 secrets/finance.tgz.enc 入库。
4) 漂移检查：把线上实际情况和仓库逐项对比并补齐：本账号现有的 bot 名单与 agent-map.json、index.json（sync.sh 在 id 对不上时按名字匹配，留意 id 变化要写回 agent-map）；每个 bot 的名字、标题、说明与 profile.md；每个 bot 的定时任务与 routines.md（我自己的看当前定时任务状态，别的 bot 读不到原文就在 Grok Bot 应用里发消息问那个 bot 要）；/home/box/agent-data/workflows/ 下的技能与 skills/；当前连接器状态与 connectors/README.md；已删除的 bot 要从仓库和 BOOTSTRAP 里去掉。
5) 运行 bash scripts/sync.sh：它会校验 remote 和分支，调用 scripts/pack-bundles.sh 用口令重打包所有加密包（缺口令就跳过打包、保留已有 .enc，并在结果里提一句），再做密钥扫描（scripts/secret-scan.sh），不通过就中止、不提交；通过且有变化才 commit 并推送（做法见 scripts/sync.md）。绝不绕过、放宽或改白名单来让扫描通过。
6) 结果发给这个聊天里的用户：没有变化就不发任何消息；有变化发一行中文说明（改了哪些 bot / 文件、补齐了哪些漂移）；密钥扫描失败、打包失败、拉取或推送失败等出错时，说清原因和需要用户做什么（只说文件名和行号，不贴可疑内容），并在 Grok Bot 应用里发消息抄送给 小萌（id 70869d39-bdf3-4146-823b-db0bd0d3da2c）。
```

如果每日同步要读别的 bot 的对话记录，需要有 ReadTranscript 工具（cursor 命名空间）。没有的话退而求其次：读 `/home/box/agent-data/agents/<id>/memory/` 和 `/home/box/agent-data/search-index.db` 的 `messages` 表（只读，先复制到 /tmp 再打开）。

## 2. 换号演练与安全审计

- **触发**：每周日 15:12（北京时间）。cron：`CRON_TZ=Asia/Shanghai 12 15 * * 0`
- **状态**：本账号在用（2026-10-12 提示词更新：演练须逐包 decrypt-check 全部 secrets/*.enc）。
- **保存的提示词（重建时用 UpdateRoutine 创建）**：

```text
每周换号演练与安全审计（公开仓库 ZMGID/grokbot-home，本地副本 /workspace/grokbot-home）。用户 2026-10-12 确认的规矩：明文不进、加密包必进。按我 profile 第 3、4 条做，只演练，不真建任何东西：
1) 换号演练：在 /tmp 下新建临时目录，不带任何登录凭证匿名克隆公开仓库，假装自己是新号上的 bot，按 BOOTSTRAP.md 从头空跑一遍（含 Step 0 各子步骤），逐步检查每一步引用的文件、脚本、命令和参数是否存在、是否和现状一致（不新建 bot、不建定时任务、不装连接器、不往盒子真实目录解包）。
2) 加密包逐个核对：对 secrets/ 下每一个 *.enc（至少 COMPOSIO_API_KEY.enc、COMPOSIO_API_KEY.box-current.enc、box-secrets.tgz.enc、feishu-cli.tgz.enc、daily.tgz.enc、finance.tgz.enc，以及新出现的），用环境变量 GROKBOT_HOME_PASSPHRASE 和 scripts/secret-crypt.py 解密（文本用 dec，tgz 用 dec-bin）：确认能解开、文本格式对、tgz 能列出文件清单且清单里有 BOOTSTRAP 恢复步骤需要的文件；再和盒子上的现状对比，确认包没有过期（例如缺了新加的凭据或目录）。解出的内容只放权限 600 的临时目录，只看文件名和格式，绝不打印内容、不记录、不写进任何文件或消息，核对完立刻删除。逐包记下结果（通过/解不开/缺文件/过期）。
3) 完整性：bots/agent-map.json 和 bots/index.json 里的每个 bot 都有完整的 profile.md、CONTEXT.md、routines.md，每条定时任务都有 cron 和提示词原文；setup.sh、scripts/pack-bundles.sh、scripts/sync.sh 能通过 bash -n；连接器和服务步骤（composio-pg、composio-zhimeng、gmail-listener、lark-cli 等）引用的文件都在。
4) 安全审计：对公开仓库的全部 git 历史和工作区跑 scripts/secret-scan.sh 和 gitleaks 全历史扫描，确认没有明文密钥、口令、验证码、一次性链接、webhook 地址、邮件正文、每日笔记明文、账本明文，secrets/ 下只有 README 和以 GBH1 开头的 .enc。检查遗留风险：旧私有仓库 ZMGID/grokbot-home-private-old 是否仍存在；口令是否仍然偏短（现在所有密钥包都在公开仓库里，短口令可被离线暴力破解，需要明确提醒）。只提醒，不替用户删仓库或改口令。
5) 发现断点就在 /workspace/grokbot-home 里修好（包过期就通过 bash scripts/sync.sh 重打包），推送前一律运行 bash scripts/sync.sh（密钥扫描不干净就中止，绝不放宽扫描或加白名单）；修不了的记下来。演练结束删除 /tmp 下所有临时目录和解密内容。
6) 结果发给这个聊天里的用户：全部正常就只发一句「本周演练通过」，遗留风险仍在时在同一句后面简短提醒；发现问题或出错时，用简短中文说清是什么问题（哪个包、哪一步）、已经修了什么、需要用户做什么（只说文件名和行号，不贴可疑内容），并把同样的内容在 Grok Bot 应用里发消息抄送给 小萌（经理 bot，id 70869d39-bdf3-4146-823b-db0bd0d3da2c）。
```
