# Task-Level Acceptance

- MingLi-Bench aggregate gate 可本地执行。
- gate summary 包含 core corpus summary、benchmark stats、baseline aggregate、licenseBoundary、evaluationBoundary、noLeak。
- gate summary 不包含题干、出生信息、选项、标准答案、逐题结果、四柱明细、报告正文、token、secret、DSN。
- Evaluation registry 继续把 MingLi-Bench 标记为 `evaluation_only`、`optional`、`releaseRequired=false`。
- data supply chain registry 的 evaluation registry hash 与实际文件一致。
- quick CI 执行 `mingli-bench-gate.sh` 并输出 `mingli-bench-gate.json`。
- focused regression 覆盖新增 gate 和既有 MingLi runner。

# Validation Plan
| Validation | Command / Evidence | Expected |
| --- | --- | --- |
| Syntax | `python3 -m json.tool ...`; `bash -n scripts/mingli-bench-gate.sh scripts/local-ci.sh`; `python3 -m py_compile scripts/mingli-bench-gate.py` | exit 0 |
| Gate | `bash scripts/mingli-bench-gate.sh --year 2025 --sample 5 --output-json <tmp>` | status passed, 0 findings |
| Data supply chain | `bash scripts/data-supply-chain-gate.sh --output-json <tmp>` | exit 0 |
| Focused pytest | `.venv/bin/python -m pytest -q tests/regression/test_mingli_bench_aggregate_gate.py tests/regression/test_mingli_bench_gate.py` | exit 0 |
| Quick CI | `bash scripts/local-ci.sh --profile quick --output <tmp>` | exit 0 |
| Task docs | `validate_task_docs.py --phase closeout`; `validate_tasks_tree.py --phase auto` | exit 0 |

# Validation Evidence
| Validation | Result |
| --- | --- |
| Syntax | passed before task docs closeout |
| Gate smoke sample 3 | passed: 160 questions, 3 answered, 0 findings |
| Gate smoke sample 5 | passed: 160 questions, 5 answered, accuracy aggregate only, 0 findings |
| Focused pytest | passed: 5 tests |
| Data supply chain | passed: 8 assets, 162 checks |
| Quick CI | passed: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0085`, 244 passed |
| Task docs | pending closeout validation after status update |

# Review Gate
- no-leak: gate summary must not include forbidden benchmark/detail fragments.
- release-boundary: MingLi-Bench remains optional/evaluation_only/releaseRequired=false.
- source-integrity: data supply chain hash must match changed evaluation registry.
- document-drift: roadmap/docs/AGENTS/local-ci must agree.

# Runtime Verification Gate
- Gate must run without external API keys or model credentials.
- Gate must fail if forbidden fragments appear in summary.
- Gate must fail if vendor/data-supply/evaluation registry boundaries drift.

# Ship Readiness
- All TODO leaves complete.
- local quick CI passes.
- Worktree is clean after commit.
- Remote GitHub Acceptance evidence is reported by the outer delivery flow after commit/push; this task snapshot does not pre-claim it.

# Task Package Acceptance
| Node ID | Acceptance |
| --- | --- |
| TP-01.01 | Existing core corpus、MingLi runner、registry、vendor and upstream HEAD fact inspected. |
| TP-02.01 | Aggregate gate contract defines required fields and forbidden fragments. |
| TP-03.01 | Python gate and shell wrapper added and smoke-tested. |
| TP-04.01 | Registry、docs、AGENTS and local-ci linked. |
| TP-04.02 | Data supply chain registry hash refreshed. |
| TP-05.01 | Focused regression tests added and passed. |
| TP-05.02 | Full local validation complete; commit/push and remote CI evidence handled by outer delivery flow after commit exists. |

# Anti-Goals

- 不证明外部模型评测质量。
- 不证明专家人工准确率。
- 不证明 MingLi-Bench 上游 HEAD 已同步到本地 vendor。
- 不证明 production provider 使用了 benchmark。

# Live Evidence

外部连通验证待执行。外部模型 benchmark、专家人工评审、上游 snapshot 更新和长期趋势库不在本任务内完成。
