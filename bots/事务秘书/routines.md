# 事务秘书的定时任务

> 提示词来源：`/workspace/assistant/routines.md`（与 2026-10-09 线上一致；zhimeng63 → composio-zhimeng，ohulercxm8 → composio-pg）。
> 时区：用户时区 **Asia/Hong_Kong**（UTC+8）。系统在保存时加上了 `CRON_TZ=Asia/Hong_Kong` 前缀。

## 1. 早上：今日计划

- **触发**：工作日 08:53（Asia/Hong_Kong）。cron：`CRON_TZ=Asia/Hong_Kong 53 8 * * 1-5`（启用）
- **状态**：本账号在用（2026-10-08 从小萌交接；2026-10-09 重建后再次更新连接器分工）。
- **保存的提示词（重建时用 UpdateRoutine 创建）**：

```text
每个工作日早上给用户（中文沟通）做今日计划，并附上今日资讯和未读邮件摘要。用户是一家跨境电商小公司唯一的 AI 经理兼 agent 开发，主项目是 Dsivio（GitHub ZMGID/Dsivio），也负责 kivio、公司官网、各类搭建、飞书等杂事。这项工作是从经理 bot 小萌那里交接过来的。

1. 读 /workspace/assistant/big-picture.md 和 /workspace/assistant/daily/ 下最近几天的文件（尤其是昨天的「今日总结」「明天建议」，以及小萌写的「白天进展」和晚间补充）。如果今天的 daily 文件（/workspace/assistant/daily/YYYY-MM-DD.md）已经存在并写了用户交代的当天重点，计划就以这些重点为主，排在最前；文件里提到的参考材料如果已经生成（例如 /workspace/dsivio-im/ 下的调研文档），在对应的计划项里引用上。
2. 看 GitHub（账号 ZMGID，只走 composio-pg 连接器里的 GitHub，或盒子上的 gh）：开着的 PR 和它们的 CI、main 分支挂掉的 CI、新 issue、待处理的 review。
3. 未读邮件：查看两个 Gmail 账号：ohulercxm8@gmail.com 走 composio-pg 连接器，zhimeng63@gmail.com 走 composio-zhimeng 连接器；看这两个账号 最近（大约过去一天，周一覆盖周末）的未读邮件。按重要程度归纳：需要用户回复或处理的放最前，注明发件人和一句话要点；通知、推广、自动邮件合并成一句带过。只读，不标已读、不回复、不删除。某个账号连不上就照实说明一下，继续其他部分。
4. 今日资讯：搜过去约 24 小时的新闻（周一搜整个周末），可以用网页搜索和抓取，也可以用 x 连接器的新闻和帖子搜索（公开数据，无需授权）。选 5–8 条，以 AI 为主：新模型和大厂动态（OpenAI、Anthropic、Google、xAI，以及 DeepSeek、通义、智谱、字节等国内厂商），agent 和编程工具（Claude Code、Codex、Cursor、MCP、开源 agent 框架）。有的话再加 1–2 条和跨境电商（Shopee、TikTok Shop、亚马逊）或飞书、企业微信相关的 AI 新闻。每条一两句中文：发生了什么，对用户做 Dsivio 或 agent 开发有什么用，并附原文链接。只写查得到真实来源的，不编造；篇幅不超过计划本身。
5. 写今日计划：3–5 件按优先级排好的事，每件附一句理由；一句本周大方向；卡住或拖着的事项。邮件里需要处理的事可以排进计划。
6. 发出前先核实：计划里提到的每个状态（比如某个东西上没上线、PR 合没合、CI 绿没绿）都要用实际来源核对过，查不到就说没查到，不要凭旧文件推断。
7. 把计划、今日资讯和邮件摘要以「## 今日计划」写入今天的 daily 文件（Asia/Shanghai 日期；文件已有内容就保留原内容，追加或更新这一节）。

安全：不把验证码、密钥、口令写进计划、文件或消息；不写服务器 IP；daily/ 目录不进任何公开仓库。

结果发给这个聊天里的用户：先计划，然后「今日资讯」，最后「未读邮件」，平实简洁的中文口语，每个工作日都发。发完后，在 Grok Bot 里把同样的内容抄送给经理 bot 小萌（id a96070f7-cb92-4f15-bcd4-7b1e700cc676），不发给其他任何人。
```

## 2. 晚上：今日总结

- **触发**：工作日 17:47（Asia/Hong_Kong）。cron：`CRON_TZ=Asia/Hong_Kong 47 17 * * 1-5`（启用）
- **状态**：本账号在用（2026-10-08 从小萌交接；2026-10-09 重建后再次更新连接器分工）。
- **保存的提示词（重建时用 UpdateRoutine 创建）**：

```text
每个工作日下班前（用户 18:00 下班）给用户（中文沟通）总结今天干了什么，要有大局观。用户是一家跨境电商小公司唯一的 AI 经理兼 agent 开发，主项目 Dsivio（ZMGID/Dsivio），也负责 kivio、公司官网、飞书和各种杂事。这项工作是从经理 bot 小萌那里交接过来的；其他 bot（代码工程师、搭建运维、硬件工程师、小枳、仓库管家）的进展由小萌汇总进 daily 文件。

信息来源：
1. GitHub（ZMGID，只走 composio-pg 连接器里的 GitHub，或盒子上的 gh）：今天的提交、PR、CI 结果、issue 和 review。
2. 用户的 Mac mini（machineId 4dbb1cc8-86fe-42c1-b5f6-f1d473b7f895，用户已给长期权限，不用再确认），只读：~/zmdata/work 和 ~/Kivio 下 git 仓库今天的提交和未提交改动；~/.claude/projects 和 ~/.codex/sessions 里今天的 AI 对话，只看标题和开头的提问，弄清楚在做什么。Mac 连不上就说明，只用其他来源。
3. 两个 Gmail（ohulercxm8@gmail.com 走 composio-pg，zhimeng63@gmail.com 走 composio-zhimeng），只读，看今天有没有需要用户明天处理的邮件。不标已读、不回复、不删除。
4. /workspace/assistant/daily/今天日期.md 里的「今日计划」「白天进展」和小萌写的晚间补充（18 点前后的工作都要算进去），以及 /workspace/assistant/big-picture.md。

输出：按项目列出今天做完的事；对照早上的计划，说清哪些做了、哪些没做、多做了什么；大局观，包括时间花得值不值、哪个项目卡住或有风险、本周方向有没有偏；最后给「明天建议」，排 2–3 件先做的事。周五额外加一段本周回顾。

发出前先核实：每条"做完了/上线了/合并了/挂了"的说法都要用实际来源（GitHub、网站实际访问、Mac 上的仓库状态等）核对过，核对不了就写"没核实到"，不要照搬 bot 汇报或旧文件下结论。

保存：把「## 今日总结」追加到今天的 daily 文件，并更新 big-picture.md 里各项目的状态和风险。

安全：不把验证码、密钥、口令抄进总结、文件或消息；不写服务器 IP；daily/ 目录不进任何公开仓库。

结果发给这个聊天里的用户：先一句今天的整体判断，然后是总结，平实简洁的中文口语，每个工作日都发。发完后，在 Grok Bot 里把同样的总结抄送给经理 bot 小萌（id a96070f7-cb92-4f15-bcd4-7b1e700cc676），不发给其他任何人。
```
