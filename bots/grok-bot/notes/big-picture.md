# 大局（2026-10-08 初始化，2026-10-08 晚更新）
## 身份
跨境电商小公司唯一的 AI 经理兼 agent 开发。主项目 Dsivio（ZMGID/Dsivio），另管 kivio、官网、各种搭建、飞书等杂事。
## 进行中
- Dsivio：10/8 发布 v1.1.0（含内置 Shopee 调研插件、图片搜 SKU 插件），发版提交都 [skip ci]，release 流程仍用 Node 20。main CI 自 9 月起一直红；PR #1（CI/release 升 Node 22）CI 全绿未合并，合并前需 Update branch 重跑完整 CI。
- kivio：PR #60「Kivio Study 材料学习工作台」草稿，检查全绿，live check-mode 验收未过，10/7 后无进展。
- 官网（https://eastforceglobal.com/dsivio/，自己服务器上的 nginx 静态站）：10/8 已上线 v1.1.0 页面，安装包放在自己服务器上的 /dsivio/downloads/v1.1.0/。由搭建运维负责。
- 飞书：未接入，等用户连接。
- grokbot-home 迁移仓库：已公开，密钥加密，仓库管家负责同步、演练和审计。
- bot 体系：10/8 搭好（代码工程师、搭建运维、事务秘书、硬件工程师（备用）、小枳、仓库管家）。
- 创作控制器（类 TourBox）：只是测试，已停止，不再跟进。
## 风险 / 注意
- Dsivio v1.1.0 未经完整 CI 发布，main 长期红灯。
- grokbot-home-private-old 仍含明文 Composio 密钥，待删除；密钥曾在聊天中出现，建议轮换。
- grokbot-home 加密口令只有 6 位数字（用户已知情并选择保留）。
## 本周方向
- 10/8 约一半时间投入 bot 和迁移基础设施；之后应回到 Dsivio 质量（CI 变绿）。

- 10/8 记录：Dsivio 新方向：① 环境配置优化（同事电脑装环境太费时间，已开 PR #2/#3/#4，10/9 用户手工继续优化，当天最重要）；② IM Gateway（接入消息平台），参考 Hermes。
