# Post-0135 Deep Research Plan

Research date: 2026-07-04

This document defines what FateCat still needs before it can honestly claim 100% measurement infrastructure. The conclusion is strict: local gates are strong, but 100% requires real external evidence and independent audit closure.

## Current Evidence Baseline

| Domain | Current evidence | Status | Meaning |
| --- | --- | --- | --- |
| Post-0135 release proof baseline | `/tmp/fatecat-current-release-audit-chain-refresh-4710659/current-release-proof.json` | passed | Commit `4710659` has release proof, remote release evidence and rollback dry-run evidence; later commits need their own release proof before production release claims. |
| Current audit bundle | `/tmp/fatecat-current-release-audit-chain-refresh-4710659/current-audit-bundle/current-audit-bundle.json` | passed | Local/current evidence bundle is structurally accepted; external pending inventory still exists. |
| External closure summary | `/tmp/fatecat-current-release-audit-chain-refresh-4710659/external-validation-closure-evidence-summary.json` | blocked gate | Real proof-ref/live proof closure remains missing. |
| Tracker import package | `/tmp/fatecat-current-release-audit-chain-refresh-4710659/external-validation-tracker-import-package.json` | operator action required | Ready for operator review, but real issue creation is not done. |
| Tracker issue template | `/tmp/fatecat-current-release-audit-chain-refresh-4710659/external-validation-tracker-issue-evidence-template.json` | operator action required | Needs sanitized issue refs and artifact hashes after real issue creation. |
| Tracker issue evidence gate | `/tmp/fatecat-current-release-audit-chain-refresh-4710659/external-validation-tracker-issue-evidence-gate.json` | blocked | No filled tracker issue evidence bundle yet. |
| Certification | `/tmp/fatecat-current-release-audit-chain-refresh-4710659/measurement-infrastructure-certification.json` | blocked | `canClaim100Percent=false`; this is the correct state. |
| Third-party audit rehearsal | `/tmp/fatecat-current-release-audit-chain-refresh-4710659/third-party-audit-rehearsal.json` | generated, gate blocked | Package is structurally usable, but independent audit and external evidence are missing. |

## External Infrastructure Source Matrix

| Source | What it teaches | FateCat mapping |
| --- | --- | --- |
| CNCF Platform Engineering Maturity Model: https://tag-app-delivery.cncf.io/whitepapers/platform-eng-maturity-model/ | Platform is a product with self-service, governance, measurement and maturity progression. | FateCat must expose capability/provider/job/report/audit resources as self-service infrastructure, not manual scripts. |
| OpenAPI Specification: https://spec.openapis.org/oas/latest.html | HTTP APIs need machine-readable schemas, errors, examples and versioning. | Public API, SDK examples, changelog and compatibility policy must be release artifacts. |
| AsyncAPI Specification: https://www.asyncapi.com/docs/reference/specification/latest | Async/event interfaces need machine-readable contracts. | Report job terminal events, webhook callbacks, evaluation events and audit events need AsyncAPI/CloudEvents alignment. |
| CloudEvents: https://cloudevents.io/ | Event producers should use a common envelope for interoperability. | Webhook/job/evaluation/release events should use consistent `id/source/type/subject/time/data`. |
| Kubernetes Controllers: https://kubernetes.io/docs/concepts/architecture/controller/ | Control planes reconcile desired and current state. | Capability/provider/release/security/evaluation resources need spec/status/drift reconciliation. |
| Backstage System Model: https://backstage.io/docs/features/software-catalog/system-model/ | Software platforms need discoverable components, APIs, resources and systems. | Contracts/catalog should become the developer-facing inventory of all FateCat resources. |
| Temporal Durable Execution: https://docs.temporal.io/evaluate/understanding-temporal | Long-running work needs durable event history, recovery and retry semantics. | Calculation jobs and evaluation jobs need production job store, outbox, retry, timeout and restart recovery evidence. |
| OpenTelemetry Signals: https://opentelemetry.io/docs/concepts/signals/ | Modern observability uses traces, metrics and logs. | API -> job -> provider -> report must produce correlated trace/log/metric evidence. |
| Google SRE SLOs: https://sre.google/sre-book/service-level-objectives/ | Reliability should be governed by SLIs, SLOs and error budgets. | FateCat needs availability, latency, job success, provider success and alert evidence. |
| DORA metrics: https://dora.dev/guides/dora-metrics-four-keys/ | Delivery performance should be measured and improved. | Release gate must track deploy frequency, lead time, failure rate, restore time and rollback drills. |
| OWASP API Security Top 10 2023: https://owasp.org/API-Security/editions/2023/en/0x11-t10/ | API platforms must defend authorization, authentication, resource consumption and inventory risks. | Token/RBAC/rate limit/body limit/API inventory/privacy regression must stay release blockers. |
| NIST SSDF SP 800-218: https://csrc.nist.gov/pubs/sp/800/218/final | Secure software development requires practices for reducing vulnerabilities and communicating risk. | Secret scan, dependency/source review, incident response and release evidence must be formal gates. |
| SLSA v1.2: https://slsa.dev/spec/v1.2/ | Supply-chain trust depends on provenance and verifiable build properties. | Current GHCR digest, artifact attestation, SBOM/provenance and source/data manifests must be required per release. |
| GitHub Artifact Attestations: https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations | Build artifacts can carry verifiable provenance in GitHub Actions. | Container release workflow must keep generating and verifying artifact attestations for each release commit. |
| CycloneDX: https://cyclonedx.org/specification/overview/ | SBOM should describe components, dependencies, services and relationships. | Code, container, vendor and data supply-chain artifacts need SBOM/provenance coverage. |

