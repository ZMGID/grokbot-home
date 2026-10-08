# grokbot-home

我的 Grok Bot「家」：换到新的 Grok Bot 账号时，让新号上的 bot 按这个仓库把自己和其他所有 bot 一起配好，做到基本无缝切换。

## 怎么用

在新号上打开任意一个 Grok Bot（一般是默认的主 bot），对它说：

> 按 https://github.com/ZMGID/grokbot-home 配置你自己

它会读 [`BOOTSTRAP.md`](BOOTSTRAP.md)，然后依次：

1. 克隆本仓库，跑 `setup.sh` 装好工具环境（KiCad、PlatformIO、cadquery、Composio SDK 等）；
2. 按 `connectors/README.md` 装连接器（官方连接器需要我点一次授权；`composio-pg` 会弹出密码框让我填 Composio API key）；
3. 导入 `skills/` 里的技能，重装 pstack 插件；
4. 按 `bots/grok-bot/` 设置自己的名字和说明，读 `CONTEXT.md`；
5. 用 CreateAgent 把 `bots/` 下其他每个 bot（小枳、dr eggbot……）重新建出来，并重建它们的定时任务；
6. 自检，最后把新学到的东西写回仓库。

我需要亲自做的只有：点连接器授权、在密码框里填一次密钥。

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
- 每个号用完，新记住的东西写回对应的 `CONTEXT.md` 再推送。主 bot 每天凌晨 3:17（北京时间）自动同步一次。
- 仓库保持私有，不要分享，也不要做成公开模板。
