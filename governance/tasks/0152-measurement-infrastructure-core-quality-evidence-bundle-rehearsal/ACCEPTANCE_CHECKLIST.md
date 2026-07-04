# Acceptance Checklist

# Global Standards
- [x] 不得输出真实密钥、token、专家身份、真实用户资料、benchmark 题目/答案或完整报告正文。
- [x] 不得新增旧路径 fallback 或绕过统一 core-quality-human-review-gate。
- [x] 不得让 planned/external/pending evidence 被模板伪装成 accepted。
- [x] 所有新增文件必须有测试或文档验证命令。

# Task Package Checklists
## TP-01
- 标题: 资料与仓库事实对齐
- 验收项:
  - [x] 达成 `资料与仓库事实对齐` 的 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 任务目标与上下文已确认
- 输出物:
  - [x] 读取 0151、core quality gate、professional rubric、local-ci 和官方基础设施资料，形成 0152 的事实边界。
- 标准清单:
  - [x] Verify: 确认子节点范围、依赖与状态闭环
  - [x] Gate: 任务目标与上下文已确认
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-01.01
- 标题: 盘点当前仓库证据链
- 验收项:
  - [x] 达成 `盘点当前仓库证据链` 的 objective，且输出物可复核
- Verify: git status --short --branch && git log -1 --oneline --decorate && rg -n "core-quality-human-review|professional-quality-rubric|external-evidence-submission-readiness" contracts scripts tests docs/reference-materials/roadmap/测算基础设施100%实现计划.md
- Gate: 仓库事实来自命令输出，未脑补外部证据。
- 输出物:
  - [x] 0152 CONTEXT/STATUS 事实基线。
- 标准清单:
  - [x] Verify: git status --short --branch && git log -1 --oneline --decorate && rg -n "core-quality-human-review|professional-quality-rubric|external-evidence-submission-readiness" contracts scripts tests docs/reference-materials/roadmap/测算基础设施100%实现计划.md
  - [x] Gate: 仓库事实来自命令输出，未脑补外部证据。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-01.02
- 标题: 基础设施同构资料映射
- 验收项:
  - [x] 达成 `基础设施同构资料映射` 的 objective，且输出物可复核
- Verify: rg -n "OpenAPI|AsyncAPI|CloudEvents|Kubernetes|OpenTelemetry|SRE|SLSA|CycloneDX|OWASP|NIST|Backstage|Temporal" docs/reference-materials/roadmap/测算基础设施100%实现计划.md governance/tasks/0152-measurement-infrastructure-core-quality-evidence-bundle-rehearsal
- Gate: 调研使用一手资料 URL，且只映射要求，不宣称外部 live 完成。
- 输出物:
  - [x] 路线图 Post-0151 同构矩阵。
- 标准清单:
  - [x] Verify: rg -n "OpenAPI|AsyncAPI|CloudEvents|Kubernetes|OpenTelemetry|SRE|SLSA|CycloneDX|OWASP|NIST|Backstage|Temporal" docs/reference-materials/roadmap/测算基础设施100%实现计划.md governance/tasks/0152-measurement-infrastructure-core-quality-evidence-bundle-rehearsal
  - [x] Gate: 调研使用一手资料 URL，且只映射要求，不宣称外部 live 完成。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-02
- 标题: Core quality bundle 模板契约设计
- 验收项:
  - [x] 达成 `Core quality bundle 模板契约设计` 的 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: source_alignment
- 输出物:
  - [x] 定义 template-only 输出、artifact hash 指南、rubric checklist、benchmark aggregate skeleton、no-leak checklist 和 gate expectation。
- 标准清单:
  - [x] Verify: 确认子节点范围、依赖与状态闭环
  - [x] Gate: 前置步骤已完成: source_alignment
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-02.01
- 标题: 新增模板契约
- 验收项:
  - [x] 达成 `新增模板契约` 的 objective，且输出物可复核
- Verify: .venv/bin/python -m json.tool contracts/fate/evaluations/core-quality-human-review-bundle-template.json >/dev/null
- Gate: 契约声明模板不能作为 accepted review bundle。
- 输出物:
  - [x] contracts/fate/evaluations/core-quality-human-review-bundle-template.json
