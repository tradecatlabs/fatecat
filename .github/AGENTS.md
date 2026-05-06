# AGENTS.md - GitHub automation

## 目录用途

`.github/` 存放远端自动化配置，使 GitHub 能复现本地交付门禁。

## 目录结构

```text
.github/
├── AGENTS.md
└── workflows/
    └── acceptance.yml
```

## 职责边界

- `workflows/acceptance.yml`：在 push / pull_request 时执行 FateCat skill 验收链。
- 这里不放业务代码、不保存 secret、不生成运行态产物。

## 依赖方向

- `.github/workflows/* -> scripts/acceptance.sh -> scripts/project/*`
- CI 只调用仓库脚本；具体质量门禁仍以 `scripts/acceptance.sh` 为单一入口。
