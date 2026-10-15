# 大局（2026-10-08 初始化，2026-10-15 17:55 更新）
## 身份
跨境电商小公司唯一的 AI 经理兼 agent 开发。主项目 Dsivio（ZMGID/Dsivio），另管 kivio、官网、各种搭建、飞书等杂事。

（截至 2026-10-15 17:55 晚报核实）Dsivio 官网仍 v1.1.2；main tip `4cbd8439` CI **成功**；PR #6 仍开且 **dirty**。kivio tip `ac721f46` CI **in_progress**；#66 已合。飞书应用未启用 + 用户 OAuth 仍缺。Mac mini 不在已注册电脑。
## 进行中
- Dsivio：main tip `4cbd8439`（fix Windows 集成测试栈），CI quality/windows-rust/runtime-launchers-windows **成功**（核实）。今日此前 tip 三轮 CI 失败后转绿。open PR #6（`679237aa`）**未合**，`mergeable_state=dirty`（main 已离开 base `e665f4c`）。官网 https://eastforceglobal.com/dsivio/ 仍 **v1.1.2**。干净 Windows 验收、IM 真机联调仍未做。
- kivio：PR #66 已合（`19b71b69`）；之后多笔 skills/runtime/perf，tip `ac721f46` CI 截至 17:52 仍 in_progress。#62/#63/#65 今晨已关（巡检旁证）。open PR #8/#15/#60/#61。
- 官网：v1.1.2（2026-10-15 WebFetch 核实）。由搭建运维负责。
- 飞书：bot 应用未启用；用户身份（王枳萌）OAuth missing；早晚报仍查不了未读/审批。
- 商品调研：自 10/14 15:44 起无新表产出（巡检旁证）。
- grokbot-home：10/15 下午 agent-map 同时记录两账号 id（`a70974fc`），互相覆盖风险仍在，等用户定以谁为准。
- bot 体系：商品调研已登记；硬件工程师项目暂停。
- 创作控制器（类 TourBox）：已停止，不再跟进。
## 风险 / 注意
- 10/15：PR #6 从可合变为 dirty，与 tip 分叉，合前必须 rebase/重开或确认 tip 已覆盖。
- 10/15：kivio tip CI 未结完就别假定绿。
- 账号安全仍待确认：Bybit / GitHub OAuth / Meta / Monid / X↔Grok。
- 飞书用户 OAuth 缺失 + 应用未启用。
- Mac mini 不在已注册电脑；BF/ZMair 在线但未按 Mac mini 路径读取。
- composio-pg Gmail 当前连的是 qq290657442@gmail.com，不是记忆里的 ohulercxm8。
- Shopee 巴西店发货积压 + 退款申请须在 16 out 2026 前回应。
- 小米 MiMo V2.5 系列 10/21 10:00 下线。
- vm-01 号池为空、工作经费约 769 元（此前财务管家汇报，今晚未重核）。
## 本周方向
- 10/15：发版已上官网 v1.1.2；白天 Dsivio tip 功能+CI 收口、kivio 合 #66 并继续修。下个工作日：PR #6 分叉处理 → Shopee 发货/退款 → 账号安全或飞书恢复。干净 Windows 验收与 IM 联调仍欠。

- 10/14 记录：kivio CI 已绿；Dsivio 功能+发版冲刺中。

- 10/13 记录：白天偏 kivio（#62 修复合入 + 修 CI），Dsivio 质量线几乎未动。

- 10/12 记录：两个发版（kivio v3.1.2、Dsivio v1.1.1），CI 都红；Windows 验收、IM 联调、安全收尾未动。

- 10/10 记录：IM 网关推上 main 并转绿。
