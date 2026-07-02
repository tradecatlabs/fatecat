# Acceptance Checklist

# Global Standards
- [x] 文件路径具体，命令可复现。
- [x] 测试结果来自真实执行输出。
- [x] 不输出 token、secret、password、DSN 或 registry credential。
- [x] 文档说明本任务只覆盖本地 container baseline。

# Task Package Checklists
## TP-01.01
- [x] Docker 和现有容器脚本已盘点。
- Verify: `docker version`、`scripts/container-build.sh`、`scripts/container-smoke.sh`。
- Gate: Docker daemon 可用。

## TP-02.01
- [x] container release evidence 生成器完成。
- Verify: `bash scripts/container-release-evidence.sh --output-json <path>`。
- Gate: JSON 字段完整。

## TP-03.01
- [x] live gate 校验 container JSON 内容。
- Verify: pytest pass/fail。
- Gate: 错误 imageId/smokeStatus 不通过。

## TP-04.01
- [x] public-release 可选生成并传递 container evidence。
- Verify: `FATECAT_PUBLIC_RELEASE_WITH_CONTAINER=1 ... public-release-gate.sh`。
- Gate: container check 为 pass。

## TP-05.01
- [x] targeted tests、container smoke、task tree validation、closeout 全部完成。
- Verify: closeout packet。
- Gate: 任务树有效。
