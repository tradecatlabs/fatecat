# Repo Evidence
| Evidence | Result |
| --- | --- |
| Branch | `main` |
| Prior W1 | `0111-measurement-infrastructure-control-plane-resource-gate` completed control-plane resource gate baseline. |
| Runtime backend source | `contracts/fate/delivery/runtime-backends.json` keeps `backend.postgres` as planned external backend candidate. |
| Public webhook source | `scripts/postgres-public-webhook-live-smoke.py` writes passed/blocked/failed sanitized summaries. |
| Secret provider source | `scripts/external-secret-provider-gate.py` validates external secret provider evidence contract and negative cases. |
| Multi-replica source | `scripts/multi-replica-runtime-gate.py` validates long-running multi-replica evidence and exactly-once non-claim. |

# Constraints Matrix
| Constraint | Handling |
| --- | --- |
| No live external environment | Default runtime proof output remains `external_connectivity_pending`. |
| Reuse existing gates | Runtime proof imports runtime backend, external secret and multi-replica gates. |
| No secret exposure | Gate rejects raw URL/DSN/token/secret-looking output. |
| No exactly-once overclaim | Runtime proof only enforces non-claim boundary. |
| Audit visibility | local-ci, certification and current audit bundle consume runtime proof artifact. |

# Change Boundary
- Allowed: `contracts/fate/delivery/runtime-proof-pack.json`, `contracts/fate/delivery/schemas/runtime-proof.schema.json`, delivery registry, runtime proof scripts, local-ci/certification/current-audit wiring, regression tests, AGENTS, roadmap and task docs.
- Not allowed: production deployment, real external credentials, runtime backend algorithm rewrite, webhook receiver setup, Vault/KMS setup, exactly-once claims.

# Risk Matrix
| Risk | Impact | Mitigation |
| --- | --- | --- |
| Aggregator duplicates sub-gate logic | Future drift and false confidence | Import and reuse sub-gate run/validation functions. |
| Blocked summary treated as live | Production overclaim | Public webhook status must be `passed` and `publicWebhookLiveDelivery=true`. |
| Local secret treated as external | False production security | External secret gate negative cases remain source of truth. |
| Single replica treated as runtime proof | False multi-replica claim | Multi-replica gate validates evidence and rejects negative cases. |
| Sensitive evidence leaked | Privacy/security incident | Regex check for raw URL, DSN, token, secret, private key markers. |

# Assumptions and Falsification
| Assumption | Falsifier |
| --- | --- |
| Runtime proof aggregation can be a thin gate before real production live environment exists. | User provides live environment and requires immediate live proof execution in this slice. |
| Existing sub-gates are authoritative for their domains. | Sub-gates accept negative fixtures that runtime proof should reject. |
| No exactly-once claim is the correct boundary. | A future external workflow backend provides stronger, audited delivery semantics and ADR changes the policy. |
| Audit bundle should track runtime proof artifact. | Audit owner explicitly removes W2 runtime proof from current handoff scope. |

# Critical Ambiguities
- Real external production evidence remains outside current local execution environment.
- Exactly-once remains a forbidden claim; current acceptable wording is at-least-once plus idempotency plus no duplicate terminal job observed in supplied evidence.

# Debug Evidence Contract
- 调试模式: Optional

If runtime proof gate fails, collect the failing check name, offending evidence path and sub-gate output; do not print raw evidence values.

# Task Package Context Map
| Context | Path |
| --- | --- |
| Runtime proof contract | `contracts/fate/delivery/runtime-proof-pack.json` |
| Runtime proof schema | `contracts/fate/delivery/schemas/runtime-proof.schema.json` |
| Runtime proof gate | `scripts/runtime-proof-gate.py` |
| Runtime proof wrapper | `scripts/runtime-proof-gate.sh` |
| Runtime backend gate | `scripts/runtime-backend-gate.py` |
| External secret provider gate | `scripts/external-secret-provider-gate.py` |
| Multi-replica gate | `scripts/multi-replica-runtime-gate.py` |
| Regression tests | `tests/regression/test_runtime_proof_gate.py` |
