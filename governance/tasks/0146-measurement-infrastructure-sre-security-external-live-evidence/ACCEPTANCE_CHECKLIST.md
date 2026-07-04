# Acceptance Checklist

# Global Standards
- [x] Current local evidence is bound to HEAD `aea19ff4b060d30306cf65e008c3ba170f4f1df7`.
- [x] Local readiness is not claimed as external live completion.
- [x] OTel/SLO/alert live remains blocked.
- [x] OIDC/IdP live remains blocked.
- [x] SIEM/immutable audit live remains blocked.
- [x] External secret provider/Vault/KMS live remains blocked.
- [x] Production retention cleanup live remains blocked.
- [x] Real credentials and raw production evidence are not stored.
- [x] 100% certification remains blocked.

# Task Package Checklists
## Current SRE/security evidence

### TP-01.01 Current HEAD SRE/security gates
- [x] quick local CI passed.
- [x] production security gate passed.
- [x] security externalization gate passed.
- [x] external secret provider gate passed.
- [x] retention production cleanup staged gate passed.
- [x] observability and OTel gates passed.
Verify: `test -d /tmp/fatecat-local-ci-0146-aea19ff && jq '.status' /tmp/fatecat-local-ci-0146-aea19ff/production-security-gate.json`.
Gate: artifact root exists and focused regression showed `389 passed`.

## Observability and OTel live

### TP-02.01 OTel backend SLO live proof
- [ ] OTel collector runtime proof submitted by operator.
- [ ] Trace backend proof submitted by operator.
- [ ] Metrics backend and SLO dashboard proof submitted by operator.
- [ ] Alert route, error budget and incident drill proof submitted by operator.
Verify: `jq '.liveEvidenceStatus' <accepted-otel-backend-slo-live-proof-json>`.
Gate: `observability.otel_slo_live` proof-ref/live-proof accepted without raw traces, tokens, DSNs or report bodies.

## Identity and SIEM live

### TP-03.01 OIDC SIEM security proof
- [ ] OIDC/IdP token validation proof submitted by operator.
- [ ] SIEM/immutable audit storage proof submitted by operator.
- [ ] Security externalization proof accepted without raw issuer URL, tokens or audit payloads.
Verify: `jq '.liveEvidenceStatus' <accepted-security-externalization-proof-json>`.
Gate: `security.identity_oidc`, `security.siem_audit` and `security.externalization_live` proof refs accepted.

## Secret provider and retention live

### TP-04.01 Vault KMS retention proof
- [ ] External secret provider/Vault/KMS proof submitted by operator.
- [ ] Key rotation/access audit proof submitted by operator.
- [ ] Retention cleanup scheduler/smoke/audit proof submitted by operator.
- [ ] No raw secret, DSN, deletion payload or production deletion marker is stored.
Verify: `jq '.liveEvidenceStatus' <accepted-secret-retention-proof-json>`.
Gate: `security.external_secret_provider` and `security.retention_cleanup_live` proof refs accepted.

## Certification refresh

### TP-05.01 SRE security proof bundle
- [ ] Six SRE/security work items leave pending state.
- [ ] proof-ref gate accepts all relevant SRE/security proof refs.
- [ ] live-proof gate accepts all relevant SRE/security live proofs.
- [ ] certification rerun references accepted proof without leaking sensitive material.
Verify: `jq '.acceptedProofRefs, .acceptedLiveProofs' <accepted-external-validation-gate-json>`.
Gate: SRE/security categories no longer block certification.
