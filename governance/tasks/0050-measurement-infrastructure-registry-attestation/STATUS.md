# Task Status

- Overall Status: `Done`

# Next Executable Leaves

None. 0050 已完成；下一步按主路线图进入 `MI-NEXT-03` durable runtime 二期。

# Task Package Status Table

| Node ID | Parent | Depth | Depends On | Ready | Status | Recent Evidence | Blocker | Unblock Needed |
| --- | --- | ---: | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | - | No | Done | workflow 与官方 action 用法已复核。 | 无 | 无 |
| TP-01.01 | TP-01 | 2 | - | No | Done | `actions/attest@v4.1.1` latest；README 确认 container image 参数和权限。 | 无 | 无 |
| TP-02 | ROOT | 1 | TP-01.01 | No | Done | `.github/workflows/container.yml` 已增加 digest、release artifacts upload、attestation 和 verify。 | 无 | 无 |
| TP-02.01 | TP-02 | 2 | TP-01.01 | No | Done | workflow YAML 解析通过；新增 workflow regression 通过。 | 无 | 无 |
| TP-03 | ROOT | 1 | TP-02.01 | No | Done | 门禁、contract、AGENTS、操作文档和 roadmap 已同步。 | 无 | 无 |
| TP-03.01 | TP-03 | 2 | TP-02.01 | No | Done | `test_container_workflow_attestation.py` 与 `check-public-release-policy.sh` 覆盖关键断言。 | 无 | 无 |
| TP-03.02 | TP-03 | 2 | TP-02.01 | No | Done | release gate、delivery registry、AGENTS、操作文档和 roadmap 已同步。 | 无 | 无 |
| TP-04 | ROOT | 1 | TP-03.01, TP-03.02 | No | Done | 本地 quick CI 通过；远端 run `28580109478` 对 `5b301db` 成功，digest/attestation/verify 均通过。 | 无 | 无 |
| TP-04.01 | TP-04 | 2 | TP-03.01, TP-03.02 | No | Done | `https://github.com/tradecatlabs/fatecat/actions/runs/28580109478` success；digest `sha256:2544ae3c30ce66141652199dbf065cd168ec2618c7b51bb6afc922172d9a0756`；attestation `33588466`。 | 无 | 无 |

# Blockers

当前无本地 blocker。远端 workflow 可能因 GitHub runner `gh attestation`、permissions 或 GHCR 权限失败，失败后进入 debug。

# Runtime State

- 当前任务：0050
- 当前阶段：Done
- 生产副作用：尚未发生；远端 `push_image=true` 才会发布 GHCR image

# Remaining Risks

- 0048 Telegram Bot live smoke 仍缺真实 `FATE_BOT_TOKEN`。
- 本地 `gh` 不支持 attestation 子命令；远端 verify 必须用 GitHub-hosted runner 证明。

# Current Evidence

| Item | Evidence |
| --- | --- |
| Workflow attestation regression | `.venv/bin/python -m pytest -q tests/regression/test_container_workflow_attestation.py` passed |
| Public release policy | `bash scripts/check-public-release-policy.sh` passed |
| Workflow YAML syntax | `yaml.safe_load(.github/workflows/container.yml)` passed |
| Targeted release regression | `.venv/bin/python -m pytest -q tests/regression/test_live_release_gate.py tests/regression/test_container_release_evidence.py tests/regression/test_operability_docs.py tests/regression/test_container_workflow_attestation.py` passed |
| Task docs validation | `validate_task_docs.py --phase decompose` passed |
| Task tree validation | `validate_tasks_tree.py --phase auto` passed |
| Local quick CI | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0050-rerun` passed; focused regression `132 passed in 76.62s` |
| Remote workflow first attempt | `https://github.com/tradecatlabs/fatecat/actions/runs/28579776942` failed at `Push main image`; root cause and fix recorded in `DEBUG.md` |
| Digest parser fix regression | `.venv/bin/python -m pytest -q tests/regression/test_container_workflow_attestation.py` passed |
| Digest parser fix policy | `bash scripts/check-public-release-policy.sh` passed |
| Digest parser fix YAML | `yaml.safe_load(.github/workflows/container.yml)` passed |
| Remote workflow success | `https://github.com/tradecatlabs/fatecat/actions/runs/28580109478` success for `5b301dbbd56d64709b1996641787647f6309e048` |
| GHCR digest | `ghcr.io/tradecatlabs/fatecat-delivery@sha256:2544ae3c30ce66141652199dbf065cd168ec2618c7b51bb6afc922172d9a0756` |
| GitHub attestation | `https://github.com/tradecatlabs/fatecat/attestations/33588466` |
| Release artifact upload | Artifact `fatecat-release-artifacts-5b301dbbd56d64709b1996641787647f6309e048`, id `8034643123` |
