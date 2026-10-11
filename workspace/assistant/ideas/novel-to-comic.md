# 「小说 → 漫画」项目调研报告

> 调研时间：2026-10-11 19:20（北京时间）｜调研方式：WebSearch / WebFetch、GitHub 公开 API、X 连接器｜只读，没有注册账号、安装任何东西或发送消息
> 约定：标「未核实」= 只有二手或营销来源，或者没能打开原始页面。GitHub star 数为 2026-10-11 约 19:15（北京时间）的 API 读数。汇率按 1 USD ≈ 7.1 CNY 粗算（这是假设，不是查到的数）。

---

## 第一页：要点

**结论先说：「小说转漫剧（视频）」这条线已经极度拥挤；「小说转静态漫画」SaaS 和开源也不少，但都小而散。模型能力在快速拉平（GPT Image 2、Nano Banana 2.1 已经能整页出图、带气泡文字），单靠「能出图」建不起护城河。作为 Dsivio 的一个插件值得做，成本低、能复用 dsimage；当成独立创业项目不建议。**

1. **大厂全在做，但钱集中在「漫剧」视频，不在静态漫画。**
   - 字节：红果免费漫剧 App，上线 4 个月用户约 2400 万（QuestMobile）；另有番茄 IP 库和 Seedance 视频模型。
   - 腾讯：火龙漫剧，2026-02-04 上线，首日 1701 部。
   - 百度：柚漫剧、七猫漫剧，加上生产工具度加 AI 剧。
   - 快手：漫剧专家 Agent，目前要邀请码。
   - 阅文：火种计划和 DramaBuddy 漫剧助手。
   - 点众：双十亿计划，开放 8 万部 IP。
   - 海外：Naver 和 Kakao 用 AI 做的是 IP 聊天、条漫转短视频，没有做「小说转漫画」。
   - Google、OpenAI 没有专门的产品，它们的作用是供应底层模型。
2. **静态漫画竞品**：LlamaGen（自称 50 万以上用户，$18–$200/月）、Dashtoon（融资合计 $1800 万）、Novel2Comic（约 $0.05/页起）、GenToon、TaleAtelier、mushni、知漫剧等。
3. **开源**：漫剧方向已经有 1.4 万–1.7 万 star 的项目（Toonflow-app 17,176 MIT；huobao-drama 16,027 CC BY-NC-SA；waoowaoo 14,489 ELv2）。纯静态「小说转漫画」开源项目大多不到 100 star，例外是 ai-comic-factory（1,341，已不太活跃）和研究型的 StoryDiffusion（6,473）、DiffSensei（925）。
4. **技术已经不是瓶颈**：
   - Nano Banana 2.1 每次调用最多 14 张参考图，最多 4 个角色保持一致（Google 官方文档）。
   - GPT Image 2 / 2.5、Seedream 5.0 Pro、Qwen-Image 3.0 都主打文字渲染。
   - 真正难的是：长篇改编质量（分镜节奏）、跨章节一致性、中文气泡文字能不能改、重画成本。
5. **每页成本估算（只算图像 API，每页 4–6 格）**：
   - 整页直出（1 次调用出整页，平均重画 50%）：约 ¥0.2–¥1.8/页。Seedream 5.0 Pro / Qwen-Image 3.0 / Nano Banana 2.1 约 ¥0.25–¥0.55，GPT Image 2 high 约 ¥1.76，Nano Banana Pro 约 ¥1.43。
   - 逐格生成（5 格，平均重画 40%，即 7 次调用）：约 ¥1–¥10/页。
   - LLM 写分镜每页不到 ¥0.1，可以忽略。
6. **合规是硬门槛**：
   - 2025-09-01 起施行《人工智能生成合成内容标识办法》和强制国标 GB 45438-2025：图片要有显式「AI 生成」文字标识，字高不低于最短边的 5%，元数据里要有隐式标识。
   - 2026-04-01 起，AI 漫剧「先备案、后上线」；7 月 1 日起 AI 微短剧按投资额分层审核。
   - 最高法 2026-09-07 发布的意见第十二条：使用者明知在先作品存在，用 AI 生成实质相似内容，要担侵权责任。天津和平区法院已经调解了首例「小说喂 AI 生成漫剧」侵权案。
7. **国内变现的坑**：抖音版权中心开放的 50 万部番茄 IP，明确**不许改编成「静态解说漫剧」**，只允许 AI 仿真人剧、2D/3D 动画漫剧、沙雕漫。所以静态漫画在国内主流平台上直接变现的路很窄。
8. **推荐 MVP（两周，Dsivio 插件 `dscomic`）**：
   - 流程：TXT/EPUB 章节 → LLM 生成故事圣经和分页分格 JSON → 角色设定卡（用户确认）→ 整页直出（多图参考，留白气泡）→ React 前端可编辑叠字层（中文字体后期渲染）→ 导出 PNG/PDF/CBZ 和条漫长图。
   - 自动加 AIGC 显式和隐式标识，加一道权利确认（只许原创、已授权、公版作品）。
   - 可以接 dsvideo-plugin 做动态漫。
   - 差异化：本地优先、用户自带 key（BYOK）、可编辑文字层、合规内建，以及**电商场景**（产品故事漫画、品牌四格、A+ 页面漫画），这是你的主业优势。
9. **最大风险**：①版权：用户拿受保护的网文去生成，工具方可能被要求「采取必要措施」；②同质化：模型厂和大平台随时可以把这个能力做进自家产品；③国内静态漫画变现渠道窄；④重画成本和中文文字质量不稳定。

---

## 1. 现有产品

### 1.1 国内：平台和大厂

