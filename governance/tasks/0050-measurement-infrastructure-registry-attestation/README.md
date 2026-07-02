# Task Overview

- Task ID: `0050`
- Slug: `measurement-infrastructure-registry-attestation`
- Objective: `执行 MI-NEXT-02，把 FateCat container release 从本地 imageId baseline 推进到 GHCR registry digest、GitHub artifact attestation、release artifact CI upload 和 attestation verify gate。`
- Status: `In Progress`

## In Scope

- 修改 `.github/workflows/container.yml`：在显式 `push_image=true` 时推送 GHCR，输出 immutable digest，生成 GitHub artifact attestation，并在 workflow 内 verify。
- 上传 CI release artifacts：`release-artifacts.sh` 输出的 SBOM/provenance/manifest 作为 GitHub Actions artifact。
- 更新 release gate contract、delivery registry、`.github/AGENTS.md`、`scripts/AGENTS.md` 和操作文档口径。
- 增加回归测试/发布策略门禁，防止 workflow 回退成只推 tag。
- 记录任务包和验证证据。

## Out of Scope

- 不配置或输出 registry token；只使用 GitHub Actions `github.token`。
- 不执行真实 Telegram Bot live smoke。
- 不接 OIDC/SIEM/监控平台。
- 不把本地 `imageId` 写成 GHCR digest。
- 不改业务测算代码。

## Task Package Tree

```text
TP-01 现状与官方用法复核
  TP-01.01 复核 container workflow、release gate 和 GitHub attestation action
TP-02 Workflow 实现
  TP-02.01 增加 GHCR digest 输出、artifact upload、attestation 和 verify step
TP-03 门禁与文档
  TP-03.01 增加 workflow 回归测试和发布策略断言
  TP-03.02 同步 release gate、registry、AGENTS 和操作文档
TP-04 验证与交付
  TP-04.01 运行本地校验、提交推送并触发远端 container workflow
```

## Requirement Alignment

- 对齐 `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 的 `MI-NEXT-02`。
- 对齐 GitHub `actions/attest@v4` 官方用法：`subject-name`、`subject-digest`、`push-to-registry`。
- 对齐 release gate：真实生产容器证据必须是 registry digest，不是本地 imageId。

## Task Package Overview

| Task Package ID | Parent | Depth | Priority | Type | Leaf | Depends On | Wave | Ready | Parallelizable | Objective |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | P0 | package | No | - | - | No | Yes | 复核当前 workflow 和官方 attestation 用法。 |
| TP-01.01 | TP-01 | 2 | P0 | action | Yes | - | 1 | No | Yes | 确认 workflow 缺口和 action 权限/参数。 |
| TP-02 | ROOT | 1 | P0 | package | No | TP-01.01 | - | No | No | 修改 container workflow。 |
| TP-02.01 | TP-02 | 2 | P0 | action | Yes | TP-01.01 | 2 | No | No | 增加 digest、attestation、verify 和 artifact upload。 |
| TP-03 | ROOT | 1 | P0 | package | No | TP-02.01 | - | No | No | 更新门禁和文档。 |
| TP-03.01 | TP-03 | 2 | P0 | action | Yes | TP-02.01 | 3 | No | No | 增加回归测试和 release policy 断言。 |
| TP-03.02 | TP-03 | 2 | P0 | action | Yes | TP-02.01 | 3 | No | No | 同步 release gate、registry、AGENTS 和操作文档。 |
| TP-04 | ROOT | 1 | P0 | package | No | TP-03.01, TP-03.02 | - | No | No | 本地验证和远端验证。 |
| TP-04.01 | TP-04 | 2 | P0 | action | Yes | TP-03.01, TP-03.02 | 4 | No | No | 运行测试、提交、推送和 GitHub Actions。 |

## Reading Order

1. `README.md`
2. `CONTEXT.md`
3. `PLAN.md`
4. `ACCEPTANCE.md`
5. `ACCEPTANCE_CHECKLIST.md`
6. `TODO.md`
7. `STATUS.md`
