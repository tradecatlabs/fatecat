# Task-Level Acceptance
- Current HEAD quick local CI evidence is refreshed and recorded.
- Developer docs/platform/portal/sandbox local gates are passed and tied to artifact paths.
- Public portal, SDK/package release and live sandbox token service remain explicitly blocked until external proof exists.
- `developer_platform.live` work item is identified with owner, id, status and stale reason.
- Task status remains `Blocked`; no 100% infrastructure completion is claimed.

# Validation Plan
| Validation | Command | Expected |
| --- | --- | --- |
| Current HEAD local CI | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0145-81dd574` | Exit 0, focused regression `389 passed` |
| Developer platform gate | `jq '{status, check_count:(.checks|length)}' /tmp/fatecat-local-ci-0145-81dd574/developer-platform-gate.json` | `status=passed`, checks `92` |
| Developer portal gate | `jq '{status, check_count:(.checks|length)}' /tmp/fatecat-local-ci-0145-81dd574/developer-portal-gate.json` | `status=passed`, checks `63` |
| Sandbox gateway gate | `jq '{status, livePublicTokenService}' /tmp/fatecat-local-ci-0145-81dd574/sandbox-access-gateway-gate.json` | `status=passed`, `livePublicTokenService=false` |
| External work item | `jq '.workItems[] | select(.category=="developer_platform.live")' /tmp/fatecat-local-ci-0145-81dd574/external-validation-closure-work-queue.json` | Pending external evidence, proof ref missing |
| Task docs | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0145-measurement-infrastructure-developer-public-platform-live --phase decompose` | Pass |

# Review Gate
- Verify wording does not claim public live completion.
- Verify no token, secret, raw URL, production user input or report body is copied into task docs.
- Verify local gates and external blockers are separated.
- Verify 0145 remains aligned with 0143/0144 and does not supersede 0144 external proof/live blockers.

# Runtime Verification Gate
- No long-running service is started by this task.
- Runtime evidence is limited to quick local CI artifacts in `/tmp/fatecat-local-ci-0145-81dd574`.
- Public live verification remains operator-owned and must be supplied as redacted proof-ref/live proof bundles.

# Ship Readiness
- Local task package can be committed once decompose validation passes.
- Developer public platform itself is not shippable as live until:
  - public developer portal URL proof is accepted,
  - at least one SDK/package publication proof or install smoke against a public package is accepted,
  - sandbox token issuer and revocation live proof is accepted,
  - public API changelog publication proof is accepted.
- Measurement infrastructure 100% certification remains blocked.

# Task Package Acceptance
## TP-01 Current HEAD developer evidence refresh
- Acceptance: current HEAD quick local CI passed and developer artifacts exist.
- Evidence: `/tmp/fatecat-local-ci-0145-81dd574`.

## TP-02 Public portal readiness
- Acceptance: public portal live proof is recorded as missing, not completed.
- Evidence: `externalPortalLive=false`, portal external status `not_implemented`.

## TP-03 SDK/package release readiness
- Acceptance: SDK candidates are visible, but package registry release is blocked.
- Evidence: `sdkPackageCandidates=4`, `publishedSdkPackages=0`, package registry `not_published`.

## TP-04 Sandbox token issuer/revocation readiness
- Acceptance: local gateway baseline is passed, live public token service remains blocked.
- Evidence: `livePublicTokenService=false`, live public token service `not_implemented`.

## TP-05 API changelog and final public proof
- Acceptance: local changelog and docs are present; public proof bundle is pending.
- Evidence: developer platform gate passed, developer public live work item pending.

# Anti-Goals
- 不得修改 `governance/tasks/` 以外路径
- 不得虚构证据
- 不得越权补全未确认信息
