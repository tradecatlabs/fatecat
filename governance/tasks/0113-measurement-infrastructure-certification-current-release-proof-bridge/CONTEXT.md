# Repo Evidence
| Evidence | Result |
| --- | --- |
| Branch | `main` |
| Certification source | `scripts/measurement-infrastructure-certification.py` release domain currently includes `live-release-gate.json` and `current-release-proof.json`. |
| Current behavior | `_evaluate_domain()` reads every evidence file from `evidence_dir / rel_path`. |
| Current tests | `tests/regression/test_measurement_infrastructure_certification.py` writes blocked `current-release-proof.json` with `proofGate.status=fail`. |
| Release proof evidence | Final `current-release-proof.json` can be generated after remote CI/release proof, outside local-ci output. |
| Live gate boundary | `live-release-gate.json` represents external production live conditions and must remain independently blocking. |

# Constraints Matrix
| Constraint | Handling |
| --- | --- |
| Final release proof cannot be committed back | Accept sidecar path instead of writing proof into Git or local-ci output. |
| Existing certification behavior must remain compatible | Optional argument only; no sidecar keeps evidence-dir behavior. |
| No production overclaim | Sidecar overrides only `current-release-proof.json`, never `live-release-gate.json`. |
| Audit visibility | Summary records `evidenceOverrides`, and evidence records `logicalPath` plus `source`. |
| No sensitive leakage | Only state, count, blocking item and path metadata are stored. |

# Change Boundary
- Allowed: certification script optional CLI input, evidence source metadata, certification contract, regression tests, roadmap and task docs.
- Not allowed: production deployment, live smoke execution, branch switch, release proof logic rewrite, live gate override, real secret access, report body persistence.

# Risk Matrix
| Risk | Impact | Mitigation |
| --- | --- | --- |
| Sidecar bypasses live release gate | False production readiness | Only allow override for `current-release-proof.json`; `live-release-gate.json` remains evidence-dir only. |
| Invalid sidecar silently ignored | Audit confusion | Explicit sidecar path must exist or fail-fast. |
| Summary hides evidence source | Third-party cannot reproduce | Emit `evidenceOverrides`, `logicalPath` and `source`. |
| Local-ci stale proof still used accidentally | False blocked or stale release state | Operators pass explicit sidecar for final current HEAD proof. |
| Sensitive data in summary | Security/privacy issue | Existing forbidden-fragment scan still applies to full summary. |

# Assumptions and Falsification
| Assumption | Falsifier |
| --- | --- |
| Current release proof can be side-loaded as a standalone JSON artifact. | Release proof generator changes to produce multiple required files that cannot be represented by one JSON. |
| `live-release-gate.json` must stay separate from release artifact proof. | Future ADR redefines release live proof as a different domain with separate contract. |
| Optional CLI input is the lowest-cost bridge. | Auditors require immutable artifact bundle format instead of CLI sidecar input. |
| Path metadata is acceptable to expose. | Path contains sensitive production host/user data; then output must switch to proof ref IDs. |

# Critical Ambiguities
- External production live evidence remains unavailable in the local environment.
- Sidecar can prove current release artifact state, but cannot prove Bot/API/HF/OIDC/SIEM/OTel/Vault/KMS live state.
- The current contract uses local filesystem paths as evidence references; long term audit bundles may replace these with immutable artifact URIs.

# Debug Evidence Contract
- 调试模式: Optional

If certification output drifts, collect the evidence dir, sidecar path, release domain evidence array and `evidenceOverrides`. Do not print raw secret values or full report bodies.

# Task Package Context Map
| Context | Path |
| --- | --- |
| Certification script | `scripts/measurement-infrastructure-certification.py` |
| Certification shell wrapper | `scripts/measurement-infrastructure-certification.sh` |
| Certification contract | `contracts/fate/audit/measurement-infrastructure-certification.json` |
| Regression tests | `tests/regression/test_measurement_infrastructure_certification.py` |
| Roadmap | `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` |
| Task index | `governance/tasks/INDEX.md` |
