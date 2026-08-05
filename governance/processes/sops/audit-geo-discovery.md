---
id: SOP-DEV-GEO-DISCOVERY
type: process
status: current
owner: experience-delivery
route_key: audit_geo_discovery
route_aliases: ["执行 GEO 审计", "检查 llms.txt", "验证 AI 发现入口"]
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P30D
---

# 审计 GEO 机器发现链路

## 任务定义
对公开服务的 Web、指南、llms.txt、robots、sitemap、OpenAPI、capability/provider 和 query-set 入口执行可重复 GEO 审计。

## 当前状态
本地审计器、GEO contracts 和回归门禁可用；被外部 AI 引用和推荐仍需长期观测，不能由本地测试证明。

## 适用场景
公开内容、实体、发现入口、API 文档或 HF Space 更新后的 GEO 复核。

## 输入要求
公开 `--base-url`，可选 output JSON 和 timeout；URL 必须是授权审计目标。

## 前置条件
目标服务已部署并可公开访问；根路径、`/web`、`/llms.txt` 等入口应由同一版本提供。

## 默认工具链
`.venv/bin/python scripts/geo-audit.py --base-url <url> --output-json <file>` 和 GEO regression tests。

## 固定路径
根 `llms.txt`、delivery GEO routes、`contracts/fate/discovery/`、`tests/regression/test_geo_discovery.py`。

## 成熟参数
单请求 timeout 默认 30 秒；跟随公开内容跳转但保留根路由状态；输出机器可读 JSON。

## 分步执行流程
1. 记录目标 commit/deployment。
2. 执行 GEO audit。
3. 检查状态码、canonical URL、实体事实、更新时间、来源链接和结构化入口。
4. 运行本地 GEO tests。
5. 比较 GitHub/HF 内容一致性和历史指标。

## 幂等与增量策略
同一部署版本应稳定；内容变更只重审受影响入口，但发布前跑完整集合。

## 限速与并发规则
审计器顺序执行少量 GET；不得扩展为爬虫或高并发请求。

## 输出目录
`infra/runtime/local-state/exports/geo/`。

## 命名规范
`geo-audit-<host>-<short-sha>-<UTC>.json`。

## 质量验收门禁
全部 required route 可访问、事实一致、llms/robots/sitemap/OpenAPI 可解析、无虚假能力声明。

## 失败处理
404、版本不一致、陈旧事实或机器入口不可解析时 block GEO 发布结论。

## 恢复与重试策略
网络瞬时失败有限重试；内容问题修复并部署后重审，不使用缓存截图代替。

## 安全边界
只访问公开授权 URL；不抓私有接口；不堆关键词、不制造虚假作者/来源/评价。

## 临时文件清理
删除 HTTP 临时响应；保留审计 JSON、deployment/commit 和必要 header 摘要。

## 运行记录登记
记录 base URL、commit/deployment、入口状态、内容 hash、失败项和外部索引观察。

## 明确禁止事项
- 禁止承诺 AI 排名或引用率。
- 禁止低质量批量内容。
- 禁止以本地通过代替线上审计。
