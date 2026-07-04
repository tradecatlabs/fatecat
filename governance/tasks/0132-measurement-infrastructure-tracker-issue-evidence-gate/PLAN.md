# Plan

# Planning Summary

Build a bounded local evidence gate between 0131 tracker import package and later proof-ref/live proof closure. The correct target state is not automated issue creation; it is a verifiable binding point that prevents an operator from claiming issue creation without package hash, commit and work item evidence.

# Lifecycle Gates

| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | Scope excludes real issue creation and live proof | Done |
| PLAN | Contract/script/test/local-ci/doc paths identified | Done |
| BUILD | Gate and wrapper implemented | Done |
| TEST | Focused pytest, ruff, format, secret scan and quick local-ci | Done |
| REVIEW | Non-claim, privacy and doc drift reviewed | Done |
| SHIP | Commit/push/remote CI handled by outer delivery flow | Pending outside task docs |

不得跳过 gate。If real tracker credentials, issue permissions, live proof, certification or third-party audit evidence are required, the task must stop at `外部连通验证待执行` instead of fabricating issue creation or live validation evidence.

## SPEC

新增本地 gate，消费 tracker import package 和可选 operator 脱敏 tracker issue evidence bundle，输出 issue evidence accepted/rejected/pending summary。默认无 evidence 时保持 blocked。

## PLAN

1. 新增 contract：`contracts/fate/audit/external-validation-tracker-issue-evidence.json`。
2. 新增 gate：`scripts/external-validation-tracker-issue-evidence-gate.py`。
3. 新增 wrapper：`scripts/external-validation-tracker-issue-evidence-gate.sh`。
4. 接入 `scripts/local-ci.sh --profile quick`，在 tracker import package 后生成 gate artifact。
5. 新增 regression：`tests/regression/test_external_validation_tracker_issue_evidence_gate.py`。
6. 同步 `scripts/AGENTS.md`、`contracts/fate/audit/AGENTS.md`、`tests/AGENTS.md`、roadmap 和 task index。
7. 跑聚焦验证、secret scan、task docs、quick local-ci。
8. 提交、推送并观察远端 CI。

## BUILD

实现必须复用现有 JSON artifact/hash/gate 风格，不新增数据库、外部 tracker client、队列、网络请求或长期状态。

## TEST

聚焦测试覆盖：

- contract required fields。
- 无 evidence 默认 pending/blocked。
- 全量 evidence accepted。
- raw URL、敏感赋值、placeholder 拒绝。
- body hash mismatch、unknown work item、duplicate work item 阻断。
- CLI 输出 summary。
- local-ci/AGENTS/roadmap wiring。

## REVIEW

- Future-optimal drift：该切片应推进外部验证闭环，而不是重复 issue export。
- Ponytail complexity：只允许一个 bounded gate 和 wrapper，不引入 tracker SDK 或 issue client。
- Document drift：AGENTS、roadmap、task index 必须同步。
- Security/privacy：输出只允许 sanitized issue ref/hash/ids/status。

## SHIP

本任务完成后仍不能声明真实 issue 已创建、live validation passed、certification 100% 或 third-party audit passed。

# Simplest Path

Use the existing JSON artifact gate pattern:

- one contract file,
- one Python validator,
- one shell wrapper,
- one regression test file,
- one local-ci artifact.

No tracker SDK, database, queue or network client is introduced.

# Split Strategy

The task is a single vertical slice:

```text
tracker import package -> optional evidence bundle -> issue evidence gate JSON -> local-ci summary
```

This is intentionally not split by contract/script/test layers because the acceptance criterion is the end-to-end gate artifact.

# Execution Waves

| Wave | Leaves | Result |
| --- | --- | --- |
| W1 | TP-01, TP-02 | Scope, contract and gate |
| W2 | TP-03, TP-04 | local-ci, regression and docs |
| W3 | TP-05 | local validation |
| W4 | TP-06 | git delivery and remote CI |

# Runtime Workflow Contract

Inputs:

- `--tracker-import-package-json`
- optional `--issue-evidence-json`
- optional `--expected-commit`

Output:

- `fatecat.external_validation_tracker_issue_evidence_gate`

Side effects:

- Writes local JSON only.
- Does not call network.
- Does not run `gh`.
- Does not create issues.

# Next Executable Leaves

- No remaining task-local executable leaves after TP-05.
- Git delivery and remote CI are executed by the outer delivery flow.

# Dependency Graph

```text
TP-01
  -> TP-02
    -> TP-03
      -> TP-04
        -> TP-05
          -> TP-06
```

# Rollback Protocol

Rollback is local and mechanical:

- remove `contracts/fate/audit/external-validation-tracker-issue-evidence.json`;
- remove `scripts/external-validation-tracker-issue-evidence-gate.py`;
- remove `scripts/external-validation-tracker-issue-evidence-gate.sh`;
- remove `tests/regression/test_external_validation_tracker_issue_evidence_gate.py`;
- remove local-ci and documentation references.

No database or external tracker state is touched.
