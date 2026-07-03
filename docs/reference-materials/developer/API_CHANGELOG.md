# FateCat API Changelog

This changelog records developer-facing API and contract changes for the local developer platform baseline.

## v1 baseline

- `2026-07-02`: Local OpenAPI export, sandbox fixtures, curl/Python/Node/Agent examples and developer docs smoke baseline.
- `2026-07-02`: Developer platform contract, SDK/package baseline metadata, sandbox token contract and developer platform gate.
- `2026-07-03`: Local developer portal baseline, SDK release-readiness manifest, fixed sandbox output snapshot and developer portal gate.
- `2026-07-03`: Local sandbox access gateway baseline for scoped capability execution, rate-limit smoke and redacted audit evidence.

## Compatibility Policy

- Breaking changes require a machine-readable changelog entry in `contracts/fate/developer/api-changelog.json`.
- Public removals require migration guidance and a compatibility window.
- Current SDK assets are examples and package metadata only; no PyPI or npm package is claimed.
- Public sandbox token issuance remains future work until live external evidence exists; the local gateway only proves runtime access-control semantics.
