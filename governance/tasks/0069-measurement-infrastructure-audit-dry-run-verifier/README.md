# Task Overview

- Task ID: `0069`
- Slug: `measurement-infrastructure-audit-dry-run-verifier`
- Objective: `执行 0061/0068 后续任务树的 third-party audit dry-run 切片：新增 audit handoff dry-run verifier，消费 0068 生成的 Markdown/JSON 审计交接包，验证必备字段、Markdown 区块、pending external validations、risk register、敏感赋值防护和禁止 100% live 伪声明，并接入 local-ci artifact；不替代真实第三方审计，不声明外部 live evidence 已完成。`
- Status: `Done`

## In Scope

- 新增 `contracts/fate/audit/dry-run.json`，定义 audit dry-run verifier 的输入、输出、检查项、ship gate 和 non-claim 策略。
- 新增 `scripts/audit-handoff-dry-run.py` 与 `scripts/audit-handoff-dry-run.sh`，消费 0068 生成的 `audit-handoff.json` 和 `AUDIT_HANDOFF.md`。
- verifier 必须检查 JSON 必备字段、Markdown 必备区块、pending external validation count、risk register、敏感赋值防护和 final conclusion 不夸大 100% live。
- 接入 `scripts/local-ci.sh`，在 audit handoff 之后生成 `audit-dry-run` artifact。
- 新增 `tests/regression/test_audit_handoff_dry_run.py`，锁定 verifier 输出、ship gate blocked 语义和 local-ci 接线。
- 更新 `contracts/fate/AGENTS.md`、`contracts/fate/audit/AGENTS.md`、`scripts/AGENTS.md`、roadmap 和 0069 任务文档。

## Out of Scope

- 不执行真实第三方人工审计。
- 不连接真实生产 API、Bot、OIDC、SIEM、监控平台、developer portal、sandbox token 或外部审计 SaaS。
- 不把 dry-run passed 写成 production/live/100% passed。
- 不保存真实 token、secret、DSN、私钥、证书、生产日志、用户报告正文或外部账号数据。

## Task Package Tree

```text
TP-01 Context audit
  TP-01.01 复核 0068 handoff contract、generator、local-ci artifact 和 MI-100.10.04 缺口
TP-02 Dry-run contract and verifier
  TP-02.01 新增 audit dry-run contract
  TP-02.02 新增 audit handoff dry-run verifier
TP-03 Gate and integration
  TP-03.01 新增 audit dry-run regression tests
  TP-03.02 接入 local-ci artifact 和目录级 AGENTS
  TP-03.03 同步 roadmap 与任务索引
TP-04 Validation and closeout
  TP-04.01 运行 focused validation 和 secret scan
  TP-04.02 运行 quick local-ci、任务校验并收口证据
```

## Requirement Alignment

- 对齐 MI-100.10.04 `third-party audit dry-run`：在真实第三方审计前，先用本地 verifier 检查审计交接包是否具备可复核结构。
- 对齐 0068 输出：dry-run 只消费 handoff bundle，不重新定义审计包事实源。
- 对齐不可伪造证据口径：外部 live 项缺证时必须保持 ship/live claim blocked。

## Task Package Overview

| Task Package ID | Parent | Priority | Type | Leaf | Depends On | Objective |
| --- | --- | --- | --- | --- | --- | --- |
| TP-01.01 | TP-01 | P0 | action | Yes | - | 明确 0068 handoff 输出和 audit dry-run 缺口。 |
| TP-02.01 | TP-02 | P0 | action | Yes | TP-01.01 | 新增 audit dry-run 机器契约。 |
| TP-02.02 | TP-02 | P0 | action | Yes | TP-02.01 | 新增 Markdown/JSON handoff verifier。 |
| TP-03.01 | TP-03 | P0 | action | Yes | TP-02.02 | 新增 dry-run 回归测试。 |
| TP-03.02 | TP-03 | P0 | action | Yes | TP-03.01 | 接入 local-ci artifact 和目录级 AGENTS。 |
| TP-03.03 | TP-03 | P0 | action | Yes | TP-03.02 | 同步 roadmap 与任务索引。 |
| TP-04.01 | TP-04 | P0 | action | Yes | TP-03.03 | 运行 focused validation 和 secret scan。 |
| TP-04.02 | TP-04 | P0 | action | Yes | TP-04.01 | 运行 quick local-ci、任务 validators 并收口证据。 |

## Reading Order

1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
