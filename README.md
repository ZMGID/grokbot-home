# grokbot-home

我的 Grok Bot「家」：换到新的 Grok Bot 账号时，让新号上的 bot 按这个仓库把自己和其他所有 bot 一起配好，做到基本无缝切换。

## 怎么用

仓库是**私有**的：新号上的 bot 在拿到访问权之前读不到 `BOOTSTRAP.md`。所以开场要先拿 Composio key（应用连接只走 `composio-pg`，2026-10-08 起不再装官方 GitHub/Origin 等连接器）。

在新号上打开任意一个 Grok Bot（一般是默认的主 bot），把下面这段贴给它：

```text
先按下面做完再配自己（仓库 ZMGID/grokbot-home 是私有的）：
1) 用密码框（secret-request）向我要 Composio 项目 API key，写入 /home/box/.composio_pg_key 并 chmod 600，不要打印、不要贴进聊天。
2) 按 BOOTSTRAP 的 Step 0：在 /workspace/composio-pg/ 内联写出 launch.py/launch.sh（与仓库 connectors/composio-pg 相同），装 composio SDK，AddMcpServer composio-pg；再用 Composio 里 GitHub（ZMGID）的 token 做 gh auth login --with-token（勿打印 token），然后 gh repo clone ZMGID/grokbot-home /workspace/grokbot-home。
3) 克隆成功后读 BOOTSTRAP.md，从 Step 1 继续把我和其它 bot 配好。应用连接只走 composio-pg，不要装官方 GitHub/Origin/Finance/Composio 插件。
```

（短版也可以说「按 https://github.com/ZMGID/grokbot-home 配置你自己，先问我 Composio key」。）

它会读 [`BOOTSTRAP.md`](BOOTSTRAP.md)，然后依次：

1. （Step 0）拿 Composio key → 内联启动 composio-pg → 用 Composio GitHub 登录 `gh` → 克隆本仓库；
2. 跑 `setup.sh` 装好工具环境（KiCad、PlatformIO、cadquery、Composio SDK 等）；
3. 确认 `composio-pg` 已接通；重装 pstack 插件（技能用，不是应用连接）；
4. 导入 `skills/` 里的技能（若有）；
5. 按 `bots/grok-bot/` 设置自己的名字和说明，读 `CONTEXT.md`；
6. 用 CreateAgent 把 `bots/` 下其他每个 bot（小枳、dr eggbot、仓库管家……）重新建出来，并重建它们的定时任务；
7. 自检，最后把新学到的东西写回仓库。

我需要亲自做的只有：在密码框里填一次 Composio key（设备码登录仅作备用）。

## 目录

| 路径 | 内容 |
|---|---|
| `BOOTSTRAP.md` | 写给新 bot 的开机步骤（英文为主，附中文） |
| `CONTEXT.md` | 关于我的共享记忆：习惯、账号、项目进度、换号决定 |
| `bots/<名字>/` | 每个 bot 一个文件夹：`profile.md`（设定）、`CONTEXT.md`（它自己的记忆）、`routines.md`（定时任务） |
| `connectors/` | 连接器清单 + `composio-pg` 启动脚本（不含密钥） |
| `skills/` | 我自己创建的技能（目前没有） |
| `setup.sh` | 工具环境安装脚本（可重复运行） |
| `scripts/` | 每日同步任务说明和脚本 |
| `projects/` | 项目文件（仿 TourBox 创作控制器） |

## 规矩

- **密钥永远不进仓库**，即使是私有仓库。密钥只通过 bot 的密码框（secret prompt）输入，或者放 1Password。
- 每个号用完，新记住的东西写回对应的 `CONTEXT.md` 再推送。仓库管家每天凌晨 3:14（北京时间）自动同步一次。
- 仓库保持私有，不要分享，也不要做成公开模板。
