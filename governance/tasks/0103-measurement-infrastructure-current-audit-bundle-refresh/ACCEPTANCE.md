# Task-Level Acceptance
- current audit bundle 能通过 `--local-ci-output-dir` 读取 local-ci gate artifact。
- evidence index 必须包含 `evidence.evidence_coverage_trend_gate`。
- 缺失或失败的 required gate artifact 必须让该 evidence item fail。
- bundle 输出不得包含真实 token、secret、DSN、私钥、报告正文、真实生产日志正文或真实用户 payload。
- local-ci current audit bundle 调用必须传入自身 output dir。

# Validation Plan
| Scope | Command | Expected |
| --- | --- | --- |
| Focused tests | `.venv/bin/python -m pytest -q tests/regression/test_current_audit_bundle.py tests/regression/test_evidence_coverage_trend_gate.py` | Regression passed。 |
| Bundle generation | `bash scripts/current-audit-bundle.sh --output-dir /tmp/fatecat-current-audit-bundle-0103 ... --local-ci-output-dir <dir>` | `evidence-index.json` 包含 evidence coverage trend gate。 |
| Lint/format | `.venv/bin/ruff check scripts/current-audit-bundle.py tests/regression/test_current_audit_bundle.py && .venv/bin/ruff format --check scripts/current-audit-bundle.py tests/regression/test_current_audit_bundle.py` | Ruff passed。 |
| Secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0103-final.json` | findingCount=0。 |
| Task docs | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0103-measurement-infrastructure-current-audit-bundle-refresh --phase closeout` | ok=true。 |

# Review Gate
- 检查 current audit bundle 没有把 local-ci artifact 写成外部 live。
- 检查 evidence item 只保存摘要计数、路径和 digest。
- 检查 local-ci 调用、contract、AGENTS 和 tests 口径一致。

# Runtime Verification Gate
- 本任务本地验证必须覆盖 current bundle 生成、evidence index 展开和 required mode 原有语义。
- 真实外部 live 不在本任务执行；所有真实生产系统均为外部连通验证待执行。

# Task Package Acceptance
## TP-01 current audit bundle 需求和证据边界
Acceptance: A4 被限定为审计包刷新，不替代外部 live 或第三方审计。

### TP-01.01 盘点当前 bundle 输入和 0102 evidence artifact 缺口
Verify: `rg -n "current-audit-bundle|evidenceCoverageTrendGate" scripts tests contracts docs`

Gate: current bundle 现有输入和 evidence coverage artifact 缺口明确。

### TP-01.02 定义 local-ci gate artifact 纳入策略和 non-claim
Verify: `cat contracts/fate/audit/current-bundle.json`

Gate: contract 登记 local-ci gate artifact evidence source，non-claims 不回退。

## TP-02 current audit bundle 刷新实现与接线
Acceptance: current bundle 能把 local-ci gate artifact 展开到 evidence index。

### TP-02.01 实现 local-ci output dir artifact evidence
Verify: `.venv/bin/python -m pytest -q tests/regression/test_current_audit_bundle.py`

Gate: evidence index 包含 `evidence.evidence_coverage_trend_gate`。

### TP-02.02 接入 local-ci、contract、AGENTS、tests 和 roadmap
Verify: `rg -n "local-ci-output-dir|evidence.evidence_coverage_trend_gate|0103" scripts contracts tests docs governance/tasks`

Gate: local-ci 会把 output dir 传给 current audit bundle，文档口径同步。

## TP-03 验证与审查
Acceptance: 本地可执行验证覆盖生成和回归。

### TP-03.01 增加/更新 regression tests
Verify: `.venv/bin/python -m pytest -q tests/regression/test_current_audit_bundle.py`

Gate: current bundle regression passed。

### TP-03.02 执行 focused tests、bundle generation、ruff、secret scan 和必要 local-ci
Verify: `bash scripts/current-audit-bundle.sh --output-dir /tmp/fatecat-current-audit-bundle-0103 ...`

Gate: current bundle 生成成功，evidence index 包含 evidence coverage trend gate。

## TP-04 closeout 与版本控制
Acceptance: 文档、任务索引、版本控制和远端状态一致。

### TP-04.01 同步任务文档、INDEX 和验收清单
Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0103-measurement-infrastructure-current-audit-bundle-refresh --phase closeout`

Gate: closeout validator passed。

### TP-04.02 提交、推送并记录远端状态
Verify: `git status --short --branch && git ls-remote origin refs/heads/main`

Gate: 本地 HEAD 与 origin/main 匹配，或如实说明远端 CI 未覆盖当前 commit。

# Ship Readiness
- [x] closeout validator passed。
- [x] focused tests passed。
- [x] secret scan passed。
- [x] commit pushed to `origin/main`。
- [x] 远端 CI 对当前 commit 的状态如实记录；未观察到则不得写通过。

# Anti-Goals
- 不得只修改任务包而不落地 current audit bundle 接线。
- 不得虚构外部 live evidence。
- 不得把 blocked auditGate 写成第三方审计通过。
