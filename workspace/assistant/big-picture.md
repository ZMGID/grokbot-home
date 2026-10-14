# 大局（2026-10-08 初始化，2026-10-14 17:55 更新）
## 身份
跨境电商小公司唯一的 AI 经理兼 agent 开发。主项目 Dsivio（ZMGID/Dsivio），另管 kivio、官网、各种搭建、飞书等杂事。
## 进行中
- Dsivio：10/14 白天大幅推进。main `e665f4c`（release: prepare v1.1.2 [skip ci]）。今日约 12 笔提交（Monid/Gecko 网关、竞品调研插件、Windows/重试、去掉 Vision OCR 等，GitHub 核实）。open PR #6（fix/ci-windows-rust）最新 CI 截至 17:55 仍 in_progress，此前多轮失败。v1.1.2 Release workflow 仍 in_progress（create-release 成功，macOS/Windows 打包进行中）。官网实际访问仍 v1.1.0。干净 Windows 验收、IM 真机联调仍未做。
- kivio：10/14 main `5b0c96f`（#64），CI quality + windows-rust **成功**（已核实）。issue #62/#63 仍开；新开 #65（技能商店 CSP）。open PR #8/#15/#60/#61。
- 官网（https://eastforceglobal.com/dsivio/）：10/14 仍是 v1.1.0，未换到 v1.1.1/v1.1.2。由搭建运维负责。
- 飞书：bot ready，用户身份（王枳萌）OAuth missing；早晚报仍查不了未读/审批。
- 商品调研：10/14 出 DIVISORIA / CILIOS / PINCEL 表，并更新 tiktok 调研 skill v2。
- grokbot-home：10/14 凌晨新旧号都同步过，互相覆盖风险仍在，等用户定以谁为准。
- bot 体系：商品调研已登记；硬件工程师项目暂停。
- 创作控制器（类 TourBox）：已停止，不再跟进。
## 风险 / 注意
- 10/14：Dsivio 在 windows CI 未稳绿时 skip ci 打 v1.1.2；Release 未完成前不要假定发版可用；官网仍 v1.1.0。
- 10/14：PR #6 连续 CI 失败，质量线与发版分叉。
- 账号安全仍待确认：Bybit ~210 USDT + 异地登录 + cashback；GitHub Cursor/Reason Machines/sub2api；Meta/Facebook 一串；Monid 新设备；X/Grok 链接。
- 飞书用户 OAuth 缺失。
- Mac mini 不在已注册电脑；ZMair/BF 常 offline。
- composio-pg Gmail 当前连的是 qq290657442@gmail.com，不是记忆里的 ohulercxm8——读「工作邮箱」时要注意。
- 小米 MiMo V2.5 系列 10/21 10:00 下线。
- vm-01 号池为空、工作经费约 769 元（此前财务管家汇报，今晚未重核）。
- grokbot-home 加密口令 6 位数字（用户已知情）。
## 本周方向
- 10/14 记录：kivio CI 已绿；Dsivio 功能+发版冲刺中。下个工作日：Release 出结果 → 官网是否换版 → PR #6 收口 → 账号安全 15 分钟 → 飞书扫码 / 定 bot 主号。干净 Windows 验收与 IM 联调仍欠。

- 10/13 记录：白天偏 kivio（#62 修复合入 + 修 CI），Dsivio 质量线几乎未动。

- 10/12 记录：两个发版（kivio v3.1.2、Dsivio v1.1.1），CI 都红；Windows 验收、IM 联调、安全收尾未动。

- 10/10 记录：IM 网关推上 main 并转绿。