- 标准清单:
  - [x] Verify: .venv/bin/python -m json.tool contracts/fate/evaluations/core-quality-human-review-bundle-template.json >/dev/null
  - [x] Gate: 契约声明模板不能作为 accepted review bundle。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-02.02
- 标题: 设计模板生成器输出
- 验收项:
  - [x] 达成 `设计模板生成器输出` 的 objective，且输出物可复核
- Verify: bash scripts/core-quality-human-review-bundle-template.sh --output-json /tmp/fatecat-core-quality-template.json --output-markdown /tmp/fatecat-core-quality-template.md && .venv/bin/python -m json.tool /tmp/fatecat-core-quality-template.json >/dev/null
- Gate: 输出中没有 raw URL、secret/token/DSN、专家身份、题目答案或完整报告正文。
- 输出物:
  - [x] scripts/core-quality-human-review-bundle-template.py
  - [x] scripts/core-quality-human-review-bundle-template.sh
- 标准清单:
  - [x] Verify: bash scripts/core-quality-human-review-bundle-template.sh --output-json /tmp/fatecat-core-quality-template.json --output-markdown /tmp/fatecat-core-quality-template.md && .venv/bin/python -m json.tool /tmp/fatecat-core-quality-template.json >/dev/null
  - [x] Gate: 输出中没有 raw URL、secret/token/DSN、专家身份、题目答案或完整报告正文。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-03
- 标题: 实现、测试与 local-ci 接线
- 验收项:
  - [x] 达成 `实现、测试与 local-ci 接线` 的 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: template_contract_design
- 输出物:
  - [x] 落地模板生成器、回归测试和 quick local-ci artifact，证明模板不会解除 blocked gate。
- 标准清单:
  - [x] Verify: 确认子节点范围、依赖与状态闭环
  - [x] Gate: 前置步骤已完成: template_contract_design
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-03.01
- 标题: 新增回归测试
- 验收项:
  - [x] 达成 `新增回归测试` 的 objective，且输出物可复核
- Verify: .venv/bin/python -m pytest tests/regression/test_core_quality_human_review_bundle_template.py tests/regression/test_core_quality_human_review_gate.py
- Gate: 模板不会被 core-quality-human-review-gate 接受。
- 输出物:
  - [x] tests/regression/test_core_quality_human_review_bundle_template.py
- 标准清单:
  - [x] Verify: .venv/bin/python -m pytest tests/regression/test_core_quality_human_review_bundle_template.py tests/regression/test_core_quality_human_review_gate.py
  - [x] Gate: 模板不会被 core-quality-human-review-gate 接受。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检
  - [x] 维护 `DEBUG.md` 并保留回归证据

### TP-03.02
- 标题: 接入 local-ci artifact
- 验收项:
  - [x] 达成 `接入 local-ci artifact` 的 objective，且输出物可复核
- Verify: bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0152-core-quality-template
- Gate: local-ci summary 可发现模板 artifact，certification 仍 blocked。
- 输出物:
  - [x] scripts/local-ci.sh
- 标准清单:
  - [x] Verify: bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0152-core-quality-template
  - [x] Gate: local-ci summary 可发现模板 artifact，certification 仍 blocked。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-04
- 标题: 文档和路线图同步
- 验收项:
  - [x] 达成 `文档和路线图同步` 的 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: implementation_and_tests
- 输出物:
  - [x] 刷新 100% 基础设施实现计划、AGENTS 目录说明和 0152 任务文档。
- 标准清单:
  - [x] Verify: 确认子节点范围、依赖与状态闭环
  - [x] Gate: 前置步骤已完成: implementation_and_tests
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-04.01
- 标题: 刷新 100% 路线图
- 验收项:
  - [x] 达成 `刷新 100% 路线图` 的 objective，且输出物可复核
- Verify: rg -n "6\.42|0152|core_quality_human_review_bundle|template-only|Post-0151" docs/reference-materials/roadmap/测算基础设施100%实现计划.md
- Gate: 路线图区分本地模板演练与真实人审/benchmark/no-leak accepted evidence。
- 输出物:
  - [x] docs/reference-materials/roadmap/测算基础设施100%实现计划.md
