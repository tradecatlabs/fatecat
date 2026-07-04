# Task Context

- 调试模式: `Optional`

## Repo Evidence
| Evidence | Current fact |
| --- | --- |
| Current branch | `main` |
| Current commit | `6e99cf24bb086d0ee73418feea0a3e21bf48cd9c` |
| Commit message | `feat: add core quality human review gate` |
| Remote Acceptance | `28717205411`, success, `https://github.com/tradecatlabs/fatecat/actions/runs/28717205411` |
| 0149 task | local and remote delivery complete; overall remains `Blocked` because TP-04 expert/benchmark/no-leak evidence is missing |
| Local CI baseline | `/tmp/fatecat-local-ci-0149-final`, quick profile passed with 395 focused regression tests |
| Certification dry-run | `status=blocked`, `canClaim100Percent=false`, `domains=9`, `externalPending=15`, `blockingItems=5` |

## External Source Matrix
| Infra domain | Official source | FateCat implication |
| --- | --- | --- |
| Control plane | Kubernetes Controllers: https://kubernetes.io/docs/concepts/architecture/controller/ | Capability、provider、release、evaluation、audit 都要具备 spec/status、desired/current 和 drift/reconciliation。 |
| API contract | OpenAPI Specification: https://spec.openapis.org/oas/latest.html | 对外能力必须有机器可读 API、版本、错误码、兼容性与示例。 |
| Async/event contract | AsyncAPI Specification: https://www.asyncapi.com/docs/reference/specification/latest | webhook、job、event consumer 和 replay/DLQ 必须有 channels、operations、payload 和版本策略。 |
| Observability | OpenTelemetry Signals: https://opentelemetry.io/docs/concepts/signals/ | 生产 API -> job -> provider -> report 需要 logs、metrics、traces，且能绑定 requestId/traceId。 |
| SRE | Google SRE SLO: https://sre.google/sre-book/service-level-objectives/ | 100% 不能只有健康检查；必须有 SLO、error budget、alert、runbook 和真实平台证据。 |
| API security | OWASP API Security Top 10 2023: https://owasp.org/API-Security/editions/2023/en/0x11-t10/ | OIDC/RBAC、对象授权、API inventory、rate/body limit、token 边界和 negative tests 必须进入 release gate。 |
| Supply chain | SLSA v1.2: https://slsa.dev/spec/v1.2/ | 最终 release 必须绑定当前 commit 的 provenance、artifact、digest 与构建过程完整性。 |
| Security score | OpenSSF Scorecard: https://github.com/ossf/scorecard | 供应链安全不能只看本地脚本；后续需要公开仓库安全姿态和可复核门禁。 |
| Platform engineering | CNCF Platform Engineering Maturity Model: https://tag-app-delivery.cncf.io/whitepapers/platform-eng-maturity-model/ | FateCat 作为基础设施必须服务 Agent/开发者自助接入、反馈、度量和治理。 |

## Constraints Matrix
| Constraint | Impact |
| --- | --- |
| No real external credentials in repo | 不能把 production API/Bot/OIDC/SIEM/Vault/KMS/Postgres live 写成完成。 |
| 0149 accepts only redacted bundles | 专家评审和 benchmark 只能通过 ref/hash/aggregate/status 进入仓库。 |
| Certification is current evidence gate | 只要 certification `blocked` 或 `canClaim100Percent=false`，不得声明 100%。 |
| Final release proof must bind current commit | 任何新 commit 后 release proof、audit bundle、certification 必须重跑。 |
| Planned capabilities remain out of production | 100% 前不扩张 production 术数体系。 |

## Critical Ambiguities
| Ambiguity | Resolution |
| --- | --- |
| 0150 是否应该执行 final certification | No. 0149 仍缺真实人审/benchmark/no-leak，0144-0147 仍缺外部 live，因此 0150 只能刷新计划和阻断矩阵。 |
| 是否可以用 synthetic review bundle 关闭 core quality | No. Synthetic bundle 只用于测试 negative/positive parser，不是专家结论。 |
| 是否可以跳过外部 operator 证据直接声明 100% | No. Certification 的 `canClaim100Percent=true` 是唯一最终信号。 |
| 是否新增新术数 capability | No. 100% 当前生产范围关闭前，新体系只能 planned/experimental，不进入默认生产。 |

## Task Package Context Map
| Package node | Context needed | Source |
| --- | --- | --- |
| TP-01.01 | Current branch, commit, CI, 0149 delivery state | `git status`, `gh run view 28717205411`, 0149 task package |
| TP-01.02 | Mature infrastructure analogy | Kubernetes/OpenAPI/AsyncAPI/OpenTelemetry/SRE/OWASP/SLSA/OpenSSF/CNCF official docs |
| TP-02.01 | Certification blocked state | `/tmp/fatecat-local-ci-0149-final`, `/tmp/measurement-certification-0150-baseline.json` |
| TP-02.02 | Non-forgeable evidence categories | existing external validation, core quality, release and audit gates |
| TP-03.01 | Remaining task tree | roadmap and certification blockers |
| TP-03.02 | Next executable order | local/operator/audit/release dependency split |
| TP-04.01 | Documentation target | roadmap post-0149 section and task docs |
| TP-04.02 | Validation target | task docs validator, roadmap marker check, certification baseline, diff check |

## Assumptions and Falsification
| Assumption | Falsifier |
| --- | --- |
| 0149 closed local infrastructure but not external evidence | A real accepted `fatecat.core_quality_human_review_bundle` exists and gate reports human/benchmark/no-leak passed. |
| The next correct local action is post-0149 plan refresh | User supplies real external credentials/evidence and instructs live execution now. |
| Certification remains blocked | `measurement-infrastructure-certification.py --require-certified` passes for current commit with all required sidecars. |

## Change Boundary
- Allowed: 0150 task docs, roadmap post-0149 section, 0149 task delivery evidence doc sync.
- Not allowed: runtime/provider/API behavior changes, external live execution, credential handling, synthetic proof marked as accepted.

## Risk Matrix
| Risk | Mitigation |
| --- | --- |
| Planning inflation | 0150 must output concrete next tasks and failure predicates, not another generic manifesto. |
| Evidence overclaim | Every blocked external item must remain pending/blocked until gate accepts real redacted evidence. |
| Roadmap drift | Bind statements to commit `6e99cf2`, Acceptance `28717205411`, and certification dry-run evidence. |
| Task tree inconsistency | Run `validate_task_docs.py --phase decompose` after edits. |

## Debug Evidence Contract
Optional. This is not a bugfix task; failures in validation should be handled by targeted command output and task doc correction.
