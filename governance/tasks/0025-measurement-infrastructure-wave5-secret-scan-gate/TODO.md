# Execution Checklist
[x] TP-01.01 | P0 | 盘点 SecurityControl、source hygiene、release gate 和 secret scanner 缺口 | Verify: `rg -n "secret scanner|secret scan|source hygiene|public release|token|DSN|webhook" docs contracts scripts tests governance/tasks/0019-measurement-infrastructure-wave5-security-privacy-resources` | Gate: scanner 与 source hygiene/release gate 边界明确 | Parallelizable: No
[x] TP-01.02 | P0 | 回填任务契约与任务树 | Verify: `validate_task_docs.py --phase decompose` | Gate: 任务文档无占位符且任务树可解析 | Parallelizable: No
[x] TP-02.01 | P0 | 新增 secret-scan 脚本与脱敏 summary | Verify: `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan.json` | Gate: 当前 worktree findingCount=0，输出不含疑似密钥原文 | Parallelizable: No
[x] TP-02.02 | P0 | 新增 allowlist 并处理占位符/函数调用误报 | Verify: `python3 -m json.tool contracts/fate/security/secret-scan-allowlist.json >/dev/null` | Gate: allowlist 不包含真实 secret，只记录占位符、示例片段和排除边界 | Parallelizable: No
[x] TP-03.01 | P0 | 登记 SecurityControl 和 schema controlType | Verify: `python3 -m json.tool contracts/fate/security/registry.json >/dev/null && rg -n "control.secret_scan_gate|secret_scan|secretScanCommand" contracts/fate/security` | Gate: registry/schema/API 均可发现 secret scan gate | Parallelizable: No
[x] TP-03.02 | P0 | 新增 scanner 回归测试并接入 quick CI | Verify: `.venv/bin/python -m pytest -q tests/regression/test_secret_scan.py tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py -k 'secret or security' && rg -n "test_secret_scan.py|secret scan" scripts/local-ci.sh` | Gate: scanner 命中、占位符忽略、CLI summary、API/contract tests 全覆盖 | Parallelizable: No
[x] TP-03.03 | P0 | 更新 AGENTS、API 文档和 100% 路线图 | Verify: `rg -n "secret-scan|secret scan|secret scanner|secretScanCommand" scripts/AGENTS.md contracts/fate/security/AGENTS.md docs/reference-materials` | Gate: 文档区分本地 scanner 与未完成生产安全能力 | Parallelizable: No
[x] TP-04.01 | P0 | 执行 scanner、focused tests、ruff/format、quick CI 和 diff check | Verify: `bash scripts/local-ci.sh --profile quick && git diff --check` | Gate: quick CI 和 diff check 通过 | Parallelizable: No
[x] TP-04.02 | P0 | 回填 closeout 状态、全任务树验证和 closeout packet | Verify: `validate_task_docs.py --phase closeout && validate_tasks_tree.py --phase auto` | Gate: 0025 closeout 和全任务树校验通过 | Parallelizable: No

说明：
- 每一行必须绑定 `TP-XX(.YY...)`。
- 不允许出现无归属 TODO。
