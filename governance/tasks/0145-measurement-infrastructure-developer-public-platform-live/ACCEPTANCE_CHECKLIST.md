# Acceptance Checklist

# Global Standards
- [x] Current local evidence is bound to HEAD `81dd574101c842506d1765d544882b0953cff235`.
- [x] Local readiness is not claimed as public live completion.
- [x] Public portal live remains blocked.
- [x] SDK/package registry publication remains blocked.
- [x] Live sandbox token service remains blocked.
- [x] Real credentials are not stored.
- [x] 100% certification remains blocked.

# Task Package Checklists
## Current developer evidence

### TP-01.01 Current HEAD developer gates
- [x] quick local CI passed.
- [x] developer docs smoke passed.
- [x] developer platform gate passed.
- [x] developer portal gate passed.
- [x] sandbox access gateway gate passed.
Verify: `test -d /tmp/fatecat-local-ci-0145-81dd574 && jq '.status' /tmp/fatecat-local-ci-0145-81dd574/developer-platform-gate.json`.
Gate: artifact root exists and focused regression showed `389 passed`.

## Public portal live

### TP-02.01 Public developer portal proof
- [ ] Public developer portal URL proof submitted by operator.
- [ ] Portal external status no longer `not_implemented`.
- [ ] Public docs smoke against live portal accepted.
Verify: `jq '.externalPortalLive' <accepted-developer-portal-live-proof-json>`.
Gate: `externalPortalLive=true` with redacted public proof ref accepted.

## SDK/package registry

### TP-03.01 SDK package publish proof
- [ ] At least one public SDK/package publication proof submitted by operator.
- [ ] Public install smoke succeeds against package registry.
- [ ] Package version and changelog are bound to current release.
Verify: `python -m pip install <published-package>` or `npm view <published-package> version`, using redacted proof output.
Gate: `publishedSdkPackages>=1` or an accepted public installable SDK proof.

## Sandbox token live

### TP-04.01 Sandbox token issuer and revocation proof
- [ ] Sandbox token issuer live proof submitted by operator.
- [ ] Sandbox token revocation live proof submitted by operator.
- [ ] Tokens are redacted and no raw token value is stored.
Verify: `jq '.livePublicTokenService' <accepted-sandbox-token-live-proof-json>`.
Gate: `livePublicTokenService=true` and issuer/revocation proof refs accepted.

## API changelog and final proof

### TP-05.01 Developer platform public proof bundle
- [ ] API changelog public publication proof submitted.
- [ ] developer_platform.live proof-ref accepted.
- [ ] developer_platform.live live proof accepted.
- [ ] certification rerun still references accepted proof without leaking secrets.
Verify: `jq '.acceptedProofRefs, .acceptedLiveProofs' <accepted-external-validation-gate-json>`.
Gate: developer_platform.live leaves proof-ref/live pending state and certification no longer blocks on this category.
