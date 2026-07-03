# Planning Summary

0089 converts “current release proof + audit handoff + dry-run + rollback + SBOM/provenance” from scattered artifacts into one current commit audit bundle. The goal is not to claim production is fully verified; the goal is to make the evidence boundary explicit enough for third-party audit.

# Lifecycle Gates

SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP 不得跳过 gate；任一阶段缺少证据时，后续阶段只能记录为 pending/blocked，不能声明 passed。

| Phase | Gate |
| --- | --- |
| SPEC | 0088 release proof exists and MI-NEXT-10 audit package gap confirmed. |
| PLAN | current audit bundle local/required modes and non-claims documented. |
| BUILD | Script aggregates existing evidence and writes Markdown/JSON outputs. |
| TEST | Focused regression, ruff, secret scan and quick CI pass. |
| REVIEW | Required mode cannot accept local-contract current release proof or dirty git. |
| SHIP | Final commit remote CI/current release proof/current audit bundle pass. |

# Simplest Path

- Add one audit contract.
- Add one script pair.
- Wire it into local-ci.
- Add focused regression.
- Document boundaries in AGENTS/task/roadmap.

# Split Strategy

- TP-01/02 define what a current audit bundle is and is not.
- TP-03 implements contract/generator/wiring.
- TP-04 validates locally.
- TP-05 performs final commit delivery proof.

# Execution Waves

| Wave | Nodes |
| --- | --- |
| W1 | TP-01, TP-02 |
| W2 | TP-03 |
| W3 | TP-04 |
| W4 | TP-05 |

# Runtime Workflow Contract

- Local mode: `current-audit-bundle.sh --output-dir <dir> ...` returns command success if bundle structure is valid, even when `auditGate=blocked` due local proof/external pending.
- Required mode: `current-audit-bundle.sh --require-current-release --local-ci-summary <summary.json> ...` returns non-zero unless current release proof, local CI, audit handoff, dry-run, release artifacts and rollback evidence are accepted for current HEAD.
- Output kind: `fatecat.current_audit_bundle`.
- Side effects: writes only output files under requested output dir.

# Next Executable Leaves

| Node ID | Action |
| --- | --- |
| TP-04 | Run focused tests, ruff, secret scan and quick CI. |

# Dependency Graph

```text
TP-01 -> TP-02 -> TP-03 -> TP-04 -> TP-05
```

# Rollback Protocol

- Remove `scripts/current-audit-bundle.py/.sh`.
- Remove `contracts/fate/audit/current-bundle.json`.
- Remove local-ci current audit bundle wiring and focused regression.
- Remove AGENTS/task/roadmap references.
- Existing audit handoff, dry-run, release artifacts, rollback drill and current release proof remain unchanged.

# Plan

## TP-01 SPEC

- Confirm audit package gap after 0088.
- Confirm existing artifacts to consume.

## TP-02 PLAN

- Define required outputs and evidence IDs.
- Keep external live and third-party audit signatures outside current scope.

## TP-03 BUILD

- Implement current audit bundle generator.
- Add audit contract.
- Wire local-ci summary and docs.
- Add focused tests.

## TP-04 TEST

- Focused pytest.
- Ruff/format.
- Secret scan.
- Quick CI.

## TP-05 SHIP

- Commit and push.
- Verify remote acceptance/container workflow.
- Generate final current release proof and required current audit bundle.
