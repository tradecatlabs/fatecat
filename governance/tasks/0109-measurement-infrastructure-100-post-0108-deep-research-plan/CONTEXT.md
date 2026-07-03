# Repo Evidence
| Evidence | Result |
| --- | --- |
| Branch | `git status --short --branch` -> `## main...origin/main` plus scoped docs changes |
| HEAD | `git rev-parse HEAD` -> `4d4abe2edab118e661382cbcd6d0bd244591d3a1` |
| Commit | `git log -1 --oneline` -> `4d4abe2 docs: add current release artifact proof task` |
| Remote Container | `gh run list --commit 4d4abe2...` -> `FateCat Container` run `28675409943`, `success` |
| Remote Acceptance | `gh run list --commit 4d4abe2...` -> `FateCat Acceptance` run `28675408793`, `in_progress` at snapshot |
| Task index | `governance/tasks/INDEX.md` contains duplicate 0108 status rows (`Done` and `In Progress`) at snapshot |
| Roadmap | `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` already includes post-0105 plan; needs post-0108 refresh |

# Constraints Matrix
| Constraint | Handling |
| --- | --- |
| Current branch only | Do not switch branch or inspect alternate worktree. |
| Planning task only | No business code, workflow behavior or production script changes. |
| External source freshness | Use official or fact-standard docs; record version/date facts where visible. |
| Remote run in_progress | Treat as pending, not success. |
| External live pending | Do not claim Bot/API/HF/OIDC/SIEM/OTel/Vault/KMS completion. |
| Existing roadmap as truth source | Append a post-0108 section instead of creating a parallel roadmap. |

# Change Boundary
- Allowed: `governance/tasks/0109-*`, `governance/tasks/INDEX.md`, `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`.
- Not allowed: runtime code, provider algorithms, workflow trigger behavior, secrets, external deployment.

# Risk Matrix
| Risk | Impact | Mitigation |
| --- | --- | --- |
| 0108 状态漂移 | Release proof 被误判完成 | Promote W0 release truth finalizer as next P0. |
| Plan overclaims 100% | Audit rejection and false readiness | Explicit pass/pending/blocked/external live wording. |
| External standards drift | Protocol baseline becomes stale | Record observed versions: OpenAPI 3.2.0, AsyncAPI 3.1.0, CycloneDX 1.7, SLSA 1.2. |
| Feature pile-up | Infrastructure target diluted into module collection | Prioritize control plane, runtime proof, SRE, security, release and audit before new systems. |

# Assumptions and Falsification
| Assumption | Falsifier |
| --- | --- |
| 100% infrastructure means infra completeness, not prediction accuracy. | User explicitly redefines success as prediction hit rate; current request did not. |
| 0108 release proof cannot be final while Acceptance is `in_progress`. | Acceptance terminal success plus current-release-proof gate passes for current HEAD. |
| OpenAPI latest is 3.2.0 | `https://spec.openapis.org/oas/latest.html` no longer shows v3.2.0. |
| AsyncAPI latest is 3.1.0 | `https://www.asyncapi.com/docs/reference/specification/latest` no longer resolves to v3.1.0. |
| CycloneDX current version is 1.7 | `https://cyclonedx.org/specification/overview/` no longer shows 1.7. |

# Critical Ambiguities
- Whether maintainers want to wait for 0108 Acceptance and run current-release-proof immediately after this planning task.
- Which external platforms will be used for IdP, SIEM, OTel backend, Vault/KMS and public webhook receiver.
- Who owns legal/copyright review for classical texts, vendor snapshots and benchmark assets.

# Debug Evidence Contract
- 调试模式: Optional

Not required. This is a planning/documentation task, not a defect reproduction or runtime regression. The 0108 state drift is recorded as a W0 follow-up, not debugged here.

# Task Package Context Map
| Context | Path |
| --- | --- |
| Main roadmap | `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` |
| Infrastructure requirements | `docs/reference-materials/roadmap/测算基础设施需求文档.md` |
| Current release proof task | `governance/tasks/0108-measurement-infrastructure-current-release-artifact-proof/` |
| This research snapshot | `governance/tasks/0109-measurement-infrastructure-100-post-0108-deep-research-plan/RESEARCH.md` |
| Release proof gate | `scripts/current-release-proof.sh`、`scripts/current-release-proof.py` |
| GitHub workflows | `.github/workflows/acceptance.yml`、`.github/workflows/container.yml` |
