# Execution Checklist
[x] TP-01.01 | P0 | 盘点 provider metadata、schema、vendor manifest、roadmap 缺口 | Verify: `rg -n "ProviderMetadata|provider.schema|vendor_sources|MI-04|provider lifecycle" domains contracts tools docs scripts tests` | Gate: MI-04 缺口明确 | Parallelizable: No
[x] TP-02.01 | P0 | 扩展 `ProviderMetadata` / `UsecaseProvider` lifecycle 字段 | Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k provider` | Gate: runtime metadata 字段完整 | Parallelizable: No
[x] TP-02.02 | P0 | 补 Provider/resource schema lifecycle 契约 | Verify: `python3 -m json.tool contracts/fate/capabilities/schemas/provider.schema.json` | Gate: required fields 与 runtime metadata 对齐 | Parallelizable: No
[x] TP-02.03 | P0 | 将 `iztro` 登记为紫微 production dependency | Verify: `python3 -m json.tool tools/reference-repos/vendor_sources.json` | Gate: productionUseAllowed=true 且 licenseStatus=spdx | Parallelizable: No
[x] TP-03.01 | P0 | 新增 provider lifecycle gate 脚本 | Verify: `bash scripts/provider-lifecycle-gate.sh --output-json /tmp/fatecat-provider-lifecycle.json` | Gate: status passed, providerCount=4 | Parallelizable: No
[x] TP-03.02 | P0 | 新增 provider lifecycle 回归测试 | Verify: `.venv/bin/python -m pytest -q tests/regression/test_provider_lifecycle_gate.py tests/regression/test_capability_protocol.py -k 'provider or schema' tests/regression/test_api_contracts.py -k provider` | Gate: focused tests pass | Parallelizable: No
[x] TP-03.03 | P0 | 接入 quick local-ci 并运行 | Verify: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-provider-lifecycle` | Gate: quick CI passes | Parallelizable: No
[x] TP-04.01 | P1 | 更新 docs/AGENTS/roadmap | Verify: `rg -n "provider-lifecycle-gate|versionLock|MI-04.01|0032" docs/reference-materials scripts/AGENTS.md contracts/fate/capabilities/AGENTS.md domains/fate-analysis/services/fate-core/src/fate_core/capabilities/AGENTS.md` | Gate: 不夸大外部依赖 live 能力 | Parallelizable: No
[x] TP-04.02 | P0 | 生成任务 closeout packet | Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0032-measurement-infrastructure-provider-lifecycle-gates --phase closeout` | Gate: closeout packet 写入任务目录 | Parallelizable: No

说明：
- 每一行绑定 `TP-XX(.YY...)`。
- 不允许出现无归属 TODO。
