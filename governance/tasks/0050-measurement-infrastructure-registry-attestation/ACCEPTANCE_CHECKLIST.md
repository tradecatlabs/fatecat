# Acceptance Checklist

# Global Standards

- [x] 不输出 secret。
- [x] 不把本地 imageId 写成 registry digest。
- [x] workflow 包含 `id-token: write`、`attestations: write`、`artifact-metadata: write`。
- [x] workflow push 后输出 digest。
- [x] workflow 使用 `actions/attest@v4` 且 `push-to-registry: true`。
- [x] workflow 运行 `gh attestation verify`。
- [x] release artifacts 上传为 Actions artifact。
- [x] 本地回归测试通过。
- [x] 任务文档校验通过。
- [x] 远端 workflow 对当前 commit 成功或失败证据已落盘。

# Task Package Checklists

## TP-01.01

- [x] 当前 workflow 缺口已确认。
- [x] 官方 action README 已复核。
- Verify: `.github/workflows/container.yml`、`gh api repos/actions/attest/...`。
- Gate: 不猜 action 参数。

## TP-02.01

- [x] workflow 已实现 digest/attestation/verify。
- Verify: `.github/workflows/container.yml`。
- Gate: `push_image=false` 仍不发布。

## TP-03.01

- [x] 回归测试和 release policy 断言已覆盖 attestation 关键文本。
- Verify: pytest + `bash scripts/check-public-release-policy.sh`。
- Gate: workflow 退化时测试失败。

## TP-03.02

- [x] release gate、registry、AGENTS 和操作文档已同步。
- Verify: `rg -n "attestation|artifact-metadata|gh attestation|push-to-registry"`。
- Gate: 文档明确本地 baseline 与 registry attestation 区别。

## TP-04.01

- [x] 本地验证通过。
- [x] 提交推送完成。
- [x] 远端 workflow 证据已记录。
- Verify: command output and GitHub Actions run URL。
- Gate: 未跑远端 workflow 时不写生产完成。
