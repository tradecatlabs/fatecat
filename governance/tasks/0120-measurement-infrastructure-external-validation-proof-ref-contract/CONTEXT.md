# Repo Evidence

- `contracts/fate/audit/external-validation-closure-work-queue.json` 已定义 0119 work queue。
- `scripts/external-validation-closure-work-queue.py` 已输出 owner/category work items。
- `scripts/current-audit-bundle.py` 已产出 pending external validations。
- `scripts/measurement-infrastructure-certification.py` 已按 domain 聚合本地证据。
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 已列出 `MI-100.A.02 proof-ref schema and evidence upload contract`。

# Constraints Matrix

| Constraint | Decision |
| --- | --- |
| 无真实外部凭证 | 只做本地 proof-ref schema/verifier |
| 不泄露敏感信息 | 禁止 raw URL、token/secret/DSN/private-key marker |
| 不伪造 production live | `shipGate.status=blocked` 必须保持 |
| 不引入重型服务 | 不做 upload API、DB、dashboard |
| certification 不绕过 proof-ref | audit domain 同时要求 audit bundle 与 proof-ref gate |

# Change Boundary

允许改动：

- audit contract/schema
- scripts gate/wrapper/local-ci/certification aggregator
- regression tests
- AGENTS/roadmap/task docs/index

禁止改动：

- 业务排盘核心
- 生产部署凭证
- GitHub secret
- 真实外部服务配置

# Risk Matrix

| Risk | Mitigation |
| --- | --- |
| 把 schema accepted 写成 live passed | `shipGate` 始终 blocked，non-claims 明确 |
| proof-ref 保存 raw URL | verifier 全量扫描并拒绝 raw URL |
| command 泄露凭证 | summary 只保存 command sha256 |
| audit sidecar 绕过 proof-ref | certification audit domain 追加 proof-ref gate |
| 任务文档漂移 | auto-tasks 文档校验和 AGENTS/roadmap 同步 |

# Assumptions and Falsification

- Assumption: 本任务只需要本地 JSON 合同，不需要运行外部 live。
- Falsifier: 如果用户提供真实外部凭证并要求 live 验证，则必须新开 category runbook/live gate 切片，不能在 0120 中伪造。
- Assumption: `evidence://`、`artifact://`、`ci-artifact://` 是可审计句柄，不含真实 endpoint。
- Falsifier: 如果句柄中出现 raw URL、placeholder、localhost、token/secret/DSN marker，gate 必须失败。

# Critical Ambiguities

- 真实 artifact 存储位置尚未确定；本任务只规定 proof-ref 句柄前缀和 hash。
- 第三方审计人员如何签收 evidence 尚未确定；后续 runbook 需要定义 issuer 和 review flow。
- 各 category live command 的真实参数取决于外部账号权限；本任务只允许脱敏 command 模板。

# Debug Evidence Contract

- 调试模式: `Optional`

本任务不是 bug 修复；若验证失败，以 targeted pytest、ruff、secret scan 和 quick CI 输出作为定位证据。

# Task Package Context Map

## TP-01 Scope Confirmation

确认 0120 只覆盖 proof-ref schema/verifier，不进入 category runbook 或 live validation。

## TP-02 Contract And Gate

新增 contract/schema/script/wrapper，并让 certification audit domain 消费 proof-ref gate。

## TP-03 Regression And Local-CI

新增 proof-ref gate regression，覆盖 pending、脱敏 evidence、raw URL 拒绝和 wiring。

## TP-04 Validation

运行 targeted pytest、ruff、secret scan、real gate chain、quick CI 和任务文档校验。

## TP-05 Delivery

提交、推送并观察当前 commit 远端 CI；远端 CI 结果不写入仓库，只在交付汇报中报告。
