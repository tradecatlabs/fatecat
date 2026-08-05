---
id: SOP-INDEX
type: process-index
status: current
owner: engineering
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P60D
---

# 标准作业程序索引

## 路由规则

1. 先对用户任务做意图归一化，不按单个关键词猜测。
2. 优先匹配明确 capability 名称，再匹配操作目标；命中排除条件时继续查找。
3. 每次只允许选中一个 `route_key`；零命中或多命中都必须停止并补充上下文。
4. SOP 的状态不是生产证明；外部 live 结果只能由该 SOP 指定的证据门禁确认。
5. 未投产 capability 只能路由到研发接入 SOP，执行请求必须 fail closed。

## Capability

| Route Key | 自然语言任务别名 | 排除条件 | 当前状态 | SOP |
| --- | --- | --- | --- | --- |
| `execute_bazi_report` | 生成综合八字报告；执行八字排盘；计算八字 capability | 修改八字算法、规则或报告模板 | L4 production | [执行综合八字报告](execute-bazi-report.md) |
| `execute_ziwei_report` | 生成紫微报告；执行紫微斗数排盘；计算紫微 capability | 修改紫微算法、星曜规则或报告模板 | L4 production | [执行紫微斗数报告](execute-ziwei-report.md) |
| `execute_almanac` | 查询黄历；执行黄历 capability；计算基础择日数据 | 完整择日规则研发 | L3 validated | [执行黄历能力](execute-almanac.md) |
| `execute_meihua` | 梅花起卦；执行梅花易数；计算梅花 capability | 六爻、奇门或确定性断语 | L3 validated | [执行梅花易数能力](execute-meihua.md) |
| `activate_liuyao` | 实现六爻；接入六爻 provider；六爻能力投产 | 直接生成六爻生产结果 | L0 planned / blocked | [研发接入六爻](activate-liuyao.md) |
| `activate_qimen` | 实现奇门；接入奇门 provider；奇门能力投产 | 直接生成奇门生产结果 | L0 planned / blocked | [研发接入奇门遁甲](activate-qimen.md) |
| `activate_daliuren` | 实现大六壬；接入六壬 provider；大六壬能力投产 | 直接生成大六壬生产结果 | L0 planned / blocked | [研发接入大六壬](activate-daliuren.md) |
| `activate_fengshui_nine_stars` | 实现风水九星；接入九星 provider；玄空九星能力投产 | 建筑安全鉴定或直接生成生产结果 | L0 planned / blocked | [研发接入风水九星](activate-fengshui-nine-stars.md) |
| `activate_name_marriage` | 实现姓名合婚；接入合婚 provider；姓名关系能力投产 | 直接输出婚姻决定或歧视性判断 | L0 planned / blocked | [研发接入姓名合婚](activate-name-marriage.md) |
| `onboard_capability_provider` | 新增未知测算能力；注册新 capability；新增通用 provider | 已登记的九个明确 capability | framework available | [接入新的 Capability Provider](onboard-capability-provider.md) |

## 数据与评测

| Route Key | 自然语言任务别名 | 排除条件 | 当前状态 | SOP |
| --- | --- | --- | --- | --- |
| `rebuild_solar_term_golden` | 更新节气 golden；重建交节回归；校验月令边界 | 修改天文算法本体 | fixture validation current / rebuild blocked | [重建节气 Golden](rebuild-solar-term-golden.md) |
| `rebuild_location_catalog` | 更新出生地区库；重建地点目录；更新时区数据 | 单次地点查询 | production data | [重建地点与时区目录](rebuild-location-catalog.md) |
| `build_classics_dataset` | 清洗命理典籍；重建典籍数据集；验证 classics v3 | 修改 canonical 原典 | internal validated | [构建典籍派生数据集](build-classics-dataset.md) |
| `crawl_suanzhun_corpus` | 抓取算准网；增量更新研究语料；校验抓取完整性 | 直接发布或训练使用语料 | research only | [抓取算准网研究语料](crawl-suanzhun-corpus.md) |
| `run_evaluation_registry` | 运行评测；执行 EvaluationRun；更新评测历史 | MingLi 专项 benchmark | local runner available | [执行统一评测注册表](run-evaluation-registry.md) |
| `run_mingli_bench` | 运行 MingLi-Bench；生成命理评测 prompts；评分 predictions | 普通 pytest 或核心人审 | optional benchmark | [执行 MingLi-Bench](run-mingli-bench.md) |
| `intake_core_quality_human_review` | 提交八字紫微专家评审；录入专业人审证据；验收外部 benchmark | 自动生成专家结论 | external evidence blocked | [接收核心质量人审证据](intake-core-quality-human-review.md) |

## 开发与质量

