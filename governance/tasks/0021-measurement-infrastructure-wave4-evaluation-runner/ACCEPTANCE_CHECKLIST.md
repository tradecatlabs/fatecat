# Acceptance Checklist

# Global Standards
- [x] 无用户输入、报告正文、真实 token、secret、DSN、私钥、生产日志进入 registry、summary、docs 或 tests。
- [x] runner 不使用 `shell=True`，命令执行受白名单约束。
- [x] `/evaluations` 仍是只读发现层，不启动本地进程或外部评测。
- [x] optional / reference repo benchmark 不进入默认 release 必跑集合。
- [x] 文档只声明本地最小集 runner，不夸大 dashboard、nightly、跨 commit diff 或外部 eval。

# Task Package Checklists

## TP-01.01 盘点现有评测入口
- [x] Verify: `rg -n "EvaluationRun|run\\.solar_terms|run\\.local_ci|run-mingli|test_solar_terms_golden|golden/eval" contracts docs scripts tests governance/tasks/0021-measurement-infrastructure-wave4-evaluation-runner`
- [x] Gate: required / optional / requires_reference_repo 边界明确。

## TP-01.02 回填任务契约
- [x] Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0021-measurement-infrastructure-wave4-evaluation-runner --phase decompose`
- [x] Gate: 任务文档无占位符，任务树可解析。

## TP-02.01 新增 Python runner 与 bash wrapper
- [x] Verify: `bash scripts/run-evaluations.sh --list`
- [x] Gate: runner 可读取 registry 并列出 EvaluationRun。

## TP-02.02 实现选择器、命令白名单、dry-run 和 summary JSON
- [x] Verify: `bash scripts/run-evaluations.sh --dry-run --run-id run.solar_terms_golden --output-json /tmp/fatecat-evaluation-dry-run.json && python3 -m json.tool /tmp/fatecat-evaluation-dry-run.json >/dev/null`
- [x] Gate: dry-run 不执行命令，summary JSON 结构有效。

## TP-02.03 登记 runner 边界
- [x] Verify: `python3 -m json.tool contracts/fate/evaluations/registry.json >/dev/null && python3 -m json.tool contracts/fate/evaluations/schemas/evaluation-run.schema.json >/dev/null`
- [x] Gate: schema/registry/AGENTS 记录 runner、summary fields 和安全边界。

## TP-03.01 新增 runner 测试
- [x] Verify: `.venv/bin/python -m pytest -q tests/regression/test_evaluation_runner.py`
- [x] Gate: 默认选择、dry-run、skip reference repo、命令拒绝和 list 均被覆盖。

## TP-03.02 更新 contract/API 测试
- [x] Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py -k evaluation`
- [x] Gate: registry metadata、schema runner fields 和 API payload 一致。

## TP-03.03 接入 quick CI
- [x] Verify: `rg -n "test_evaluation_runner.py" scripts/local-ci.sh`
- [x] Gate: quick CI focused regression tests 覆盖 runner。

## TP-04.01 更新 API 接入文档
- [x] Verify: `rg -n "run-evaluations|all-local-required|shell=True|requires_reference_repo" docs/reference-materials/operations/测算基础设施\\ API\\ 接入.md`
- [x] Gate: 文档明确 API 不执行评测，runner 负责本地执行。

## TP-04.02 更新 100% 路线图
- [x] Verify: `rg -n "本地 EvaluationRun runner|golden/eval 能跑本地最小集|扩展集" docs/reference-materials/roadmap/测算基础设施100%实现计划.md`
- [x] Gate: checklist 区分已完成本地最小集和未完成扩展集。

## TP-05.01 执行本地门禁
- [x] Verify: `bash scripts/run-evaluations.sh --run-id run.solar_terms_golden --output-json /tmp/fatecat-evaluation-solar-terms.json && bash scripts/local-ci.sh --profile quick && git diff --check`
- [x] Gate: runner 实跑、quick CI 和 diff check 通过。

## TP-05.02 回填 closeout 状态和验证证据
- [x] Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0021-measurement-infrastructure-wave4-evaluation-runner --phase closeout && python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_tasks_tree.py --tasks-dir governance/tasks --phase auto --format markdown`
- [x] Gate: 0021 closeout 和全任务树校验通过。
