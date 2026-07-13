# FateCat GEO 发现与引用治理

最后审阅：2026-07-14（Asia/Hong_Kong）
负责人：TradeCat Labs
方法来源：`/home/lenovo/.projects/geo` 固定上游中的 `yao-geo-panorama-audit`、`yao-geo-page-audit`、`yao-geo-brand-graph`、`yao-geo-tracking` 与 `yao-geo-effect-monitor`。

## 目标与边界

FateCat 的 GEO 目标是提高公开项目被搜索引擎、AI 问答系统和 Agent 正确发现、解析、引用和集成的概率。优化只发布可由仓库契约、源码、测试、CI 或线上端点证明的事实，不制造关键词页、伪造第三方背书、虚构引用率，也不承诺任何平台必然收录或推荐。

## 2026-07-13 基线

| 诊断域 | 改造前证据 | 改造后目标 | 验证方式 |
|---|---|---|---|
| 根入口 | `/` 返回 404 | 308 到 `/web` | `geo-audit.py` |
| 抓取策略 | `/robots.txt` 返回 404 | 200，声明 sitemap 与受限运行端点 | HTTP + 文本断言 |
| 站点地图 | `/sitemap.xml` 返回 404 | 200，可解析 XML，覆盖稳定公开资源 | XML 解析 |
| 规范 URL | Web 无 canonical | `/web` 使用公开绝对 canonical | HTML 断言 |
| 实体结构 | Web 无 JSON-LD | Organization、SoftwareApplication、WebSite、WebApplication | JSON 解析 |
| 机器事实 | `llms.txt` 以接口说明为主 | 身份、能力矩阵、来源、问答、引用与风险边界 | 章节门禁 |
| 能力真相 | Web 与 API 状态容易混淆 | Web、production API、planned 三层明确分开 | registry 对照 |
| 作者与新鲜度 | Web 缺作者与更新时间 | author 与 date 元数据 | HTML 断言 |
| 可重复验证 | 无 GEO 专项命令 | 本地/线上统一 JSON 审计 | `scripts/geo-audit.py` |

## 第二阶段：可引用权威页

第一阶段解决“能否被发现”，第二阶段解决“发现后是否有可独立引用的正文”。`/about` 是无 CSS、服务端直出的公开权威说明页，包含答案前置摘要、项目事实、实时 capability 生命周期表、计算与解释边界、Agent 接入步骤、来源复核入口、可见 FAQ、风险与隐私边界。页面正文与 `TechArticle`、`FAQPage` JSON-LD 共用同一问答事实源，避免结构化数据与用户可见内容不一致。

GitHub 仓库元数据必须同步维护项目描述、公开主页和主题标签；它们用于仓库发现，不替代 README、`llms.txt`、实时注册表或源码证据。任何标签都必须描述项目真实能力，禁止添加未实现体系或泛化流量词。

## 第三阶段：旗舰能力权威页与采样基线

项目总览无法独立承载每个能力的高意图问题。`/guides/bazi` 与 `/guides/ziwei` 只面向同时达到 L4、production 和 Web 可用的两个旗舰 capability，分别公开答案前置摘要、输入、引擎版本、确定性、证据要求、能力范围、禁止声明、来源和 FAQ。动态字段来自 capability registry；正文、`DefinedTerm`、`TechArticle`、`BreadcrumbList` 与 `FAQPage` 共用同一事实源。L3、planned 或没有 Web 交付面的能力不会自动生成页面。

`contracts/fate/discovery/query-set.json` 固定品牌验证、能力、接入、证据、隐私和风险六组问题。每题只登记预期事实、官方来源与禁止声明，不保存虚构答案、排名、推荐或引用率。`scripts/geo-query-set-gate.py` 负责拒绝无来源题目、重复 ID、结果字段和外部指标越界；真实采样仍需要平台、时间、答案、采集人和引用 URL 证据。

## 事实与实体模型

规范实体包括 TradeCat Labs、FateCat、FateCat Web 和公开站点。关系只使用公开证据：TradeCat Labs 发布 FateCat；FateCat 提供 capability、evidence 与多端交付；Web 暴露独立的综合八字和紫微报告。`contracts/fate/capabilities/registry.json` 是能力生命周期真相源，`llms.txt` 不得把 `planned` 写成已实现。

## 指标体系

| 指标 | 计算口径 | 当前状态 | 数据要求 |
|---|---|---|---|
| 技术发现通过率 | GEO 审计通过项 / 总项 | 仓库内可测 | 公开 HTTP |
| AI 抓取成功率 | 成功抓取请求 / AI crawler 请求 | 外部连通验证待执行 | CDN/网关访问日志与 crawler UA 分类 |
| 索引覆盖率 | 已索引规范 URL / sitemap URL | 外部连通验证待执行 | Google/Bing/百度站长平台所有权 |
| 品牌与核心实体提及率 | 正确提及 FateCat/TradeCat Labs 的答案 / 有效样本 | 外部连通验证待执行 | 固定问题集、平台、地区、日期和重复采样 |
| 答案引用率 | 含 FateCat 官方来源链接的答案 / 有效答案 | 外部连通验证待执行 | 平台采样与引用 URL 归一化 |
| 推荐曝光量 | 在推荐/比较问题中进入候选的次数 | 外部连通验证待执行 | 稳定问题集和周期采样 |
| 自然流量 | 非付费入口会话及来源 | 外部连通验证待执行 | 合规分析工具或 HF Analytics |
| 有效访问 | 到达 Web 后完成关键交互的会话 | 外部连通验证待执行 | 同意后的匿名事件 |
| 转化率 | 成功提交报告任务 / 有效访问 | 外部连通验证待执行 | 隐私合规事件与去重口径 |

外部指标不得用一次性手工查询冒充趋势。建议每周固定平台、固定问题、固定地区与新会话采样，至少保留样本数、答案、引用 URL、时间和失败原因；月度汇总时再计算提及率、引用率与推荐曝光。

稳定问题集入口：`GET /api/v1/discovery/query-set`。本地修改后先运行：

```bash
python3 scripts/geo-query-set-gate.py
```

## 运行方式

本地服务启动后：

```bash
python3 scripts/geo-audit.py \
  --base-url http://127.0.0.1:8001 \
  --output-json /tmp/fatecat-geo-local.json
```

线上部署后：

```bash
python3 scripts/geo-audit.py \
  --base-url https://tradecatlabs-fatecat.hf.space \
  --output-json /tmp/fatecat-geo-hf.json
```

公开发布门禁在传入 `--api-url` 时自动执行相同审计：

```bash
bash scripts/public-release-gate.sh \
  --api-url https://tradecatlabs-fatecat.hf.space
```

## 复测与迭代

1. capability 生命周期、公开 URL、品牌身份、隐私策略或输出边界变化时，同步更新 `/about`、匹配的 `/guides/*`、`llms.txt`、JSON-LD、README 和 sitemap。
2. 每次部署后运行线上 GEO 审计，保存 JSON 证据并比较失败项。
3. 每月审查高意图问题覆盖；只有存在真实用户需求和可靠来源时才新增内容。
4. 有访问日志和平台所有权后接入 crawler、索引与流量指标；没有数据时保持“外部连通验证待执行”。
5. 发现 AI 误引时优先修正事实源、能力边界和来源链接，不通过堆词或批量文章掩盖问题。
