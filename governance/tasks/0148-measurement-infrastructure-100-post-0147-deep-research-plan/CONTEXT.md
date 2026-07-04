# Repo Evidence
| Evidence | Observation |
| --- | --- |
| Branch/HEAD before 0148 edits | `main...origin/main`, HEAD `a7b6a6f8edf47f1d945ef3986cd9d0bf8064c481` |
| Previous task | `0147-measurement-infrastructure-runtime-event-external-live-evidence` recorded runtime/event external live blockers. |
| 0145 | Developer public platform handoff committed and pushed; remote Acceptance for commit `aea19ff...` was success. |
| 0146 | SRE/security live evidence handoff committed and pushed; remote Acceptance for commit `c539c29...` was success. |
| 0147 local evidence | `/tmp/fatecat-local-ci-0147-c539c29`, quick local CI passed, focused regression `389 passed`. |
| 0147 remote evidence | GitHub Actions run `28715288541` for commit `a7b6a6f...` completed with `success`: https://github.com/tradecatlabs/fatecat/actions/runs/28715288541 |
| 0148 local CI evidence | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0148-a7b6a6f` passed; focused regression `389 passed in 142.34s`. |
| Certification status | `measurement-infrastructure-certification` remains `blocked`, `canClaim100Percent=false`, external pending remains nonzero. |
| Current roadmap | `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` already contains pre-0148 100% plan through section `6.37`; this task appends post-0147 refresh instead of replacing history. |

# External Research Sources
| Domain | Source | Infra lesson for FateCat |
| --- | --- | --- |
| Platform engineering | CNCF Platform Engineering Maturity Model: https://tag-app-delivery.cncf.io/whitepapers/platform-eng-maturity-model/ | Treat FateCat as a platform product: self-service discovery, onboarding, feedback, measurement and continuous improvement. |
| Cloud native | CNCF Cloud Native Definition: https://www.cncf.io/about/who-we-are/ | Capability/provider/report/job components must be loosely coupled, observable, resilient and automated. |
| Control plane | Kubernetes Controllers: https://kubernetes.io/docs/concepts/architecture/controller/ | Use spec/status, desired/current reconciliation, readiness and drift detection for capabilities, providers, runtime and release. |
| API contract | OpenAPI Specification: https://spec.openapis.org/oas/latest.html | Public APIs must be machine-readable, versioned, example-backed and compatible across releases. |
| Event contract | AsyncAPI Specification: https://www.asyncapi.com/docs/reference/specification/latest | Asynchronous report jobs, webhooks and event consumers need event contracts, channels, operations and examples. |
| Event envelope | CloudEvents: https://cloudevents.io/ | Event payloads need common metadata, type/source/id/time and extension discipline. |
| Durable execution | Temporal durable execution: https://docs.temporal.io/evaluate/understanding-temporal | Long-running jobs need event history, retry/timeout policy, worker recovery and explicit non-retryable failure classes. |
| Observability | OpenTelemetry signals: https://opentelemetry.io/docs/concepts/signals/ | Logs, metrics and traces must correlate API/job/provider/report paths through requestId/traceId. |
| SRE | Google SRE SLO chapter: https://sre.google/sre-book/service-level-objectives/ | Availability, latency, job success and error budget must have measured SLOs, dashboards and alert runbooks. |
| API security | OWASP API Security Top 10 2023: https://owasp.org/API-Security/editions/2023/en/0x11-t10/ | OIDC/RBAC, inventory, object/property authorization, rate/body limit, token and negative tests are production requirements. |
| Secure SDLC | NIST SSDF SP 800-218: https://csrc.nist.gov/pubs/sp/800/218/final | Security requirements, source integrity, vulnerability response and release evidence must be auditable. |
| AI risk | NIST AI RMF 1.0: https://www.nist.gov/itl/ai-risk-management-framework | Agent layer must be governed: no self-calculated chart fabrication, no high-risk deterministic claims, no medical/legal/financial replacement. |
| Supply chain | SLSA v1.2: https://slsa.dev/spec/v1.2/ | Build provenance, tamper evidence and release process integrity are part of infrastructure, not optional docs. |
| SBOM | CycloneDX specification: https://cyclonedx.org/specification/overview/ | Release packages need machine-readable dependency/component inventory and verification. |
| Artifact proof | GitHub Artifact Attestations: https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations | Final release artifacts should be attested and bound to the current commit. |

# Constraints Matrix
| Constraint | Decision |
| --- | --- |
| Planning-only task | Only task docs and roadmap are changed. |
| Current branch only | No branch switch, rebase or history rewrite. |
| External live | Missing real token/account/platform proof remains `外部连通验证待执行`. |
| Privacy | Do not store real DSN, token, webhook URL, production log payload, user input or report body. |
| Capability boundary | New prediction systems cannot enter default comprehensive bazi report; they must use independent capability registration. |
| Evidence boundary | Local contract/smoke/dry-run proves readiness only; it does not prove production live. |

# Change Boundary
- Allowed:
  - `governance/tasks/0148-measurement-infrastructure-100-post-0147-deep-research-plan/*`
  - `governance/tasks/INDEX.md`
  - `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`
- Not allowed:
  - production service code
  - contracts/schema behavior
  - CI script behavior
  - runtime secrets or external live evidence payloads

# Risk Matrix
| Risk | Impact | Mitigation |
| --- | --- | --- |
| Plan repeats old sections without current evidence | Roadmap becomes noisy and misleading | Append only post-0147 delta and reference existing sections. |
| 100% becomes vague marketing | Future work cannot be audited | Define 100% as certification gate plus nine passed domains. |
| Dry-run is mistaken for live | False production readiness claim | Explicit non-claim rules and failure predicates. |
| Task numbering drift | Operators execute wrong next node | 0148 is planning-only; next execution nodes are explicitly renumbered. |
| External source drift | Plan uses outdated infra assumptions | Cite official/current sources and bind decisions to verifiable gates, not prose. |

# Assumptions and Falsification
| Assumption | Falsifier |
| --- | --- |
| 100% infrastructure should be measured by evidence closure, not module count | If all external live/audit/release gates pass while a planned module remains unimplemented, 100% can still be claimed for current production scope. |
| Remaining blockers are mostly external proof/human review/final release proof | If certification shows a local domain failed after latest CI, add a local remediation task before external operator tasks. |
| New functionality should wait behind platform evidence closure | If a committed business requirement demands a new production capability, it must first pass the capability/provider/evidence/eval/security/release path. |
| 0148 should be planning-only | If user requests direct execution of a live proof item with credentials, create/continue the specific operator task instead. |

# Critical Ambiguities
- Exact external operator credentials, accounts and platform permissions are not available in the repo.
- Expert reviewer identity, rubric acceptance process and external benchmark corpus are not yet provided.
- Third-party auditor identity and accepted result format remain external/human-controlled.
- Final release commit cannot be known until all remaining changes are complete.

# Debug Evidence Contract
- 调试模式: Optional
Not required. This is a planning and documentation task, not a defect reproduction task.

# Task Package Context Map
| Node | Context |
| --- | --- |
| TP-01.01 | External research sources listed above. |
| TP-01.02 | Current HEAD, 0145-0147 status, certification blocked state and roadmap section `6.37`. |
| TP-02.01 | Future-optimal target state: resource protocol, provider lifecycle, runtime/event proof, security/SRE, release/audit/certification. |
| TP-02.02 | Nine-domain maturity matrix in roadmap post-0147 section. |
| TP-03.01 | MI-100 remaining task tree and next task numbering. |
| TP-03.02 | Completion gate, non-claim rule and failure predicates. |
| TP-04.01 | Roadmap and task package edits. |
| TP-04.02 | `validate_task_docs.py --phase decompose` and git/CI delivery evidence. |
