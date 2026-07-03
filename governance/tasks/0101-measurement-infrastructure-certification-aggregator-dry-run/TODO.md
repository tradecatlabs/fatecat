# Execution Checklist
[x] TP-01.01 | P0 | 盘点 local-ci 现有 gate evidence 与不可声明边界 | Verify: rg -n "current audit bundle|live release gate|provider drift trend" scripts/local-ci.sh | Gate: 必备 evidence 来源和 non-claim 边界明确 | Parallelizable: Yes
[x] TP-01.02 | P0 | 定义 certification contract、必备证据和分域状态 | Verify: cat contracts/fate/audit/measurement-infrastructure-certification.json | Gate: contract 列出 required evidence、forbidden fragments、privacy/release boundary | Parallelizable: Yes
[x] TP-02.01 | P0 | 实现 CLI/wrapper、分域聚合、blocked/pending/failed 语义 | Verify: bash scripts/measurement-infrastructure-certification.sh --evidence-dir /tmp/fatecat-local-ci-0100-final --output-json /tmp/fatecat-certification-0101.json | Gate: blocked dry-run 输出 canClaim100Percent=false | Parallelizable: No
[x] TP-02.02 | P0 | 接入 local-ci summary、AGENTS、API 文档和 roadmap | Verify: rg -n "measurement-infrastructure-certification|certification aggregator" scripts/local-ci.sh scripts/AGENTS.md contracts/fate/audit/AGENTS.md tests/AGENTS.md | Gate: quick local-ci 生成 certification artifact 路径 | Parallelizable: Yes
[x] TP-03.01 | P0 | 增加 regression tests | Verify: .venv/bin/python -m pytest -q tests/regression/test_measurement_infrastructure_certification.py | Gate: blocked、missing、require-certified、synthetic passed 覆盖 | Parallelizable: Yes
[x] TP-03.02 | P0 | 执行 gate smoke、focused tests、ruff、quick local-ci 和 secret scan | Verify: bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0101-final | Gate: 本地 quick CI 和 secret scan 通过 | Parallelizable: No
[x] TP-04.01 | P0 | 同步任务文档、INDEX 和验收清单 | Verify: python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0101-measurement-infrastructure-certification-aggregator-dry-run --phase closeout | Gate: task docs closeout validator passed | Parallelizable: No
[x] TP-04.02 | P0 | 提交、推送并记录远端状态 | Verify: git status --short --branch && git ls-remote origin refs/heads/main | Gate: 本地 HEAD 与 origin/main 匹配或明确说明远端状态 | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
