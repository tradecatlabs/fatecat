# Task Index

| ID | Slug | Status | Priority | Objective | Link |
| --- | --- | --- | --- | --- | --- |

| 0001 | quality-standards-100 | Blocked | P0 | 把 FateCat 项目质量标准从当前 72% 推进到可审查、可验证、可维护、可生产运行的 100% 状态 | 0001-quality-standards-100/ |

| 0002 | quality-completion-to-100 | In Progress | P0 | 把 FateCat 当前质量完善度从本地可用状态推进到本地工程 100%、八字专业能力 100%、公共生产 HITL 100% 的可审查交付状态 | 0002-quality-completion-to-100/ |

| 0003 | bazi-system-100 | In Progress | P0 | 把 FateCat 八字体系从当前综合 76% 推进到基础排盘、专业规则、专题推理、样本外评测和报告证据均可验收的 100% 状态 | 0003-bazi-system-100/ |

| 0004 | bazi-professional-system-100 | Done | P0 | 把 FateCat 八字体系从当前工程可验收状态推进到专业八字体系 100% 验收口径：基础排盘、历法时间、证据解释、常规分析、高级格局、合化成败、用神裁决、岁运专题、Golden 回归和样本外 benchmark 全部具备可追溯规则、可验证测试、失败边界和发布门禁。 | 0004-bazi-professional-system-100/ |

| 0005 | bazi-capability-100-roadmap | Blocked | P0 | 调研并设计把八字功能十个完善度维度从当前基线推进到100%的任务树、验收门禁和执行波次计划。当前被真实 corpus 数量门禁阻塞。 | 0005-bazi-capability-100-roadmap/ |

| 0006 | business-logic-audit-remediation | Done | P0 | 修复 REVIEW-0001 业务代码业务模型与业务逻辑审计发现的阻塞级和警告级问题，恢复 fate-core 领域边界、业务选项语义一致性、入口真相源一致性、坐标边界校验和治理汇报准确性。 | 0006-business-logic-audit-remediation/ |

| 0007 | measurement-infrastructure-foundation | Done | P0 | 把 FateCat 从命理工具集合升级为面向 Agent 与应用开发者的测算基础设施基线：统一能力协议、可复现计算核心、证据化解释层、多端交付接口、能力成熟度和生产门禁。 | 0007-measurement-infrastructure-foundation/ |

| 0008 | measurement-infrastructure-hardening | Done | P0 | 继续把 FateCat 测算基础设施从协议骨架推进到开发者可接入、能力准入可拒绝、隐私与生产门禁可审计的基础设施硬化状态。 | 0008-measurement-infrastructure-hardening/ |

| 0009 | measurement-infrastructure-100-plan | Done | P0 | 基于成熟基础设施官方资料调研，制定 FateCat 达到 100% 测算基础设施所需的完整实现计划、递归任务树、验收门禁和分阶段执行路线。 | 0009-measurement-infrastructure-100-plan/ |

| 0010 | measurement-infrastructure-wave1-resources | Done | P0 | 执行测算基础设施 100% 实现计划 Wave 1 的首批切片：补资源 schema、capability 详情 API、标准错误码入口、API contract tests，并保持任务树和文档可验收。 | 0010-measurement-infrastructure-wave1-resources/ |

| 0011 | measurement-infrastructure-wave1-jobs | Done | P0 | 执行测算基础设施 100% 实现计划 Wave 1 的第二个切片：在现有报告任务队列上补 Idempotency-Key、cancelled 状态、取消 API、job resource links 和对应回归测试。 | 0011-measurement-infrastructure-wave1-jobs/ |

| 0012 | measurement-infrastructure-wave2-provider-protocol | Done | P0 | 执行测算基础设施 100% 实现计划 Wave 2 的第一个切片：把 CapabilityExecutor 从散落函数路由提升为统一 ProviderProtocol / provider registry，先接入 bazi、ziwei、almanac、meihua 四个生产 capability，并暴露 provider metadata、health 与标准错误归一化边界。 | 0012-measurement-infrastructure-wave2-provider-protocol/ |

| 0013 | measurement-infrastructure-wave2-provider-resources | Done | P0 | 执行测算基础设施 100% 实现计划 Wave 2 的第二个切片：把已落地的 production provider registry 资源化，新增 Provider schema、/providers 与 /providers/{provider_id} 发现入口、metadata 链接、API 回归测试和文档说明。 | 0013-measurement-infrastructure-wave2-provider-resources/ |

| 0014 | measurement-infrastructure-wave2-report-evidence-envelope | Done | P0 | 执行测算基础设施 100% 实现计划 IMP-05 的第一个切片：新增 Report schema 和 evidence reference 契约，并让 capability 执行响应携带统一 Report resource envelope，包含 profile、format、sections、evidenceRefs、links 与风险边界；不重写 Markdown 生成器或具体算法。 | 0014-measurement-infrastructure-wave2-report-evidence-envelope/ |

