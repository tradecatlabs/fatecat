# Context

0087 已完成本地 sandbox access gateway 并推送。路线图中 0088 明确要求当前 release proof：remote CI、container digest、SBOM/provenance、attestation verify 和 rollback evidence。当前仓库已有 `live-release-gate`、container workflow、release artifacts 和 rollback drill，但缺少一个专门验证“这些证据是否属于当前 HEAD”的聚合 gate。

## Current Facts

- `acceptance.yml` 已可手动对当前 commit 运行完整 acceptance。
- `container.yml` 已支持 `push_image=true`，推送 GHCR image、上传 release artifacts 并执行 GitHub attestation verify。
- `release-artifacts.py` 可生成本地 SBOM/provenance baseline。
- `rollback-drill.py` 可生成本地 dry-run rollback evidence。
- 当前仍缺生产 API、HF Space 和 Telegram Bot live 真实证据。

## Design Decision

新增 `current-release-proof` gate，而不是扩大 `live-release-gate`：

- `live-release-gate` 继续表达完整 live release readiness。
- `current-release-proof` 专注当前 commit 的 CI/container/attestation/artifact/rollback/git clean 证据。
- 默认 local-contract 不触网，required mode 才查询 GitHub/GHCR。

## Risk Level

`medium`：新增 GitHub/GHCR 查询脚本和 release gate 证据口径。无生产写入；远端 container workflow 会在显式触发时写 GHCR package。

## External Pending

- 外部连通验证待执行：生产 API /health /ready /metrics。
- 外部连通验证待执行：Hugging Face Space /web。
- 外部连通验证待执行：Telegram Bot live smoke。

# Repo Evidence

- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 已列出 0088 Current release proof。
- `.github/workflows/container.yml` 已包含 GHCR digest、release artifact upload 和 attestation verify。
- `contracts/fate/delivery/release-gate.json` 是 release evidence 真相源。
- `scripts/live-release-gate.py` 已有 release evidence contract gate。

# Constraints Matrix

| Constraint | Decision |
| --- | --- |
| No remote dependency in quick CI | Provide `--skip-remote` local-contract mode. |
| Current commit only | Check `headSha == HEAD`, origin branch, short SHA container tag and rollback commit. |
| Do not leak credentials | Use gh/docker only through captured redacted output; never print tokens. |
| Existing release gate remains | Register current proof as additional local/external command, not replacement. |

# Change Boundary

- Changed: scripts, release contracts, tests, AGENTS, task docs and roadmap.
- Not changed: production API/HF/Bot live logic, container workflow behavior, release artifact format.

# Risk Matrix

| Risk | Level | Mitigation |
| --- | --- | --- |
| Historical run reused accidentally | High | Require run `headSha` to equal current commit. |
| Local imageId mistaken for registry digest | High | Require `docker buildx imagetools inspect` registry digest or provided `sha256:<64 hex>`. |
| Token leakage from gh output | Medium | Redact sensitive patterns and do not call `gh auth status`. |

# Assumptions and Falsification

- Assumption: GitHub Actions + GHCR attestation are sufficient current release proof for container supply chain.
- Falsifier: current commit container tag not found, attestation verify fails, or release artifact for current SHA is missing.

# Critical Ambiguities

- Production API/HF/Bot live readiness remains outside 0088.
- True production rollback execution remains operator-signed future evidence; local rollback is dry-run only.

# Debug Evidence Contract

- 调试模式: Optional
- If GitHub/GHCR verification fails, capture run URL, digest/ref and redacted error output before changing code.

# Task Package Context Map

## TP-01 SPEC

Context: Identify current commit release proof gap after 0087.

## TP-02 PLAN

Context: Define local-contract and required-current-release modes.

## TP-03 BUILD

Context: Implement current proof script, contracts, AGENTS and regression.

## TP-04 TEST

Context: Run focused tests, local proof, secret scan and quick CI.

## TP-05 SHIP

Context: Commit/push, trigger remote acceptance/container workflow and verify current release proof.
