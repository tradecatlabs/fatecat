# Acceptance Checklist

# Global Standards
- [x] 不修改业务代码、生产 provider、API、Web、Bot、脚本或测试。
- [x] 不伪造外部 proof-ref、live proof、第三方审计或 production certification。
- [x] 使用官方资料 URL 支撑基础设施同构调研。
- [x] 明确 100% 是基础设施成熟度，不是预测命中率。
- [x] 所有外部项未验证时写为 `外部连通验证待执行` 或 pending/blocked。
- [x] 任务包无模板占位符。

# Task Package Checklists
## Current-state evidence intake

### TP-01.01 Evidence intake
- [x] 当前 commit、远端 CI、本地 CI 证据已记录。
- [x] 0142 核心质量扩容证据已记录。
- [x] external proof/live 0 accepted、22 pending 的事实已记录。
Verify: `jq '{status, summary, shipGate}' /tmp/fatecat-local-ci-20260704233925/external-validation-closure-gate.json`.
Gate: external shipGate 仍 blocked，不写成 100% completed。

## External infrastructure research mapping

### TP-02.01 Official source mapping
- [x] 官方资料覆盖平台工程、API、事件、控制面、provider、durable runtime、可观测、SRE、安全、供应链。
- [x] 每个资料映射到 FateCat 资源域和后续要求。
Verify: `rg -n "CNCF Platform Engineering|OpenAPI|AsyncAPI|CloudEvents|Kubernetes|Terraform|Temporal|OpenTelemetry|Google SRE|OWASP|NIST|SLSA|CycloneDX|GitHub Artifact Attestations|Stripe" docs/reference-materials/roadmap/测算基础设施100%实现计划.md`.
Gate: roadmap 保留 URL，未依赖不可复核来源。

## 100% implementation plan refresh

### TP-03.01 Roadmap refresh
- [x] roadmap 新增 post-0142/post-0143 增量刷新。
- [x] 下一批任务编号和依赖顺序明确。
- [x] 完成门禁和失败判定明确。
Verify: `rg -n "Post-0142|0144|0145|0146|0147|0148|0149" docs/reference-materials/roadmap/测算基础设施100%实现计划.md`.
Gate: 后续任务可以直接进入 auto-tasks 执行。

## Task docs and validation closeout

### TP-04.01 Task docs validator
- [x] 0143 任务包完整回填。
- [x] `governance/tasks/INDEX.md` 同步。
- [x] task docs validator 通过。
Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0143-measurement-infrastructure-100-post-0142-deep-research-plan --phase closeout`.
Gate: task docs validator 通过。

### TP-04.02 Placeholder scan
- [x] 占位符扫描无匹配。
Verify: `rg -n "\\{\\{[A-Z0-9_]+\\}\\}" governance/tasks/0143-measurement-infrastructure-100-post-0142-deep-research-plan docs/reference-materials/roadmap/测算基础设施100%实现计划.md`.
Gate: no matches。