- 标准清单:
  - [x] Verify: rg -n "6\.42|0152|core_quality_human_review_bundle|template-only|Post-0151" docs/reference-materials/roadmap/测算基础设施100%实现计划.md
  - [x] Gate: 路线图区分本地模板演练与真实人审/benchmark/no-leak accepted evidence。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-04.02
- 标题: 同步 AGENTS 与任务文档
- 验收项:
  - [x] 达成 `同步 AGENTS 与任务文档` 的 objective，且输出物可复核
- Verify: python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0152-measurement-infrastructure-core-quality-evidence-bundle-rehearsal --phase decompose
- Gate: 任务文档无占位符，AGENTS 说明新模板职责。
- 输出物:
  - [x] governance/tasks/0152-measurement-infrastructure-core-quality-evidence-bundle-rehearsal/*
  - [x] contracts/fate/evaluations/AGENTS.md
  - [x] scripts/AGENTS.md
  - [x] tests/AGENTS.md
- 标准清单:
  - [x] Verify: python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0152-measurement-infrastructure-core-quality-evidence-bundle-rehearsal --phase decompose
  - [x] Gate: 任务文档无占位符，AGENTS 说明新模板职责。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-05
- 标题: 验证、审查与版本控制
- 验收项:
  - [x] 达成 `验证、审查与版本控制` 的 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: docs_and_roadmap
- 输出物:
  - [x] 执行 targeted tests、lint、local-ci、diff check、提交推送并观察远端 CI。
- 标准清单:
  - [x] Verify: 确认子节点范围、依赖与状态闭环
  - [x] Gate: 前置步骤已完成: docs_and_roadmap
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-05.01
- 标题: 执行本地验证
- 验收项:
  - [x] 达成 `执行本地验证` 的 objective，且输出物可复核
- Verify: python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0152-measurement-infrastructure-core-quality-evidence-bundle-rehearsal --phase decompose && .venv/bin/python -m pytest tests/regression/test_core_quality_human_review_bundle_template.py tests/regression/test_core_quality_human_review_gate.py && .venv/bin/ruff check scripts/core-quality-human-review-bundle-template.py tests/regression/test_core_quality_human_review_bundle_template.py && .venv/bin/ruff format --check scripts/core-quality-human-review-bundle-template.py tests/regression/test_core_quality_human_review_bundle_template.py && bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0152-core-quality-template && git diff --check
- Gate: 所有本地验证通过，或失败原因写入 STATUS。
- 输出物:
  - [x] STATUS.md validation evidence
- 标准清单:
  - [x] Verify: python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0152-measurement-infrastructure-core-quality-evidence-bundle-rehearsal --phase decompose && .venv/bin/python -m pytest tests/regression/test_core_quality_human_review_bundle_template.py tests/regression/test_core_quality_human_review_gate.py && .venv/bin/ruff check scripts/core-quality-human-review-bundle-template.py tests/regression/test_core_quality_human_review_bundle_template.py && .venv/bin/ruff format --check scripts/core-quality-human-review-bundle-template.py tests/regression/test_core_quality_human_review_bundle_template.py && bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0152-core-quality-template && git diff --check
  - [x] Gate: 所有本地验证通过，或失败原因写入 STATUS。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

### TP-05.02
- 标题: 提交推送并观察远端 Acceptance
- 验收项:
  - [x] 达成 `提交推送并观察远端 Acceptance` 的 objective，且输出物可复核
- Verify: git status --short --branch && git log -1 --oneline --decorate && gh run list --workflow Acceptance --limit 5
- Gate: 提交推送完成，远端 Acceptance 对当前 commit 成功或明确记录 pending/failure。
- 输出物:
  - [x] Git commit and remote Acceptance evidence
- 标准清单:
  - [x] Verify: git status --short --branch && git log -1 --oneline --decorate && gh run list --workflow Acceptance --limit 5
  - [x] Gate: 提交推送完成，远端 Acceptance 对当前 commit 成功或明确记录 pending/failure。
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检