| 0015 | measurement-infrastructure-wave2-report-policy-gate | Done | P0 | 实现 Report policyGate 与 forbidden claims scanner，把 capability 报告交付结果纳入最小风险断语门禁。 | 0015-measurement-infrastructure-wave2-report-policy-gate/ |
| 0016 | measurement-infrastructure-wave2-markdown-report-gates | Done | P0 | 把 Markdown 同步报告、异步报告任务和 Web 报告结果接入统一 policyGate 与 snapshotGate，补齐多端报告正文最小发布门禁。 | 0016-measurement-infrastructure-wave2-markdown-report-gates/ |

| 0017 | measurement-infrastructure-wave3-evaluation-resources | Done | P0 | 把已有 golden、benchmark 与评测入口资源化为 Dataset / EvaluationRun 发现层，提供 schema、registry、API 入口、文档和回归测试。 | 0017-measurement-infrastructure-wave3-evaluation-resources/ |

| 0018 | measurement-infrastructure-wave5-observability-resources | Done | P0 | 把现有 health、ready、metrics、requestId 和结构化日志能力资源化为 Observability 发现层，提供 schema、registry、API 入口、文档和回归测试。 | 0018-measurement-infrastructure-wave5-observability-resources/ |

| 0019 | measurement-infrastructure-wave5-security-privacy-resources | Done | P0 | 把现有 token 权限、CORS、限流、请求体限制、响应安全头、隐私示例、source hygiene、public release policy 和 production readiness 门禁资源化为 SecurityControl 发现层，提供 schema、registry、API 入口、文档和回归测试。 | 0019-measurement-infrastructure-wave5-security-privacy-resources/ |

| 0020 | measurement-infrastructure-wave6-delivery-surface-contracts | Done | P0 | 把 Web、FastAPI、Telegram Bot、CLI、Agent Skill 等交付面资源化为 DeliverySurface 发现层，明确每个入口的同源计算链路、输出契约、验证命令、隐私边界和外部连通状态，补 schema、registry、API、文档和回归测试。 | 0020-measurement-infrastructure-wave6-delivery-surface-contracts/ |

| 0021 | measurement-infrastructure-wave4-evaluation-runner | Done | P0 | 把 EvaluationRun 从资源发现推进到本地可执行 runner：读取 contracts/fate/evaluations/registry.json，按 run id 或本地必跑集合执行安全白名单命令，输出机器可读 summary JSON，并补测试、文档、路线图和任务 closeout。 | 0021-measurement-infrastructure-wave4-evaluation-runner/ |

| 0022 | measurement-infrastructure-wave4-evaluation-history-diff | Done | P0 | 把本地 EvaluationRun runner 进一步推进为可审计质量闭环：支持本地结果历史留痕、latest 指针、summary diff、diff policy 阈值判定和回归测试；不实现 dashboard/nightly/远端 CI。 | 0022-measurement-infrastructure-wave4-evaluation-history-diff/ |

| 0023 | measurement-infrastructure-wave5-observability-runtime-smoke | Done | P0 | 把 ObservabilitySignal 从资源发现推进到本地可执行观测 smoke：用 TestClient 验证 health、ready、metrics、request-id、结构化 http_request log 和 registry metadata，输出机器可读 summary JSON；不接入 OpenTelemetry collector、dashboard 或生产监控平台。 | 0023-measurement-infrastructure-wave5-observability-runtime-smoke/ |

| 0024 | measurement-infrastructure-wave5-security-runtime-smoke | Done | P0 | 把 SecurityControl 从资源发现推进到本地可执行安全 smoke：用 TestClient 验证记录接口 token/owner 边界、响应安全头、请求体限制、限流，并串联 privacy/source/public-release 本地门禁，输出机器可读 summary JSON；不伪造真实生产域名、真实 token 或 Bot live smoke。 | 0024-measurement-infrastructure-wave5-security-runtime-smoke/ |

| 0025 | measurement-infrastructure-wave5-secret-scan-gate | Done | P0 | 把 SecurityControl 的专用 secret scanner 从后续缺口推进到本地可执行门禁：扫描 tracked first-party 文件中的真实密钥、高熵 token、私钥/证书、DSN 和 webhook 风险，输出机器可读 summary JSON，接入 security registry、quick CI、回归测试和文档；不读取真实 .env、不输出密钥原文、不替代真实生产凭证审计。 | 0025-measurement-infrastructure-wave5-secret-scan-gate/ |

| 0026 | measurement-infrastructure-wave5-audit-retention-policy | Done | P0 | 把 SecurityControl 的审计日志与 retention policy 从后续缺口推进到本地可验证基线：为记录读写/删除、报告 job 提交/取消等关键动作输出脱敏结构化 audit_event，登记 retention policy 和 audit log SecurityControl，补回归测试、quick CI、文档和任务 closeout；不接入外部 SIEM、不保存真实请求体、不伪造生产审计平台。 | 0026-measurement-infrastructure-wave5-audit-retention-policy/ |

| 0027 | measurement-infrastructure-100-research-plan-refresh | Done | P0 | 基于成熟基础设施官方资料与当前 FateCat worktree 事实，刷新测算基础设施 100% 完整实现计划：建立外部同构调研矩阵、当前能力差距、剩余任务树、执行波次、验收门禁与不可伪造证据口径；本任务只落盘计划与任务容器，不实现业务功能。 | 0027-measurement-infrastructure-100-research-plan-refresh/ |

