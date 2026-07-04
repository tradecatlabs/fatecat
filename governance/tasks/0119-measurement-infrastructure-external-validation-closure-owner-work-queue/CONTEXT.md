# Repo Evidence

| Evidence | Result |
| --- | --- |
| `git status --short --branch` | `## main...origin/main` before edits |
| Main roadmap | `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` lists `MI-100.A.01 closure owner work queue` as next step |
| Upstream gate | `scripts/external-validation-closure-gate.py` outputs `fatecat.external_validation_closure_plan` |
| Existing contract | `contracts/fate/audit/external-validation-closure.json` defines owner/category/credential/closure condition fields |

# Constraints Matrix

| Constraint | Handling |
| --- | --- |
| No fake live | work queue has empty `proofRef` and blocked ship gate |
| No secret leakage | output stores source path/line/hash only, not pending excerpt body |
| Single truth source | roadmap remains `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` |
| Local verifiability | contract/script/tests/local-ci are all local commands |
| External systems | external connectivity remains pending |

# Change Boundary

Allowed files:

- `contracts/fate/audit/external-validation-closure-work-queue.json`
- `scripts/external-validation-closure-work-queue.py`
- `scripts/external-validation-closure-work-queue.sh`
- `scripts/local-ci.sh`
- `tests/regression/test_external_validation_closure_work_queue.py`
- `contracts/fate/audit/AGENTS.md`
- `scripts/AGENTS.md`
- `tests/AGENTS.md`
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`
- `governance/tasks/INDEX.md`
- this task directory

# Risk Matrix

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Work queue 被误读为 live passed | 伪造 100% 完成 | `shipGate.status=blocked` and nonClaims |
| Pending excerpt 泄露敏感片段 | 安全事故 | occurrences 只保存 path/line/excerptSha256 |
| 分组过粗导致 owner 丢失 | 后续闭环不可执行 | grouping key fixed to `(owner, category)` |
| local-ci 证据不同步 | 审计链断裂 | summary artifact includes `externalValidationClosureWorkQueue` |

# Assumptions and Falsification

- Assumption: closure plan item already has owner/category/credential/closure fields. Falsifier: script rejects missing required fields.
- Assumption: work queue can be produced without external credentials. Falsifier: script must not read token/DSN/env secrets.
- Assumption: grouped work item should remain blocked until proof verifier exists. Falsifier: any generated work item with non-empty proofRef or passed close result.

# Critical Ambiguities

- `proofRef` schema has not been implemented; it is intentionally an empty string in this slice.
- Owner assignment is category-derived, not human-assigned user identity.
- Stale alert/dashboard is the next MI-100.A follow-up, not part of this task.

# Debug Evidence Contract

- 调试模式: `Optional`
- If tests fail, capture failing command, input fixture, traceback, and whether failure is contract/schema/wiring/privacy related.

# Task Package Context Map

| TP | Context |
| --- | --- |
| TP-01 | Roadmap and existing closure plan contract |
| TP-02 | New work queue contract/script/wrapper/local-ci |
| TP-03 | Regression tests and targeted gates |
| TP-04 | AGENTS/roadmap/task docs/index |
| TP-05 | local CI, secret scan, commit/push/remote CI |
