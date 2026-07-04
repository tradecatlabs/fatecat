# Task-Level Acceptance
- 生成的模板契约明确 template-only、operator-action-required 和 non-claim 边界。
- 模板包含 artifact hash 计算说明、rubric dimension checklist、benchmark aggregate skeleton、no-leak checklist、gate 执行命令和禁止泄露字段。
- 测试证明模板不会被 core-quality-human-review-gate 接受。
- local-ci quick 生成模板 JSON/Markdown，但 core quality gate 仍保持 blocked-as-expected。
- 100% 路线图新增 Post-0151/0152 切片，下一步任务清楚区分本地可做与外部 operator 阻断。
- approved plan 已成功编译为递归任务树
- 叶子节点数量: 10
- 当前可立即执行叶子节点: TP-01.01, TP-01.02

# Validation Plan
- python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0152-measurement-infrastructure-core-quality-evidence-bundle-rehearsal --phase decompose
- .venv/bin/python -m pytest tests/regression/test_core_quality_human_review_bundle_template.py tests/regression/test_core_quality_human_review_gate.py
- bash scripts/core-quality-human-review-bundle-template.sh --output-json /tmp/fatecat-core-quality-template.json --output-markdown /tmp/fatecat-core-quality-template.md
- .venv/bin/ruff check scripts/core-quality-human-review-bundle-template.py tests/regression/test_core_quality_human_review_bundle_template.py
- .venv/bin/ruff format --check scripts/core-quality-human-review-bundle-template.py tests/regression/test_core_quality_human_review_bundle_template.py
- bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0152-core-quality-template
- git diff --check
- bugfix / regression / flaky 任务必须把 DEBUG.md 的回归证据串到 Recent Evidence
- TP-01.01 | Verify: git status --short --branch && git log -1 --oneline --decorate && rg -n "core-quality-human-review|professional-quality-rubric|external-evidence-submission-readiness" contracts scripts tests docs/reference-materials/roadmap/测算基础设施100%实现计划.md | Gate: 仓库事实来自命令输出，未脑补外部证据。
- TP-01.02 | Verify: rg -n "OpenAPI|AsyncAPI|CloudEvents|Kubernetes|OpenTelemetry|SRE|SLSA|CycloneDX|OWASP|NIST|Backstage|Temporal" docs/reference-materials/roadmap/测算基础设施100%实现计划.md governance/tasks/0152-measurement-infrastructure-core-quality-evidence-bundle-rehearsal | Gate: 调研使用一手资料 URL，且只映射要求，不宣称外部 live 完成。
- TP-02.01 | Verify: .venv/bin/python -m json.tool contracts/fate/evaluations/core-quality-human-review-bundle-template.json >/dev/null | Gate: 契约声明模板不能作为 accepted review bundle。
- TP-02.02 | Verify: bash scripts/core-quality-human-review-bundle-template.sh --output-json /tmp/fatecat-core-quality-template.json --output-markdown /tmp/fatecat-core-quality-template.md && .venv/bin/python -m json.tool /tmp/fatecat-core-quality-template.json >/dev/null | Gate: 输出中没有 raw URL、secret/token/DSN、专家身份、题目答案或完整报告正文。
- TP-03.01 | Verify: .venv/bin/python -m pytest tests/regression/test_core_quality_human_review_bundle_template.py tests/regression/test_core_quality_human_review_gate.py | Gate: 模板不会被 core-quality-human-review-gate 接受。
- TP-03.02 | Verify: bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0152-core-quality-template | Gate: local-ci summary 可发现模板 artifact，certification 仍 blocked。
- TP-04.01 | Verify: rg -n "6\.42|0152|core_quality_human_review_bundle|template-only|Post-0151" docs/reference-materials/roadmap/测算基础设施100%实现计划.md | Gate: 路线图区分本地模板演练与真实人审/benchmark/no-leak accepted evidence。
- TP-04.02 | Verify: python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0152-measurement-infrastructure-core-quality-evidence-bundle-rehearsal --phase decompose | Gate: 任务文档无占位符，AGENTS 说明新模板职责。
- TP-05.01 | Verify: python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0152-measurement-infrastructure-core-quality-evidence-bundle-rehearsal --phase decompose && .venv/bin/python -m pytest tests/regression/test_core_quality_human_review_bundle_template.py tests/regression/test_core_quality_human_review_gate.py && .venv/bin/ruff check scripts/core-quality-human-review-bundle-template.py tests/regression/test_core_quality_human_review_bundle_template.py && .venv/bin/ruff format --check scripts/core-quality-human-review-bundle-template.py tests/regression/test_core_quality_human_review_bundle_template.py && bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0152-core-quality-template && git diff --check | Gate: 所有本地验证通过，或失败原因写入 STATUS。
- TP-05.02 | Verify: git status --short --branch && git log -1 --oneline --decorate && gh run list --workflow Acceptance --limit 5 | Gate: 提交推送完成，远端 Acceptance 对当前 commit 成功或明确记录 pending/failure。