| 0028 | measurement-infrastructure-rbac-policy | Done | P0 | 把记录接口的隐含 admin/user/owner 权限边界推进为本地可验证 RBAC baseline：显式 record scopes、兼容旧 user token、支持 scoped FATE_API_USER_TOKENS、登记 control.rbac_policy，补回归测试、生产预检兼容、文档和 closeout；不实现 OAuth/OIDC、外部 IdP 或多租户身份系统。 | 0028-measurement-infrastructure-rbac-policy/ |

| 0029 | measurement-infrastructure-openapi-sdk-sandbox | Done | P0 | 把开发者接入面推进为本地可验证 baseline：提供 OpenAPI 导出脚本、developer docs smoke、sandbox fixture、curl/Python/Node/Agent 示例，接入 quick CI，并回填任务包与 closeout；不实现公网 SDK 发布、真实 sandbox token 服务或远端开发者门户。 | 0029-measurement-infrastructure-openapi-sdk-sandbox/ |

| 0030 | measurement-infrastructure-durable-job-store | Done | P0 | 把报告任务运行面从纯内存队列推进为本地可验证持久 job store baseline：新增 ReportJobStore 抽象与 SQLite backend，保持默认内存模式兼容，支持任务元数据、状态、结果、幂等键、取消和 TTL 过期跨 manager 重建可查询；补环境变量、文档、回归测试、任务 closeout。不实现 webhook、retry policy、分布式 worker、外部队列或生产多副本锁。 | 0030-measurement-infrastructure-durable-job-store/ |

| 0031 | measurement-infrastructure-webhook-callbacks | Done | P0 | 把异步报告任务推进为本地可验证 webhook callback baseline：定义 webhook callback 契约、HMAC-SHA256 签名、终态事件 payload、可插拔 dispatcher 和本地 simulator/smoke，接入 report job succeeded/failed/cancelled 终态；保留默认无 webhook、且不做真实公网连通、持久重试队列、分布式 worker 或外部任务系统。 | 0031-measurement-infrastructure-webhook-callbacks/ |

| 0032 | measurement-infrastructure-provider-lifecycle-gates | Done | P0 | 把 production provider 生命周期从基础 metadata 推进为本地可验证 gate：为 provider 增加 version lock、source/license/resource manifest、lifecycle/deprecation/promotion policy 和 health gate，新增 provider lifecycle smoke/check 脚本并接入 quick CI；不实现真实外部依赖探测、trace span、供应链许可证人工审计或新 provider。 | 0032-measurement-infrastructure-provider-lifecycle-gates/ |

| 0033 | measurement-infrastructure-provider-dependency-smoke | Done | P0 | 把 provider health 从静态 in-process metadata 推进为本地可执行 dependency smoke baseline：为每个 production capability 准备固定脱敏样例，通过统一 CapabilityExecutor 执行 provider validate/calculate，输出机器可读 provider dependency smoke summary，接入 quick CI、API 文档、roadmap 和任务 closeout；不做真实公网外部依赖、OpenTelemetry trace span、SBOM、法律审计或新 provider。 | 0033-measurement-infrastructure-provider-dependency-smoke/ |

| 0034 | bazi-ziwei-l4-golden-evidence | Done | P0 | 把八字/紫微两个核心 production capability 推进为本地可验证 L4 golden/evidence baseline：复用现有匿名 golden fixture，新增 bazi/ziwei L4 golden smoke，统一验证八字节气/真太阳时/起运代表边界、格局/用神/调候/evidence coverage、紫微十二宫/星曜/四化/运限 golden、Markdown profile snapshot gate、冲突解释和反证说明，并接入 quick CI、文档、roadmap 与任务 closeout；不新增真实命例、不做全文断语 golden、不声明专业能力 100%。 | 0034-bazi-ziwei-l4-golden-evidence/ |

| 0035 | measurement-infrastructure-data-supply-chain | Done | P0 | 把数据、典籍、vendor、benchmark 供应链从散落 source_manifest/copyright_review/vendor_sources/evaluation registry 推进为本地可验证 DataSupplyChain baseline：新增统一 data supply chain manifest 和 schema，登记 raw/canonical/derived/export/runtime 分层、来源 hash、许可/版权状态、usageRole、productionEligibility、exportPolicy 与 verification commands；新增 data-supply-chain-gate 脚本和回归测试，接入 quick CI、API 文档、roadmap、data-products AGENTS 和任务 closeout；不引入新外部资料、不做法律意见、不生成 SBOM/provenance、不改变 production provider 算法。 | 0035-measurement-infrastructure-data-supply-chain/ |

