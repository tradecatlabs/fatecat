# 100% Measurement Infrastructure Complete Implementation Plan

Research date: 2026-07-04

This plan is about infrastructure maturity, not divination accuracy claims. FateCat reaches 100% only when every production calculation path is resourceized, reproducible, externally verifiable, observable, secure, policy-gated and independently auditable.

## Current Baseline

| Domain | Current state | Strict conclusion |
| --- | --- | --- |
| Git state | `main` is clean and synced at task start | Planning can proceed without dirty-worktree ambiguity. |
| Independent audit intake | 0140 adds an independent audit result gate and local-ci integration | Audit result can now be ingested structurally, but real auditor result is still external. |
| External proof/live | 0138 remains blocked without real operator credentials and proof/live bundles | This is still the main 100% blocker. |
| Production live | API/HF/Bot/webhook evidence exists as contracts/operator packets, not all real live proofs | External live validation pending. |
| Developer platform | Local developer portal/SDK/sandbox contracts exist | Public portal, installable SDK/package, token issuer/revocation and public docs smoke pending. |
| Core quality | Bazi/Ziwei L4 baseline, evidence trend and MingLi-Bench aggregate baseline exist | Professional corpus, full report diff, human review rubric and external benchmark trend still need expansion. |

## External Infrastructure Source Matrix

| Infra field | Official / standard source | Principle extracted | FateCat mapping |
| --- | --- | --- | --- |
| Cloud architecture | AWS Well-Architected Framework: https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html | Operational excellence, security, reliability, performance, cost and sustainability are explicit pillars | FateCat 100% must be scored by architecture domains, not by a single happy-path smoke. |
| Platform engineering | CNCF Platform Engineering Maturity Model: https://tag-app-delivery.cncf.io/whitepapers/platform-eng-maturity-model/ | Platform is a product with self-service, governance, measurement and continuous maturity | Capability, provider, report, job, evaluation and audit must be self-service resources. |
| API contracts | OpenAPI Specification: https://spec.openapis.org/oas/latest.html | Public HTTP API must be machine-readable and versioned | `/capabilities`, `/reports`, `/metadata`, errors and examples must be release artifacts. |
| Event contracts | AsyncAPI Specification: https://www.asyncapi.com/docs/reference/specification/latest | Async/event interfaces need schemas and examples | Job terminal events, webhook callbacks, evaluation and release events need AsyncAPI/CloudEvents-compatible contracts. |
| Event envelope | CloudEvents: https://cloudevents.io/ | Events should share `id/source/type/subject/time/data` style metadata | FateCat webhook/job/audit/release events need a common envelope for replay and audit. |
| API side effects | Stripe Idempotent Requests: https://docs.stripe.com/api/idempotent_requests | Retried requests must not duplicate side effects | Report jobs and callback submissions need idempotency keys and duplicate suppression. |
| Webhook delivery | Stripe Webhooks: https://docs.stripe.com/webhooks | Event delivery needs signing, retries and endpoint validation | FateCat callbacks need signature, retry policy, delivery history and redacted evidence. |
| Durable workflows | Temporal Durable Execution: https://docs.temporal.io/evaluate/understanding-temporal | Long workflows need durable event history and recovery | CalculationJob/EvaluationJob need event history, restart recovery, retry and timeout policy. |
| Control planes | Kubernetes Controllers: https://kubernetes.io/docs/concepts/architecture/controller/ | Desired/current state and reconciliation are the control-plane core | Capability/provider/release/security/evaluation need spec/status/admission/drift views. |
| Provider ecosystems | Terraform Providers: https://developer.hashicorp.com/terraform/language/providers | Providers are versioned, configured and independently governed | Bazi/Ziwei/Almanac/Meihua providers need version/source/license/deprecation gates. |
| Software catalog | Backstage System Model: https://backstage.io/docs/features/software-catalog/system-model/ | Platform assets need Component/API/Resource/System discovery | FateCat needs catalog discovery for Capability, Provider, Dataset, DeliverySurface and SecurityControl. |
| Observability | OpenTelemetry Signals: https://opentelemetry.io/docs/concepts/signals/ | Traces, metrics and logs are first-class signals | API -> job -> provider -> report needs correlated trace/log/metric evidence. |
| Reliability | Google SRE SLO chapter: https://sre.google/sre-book/service-level-objectives/ | Services are managed by SLI/SLO and error budgets | FateCat needs availability, latency, job success and provider success SLOs. |
| Delivery performance | DORA metrics: https://dora.dev/guides/dora-metrics-four-keys/ | Delivery is measured by deployment frequency, lead time, failure rate and recovery time | Release proof, rollback drill and incident evidence must be trendable. |
| API security | OWASP API Security Top 10 2023: https://owasp.org/API-Security/editions/2023/en/0x11-t10/ | APIs must control authorization, authentication, resource consumption and inventory | RBAC, token scopes, rate limit, body limit, API inventory and negative tests are release blockers. |
| Secure development | NIST SSDF SP 800-218: https://csrc.nist.gov/pubs/sp/800/218/final | Secure software development needs repeatable practices and vulnerability response | Secret scans, dependency review, release evidence and incident response are mandatory. |
| Supply chain | SLSA v1.2: https://slsa.dev/spec/v1.2/ | Build integrity needs provenance and verifiable controls | Every release commit needs CI, artifact provenance, digest and attestation. |
| SBOM | CycloneDX: https://cyclonedx.org/specification/overview/ | Components, services, dependencies and relationships should be machine-readable | Code, container, vendor and data supply-chain assets need SBOM/provenance coverage. |
| AI/evaluation | MLflow docs: https://mlflow.org/docs/latest/index.html | Experiments, artifacts, model/eval metadata need tracking | FateCat evaluation runs need trend store, benchmark policy, corpus version and diff artifacts. |

