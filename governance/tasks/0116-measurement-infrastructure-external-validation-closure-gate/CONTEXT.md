# Context

- 调试模式: `Optional`

## Current Facts
- 0115 已让 certification 支持 live-release-gate、current-release-proof、current-audit-bundle 三类 sidecar。
- `/tmp/fatecat-current-audit-bundle-finalizer-0115/pending-external-validations.json` 有 383 个 occurrence，但每项只包含 path/line/phrase/excerpt 等扫描信息。
- 这些 occurrence 缺少 owner、credential dependencies、required evidence、verification commands 和 closure condition。
- 这会导致审计人员知道“还有外部连通验证待执行”，但无法直接分派和关闭。

## Constraints
- 只允许分析当前 worktree 和当前分支。
- 不读取真实 token、secret、DSN、私钥、生产日志正文、用户报告正文或外部账号数据。
- 不连接真实外部系统；真实连通验证仍必须独立执行。
- 不得把 closure plan 写成 `passed live evidence`。

## External Research Mapping
| Infra Pattern | Lesson | FateCat Mapping |
| --- | --- | --- |
| OpenAPI / AsyncAPI | 机器可读 contract 优于自然语言接口说明。 | 外部待验证项也应输出机器可读 JSON。 |
| CloudEvents | 标准字段让事件可路由、可审计。 | closure item 必须有 id、source、category、owner、status。 |
| Kubernetes Controller | spec/status 支撑 reconciliation。 | pending occurrence 是 observed state，closure plan 是 desired close path。 |
| Backstage Catalog | Component/API/Resource 可发现。 | closure item 应成为 audit/control-plane 可发现资源。 |
| SLSA / CycloneDX | 证据要可追溯、可验证、可复核。 | closure condition 和 required evidence 必须明确。 |

## Risk Register
| Risk | Impact | Mitigation |
| --- | --- | --- |
| closure plan 被误解为 live passed | 伪造生产就绪 | `shipGate.status=blocked`，nonClaims 明确。 |
| 敏感赋值进入 JSON | 凭证泄露 | 禁止 token、secret、数据库 URL、DSN 等敏感赋值形态。 |
| 未分类 occurrence 被忽略 | 审计漏项 | `manual_triage`，不丢弃。 |
| local-ci 没有接线 | gate 漂在仓库外 | current audit bundle 后运行并进入 summary.json。 |

## Source Files
| Path | Role |
| --- | --- |
| `scripts/current-audit-bundle.py` | pending external validations 来源。 |
| `contracts/fate/audit/external-validation-closure.json` | closure gate contract。 |
| `scripts/external-validation-closure-gate.py` | closure plan generator。 |
| `scripts/local-ci.sh` | 本地 quick CI 接线。 |
| `tests/regression/test_external_validation_closure_gate.py` | 回归合同测试。 |
| `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | 100% roadmap 真相源。 |

# Repo Evidence
| Evidence | Result |
| --- | --- |
| `git status --short --branch` | `main` clean before 0116 edits; 0116 introduced scoped changes. |
| `pending-external-validations.json` finalizer sample | 383 occurrence items, no owner/credential/closure fields. |
| `scripts/audit-handoff.py` | Existing audit generator scans tracked and untracked pending phrase occurrences and blocks sensitive assignment markers. |

# Constraints Matrix
| Constraint | Handling |
| --- | --- |
| No external live access | Gate only emits plan and keeps ship gate blocked. |
| No secret leakage | Redaction and forbidden marker self-check. |
| Current branch only | No branch switch, no rebase, no destructive git. |
| Project contract style | New contract placed under `contracts/fate/audit/`. |

# Change Boundary
| In Boundary | Out of Boundary |
| --- | --- |
| Audit closure contract and local gate | Real API/Bot/Postgres/OIDC/SIEM/OTel/Vault/KMS live validation |
| local-ci wiring | Production deployment |
| Regression tests and docs | Third-party audit execution |

# Risk Matrix
| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Sensitive marker appears in audit handoff pending excerpt | Medium | High | Avoid forbidden assignment forms in pending lines; self-check JSON output. |
| Manual triage count high | High | Medium | Preserve manual items and make owner `engineering-audit`. |
| Closure plan misread as live evidence | Medium | High | nonClaims and blocked ship gate. |

# Assumptions and Falsification
| Assumption | Falsifier |
| --- | --- |
| Pending occurrence list is the correct source input. | current audit bundle stops emitting `pending-external-validations.json`. |
| Keyword profiles are enough for first triage. | manual triage dominates unacceptable share after review. |
| No external connection is needed for this slice. | User requires live smoke closure instead of closure planning. |

# Critical Ambiguities
- Manual triage ownership is intentionally generic until real team ownership exists.
- Verification commands are closure templates and may require environment-specific secret injection.

# Debug Evidence Contract
- Required: targeted pytest failure output if regression breaks.
- Optional: no `DEBUG.md` required unless closure gate has a reproducible bug beyond test assertion drift.
- Evidence must not include secret values or production logs.

# Task Package Context Map
| File | Reason |
| --- | --- |
| `README.md` | Task objective and boundary. |
| `PLAN.md` | Execution gates and split. |
| `ACCEPTANCE.md` | Validation commands. |
| `STATUS.md` | Current node status. |