| Route Key | 自然语言任务别名 | 排除条件 | 当前状态 | SOP |
| --- | --- | --- | --- | --- |
| `run_local_quality_gates` | 跑本地 CI；执行 quick gate；运行完整 acceptance | 真实生产 live 验收 | mature | [执行本地质量门禁](run-local-quality-gates.md) |
| `verify_multi_surface_parity` | 检查多端同源；对比 Web API Bot 报告；验证 Markdown 一致性 | 浏览器视觉验收 | mature | [验证多交付面语义一致性](verify-multi-surface-parity.md) |
| `audit_provider_supply_chain` | 扫描 provider 漂移；检查 vendor 健康；审计来源许可证 | 法律许可证最终意见 | mature local gate | [审计 Provider 供应链](audit-provider-supply-chain.md) |
| `verify_security_controls` | 扫描密钥；执行生产安全门禁；检查隐私控制 | 真实 IdP、SIEM、Vault live | local/staged | [验证安全与隐私控制](verify-security-controls.md) |
| `verify_observability_slo` | 验证 metrics；检查 OTel SLO；运行观测门禁 | 真实告警或事故演练 | local/staged | [验证可观测性与 SLO](verify-observability-slo.md) |
| `audit_geo_discovery` | 执行 GEO 审计；检查 llms.txt；验证 AI 发现入口 | 内容创作或搜索排名承诺 | live URL required | [审计 GEO 机器发现链路](audit-geo-discovery.md) |
| `start_local_delivery_service` | 启动本地 Web；启动 FastAPI；运行 delivery 服务 | Telegram polling Bot | mature | [启动本地 Web 与 API 服务](start-local-delivery-service.md) |
| `start_local_telegram_bot` | 启动本地 Telegram Bot；运行 Bot polling；Bot dry-run | HF Space webhook 配置 | token-dependent | [启动本地 Telegram Bot](start-local-telegram-bot.md) |
| `export_openapi_developer_docs` | 导出 OpenAPI；校验开发者文档；更新接口快照 | 发布 SDK 包 | mature | [导出 OpenAPI 与校验开发者文档](export-openapi-developer-docs.md) |

## 分发与部署

| Route Key | 自然语言任务别名 | 排除条件 | 当前状态 | SOP |
| --- | --- | --- | --- | --- |
| `export_skill_runtime` | 导出 FateCat Skill；生成 lite skill；生成 full skill | 构建 Python wheel | mature | [导出 Skill Runtime](export-skill-runtime.md) |
| `verify_distribution_package` | 检查分发包；运行 package smoke；验证独立安装包 | 容器镜像构建 | mature | [验证独立分发包](verify-distribution-package.md) |
| `build_smoke_container` | 构建 Docker 镜像；运行容器 smoke；验证 delivery image | 推送 GHCR 或 HF Space | mature | [构建并验证容器镜像](build-smoke-container.md) |
| `deploy_huggingface_space` | 更新 HF Space；部署 Hugging Face；同步 Space 生产 | GitHub 仓库 push | external deploy | [部署 Hugging Face Space](deploy-huggingface-space.md) |

## 生产运行

| Route Key | 自然语言任务别名 | 排除条件 | 当前状态 | SOP |
| --- | --- | --- | --- | --- |
| `verify_production_readiness` | 执行生产就绪检查；验证公网 API；运行 live release gate | 仅本地 quick CI | external evidence required | [验证生产就绪与 Live Release](verify-production-readiness.md) |
| `verify_postgres_runtime` | 验证 Postgres job store；测试多 worker lease；检查持久任务恢复 | SQLite 本地开发 | external database required | [验证 Postgres Durable Runtime](verify-postgres-runtime.md) |
| `verify_public_webhook` | 验证公网 webhook；测试 outbox 投递；检查 HMAC 回调 | Telegram webhook | external endpoint required | [验证公网 Report Webhook](verify-public-webhook.md) |
| `configure_telegram_webhook` | 配置 Telegram webhook；部署 HF Bot webhook；检查 getWebhookInfo | 本地 polling Bot | external token/domain required | [配置 Telegram Webhook](configure-telegram-webhook.md) |
| `run_retention_cleanup` | 清理过期记录；执行 retention；删除过期报告任务 | 清理开发缓存 | dry-run first | [执行数据保留期清理](run-retention-cleanup.md) |

## 发布、审计与卫生

| Route Key | 自然语言任务别名 | 排除条件 | 当前状态 | SOP |
| --- | --- | --- | --- | --- |
| `generate_release_artifacts` | 生成 SBOM；生成 provenance；制作发布证据 | 推送镜像或部署服务 | mature local | [生成发布制品证据](generate-release-artifacts.md) |
| `run_rollback_drill` | 执行回滚演练；生成 rollback evidence；验证回退路径 | 真实生产回滚 | dry-run evidence | [执行回滚演练](run-rollback-drill.md) |
| `prepare_third_party_audit` | 生成审计交接包；制作 current audit bundle；第三方审计预演 | 代替第三方作结论 | mature local | [准备第三方审计交接](prepare-third-party-audit.md) |
| `close_external_validation` | 关闭外部验证项；生成 operator packet；提交 proof ref | 自动伪造 live 证据 | externally blocked | [关闭外部验证事项](close-external-validation.md) |
| `clean_runtime_artifacts` | 清理运行缓存；整理仓库卫生；删除临时导出 | 数据保留期清理或删除 canonical | mature | [清理运行态与仓库卫生](clean-runtime-artifacts.md) |
| `deliver_git_github` | 提交 Git；推送 GitHub；检查 Actions | 部署 HF Space | mature / external remote | [提交并推送 GitHub](deliver-git-github.md) |

## 无匹配处理

- 不允许选择“看起来最接近”的 SOP。
- 先读取 `contracts/fate/capabilities/registry.json` 和 `scripts/AGENTS.md` 判断是否已有任务入口。
- 若确属新的稳定重复任务，先完成存在性检查，再新增一个独立 SOP、唯一 route key、唯一 aliases 和回归覆盖。