## 100% Admission Model

FateCat should use two maturity axes:

| Axis | Meaning | Release consequence |
| --- | --- | --- |
| Capability maturity | Whether a measurement system can be executed and exposed | `planned` cannot execute; `production` must pass schema, provider, evidence, privacy and regression gates. |
| Infrastructure maturity | Whether the platform can be externally operated and audited | Local pass is not enough; public live, security, SRE, release, audit and developer evidence must close. |

Infrastructure maturity levels:

| Level | Name | Requirement |
| --- | --- | --- |
| I0 | Registered | Resource exists in contracts/catalog but is not executable. |
| I1 | Local baseline | Local smoke or dry-run exists; no production claim. |
| I2 | Gated | Schema, privacy, policy and regression gates fail fast locally. |
| I3 | Release evidence | Current commit has CI, release artifact, SBOM/provenance and rollback evidence. |
| I4 | External live | Real public endpoint/platform evidence exists with redacted proof refs. |
| I5 | Independently audited | Third-party auditor result and all external pending items are accepted. |

100% requires all production resource domains to reach the declared target level. Most code/resources are around I2-I3; external live and audit domains remain I4/I5 blockers.

## Resource Maturity Matrix

| Resource domain | Target 100% state | Current next gap |
| --- | --- | --- |
| Capability | All production capabilities execute only through unified executor and admission gate | Keep planned future systems non-executable; promote only after provider/eval gates. |
| Provider | Version/source/license/dependency/trace/deprecation governed | Add long-term provider drift trends and external legal review where needed. |
| CalculationJob | Durable external backend, outbox, retry, timeout, recovery, live callback evidence | Real multi-replica/Postgres/webhook/Vault/KMS live proof pending. |
| ReportProfile | JSON/Markdown profile stable across Web/API/Bot/CLI/Skill | Full report golden diff and live multi-surface parity pending. |
| Evidence | Every key conclusion has rule/source/basis/weight/risk/counter-evidence | Expand professional evidence coverage and broken-ref gates. |
| Dataset/KnowledgeSource | Source/hash/license/usage/export policy tracked and audited | Legal/human review and larger anonymous corpus pending. |
| EvaluationRun | History, trend, benchmark, corpus and regression thresholds release-blocking | Expert corpus, MingLi-Bench runner depth and human review rubric pending. |
| DeliverySurface | Public Web/API/Bot/CLI/Skill all prove same profile and privacy behavior | Bot/API/HF/webhook live evidence pending. |
| DeveloperPlatform | OpenAPI, SDK/package, sandbox token issuer/revocation, portal smoke live | Public live developer platform pending. |
| ObservabilitySignal | OTel collector/backend, metrics, traces, logs, SLO, alert and incident drill live | External OTel/SLO/alert evidence pending. |
| SecurityControl | OIDC/IdP, SIEM, Vault/KMS, retention cleanup, tenant isolation and OWASP negative tests | External security platform live evidence pending. |
| ReleaseArtifact | Per-release digest, SBOM/provenance, attestation verify and rollback drill | Must refresh for final release commit. |
| AuditHandoff | Audit package, external proof refs, live proof and independent auditor result all accepted | 0138 and true third-party audit remain pending. |

## Complete Implementation Tree

