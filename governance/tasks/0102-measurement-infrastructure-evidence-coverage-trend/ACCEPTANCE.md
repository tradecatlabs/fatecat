# Task-Level Acceptance
- evidence coverage trend gate 能读取 tracked baseline、rule depth registry、classics rule index、CapabilityExecutor 输出和 API Report envelope。
- 规则引用断链时输出 `failed`，不得默默跳过。
- analysisEvidence、Report evidenceRefs、appliedRules、conflict explanation、counterEvidence 和 combinationStatements 低于 baseline 或缺字段时输出 `failed`。
- 输出不得包含真实 token、secret、DSN、私钥、报告正文、出生地区或真实用户 payload。
- local-ci summary 必须包含 `evidenceCoverageTrendGate` artifact 路径。

# Validation Plan
| Scope | Command | Expected |
| --- | --- | --- |
| Gate smoke | `bash scripts/evidence-coverage-trend-gate.sh --output-json /tmp/fatecat-evidence-coverage-trend-0102-rerun.json` | 当前 baseline passed，summary 不保存报告正文。 |
| Focused tests | `.venv/bin/python -m pytest -q tests/regression/test_evidence_coverage_trend_gate.py tests/regression/test_bazi_ziwei_l4_golden_smoke.py tests/regression/test_bazi_ziwei_rule_depth.py` | Regression passed。 |
| Lint/format | `.venv/bin/ruff check scripts/evidence-coverage-trend-gate.py tests/regression/test_evidence_coverage_trend_gate.py && .venv/bin/ruff format --check scripts/evidence-coverage-trend-gate.py tests/regression/test_evidence_coverage_trend_gate.py` | Ruff passed。 |
| Quick CI | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0102-final` | 本地 quick CI passed，并生成 evidence coverage artifact。 |
| Secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0102-final.json` | findingCount=0。 |
| Task docs | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0102-measurement-infrastructure-evidence-coverage-trend --phase closeout` | ok=true。 |

# Review Gate
- 检查 baseline 不低于当前八字/紫微真实输出。
- 检查 Report evidenceRefs completeRatio 被纳入 baseline fail 条件。
- 检查 forbidden fragments 防护和 secret scan。
- 检查 local-ci summary artifact 是否包含 evidence coverage output。

# Runtime Verification Gate
- 本任务本地验证必须至少覆盖当前 baseline pass、严格 baseline fail、规则引用断链 fail 和 CLI summary 写出。
- 真实外部 live 不在本任务执行；所有真实生产系统均为外部连通验证待执行。

# Ship Readiness
- [x] closeout validator passed。
- [x] quick local-ci passed。
- [x] secret scan passed。
- [x] commit pushed to `origin/main`。
- [x] 远端 CI 对当前 commit 的状态如实记录；未观察到则不得写通过。

# Task Package Acceptance
## TP-01 evidence coverage 需求和 baseline 边界
Acceptance: evidence coverage trend 的语义被限定为本地结构化证据覆盖门禁，不替代外部 live 或专家审稿。

### TP-01.01 盘点八字/紫微现有 evidence surface
Verify: `rg -n "baziRuleDepth|ziweiRuleDepth|evidenceRefs|classics_rule_index" domains contracts scripts tests`

Gate: rule depth、classics index、analysisEvidence 和 Report evidenceRefs 的来源明确。

### TP-01.02 定义 tracked baseline、contract 和隐私边界
Verify: `cat contracts/fate/evidence-coverage-baseline.json contracts/fate/evidence-coverage-trend-contract.json`

Gate: baseline 与 contract 包含 required checks、forbidden fragments、privacy boundary 和 production boundary。

## TP-02 evidence coverage gate 实现与接线
Acceptance: gate 以只读方式消费 registry 和脱敏测试样本，输出可复核 JSON。

### TP-02.01 实现 CLI/wrapper、coverage metrics 和趋势比较
Verify: `bash scripts/evidence-coverage-trend-gate.sh --output-json /tmp/fatecat-evidence-coverage-trend-0102.json`

Gate: 当前 baseline 输出 `passed`，断链或回退输出 `failed`。

### TP-02.02 接入 local-ci summary、AGENTS、API 文档和 roadmap
Verify: `rg -n "evidence-coverage-trend|evidenceCoverageTrendGate" scripts/local-ci.sh scripts/AGENTS.md contracts/fate/AGENTS.md tests/AGENTS.md docs/reference-materials`

Gate: `scripts/local-ci.sh` 会生成 `evidence-coverage-trend-gate.json`，summary artifacts 可追踪。

## TP-03 验证与审查
Acceptance: 本地可执行验证覆盖主要状态转换和集成路径。

### TP-03.01 增加 regression tests
Verify: `.venv/bin/python -m pytest -q tests/regression/test_evidence_coverage_trend_gate.py`

Gate: pass、strict baseline fail、broken classics refs fail、CLI 输出均有覆盖。

### TP-03.02 执行 gate smoke、focused tests、ruff、quick local-ci 和 secret scan
Verify: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0102-final`

Gate: quick local-ci、secret scan、ruff 和 focused pytest 通过。

## TP-04 closeout 与版本控制
Acceptance: 文档、任务索引、版本控制和远端状态一致。

### TP-04.01 同步任务文档、INDEX 和验收清单
Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0102-measurement-infrastructure-evidence-coverage-trend --phase closeout`

Gate: closeout validator passed。

### TP-04.02 提交、推送并记录远端状态
Verify: `git status --short --branch && git ls-remote origin refs/heads/main`

Gate: 本地 HEAD 与 origin/main 匹配，或如实说明远端 CI 未覆盖当前 commit。

# Anti-Goals
- 不得只修改 `governance/tasks/` 而不落地 code gate。
- 不得虚构证据。
- 不得越权补全未确认信息。
- 不得把 evidence coverage passed 写成预测准确率、专业能力或外部 live passed。
