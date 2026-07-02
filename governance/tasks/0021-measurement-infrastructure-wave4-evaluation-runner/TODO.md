# Execution Checklist
[x] TP-01.01 | P0 | 盘点 registry、golden、benchmark 和现有评测脚本 | Verify: `rg -n "EvaluationRun|run\\.solar_terms|run\\.local_ci|run-mingli|test_solar_terms_golden|golden/eval" contracts docs scripts tests governance/tasks/0021-measurement-infrastructure-wave4-evaluation-runner` | Gate: required / optional / requires_reference_repo 边界明确 | Parallelizable: No
[x] TP-01.02 | P0 | 回填任务契约与文档字段 | Verify: `validate_task_docs.py --phase decompose` | Gate: 任务文档无占位符且任务树可解析 | Parallelizable: No
[x] TP-02.01 | P0 | 新增 Python runner 与 bash wrapper | Verify: `bash scripts/run-evaluations.sh --list` | Gate: runner 可读取 registry 并列出 EvaluationRun | Parallelizable: No
[x] TP-02.02 | P0 | 实现选择器、命令白名单、dry-run 和 summary JSON | Verify: `bash scripts/run-evaluations.sh --dry-run --run-id run.solar_terms_golden --output-json /tmp/fatecat-evaluation-dry-run.json` | Gate: dry-run 不执行命令且 summary JSON 结构有效 | Parallelizable: No
[x] TP-02.03 | P0 | 在 registry/schema/AGENTS 中登记 runner 边界 | Verify: `python3 -m json.tool contracts/fate/evaluations/registry.json >/dev/null && python3 -m json.tool contracts/fate/evaluations/schemas/evaluation-run.schema.json >/dev/null` | Gate: schema/registry/AGENTS 记录 runner、summary fields 和安全边界 | Parallelizable: No
[x] TP-03.01 | P0 | 新增 runner 单元和契约测试 | Verify: `.venv/bin/python -m pytest -q tests/regression/test_evaluation_runner.py` | Gate: 默认选择、dry-run、skip reference repo、命令拒绝和 list 均被覆盖 | Parallelizable: No
[x] TP-03.02 | P0 | 更新 capability/API contract tests | Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py -k evaluation` | Gate: registry metadata、schema runner fields 和 API payload 一致 | Parallelizable: No
[x] TP-03.03 | P0 | 把 runner 测试纳入 quick CI focused tests | Verify: `rg -n "test_evaluation_runner.py" scripts/local-ci.sh` | Gate: quick CI focused regression tests 覆盖 runner | Parallelizable: No
[x] TP-04.01 | P0 | 更新 API 接入文档 | Verify: `rg -n "run-evaluations|all-local-required|shell=True|requires_reference_repo" docs/reference-materials/operations/测算基础设施\\ API\\ 接入.md` | Gate: 文档明确 API 不执行评测，runner 负责本地执行 | Parallelizable: No
[x] TP-04.02 | P0 | 更新 100% 基础设施路线图 checklist | Verify: `rg -n "本地 EvaluationRun runner|golden/eval 能跑本地最小集|扩展集" docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | Gate: checklist 区分已完成本地最小集和未完成扩展集 | Parallelizable: No
[x] TP-05.01 | P0 | 执行 runner dry-run、focused tests、实际 solar_terms run 和 quick CI | Verify: `bash scripts/run-evaluations.sh --run-id run.solar_terms_golden --output-json /tmp/fatecat-evaluation-solar-terms.json && bash scripts/local-ci.sh --profile quick && git diff --check` | Gate: runner 实跑、quick CI 和 diff check 通过 | Parallelizable: No
[x] TP-05.02 | P0 | 回填 closeout 状态和验证证据 | Verify: `validate_task_docs.py --phase closeout && validate_tasks_tree.py --phase auto` | Gate: 0021 closeout 和全任务树校验通过 | Parallelizable: No

说明：
- 每一行必须绑定 `TP-XX(.YY...)`。
- 不允许出现无归属 TODO。
