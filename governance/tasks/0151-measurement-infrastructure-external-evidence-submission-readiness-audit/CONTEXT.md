# Repo Evidence
| Evidence | Current Fact |
| --- | --- |
| Branch | `main` |
| Previous task | 0150 Done, remote Acceptance `28717874489` passed for commit `abfd6fb` |
| Current blocker | `measurement-infrastructure-certification` remains blocked until external proof/live/human/audit evidence closes |
| Existing proof-ref gate | `scripts/external-validation-proof-ref-gate.py` accepts redacted proof refs but keeps ship blocked |
| Existing live proof gate | `scripts/external-validation-live-proof-gate.py` accepts category live proof only after proof-ref gate |
| Existing operator packet | `scripts/external-validation-operator-execution-packet.py` emits operator steps, command hashes and proof-ref templates |
| Existing core quality gate | `scripts/core-quality-human-review-gate.py` defaults to external review/benchmark/no-leak pending |
| local-ci chain | quick profile already emits proof-ref/live/operator/human/rehearsal/certification artifacts |

# Constraints Matrix
| Constraint | Handling |
| --- | --- |
| 不执行真实 live | 0151 只读取 JSON artifacts，不发起网络请求。 |
| 不泄露敏感信息 | script 拒绝 raw URL、token/secret/password/DSN/private key 等敏感片段。 |
| 不伪造 100% | 默认 `submissionReadinessGate.status=blocked` 是正确结果。 |
| 复用现有体系 | 不新增平行 proof schema；只聚合现有 gate summary。 |
| 文档驱动 | 新增文件同步 AGENTS、roadmap 和任务包。 |

# Change Boundary
- Add: `contracts/fate/audit/external-evidence-submission-readiness-audit.json`
- Add: `scripts/external-evidence-submission-readiness-audit.py`
- Add: `scripts/external-evidence-submission-readiness-audit.sh`
- Add: `tests/regression/test_external_evidence_submission_readiness_audit.py`
- Modify: `scripts/local-ci.sh`
- Modify: `scripts/AGENTS.md`
- Modify: `contracts/fate/audit/AGENTS.md`
- Modify: `tests/AGENTS.md`
- Modify: `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`
- Modify: 0151 task docs and `governance/tasks/INDEX.md`

# Risk Matrix
| Risk | Mitigation |
| --- | --- |
| readiness audit 被误读为 live passed | Output includes `nonClaims`; gate remains blocked unless all upstream gates are actually passed. |
| 新脚本重复实现 live/proof validation | It only checks already generated gate summaries and operator packet structure. |
| local-ci order wrong | Run after certification and third-party rehearsal, because both are inputs. |
| sensitive evidence leak | Reject raw URL and sensitive assignment regex before writing output. |
| CI drag | Targeted regression is small; quick CI already runs the upstream artifacts needed. |

# Assumptions and Falsification
| Assumption | Falsifier |
| --- | --- |
| Existing artifacts contain enough fields to summarize readiness | Test fixtures and local-ci smoke fail because required fields are missing. |
| Operator packet template may keep placeholder artifact hash while still being operator-ready | Contract explicitly distinguishes template placeholder from accepted evidence. |
| Certification remains the final claim gate | If certification `canClaim100Percent=false`, readiness audit cannot claim 100%. |

# Critical Ambiguities
- 无。0151 不需要真实外部凭证；真实证据提交仍留给后续 operator 任务。

# Debug Evidence Contract
- 调试模式: `Optional`
- 若 tests/local-ci 失败，先保留 failing command、stderr 摘要和最小修复证据。

# Task Package Context Map
| Artifact | Role |
| --- | --- |
| `README.md` | 任务树与范围 |
| `PLAN.md` | 执行波次与 gate |
| `ACCEPTANCE.md` | 验收命令和预期 |
| `STATUS.md` | 叶子节点状态和证据 |
