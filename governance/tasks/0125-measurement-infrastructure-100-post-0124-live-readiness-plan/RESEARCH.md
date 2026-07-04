# Post-0124 Live Readiness Research

## 1. Current State

0124 added the missing adapter between real live summaries and the 0123 live proof gate:

- `live-release-gate` can be the source for production API, HF Space and Telegram Bot live checks.
- `postgres-public-webhook-live-smoke` can be the source for public webhook delivery evidence.
- `multi-surface semantic diff` can become live parity evidence only when API/HF/Bot live checks are also passed.
- `production-live-delivery-evidence-bundle` converts those redacted summaries into `fatecat.external_validation_live_evidence_bundle`.

This means the remaining gap is no longer “how to model live evidence”. The remaining gap is “how to obtain real external live evidence without leaking secrets, and how to keep every claim bound to current commit, runbook, proof-ref and source occurrence”.

## 2. External Infrastructure Source Mapping

| Source | Official URL | Infrastructure lesson | FateCat post-0124 mapping |
| --- | --- | --- | --- |
| OpenAPI Specification 3.2.0 | `https://spec.openapis.org/oas/latest.html` | HTTP API consumers should understand a service without source code or traffic inspection. | Public API/HF smoke must prove API contract, TLS/CORS/token and response shape against documented contract. |
| AsyncAPI 3.1.0 | `https://www.asyncapi.com/docs/reference/specification/latest` | Event-driven APIs need machine-readable channels, messages and operations. | Webhook live evidence must bind terminal job events to event contracts and replay/DLQ policy. |
| CloudEvents | `https://cloudevents.io/` | Events should carry standard metadata for routing and auditing. | Public webhook proof must preserve event id/source/type/subject/time hash-level evidence without storing payload body. |
| Stripe webhooks | `https://docs.stripe.com/webhooks` | Webhook delivery is an operational interface with endpoint, retry, signature and event handling concerns. | FateCat public webhook smoke must prove signed delivery and terminal outbox state, not just local callback invocation. |
| OpenTelemetry signals | `https://opentelemetry.io/docs/concepts/signals/` | Production operation needs traces, metrics and logs as distinct signals. | MI-100.D remains incomplete until real collector/backend trace query, metrics/SLO and logs/alerts are evidenced. |
| Google SRE SLO guidance | `https://sre.google/sre-book/service-level-objectives/` | Service reliability must be expressed as SLI/SLO/error budget, not informal uptime claims. | Certification cannot pass SRE domain until dashboard/error budget/alert proof exists. |
| SLSA 1.2 | `https://slsa.dev/spec/v1.2/` | Supply chain claims require provenance and verifiable build levels. | Release proof must stay current per commit; old attestation cannot certify a new commit. |
| GitHub artifact attestations | `https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations` | Attestations establish where and how software was built and can be verified with GitHub CLI. | Final release evidence must include current run URL, digest, attestation and verification command output. |

## 3. Post-0124 Resource Readiness Matrix

| Domain | Current post-0124 state | 100% blocker | Next evidence |
| --- | --- | --- | --- |
| Production delivery | Bundle assembler exists; local pending and synthetic accepted paths covered. | Real API URL, HF URL, auth token, Bot token, public receiver, webhook secret. | Redacted live summaries accepted by 0124 and 0123 gates. |
| Runtime live | Postgres/restart/heartbeat/webhook/secret/multi-replica gates exist. | External secret provider, long-running multi-replica deployment and duplicate terminal negative proof. | Runtime live proof bundle accepted without exactly-once overclaim. |
| Observability/SRE | OTel/SLO staged gates exist. | Real collector/exporter/backend/dashboard/alert/incident drill. | Trace query proof, SLO dashboard proof, alert route proof, incident drill summary. |
| Security/privacy | RBAC, retention, OIDC/SIEM staged gates and secret scan exist. | Real IdP/SIEM/retention scheduler/tenant authz evidence. | Redacted IdP/SIEM/retention proof refs accepted by external live gates. |
| Developer platform | OpenAPI/docs/SDK baseline/sandbox access baseline exist. | Public portal, published SDK/package, public token issuer/revocation. | Install smoke, portal smoke, issue/revoke smoke. |
| Release/audit | Current release and audit bundle gates exist. | Final release commit must be re-proved; third-party review not performed. | Remote CI, artifact attestation, SBOM/provenance, rollback drill, audit reviewer notes. |

## 4. Next Task Tree

```text
MI-100 FateCat 100% Measurement Infrastructure
  MI-100.B Production Live Delivery
    MI-100.B.00 operator live execution packet and evidence template
    MI-100.B.01 production API/HF live smoke
    MI-100.B.02 Telegram Bot live smoke
    MI-100.B.03 public webhook live delivery smoke
    MI-100.B.04 multi-surface live parity diff
  MI-100.C Runtime Live Proof
    MI-100.C.01 external secret provider live
    MI-100.C.02 multi-replica runtime drill
    MI-100.C.03 duplicate terminal negative proof
  MI-100.D Observability/SRE Live
    MI-100.D.01 OTel collector/backend proof
    MI-100.D.02 SLO/error budget dashboard proof
    MI-100.D.03 alert route and incident drill proof
  MI-100.E Security/Privacy Live
    MI-100.E.01 OIDC/IdP proof
    MI-100.E.02 SIEM ingestion/query proof
    MI-100.E.03 production retention scheduler proof
    MI-100.E.04 tenant authz negative proof
  MI-100.F Developer/Public Platform
    MI-100.F.01 public developer portal live smoke
    MI-100.F.02 SDK/package public install smoke
    MI-100.F.03 sandbox token issuer/revocation live smoke
  MI-100.G Release/Audit Closeout
    MI-100.G.01 current commit release proof rerun
    MI-100.G.02 current audit bundle rerun
    MI-100.G.03 certification aggregator all-sidecar run
    MI-100.G.04 third-party audit rehearsal
```

## 5. Recommended Next Slice

If real credentials are not available, the next local slice should be `MI-100.B.00 operator live execution packet and evidence template`.

Reason:

- 0121 has category runbooks, 0123 has live proof gate, and 0124 has the bundle assembler.
- Operators still need one deterministic packet that binds exact command order, required environment variables, redacted output paths, expected hashes, proof-ref inputs and final gate commands for the production delivery workstream.
- This packet does not replace live evidence; it reduces the chance of leaking secrets or collecting unbound evidence when real credentials become available.

If real credentials are available, skip `B.00` and run the live workstream directly:

1. `live-release-gate.sh` with real production API URL, HF Space URL and token.
2. `live-release-gate.sh --run-live-bot` with real `FATE_BOT_TOKEN`.
3. `postgres-public-webhook-live-smoke.sh` with real Postgres DSN, public HTTPS receiver and webhook secret.
4. `production-live-delivery-evidence-bundle.sh`.
5. `external-validation-live-proof-gate.sh`.

## 6. Non-Claim Boundary

The following remain external connectivity pending:

- Production API/HF live.
- Telegram Bot live.
- Public webhook live.
- Multi-surface live parity.
- OTel/SLO/alert live.
- OIDC/SIEM/retention live.
- Vault/KMS/multi-replica runtime live.
- Public developer portal and SDK/package release.
- Third-party audit review.

No local plan, fixture, dry-run, CI pass or synthetic evidence can close those items.
