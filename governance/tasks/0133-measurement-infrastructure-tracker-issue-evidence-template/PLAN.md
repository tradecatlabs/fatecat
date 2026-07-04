# Plan

# Planning Summary

Build a bounded local template generator between 0131 tracker import package and 0132 evidence gate. The target end state is a reproducible evidence skeleton that reduces manual errors without automating issue creation or claiming external validation.

# Lifecycle Gates

| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | Scope excludes real issue creation and live proof | Done |
| PLAN | Contract/script/test/local-ci/doc paths identified | Done |
| BUILD | Template generator and wrapper implemented | Done |
| TEST | Focused pytest, ruff, format, secret scan and quick local-ci | Done |
| REVIEW | Non-claim, privacy and doc drift reviewed | Done |
| SHIP | Commit/push/remote CI handled by outer delivery flow | Pending outside task docs |

不得跳过 gate。If real tracker credentials, issue permissions, live proof, certification or third-party audit evidence are required, the task must stop at `外部连通验证待执行` instead of fabricating issue creation or live validation evidence.

## SPEC

新增本地 template generator，消费 tracker import package，输出 operator 可填写的 evidence bundle skeleton。模板默认不可提交为通过证据。

## PLAN

1. 新增 contract：`contracts/fate/audit/external-validation-tracker-issue-evidence-template.json`。
2. 新增 generator：`scripts/external-validation-tracker-issue-evidence-template.py`。
3. 新增 wrapper：`scripts/external-validation-tracker-issue-evidence-template.sh`。
4. 接入 `scripts/local-ci.sh --profile quick`，在 tracker import package 后生成 template artifact。
5. 新增 regression：`tests/regression/test_external_validation_tracker_issue_evidence_template.py`。
6. 同步 `scripts/AGENTS.md`、`contracts/fate/audit/AGENTS.md`、`tests/AGENTS.md`、roadmap 和 task index。
7. 跑聚焦验证、secret scan、task docs、quick local-ci。
8. 提交、推送并观察远端 CI。

## BUILD

实现必须复用现有 JSON artifact/hash/gate 风格，不新增数据库、外部 tracker client、队列、网络请求或长期状态。

## TEST

聚焦测试覆盖：

- contract required fields。
- template JSON/Markdown 输出。
- skeleton 预填 package sha、commit、workItemId、issueTemplateId、bodySha256、labels。
- skeleton 填入 sanitized issue ref/hash 后可被 0132 gate 接受。
- raw URL 和 sensitive assignment 拒绝。
- CLI 输出 summary。
- local-ci/AGENTS/roadmap wiring。

## REVIEW

- Future-optimal drift：该切片应降低 external evidence 人工错配风险，而不是绕过 0132 gate。
- Ponytail complexity：只允许一个 bounded generator 和 wrapper，不引入 tracker SDK 或 issue client。
- Document drift：AGENTS、roadmap、task index 必须同步。
- Security/privacy：输出只允许 ids/hash/status/空白 fill fields。

## SHIP

本任务完成后仍不能声明真实 issue 已创建、tracker issue evidence accepted、live validation passed、certification 100% 或 third-party audit passed。

# Simplest Path

Use the existing JSON artifact pattern:

- one contract file,
- one Python template generator,
- one shell wrapper,
- one regression test file,
- one local-ci artifact.

No tracker SDK, database, queue or network client is introduced.

# Split Strategy

The task is a single vertical slice:

```text
tracker import package -> evidence bundle template -> filled bundle can pass 0132 gate
```

# Execution Waves

| Wave | Leaves | Result |
| --- | --- | --- |
| W1 | TP-01, TP-02 | Scope, contract and generator |
| W2 | TP-03, TP-04 | local-ci, regression and docs |
| W3 | TP-05 | local validation |
| W4 | TP-06 | git delivery and remote CI |

# Runtime Workflow Contract

Inputs:

- `--tracker-import-package-json`
- optional `--expected-commit`

Outputs:

- `fatecat.external_validation_tracker_issue_evidence_bundle_template`
- Markdown operator fill guide

Side effects:

- Writes local JSON/Markdown only.
- Does not call network.
- Does not run `gh`.
- Does not create issues.

# Next Executable Leaves

- TP-05 validation gates.
- TP-06 git delivery and remote CI after local validation.

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

- remove `contracts/fate/audit/external-validation-tracker-issue-evidence-template.json`;
- remove `scripts/external-validation-tracker-issue-evidence-template.py`;
- remove `scripts/external-validation-tracker-issue-evidence-template.sh`;
- remove `tests/regression/test_external_validation_tracker_issue_evidence_template.py`;
- remove local-ci and documentation references.

No database or external tracker state is touched.
