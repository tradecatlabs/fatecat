# FateCat

<p align="center">
  <img src="./docs/reference-materials/fatecat-readme-banner.svg" alt="FateCat Banner" width="100%">
</p>

<div align="center">

**FateCat 是面向 Agent 与应用开发者的测算基础设施，提供统一的能力协议、可复现计算核心、证据化解释层和多端交付接口。**

**统一能力协议 × 可复现计算核心 × 证据化解释层 × CLI / Web / Telegram / FastAPI / Agent 多端交付接口**

<p>
  <a href="https://tradecatlabs-fatecat.hf.space/web"><strong>立即免费使用 FateCat Web 工作台</strong></a>
</p>

<p>
  <a href="https://tradecatlabs-fatecat.hf.space/web"><img src="https://img.shields.io/badge/Hugging%20Face-Web%20Demo-FFD21E?style=for-the-badge&logo=huggingface&logoColor=111827" alt="FateCat Hugging Face Web Demo"></a>
  <a href="https://github.com/tradecatlabs/fatecat"><img src="https://img.shields.io/github/stars/tradecatlabs/fatecat?style=for-the-badge&label=Stars" alt="GitHub Stars"></a>
  <a href="https://github.com/tradecatlabs/fatecat"><img src="https://img.shields.io/github/languages/top/tradecatlabs/fatecat?style=for-the-badge&label=Top%20Language" alt="Top Language"></a>
  <a href="https://github.com/tradecatlabs/fatecat"><img src="https://img.shields.io/github/languages/code-size/tradecatlabs/fatecat?style=for-the-badge&label=Code%20Size" alt="Code Size"></a>
  <img src="https://img.shields.io/badge/License-MIT-2EA44F?style=for-the-badge" alt="MIT License">
  <img src="https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.12+">
  <img src="https://img.shields.io/badge/Skill-Codex%20Ready-111827?style=for-the-badge" alt="Codex Skill Ready">
  <img src="https://img.shields.io/badge/Delivery-Web%20%2F%20Telegram%20%2F%20FastAPI-26A5E4?style=for-the-badge" alt="Web Telegram FastAPI">
  <img src="https://img.shields.io/badge/Lab-TradeCat%20Labs-FF6A00?style=for-the-badge" alt="TradeCat Labs">
</p>

<p>
  <a href="#overview">项目总览</a> ·
  <a href="#skill-repo">Skill 仓库</a> ·
  <a href="#modes">模式选择</a> ·
  <a href="#architecture">架构</a> ·
  <a href="#quick-start">快速开始</a> ·
  <a href="#web">Web HTML</a> ·
  <a href="#hf-space">HF 免费部署</a> ·
  <a href="#report-structure">报告结构</a> ·
  <a href="#commands">常用命令</a> ·
  <a href="#layout">目录结构</a> ·
  <a href="#hygiene">仓库卫生</a> ·
  <a href="#docs">文档地图</a> ·
  <a href="#disclaimer">免责声明</a>
</p>

</div>

> [!WARNING]
> 本项目及 AI 分析结果仅供传统文化研究、算法测试与娱乐参考。命理学非精密科学，命运掌握在自己手中。使用者因轻信或误读本程序结果而产生的任何心理、财务及生活决策后果，本开源项目及开发者概不负责。

> [!TIP]
> `FateCat` 是 `TradeCat Labs` 的测算基础设施项目。推荐工作流：先由成熟算法或生产 capability 完成确定性计算，再把结构化结果交给 AI / Agent 深度分析，尽量减少模型乱编。
>
> - DEX Screener: `https://dexscreener.com/bsc/0x8a99b8d53eff6bc331af529af74ad267f3167777`
> - X: `https://x.com/tradecatlabs`
> - GitHub: `https://github.com/tradecatlabs`
> - Hugging Face: `https://huggingface.co/tradecatlabs`
> - FateCat Repo: `https://github.com/tradecatlabs/fatecat`
> - CA: `0x8a99b8d53eff6bc331af529af74ad267f3167777`

### AI / Agent 机器发现入口

