# Task-Level Acceptance

- Developer portal contract and human portal doc exist.
- SDK release baseline manifest exists and keeps package registry status `not_published`.
- Sandbox output snapshot exists and stores only digests/shape checks, not response bodies.
- Developer portal gate executes locally and validates contracts, SDK smoke, snapshot digest, changelog, platform/docs smoke and privacy fragments.
- Quick CI runs developer portal gate and focused regression.
- Documentation states public portal, PyPI/npm and sandbox token live remain not implemented.

# Validation Plan
| Validation | Command / Evidence | Expected |
| --- | --- | --- |
| Syntax | `python3 -m json.tool ...`; `bash -n scripts/developer-portal-gate.sh scripts/local-ci.sh`; `python3 -m py_compile scripts/developer-portal-gate.py` | exit 0 |
| Gate | `bash scripts/developer-portal-gate.sh --output-json <tmp>` | status passed, 4 SDK candidates, 2 snapshots |
| Focused pytest | `.venv/bin/python -m pytest -q tests/regression/test_developer_portal_gate.py tests/regression/test_developer_platform_gate.py tests/regression/test_developer_docs_smoke.py` | exit 0 |
| Quick CI | `bash scripts/local-ci.sh --profile quick --output <tmp>` | exit 0 |
| Task docs | `validate_task_docs.py --phase closeout`; `validate_tasks_tree.py --phase auto` | exit 0 |

# Validation Evidence
| Validation | Result |
| --- | --- |
| Gate smoke | passed before final task closeout: 4 SDK candidates, 2 snapshots, 58 checks |
| Syntax | passed: JSON contracts, shell syntax and Python compile |
| Focused pytest | passed: 6 tests |
| Quick CI | passed: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0086`, 246 passed |
| Task docs | passed: `validate_task_docs.py --phase closeout`; `validate_tasks_tree.py --phase auto` reported 86/86 valid |

# Review Gate
- no-overclaim: published SDK count must be 0, external portal live must be false, live sandbox token service must be false.
- no-body-snapshot: snapshot must not store full response body.
- privacy: developer assets must not include known forbidden real place/user/secret fragments.
- document-drift: contracts、docs、AGENTS、local-ci and roadmap must agree.

# Runtime Verification Gate
- `developer-portal-gate` must recompute sandbox digests through FastAPI `TestClient`.
- Gate must fail on fixed snapshot digest mismatch.
- Gate must fail on known forbidden real place/user/secret fragments.
- Gate must keep public portal, published SDK and live sandbox token summary values false.

# Ship Readiness
- All TODO leaves complete.
- local quick CI passes.
- task validators pass.
- Remote GitHub Acceptance evidence is reported by the outer delivery flow after commit/push; this task snapshot does not pre-claim it.

# Task Package Acceptance
| Node ID | Acceptance |
| --- | --- |
| TP-01.01 | Existing developer baseline and 0086 gap inspected. |
| TP-02.01 | Release baseline and no-overclaim contract designed. |
| TP-03.01 | New developer portal, SDK release baseline, snapshot and docs added. |
| TP-04.01 | Developer portal gate added and smoke-tested. |
| TP-04.02 | local-ci、tests、AGENTS、docs and changelog wired. |
| TP-05.01 | Syntax、gate、focused pytest and quick CI passed. |
| TP-05.02 | Remote CI not pre-claimed inside committed task snapshot. |

# Anti-Goals
- 不证明公网 developer portal 已上线。
- 不证明 PyPI/npm SDK 已发布。
- 不证明 public sandbox token issuer、rate-limit 或 revocation live smoke。
- 不保存完整 sandbox 响应正文。

# Live Evidence

外部连通验证待执行。公网 developer portal、PyPI/npm package publication、public sandbox token issuer、gateway rate-limit/revocation smoke 不在本任务内完成。
