# AGENTS.md - GitHub automation

## 目录用途

`.github/` 存放远端自动 quick gate 和受控发布流程。PR 与 `main` push 自动执行 quick CI；完整 Acceptance、容器发布和 HF 部署仍需显式触发。

## 目录结构

```text
.github/
├── AGENTS.md
└── workflows/
    ├── acceptance.yml
    ├── container.yml
    ├── evaluation-nightly.yml
    ├── hf-space-deploy.yml
    └── quick.yml
```

## 职责边界

- `workflows/acceptance.yml`：手动触发 FateCat skill 验收链；不在 push / pull_request 自动执行。
- `workflows/container.yml`：手动构建 FateCat delivery 容器并运行容器 smoke；只有显式选择 `push_image` 时才推送 GHCR、上传 release artifacts、输出 registry digest、生成 GitHub artifact attestation 并执行 attestation verify。
- `workflows/evaluation-nightly.yml`：手动或定时触发 EvaluationRun nightly；只调用 `scripts/evaluation-nightly.sh`，上传 summary/diff/dashboard artifact，不保存 secret、不自动部署。
- `workflows/hf-space-deploy.yml`：手动触发 Hugging Face Space 部署；fork 用户设置 `HF_TOKEN` 后可从 GitHub 网页部署到自己的 Space。
- `workflows/quick.yml`：PR、`main` push 和手动触发的自动 quick gate；只调用 `scripts/local-ci.sh --profile quick`，上传短期 summary evidence，不发布制品。
- 这里不放业务代码、不保存 secret、不生成运行态产物。

## 依赖方向

- `.github/workflows/* -> scripts/acceptance.sh -> scripts/common.sh runtime root resolution`
- `.github/workflows/container.yml -> scripts/container-build.sh + scripts/container-smoke.sh + scripts/release-artifacts.sh + actions/attest@v4`
- `.github/workflows/evaluation-nightly.yml -> scripts/evaluation-nightly.sh -> scripts/run-evaluations.sh + scripts/compare-evaluations.sh + scripts/evaluation-dashboard.sh`
- `.github/workflows/hf-space-deploy.yml -> scripts/hf-space-deploy.sh + infra/huggingface-space`
- `.github/workflows/quick.yml -> scripts/local-ci.sh --profile quick`
- CI 只调用仓库脚本；代码质量门禁以 `scripts/local-ci.sh` 和 `scripts/public-release-gate.sh` 为本地真相源，容器发布门禁以 `scripts/container-smoke.sh` 为单一入口。
