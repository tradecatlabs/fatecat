# Acceptance Checklist

# Global Standards
- [x] Scope 明确，不混入外部监控平台、生产部署或 live smoke。
- [x] dashboard 隐私边界明确，不展示 stdout/stderr tail、标准答案、报告正文或真实凭证。
- [x] EvaluationRun command 保持 runner 白名单约束。
- [x] quick CI hook 已接入，并在 nightly wrapper 中通过。
- [x] data supply chain manifest hash 已同步并通过 gate。
- [x] task closeout packet 生成。

# Task Package Checklists

## TP-01.01 现状审计
Verify: `sed -n '1,260p' scripts/run-evaluations.py && sed -n '1,260p' scripts/compare-evaluations.py`

Gate: D6 缺 dashboard/nightly 明确。

- [x] 已盘点 runner、history、diff、workflow、registry 和 roadmap。

## TP-02.01 dashboard renderer
Verify: `test -f scripts/evaluation-dashboard.py && test -f scripts/evaluation-dashboard.sh`

Gate: renderer 可从 summary/diff 生成 HTML。

- [x] 已新增 renderer 和 shell wrapper。

## TP-02.02 dashboard tests/smoke
Verify: `.venv/bin/python -m pytest -q tests/regression/test_evaluation_dashboard.py`

Gate: HTML escape、隐私边界和 CLI 输出通过。

- [x] dashboard 回归测试已通过。
- [x] `bash scripts/evaluation-dashboard-smoke.sh --output-dir /tmp/fatecat-evaluation-dashboard-smoke` 已通过。

## TP-03.01 nightly wrapper
Verify: `bash scripts/evaluation-nightly.sh --output-dir /tmp/fatecat-evaluation-nightly-2 --history-dir /tmp/fatecat-evaluation-history-2 --timeout-seconds 900`

Gate: 3 个本地 releaseRequired run 全部 passed。

- [x] nightly wrapper 第二轮通过，3/3 passed。
- [x] 第一轮发现 data supply chain hash 漂移并已修复。

## TP-03.02 GitHub scheduled workflow
Verify: `test -f .github/workflows/evaluation-nightly.yml`

Gate: workflow 只调用仓库脚本并上传 artifact。

- [x] `.github/workflows/evaluation-nightly.yml` 已新增。

## TP-04.01 registry metadata
Verify: `.venv/bin/python -m pytest -q tests/regression/test_evaluation_runner.py tests/regression/test_capability_protocol.py`

Gate: registry/API/protocol 可发现。

- [x] `run.evaluation_dashboard_smoke` 已登记。
- [x] `dashboardCommand` 和 `nightlyCommand` 已登记。

## TP-04.02 quick CI/docs
Verify: `jq '.summary' /tmp/fatecat-evaluation-nightly-2/summary.json`

Gate: `run.local_ci_quick` passed。

- [x] quick CI hook 已在 nightly wrapper 中通过。
- [x] `.github`、`scripts`、`contracts/fate/evaluations` AGENTS 已同步。
- [x] API 接入文档和 100% roadmap 已同步。

## TP-05.01 validation
Verify: focused validation commands in `ACCEPTANCE.md`

Gate: shell/json/ruff/format/pytest/gate/smoke/nightly 全部通过。

- [x] focused validation 已通过。

## TP-05.02 closeout
Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0036-measurement-infrastructure-eval-dashboard-nightly --phase closeout`

Gate: closeout packet 写入任务目录。

- [x] closeout validator 已通过，`TASK_CLOSEOUT_PACKET.json` 已生成。