| 0036 | measurement-infrastructure-eval-dashboard-nightly | Done | P0 | 把 EvaluationRun runner/history/diff 从 JSON 证据推进为本地可读评测 dashboard 与 nightly baseline：新增 evaluation dashboard renderer、dry-run dashboard smoke、nightly wrapper 和 GitHub scheduled workflow artifact，接入 quick CI、文档、roadmap 与任务 closeout；不接外部监控平台、不调用外部模型 API、不把 benchmark 标准答案注入生产路径。 | 0036-measurement-infrastructure-eval-dashboard-nightly/ |

| 0037 | measurement-infrastructure-otel-slo-alerts | Done | P0 | 把 D7 SRE/可观测从 health/ready/metrics/requestId/structured log baseline 推进为本地可验证 trace/SLO/alert baseline：新增 W3C traceparent/OpenTelemetry 语义兼容 span 日志、API/provider/report 本地 trace smoke、SLO policy、alert rules、observability gate，并接入 quick CI、observability registry、API 文档、roadmap 与任务 closeout；不接外部 collector、不引入未锁定依赖、不声称生产监控已完成。 | 0037-measurement-infrastructure-otel-slo-alerts/ |

| 0038 | measurement-infrastructure-production-identity-siem-retention | Done | P0 | 把 D8 安全/隐私从 scoped RBAC、secret scan、audit_event 和 retention baseline 推进为本地可验证的生产身份/SIEM/retention 准入基线：新增生产身份外部化策略、OIDC/IdP 准入 contract、SIEM/不可变审计存储 contract、retention 自动清理计划 contract、OWASP API security regression pack gate，并接入 security registry、production-readiness、quick CI、API 文档、roadmap 与任务 closeout；不接真实 OIDC/外部 SIEM、不删除真实数据、不伪造生产 live 证据。 | 0038-measurement-infrastructure-production-identity-siem-retention/ |

| 0039 | measurement-infrastructure-live-release-gate | Done | P0 | 把测算基础设施最后一段发布准入收束为可审计的 live release gate：新增 release evidence 契约、live release gate 脚本、外部证据 JSON 输出、真实 API/HF Space/Bot/远端 CI/container digest/SBOM-provenance 的机器可读验收口径，并接入 public-release/local-ci、delivery registry、roadmap、AGENTS 与任务 closeout；没有真实外部域名、token、HF/CI 权限时只标注外部连通验证待执行，不伪造 live 通过。 | 0039-measurement-infrastructure-live-release-gate/ |

| 0040 | measurement-infrastructure-release-artifacts | Done | P0 | 把 0039 live release gate 中的 SBOM/provenance 从纯 pending 推进为本地可生成、可校验、可交给发布门禁消费的 release artifacts baseline：新增 release artifact 生成脚本，基于 pyproject、requirements lock、Dockerfile、关键 contracts/scripts 生成 CycloneDX 兼容 SBOM、SLSA/in-toto 风格 provenance 和 manifest，接入 live-release/public-release/local-ci、回归测试、文档、roadmap 和任务 closeout；不推送 registry、不声明远端 CI attestation、不伪造 container digest 或真实生产发布。 | 0040-measurement-infrastructure-release-artifacts/ |

| 0041 | measurement-infrastructure-local-ci-evidence-gate | Done | P0 | 把 live release gate 中的 evidence.local_ci_quick 从仅检查 summary 文件存在推进为可校验的本地 quick CI 证据：让 local-ci 生成机器可读 summary JSON，记录 profile、status、commit、startedAt/finishedAt、关键 artifact 路径和 live gate summary；让 live-release-gate 校验 summary 内容必须证明 profile=quick 且 status=passed 且 commit 匹配当前 HEAD；让 public-release-gate 在执行 local-ci quick 时把该 summary 传给 live gate；补回归测试、任务文档和 closeout。范围不包含远端 CI、真实生产 API/HF/Bot、container digest、rollback drill 或清理当前脏工作树。 | 0041-measurement-infrastructure-local-ci-evidence-gate/ |

| 0042 | measurement-infrastructure-rollback-drill-evidence | Done | P0 | 把 live release gate 中的 evidence.rollback_drill 从纯路径存在推进为本地可生成、可校验、可交给发布门禁消费的 rollback drill evidence baseline：新增 rollback-drill 脚本，dry-run 校验回滚前置条件、候选回滚命令、相关 runbook/部署文档、release artifacts 和 delivery smoke 证据，输出机器可读 rollback-drill.json；让 live-release-gate 校验 rollback drill JSON 内容；让 public-release-gate 生成并传递该 evidence；补回归测试、文档、任务 closeout。范围不包含真实生产流量切换、真实 registry rollback、真实 HF/Bot 外部回滚或改写 Git 历史。 | 0042-measurement-infrastructure-rollback-drill-evidence/ |

| 0043 | measurement-infrastructure-container-release-evidence | Done | P0 | 把 live release gate 中的 evidence.container_digest 从裸 sha256 字符串推进为本地可生成、可校验、可交给发布门禁消费的 container release evidence baseline：新增 container-release-evidence 脚本，复用既有 container-build/container-smoke，记录 image、imageId sha256、RepoDigests、build/smoke status、pushExecuted=false、commit 和限制说明；让 live-release-gate 校验 container evidence JSON 内容，同时保留 --container-digest 作为真实 registry digest 输入；让 public-release-gate 可生成并传递本地 container evidence；补回归测试、文档、任务 closeout。范围不包含真实 registry push、GHCR RepoDigest、远端 CI 或清理当前脏工作树。 | 0043-measurement-infrastructure-container-release-evidence/ |

