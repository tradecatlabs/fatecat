# Task Status

- Overall Status: `In Progress`

# Next Executable Leaves

- TP-05：任务 closeout、提交推送和远端 CI 证据。

# Task Package Status Table

| Node ID | Parent | Depth | Depends On | Ready | Status | Recent Evidence | Blocker | Unblock Needed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | - | No | Done | `report_jobs.py`、`webhook_callbacks.py`、0075 task docs、runtime backend contract 已审查。 | - | - |
| TP-02 | ROOT | 1 | TP-01 | No | Done | 新增 `scripts/postgres-public-webhook-live-smoke.py` 与 `.sh` wrapper；支持 `--allow-missing` blocked summary 和真实 live path。 | - | - |
| TP-03 | ROOT | 1 | TP-02 | No | Done | runtime backend contract/schema/gate、local-ci、operations docs、roadmap、AGENTS、regression tests 已接线。 | - | - |
| TP-04 | ROOT | 1 | TP-03 | No | Done | py_compile、bash -n、blocked preflight、secret scan、runtime backend gate、focused tests、ruff、format、quick CI 已通过。 | - | - |
| TP-05 | ROOT | 1 | TP-04 | No | In Progress | 本地验证完成；待提交推送并记录 GitHub Acceptance URL。 | - | 需要 git commit/push 与远端 CI |

# Blockers

- live passed 需要真实 `FATE_REPORT_JOB_DATABASE_URL` 和真实公网 `FATE_WEBHOOK_LIVE_URL`；当前本地只完成 blocked preflight 与 quick CI 门禁。

# Runtime State

- Branch: `main`
- Base evidence: 0075 已提交并推送，GitHub Acceptance run `28629504843` success。
- Worktree at task start: clean before 0076 files were generated。
- Local CI evidence: `bash scripts/local-ci.sh --profile quick` passed，209 regression tests passed，evidence `/tmp/fatecat-local-ci-20260703084710`。