# Review Gate
- Future-optimal: 本轮切片必须通向 100% 基础设施证据闭环，不形成孤立文档。
- Ponytail: 新模板对象必须降低人工提交错误率，并由测试证明不能被当成真实证据。
- Document drift: README/SKILL/API docs/roadmap/AGENTS 中与 100% 状态相关口径不能冲突。

# Runtime Verification Gate
- [ ] 每个 tool/action 结果都有可回指证据或明确未执行原因。
- [ ] 高风险动作没有由 worker/agent 自我批准；审批状态可追踪。
- [ ] compaction / resume 后目标、计划、修改文件、审批状态和验证项未丢失。
- [ ] verifier / 自审已检查关键发现是否有证据支持。
- [ ] closeout 明确 coverage gaps、failed packets 和 unresolved questions。
- [ ] TP-01.01: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [ ] TP-01.02: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [ ] TP-02.01: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [ ] TP-02.02: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [ ] TP-03.01: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [ ] TP-03.02: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [ ] TP-04.01: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [ ] TP-04.02: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [ ] TP-05.01: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [ ] TP-05.02: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据

# Ship Readiness
- 所有本地验证通过。
- core quality gate 对模板仍 blocked-as-expected。
- 路线图明确 0152 不代表专家评审/benchmark/no-leak 完成。
- 提交推送后等待远端 Acceptance。

# Task Package Acceptance
## TP-01
- 标题: 资料与仓库事实对齐
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 任务目标与上下文已确认
- 输出物: 无

### TP-01.01
- 标题: 盘点当前仓库证据链
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: git status --short --branch && git log -1 --oneline --decorate && rg -n "core-quality-human-review|professional-quality-rubric|external-evidence-submission-readiness" contracts scripts tests docs/reference-materials/roadmap/测算基础设施100%实现计划.md
- Gate: 仓库事实来自命令输出，未脑补外部证据。
- 输出物: 0152 CONTEXT/STATUS 事实基线。

### TP-01.02
- 标题: 基础设施同构资料映射
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: rg -n "OpenAPI|AsyncAPI|CloudEvents|Kubernetes|OpenTelemetry|SRE|SLSA|CycloneDX|OWASP|NIST|Backstage|Temporal" docs/reference-materials/roadmap/测算基础设施100%实现计划.md governance/tasks/0152-measurement-infrastructure-core-quality-evidence-bundle-rehearsal
- Gate: 调研使用一手资料 URL，且只映射要求，不宣称外部 live 完成。
- 输出物: 路线图 Post-0151 同构矩阵。

## TP-02
- 标题: Core quality bundle 模板契约设计
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: source_alignment
- 输出物: 无

