# Acceptance Checklist

# Global Standards
- [x] history 默认写入 `.gitignore` 覆盖的运行态目录。
- [x] diff 只比较 summary 状态和 exitCode，不解析用户输入、标准答案、token、secret、DSN 或生产日志。
- [x] `/evaluations` 仍是只读发现层，不启动本地 diff 或 runner。
- [x] 文档不宣称 dashboard、nightly、远端 CI 同步或外部 eval 已完成。

# Task Package Checklists

## TP-01.01 盘点 history/diff 缺口
- [x] Verify: `rg -n "EvaluationRun runner|summary history|diff policy|golden/eval|infra/runtime/local-state/exports" docs contracts scripts tests .gitignore governance/tasks/0022-measurement-infrastructure-wave4-evaluation-history-diff`
- [x] Gate: history/diff 与 dashboard/nightly 边界明确。

## TP-01.02 回填任务契约
- [x] Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0022-measurement-infrastructure-wave4-evaluation-history-diff --phase decompose`
- [x] Gate: 任务文档无占位符且任务树可解析。

## TP-02.01 扩展 runner history
- [x] Verify: `bash scripts/run-evaluations.sh --dry-run --run-id run.solar_terms_golden --record-history --history-dir /tmp/fatecat-evaluation-history --output-json /tmp/fatecat-evaluation-current.json`
- [x] Gate: history 文件和 latest.json 生成。

## TP-02.02 新增 diff 工具
- [x] Verify: `bash scripts/compare-evaluations.sh --baseline-json /tmp/fatecat-evaluation-history/latest.json --current-json /tmp/fatecat-evaluation-current.json --output-json /tmp/fatecat-evaluation-diff.json`
- [x] Gate: diff JSON 生成且 summary.status=passed。

## TP-02.03 新增 diff policy 和协议登记
- [x] Verify: `python3 -m json.tool contracts/fate/evaluations/diff-policy.json >/dev/null && rg -n "diff-policy|compare-evaluations" contracts/fate/evaluations scripts/AGENTS.md`
- [x] Gate: policy、registry 和 AGENTS 同步。

## TP-03.01 新增 history/diff 回归测试
- [x] Verify: `.venv/bin/python -m pytest -q tests/regression/test_evaluation_history_diff.py`
- [x] Gate: history/latest、diff pass/fail 和 CLI 输出均覆盖。

## TP-03.02 更新 contract/API tests 与 quick CI
- [x] Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py -k evaluation && rg -n "test_evaluation_history_diff.py" scripts/local-ci.sh`
- [x] Gate: diff policy metadata 和 quick CI 测试入口一致。

## TP-03.03 更新文档与路线图
- [x] Verify: `rg -n "record-history|compare-evaluations|diff-policy|summary history|golden/eval 具备本地 summary history" docs/reference-materials`
- [x] Gate: 文档区分已完成本地能力和未完成 dashboard/nightly。

## TP-04.01 修正任务 INDEX 状态漂移
- [x] Verify: `rg -n "0017|0018|0019|0020|0021|0022" governance/tasks/INDEX.md`
- [x] Gate: 0017-0021 与各自 STATUS closeout 一致，0022 为当前任务。

## TP-05.01 执行本地门禁
- [x] Verify: `bash scripts/local-ci.sh --profile quick && git diff --check`
- [x] Gate: quick CI 和 diff check 通过。

## TP-05.02 回填 closeout 状态和验证证据
- [x] Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0022-measurement-infrastructure-wave4-evaluation-history-diff --phase closeout && python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_tasks_tree.py --tasks-dir governance/tasks --phase auto --format markdown`
- [x] Gate: 0022 closeout 和全任务树校验通过。
