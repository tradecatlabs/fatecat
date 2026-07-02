# Acceptance

## Task-Level Acceptance

- `contracts/fate/developer/developer-platform.json` exists and declares SDK/package baseline as not published.
- `contracts/fate/developer/sandbox-token-contract.json` exists and declares current status as contract-only and live token service not implemented.
- `contracts/fate/developer/api-changelog.json` exists and records API compatibility policy plus 0067 changelog entry.
- `scripts/developer-platform-gate.sh` validates developer platform contract, sandbox token contract, API changelog, sandbox fixture and SDK/package boundary.
- `/metadata` exposes developer platform, SDK/package baseline, sandbox token contract, API changelog and gate command pointers.
- `scripts/local-ci.sh --profile quick` runs developer platform gate and records a summary artifact.
- Docs do not claim PyPI/npm SDK publication or live public sandbox token service.

## Task Package Acceptance

| Task Package | Acceptance |
| --- | --- |
| TP-01.01 | Existing developer docs/sandbox/OpenAPI/local-ci/metadata state is documented. |
| TP-02.01 | Developer platform machine contract is present and linked to docs/gates. |
| TP-02.02 | Sandbox token contract has required/forbidden claims, scope fixture links and negative rules. |
| TP-02.03 | API changelog has machine and human entries, compatibility policy and evidence links. |
| TP-03.01 | Developer platform gate passes and writes `kind=fatecat.developer_platform_gate`. |
| TP-03.02 | `/metadata` and local-ci expose/run the new developer platform gate. |
| TP-03.03 | Regression tests cover gate summary and publication boundary. |
| TP-04.01 | AGENTS/README/API docs/roadmap are synchronized without overclaiming live status. |
| TP-04.02 | Focused validation and quick local-ci pass before commit/push. |

## Validation Plan

| Validation | Command | Expected |
| --- | --- | --- |
| JSON syntax | `python3 -m json.tool contracts/fate/developer/developer-platform.json` and related JSON files | valid JSON |
| Gate | `bash scripts/developer-platform-gate.sh --output-json /tmp/fatecat-developer-platform-gate.json` | status passed |
| Docs smoke | `bash scripts/developer-docs-smoke.sh --output-json /tmp/fatecat-developer-docs-smoke-0067.json --openapi-json /tmp/fatecat-openapi-0067.json` | status passed |
| Focused pytest | `.venv/bin/python -m pytest -q tests/regression/test_developer_platform_gate.py tests/regression/test_developer_docs_smoke.py tests/regression/test_api_contracts.py::test_measurement_infrastructure_metadata_exposes_capability_protocol_and_developer_entries` | passed |
| Lint/format | `ruff check` / `ruff format --check` focused files | passed |
| Task validators | `python3 governance/tools/validate_task_docs.py --task-dir governance/tasks/0067-measurement-infrastructure-developer-platform-baseline --phase closeout` and `python3 governance/tools/validate_tasks_tree.py --task-dir governance/tasks/0067-measurement-infrastructure-developer-platform-baseline --phase auto` | passed |
| Quick local-ci | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0067` | passed |

## Non-Acceptance

- 不能把 docs smoke、examples 或 package baseline metadata 写成已发布 SDK。
- 不能把 sandbox token contract 写成公网 token issuer/gateway 已上线。
- 不能把本地 quick CI 写成真实外部 developer portal、真实 token 或线上生产验证。

# Review Gate

- BLOCK if any doc or metadata claims PyPI/npm SDK publication.
- BLOCK if any doc or contract claims live public sandbox token issuance.
- BLOCK if any fixture/example stores real token, secret, production URL, real non-Beijing place, report body or user payload.
- WARN if developer portal remains local-only; this is expected and documented.

# Runtime Verification Gate

- Gate output must include `publishedSdkPackages=0`.
- Gate output must include `liveSandboxTokenService=false`.
- local-ci quick must include `developerPlatformGate` artifact path.
- `/metadata` must expose developer platform, SDK/package baseline, sandbox token contract, API changelog and gate command pointers.

# Ship Readiness

- Local focused validation: passed.
- quick local-ci: passed.
- Commit/push: handled by Git delivery step after task closeout.
- Remote CI current commit: handled by Git delivery step after push.

# Anti-Goals

- 不得发布 SDK package。
- 不得上线或伪造公网 sandbox token issuer/gateway。
- 不得把本地 docs smoke、examples 或 gate 写成外部 developer portal live 证据。
