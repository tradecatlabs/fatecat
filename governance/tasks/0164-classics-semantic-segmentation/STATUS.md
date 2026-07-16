# Task Status
- Overall Status: `Done`

# Next Executable Leaves
- 无；全部节点已完成。

# Task Package Status Table
| Node ID | Parent | Depth | Depends On | Ready | Status | Recent Evidence | Blocker | Unblock Needed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | - | No | Done | v3 contract、7 个目录范围和 22 条新增格式噪声排除 | - | - |
| TP-02 | ROOT | 1 | TP-01 | No | Done | 物理行状态机、4 类 paragraph 和精确 sourceLineNumbers | - | - |
| TP-03 | ROOT | 1 | TP-02 | No | Done | navigation 零入 passage；heading boundary violation=0 | - | - |
| TP-04 | ROOT | 1 | TP-03 | No | Done | 17 focused/data-gate tests；14 本双重重建；355 supply checks | - | - |
| TP-05 | ROOT | 1 | TP-04 | No | Done | deep review PASS；Quick CI 529 passed；task strict PASS | - | - |

# Blockers
- 无内部阻塞；书目、版权和底本人工复核继续保持外部边界。

# Runtime State
| Signal | Value |
| --- | --- |
| branch baseline | `main` ahead 3, clean before task |
| v2 documents | 14 |
| v2 paragraphs | 32,931 |
| v2 passages | 943 |
| paragraphs under 12 chars | 12,125 |
| passages crossing detected headings | 142 |
| max heading paths in one passage | 53 |
| canonical mutation | forbidden |
| v3 output | `infra/runtime/local-state/exports/datasets/classics-clean-v3` |
| v3 records | 14 documents / 16,079 paragraphs / 1,430 passages / 484 duplicate records |
| v3 governance | 146 exclusions / 21 human review items / 458 navigation paragraphs |
| v3 quality | semantic replay 0 / heading violations 0 / navigation passages 0 / lineage errors 0 |
| deterministic dataset hash | `48076db9c604017c8cdf51495f5309c68b413d22c6f48324a4674cb5f654a310` |
| canonical aggregate before/after | `7fb963a33eab652d28c76500e7c99678b76c1c7630fa05724acd2e7e7f38c2e9` |
| local build performance | 2.32s wall clock / 117844 KB max RSS |
| focused/data-gate tests | 17 passed |
| Quick CI | 529 passed；evidence `/tmp/fatecat-local-ci-20260717045106` |
