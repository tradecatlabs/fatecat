# Repo Evidence
| Evidence | Result |
| --- | --- |
| Branch | `main` |
| Certification source | `scripts/measurement-infrastructure-certification.py` release domain reads `live-release-gate.json` and `current-release-proof.json`. |
| 0113 bridge | Certification supports `--current-release-proof-json`. |
| 0114 bridge | Certification supports `--current-audit-bundle-json`. |
| Live gate source | `scripts/live-release-gate.py` already accepts local-ci summary, remote CI URL/commit, container evidence, SBOM/provenance, rollback evidence and external live URLs. |
| Observed blind spot | Certification had no way to consume a final current live gate sidecar after final release/audit evidence is generated. |
| Live boundary | Production API/HF/Bot evidence remains true external live evidence and cannot be inferred from sidecar presence. |

# Constraints Matrix
| Constraint | Handling |
| --- | --- |
| Final live gate cannot be committed back | Accept sidecar path instead of writing proof into Git or local-ci output. |
| Default certification behavior must remain compatible | Optional argument only; no sidecar keeps evidence-dir behavior. |
| No release/audit overclaim | Live gate override only maps to logical `live-release-gate.json`. |
| No production live overclaim | Sidecar payload can still contain `shipGate.status=blocked`; certification must preserve blocking items. |
| No sensitive leakage | Only status, path, source, pending and blocking metadata are stored. |

# Change Boundary
- Allowed: certification script optional CLI input, certification contract, regression tests, scripts/audit AGENTS, roadmap and task docs.
- Not allowed: production deployment, live smoke execution, branch switch, rebase, reset, real secret access, production database access, release proof/audit generator rewrite, report body persistence.

# Risk Matrix
| Risk | Impact | Mitigation |
| --- | --- | --- |
| Live sidecar bypasses release proof | False release readiness | Override only exact logical live gate path; release proof remains separate. |
| Live sidecar bypasses audit gate | False audit readiness | Audit domain path remains independent. |
| Sidecar presence interpreted as external live pass | False 100% claim | Contract/docs state pending external live remains blocked. |
| Invalid sidecar silently ignored | Audit confusion | Explicit sidecar path must exist or fail-fast. |
| Sensitive data in sidecar path/payload | Security/privacy issue | Existing forbidden-fragment scan still applies to full certification summary. |

# Assumptions and Falsification
| Assumption | Falsifier |
| --- | --- |
| Current live gate can be represented by one JSON sidecar for certification purposes. | Future live release evidence requires multiple files to determine status. |
| Certification should not regenerate live gate. | Future ADR changes certification from aggregator to orchestration engine. |
| Live sidecar should not affect release proof or audit bundle. | A test shows non-live logical evidence source changes solely because live sidecar is supplied. |
| Path metadata is acceptable to expose. | Path contains sensitive production host/user data; then output must switch to proof ref IDs. |

# Critical Ambiguities
- Production API, HF Space and Telegram Bot live smoke remain unavailable in this local environment.
- Current live gate sidecar can prove latest gate assembly, not live success.
- The current contract uses filesystem paths as evidence references; immutable artifact URI support is a future hardening target.

# Debug Evidence Contract
- 调试模式: Optional

If certification release domain drifts, collect the evidence dir, live gate sidecar path, release domain evidence array and `evidenceOverrides`. Do not print raw secret values, full URLs with embedded credentials or report bodies.

# Task Package Context Map
| Context | Path |
| --- | --- |
| Certification script | `scripts/measurement-infrastructure-certification.py` |
| Certification shell wrapper | `scripts/measurement-infrastructure-certification.sh` |
| Live release gate | `scripts/live-release-gate.py` |
| Certification contract | `contracts/fate/audit/measurement-infrastructure-certification.json` |
| Release gate contract | `contracts/fate/delivery/release-gate.json` |
| Regression tests | `tests/regression/test_measurement_infrastructure_certification.py` |
| Scripts AGENTS | `scripts/AGENTS.md` |
| Audit contract AGENTS | `contracts/fate/audit/AGENTS.md` |
| Roadmap | `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` |
| Task index | `governance/tasks/INDEX.md` |
