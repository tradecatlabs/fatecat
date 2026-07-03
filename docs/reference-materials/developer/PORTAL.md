# FateCat Developer Portal

FateCat developer portal baseline is a local, reproducible entrypoint for Agent and application developers. It points to machine contracts, examples, sandbox fixtures and validation commands. It is not a hosted public portal.

## Entry Points

| Resource | Path |
| --- | --- |
| OpenAPI | `/openapi.json` |
| Metadata | `/metadata` |
| Capabilities | `/capabilities` |
| Providers | `/providers` |
| Evaluations | `/evaluations` |
| Observability | `/observability` |
| Security | `/security` |
| Surfaces | `/surfaces` |
| Errors | `/errors` |

## Machine Contracts

```text
contracts/fate/developer/developer-platform.json
contracts/fate/developer/developer-portal.json
contracts/fate/developer/sdk-release-baseline.json
contracts/fate/developer/sandbox.json
contracts/fate/developer/sandbox-token-contract.json
contracts/fate/developer/sandbox-output-snapshot.json
contracts/fate/developer/api-changelog.json
```

## Local Validation

```bash
bash scripts/developer-docs-smoke.sh
bash scripts/developer-platform-gate.sh
bash scripts/developer-portal-gate.sh
```

The portal gate validates the OpenAPI baseline, SDK example smoke, sandbox fixture execution, fixed output snapshot digests, API changelog and no-overclaim boundaries.

## Boundaries

- No PyPI package is claimed.
- No npm package is claimed.
- No public sandbox token service is implemented.
- No external hosted developer portal is claimed.
- No real token, production URL, real user data, non-Beijing real place or report body may appear in developer assets.