### TP-02.01
- 标题: 新增模板契约
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: .venv/bin/python -m json.tool contracts/fate/evaluations/core-quality-human-review-bundle-template.json >/dev/null
- Gate: 契约声明模板不能作为 accepted review bundle。
- 输出物: contracts/fate/evaluations/core-quality-human-review-bundle-template.json

### TP-02.02
- 标题: 设计模板生成器输出
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: bash scripts/core-quality-human-review-bundle-template.sh --output-json /tmp/fatecat-core-quality-template.json --output-markdown /tmp/fatecat-core-quality-template.md && .venv/bin/python -m json.tool /tmp/fatecat-core-quality-template.json >/dev/null
- Gate: 输出中没有 raw URL、secret/token/DSN、专家身份、题目答案或完整报告正文。
- 输出物: scripts/core-quality-human-review-bundle-template.py；scripts/core-quality-human-review-bundle-template.sh

## TP-03
- 标题: 实现、测试与 local-ci 接线
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: template_contract_design
- 输出物: 无

### TP-03.01
- 标题: 新增回归测试
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: .venv/bin/python -m pytest tests/regression/test_core_quality_human_review_bundle_template.py tests/regression/test_core_quality_human_review_gate.py
- Gate: 模板不会被 core-quality-human-review-gate 接受。
- 输出物: tests/regression/test_core_quality_human_review_bundle_template.py

### TP-03.02
- 标题: 接入 local-ci artifact
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0152-core-quality-template
- Gate: local-ci summary 可发现模板 artifact，certification 仍 blocked。
- 输出物: scripts/local-ci.sh

## TP-04
- 标题: 文档和路线图同步
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: implementation_and_tests
- 输出物: 无

### TP-04.01
- 标题: 刷新 100% 路线图
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: rg -n "6\.42|0152|core_quality_human_review_bundle|template-only|Post-0151" docs/reference-materials/roadmap/测算基础设施100%实现计划.md
- Gate: 路线图区分本地模板演练与真实人审/benchmark/no-leak accepted evidence。
- 输出物: docs/reference-materials/roadmap/测算基础设施100%实现计划.md

### TP-04.02
- 标题: 同步 AGENTS 与任务文档
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0152-measurement-infrastructure-core-quality-evidence-bundle-rehearsal --phase decompose
- Gate: 任务文档无占位符，AGENTS 说明新模板职责。
- 输出物: governance/tasks/0152-measurement-infrastructure-core-quality-evidence-bundle-rehearsal/*；contracts/fate/evaluations/AGENTS.md；scripts/AGENTS.md；tests/AGENTS.md

## TP-05
- 标题: 验证、审查与版本控制
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 前置步骤已完成: docs_and_roadmap
- 输出物: 无

### TP-05.01
- 标题: 执行本地验证
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0152-measurement-infrastructure-core-quality-evidence-bundle-rehearsal --phase decompose && .venv/bin/python -m pytest tests/regression/test_core_quality_human_review_bundle_template.py tests/regression/test_core_quality_human_review_gate.py && .venv/bin/ruff check scripts/core-quality-human-review-bundle-template.py tests/regression/test_core_quality_human_review_bundle_template.py && .venv/bin/ruff format --check scripts/core-quality-human-review-bundle-template.py tests/regression/test_core_quality_human_review_bundle_template.py && bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0152-core-quality-template && git diff --check
- Gate: 所有本地验证通过，或失败原因写入 STATUS。
- 输出物: STATUS.md validation evidence

### TP-05.02
- 标题: 提交推送并观察远端 Acceptance
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: git status --short --branch && git log -1 --oneline --decorate && gh run list --workflow Acceptance --limit 5
- Gate: 提交推送完成，远端 Acceptance 对当前 commit 成功或明确记录 pending/failure。
- 输出物: Git commit and remote Acceptance evidence

# Anti-Goals
- 不得修改 `governance/tasks/` 以外路径
- 不得虚构证据
- 不得越权补全未确认信息
