# Planning Summary

本任务把 `MI-NEXT-02` 落地为最小生产发布证明切片：保持 container workflow 手动触发，只有 `push_image=true` 才推送 GHCR；推送后读取 immutable digest，用 `actions/attest@v4` 生成 registry attestation，并用 GitHub CLI verify。

# Lifecycle Gates

禁止跳过任何 gate；不得把 tag push、本地 imageId 或本地 SBOM baseline 写成 registry attestation 已完成。

| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | 明确 GHCR digest/attestation 验收口径 | Done |
| RESEARCH | 官方 action 和 CLI 用法已复核 | Done |
| PLAN | 任务树和变更边界明确 | Done |
| BUILD | workflow、门禁、文档待实现 | In Progress |
| TEST | 本地回归与任务文档校验待执行 | Pending |
| REVIEW | 远端 workflow 待验证 | Pending |
| SHIP | 提交、推送、CI 证据待完成 | Pending |

# Simplest Path

不替换既有 `scripts/container-build.sh` / `scripts/container-smoke.sh`。只在现有 manual container workflow 的 push 分支后补 digest、artifact upload、attestation 和 verify。

# Split Strategy

- TP-01：确认当前缺口和官方用法。
- TP-02：修改 workflow。
- TP-03：增加回归门禁并同步文档。
- TP-04：本地验证、提交推送、远端 workflow。

# Execution Waves

| Wave | Nodes | Purpose | Status |
| --- | --- | --- | --- |
| 1 | TP-01.01 | 现状和官方用法复核 | Done |
| 2 | TP-02.01 | workflow 实现 | In Progress |
| 3 | TP-03.01, TP-03.02 | 门禁和文档 | Pending |
| 4 | TP-04.01 | 验证、提交、远端 workflow | Pending |

# Next Executable Leaves

| Node ID | Action |
| --- | --- |
| TP-02.01 | 修改 `.github/workflows/container.yml`。 |

# Future-Optimal Contract

Target end state: release artifact 必须从“本地可构建”提升为“registry digest + CI artifact + attestable provenance + verify command”。

Real constraints: GitHub Actions attestation 只能在远端 workflow 真跑后证明；本地没有 `gh attestation` 子命令。

Inertia constraints: 现有 workflow 只 push tag，不能继续把 tag 当 release proof。

Kill list: 只推 `:main` tag、只记录 imageId、只上传本地 provenance、没有 verify step。

Proof point: workflow run with `push_image=true` 产生 digest summary、attestation URL 或 verify pass。

Falsifier: 远端 workflow push 成功但 verify 失败，或 digest 输出为空。

Migration slice: 本轮只处理 container workflow release proof；Telegram Bot、OIDC/SIEM、OTel 继续后续任务。

# Ponytail Contract

Existence check: MI-NEXT-02 是 0049 后明确下一项，且 release gate 当前缺真实 registry digest/attestation。

Selected ladder rung: 复用 GitHub Actions 官方 `actions/attest@v4`，只写 glue workflow 和测试。

Skipped scope: 不自研签名，不接 cosign，不实现 SBOM registry attestation，不改业务代码。

Ceiling / upgrade path: 后续可把 SBOM 也作为 registry attestation 或 release asset attestation。

Minimal runnable check: workflow text regression、public release policy、task docs validation。

# Runtime Workflow Contract

- risk_level: medium
- affected_flows: container release workflow, live release evidence, public release policy
- state_changes: GitHub workflow and docs
- side_effects: remote workflow with `push_image=true` will publish GHCR image tags
- rollback: revert workflow/docs/tests/task files; optionally delete GHCR tags if required by release owner

# Dependency Graph

```text
TP-01.01 -> TP-02.01 -> TP-03.01
TP-02.01 -> TP-03.02
TP-03.01 + TP-03.02 -> TP-04.01
```

# Rollback Protocol

- 恢复 `.github/workflows/container.yml` 到只 build/smoke/push tag 状态。
- 恢复 release gate、registry、AGENTS、docs 和 tests 的 attestation 口径。
- 保留任务记录中的失败证据，不删除历史事实。
