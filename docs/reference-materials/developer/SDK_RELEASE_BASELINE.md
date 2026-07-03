# FateCat SDK Release Baseline

This document describes the local SDK release-readiness baseline. It is stronger than the earlier example-only baseline, but it still does not claim package registry publication.

## Package Candidates

| Candidate | Language | Status | Smoke |
| --- | --- | --- | --- |
| `fatecat-python` | Python | installable example | `python_compile` |
| `fatecat-js` | Node | installable example | `node_syntax_or_shape` |
| `fatecat-curl-examples` | Shell | installable example | `bash_syntax` |
| `fatecat-agent-tool-call` | Agent JSON | installable example | `json_shape` |

Machine truth:

```text
contracts/fate/developer/sdk-release-baseline.json
```

## Release Boundary

- `packageRegistryStatus` remains `not_published`.
- `version` is `0.1.0-local`.
- `publishEvidence` must remain `null` until there is real registry publication evidence.
- Registry publication requires install smoke from the package registry, current commit CI evidence, API compatibility notes and provenance evidence.

## Validation

```bash
bash scripts/developer-portal-gate.sh
```

The gate checks package candidate source files, smoke commands, fixed sandbox snapshot digests and developer portal contract wiring.
