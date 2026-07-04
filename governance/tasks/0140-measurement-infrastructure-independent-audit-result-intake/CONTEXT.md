# Repo Evidence
- 调试模式: Optional
- Current worktree: current `main` branch.
- 现状缺口：`scripts/third-party-audit-rehearsal.py` 原先将 `third_party.independent_result` 硬编码为 blocked。
- 新 gate 证据：`evidence/INDEPENDENT_AUDIT_RESULT_GATE_PENDING.json`。
- 三方演练证据：`evidence/THIRD_PARTY_AUDIT_REHEARSAL_WITH_INDEPENDENT_GATE.json`。
- local-ci 证据：`evidence/LOCAL_CI_SUMMARY.json`，quick profile 388 tests passed。

# Constraints Matrix
| Constraint | Handling |
| --- | --- |
| 不伪造真实审计结果 | 默认 gate 只输出 pending/blocked。 |
| 独立审计结果需要结构化入口 | 新增 contract + gate + rehearsal input。 |
| accepted intake 不等于 release passed | `shipGate.status=blocked` 保持不变。 |
| 隐私边界 | raw URL、敏感赋值、placeholder、commit mismatch 均有负向测试。 |
| 当前 worktree only | 只分析并修改当前分支当前文件。 |

# Change Boundary
- Added `contracts/fate/audit/independent-audit-result.json`.
- Added `scripts/independent-audit-result-gate.py` / `.sh`.
- Updated third-party audit rehearsal and local-ci wiring.
- Updated regression tests, AGENTS, roadmap and task package.
- Did not execute live external systems or create real auditor result.

# Risk Matrix
| Risk | Status | Evidence / Mitigation |
| --- | --- | --- |
| 审计结果被伪造 | Controlled | gate 不生成结果，只校验 operator supplied bundle；默认 pending。 |
| accepted intake 被误认为 100% | Controlled | `shipGate=blocked`，third-party rehearsal 仍看 external pending。 |
| 隐私泄漏 | Controlled | raw URL/sensitive/placeholder tests and secret scan from local-ci. |
| 文档漂移 | Controlled | AGENTS、roadmap、task index 已同步。 |

# Assumptions and Falsification
| Assumption | Falsifier | Current Result |
| --- | --- | --- |
| independent result 应是一等证据资源 | 审计结果可用无 schema 自由文本安全闭合 | Not falsified; gate added. |
| local-ci 默认不应伪造 accepted | quick local-ci 输出 acceptedResults > 0 | Not falsified; pendingResults=1. |
| accepted independent gate 不应清空 external pending | rehearsalGate 变 passed while externalPending > 0 | Not falsified; rehearsalGate=blocked. |
| no sensitive output | secret scan findingCount > 0 | Not falsified; local-ci secret scan passed. |

# Critical Ambiguities
- 真实独立审计人员身份、签名方式和外部审计报告位置需要授权 operator 提供。
- 真实审计结果的法律效力和合同边界不在本地代码仓库内完成。
- 当前任务不决定 certification 最终是否可通过，只提供审计结果 intake 控制面。

# Debug Evidence Contract
- Debug mode is optional because this is a control-plane feature slice, not a bugfix.
- Regression reproduction:

```bash
.venv/bin/python -m pytest -q \
  tests/regression/test_independent_audit_result_gate.py \
  tests/regression/test_third_party_audit_rehearsal.py
```

# Task Package Context Map
- `evidence/INDEPENDENT_AUDIT_RESULT_GATE_PENDING.json`: default pending independent audit result gate.
- `evidence/THIRD_PARTY_AUDIT_REHEARSAL_WITH_INDEPENDENT_GATE.json`: rehearsal output consuming independent gate.
- `evidence/LOCAL_CI_SUMMARY.json`: quick local-ci artifact index.

## TP-01 Current Rehearsal Gap
Third-party audit rehearsal hard-coded the independent result checklist item as blocked.

## TP-02 Independent Audit Result Intake Gate
The new gate validates redacted signed result bundle structure and current commit binding.

## TP-03 Rehearsal and Local-CI Wiring
Third-party audit rehearsal consumes the independent gate; quick local-ci produces pending gate by default.

## TP-04 Regression and Documentation
Focused regression and quick local-ci validate behavior; AGENTS and roadmap are synchronized.

## TP-05 Task Evidence Closeout
Machine evidence is copied into this task package.
