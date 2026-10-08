# grokbot-home

我的 Grok Bot「家」：换到新的 Grok Bot 账号时，让新号上的 bot 按这个仓库把自己和其他所有 bot 一起配好，做到基本无缝切换。

## 怎么用

仓库是**公开**的（2026-10-08 起），新号上的 bot 不用登录 GitHub 就能匿名克隆、读 `BOOTSTRAP.md`。Composio API key 只以**加密**形式放在 `secrets/*.enc`，解密口令只有我知道（应用连接只走 `composio-pg`，不装官方 GitHub/Origin 等连接器）。

在新号上打开任意一个 Grok Bot（一般是默认的主 bot），对它说：

```text
按这个仓库配置自己：https://github.com/ZMGID/grokbot-home
```

它会读 [`BOOTSTRAP.md`](BOOTSTRAP.md)，然后依次：

1. （Step 0）匿名克隆本仓库 → 用密码框（secret-request）向我要口令 `GROKBOT_HOME_PASSPHRASE` → 解密 `secrets/COMPOSIO_API_KEY.enc` 到 `~/.composio_pg_key`（连不上就换 `.box-current.enc`）→ 从 `connectors/composio-pg/` 装好并添加 composio-pg；
2. （Step 1）用 Composio 里 GitHub（ZMGID）的 token 登录 `gh`——只有往仓库推送（写回、每日同步）才需要；
3. 跑 `setup.sh` 装好工具环境（KiCad、PlatformIO、cadquery、Composio SDK 等）；
4. 确认 `composio-pg` 已接通；pstack 插件可选（原为 dr eggbot 安装）；导入 `skills/` 里的技能（若有）；
5. 按 `bots/grok-bot/` 设置自己的名字和说明，读 `CONTEXT.md`；
6. 用 CreateAgent 把 `bots/` 下其他每个 bot（小枳、仓库管家、代码工程师、搭建运维、邮件秘书、硬件工程师……，以 `bots/index.json` 为准）重新建出来，并重建它们的定时任务；
7. 自检，最后把新学到的东西写回仓库。

我需要亲自做的只有：在密码框里填一次仓库口令（解密失败时才要 Composio key 本身；`gh` 设备码只在推送权限拿不到时备用）。

## 目录

| 路径 | 内容 |
|---|---|
| `BOOTSTRAP.md` | 写给新 bot 的开机步骤（英文为主，附中文） |
| `CONTEXT.md` | 关于我的共享记忆：习惯、账号、项目进度、换号决定 |
| `bots/<名字>/` | 每个 bot 一个文件夹：`profile.md`（设定）、`CONTEXT.md`（它自己的记忆）、`routines.md`（定时任务） |
| `connectors/` | 连接器清单 + `composio-pg` 启动脚本（不含密钥） |
| `skills/` | 我自己创建的技能（目前没有） |
| `setup.sh` | 工具环境安装脚本（可重复运行） |
| `scripts/` | 每日同步任务说明和脚本、密钥扫描 `secret-scan.sh`、加解密 `secret-crypt.py` |
| `secrets/` | 只放加密后的密钥（`*.enc`），见 `secrets/README.md` |
| `projects/` | 项目文件（仿 TourBox 创作控制器） |

## 规矩

- **仓库是公开的，明文密钥永远不进仓库**。唯一例外是 `secrets/*.enc`：用 `scripts/secret-crypt.py` 加密后的 Composio key。口令只通过 bot 的密码框（secret prompt）给，绝不写进仓库或聊天。推送前必须 `bash scripts/secret-scan.sh` 通过。
- 每个号用完，新记住的东西写回对应的 `CONTEXT.md` 再推送。仓库管家每天凌晨 3:14（北京时间）自动同步一次。
- 仓库公开后，里面的共享记忆（`CONTEXT.md`、`bots/*/CONTEXT.md`、`bots/*/raw/memory/`）任何人都能看到；不要再写进不想公开的内容。不做 export-bot-template 分享模板。