| 0044 | measurement-infrastructure-public-hf-api-live-evidence | Done | P0 | 把 live release gate 中已可通过的公开 Hugging Face Space/API 外部连通证据落成任务树 closeout：使用现有 live-release-gate 以 https://tradecatlabs-fatecat.hf.space 同时验证 production_api_live 与 hf_space_live，结合本地 local_ci、container、SBOM、provenance、rollback 证据，输出机器可读 gate JSON；记录 passed=7、pending=3 的真实结果，更新 roadmap 剩余缺口。范围不包含 Telegram Bot token、远端 GitHub Actions 当前 commit、clean git/提交推送或生产私有域名。 | 0044-measurement-infrastructure-public-hf-api-live-evidence/ |

| 0045 | measurement-infrastructure-100-final-plan-refresh | Done | P0 | 基于成熟基础设施官方资料、当前 0009-0044 任务事实和 live release gate 现状，刷新 FateCat 达到 100% 测算基础设施所需的完整实现计划、剩余任务树、验收证据和不可伪造外部验证口径；本任务只落盘规划，不实现业务功能。 | 0045-measurement-infrastructure-100-final-plan-refresh/ |

| 0046 | measurement-infrastructure-release-clean-ci | Done | P0 | 把当前本地测算基础设施改动收口为可发布交付状态：审计并归类未提交改动，运行本地发布门禁，按清晰边界提交并推送当前 main，获取远端 GitHub Actions 当前 commit 证据，最终让 clean git state 和 remote_ci_current_commit 进入 live release gate；不伪造 Bot token、registry signature 或外部生产平台证据。 | 0046-measurement-infrastructure-release-clean-ci/ |

| 0047 | measurement-infrastructure-100-post-0046-implementation-plan | Done | P0 | 基于当前 main、0009-0046 任务事实、远端 CI 状态和外部基础设施一手资料，刷新 FateCat 达到 100% 测算基础设施所需的完整实现计划、post-0046 剩余任务树和不可伪造证据口径。 | 0047-measurement-infrastructure-100-post-0046-implementation-plan/ |

| 0048 | measurement-infrastructure-telegram-bot-live-smoke | Blocked | P0 | 执行 MI-NEXT-01 Telegram Bot live smoke，用真实 FATE_BOT_TOKEN 调用 Telegram get_me()；当前环境缺少真实 token，任务保持 Blocked，不伪造 live 通过。 | 0048-measurement-infrastructure-telegram-bot-live-smoke/ |

| 0049 | measurement-infrastructure-100-deep-research-implementation-plan | Done | P0 | 基于当前 main worktree 和外部基础设施一手资料，补强 FateCat 达到 100% 测算基础设施所需的完整实现计划、资源模型、实现波次和不可伪造验收口径。 | 0049-measurement-infrastructure-100-deep-research-implementation-plan/ |

| 0050 | measurement-infrastructure-registry-attestation | Done | P0 | 执行 MI-NEXT-02，把 FateCat container release 从本地 imageId baseline 推进到 GHCR registry digest、GitHub artifact attestation、release artifact CI upload 和 attestation verify gate。 | 0050-measurement-infrastructure-registry-attestation/ |

| 0051 | measurement-infrastructure-100-post-0050-executable-plan | Done | P0 | 基于当前 post-0050 状态和外部基础设施同构资料，制作 FateCat 达到 100% 测算基础设施所需的可执行实现计划、任务树、优先级和失败判定。 | 0051-measurement-infrastructure-100-post-0050-executable-plan/ |

| 0052 | measurement-infrastructure-durable-runtime-event-history | Done | P0 | 执行 MI-NEXT-03 durable runtime 二期首个可验证切片：为 CalculationJob 增加 memory/sqlite 可审计 event history，API 返回 CalculationJobEvent，并同步回归测试、文档和任务 closeout；不实现 retry/timeout、callback retry/outbox、external backend 或分布式 worker。 | 0052-measurement-infrastructure-durable-runtime-event-history/ |

| 0053 | measurement-infrastructure-report-job-retry-timeout-policy | Done | P0 | 执行 MI-NEXT-03 durable runtime 二期第二个可验证切片：为 CalculationJob/report job 增加声明式 retry/timeout/non-retryable policy、本地事件证据、API 可见字段、回归测试与文档说明；不实现 callback retry/outbox、external backend、分布式 worker 或生产级硬中断。 | 0053-measurement-infrastructure-report-job-retry-timeout-policy/ |

| 0054 | measurement-infrastructure-webhook-callback-retry-outbox-baseline | Done | P0 | 执行 MI-NEXT-03 durable runtime 二期第三个可验证切片：为 report job webhook callback 增加本地有限 retry、retry/outbox 事件轨迹、生产预检配置、回归测试和文档说明；不实现跨进程持久 outbox、external backend、真实公网 webhook live smoke 或多副本 worker。 | 0054-measurement-infrastructure-webhook-callback-retry-outbox-baseline/ |

