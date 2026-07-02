# Repo Evidence

- 当前目录：`/home/lenovo/.projects/fatecat`。
- 当前分支：`main...origin/main [ahead 1]`。
- 当前未推送 commit：`b46d19d docs: add measurement infrastructure deep plan`。
- 当前 workflow 缺口：`.github/workflows/container.yml` 只 build/smoke/push tag，不输出 digest、不生成 attestation、不 verify。
- 上游任务：0049 已把 `MI-NEXT-02` 定为下一步。

# Official Evidence

- `actions/attest@v4.1.1` latest release confirmed by `gh api repos/actions/attest/releases/latest`。
- `actions/attest@v4` README 明确容器镜像使用 `subject-name` + `subject-digest`，`push-to-registry: true`，并要求 `id-token: write`、`attestations: write`、`artifact-metadata: write`。
- 本地 `gh` 版本没有 `gh attestation` 子命令；workflow verify 依赖 GitHub-hosted runner 提供的新版本 GitHub CLI。

# Constraints Matrix

| 约束 | 处理 |
| --- | --- |
| 只允许显式发布 | workflow 继续只支持 `workflow_dispatch`，`push_image=false` 默认不发布 |
| 不泄露 token | 使用 `${{ github.token }}` 登录 GHCR，不输出 token |
| registry digest 必须 immutable | push 后用 `docker buildx imagetools inspect` 读取 `sha256:<64 hex>` digest |
| tag 不能替代 digest | tests 和 release policy 必须检查 digest/attestation 字段 |
| attestation 必须可验证 | workflow 内使用 `gh attestation verify oci://<image>@<digest>` |
| Bot token 仍缺失 | 不处理 0048，不把 Bot live 写成完成 |

# Change Boundary

允许修改：

- `.github/workflows/container.yml`
- `.github/AGENTS.md`
- `scripts/check-public-release-policy.sh`
- `scripts/AGENTS.md`
- `contracts/fate/delivery/release-gate.json`
- `contracts/fate/delivery/registry.json`
- `docs/reference-materials/operations/测算基础设施 API 接入.md`
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`
- `tests/regression/*`
- `governance/tasks/0050-*`
- `governance/tasks/INDEX.md`

禁止修改：

- 业务测算源码
- Dockerfile 构建逻辑
- 真实 secret 和 `.env`
- Telegram Bot live smoke 口径

# Risk Matrix

| 风险 | 等级 | 控制 |
| --- | --- | --- |
| workflow permission 不兼容 | 高 | 使用 `actions/attest@v4` README 列出的权限；本地测试只检查文本，远端 workflow 是最终证据 |
| gh CLI attestation 子命令缺失 | 中 | 记录本地缺口；远端验证失败时进入后续修复，不伪造通过 |
| 推送 GHCR 有副作用 | 中 | 只在手动 `push_image=true` 时执行；默认 workflow 不发布 |
| tag 被误认为 digest | 高 | workflow 输出 digest，并用 attestation subject digest 验证 |
| release artifact 与远端 attestation 混淆 | 中 | 文档区分 CI upload、本地 baseline 和 registry attestation |

# Assumptions and Falsification

- 假设：GitHub-hosted runner 的 `gh` 支持 `gh attestation verify`。
- 证伪方式：远端 container workflow 在 verify step 失败。
- 调试模式: Optional

# Critical Ambiguities

- 是否同时要求 SBOM registry attestation：本轮上传 SBOM/provenance artifact，并为 container digest 做 provenance attestation；SBOM registry attestation 可作为后续增强。
- release tag 与 main 是否都要 attest：本轮 main 和 `refs/tags/v*` 都会分别 push digest、attest 和 verify。

# Debug Evidence Contract

Required if remote workflow fails. 需要记录 run URL、失败 step、stdout/stderr 摘要、根因和回归验证。

# Task Package Context Map

- TP-01.01：读取 workflow、release gate、action README 和 gh CLI。
- TP-02.01：修改 `.github/workflows/container.yml`。
- TP-03.01：新增测试和 shell policy 断言。
- TP-03.02：同步 contracts/docs/AGENTS/roadmap。
- TP-04.01：运行本地测试、提交推送、触发远端 workflow。
