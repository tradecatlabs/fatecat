# Acceptance Checklist

# Global Standards
- [x] Target end state is described before migration tasks.
- [x] Real constraints and inertia constraints are separated.
- [x] External source research is traceable by URL.
- [x] Current repo facts come from git/task/CI artifacts, not memory.
- [x] Planning-only boundary is explicit.
- [x] No external live result is fabricated.
- [x] No secret, token, DSN, raw URL, user input or report body is written.
- [x] The roadmap update keeps `canClaim100Percent=false` until certification passes.

# Task Package Checklists
## Research baseline

### TP-01.01 External infrastructure sources
- [x] CNCF Platform Engineering source recorded.
- [x] Kubernetes controller source recorded.
- [x] OpenAPI, AsyncAPI and CloudEvents sources recorded.
- [x] Temporal, OpenTelemetry and Google SRE sources recorded.
- [x] OWASP, NIST, SLSA, CycloneDX and GitHub attestation sources recorded.
Verify: source URLs appear in `CONTEXT.md` and roadmap section `6.38.1`.
Gate: research covers the required infrastructure domains.

### TP-01.02 Current repo evidence
- [x] Current HEAD and 0145/0146/0147 evidence recorded.
- [x] 0147 local CI and remote Acceptance run recorded without overclaim.
- [x] Certification remains blocked and `canClaim100Percent=false`.
Verify: `CONTEXT.md` repo evidence table.
Gate: local, remote and external-pending evidence are separated.

## Target and gap model

### TP-02.01 Target end state
- [x] 100% target state is defined by infrastructure evidence closure.
- [x] Non-claim rule is explicit.
- [x] New prediction systems are excluded from default report until admitted through protocol.
Verify: roadmap section `6.38.3`.
Gate: no feature-count or marketing definition of 100% remains.

### TP-02.02 Gap matrix
- [x] Nine-domain gap matrix exists.
- [x] Every domain has current state, 100% target and next evidence.
- [x] External proof blockers are visible.
Verify: roadmap section `6.38.4`.
Gate: no domain is marked complete without evidence.

## Implementation plan

### TP-03.01 Remaining task tree
- [x] MI-100 post-0147 task tree exists.
- [x] Operator, human review and final release proof nodes are separated.
- [x] 0149/0150 next tasks are named without replacing 0144-0147 external blockers.
Verify: roadmap sections `6.38.5` and `6.38.6`.
Gate: task tree can be executed without second-order interpretation.

### TP-03.02 Completion gates and failure predicates
- [x] Completion gate list exists.
- [x] Failure predicate list exists.
- [x] `canClaim100Percent=true` is gated by certification only.
Verify: roadmap sections `6.38.7` and `6.38.8`.
Gate: any missing external proof prevents 100% claim.

## Documentation and validation

### TP-04.01 Roadmap and task package
- [x] Roadmap post-0147 section added.
- [x] Task package README/CONTEXT/PLAN/ACCEPTANCE/TODO/STATUS updated.
- [x] Scope remains documentation-only.
Verify: git diff for roadmap and task directory.
Gate: no business code changed.

### TP-04.02 Validation
- [x] Task docs validator executed after edits.
- [x] Placeholder scan executed after edits.
- [x] `git diff --check` executed after edits.
Verify: command outputs in terminal.
Gate: validation must pass before commit.