## 100% Resource Maturity Matrix

| Resource domain | Current baseline | 100% requirement | Remaining blocker |
| --- | --- | --- | --- |
| Capability | Registry/executor/profiles exist; bazi and ziwei are production samples. | All production capabilities use one executor, one policy/evidence/report envelope and promotion gate. | Planned capabilities remain registered only; future modules need provider-quality gates before production. |
| Provider | Provider protocol, lifecycle, dependency smoke and drift baseline exist. | Version/source/license drift, dependency health and trace spans are release-blocking. | External provider/source legal review and long-term trend evidence need closure. |
| CalculationJob | Memory/SQLite/Postgres baselines, retry/outbox/restart/lease smokes exist. | Production multi-replica runtime with external job store, durable outbox, bounded retries and live webhook evidence. | Real Postgres/webhook/multi-replica live evidence pending. |
| ReportProfile | Markdown/JSON envelope, policy and snapshot gates exist. | Cross-surface semantic diff, full report golden diff and policy enforcement for every surface. | Bot/live and larger golden corpus pending. |
| Evidence | evidenceRefs, rule IDs, coverage trend and broken-ref gates exist. | Every conclusion has rule/source/weight/risk/counter-evidence; coverage regression blocks release. | Expert review and corpus expansion pending. |
| Dataset/KnowledgeSource | Data supply-chain registry and canonical text assets exist. | Production-eligible source, license, hash, usage role and export policy for every dataset. | Legal/human review and corpus growth pending. |
| EvaluationRun | Runner/history/diff/dashboard/nightly baseline exists. | Nightly current-commit artifacts, benchmark trends, thresholds and sample-out quality tracking. | External benchmark policy and expert-labeled corpus pending. |
| DeliverySurface | Web/API/Bot/CLI/Skill registry exists. | Live parity for Web/API/Bot/CLI/Skill, public HF/API evidence and stable copy/export behavior. | Bot live and public production evidence pending. |
| SecurityControl | RBAC, rate limit, secret scan, audit and retention baselines exist. | OIDC/IdP, SIEM/immutable audit storage, retention cleanup, tenant isolation and OWASP regression live evidence. | Real external security platform pending. |
| ObservabilitySignal | health/ready/metrics/logs/local trace/SLO contracts exist. | OTel collector/backend, dashboards, alerts, error budget and incident drill evidence. | Real observability backend pending. |
| ReleaseArtifact | Release proof baseline for `4710659` exists; GHCR digest/attestation is recorded in that proof. | Every release commit has remote CI, container digest, SBOM/provenance, attestation verify and rollback drill. | Must be refreshed for every new release commit. |
| AuditHandoff | Current audit bundle, certification, closure summary, tracker chain and rehearsal exist. | Independent auditor result and all external pending items closed with redacted proof refs. | Third-party audit and real live evidence pending. |
| DeveloperPlatform | OpenAPI, examples, portal contracts, sandbox contracts and local smokes exist. | Public developer portal, SDK/package install, sandbox token issuer/revocation and docs smoke against public endpoint. | External public platform pending. |

## Complete Implementation Tree