| 0055 | measurement-infrastructure-restart-recovery-smoke | Done | P0 | 执行 MI-NEXT-03 durable runtime 二期第四个可验证切片：为 report job SQLite manager 重建增加本地 restart-safe failure smoke、quick CI 门禁、回归测试和文档说明；不实现 external backend、跨进程继续执行、生产多副本 worker 或持久 callback outbox。 | 0055-measurement-infrastructure-restart-recovery-smoke/ |

| 0056 | measurement-infrastructure-persistent-webhook-outbox-baseline | Done | P0 | 执行 MI-NEXT-03 durable runtime 二期第五个可验证切片：为 report job webhook callback 增加 SQLite 本地持久 outbox baseline、API 可见状态、smoke、quick CI 门禁和文档证据；不实现公网 live webhook、跨进程自动重投、external backend、生产多副本 worker 或加密 secret 存储。 | 0056-measurement-infrastructure-persistent-webhook-outbox-baseline/ |
| 0057 | measurement-infrastructure-replayable-report-job-recovery-baseline | Done | P0 | 执行 MI-NEXT-03 durable runtime 二期第六个可验证切片：为 report job 增加可序列化 task payload、task factory 和 SQLite manager 重建后重新入队执行 baseline；让 Web/Markdown 两类生产报告任务具备本地跨 manager 重建继续执行能力。不实现 external backend、分布式 worker lease、多副本锁、持久 webhook secret 或真实公网 webhook live smoke。 | 0057-measurement-infrastructure-replayable-report-job-recovery-baseline/ |
| 0058 | measurement-infrastructure-webhook-outbox-redelivery-baseline | Done | P0 | 执行 MI-NEXT-03 durable runtime 二期第七个可验证切片：为 report job webhook outbox 增加 SQLite manager 重建后的本地自动重投 baseline；通过运行时 delivery resolver 重建 callback 配置并重投 failed/pending outbox record。不实现 external backend、分布式 worker lease、多副本锁、持久明文 webhook secret、真实公网 webhook live smoke 或 exactly-once。 | 0058-measurement-infrastructure-webhook-outbox-redelivery-baseline/ |
| 0059 | measurement-infrastructure-webhook-encrypted-config-vault-baseline | Done | P0 | 执行 MI-NEXT-03 durable runtime 二期第八个可验证切片：为 report job webhook callback 增加 SQLite encrypted delivery config vault baseline；使用成熟 Fernet 加密持久 callback config，支持 manager 重建后无外部 resolver 重投、成功后删除密文和 key rotation。不实现外部 Vault/KMS、external backend、分布式 worker lease、多副本锁、真实公网 webhook live smoke 或 exactly-once。 | 0059-measurement-infrastructure-webhook-encrypted-config-vault-baseline/ |
| 0060 | measurement-infrastructure-webhook-outbox-lease-baseline | Done | P0 | 执行 MI-NEXT-03 durable runtime 二期第九个可验证切片：为 report job webhook outbox 增加 SQLite 本地 claim/release lease baseline，避免多个 manager 重建时重复重投同一条 failed/pending outbox record。不实现 external backend、生产级分布式 worker lease、多副本锁、真实公网 webhook live smoke、外部 Vault/KMS 或 exactly-once。 | 0060-measurement-infrastructure-webhook-outbox-lease-baseline/ |

| 0061 | measurement-infrastructure-100-post-0060-deep-research-plan | Done | P0 | 基于当前 main、0060 之后的 durable runtime 状态和外部基础设施一手资料，制作 FateCat 达到 100% 测算基础设施所需的完整实现计划、资源成熟度矩阵、任务树、执行顺序和不可伪造验收口径；本任务只落盘规划，不实现业务代码。 | 0061-measurement-infrastructure-100-post-0060-deep-research-plan/ |

| 0062 | measurement-infrastructure-runtime-backend-contract | Done | P0 | 执行 0061 后续任务树的第一个 P0 切片：为 CalculationJob durable runtime 新增 external backend contract baseline，登记 memory/sqlite/postgres/temporal/redis_queue 的成熟度、生产边界、证据要求和迁移路径，新增 runtime backend gate、回归测试、文档和任务 closeout；本任务不实现真实 Postgres/Temporal adapter、不声明 external backend 已生产。 | 0062-measurement-infrastructure-runtime-backend-contract/ |

| 0063 | measurement-infrastructure-event-contract-baseline | Done | P0 | 执行 0061 后续任务树的 Event Platform P0 切片：为 job/webhook/evaluation/release 事件新增 CloudEvents envelope 与 AsyncAPI 风格事件契约基线，提供 schema、registry、examples、event contract gate、回归测试和文档 closeout；本任务不实现真实公网 webhook live delivery、不连接外部 broker、不声明事件平台已生产。 | 0063-measurement-infrastructure-event-contract-baseline/ |

