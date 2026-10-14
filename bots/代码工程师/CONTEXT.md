# 代码工程师自己的记忆与项目状态

> 先读根目录 `/CONTEXT.md`。这里只记代码工程师自己的工作记录。

## 职责
- 负责 `ZMGID/Dsivio`（main，优先）和 `ZMGID/kivio` 的 CI、开着的 PR 与代码修复。
- GitHub 访问只走 `composio-pg`（Composio），不装、不要求授权官方 GitHub 连接器。

## 记录
- (2026-10-08) 用户创建本 bot（agent id `30f7829c-e287-44d7-bfdc-7c409b7da1c4`）。
- (2026-10-08) 职责定为：盯 CI 与开着的 PR，CI 挂了查根因并开修复 PR；接主 bot / 用户派来的代码任务；被问时说明 PR 或分支状态。


- (2026-10-08) Dsivio：**PR #1**（CI/release 升 Node 22）CI 全绿未合并；为同事装环境开了 **PR #2/#3/#4**（均绿未合；合并顺序建议 #3→#4，#2 独立）。另有 dsimage **PR #1**（文档），用户称 dsimage 上游不再更新、覆盖风险可忽略。v1.1.0 已发但带 `[skip ci]`。
- (2026-10-08) 用户次日重点：手工继续优化环境配置（PR #2/#3/#4 基础上）；并启动 IM Gateway（调研归小枳）。

- (2026-10-09) 用户说不需要内置 WebView2，Dsivio **PR #2 已关闭未合并**（分支保留）。随后 #1、#5（15:21）和 #3、#4（16:00/16:01）都已合入 main，Dsivio 无开着的 PR；main CI 15:21 首次转绿，合 #3/#4 后最新提交的 CI 被取消、待核实。kivio #60 仍为草稿。

- (2026-10-12) Dsivio 发布 v1.1.1（Release CI 绿），但 main windows-rust 连续红；干净 Windows 验收与 IM 真机联调仍未做。
- (2026-10-12) kivio 发布 v3.1.2；main windows-rust 红；新 issue #62（上下文超限后永久 400）。
- (2026-10-13) kivio 合并 PR #58、#59；下午修 Windows CI（quality 绿、windows-rust 仍红）；bot 模式分支 `codex/bot-development` 无新提交且落后 main。Dsivio 当天无提交，main 仍红。

- (2026-10-14) kivio：`23cddd2` 的 CI 挂在 3 个 Rust 测试（重试文案断言、thinking 档位、key failover；其中 thinking 档位由 models catalog 引入，另两个是 unify retries 留下的）。开 PR #64 修，CI 全绿后 12:27 squash 合入 main（`5b0c96f`）。#62（长会话压缩死锁）与此无关，仍开。本机 `/workspace/kivio` 旧改动已 stash，快进到 main。
- (2026-10-14) Dsivio：windows-rust 只挂 `oversized_output_is_rejected`（推断 Windows 上子进程 5 秒超时太短，改 60 秒并打印真实错误），另修 runtime-launchers-windows 改名 EPERM 偶发；开 PR #6，多轮 CI 未全绿。用户当天另推约 12 笔并在 `e665f4c` 准备 v1.1.2（skip ci），Release 打包当晚未完成，官网仍 v1.1.0。
- (2026-10-14) 临时定时任务：盯 PR #64 的两个例程合并后已删；17:56 设了盯 PR #6 的检查（每 15 分钟、到 10-14 23:56 为止，全绿就 squash 合并并告诉用户和小萌）。另建了 GitHub 事件监听，要 Cursor 账号里的 GitHub 连上才会生效。
