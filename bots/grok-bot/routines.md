# grok-bot 的定时任务

## 1. 每日同步到 grokbot-home（daily-grokbot-sync）——已移交

- **状态**：**已移交给仓库管家**（2026-10-08）。grok-bot 不再跑此任务。
- **规范提示词与重建说明**：见 `bots/仓库管家/routines.md`。
- **详细步骤**：见 `scripts/sync.md`，脚本 `scripts/sync.sh`。

## 2. 早上：今日计划

- **触发**：工作日 08:53（北京时间）。cron：`CRON_TZ=Asia/Shanghai 53 8 * * 1-5`（启用）
- **状态**：本账号在用。提示词取自 `/workspace/assistant/routines.md`（2026-10-08；是否把 assistant 其它笔记同步进仓库仍待用户决定，**未**把 `daily/` 或 `big-picture.md` 拷进本仓）。
- **保存的提示词（重建时用 UpdateRoutine 创建）**：

```text
每个工作日早上给用户（中文沟通）做今日计划，并附上未读邮件摘要。用户是一家跨境电商小公司唯一的 AI 经理兼 agent 开发，主项目是 Dsivio（GitHub ZMGID/Dsivio），也负责 kivio、公司官网、各类搭建、飞书等杂事。

1. 读 /workspace/assistant/big-picture.md 和 /workspace/assistant/daily/ 下最近几天的文件（尤其是昨天的「今日总结」和「明天建议」）。
2. 看 GitHub（账号 ZMGID，用 gh 或 composio-pg 连接器的 GitHub）：开着的 PR 和它们的 CI、main 分支挂掉的 CI、新 issue、待处理的 review。
3. 未读邮件：通过 composio-pg 连接器的 Gmail，查看两个账号 ohulercxm8@gmail.com 和 zhimeng63@gmail.com 最近（大约过去一天，周一覆盖周末）的未读邮件。按重要程度归纳：需要用户回复或处理的放最前，注明发件人和一句话要点；通知、推广、自动邮件合并成一句带过。只读，不标已读、不回复、不删除，不把邮件里的验证码、密码或密钥写进摘要。某个账号连不上就说明一下，继续其他部分。
4. 写今日计划：3–5 件按优先级排好的事，每件附一句理由；一句本周大方向；卡住或拖着的事项。邮件里需要处理的事可以排进计划。
5. 把计划和邮件摘要以「## 今日计划」写入 /workspace/assistant/daily/YYYY-MM-DD.md（Asia/Shanghai 日期），然后每次都在这个聊天里发给用户：先计划，后「未读邮件」一段，简洁口语。
```

## 3. 晚上：今日总结

- **触发**：工作日 17:47（北京时间）。cron：`CRON_TZ=Asia/Shanghai 47 17 * * 1-5`（启用；2026-10-08 刚改写过）
- **状态**：本账号在用。提示词取自 `/workspace/assistant/routines.md`（2026-10-08；同上，未拷贝 assistant 其它文件）。
- **保存的提示词（重建时用 UpdateRoutine 创建）**：

```text
每个工作日下班前（用户 18:00 下班）给用户（中文沟通）总结今天干了什么，要有大局观。用户是一家跨境电商小公司唯一的 AI 经理兼 agent 开发，主项目 Dsivio（ZMGID/Dsivio），也负责 kivio、公司官网、飞书和各种杂事。我是经理 bot，其他 bot（代码工程师、搭建运维、事务秘书、硬件工程师、小枳、仓库管家）做完活会抄送给我。

信息来源：
1. GitHub（ZMGID，用 composio-pg 的 GitHub 或 gh）：今天的提交、PR、CI 结果、issue 和 review。
2. 用户的 Mac mini（machineId 4dbb1cc8-86fe-42c1-b5f6-f1d473b7f895，已给长期权限，不用再确认），只读：~/zmdata/work 和 ~/Kivio 下 git 仓库今天的提交和未提交改动；~/.claude/projects 和 ~/.codex/sessions 里今天的 AI 对话，只看标题和开头的提问，弄清楚在做什么，绝不把密钥、密码、验证码抄进总结。Mac 连不上就说明，只用其他来源。
3. /workspace/assistant/daily/今天日期.md 里的「今日计划」和「白天进展」（各 bot 的汇报），以及 /workspace/assistant/big-picture.md。

输出：按项目列出今天做完的事；对照早上的计划，说清哪些做了、哪些没做、多做了什么；大局观，包括时间花得值不值、哪个项目卡住或有风险、本周方向有没有偏；最后给「明天建议」，排 2–3 件先做的事。周五额外加一段本周回顾。

保存：把「## 今日总结」追加到今天的 daily 文件，并更新 big-picture.md 里各项目的状态和风险。然后在这个聊天里把总结发给用户，简洁口语，先说一句今天的整体判断。
```