```text
MI-100 FateCat measurement infrastructure 100%
  MI-100.00 Current truth and anti-overclaim
    MI-100.00.01 Refresh current-release-proof for every release commit
    MI-100.00.02 Refresh current-audit-bundle/certification/rehearsal from same evidence dir
    MI-100.00.03 Keep certification canClaim100Percent=false until all external gates pass
  MI-100.10 External validation closure
    MI-100.10.01 Create real tracker issues from import package
    MI-100.10.02 Fill redacted tracker issue evidence bundle
    MI-100.10.03 Execute proof-ref gate with operator artifacts
    MI-100.10.04 Execute live proof gate for all work items
    MI-100.10.05 Close closure summary and trend dashboard stale alerts
  MI-100.20 Production live delivery
    MI-100.20.01 Production API/HF live health/ready/metrics smoke
    MI-100.20.02 Telegram Bot live smoke with real token
    MI-100.20.03 Public webhook callback live smoke
    MI-100.20.04 Multi-surface semantic diff on live outputs
  MI-100.30 Runtime platform
    MI-100.30.01 Production Postgres job store and outbox live
    MI-100.30.02 Multi-replica worker lease/heartbeat live
    MI-100.30.03 Exactly-once boundary documented with accepted limitations
    MI-100.30.04 Recovery and rollback drills under production-like load
  MI-100.40 Observability/SRE
    MI-100.40.01 OTel collector/exporter/backend live evidence
    MI-100.40.02 SLO dashboard and error budget policy
    MI-100.40.03 Alert dry/live evidence and incident drill
    MI-100.40.04 DORA/release operations trend reporting
  MI-100.50 Security/privacy
    MI-100.50.01 OIDC/IdP integration evidence
    MI-100.50.02 SIEM/immutable audit storage evidence
    MI-100.50.03 Vault/KMS/external secret provider live evidence
    MI-100.50.04 Retention cleanup staged/production evidence
    MI-100.50.05 Tenant isolation and OWASP API negative regression pack
  MI-100.60 Developer platform
    MI-100.60.01 Public OpenAPI and changelog release artifact
    MI-100.60.02 SDK/package install smoke
    MI-100.60.03 Sandbox token issuer/revocation/live gateway
    MI-100.60.04 Public developer portal smoke and examples
  MI-100.70 Core quality
    MI-100.70.01 八字 expert/anonymous corpus expansion
    MI-100.70.02 紫微 expert/anonymous corpus expansion
    MI-100.70.03 Full report golden diff and contradiction/counter-evidence checks
    MI-100.70.04 MingLi-Bench and external benchmark trend gate
    MI-100.70.05 Human review rubric for domain interpretation quality
  MI-100.80 Supply chain and release
    MI-100.80.01 Per-release GHCR digest and attestation verification
    MI-100.80.02 SBOM/provenance/data/vendor manifest attestation
    MI-100.80.03 Provider/source/license drift trend closure
    MI-100.80.04 Export package hygiene and install smoke
  MI-100.90 Independent audit
    MI-100.90.01 Generate final audit handoff pack
    MI-100.90.02 External auditor executes checklist
    MI-100.90.03 Ingest signed/traceable audit result
    MI-100.90.04 Certification passes only after all domains pass
```

## Recommended Next Tasks

| Next ID | Task | Why first | Required evidence |
| --- | --- | --- | --- |
| 0137 | External tracker issue creation execution | Tracker import/template/gate is now the nearest blocked chain visible to audit and certification. | Redacted tracker issue evidence bundle; no raw secrets or private URLs. |
| 0138 | External proof-ref/live proof execution | Closure summary still blocks 22 external categories. | proof-ref bundle, live proof bundle, work item binding and gate pass. |
| 0139 | Production live delivery execution | API/HF/Bot/webhook live proof is the main product-facing blocker. | Real endpoint/token smoke summaries with redaction. |
| 0140 | Independent audit result intake | Rehearsal is not audit completion. | Traceable auditor result and checklist disposition. |
| 0141 | Developer public platform live | Infrastructure for external developers must be self-service. | Public portal, SDK install, sandbox token and docs smoke. |
| 0142 | Core bazi/ziwei professional quality expansion | Infrastructure must prove domain quality, not only runtime health. | Expert/anonymous corpus, golden diff, benchmark trend and review rubric. |

## Non-Claim Rule

FateCat can only claim 100% measurement infrastructure when all of these are true:

- `current-release-proof.proofGate.status=passed` for the final release commit.
- `current-audit-bundle.auditGate.status=passed` for the same commit.
- `measurement-infrastructure-certification.status=passed` and `canClaim100Percent=true`.
- `third-party-audit-rehearsal.rehearsalGate.status=passed` plus independent auditor result attached.
- All external pending work items have accepted proof-ref and live proof evidence.
- Production live API/HF/Bot/webhook/OIDC/SIEM/OTel/Vault/KMS/multi-replica/developer-platform evidence exists and is redacted.
- 八字/紫微 production quality corpus and benchmark gates are sufficient for the declared service level.

Until then, the correct phrase remains: `外部连通验证待执行`.