| 0064 | measurement-infrastructure-otel-collector-slo-adapter | Done | P0 | 执行 0061 后续任务树的 OTel collector/SLO adapter P0 切片：为 FateCat observability 新增 OpenTelemetry Collector dry-run 配置、SLO evidence contract、collector contract gate、回归测试和文档 closeout；本任务不接入真实 trace backend、不声明生产监控或真实 error budget 已完成。 | 0064-measurement-infrastructure-otel-collector-slo-adapter/ |

| 0065 | measurement-infrastructure-security-externalization-gate | Done | P0 | 执行 0061 后续任务树的 Security externalization P0 切片：新增 OIDC/SIEM/retention cleaner 外部化证据契约、反伪造 gate、回归测试、quick CI 接线和文档 closeout；本任务不接入真实 IdP、SIEM、不可变审计平台或真实数据清理器，不把本地 scoped token 写成生产身份。 | 0065-measurement-infrastructure-security-externalization-gate/ |

| 0066 | measurement-infrastructure-core-quality-corpus | Done | P0 | 执行 0061 后续任务树的 core quality corpus expansion 切片：新增八字/紫微核心质量语料 manifest、完整报告 diff 策略、语料门禁和匿名紫微样本扩容，并接入 quick CI；不使用真实用户隐私样例，不把 evaluation fixture 变成生产输入。 | 0066-measurement-infrastructure-core-quality-corpus/ |

| 0067 | measurement-infrastructure-developer-platform-baseline | Done | P0 | 执行 0061 后续任务树的 developer platform 切片：新增 SDK/package baseline、sandbox token contract、API changelog 与开发者平台 gate，并接入 docs smoke/local-ci；不把本地 docs smoke 伪装成已发布 SDK，不声明公网 sandbox token 服务已上线。 | 0067-measurement-infrastructure-developer-platform-baseline/ |

| 0068 | measurement-infrastructure-audit-handoff-generator | Done | P0 | 执行 0061 后续任务树的 audit handoff generator 切片：新增可一键生成第三方审计交接包的 Markdown/JSON generator、审计包 gate、任务与证据索引、pending external validations 扫描和 local-ci 接入；不能遗漏外部连通验证待执行项，不能把本地或 contract baseline 伪造成生产 live 证据。 | 0068-measurement-infrastructure-audit-handoff-generator/ |

| 0069 | measurement-infrastructure-audit-dry-run-verifier | Done | P0 | 执行 0061/0068 后续任务树的 third-party audit dry-run 切片：新增 audit handoff dry-run verifier，消费 0068 生成的 Markdown/JSON 审计交接包，验证必备字段、Markdown 区块、pending external validations、risk register、敏感赋值防护和禁止 100% live 伪声明，并接入 local-ci artifact；不替代真实第三方审计，不声明外部 live evidence 已完成。 | 0069-measurement-infrastructure-audit-dry-run-verifier/ |

| 0070 | measurement-infrastructure-postgres-job-store-adapter | Done | P0 | 执行 MI-100.01 Durable Runtime 的 Postgres job store adapter 切片：在不伪造真实外部数据库 live 的前提下，为 CalculationJob/ReportJobStore 新增可选 Postgres adapter、Postgres DDL/migration dry-run、webhook outbox transactional claim/release 语义、配置入口和回归门禁；真实 Postgres 连通、生产多副本 worker、外部 Vault/KMS 与公网 webhook live 仍保留为外部验证待执行。 | 0070-measurement-infrastructure-postgres-job-store-adapter/ |

| 0071 | measurement-infrastructure-postgres-live-smoke | Done | P0 | 执行 MI-100.02 Durable Runtime 的 Postgres migration/job live smoke 切片：在 0070 PostgresReportJobStore adapter baseline 之后，新增可连接真实或一次性 Postgres 的 live smoke 工具，验证 schema 初始化、job/event/idempotency/task payload、webhook outbox claim/release 和 encrypted delivery config 基本读写；证据 JSON 必须脱敏，不输出 DSN、用户名、密码、callback URL、webhook secret 或报告正文；若缺少 DSN/psycopg/Postgres 环境则明确标记外部连通验证待执行，不伪造 production ready、多副本 worker、exactly-once、外部 Vault/KMS 或公网 webhook live。 | 0071-measurement-infrastructure-postgres-live-smoke/ |

| 0072 | measurement-infrastructure-postgres-worker-lease-negative-smoke | Done | P0 | 执行 MI-100.03 Durable Runtime 的 Postgres worker lease negative smoke 切片：在 0071 Postgres migration/job live smoke baseline 之后，新增可连接真实或一次性 Postgres 的多 worker outbox lease 竞争 smoke，用两个独立 PostgresReportJobStore/连接模拟多副本 worker 并验证同一 webhook outbox 记录在并发 claim 下只能一个 worker 成功、失败 worker 不能错误 release、lease 过期后可被其他 worker 重新 claim；证据 JSON 必须脱敏，不输出 DSN、用户名、密码、callback URL、webhook secret 或报告正文；无 DSN/psycopg/Postgres 时明确 blocked，不伪造 production ready、exactly-once、公网 webhook live 或外部 Vault/KMS。 | 0072-measurement-infrastructure-postgres-worker-lease-negative-smoke/ |

