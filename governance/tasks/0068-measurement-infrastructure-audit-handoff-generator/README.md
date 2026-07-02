# Task Overview

- Task ID: `0068`
- Slug: `measurement-infrastructure-audit-handoff-generator`
- Objective: `执行 0061 后续任务树的 audit handoff generator 切片：新增可一键生成第三方审计交接包的 Markdown/JSON generator、审计包 gate、任务与证据索引、pending external validations 扫描和 local-ci 接入；不能遗漏外部连通验证待执行项，不能把本地或 contract baseline 伪造成生产 live 证据。`
- Status: `Done`

## In Scope

- 新增 `contracts/fate/audit/handoff.json`，定义 audit handoff bundle 的机器契约、必备 Markdown 区块、JSON 字段和 pending external validation 策略。
- 新增 `scripts/audit-handoff.py` 与 `scripts/audit-handoff.sh`，生成 `audit-handoff.json` 与 `AUDIT_HANDOFF.md`。
- 审计包必须聚合 Git 状态、任务索引、关键 contract 资产、local-ci/CI 证据入口、risk register 和所有 tracked `外部连通验证待执行` occurrence。
- 接入 `scripts/local-ci.sh`，把 audit handoff 作为 quick profile artifact。
- 新增 `tests/regression/test_audit_handoff.py`，锁定 Markdown/JSON 输出、pending external validations 不遗漏和 local-ci 接线。
- 更新 `contracts/fate/AGENTS.md`、`scripts/AGENTS.md`、roadmap 和 0068 任务文档。

## Out of Scope

- 不执行第三方人工审计。
- 不补齐真实生产 API、Bot、OIDC、SIEM、监控平台、developer portal 或 sandbox token live evidence。
- 不把本地 generator、contract 或 quick local-ci 写成 100% 生产 live 证明。
- 不保存真实 token、secret、DSN、私钥、证书、生产日志、用户报告正文或外部账号数据。

## Requirement Alignment

- 对齐 0061 推荐任务：`0068 audit handoff generator`，最小交付物为 audit bundle markdown/json generator。
- 对齐基础设施目标：第三方审计必须能拿到一键生成、可复核、证据路径明确、风险不隐藏的交接包。
- 对齐风险约束：审计包必须完整列出 `外部连通验证待执行`，不能遗漏 pending external validations。

## Task Package Tree

```text
TP-01 Context audit
  TP-01.01 复核现有 closeout、release gate、local-ci、roadmap 和 pending external validation 事实
TP-02 Audit handoff contract
  TP-02.01 新增 audit handoff contract
  TP-02.02 新增 audit handoff generator
TP-03 Gate and integration
  TP-03.01 新增 audit handoff regression tests
  TP-03.02 接入 local-ci artifact 和 scripts/contracts AGENTS
  TP-03.03 同步 roadmap 与任务索引
TP-04 Validation and closeout
  TP-04.01 运行 focused validation 和 secret scan
  TP-04.02 运行 quick local-ci、任务校验并收口证据
```

## Task Package Overview

| Task Package ID | Parent | Priority | Type | Leaf | Depends On | Objective |
| --- | --- | --- | --- | --- | --- | --- |
| TP-01.01 | TP-01 | P0 | action | Yes | - | 明确当前审计交接资产和 pending external validation 来源。 |
| TP-02.01 | TP-02 | P0 | action | Yes | TP-01.01 | 新增 audit handoff 机器契约。 |
| TP-02.02 | TP-02 | P0 | action | Yes | TP-02.01 | 新增 Markdown/JSON audit handoff generator。 |
| TP-03.01 | TP-03 | P0 | action | Yes | TP-02.02 | 新增 audit handoff 回归测试。 |
| TP-03.02 | TP-03 | P0 | action | Yes | TP-03.01 | 接入 local-ci artifact 和目录级 AGENTS。 |
| TP-03.03 | TP-03 | P0 | action | Yes | TP-03.02 | 同步 roadmap 与任务索引。 |
| TP-04.01 | TP-04 | P0 | action | Yes | TP-03.03 | 运行 focused validation 和 secret scan。 |
| TP-04.02 | TP-04 | P0 | action | Yes | TP-04.01 | 运行 quick local-ci、任务校验并收口证据。 |

## Reading Order

1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
