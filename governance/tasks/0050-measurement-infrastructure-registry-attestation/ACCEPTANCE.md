# Task-Level Acceptance

`MI-NEXT-02` 完成条件：container workflow 在 `push_image=true` 时能发布 GHCR image，输出 immutable digest，用 GitHub artifact attestation 绑定 digest，并运行 verify step；本地门禁和文档同步防止回退。

# Validation Plan

| Check | Command | Expected |
| --- | --- | --- |
| Workflow regression | `.venv/bin/python -m pytest -q tests/regression/test_container_workflow_attestation.py` | pass |
| Release policy | `bash scripts/check-public-release-policy.sh` | pass |
| Targeted release tests | `.venv/bin/python -m pytest -q tests/regression/test_live_release_gate.py tests/regression/test_container_release_evidence.py tests/regression/test_operability_docs.py` | pass |
| Task docs | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0050-measurement-infrastructure-registry-attestation --phase decompose` | pass |
| Task tree | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_tasks_tree.py --tasks-dir governance/tasks --phase auto` | pass |
| Remote workflow | `gh workflow run container.yml -f push_image=true` then `gh run watch` | success |

# Runtime Verification Gate

- 本地只证明 workflow 和门禁配置正确。
- 真实 registry digest/attestation 只能由远端 GitHub Actions run 证明。
- 如果远端 workflow 未执行，本任务不能宣称 registry attestation 生产闭环完成，只能宣称本地实现已准备好。

# Task Package Acceptance

- TP-01.01 Done：官方 action 和 workflow 缺口已复核。
- TP-02.01 Done：workflow 已增加 digest、artifact upload、attestation 和 verify。
- TP-03.01 Done：测试/策略门禁已修改并通过 targeted checks。
- TP-03.02 Done：文档/contract 已同步。
- TP-04.01 Done：本地验证通过；远端 Container workflow `28580109478` 对 `5b301db` 成功，main image digest 和 attestation verify 通过。

# Review Gate

- workflow 仍必须是 `workflow_dispatch` 手动触发，不能新增 push/pull_request 自动发布。
- `push_image=false` 必须只构建和 smoke，不推送 GHCR。
- `push_image=true` 的发布证据必须包含 immutable digest、attestation 和 verify。
- 未拿到远端 workflow success URL 前，不得宣称 registry attestation 生产闭环完成。

# Anti-Goals

- 不把 tag 当 digest。
- 不把本地 Docker imageId 当 registry digest。
- 不在仓库保存 registry token。
- 不声明 Telegram Bot live 完成。
- 不跳过远端 workflow 证据。

# Ship Readiness

- 本地测试通过。
- 任务包 closeout 通过。
- commit/push 完成。
- container workflow `push_image=true` 成功，失败首轮已形成 `DEBUG.md` 证据并修复。
