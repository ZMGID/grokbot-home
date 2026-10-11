# Monid：统一 API 平台（2026-10-10 记录）

用户觉得这个方向很有用，先记下来，以后再决定怎么用。

## 是什么
- 网址：https://monid.ai （文档：https://monid.ai/docs/llms.txt）
- 把各种工具和数据接口集中到一个平台，用一个余额统一付费，按次计费，约加收 10% 平台费。
- 接口范围：抓数据（亚马逊、TikTok、Instagram、Reddit、YouTube、X、谷歌地图，很多是转售 Apify）、搜索（Exa、Firecrawl）、人员和公司数据（Apollo、PDL）、SEO（Ahrefs、DataForSEO）、视频和语音生成、浏览器自动化。号称 1700+ 工具、55+ 家供应商。
- 不做大模型调用，所以不能替代中转站（vm2api），也和 Composio 互补：Composio 连接自己的账号，Monid 卖手里没有的数据。
- 调用方式：REST（api.monid.ai/v1）、远程 MCP（https://mcp.monid.ai/v1）、npm CLI、SKILL.md。discover 和 inspect 免费，run 收费。

## 开源情况
- 仓库：https://github.com/monid-ai/monid ，MIT 协议，TypeScript/Deno。
- 开源的只有约 700 个接口的定义和一个本地执行引擎，运行时要填自己的各家 key。
- 钱包、计费、密钥托管、MCP 服务都没开源，所以自己搭省不下各家的订阅。

## 公司情况
- 在旧金山，2 到 3 个人，2026-10-06 宣布 770 万美元种子轮。上线约两个月。
- 服务条款和隐私政策页面打不开；国内能不能付款不清楚。

## 可以怎么用
1. 小额试用：充 5 到 10 美元，跑亚马逊评论、TikTok 趋势、谷歌地图这类选品数据，可以给小枳用。要设预算上限，不传客户隐私。
2. 借鉴到 Dsivio：做一层"一个 key 通吃"的代理，模型走中转站，应用连接走 Composio，数据接口可选接 Monid。同事装好 Dsivio 只要一个 key。
3. 它的 MIT 接口定义格式可以借来，包装我们自己的 API。

## 待定
- 用户还没决定要不要试用，也没决定 Dsivio 是否做统一 key 代理。
