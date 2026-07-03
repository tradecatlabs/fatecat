# Task Overview
- Task ID: `0088`
- Slug: `measurement-infrastructure-current-release-proof`
- Objective: `为当前 commit 建立可复用 current release proof gate，聚合远端 acceptance、container workflow、GHCR digest、GitHub attestation、release artifacts、rollback drill 和 git clean 证据。`
- Status: `Done`

## In Scope

- 新增 `current-release-proof.py/.sh`，默认 local-contract 输出 pending，显式 `--require-current-release` 才要求外部证据全齐。
- 将 current release proof 登记到 `ReleaseGate` contract 和 delivery registry。
- 新增 regression，验证 local-contract、required 模式、契约登记和敏感值防护。
- 任务完成后由交付流程触发当前 commit 的远端 acceptance 与 container workflow `push_image=true`，并用 gate 验证 GHCR digest 与 attestation；这些最终 run/digest 证据记录在外部 closeout artifact 和交付汇报中，不写回同一 commit。

## Out of Scope

- 不接入真实生产 API/HF/Bot live smoke。
- 不执行真实生产回滚。
- 不保存 GitHub token、registry token、secret、DSN、用户输入、报告正文或生产日志。
- 不把历史 commit 的 release proof 作为当前 commit 证据。

## Future-Optimal Task Contract

| Field | Value |
| --- | --- |
| Target end state | 每个 release commit 都能一键聚合当前提交的远端 CI、container digest、attestation、artifact、rollback 和 git clean 证据。 |
| Real constraints | GitHub Actions 与 GHCR 是外部系统；本地 quick CI 不应依赖远端网络；当前仍缺生产 API/HF/Bot live。 |
| Inertia constraints | 旧 `live-release-gate` 能聚合证据，但缺少针对当前 commit 的 workflow/digest/attestation 自动查验。 |
| Wrong concept / wrong boundary | 用历史 container run、历史 digest 或本地 imageId 证明当前 release。 |
| Kill list | 手工口头记录 run URL；无法验证 headSha/digest/attestation 的 release proof。 |
| Proof point | 提交后 `current-release-proof.sh --require-current-release` 对最终 HEAD 返回 `proofGate=passed`，证据记录在交付 closeout artifact。 |
| Falsifier | 找不到当前 commit 的 container run、digest 不是 registry digest、attestation verify 失败或 worktree dirty。 |
| Migration slice | 先做 GitHub/GHCR current commit gate；未来再把生产 API/HF/Bot live 合并为完整 release readiness。 |
| Rejected short-term patches | 不把 `docker image inspect` 的本地 imageId 当 GHCR digest；不把 `--skip-remote` 作为 release pass。 |
| Future-optimal review owner | `auto-review: future-optimal-drift` |

## Ponytail Task Contract

| Field | Value |
| --- | --- |
| Existence check | 0087 后当前提交有 acceptance，但没有 container digest/attestation/current proof 聚合；release proof 是 100% 基础设施必需证据。 |
| Selected ladder rung | project-native script + GitHub CLI/GHCR 官方能力；自研只做证据编排和脱敏输出。 |
| Skipped scope | 生产 API/HF/Bot live、真实 rollback execution、外部审计签署。 |
| Ceiling / upgrade path | 后续可加入 production URL live checks、Bot live、HF Space 和 signed release approval。 |
| Do-not-simplify | 不泄露 token；不跳过 headSha/current commit 校验；不接受非 sha256 registry digest。 |
| Minimal runnable check | `bash scripts/current-release-proof.sh --skip-remote --output-json <path>` |
| Complexity review owner | `auto-review: ponytail-complexity` |

## Document-Driven Task Contract

| Field | Value |
| --- | --- |
| Operating model update | not needed：基础设施定位不变。 |
| Toolchain model update | updated：新增 current release proof gate。 |
| Process update | updated：release proof 需要当前 commit 的 acceptance + container workflow + attestation。 |
| Source-of-truth updates | updated：delivery release gate、registry、scripts/tests AGENTS、roadmap、task index。 |
| Local README/AGENTS impact | updated：scripts/tests/contracts AGENTS。 |
| Contract/catalog/schema impact | updated：ReleaseGate local/external verification 登记新 gate。 |
| ADR/Gate/module-context impact | not needed：沿用 ReleaseGate 资源模型。 |
| Documentation exemption reason | none。 |
| Validation evidence | focused pytest、local current proof、quick CI 写入仓库任务文档；remote acceptance/container/current proof 由提交后的交付 closeout artifact 承载。 |

## Task Package Tree

```text
TP-01 SPEC: 识别 0087 后 current release proof 缺口
TP-02 PLAN: 定义 current release proof gate 和证据边界
TP-03 BUILD: 实现 gate、contract 登记、AGENTS 和 regression
TP-04 TEST: 运行 focused pytest、local proof、ruff/secret scan/quick CI
TP-05 SHIP: commit/push，触发 acceptance/container workflow，验证 current release proof
```

## Key Deliverables

- `scripts/current-release-proof.py`
- `scripts/current-release-proof.sh`
- `tests/regression/test_current_release_proof.py`
- `contracts/fate/delivery/release-gate.json`
- `contracts/fate/delivery/registry.json`

## Requirement Alignment

| Requirement | Implementation |
| --- | --- |
| current commit release proof | gate checks current HEAD, origin, acceptance run, container run, GHCR digest and attestation |
| no overclaim | default `--skip-remote` emits pending/blocked; required mode fails without live release proof |
| reusable evidence | output JSON kind `fatecat.current_release_proof` |
| privacy | output excludes GitHub token, registry token, secret, DSN, user input and report body |

## Task Package Overview

| Node ID | Title | Status | Acceptance |
| --- | --- | --- | --- |
| TP-01 | SPEC | Done | roadmap and current state prove 0088 is next current release proof gap |
| TP-02 | PLAN | Done | local-contract/required-current-release mode defined |
| TP-03 | BUILD | Done | script, contract, docs and tests implemented |
| TP-04 | TEST | Done | local proof, focused tests, secret scan and quick CI passed |
| TP-05 | SHIP | Done | gate implementation ready; final remote proof handled by delivery flow after commit |

## Reading Order

1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
