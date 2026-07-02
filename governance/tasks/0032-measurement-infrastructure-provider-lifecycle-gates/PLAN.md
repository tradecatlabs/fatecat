# Planning Summary
本轮把 production provider 从“有基础 metadata 和 in-process health”推进到“有本地可验证生命周期门禁”。正确终态是 provider 具备版本锁、来源、许可、资源 manifest、promotion/deprecation policy、动态健康、trace、SBOM、外部依赖 smoke 和审计证据。本轮只实现仓库内可证明的 lifecycle baseline，避免把需要真实环境或人工法律判断的部分伪装成完成。

# Lifecycle Gates
不得跳过 gate；每个 gate 必须有证据或保留为 Pending。

| Gate | Status | Evidence |
| --- | --- | --- |
| SPEC | Done | README/CONTEXT 已定义 provider lifecycle 范围和 anti-goals。 |
| PLAN | Done | 本文件拆出 runtime/schema、gate/tests、docs/closeout。 |
| BUILD | Done | provider metadata、schemas、vendor manifest、gate script、tests、quick CI hook 已落地。 |
| TEST | Done | focused tests 和 quick local-ci 已通过。 |
| REVIEW | Done | task validator、lint/format、vendor health、diff check 已通过。 |
| SHIP | Done | closeout packet 已生成。 |

# Simplest Path
- 复用现有 `UsecaseProvider`，不新增 provider 抽象层。
- 把生命周期字段放进 `ProviderMetadata.as_dict()`，让 API/resource/schema 同源输出。
- gate 通过运行时 `list_capabilities()` 和 `list_providers()` 取真实 provider，而不是手写一份重复清单。
- 供应链校验只解析 `vendor_sources.json#id`，不引入外部 SBOM 工具。

# Split Strategy
- TP-01：先确认 lifecycle 缺口来自路线图和现有 provider/resource contract。
- TP-02：先扩 provider runtime metadata，再扩 schema 和 vendor manifest。
- TP-03：先做本地 gate 脚本，再把 API/contract/provider 测试接上 quick CI。
- TP-04：最后同步文档、AGENTS、路线图和任务 closeout。

# Execution Waves
| Wave | Leaves | Status |
| --- | --- | --- |
| Wave 1 | TP-01.01 | Done |
| Wave 2 | TP-02.01, TP-02.02, TP-02.03 | Done |
| Wave 3 | TP-03.01, TP-03.02 | Done |
| Wave 4 | TP-03.03, TP-04.01, TP-04.02 | Done |

# Runtime Workflow Contract
- Input: production capability registry and provider registry.
- State: provider lifecycle metadata remains owned by `ProviderMetadata` and `UsecaseProvider`.
- Gate: `scripts/provider-lifecycle-gate.py` composes Provider resources and validates required fields, refs and vendor policies.
- Output: machine-readable JSON summary under `infra/runtime/local-state/exports/providers/lifecycle-gate.json` by default.
- Privacy: gate reads no user input, report body, token, secret, DSN or production environment.
- Failure: any missing field, broken path, unapproved vendor, non-SPDX vendor or versionLock mismatch returns non-zero.

# Next Executable Leaves
- 无；任务已完成。

# Dependency Graph
```text
TP-01.01 -> TP-02.01 -> TP-02.02 -> TP-02.03 -> TP-03.01 -> TP-03.02 -> TP-03.03 -> TP-04.02
TP-03.02 -> TP-04.01 -> TP-04.02
```

# Rollback Protocol
- 回退 `ProviderMetadata` / `UsecaseProvider` 新 lifecycle 字段。
- 移除 `scripts/provider-lifecycle-gate.*` 和 `tests/regression/test_provider_lifecycle_gate.py`。
- 恢复 `provider.schema.json`、`resource.schema.json`、`vendor_sources.json` 的 lifecycle baseline 前口径。
- 恢复 `local-ci.sh`、docs、AGENTS 和 roadmap 的 provider lifecycle gate 文案。
- 不回滚 0009-0031 已完成测算基础设施切片。
