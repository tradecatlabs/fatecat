# Repo Evidence
| Evidence | Result |
| --- | --- |
| Branch | `main` |
| Certification source | `scripts/measurement-infrastructure-certification.py` audit domain currently reads `current-audit-bundle/current-audit-bundle.json`. |
| 0113 bridge | Certification already supports `--current-release-proof-json` for final release proof sidecar. |
| Current audit bundle source | `scripts/current-audit-bundle.py` already accepts `--current-release-proof`, but local-ci invokes it before final remote release proof exists. |
| Observed stale bundle | `/tmp/fatecat-local-ci-certification-bridge/current-audit-bundle/current-audit-bundle.json` references `current-release-proof.json` for old commit `14d239c...`, while current HEAD is `418472d...`. |
| Live boundary | `live-release-gate.json` and production external validations remain separate and cannot be overridden by audit bundle sidecar. |

# Constraints Matrix
| Constraint | Handling |
| --- | --- |
| Final audit bundle cannot be committed back | Accept sidecar path instead of writing proof into Git or local-ci output. |
| Default certification behavior must remain compatible | Optional argument only; no sidecar keeps evidence-dir behavior. |
| No release/live overclaim | Audit bundle override only maps to logical `current-audit-bundle/current-audit-bundle.json`. |
| Audit visibility | Summary already records `evidenceOverrides`; new override must use the same mechanism. |
| No sensitive leakage | Only status, path, source, pending and blocking metadata are stored. |

# Change Boundary
- Allowed: certification script optional CLI input, certification contract, regression tests, scripts/audit AGENTS, roadmap and task docs.
- Not allowed: production deployment, live smoke execution, branch switch, audit bundle generator rewrite, release proof override changes beyond existing 0113 path, real secret access, report body persistence.

# Risk Matrix
| Risk | Impact | Mitigation |
| --- | --- | --- |
| Audit sidecar bypasses release gate | False release readiness | Override only exact logical audit bundle path; release domain files remain separate. |
| Audit sidecar interpreted as third-party audit pass | False audit claim | Contract and docs keep non-claim boundary. |
| Invalid sidecar silently ignored | Audit confusion | Explicit sidecar path must exist or fail-fast. |
| Summary hides audit source | Third-party cannot reproduce | Evidence item records `logicalPath`, `path` and `source=override`. |
| Sensitive data in sidecar path/payload | Security/privacy issue | Existing forbidden-fragment scan still applies to full certification summary. |

# Assumptions and Falsification
| Assumption | Falsifier |
| --- | --- |
| Current audit bundle can be represented by one JSON sidecar for certification purposes. | Future audit package requires multiple files to determine status. |
| Certification should not regenerate audit bundle. | Future ADR changes certification from aggregator to orchestration engine. |
| Current audit bundle sidecar should not affect release domain. | A test shows release evidence status changes solely because audit sidecar is supplied. |
| Path metadata is acceptable to expose. | Path contains sensitive production host/user data; then output must switch to proof ref IDs. |

# Critical Ambiguities
- External third-party audit remains unavailable in the local environment.
- Audit bundle sidecar can prove latest audit package assembly, not production API/HF/Bot/OIDC/SIEM/OTel/Vault/KMS live state.
- The current contract uses filesystem paths as evidence references; immutable artifact URI support is a future hardening target.

# Debug Evidence Contract
- 调试模式: Optional

If certification audit domain drifts, collect the evidence dir, audit bundle sidecar path, audit domain evidence array and `evidenceOverrides`. Do not print raw secret values or full report bodies.

# Task Package Context Map
| Context | Path |
| --- | --- |
| Certification script | `scripts/measurement-infrastructure-certification.py` |
| Certification shell wrapper | `scripts/measurement-infrastructure-certification.sh` |
| Current audit bundle generator | `scripts/current-audit-bundle.py` |
| Certification contract | `contracts/fate/audit/measurement-infrastructure-certification.json` |
| Regression tests | `tests/regression/test_measurement_infrastructure_certification.py` |
| Scripts AGENTS | `scripts/AGENTS.md` |
| Audit contract AGENTS | `contracts/fate/audit/AGENTS.md` |
| Roadmap | `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` |
| Task index | `governance/tasks/INDEX.md` |