```text
MI-100 FateCat measurement infrastructure 100%
  MI-100.00 Current truth and anti-overclaim
    MI-100.00.01 Refresh git/CI/release proof for final commit
    MI-100.00.02 Keep certification canClaim100Percent=false until all domains close
    MI-100.00.03 Maintain external pending inventory and issue/proof/live binding
  MI-100.10 External validation closure
    MI-100.10.01 Complete 0138 proof-ref bundle with operator credentials
    MI-100.10.02 Complete live proof bundle for all work items
    MI-100.10.03 Re-run closure summary, certification and rehearsal against accepted proof/live
  MI-100.20 Production live delivery
    MI-100.20.01 API/HF public health/ready/metrics smoke
    MI-100.20.02 Telegram Bot live smoke
    MI-100.20.03 Public webhook callback live smoke
    MI-100.20.04 Live multi-surface semantic diff
  MI-100.30 Runtime platform
    MI-100.30.01 Production Postgres job store and outbox live
    MI-100.30.02 Multi-replica worker lease/heartbeat live
    MI-100.30.03 Recovery, retry, timeout and rollback drills under production-like load
    MI-100.30.04 Exactly-once boundary documented as limitation, not false claim
  MI-100.40 Observability and SRE
    MI-100.40.01 OTel SDK/collector/exporter/backend live evidence
    MI-100.40.02 SLO dashboard, error budget policy and alert evidence
    MI-100.40.03 Incident drill, runbook and DORA trend reporting
  MI-100.50 Security and privacy
    MI-100.50.01 OIDC/IdP integration
    MI-100.50.02 SIEM or immutable audit storage
    MI-100.50.03 Vault/KMS/external secret provider
    MI-100.50.04 Retention cleanup and tenant isolation
    MI-100.50.05 OWASP API negative regression and LLM output policy scan
  MI-100.60 Developer platform
    MI-100.60.01 Public OpenAPI and changelog artifact
    MI-100.60.02 SDK/package install smoke
    MI-100.60.03 Sandbox token issuer, revocation and live gateway
    MI-100.60.04 Public developer portal docs smoke
  MI-100.70 Core quality
    MI-100.70.01 Bazi professional/anonymous corpus expansion
    MI-100.70.02 Ziwei professional/anonymous corpus expansion
    MI-100.70.03 Full report golden diff and semantic summary
    MI-100.70.04 MingLi-Bench/external benchmark trend gate
    MI-100.70.05 Human review rubric and disagreement/counter-evidence handling
  MI-100.80 Supply chain and release
    MI-100.80.01 Per-release GHCR digest and attestation verification
    MI-100.80.02 SBOM/provenance/data/vendor manifest attestation
    MI-100.80.03 Provider/source/license drift trend closure
    MI-100.80.04 Export package hygiene and install smoke
  MI-100.90 Independent audit
    MI-100.90.01 Generate final audit handoff pack
    MI-100.90.02 External auditor executes checklist
    MI-100.90.03 Ingest signed/traceable audit result through 0140 gate
    MI-100.90.04 Certification passes only after all domains pass
```

## Execution Waves

| Wave | Purpose | Tasks | Blocker |
| --- | --- | --- | --- |
| W0 Truth refresh | Keep current commit evidence honest | current release proof, current audit bundle, certification and third-party rehearsal refresh | Needs final commit and remote CI runs. |
| W1 External closure | Close true proof/live blockers | 0138 proof-ref/live evidence execution | Needs operator credentials and redacted evidence bundles. |
| W2 Core quality | Strengthen service-specific correctness | 0142 bazi/ziwei corpus, report diff, human review rubric | Local work possible; human review remains additional evidence. |
| W3 Developer platform | Make the infra self-service | public portal, SDK/package, sandbox token issuer/revocation | Needs public endpoint and package registry/token service. |
| W4 Runtime/SRE/security live | Prove production operability | OTel, SLO, alerts, OIDC, SIEM, Vault/KMS, multi-replica runtime | Needs external platforms. |
| W5 Release/supply chain | Prove final artifact integrity | digest, SBOM, provenance, attestation, rollback drill | Needs final release commit. |
| W6 Independent audit | Close 100% certification | audit handoff, external auditor result, certification pass | Needs third-party authority. |

## Recommended Next Tasks

| Proposed ID | Task | Type | Why next | Required evidence |
| --- | --- | --- | --- | --- |
| 0142 | Core bazi/ziwei professional quality corpus expansion | Local executable | It improves the core service quality without waiting for external credentials. | Expanded anonymous corpus, report diff policy, review rubric, regression pass. |
| 0143 | External proof/live execution continuation | External operator | 0138 remains the main 100% blocker. | Accepted proof-ref and live proof bundles for all work items. |
| 0144 | Developer public platform live | External/public | Infrastructure must be self-service for developers. | Public portal smoke, SDK/package install smoke, sandbox token issue/revoke proof. |
| 0145 | SRE/security external live evidence | External platform | Production infra needs OTel/SLO/OIDC/SIEM/Vault/KMS evidence. | Redacted trace/dashboard/alert/IdP/SIEM/Vault proof refs. |
| 0146 | Final release proof and audit certification refresh | Mixed | 100% can only be claimed for one final commit. | Remote CI URLs, digest, attestation, audit bundle, certification passed. |

## Non-Claim Rule

FateCat cannot claim 100% measurement infrastructure until all of these are true for the same final release commit:

- `current-release-proof.proofGate.status=passed`.
- `current-audit-bundle.auditGate.status=passed`.
- `measurement-infrastructure-certification.status=passed` and `canClaim100Percent=true`.
- `third-party-audit-rehearsal.rehearsalGate.status=passed` with accepted independent audit result attached.
- All external proof-ref/live proof items are accepted.
- Production API/HF/Bot/webhook/OIDC/SIEM/OTel/Vault/KMS/multi-replica/developer-platform evidence exists as redacted proof refs.
- Bazi/Ziwei core quality corpus, benchmark, report diff and review rubric support the declared service level.

Until then, the correct status is: `外部连通验证待执行`.
