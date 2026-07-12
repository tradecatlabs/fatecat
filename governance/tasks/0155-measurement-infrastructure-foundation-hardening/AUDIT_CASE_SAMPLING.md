# Audit Case Sampling Decision

- Source: governance/tasks/0155-measurement-infrastructure-foundation-hardening
- Fixed Problem: 分发 smoke、性能 smoke 和全量测试可在源码仓内通过，但 wheel 只验证能力列表、任务文档仍是 Not Started、独立运行的性能脚本会向只读 vendor 写入字节码，形成完成声明、分发边界和副作用门禁的灯下黑。
- Decision: no-case
- Case ID: CASE-0003
- Case Path: /home/lenovo/.codex/skills/auto-review/audit-cases/CASE-0003-task-closeout-evidence-drift.json
- Root Cause Class: implicit-caller-safety-and-closeout-evidence-drift
- Trigger Signals: 子脚本只依赖调用方设置安全环境；测试前卫生检查通过但测试后污染；wheel discovery 被误解为计算引擎可用；任务状态与真实实现不同步。
- Evidence: `DEBUG.md`；`scripts/core-performance-smoke.sh`；`scripts/package-distribution-smoke.sh`；`scripts/vendor-health.sh`；`scripts/local-ci.sh --profile quick`；`TREE_SPEC.json`；`STATUS.md`。
- No-Case Reason: 完成声明与任务状态漂移已由全局 `CASE-0003` 覆盖；vendor 污染的项目特有路径已由脚本自带禁写环境和测试后 `vendor-health` 机械阻断，不再创建重复案例。

## Reusable Audit Questions

- 独立脚本是否自行建立安全环境，还是只能在某个父脚本下安全运行？
- 卫生门禁是否在所有可能产生副作用的测试和 smoke 之后再次执行？
- 分发 smoke 验证的是能力发现、协议资源还是完整计算，声明是否严格匹配？
- TODO、STATUS、验收清单与当前命令证据是否描述同一个状态？

## Evidence Required

- 清理后独立执行 smoke，再执行 vendor/source hygiene。
- 仓库外从 sdist 重建 wheel、安装并检查运行模式和 provider 资产可用性。
- 当前提交对应的本地 quick CI、远端 quick CI 与任务 closeout 状态。
