# Repo Evidence
- `contracts/fate/evaluations/registry.json` 已有 Dataset/EvaluationRun 资源、runner metadata 和 diff policy metadata。
- `scripts/run-evaluations.py/.sh` 已支持本地必跑集合、命令白名单、dry-run、summary JSON、history/latest。
- `scripts/compare-evaluations.py/.sh` 已支持 baseline/current diff 和 `contracts/fate/evaluations/diff-policy.json` 阈值。
- `.github/workflows/acceptance.yml`、`container.yml`、`hf-space-deploy.yml` 已存在，但没有 evaluation nightly。
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 的 D6 缺口明确包含 dashboard/report artifact 和 nightly eval。
- 外部同构依据来自既有 100% roadmap 调研：GitHub Actions schedule/artifact、OpenAPI、Backstage、Kubernetes controller、OpenTelemetry、SRE SLO、SLSA、OWASP API、MLflow registry 等官方/主源资料；本任务只落 D6 本地 baseline。

# Constraints Matrix
| 约束 | 处理 |
| --- | --- |
| 不能伪造验证结果 | 所有通过结论绑定实际命令输出。 |
| 不扩大隐私面 | dashboard 不渲染 stdout/stderr tail、标准答案、报告正文、真实用户输入或凭证。 |
| 不引入外部平台 | 使用静态 HTML 和 GitHub artifact；外部监控平台留给后续。 |
| 不执行生产 live smoke | nightly 只执行本地 `releaseRequired` EvaluationRun。 |
| 不把 optional benchmark 混入默认 release gate | `scripts/evaluation-nightly.sh` 默认不加 `--allow-reference-repo`。 |
| 供应链 hash 必须同步 | 修改 evaluation registry 后同步 data supply chain manifest sha。 |

# Change Boundary
- 允许修改：`scripts/evaluation-*`、`scripts/local-ci.sh`、`contracts/fate/evaluations/registry.json`、`contracts/fate/data-supply-chain/registry.json`、`.github/workflows/evaluation-nightly.yml`、相关 AGENTS/docs/tests/task docs。
- 不修改：生产 provider 算法、报告生成器、API 行为、MingLi-Bench 标准答案、真实凭证、外部部署配置。

# Risk Matrix
| 风险 | 等级 | 缓解 |
| --- | --- | --- |
| Dashboard 泄露命令输出里的敏感内容 | P0 | 渲染器只显示命令、exit code、duration，不显示 stdout/stderr tail。 |
| Nightly 首次无 baseline diff | P2 | dashboard 明确首次无 baseline 属于预期；history/latest 后续自动形成 baseline。 |
| 评测 runner 递归执行导致成本过高 | P1 | quick CI 只跑 dry-run dashboard smoke；nightly 才执行真实本地必跑集合。 |
| 修改 registry 触发供应链 hash 漂移 | P1 | 运行 data supply chain gate 并同步 hash。 |
| GitHub schedule 被误解为生产验证 | P1 | docs 和 workflow 说明只上传 artifact，不代表生产 live smoke。 |

# Assumptions and Falsification
- 假设：静态 HTML artifact 是 D6 dashboard baseline 的最低充分形态。反证：如果需要多人长期趋势、筛选、权限和告警，则升级为结果库 + dashboard service。
- 假设：GitHub scheduled workflow 能作为 nightly baseline 的远端入口。反证：如果 artifact 留存期或并发不足，则引入外部结果存储。
- 假设：默认 releaseRequired 集合不包含 reference repo benchmark。反证：如果 MingLi-Bench 成为发布阻断门禁，则需要 reference repo provisioning 和 license gate。

# Critical Ambiguities
- 无阻断歧义。外部 CI 链接、真实远端 artifact 和生产域名验证需 push 后执行，当前只能标注为远端 CI 待执行。

# Debug Evidence Contract
- 调试模式: `Optional`
- 本任务不是 bugfix；不要求 `DEBUG.md`。
- 发现并修复一次供应链证据漂移：修改 evaluation registry 后 `data-supply-chain-gate` 失败，已同步 `contracts/fate/data-supply-chain/registry.json` 中对应 sha256 并复验通过。

# Task Package Context Map
| Package | Context |
| --- | --- |
| TP-01 | Runner/diff/workflow/roadmap 现状。 |
| TP-02 | Dashboard renderer、HTML 隐私边界、dry-run smoke。 |
| TP-03 | Nightly wrapper、history/latest、diff、GitHub artifact。 |
| TP-04 | Registry、quick CI、AGENTS、API docs、roadmap。 |
| TP-05 | Validation evidence、task docs、closeout。 |