| 0073 | measurement-infrastructure-100-post-0071-deep-research-plan | Done | P0 | 基于当前 main worktree、0071 Postgres live smoke 已完成事实、0072 worker lease smoke 已完成事实，以及 OpenAPI、AsyncAPI、CloudEvents、Kubernetes Controller、Terraform Provider、Temporal、OpenTelemetry、Google SRE、OWASP、NIST、SLSA、CycloneDX、CNCF 平台工程等外部一手资料，刷新 FateCat 达到 100% 测算基础设施所需的完整实现计划、资源成熟度矩阵、任务树、执行顺序、验收门禁和不可伪造证据口径；本任务只落盘调研与计划，不把未外部验证的能力写成生产完成。 | 0073-measurement-infrastructure-100-post-0071-deep-research-plan/ |

| 0074 | measurement-infrastructure-postgres-job-execution-worker-lease | Done | P0 | 执行 MI-100.01 Durable Runtime 的 Postgres job execution worker lease 切片：在 0072 Postgres webhook outbox worker lease negative smoke 之后，为 Postgres ReportJobStore 增加 queued/running job 执行 claim/release lease 的最小接口、真实或一次性 Postgres smoke、契约门禁、回归测试和文档证据；必须证明多 worker 对同一 queued job 的并发 claim 只有一个成功、错误 owner 不能 release、lease 过期后可重 claim；不得声明 exactly-once、公网 webhook live、外部 Vault/KMS 或生产 ready。 | 0074-measurement-infrastructure-postgres-job-execution-worker-lease/ |

| 0075 | measurement-infrastructure-postgres-external-worker-restart-smoke | Done | P0 | 执行 MI-100.01 Durable Runtime 的 crash/restart external backend worker 切片：在 0074 Postgres job execution worker lease primitive 之后，将 ReportJobManager 执行路径接入 job execution lease，并新增真实或一次性 Postgres smoke，证明带 task_payload 的 stale running job 在 worker crash/lease expiry/restart 后可由外部 backend 恢复执行，且两个 manager 并发恢复时只有一个执行成功；不得声明 exactly-once、公网 webhook live、外部 Vault/KMS 或 production ready。 | 0075-measurement-infrastructure-postgres-external-worker-restart-smoke/ |

| 0076 | measurement-infrastructure-postgres-public-webhook-live-smoke | Done | P0 | 执行 MI-100 Durable Runtime 的公网 webhook live smoke 切片：在 Postgres external backend worker restart baseline 之后，新增需要真实 Postgres DSN 与公网 HTTPS webhook endpoint 的 live smoke 工具，验证 report job 终态事件能通过真实 HTTP webhook 投递并持久化 outbox 成功状态；无外部配置时必须输出 blocked summary，不泄露 DSN、URL、secret、报告正文或用户输入，不声明 exactly-once、多副本生产 ready 或外部 Vault/KMS 已完成。 | 0076-measurement-infrastructure-postgres-public-webhook-live-smoke/ |

| 0077 | measurement-infrastructure-100-post-0076-deep-research-plan | Done | P0 | 基于当前 main worktree、0076 Postgres public webhook live smoke gate 已完成事实，以及 OpenAPI、AsyncAPI、CloudEvents、Kubernetes Controller、Terraform Provider、Temporal、OpenTelemetry、Google SRE、DORA、OWASP、NIST、SLSA、CycloneDX、CNCF 平台工程、Backstage、Stripe 等外部一手资料，刷新 FateCat 达到 100% 测算基础设施所需的完整实现计划、任务树、执行顺序、外部阻断项和不可伪造证据口径；本任务只落盘调研与计划，不把未外部验证的能力写成生产完成。 | 0077-measurement-infrastructure-100-post-0076-deep-research-plan/ |

| 0078 | measurement-infrastructure-postgres-worker-heartbeat-polling | Done | P0 | 执行 0077 之后的首个本地可执行 P0 实现切片：为 Postgres report job worker 增加 job execution lease heartbeat/renew、DB polling、lease expiry backoff 与 stuck job recovery 的可验证 smoke，并接入 runtime backend contract、local-ci 和回归测试；无真实 DSN/psycopg/Postgres 时输出 blocked preflight，不声明 exactly-once、长期多副本生产 ready、公网 webhook live passed 或外部 Vault/KMS。 | 0078-measurement-infrastructure-postgres-worker-heartbeat-polling/ |

| 0079 | measurement-infrastructure-external-secret-provider-gate | Done | P0 | 执行 0078 之后的本地可执行 P0 安全基础设施切片：把 webhook encrypted config vault 从本地 Fernet baseline 推进为外部 secret provider / Vault / KMS 证据契约和反伪造门禁；接入 security registry、production-security gate、local-ci、回归测试和文档。无真实外部 secret manager 权限时只输出外部连通验证待执行，不声明外部 Vault/KMS、生产密钥生命周期或 public multi-replica ready 已完成。 | 0079-measurement-infrastructure-external-secret-provider-gate/ |
