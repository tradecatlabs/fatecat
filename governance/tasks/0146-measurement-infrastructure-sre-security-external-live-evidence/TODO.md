# Execution Checklist
[x] TP-01.01 | P0 | Refresh current HEAD SRE/security local evidence | Verify: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0146-aea19ff` | Gate: quick local CI passed with `389 passed` | Parallelizable: No
[ ] TP-02.01 | P0 | Collect OTel backend SLO live proof | Verify: `jq '.liveEvidenceStatus' <accepted-otel-backend-slo-live-proof-json>` | Gate: observability.otel_slo_live proof refs accepted without raw traces or secrets | Parallelizable: Yes
[ ] TP-03.01 | P0 | Collect OIDC SIEM security proof | Verify: `jq '.liveEvidenceStatus' <accepted-security-externalization-proof-json>` | Gate: identity, SIEM and externalization proof refs accepted without raw tokens or audit payloads | Parallelizable: Yes
[ ] TP-04.01 | P0 | Collect Vault KMS retention proof | Verify: `jq '.liveEvidenceStatus' <accepted-secret-retention-proof-json>` | Gate: secret provider and retention cleanup proof refs accepted without raw secrets or deletion payloads | Parallelizable: Yes
[ ] TP-05.01 | P0 | Submit SRE/security proof bundle and rerun certification | Verify: proof-ref/live-proof/certification gate summaries | Gate: SRE/security categories no longer block certification | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
