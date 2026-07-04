# Execution Checklist
[x] TP-01.01 | P0 | Refresh current HEAD developer local evidence | Verify: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0145-81dd574` | Gate: quick local CI passed with `389 passed` | Parallelizable: No
[ ] TP-02.01 | P0 | Collect public developer portal live proof | Verify: `jq '.externalPortalLive' <accepted-developer-portal-live-proof-json>` | Gate: public portal proof ref accepted and external status live | Parallelizable: Yes
[ ] TP-03.01 | P0 | Collect SDK/package registry publish proof | Verify: public package install smoke output, redacted and bound to release | Gate: at least one package/public install proof accepted | Parallelizable: Yes
[ ] TP-04.01 | P0 | Collect sandbox token issuer/revocation live proof | Verify: `jq '.livePublicTokenService' <accepted-sandbox-token-live-proof-json>` | Gate: issuer and revocation live proof refs accepted without token leakage | Parallelizable: Yes
[ ] TP-05.01 | P0 | Submit developer public platform proof bundle and rerun certification | Verify: proof-ref/live-proof/certification gate summaries | Gate: developer_platform.live no longer pending and certification no longer blocks on developer platform | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
