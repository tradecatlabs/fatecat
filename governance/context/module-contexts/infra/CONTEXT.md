---
id: CTX-INFRA
type: module-context
status: current
owner: platform
created: 2026-07-13
last_reviewed: 2026-07-13
code_path: infra
---

# Infrastructure Context

## 模块职责

- 定义容器、HF Space、环境默认值、数据库 schema 和运行准入期望状态。
- `infra/runtime/local-state/` 只承载可删除运行态，不是源码、分发或审计真相源。
- secret 由平台环境注入，不写入镜像、Git、日志或发布制品。

## 依赖边界

- delivery 读取环境与运行路径；infra 不拥有测算规则。
- `.github` 与 `scripts` 调用容器/HF 入口，发布证据绑定具体 commit 和 digest。

## 关键门禁

- `bash scripts/container-smoke.sh`
- `bash scripts/production-readiness.sh`
- `bash scripts/check-export-hygiene.sh <bundle>`
- `bash scripts/secret-scan.sh`

## 禁止事项

- 禁止把 local-state、数据库、缓存或嵌套 exports 放入发行包。
- 禁止把 localhost/dry-run 当作公网生产证据。
- 禁止在可选渠道故障时错误标记核心进程不可用。
