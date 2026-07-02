# Acceptance Checklist

# Global Standards

- [x] 变更边界限定在 OTel collector/SLO adapter contract baseline、gate、tests、docs 和任务文档。
- [x] 不启动真实 OpenTelemetry Collector。
- [x] 不连接 trace backend、metrics backend、alert platform 或第三方监控系统。
- [x] 不保存真实 token、secret、DSN、用户输入、出生地区、报告正文、生产日志、metrics snapshot 或 trace 数据。
- [x] focused tests、validators、ruff、secret scan 和 quick local CI 通过。
- [x] 任务状态与真实 worktree 一致。

# Task Package Checklists

## TP-01.01

- [x] 读取 0061/0063、observability registry、SLO/alert gate、trace smoke。
- [x] 复核 OpenTelemetry Collector 标准结构。
Verify: `git status` / `rg` / `sed` / official docs。
Gate: 当前事实和 0064 边界明确。

## TP-02.01

- [x] 新增 OTel collector dry-run config。
- [x] 新增 SLO evidence contract。
- [x] config/contract 不包含真实 backend URL、token、secret、DSN 或 production trace。
Verify: YAML/JSON syntax + gate。
Gate: config 和 contract 可机器读取。

## TP-02.02

- [x] observability schema 链接 collector/SLO evidence。
- [x] observability registry 链接 collector config、SLO evidence contract 和 gate。
- [x] observability AGENTS 说明职责边界。
Verify: focused tests / docs diff。
Gate: registry/schema/AGENTS 链接一致。

## TP-03.01

- [x] 新增 otel-collector-slo-gate Python 脚本。
- [x] 新增 shell wrapper。
Verify: gate CLI。
Gate: 无外部 backend 依赖。

## TP-03.02

- [x] regression tests 覆盖 gate summary。
- [x] regression tests 覆盖 CLI 输出。
- [x] regression tests 覆盖 config、contract、privacy 和 pending 边界。
Verify: focused pytest。
Gate: 边界断言通过。

## TP-03.03

- [x] quick local CI 运行 otel collector SLO gate。
- [x] quick local CI summary 包含 `otelCollectorSloGate` artifact。
Verify: local-ci summary artifact。
Gate: quick CI 运行新 gate。

## TP-04.01

- [x] API 文档写入 OTel collector/SLO evidence contract。
- [x] roadmap 标记 0064 contract baseline。
- [x] scripts AGENTS 和 INDEX 同步。
Verify: docs diff + rg。
Gate: 文档不夸大。

## TP-04.02

- [x] validators 通过。
- [x] focused tests 通过。
- [x] ruff/py_compile/secret scan 通过。
- [x] quick local CI 通过。
Verify: validation evidence。
Gate: 全部通过。