| 主体 | 产品/动作 | 做什么 | 价格/模式 | 热度（可查到的） | 来源 |
|---|---|---|---|---|---|
| 字节 | 红果免费漫剧 App、番茄 IP、Seedance | 漫剧分发平台，番茄小说出 IP，Seedance 视频模型负责生产 | C 端免费，广告和分成 | 红果漫剧上线 4 个月用户约 2400 万（QuestMobile 2026-04）；红果短剧月活 2.45 亿、日活破亿（2026-01）；2026 春节档 AI 漫剧占短剧大盘近三成（36氪）；《万妖图录传》十二季 1200 集，第十二季预约超 720 万 | [新浪财经 2026-09-16](https://finance.sina.com.cn/jjxw/2026-09-16/doc-iniryzky3434425.shtml)、[36氪](https://m.36kr.com/p/3705831913648265) |
| 字节/抖音 | 抖音短剧版权中心「漫剧 IP 改编库」 | 2026-03-09 上线，开放 50 万部以上番茄原创 IP 的改编权 | 要先签「模式二/模式三」。个人每月 1 部长篇、5 部短篇；机构每月 5 部长篇、10 部短篇。**禁止改编成静态/动态解说漫剧和 AIGC 推书视频** | — | [澎湃 2026-03-13](https://www.thepaper.cn/newsDetail_forward_32758791) |
| 字节 | 即梦「小章鱼」Octo | 故事大纲 → 角色/场景资产 → 分镜 → 短片，可多人协作 | Web 端内测申请 | 2026-04 上线 | [腾讯新闻 2026-04-09](https://news.qq.com/rain/a/20260409A04U4200)、[新京报](https://www.bjnews.com.cn/detail/1775720323129620.html) |
| 快手 | 漫剧专家（AI 漫剧 Agent） | 剧本、角色、场景、分镜、图生视频、特效，一站式生产加变现 | 凭邀请码体验；单剧最高 4% 投流返点 + 2 万元现金激励 | 2025-12 快手漫剧日消耗突破 700 万 | [新浪科技 2026-01-15](https://finance.sina.com.cn/tech/roll/2026-01-15/doc-inhhkmpv3333017.shtml) |
| 腾讯 | 火龙漫剧 App（加阅文、腾讯动漫 IP） | 竖屏免费漫剧，走「追番社区」路线 | 免费 | 2026-02-04 上线，首日 1701 部；8 天上线 1849 部 | [36氪](https://m.36kr.com/p/3705831913648265)、[澎湃](https://www.thepaper.cn/newsDetail_forward_32642998?commTag=true) |
| 阅文 | 火种计划、起点剧场、DramaBuddy | 开放 IP，计划签约 1000 位 AI 导演，个人创作者扶持超 1 亿元；DramaBuddy 覆盖剧本、分镜、视觉制作 | IP 分级授权加动态分成（分成细节为二手来源，未核实） | 过去半年网文改编漫剧 1000 部，超 100 部播放破千万，26 部破亿（阅文 CEO 自述） | [环球网 2026-03-30](https://news.qq.com/rain/a/20260330A041F800)、[证券日报 2026-07-16](http://m.zqrb.cn/gscy/qiyexinxi/2026-07-16/A1784189673032.html) |
| 百度 | 柚漫剧、七猫漫剧（消费端），度加 AI 剧（生产端） | 度加 AI 剧覆盖剧本改编、角色资产、分镜、视频生成、协同；对接七猫 8 万 IP | 未查到价格 | 宣称约 3 小时改完一部剧本（二手来源，未核实） | [网易](https://www.163.com/dy/article/KHUORFMN05199KH8.html)、[飞天影业 2026-10-10](https://www.feitianyingye.com/2026/1010/7723.shtml) |
| 点众 | 「双十亿」AIGC 共创计划 | 开放 8 万部小说 IP，提供保底、分成，以及河马剧场/DramaBox 发行 | — | 未查到自研工具 | [网易](https://www.163.com/dy/article/KQNRNJGL0517STOQ.html) |
| 哔哩哔哩 | Index-AniSora（开源） | 动漫视频生成模型，支持漫画转视频、关键帧引导 | Apache-2.0，2,527 star | — | [GitHub](https://github.com/bilibili/Index-anisora) |
| 快看漫画 | Livo（内测） | 方向是「数字生命/仿生世界」交互叙事，**不做**漫画生成 | 邀请码 | 2026-09 内测 | [澎湃](https://m.thepaper.cn/newsDetail_forward_34029595) |

### 1.2 国内：第三方工具

| 产品 | 做什么 | 价格 | 用户反馈/热度 | 来源 |
|---|---|---|---|---|
| 知漫剧（jiaxunai.cn） | 小说导入 → 自动拆分 → 角色库 → 分镜 → 配音 → 字幕 → 成片 | 未查到官方价格 | 能找到的对比文章都带推广链接，偏软文。文中「偏差率约 5%」等数据**未核实** | [SegmentFault](https://segmentfault.com/a/1190000048264696)、[pwwt.cn](http://www.pwwt.cn/news/4283467/) |
| mushni | 小说 → 漫画 → 动漫/视频 → 游戏 | 未查到 | 未查到 | [mushni](https://www.mushni.com/novel-to-comic.html) |
| 「豆包 + 即梦」组合 | 豆包写剧本和分镜，即梦 4.0 出多格图、图生视频 | 按各自的积分或会员 | 自媒体常用的教程打法 | [张刚AI拆解](https://zhanggang.net/doubao-jimeng-ai-comic-workflow/) |

**创作者侧反馈（红星新闻 2026-08-21）**：
- 算力成本从约 500 元/小时涨到 1.5 万元/小时（受访者自述）。
- 一集 2.5 分钟漫剧成本约 400–500 元。
- 6 月起流量断崖式下跌。
- 番茄 8-17 新规：没有版权的拉新视频限时长、不能连载，导致一批 AI 博主停更。
- 来源：[新浪/红星](https://finance.sina.com.cn/tech/roll/2026-08-21/doc-inipakut1675946.shtml)

### 1.3 海外

| 产品 | 做什么 | 价格 | 热度 | 来源 |
|---|---|---|---|---|
| LlamaGen.ai | 故事/剧本 → 多页漫画/条漫，有 Comic Studio 编辑、角色一致性、LoRA、漫画转视频、Comic API | Standard $18/月（年付 $14），Pro $30（年付 $24），Unlimited $96，Production $200（宣称约 450 页/月，相当于每页约 $0.44）；单次积分包 $4.99 起；API $7.5–$333/月（年付价） | 官网自称「50 万以上用户、1000 万以上漫画」「2 万以上付费客户」；Tracxn 显示未融资 | [价格](https://llamagen.ai/pricing)、[API 价格](https://llamagen.ai/comic-api/pricing)、[Tracxn](https://tracxn.com/d/companies/llamagen/__3Fc2NsJ5ChvqytjW71fYL8mwINQESqehMHqGF8ubQfY) |
| Dashtoon（Dashverse） | AI 漫画创作工作室（Storyboard2Comic 等）加阅读 App | 未查到 Studio 价格 | 2023-11 种子轮 $500 万；2025-08 A 轮 $1300 万（Peak XV 领投，Z47、Stellaris 跟投）；微软页面称 8 万以上月活读者、200 以上活跃创作者（未核实时效） | [Economic Times](https://economictimes.indiatimes.com/tech/funding/ai-entertainment-startup-dashverse-raises-13-million-from-peak-xv-partners-z47-others/articleshow/123250912.cms)、[TFN](https://techfundingnews.com/dashtoon-raises-5m-to-deploy-generative-ai-for-comic-creation/)、[公司页](https://dashtoon.com/company) |
| Novel2Comic | 读章节自动出页，每页 4 格，配角色设定卡 | $20 买 4000 积分；普通画质 10 积分/张（约 $0.05/页），高画质 40 积分（约 $0.20/页）；视频 40 积分/秒 | 未查到 | [价格](https://novel2comic.com/en/pricing)、[成本博客](https://novel2comic.com/en/blog/how-much-does-it-cost-to-generate-a-full-ai-comic-from-a-novel) |
| GenToon | 小说场景 → 分格计划 → 用保存的角色出图 → 条漫/漫画排版，有社区发布 | 有免费档，具体价格页面没展示 | 未查到 | [GenToon](https://www.gentoon.ai/en/novel-to-webtoon) |
| TaleAtelier | 文字故事 → 竖屏条漫，36 种风格 | Starter $9.99/月（2000 tokens） | 未查到 | [TaleAtelier](https://taleatelier.com/ai-webtoon-maker) |
| Naver WEBTOON | byUs：用作者授权的 IP 做 AI 故事聊天（2026-07） | — | 不是漫画生成 | [ANN](https://www.animenewsnetwork.com/news/2026-07-11/webtoon-launches-ai-story-chat-service-byus-featuring-creator-approved-webtoon-ip/.239448) |
| Kakao Entertainment | Helix Shorts：把条漫自动转成约 40 秒宣传短视频，对 KakaoPage 合作方免费 | 免费 | 2025-10 发布 | [ANN](https://www.animenewsnetwork.com/news/2025-10-04/kakao-entertainment-rolls-out-free-ai-short-form-video-tool-for-webtoon-creators/.229575) |
| Google / OpenAI | **没有检索到专门的「小说转漫画」产品**，它们提供底层模型（Nano Banana、GPT Image）。很多第三方工具直接调这些模型 | — | — | 见第 3 节定价来源 |

**X 上的用户声音（样本少，只作参考）**：
- 「Novel-to-comic pipelines live or die on character consistency」：[@sybx11 2026-10-03](https://x.com/sybx11/status/2106175587949904334)
- Nano Banana 2.1 和 GPT Image 2.5 Sunburst 做四格猫漫画的对比：两者角色一致、气泡文字都对，但 Sunburst 会自己加无关文字：[@morphedai 2026-10-07](https://x.com/morphedai/status/2107878626947711168)
- 有人称 GPT-Image-2 解决了「换脸」和「气泡乱码」：[@derek_wall90176 2026-07-31](https://x.com/derek_wall90176/status/2083069678965166119)（个人体验，未核实）
- 吐槽某 AI comic generator 坏了：[@2100sw20](https://x.com/2100sw20/status/2107704791157899526)
- 有人做角色一致的长期项目，要开 GPT Pro 才够用：[@Chiyeaiart](https://x.com/Chiyeaiart/status/2061738910573895844)
- 中文圈充斥「AI 漫画变现课」引流帖，说明这个赛道已经进入卖课阶段。

---

## 2. GitHub 开源项目（2026-10-11 读数）

### 2.1 静态漫画 / 小说转漫画

| 项目 | Star | 协议 | 最近 push（北京时间） | 流程 / 模型 |
|---|---|---|---|---|
| [HVision-NKU/StoryDiffusion](https://github.com/HVision-NKU/StoryDiffusion) | 6,473 | Apache-2.0 | 2024-09-26 | 研究项目（NeurIPS 2024），用一致性自注意力保持角色一致，基于 SD 系列 |
| [jbilcke-hf/ai-comic-factory](https://github.com/jbilcke-hf/ai-comic-factory) | 1,341 | Apache-2.0 | 2025-10-31 | LLM 写分格 + SDXL 出图，有 HF Space |
| [jianzongwu/DiffSensei](https://github.com/jianzongwu/DiffSensei) | 925 | 无 | 2025-02-05 | CVPR 2025，多模态 LLM + 扩散模型做定制漫画 |
| [revfactory/webtoon-harness](https://github.com/revfactory/webtoon-harness) | 324 | MIT | 2026-06-28 | Claude Code 编排，27 个 agent 产出一话韩式条漫 |
| [victorhuangwq/story-to-manga](https://github.com/victorhuangwq/story-to-manga) | 47 | MIT | 2026-02-06 | Next.js + Nano Banana（Gemini 图像），黑客松作品 |
| [lmqvq/mq-ai-Novel2Comic](https://github.com/lmqvq/mq-ai-Novel2Comic) | 46 | 无 | 2025-10-26 | 中文小说转漫画 |
| [aiskyhub/novel_to_comic](https://github.com/aiskyhub/novel_to_comic) | 33 | 无 | 2026-10-11 | 给 Codex 等编码助手用的工作流/skill |
| [lhfer/codex-novel-to-comic-studio](https://github.com/lhfer/codex-novel-to-comic-studio) | 26 | MIT | 2026-05-19 | **流程设计最值得参考**：权利关卡 → 解析 → 故事圣经 → 视觉圣经（风格、角色卡需确认）→ 分页剧本 → 整页导演 brief → image2 整页出图 → 质检 → PDF/CBZ |
| [phaethix/inkstone](https://github.com/phaethix/inkstone) | 8 | MIT | 2026-10-11 | 本地 Python，ImageProvider 可插拔；一致性靠 L1 提示词硬描述 + L2 参考图 img2img |
| [gnipbao/story-to-handdrawn-video](https://github.com/gnipbao/story-to-handdrawn-video) | 2,194 | MIT | 2026-09-22 | Agent skill：中文故事 → 手绘日记漫画动画（MP4） |

### 2.2 漫剧/短剧（视频方向，拥挤度参考）

| 项目 | Star | 协议 | 最近 push | 备注 |
|---|---|---|---|---|
| [HBAI-Ltd/Toonflow-app](https://github.com/HBAI-Ltd/Toonflow-app) | 17,176 | MIT（README 说已从 Apache-2.0 加附加条款改成 MIT，去掉商业限制） | 2026-10-10 | 剧本、分镜、资产、图像和视频生成，无限画布，MCP，跨平台客户端；提到 Seedance、GPT-Image-2、ComfyUI |
| [chatfire-AI/huobao-drama](https://github.com/chatfire-AI/huobao-drama) | 16,027 | CC BY-NC-SA 4.0（**禁止商用**） | 2026-10-05 | 一句话生成短剧；Electron，用 Seedance、Wan、Gemini |
| [waooAI/waoowaoo](https://github.com/waooAI/waoowaoo) | 14,489 | Elastic License 2.0 | 2026-09-21 | Next.js；Nano Banana、Seedance、MiniMax |
| [dramaclaw/dramaclaw](https://github.com/dramaclaw/dramaclaw) | 6,842 | 未声明 | 2026-10-10 | 剧本到成片的 AIGC 视频引擎 |
| [eternityspring/shuohao-skills](https://github.com/eternityspring/shuohao-skills) | 4,373 | Apache-2.0 | 2026-10-08 | 短剧 skill 合集：拆角色、写大纲、切分镜 |
| [zenstory-ai/drama-skills](https://github.com/zenstory-ai/drama-skills) | 2,720 | MIT | 2026-10-03 | 适配 Claude Code / Codex 的漫剧 skill |
| [shuyu-labs/BigBanana-AI-Director](https://github.com/shuyu-labs/BigBanana-AI-Director) | 2,302 | CC BY-NC-SA 4.0 | 2026-10-06 | Electron；Nano Banana Pro、GPT Image 2、Seedance |
| [xuanyustudio/LocalMiniDrama](https://github.com/xuanyustudio/LocalMiniDrama) | 2,013 | MIT | 2026-10-02 | 本地、数据不出本机 |
| [LingyiChen-AI/AIComicBuilder](https://github.com/LingyiChen-AI/AIComicBuilder) | 1,906 | Apache-2.0 | 2026-04-27 | Next.js；Gemini、Kling、Seedance、Veo |
| [Tenney95/AI-Canvas-tauri](https://github.com/Tenney95/AI-Canvas-tauri) | 214 | 未声明 | 2026-10-10 | **Tauri** 本地 AI 画布，和 Dsivio 技术栈相同 |

### 2.3 可复用的组件

| 项目 | Star | 协议 | 用途 |
|---|---|---|---|
| [zyddnys/manga-image-translator](https://github.com/zyddnys/manga-image-translator) | 10,493 | GPL-3.0 | 文字检测、去字、嵌字，可以参考它的「后期叠字」做法 |
| [dmMaze/BallonsTranslator](https://github.com/dmMaze/BallonsTranslator) | 5,202 | GPL-3.0 | 气泡编辑、嵌字 |
| [VectorSpaceLab/OmniGen2](https://github.com/VectorSpaceLab/OmniGen2) | 4,118 | Apache-2.0 | 多图参考的开源生成模型 |
| [bytedance/UNO](https://github.com/bytedance/UNO) | 1,364 | Apache-2.0 | 单主体/多主体定制 |
| [Tencent-Hunyuan/InstantCharacter](https://github.com/Tencent-Hunyuan/InstantCharacter) | 1,044 | 自定义 | 角色一致性 |

⚠️ GPL-3.0、CC BY-NC-SA、ELv2 的代码不要直接并进闭源或商用的 Dsivio。只借鉴思路，或者作为独立进程调用（是否合规需要再核实）。

**观察**：开源热度几乎全在「漫剧视频」。纯静态漫画的开源项目都很小，说明大家默认「漫画只是漫剧的中间产物」。

---

## 3. 技术路线

### 3.1 流水线（业界共识，综合 codex-novel-to-comic-studio、Novel2Comic、GenToon 的公开流程）

1. **权利确认**：只允许原创、已授权、公版作品。
2. **解析**：TXT/EPUB 切章节。
3. **故事圣经（LLM）**：人物表（外貌硬描述、服装、口头禅）、地点、时间线、每章剧情节点。
4. **分镜脚本（LLM，结构化 JSON）**：每章 → 页 → 格，字段包括景别、机位、动作、角色、表情、对白、旁白、拟声词、阅读顺序。Novel2Comic 的公开做法是「每章列节拍，每页 4 格，安静的章节 1 页，打斗加揭秘的章节 3 页」。
5. **视觉圣经**：先出风格样张，再给每个主角出三视图或表情设定卡，人工确认后锁定，作为后续的参考图。
6. **出图**：整页直出，或逐格生成后再排版（见 3.3）。
7. **文字**：模型直出，或后期叠字（见 3.4）。
8. **质检 / 重画**：人工挑选，或用 VLM 自动检查人脸和服装一致性、文字是否正确。
9. **导出**：PNG、PDF、CBZ、条漫长图；同时写入 AIGC 显式和隐式标识。

### 3.2 角色一致性

| 方案 | 现状 | 适合 MVP 吗 |
|---|---|---|
| 多图参考的闭源 API | Nano Banana 2.1 / 3.1 Flash Image 每次最多 14 张参考图、最多 4 个角色一致；Nano Banana Pro 5 张高保真、共 14 张（[Google 官方文档](https://ai.google.dev/gemini-api/docs/image-generation)）。Seedream 5.0 Pro 支持 1–10 张参考图（[二手来源](https://www.heyuan110.com/zh/posts/ai/2026-07-09-seedream-5-pro/)，未核实官方）。Qwen-Image-2.1-Pro 支持多参考图编辑（[阿里云](https://help.aliyun.com/zh/model-studio/qwen-image-2-1-pro)）。GPT Image 2 对输入图一律高保真处理（[OpenAI 文档](https://developers.openai.com/api/docs/guides/image-generation)） | **适合，首选** |
| LoRA 微调 | 一致性最强，但每个角色都要训练；LlamaGen 把它放在付费档。BFL 开放权重的授权包含 LoRA 权利（[bfl.ai/pricing](https://bfl.ai/pricing)） | 第二阶段再说 |
| 开源方案（StoryDiffusion、UNO、InstantCharacter、OmniGen2） | 要 GPU，本地部署门槛高 | 不适合一个人两周 |
| 工程手段 | 固定的角色硬描述 prompt、每格附带设定卡、同场景复用上一格做参考、VLM 一致性打分后自动重画 | 必做 |

### 3.3 分格排版：整页直出 vs 逐格合成

- **整页直出**：1 次调用出整页（含分格线和气泡）。成本最低，画面构图连贯。缺点是分格位置不可控，想单改一格要用 edit 或局部重绘。GPT Image 2.5 / Nano Banana 2.1 有 mask 编辑。codex-novel-to-comic-studio 走的就是整页路线。
- **逐格生成加模板排版**：每格单独出图，前端按模板拼页。可控性和可编辑性最好，成本是整页的 4–7 倍，格与格之间的风格也容易漂移。
- **建议**：MVP 用整页直出，加「单格重画（mask 编辑）」作为补救；条漫（竖屏长图）可以按格出图，直接纵向拼接，天然适合逐格。

### 3.4 对白气泡和中文文字

- **模型直出**：GPT Image 2/2.5、Nano Banana 2.1、Seedream、Qwen-Image 都宣传文字渲染能力强，Qwen-Image 官方称「复杂文本渲染 SOTA」（[阿里云](https://help.aliyun.com/zh/model-studio/qwen-image)）。缺点：文字是烤在像素里的，改一个字就要重画；长对白和繁体、生僻字仍可能出错（X 上已经有人反馈模型会自己加多余文字）；文字也没法做翻译、出海多语种。
- **后期叠字（推荐）**：提示词要求「留白气泡」或者不画气泡；前端用 SVG/Canvas 渲染气泡和文字，字体用思源黑体、思源宋体、站酷等可商用字体（字体授权请自行核实）；位置由 LLM 给出建议坐标，用户可拖拽调整。好处是可编辑、可多语言（出海时一键换英文、日文），还和 manga-image-translator 的嵌字思路一致。
- **混合方案**：拟声词让模型直出（有美术感），对白和旁白后期叠。

### 3.5 每页成本估算

**官方单价（截至 2026-10-11）**

| 模型 | 单张输出价 | 来源 |
|---|---|---|
| Nano Banana 2.1（gemini-nano-banana-2.1） | 1K $0.0336，2K $0.0504，4K $0.113；Batch 半价；输入 $1.50/百万 token | [Google 定价页](https://ai.google.dev/gemini-api/docs/pricing)（页面标注更新于 2026-10-09 UTC） |
| Nano Banana 2（gemini-3.1-flash-image） | 1K $0.067，2K $0.101 | 同上 |
| Nano Banana 2 Lite | 1K $0.0336 | 同上 |
| Nano Banana Pro（gemini-3-pro-image） | 1K/2K $0.134，4K $0.24；输入图约 $0.0011/张 | 同上 |
| GPT Image 2 | 1024×1536：low $0.005、medium $0.041、high $0.165；1024²：medium $0.053、high $0.211 | [OpenAI 图像指南](https://developers.openai.com/api/docs/guides/image-generation)、[定价页](https://platform.openai.com/docs/pricing)。GPT Image 2.5 的 token 单价相同，但每张图的 token 数要用计算器算，没有静态表（**每张价格未核实**） |
| Seedream 5.0 Pro（火山方舟） | ≤261 万像素 ¥0.15/张，>261 万像素 ¥0.30/张；Flash ¥0.12/张 | [LaoZhang 博客，引用 2026-10-02 的公开价](https://blog.laozhang.ai/zh/posts/seedream-5-pro-layer-decomposition-api)。7 月首发价是 ¥0.30/¥0.60（[来源](https://zhangwenbao.com/seedream-5-pro-image-api-pricing.html)）。**火山官方价格页（[链接](https://www.volcengine.com/docs/82379/1099320)）没能直接抓到正文，未核实** |
| Qwen-Image 3.0（百炼，北京） | 生成 ¥0.18/张，输入图 ¥0.02/张；3.0-pro：1K ¥0.25、2K ¥0.50 | [阿里云官方](https://help.aliyun.com/zh/model-studio/qwen-image-3-0) |
| FLUX（BFL API） | 计算器默认 $0.048/张（1K，没写是哪个模型） | [bfl.ai/pricing](https://bfl.ai/pricing)（具体模型未核实） |

**假设**：每页 4–6 格（取 5 格）；整页直出平均每页 1.5 次调用（重画率 50%）；逐格生成每页 5 格 × 1.4 = 7 次调用（重画率 40%）；参考图输入费另计（每张约 $0.001–0.002，或 ¥0.02），影响很小。

| 模型 | 路线 A：整页直出（1.5 次） | 路线 B：逐格（7 次 × 1K） |
|---|---|---|
| Nano Banana 2.1 · 2K | $0.076 ≈ **¥0.54**（Batch 约 ¥0.27） | 1K：$0.235 ≈ ¥1.67 |
| Nano Banana Pro · 2K | $0.20 ≈ ¥1.43 | $0.94 ≈ ¥6.7 |
| GPT Image 2 high · 1024×1536 | $0.25 ≈ ¥1.76 | 1024² high：$1.48 ≈ ¥10.5 |
| GPT Image 2 medium | $0.062 ≈ ¥0.44 | 1024²：$0.37 ≈ ¥2.6 |
| Seedream 5.0 Pro ≤261 万像素 | ≈ **¥0.23**（加参考图约 ¥0.29） | ≈ ¥1.05 |
| Qwen-Image 3.0（含 2 张参考图） | ≈ ¥0.33 | ≈ ¥1.54 |

- 悲观情况（整页重画 100%，即每页 2 次调用）：上表路线 A 的数字乘以 4/3。
- LLM 分镜：用 gemini-3.8-flash（$0.75 / $3.75 每百万 token，2026 年底前价格），每页约 3k 输入 + 1.5k 输出 ≈ $0.008，不到 ¥0.1。
- 一次性成本：每个主角一张设定卡，约 $0.03–$0.4。
- 对照市场售价：Novel2Comic 约 $0.05/页（普通）、$0.20/页（高画质）；LlamaGen Production 约 $0.44/页。**原料成本和零售价之间只差几倍，价格战空间很小。**

---

## 4. 市场与合规

### 4.1 谁会付钱，怎么变现

| 客群 | 付费意愿 | 判断 |
|---|---|---|
| 漫剧工作室、MCN | 高，但他们要的是**视频**；静态分镜图只是中间产物 | 已被 Toonflow、度加、漫剧专家等工具和平台工具覆盖 |
| 网文作者（自有版权）做宣传、试水 IP | 中低，金额小 | 阅文、番茄会自己提供工具 |
| 海外独立创作者（WEBTOON Canvas、Tapas、KDP） | 中，订阅 $10–$30/月 | LlamaGen、Dashtoon 等已经在做。WEBTOON Canvas 条款未查到明确禁止 AI 内容，但上传者要对版权负责（[条款](https://www.webtoons.com/en/terms/canvasTermsOfUsePolicy)，二手解读未核实） |
| 教育、儿童绘本、企业培训 | 中 | LlamaGen 有教育版 $13.99/月 |
| **电商、品牌（你的主业）** | **中高，且和 Dsivio 现有用户重合** | 产品故事漫画、开箱四格、A+ 页面漫画、社媒条漫广告，**竞品少，是差异化点**（这是推断，没有市场数据） |

- 市场规模参考：2025 年漫剧市场规模预计突破 200 亿元（巨量引擎、火山引擎口径，[界面](https://www.jiemian.com/article/13599966.html)）。2026 年一季度上线微短剧约 12.8 万部，其中 AI 微短剧约 12.2 万部，占比超 95%（转引中国网络视听协会，[飞天影业](https://www.feitianyingye.com/2026/0911/5946.shtml)，未核实原文）。
- 静态漫画的变现：国内主流 IP 库明确禁止「静态解说漫剧」，所以静态漫画要么走海外条漫平台，要么走品牌、教育定制，或者作为漫剧的分镜前置环节。

### 4.2 AI 生成内容标识

- **《人工智能生成合成内容标识办法》**（国信办通字〔2025〕2号，2025-09-01 起施行）。来源：[网信办原文](https://www.cac.gov.cn/2025-03/14/c_1743654684782215.htm)
  - 显式标识：图片要在「适当位置添加显著的提示标识」；提供下载、导出功能时，文件里必须带显式标识（第四条）。
  - 隐式标识：在文件元数据中写入生成合成内容属性、服务提供者名称或编码、内容编号（第五条）。
  - 用户要求导出不带显式标识的内容时，服务提供者需在用户协议里明确用户责任，并留存日志不少于 6 个月（第九条）。
  - 不得删除或篡改标识，也不得为此提供工具（第十条）。
- **GB 45438-2025《网络安全技术 人工智能生成合成内容标识方法》**（强制性国标，2025-09-01 实施）。来源：[标准 PDF](https://www.xiongan.gov.cn/20250617/99e8309670814bdba91b3bcbfaca4e6c/2025061799e8309670814bdba91b3bcbfaca4e6c_38598ff9004470443c9195f1655adb29a0.pdf)
  - 图片显式标识用文字，必须同时包含「人工智能」或「AI」，以及「生成」和/或「合成」。
  - 位置在图片的边或角，字高不低于最短边的 5%。
  - 隐式元数据字段含 "AIGC"。
- **对 Dsivio 意味着什么**：
  - 如果 Dsivio 只是本地客户端、BYOK 调第三方 API，Dsivio 自己是否算「服务提供者」需要律师判断（**未核实**）。
  - 稳妥做法：导出时默认加角标「AI 生成」（字高 ≥5% 短边），PNG/JPEG 写入 XMP/tEXt 的 AIGC 字段，用户协议里写明标识义务。
- **漫剧行业额外要求（据报道）**：全流程 AI 的作品正片前 5 秒固定展示不少于 3 秒的 AIGC 提示，每集单独标注（[飞天影业](https://www.feitianyingye.com/2026/0911/5946.shtml)，**未核实原始文件**）。

### 4.3 网络小说改编的版权

- **法律依据**：《著作权法》第十条（十四）规定了改编权；第二十三条规定自然人作品的财产权保护期为作者终生加死后 50 年（截至第 50 年的 12 月 31 日）。来源：[中国人大网](http://www.npc.gov.cn/npc/c2/c30834/202011/t20201119_308796.html)
  - 也就是说，**公版作品**（作者去世满 50 年，比如四大名著、鲁迅作品）可以改编。
  - 但要注意：广电 2026-01 开展过「AI 魔改」四大名著、历史题材、英模人物的专项治理。公版不等于可以随意魔改（[腾讯新闻/21世纪](https://news.qq.com/rain/a/20260410A03NHY00)）。
- **司法**：最高法《关于依法审理涉人工智能纠纷案件的意见》（法发〔2026〕10号，2026-09-07），第十二条：
  - 使用者明知或应知在先作品存在，生成实质相似作品且没有合理抗辩的，要担责。
  - 开发者、提供者的责任按「必要措施」等因素综合划分。
  - 来源：[最高法](https://www.court.gov.cn/zixun/xiangqing/511101.html)、[全文转载](https://www.elawcn.com/rule/2026/0907/1913.html)
- **判例**：天津和平区法院首例「文字作品改编 AI 漫剧」侵权案，被告把原告小说导入 AI 生成漫剧传播，法院认定实质性相似，构成侵犯改编权和信息网络传播权；最后调解，删除内容并赔偿。来源：[天津日报/新浪 2026-10-09](https://k.sina.cn/article_5953189932_162d6782c067050c9k.html?from=news)
- **平台签约作品**：番茄、阅文签约作品的改编权一般由平台代理，个人要走授权渠道：
  - 抖音版权中心：需签模式二/三，有配额，**不许做静态解说**。
  - 阅文火种计划。
  - 番茄 8-17 新规：没有版权的拉新视频单条不超过 15 分钟，不能连载（[红星新闻](https://finance.sina.com.cn/tech/roll/2026-08-21/doc-inipakut1675946.shtml)）。
- **对工具的启示**：内置「权利声明」关卡（原创 / 已授权 / 公版 / 仅私人试验），导出的成品里带声明，保留日志，作为「必要措施」的证据。

### 4.4 漫剧平台的审核与备案

- **2026-04-01 起**：AI 漫剧「先备案后上线」，未备案的存量作品强制下线。内容红线：低俗擦边、AI 颠覆性魔改经典和英雄人物、未经授权使用真人肖像；AI 内容要在片头或显著位置标注（[21世纪/腾讯新闻 2026-04-10](https://news.qq.com/rain/a/20260410A03NHY00)）。
- **2026-06-25 广电网络视听司《管理提示》，7-01 起执行**：AI 微短剧按投资额分层。80 万元及以上或特殊题材为「重点」；30–80 万元为「普通」；30 万元以下为「其他」，由平台审核报备（[飞天影业](https://www.feitianyingye.com/2026/0911/5946.shtml)、[虎嗅](https://m.huxiu.com/article/4871001.html)，原始文件未核实）。
- **《微短剧发展管理办法（征求意见稿）》**（2026-06-24），尚未正式施行（[广电总局](https://www.nrta.gov.cn/art/2026/6/24/art_113_73514.html)）。
- **平台侧**：红果、抖音 2026-04-07 起提高漫剧审核标准；红果发布《关于规范 AI 剧角色创作的公告》，治理「高频 AI 脸」和同质化；抖音 8-03 上线预检工具，可预检肖像权和版权（[红星新闻](https://finance.sina.com.cn/tech/roll/2026-08-21/doc-inipakut1675946.shtml)）。
- 据报道备案过审率不到 30%，累计清退超 7 万部（[飞天影业](https://www.feitianyingye.com/2026/0911/5946.shtml)，**未核实**）。
- **静态漫画**（图片发布）不属于微短剧备案范围；但一旦做成动态漫或视频上平台，就要走上面的流程（这是推断，未核实有没有针对静态漫画的专门规定）。

---

## 5. 机会判断

### 5.1 拥挤度（直说）
- **漫剧视频**：非常拥挤。大厂四家同时在做平台和工具，开源有 10 个以上千星项目，监管还在收紧。**不建议进入。**
- **静态小说转漫画 SaaS**：中等拥挤。海外有 LlamaGen、Dashtoon 等，国内有知漫剧、mushni 等。底层模型能力在快速商品化，单页原料成本 ¥0.2–0.5，零售价 $0.05–0.44，护城河薄。**不建议做成独立 SaaS 去正面竞争。**
- **桌面端、本地优先、BYOK、可编辑的「漫画工作台」插件**：竞品少。Inkstone、AI-Canvas-tauri 都很小，codex-novel-to-comic-studio 只是 CLI skill。**适合当 Dsivio 的一项能力。**
- **电商漫画（产品故事、四格广告、A+ 页面）**：几乎没看到专门的工具（检索有限，这是推断）。和你现有的 dsimage、dsvideo 用户重合，**是最现实的差异化切入点。**

### 5.2 两周 MVP（一个人）：Dsivio 插件 `dscomic`

| 天数 | 内容 |
|---|---|
| D1–2 | 插件骨架：复用 dsimage 的 provider 层（Nano Banana 2.1、Seedream、Qwen-Image、GPT Image），Rust 侧做任务队列和缓存；项目目录结构参考 codex-novel-to-comic-studio（source/、bible/、chapters/、exports/） |
| D3–4 | 导入 TXT/EPUB → LLM 生成故事圣经（角色、场景 JSON）→ 用户在 React 里编辑确认；**权利声明关卡** |
| D5–6 | 角色设定卡生成（三视图或表情）、风格样张，锁定为参考图 |
| D7–9 | 分页分格 JSON（景别、动作、对白）→ 整页提示词编译器（附 ≤4 张角色参考图，要求留白气泡）→ 批量出图，支持单页重画和 mask 单格重画 |
| D10–11 | 叠字层：SVG 气泡和文字，可拖拽，字体内置；LLM 给初始坐标 |
| D12 | 导出 PNG、PDF、CBZ、条漫长图；**自动加 AIGC 角标（≥5% 短边）和元数据隐式标识** |
| D13 | 一键送 dsvideo-plugin 做动态漫（镜头推拉加配音）；电商模板（产品四格、开箱故事） |
| D14 | 用 1 部公版短篇和 1 个自家产品故事做 demo，记录每页实际成本和重画率 |

**MVP 先不做**：LoRA 训练、本地 GPU 模型、自动 VLM 质检（可以留一个人工评分入口）、多人协作、平台发布。

### 5.3 能不能做成 Dsivio 插件
- **能**。核心都是 API 调用加前端编辑，和 dsimage、dsvideo 同一套架构。Tauri 2 + React 很适合做叠字画布；Rust 侧负责并发出图、写 EPUB/CBZ、写 PNG 元数据。
- 也可以把 LLM 分镜那一段包装成 skill（参考 zenstory-ai/drama-skills、shuohao-skills 的 skill 化写法），让 Dsivio 的 agent 能直接调用。

### 5.4 差异化
1. 本地优先加 BYOK，切换模型就能比价（Seedream 和 Qwen 每页约 ¥0.3，Nano Banana Pro 每页约 ¥1.4）。
2. 文字层可编辑、支持多语言，适合出海电商和条漫翻译。
3. 合规内建：AIGC 标识、权利关卡、日志。
4. 电商场景模板，加上和 dsimage、dsvideo 的联动（漫画 → 动态漫 → 广告视频）。

### 5.5 主要风险
| 风险 | 程度 | 缓解 |
|---|---|---|
| 用户拿受保护的网文去生成并传播，工具被卷入 | 高 | 权利关卡、声明、日志；不内置任何网文抓取 |
| 同质化：模型厂（ChatGPT、Gemini App）或平台把功能做进去 | 高 | 定位成 Dsivio 的一项能力而不是独立产品；绑定电商工作流 |
| 国内静态漫画变现窄（番茄 IP 库禁止静态解说） | 中高 | 主攻电商、品牌和海外条漫 |
| 中文文字和一致性不稳，重画成本超预期 | 中 | 后期叠字、多图参考、按页预估成本并显示给用户 |
| 监管变化（标识、备案范围扩大） | 中 | 标识默认开启；视频输出时提示备案 |
| 模型价格和型号频繁变化（Gemini 2.5 Flash Image 已在 2026-10-02 下线） | 中 | provider 抽象，价格表可远程更新 |

---

## 附：主要来源清单
- 定价：[Google Gemini API Pricing](https://ai.google.dev/gemini-api/docs/pricing)｜[Gemini 图像生成文档](https://ai.google.dev/gemini-api/docs/image-generation)｜[OpenAI Pricing](https://platform.openai.com/docs/pricing)｜[OpenAI 图像指南](https://developers.openai.com/api/docs/guides/image-generation)｜[阿里云 qwen-image-3.0](https://help.aliyun.com/zh/model-studio/qwen-image-3-0)｜[BFL](https://bfl.ai/pricing)｜Seedream（二手）：[LaoZhang](https://blog.laozhang.ai/zh/posts/seedream-5-pro-layer-decomposition-api)
- 法规：[标识办法](https://www.cac.gov.cn/2025-03/14/c_1743654684782215.htm)｜[GB 45438-2025](https://www.xiongan.gov.cn/20250617/99e8309670814bdba91b3bcbfaca4e6c/2025061799e8309670814bdba91b3bcbfaca4e6c_38598ff9004470443c9195f1655adb29a0.pdf)｜[著作权法](http://www.npc.gov.cn/npc/c2/c30834/202011/t20201119_308796.html)｜[最高法 AI 意见](https://www.court.gov.cn/zixun/xiangqing/511101.html)｜[微短剧管理办法征求意见稿](https://www.nrta.gov.cn/art/2026/6/24/art_113_73514.html)
- 行业：见正文各表链接。