| 资源 | 用途 |
|---|---|
| [llms.txt](https://tradecatlabs-fatecat.hf.space/llms.txt) | 产品身份、能力状态、输入契约、证据来源、高意图问答和引用边界 |
| [robots.txt](https://tradecatlabs-fatecat.hf.space/robots.txt) | 公开抓取策略与 sitemap 发现 |
| [sitemap.xml](https://tradecatlabs-fatecat.hf.space/sitemap.xml) | Web、OpenAPI 与机器资源索引 |
| [OpenAPI](https://tradecatlabs-fatecat.hf.space/openapi.json) | 当前 HTTP 请求和响应契约 |
| [Capability Registry](https://tradecatlabs-fatecat.hf.space/api/v1/capabilities) | production 与 planned 能力的实时真相源 |

GEO 方法、当前基线、指标口径和复测命令见 [GEO 发现与引用治理](docs/geo.md)。项目不承诺任何 AI 平台必然收录、引用或推荐；公开事实必须能回指代码、契约、测试或运行端点。

<a id="overview"></a>

## 项目总览

FateCat 是面向 Agent 与应用开发者的测算基础设施，提供统一的能力协议、可复现计算核心、证据化解释层和多端交付接口。它不是让 AI 直接“脑补排盘”，而是把“确定性计算”和“解释交付”拆开：

1. 成熟排盘系统、外部算法或生产 capability 负责可复现结构化计算。
2. FateCat 负责统一能力协议、统一字段、统一证据链、统一输出和统一交付入口。
3. AI / Agent 只基于稳定 JSON 或标准 Markdown 做解释、总结与后续任务。

| 维度 | 说明 |
|------|------|
| 项目角色 | 面向 Agent 与应用开发者的测算基础设施 |
| 当前形态 | 企业级系统仓库；源码、运行资产、契约、治理和导出入口均从 canonical roots 解析 |
| 推荐链路 | `成熟算法 / capability provider` -> `FateCat capability executor` -> `AI / Web / Telegram / API / Agent` |
| 核心真相源 | 目标为 `contracts/fate/` 定义字段与 capability 契约，`tools/reference-repos/` 或供应链 manifest 保留成熟算法快照 |
| 明确边界 | 不让 AI 直接口算排盘，不在 vendor 快照内魔改外部源码；复用先于自写 |

<a id="skill-repo"></a>

## 企业级仓库

当前根仓库承担 5 个职责：

- 单-skill 仓库入口：`SKILL.md` 定义 agent 如何接手、安装、检查、执行。
- 企业治理层：`governance/` 记录标准、门禁、迁移账本、baseline evidence、任务和风险。
- 领域服务层：`domains/fate-analysis/services/fate-core/` 与 `domains/experience-delivery/services/fatecat-delivery/` 登记生产候选服务契约。
- 统一执行包装层：根 `scripts/` 把源码仓库常用动作封成稳定入口。
- 可导出 bundle 源：可把当前 skill 连同运行时骨架导出为独立交付包。

生产候选源码当前归位：

- `domains/fate-analysis/services/fate-core/src/`：测算计算、能力执行与解释证据核心。
- `domains/experience-delivery/services/fatecat-delivery/src/`：Web HTML、Telegram、FastAPI、报告生成与交付适配。

企业根运行资产当前归位：

- `infra/environments/local/`：本地配置模板与 branding。
- `infra/databases/` 与 `infra/runtime/local-state/`：数据库 schema 与本地运行态目录。
- `contracts/fate/`：capability、profile、evidence、policy 和典籍规则契约。
- `domains/fate-analysis/data-products/`：可提交数据产品与 golden fixtures。
- `tools/reference-repos/`：第三方成熟算法快照，默认只读。

旧组织退役证据见 `governance/migration/fatecat-enterprise-directory-mapping.md` 与 `governance/tasks/project-history/`。

<a id="modes"></a>

## 模式选择

| 场景 | 推荐入口 | 输出形态 | 是否要求 `FATE_BOT_TOKEN` | 说明 |
|------|----------|----------|---------------------------|------|
| 本地调试、脚本串联、先排盘再喂 AI | `bash scripts/pure-analysis.sh` | `stdout JSON` / 文件 JSON | 否 | 最稳定、最适合结构化输出 |
| 人类在浏览器中录入并复制报告 | `bash scripts/serve-api.sh` -> `/web` | HTML 表单 + Markdown | 否 | 直接输入出生信息，输出可复制 Markdown |
| 要接服务、工作流、上层系统 | `bash scripts/serve-api.sh` | HTTP JSON | 否 | 适合 Webhook、自动化平台、自建前端 |
| 想直接聊天式使用 | `bash scripts/serve-bot.sh` | Telegram 消息 / 报告文件 | 是 | 人工交互最直接 |
| OpenClaw / Harness / 自动化 Agent | 企业根自举入口 | 非交互 CLI / 健康检查 | 纯分析否，Bot 是 | 适合批处理与自动部署 |
| 用户自己免费云端部署 | HF Duplicate / GitHub Actions | Hugging Face `/web` | 否 | 不用本机保活；详见 `docs/deployment/huggingface-space.md` |

<a id="architecture"></a>

## 架构

```mermaid
flowchart LR
    A[成熟算法 / capability provider] --> B[外部成熟算法 tools/reference-repos]
    B --> C[fate-core 测算能力执行服务 domains/fate-analysis]
    F[capability / profile / evidence contracts/fate] --> C
    G[配置 / 数据 / schema infra + data-products] --> C
    C --> D[稳定 JSON + branding + disclaimer]
    D --> E1[CLI]
    D --> E2[Web HTML /web]
    D --> E3[FastAPI JSON]
    D --> E4[Telegram Bot]
    D --> E5[Agent / Skill]
    H[runtime 数据库 / 日志] --> E3
    H --> E4
```

推荐工作流：

```text
成熟算法 / capability provider
        ↓
FateCat capability executor 输出稳定 JSON / Markdown
        ↓
AI 基于结构化字段和 evidence 做解释
        ↓
Web / Telegram / API / Agent 继续交付
```

<a id="quick-start"></a>

## 快速开始

### 1. 首次准备运行时

```bash
bash scripts/bootstrap.sh --with-dev
```

只需要最小运行时：

```bash
bash scripts/bootstrap.sh
```

### 2. 先做标准预检

```bash
bash scripts/preflight.sh --mode pure --bootstrap --pretty
```

交付层检查：

```bash
bash scripts/preflight.sh --mode delivery --bootstrap --pretty
```

### 3. 本地 CI/CD profile

```bash
bash scripts/local-ci.sh --profile quick
bash scripts/local-ci.sh --profile full
bash scripts/local-ci.sh --profile container
bash scripts/local-ci.sh --profile public-service
```

`local-ci.sh` 只调用本仓脚本，不调用 GitHub Actions；`quick` 会检查 wheel clean-room、核心性能预算和关键回归，`full` 复用本地 `scripts/acceptance.sh --with-dev`，`container` 执行真实 Docker 容器 smoke，`public-service` 执行公网服务静态准入门禁。GitHub `quick.yml` 在 pull request 与 `main` push 自动执行同一个 quick profile。

公开 Web 工作台发布前使用：

```bash
bash scripts/public-release-gate.sh --api-url https://tradecatlabs-fatecat.hf.space
```

该门禁仍只调用本地脚本：quick CI、公开发布策略检查、公共导出许可检查、delivery smoke、生产静态准入和可选线上 `/health` / `/ready` / `/metrics`。GitHub Acceptance 和容器工作流只保留手动触发，避免 push 自动跑重型验收。

### 4. 执行一次命理排盘并输出文件

```bash
mkdir -p output
bash scripts/pure-analysis.sh \
  --input-json '{"birthDateTime":"1990-01-01 08:00:00","gender":"男","longitude":116.4074,"latitude":39.9042,"birthPlace":"北京市","name":"测试样本"}' \
  --output-file output/bazi-result.json \
  --pretty
```

### 5. 做完整验收

```bash
bash scripts/local-ci.sh --profile full
```

完整验收覆盖 shell 语法、strict skill 校验、纯分析 smoke、vendor health、wheel clean-room、核心性能预算、全量 pytest、ruff、format、`fate_core` mypy、API/Bot dry-run、导出包卫生检查与导出包 smoke。
其中 pytest 已包含 1900-2030 节气 golden、月令/立春边界、起运样本、综合八字报告结构、隐私脱敏和 evidence 权重策略回归。

<a id="web"></a>

## Web HTML

Web 版遵循零美化语义界面：原生 HTML 表单、服务端直出、psql ASCII 字段表、Markdown 原文 `<pre><code>` 展示、复制按钮只做渐进增强。公开入口默认使用异步报告任务：浏览器提交后先拿到 `jobId`，后端有界队列生成报告，页面轮询完成后回到 `/web?jobId=...` 展示 Markdown。

面向 AI、Agent 和抓取器的公开端点、Web 字段契约、地点解析、任务协议与风险边界集中在 [`llms.txt`](llms.txt)，线上入口为 `GET /llms.txt`；Web 顶部表格只保留人类需要的项目和使用摘要。

项目归属块提供 `免费 AI 分析入口（Gemini Gem）` 外链。该入口用于用户复制 Markdown 报告后自行打开 Gemini Gem 分析；FateCat 不会自动把排盘输入或报告发送给 Gemini。

启动 API：

```bash
bash scripts/preflight.sh --mode delivery --bootstrap --pretty
bash scripts/delivery-smoke.sh --target api
bash scripts/serve-api.sh
```

访问：

```text
http://127.0.0.1:8001/web
```

字段契约：

| 字段 | 必填 | 说明 |
|------|------|------|
| 出生日期 | 是 | `YYYY-MM-DD` |
| 出生时间 | 是 | `HH:MM` 或 `HH:MM:SS` |
| 地区模式 | 是 | `domestic` / `overseas` / `coordinates` |
| 出生地区 | 是 | 地点名称或 WGS84 `lng,lat`；文本重名时必须从候选中选择稳定地点 ID |
| 稳定地点 ID | 条件必填 | 搜索候选后使用 `cn:<code>` 或 `geonames:<id>`；直接坐标模式由服务端生成 |
| 出生时间口径 | 是 | `local_civil` / `beijing_time` / `utc`；不得默认猜测 |
| DST 重复时刻 | 条件必填 | 夏令时回拨产生重复当地时间时选择 `earlier` / `later` |
| 性别 | 是 | `male` / `female`；现有排盘逻辑必需，不能默认猜测 |
| 输出体系 | 否 | 当前可用：`bazi` / `ziwei`；默认 `bazi`，每次只输出一个已实现体系 |
| 姓名 | 否 | 为空时报告标题使用“命主” |

地点规则：国内与海外候选统一返回稳定 ID、WGS84 坐标、IANA 时区和坐标精度。重名、模糊地点、DST 缺口或重复时刻均显式报错；经纬度、时区和规范化时间用于后端计算，不写入免费 Space 记录库。

报告任务 API：

```text
POST /api/v1/report/jobs
GET /api/v1/report/jobs/{job_id}
POST /api/v1/report/jobs/web
```

免费公开版使用进程内有界队列，默认 1 个 worker、最多 20 个等待任务、结果 TTL 30 分钟。它解决浏览器同步等待和平台超时问题；如果自部署需要多副本高并发、跨重启保留任务或独立 worker 扩容，应把任务后端升级为 Redis/RQ、Celery 或同等级外部队列。

<a id="hf-space"></a>

## Hugging Face 免费 Space

FateCat 提供 Hugging Face Docker Space 分发模板，目标是让用户直接通过 Web 工作台使用 `/web`。免费公共演示默认关闭记录存储，不需要 Telegram Bot token，也不写入本地数据库。

用户自助部署有两条无需本机服务器的路径：

- HF 网页复制：打开 `https://huggingface.co/spaces/tradecatlabs/fatecat`，右上角三个点选择 `Duplicate this Space`，按页面提示选择 owner、Space name、visibility 和 CPU Basic。
- GitHub 网页部署：fork `https://github.com/tradecatlabs/fatecat`，在 fork 仓库添加 `HF_TOKEN` secret，然后到 `Actions -> Deploy Hugging Face Space -> Run workflow`，填写 `<你的HF用户名>/fatecat`。该部署 workflow 是手动触发，不会因为 push 自动发布。

完整说明见 `docs/deployment/huggingface-space.md`。

本地 hf CLI 部署：

```bash
hf auth login
bash scripts/hf-space-deploy.sh --space tradecatlabs/fatecat
```

只生成并检查分发包，不上传：

```bash
bash scripts/hf-space-deploy.sh --dry-run --bundle-dir /tmp/fatecat-hf-space
```

部署脚本默认校验当前 hf 认证必须属于 `tradecatlabs` 用户或显示 `tradecatlabs` org 权限，避免误发到个人账号。Space 模板位于 `infra/huggingface-space/`，运行端口为 `7860`，默认环境变量包含：

```text
FATE_RECORDS_ENABLED=0
FATE_SERVICE_PORT=7860
FATE_MAX_INFLIGHT_CALCULATIONS=1
FATE_REPORT_JOB_QUEUE_SIZE=20
FATE_REPORT_JOB_WORKERS=1
FATE_REPORT_JOB_TTL_SECONDS=1800
FATE_TELEGRAM_WEBHOOK_ENABLED=0
```

可选 Telegram 消费端与 FastAPI 运行在同一进程，通过
`POST /api/v1/integrations/telegram/webhook` 接收 Update，并继续复用 Bot 现有
`calculation_service -> fate-core -> report_generator` 链路。不要把 Space 改为 `start.py both`。
启用时在 Space Secrets 配置 `FATE_BOT_TOKEN`、`FATE_TELEGRAM_WEBHOOK_SECRET`，再把
Variable `FATE_TELEGRAM_WEBHOOK_ENABLED` 设为 `1`；Webhook URL 默认从 `SPACE_HOST` 推导。

<a id="report-structure"></a>

## 标准 Markdown 报告结构

默认 Markdown 输出综合八字体系，包含八字主线和袁天罡称骨民俗辅助。紫微斗数作为独立体系保留，既可通过 Web HTML 的“输出体系”控件、Telegram 确认页按钮或 API `options.reportSystem` 单独选择，也已作为 `ziwei` production capability 进入统一协议；它仍不和综合八字一起输出。黄历/择日已作为 `almanac` 生产 capability 独立提供 CLI/API 调用，梅花易数已作为 `meihua` production capability 提供轻量问事盘面，但二者都不进入默认 Markdown 报告；六爻、奇门、大六壬、风水九星、姓名合婚等仍是未来 capability，不允许混入综合八字默认报告。

综合八字 JSON 结果包含默认隐藏的 `analysisEvidence` 与 `accuracyGuards`，用于审计日主、五行喜忌、格局、干支关系、真太阳时、节气月令、起运边界、神煞和袁天罡称骨的依据、来源、规则 ID 与权重。这些字段不渲染到默认 Markdown 正文，避免用户报告变成技术附录。

可选体系：

| 值 | 输出体系 | 状态 | 是否与八字混排 |
|----|----------|------|----------------|
| `bazi` | 综合八字 | 当前可用 | 否；默认输出八字主线与袁天罡称骨 |
| `ziwei` | 紫微斗数 | 当前可用 / 独立 capability 可用 | 否；独立输出紫微斗数、紫微基础、紫微运限四化 |
| `almanac` | 黄历/择日 | 独立 capability 可用 | 否；通过 `fatecat capability almanac` 或 `/api/v1/capabilities/almanac` 调用，不属于 Markdown 报告体系 |
| `meihua` | 梅花易数 | 独立 capability 可用 | 否；通过 `fatecat capability meihua` 或 `/api/v1/capabilities/meihua` 调用，只输出盘面与证据 |
| `liuyao` | 六爻占卜 | 未来功能 | 否；事件型起卦 |
| `qimen` | 奇门遁甲 | 未来功能 | 否；独立排盘 |
| `liuren` | 大六壬 | 未来功能 | 否；独立排盘 |
| `fengshui` | 风水九星 | 未来功能 | 否；方位/山向/门向输入 |
| `name_marriage` | 姓名合婚 | 未来功能 | 否；姓名学与合婚输入 |
| `yijing` | 易经系统 | 未来功能 | 否；卦辞与起卦体系 |

API 生成 Markdown 的入口：

```text
POST /api/v1/report/markdown
```

请求体沿用 `BaziRequest`，在 `options.reportSystem` 中传入当前已实现的 `bazi` 或 `ziwei`。体系清单入口：

```text
GET /api/v1/report/systems
```

结构化 capability 入口：

```text
GET /api/v1/capabilities
POST /api/v1/capabilities/almanac
POST /api/v1/capabilities/ziwei
```

默认 `bazi` 输出块顺序固定如下：

```text
免责声明（纯文本，无 # 标题）

## TradeCat Labs 实验室

# 命理排盘报告：{姓名}

## 第一卷：先天命格（静态分析）
  ## 基本资料（含真太阳时、节气）
    ### 基本资料
  ## 八字排盘详情
    ### 五行分数
    ### 天干分数
    ### 温湿度与拱神
    ### 干支合克与入库
      #### 干支相合（依据）
      #### 天干相克（依据）
      #### 地支入库（依据）
    ### 地支关系
  ## 神煞断语
    ### 简表神煞（字段展开）
  ## 日主概览
  ## 五行喜忌（调候与平衡）
    ### 五行比例
    ### 五行分数
    ### 天干分数
  ## 五行停匀与寒湿燥热（调候依据）
  ## 干支取象（原文）
  ## 命造格局（格局用神）
  ## 节气司令
  ## 干支关系

## 第二卷：后天运路（动态趋势）
  ## 运势分析
    ### 大运分析
    ### 流年
    ### 流月运势
    ### 小运

## 第三卷：民俗与建议（生活应用）
  ## 袁天罡称骨
```

体系归属：

| 输出块 | 体系归属 | 说明 |
|--------|----------|------|
| 基本资料（含真太阳时、节气） | 八字排盘前置 | 出生时空、真太阳时、节气是八字排盘与月令判断的基础；若展示星座、星宿，只作历法/民俗辅助 |
| 八字排盘详情 | 八字主线 | 四柱、五行、天干地支、合克、入库、地支关系 |
| 神煞断语 | 八字辅助体系 | 属传统命理常见辅助，不等同于格局用神主线 |
| 日主概览 | 八字主线 | 日主、阴阳五行、强弱与坐支 |
| 五行喜忌（调候与平衡） | 八字主线 | 五行比例、分数、调候与平衡 |
| 五行停匀与寒湿燥热（调候依据） | 八字主线 | 月令气候、寒暖燥湿、调候依据 |
| 干支取象（原文） | 八字经典辅助 | 干支象义，服务八字解释 |
| 命造格局（格局用神） | 八字主线 | 格局、用神、调候取用 |
| 节气司令 | 八字主线 | 月令、人元司令与节气分野 |
| 干支关系 | 八字主线 | 干支合冲刑害破等结构关系 |
| 运势分析：大运、流年、流月、小运 | 八字动态主线 | 八字后天运路与应期分析 |
| 建除十二神 | 已退役为未来功能 | 属黄历/择日辅助，不再作为当前命理报告体系输出 |
| 紫微斗数 / 紫微基础 | 其他独立体系 | 紫微斗数独立于八字，需选择 `ziwei` 单独输出 |
| 紫微运限四化 | 其他体系 | 紫微大限、流年、流月、流日、流时 |
| 袁天罡称骨 | 综合八字民俗辅助 | 称骨法随默认 `bazi` 报告输出，不再单独作为体系选择 |

<a id="commands"></a>

## 常用命令

```bash
bash scripts/bootstrap.sh --with-dev
bash scripts/local-ci.sh --profile quick
bash scripts/local-ci.sh --profile full
bash scripts/local-ci.sh --profile container
bash scripts/local-ci.sh --profile public-service
bash scripts/preflight.sh --mode pure --bootstrap --pretty
bash scripts/preflight.sh --mode pure --bootstrap --smoke --output-file output/preflight-sample.json --pretty
bash scripts/preflight.sh --mode delivery --bootstrap --pretty
bash scripts/pure-analysis.sh --input-file input.json --output-file output/result.json --pretty
bash scripts/delivery-smoke.sh --target api
bash scripts/serve-api.sh
bash scripts/delivery-smoke.sh --target bot --startup-timeout 8
bash scripts/production-readiness.sh --api-url https://your-domain.example --require-live-bot
bash scripts/hf-space-deploy.sh --dry-run --bundle-dir /tmp/fatecat-hf-space
bash scripts/hf-space-deploy.sh --space tradecatlabs/fatecat
bash scripts/clean-runtime.sh --dry-run
bash scripts/export-runtime.sh --output-parent /tmp/fatecat-export --mode lite
bash scripts/check-export-hygiene.sh /tmp/fatecat-export/fatecat
```

<a id="layout"></a>

## 目录结构

```text
fatecat/
├── AGENTS.md
├── README.md
├── SKILL.md
├── apps/
├── ai/
├── domains/
│   ├── fate-analysis/
│   │   └── services/fate-core/
│   └── experience-delivery/
│       └── services/fatecat-delivery/
├── platform/
├── infra/
├── contracts/
├── catalog/
├── governance/
├── shared/
├── tools/
├── docs/
├── tests/
├── references/
│   ├── commands.md
│   ├── execution-playbook.md
│   └── troubleshooting.md
├── scripts/
│   ├── acceptance.sh
│   ├── check-export-hygiene.sh
│   ├── clean-runtime.sh
│   ├── delivery-smoke.sh
│   ├── export-runtime.sh
│   ├── local-ci.sh
│   └── preflight.sh
```

企业根 canonical 边界：

- 企业根：服务契约、catalog、governance、目标 docs/contracts/infra/tools 归位。
- `domains/*/services/*`：生产候选服务源码、服务契约和测试入口。
- 根 `scripts/`：预检、验收、导出、结构门禁和卫生门禁。
- vendor 快照：默认只读；后续只做供应链登记与路径归位，不魔改源码。

<a id="hygiene"></a>

## 仓库卫生

默认卫生规则：

- 不提交 `infra/environments/local/.env`。
- 不提交 `.venv`、`.pytest_cache`、`.ruff_cache`、`.mypy_cache`。
- 不提交或分发本地编辑器历史 `.history/`。
- 不分发 `node_modules/`。
- 不分发 `__pycache__`、`*.pyc`、`*.pyo`。
- 不把 `domains/*/services/*/output/`、运行态 `.db` / `.sqlite` 或本地 `.env` 放进导出包。
- 导出后必须运行 `scripts/check-export-hygiene.sh`。
- 内部 lite 运行包与公共分发包使用不同门禁：公共发布必须追加 `--public`，任何 `distributionAllowed != true` 的 vendor 都会阻断。
- 当前 `bazi-1` 与 `sxwnl` 缺少可确认的上游分发许可证，因此不得把包含它们的内部运行包称为可公开分发包。
- `tools/reference-repos/` 保存完整外部快照，体积偏大属于当前复用完整源码能力的明确取舍；如需瘦身，必须先改成 manifest / Git LFS / 按需下载方案，不能直接删除运行依赖。

API 安全开关：

- `FATE_CORS_ALLOW_ORIGINS`：逗号分隔 CORS allowlist；默认空列表，不再默认 `*`。
- `FATE_API_TOKEN` / `FATE_API_ADMIN_TOKEN`：记录接口 admin token；admin 可访问全部记录。
- `FATE_API_USER_TOKENS`：用户级 token，格式为 `user_id:token,user_id2:token2`；用户 token 只能写入、读取、列出、删除自己的记录。
- 未配置任何 API token 时，记录接口返回“记录接口未启用”，避免公网误暴露。
- `FATE_MAX_REQUEST_BYTES`：应用层请求体上限；同时建议在 Nginx / Traefik / Cloudflare 等边缘层配置 body limit。
- `FATE_RATE_LIMIT_PER_MINUTE`：应用内单 IP 每分钟限流；仅适合单副本兜底。
- `FATE_DEPLOYMENT_REPLICAS` + `FATE_RATE_LIMIT_BACKEND`：多副本公网服务必须把 `FATE_RATE_LIMIT_BACKEND` 设为 `gateway`、`redis`、`waf` 或 `external`，不能继续用单进程 `memory`。
- `FATE_TRUST_PROXY_HEADERS` / `FATE_ENABLE_HSTS`：生产反向代理后建议开启；确保直连端口只允许可信代理访问。
- 公网生产前运行 `bash scripts/production-readiness.sh --api-url <url> --require-live-bot`，缺少真实外部环境时不得宣称 live 验收通过。

清理本地运行态：

```bash
bash scripts/clean-runtime.sh
```

导出并检查：

```bash
rm -rf /tmp/fatecat-export
bash scripts/export-runtime.sh --output-parent /tmp/fatecat-export --mode lite
bash scripts/check-export-hygiene.sh /tmp/fatecat-export/fatecat
```

<a id="docs"></a>

## 文档地图

- [SKILL.md](SKILL.md)：agent 如何接手、预检、执行、验收。
- [references/index.md](references/index.md)：参考文档导航。
- [references/execution-playbook.md](references/execution-playbook.md)：标准执行链路。
- [references/commands.md](references/commands.md)：命令速查。
- [references/ops-pack.md](references/ops-pack.md)：运维与加固。
- [docs/reference-materials/README.md](docs/reference-materials/README.md)：项目级产品说明与业务背景归位副本。
- [docs/reference-materials/reference/功能状态.md](docs/reference-materials/reference/功能状态.md)：标准报告与未来功能边界。
- [docs/reference-materials/reference/综合八字陈述服务加固.md](docs/reference-materials/reference/综合八字陈述服务加固.md)：综合八字报告、节气 golden、evidence 与验收门禁。

<a id="disclaimer"></a>

## 免责声明

本项目及 AI 分析结果仅供传统文化研究、算法测试与娱乐参考。命理学非精密科学，命运掌握在自己手中。使用者因轻信或误读本程序结果而产生的任何心理、财务及生活决策后果，本开源项目及开发者概不负责。
