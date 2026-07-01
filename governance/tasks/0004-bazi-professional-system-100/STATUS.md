# Task Status
- Overall Status: `Done`

# Next Executable Leaves
- None

# Task Package Status Table
| Node ID | Parent | Depth | Depends On | Ready | Status | Recent Evidence | Blocker | Unblock Needed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | - | No | Done | Scorecard、Resource Map、Rule Source Gaps 已闭合。 | - | - |
| TP-01.01 | TP-01 | 2 | - | No | Done | `SCORECARD.md` 已新增；字段覆盖检查通过。 | - | - |
| TP-01.02 | TP-01 | 2 | - | No | Done | `RESOURCE_MAP.md` 已新增；资源角色边界检查通过。 | - | - |
| TP-01.03 | TP-01 | 2 | TP-01.01, TP-01.02 | No | Done | `RULE_SOURCE_GAPS.md` 已新增；核心 gap id 检索通过。 | - | - |
| TP-02 | ROOT | 1 | TP-01.03 | No | Done | 基础排盘与历法时间边界 gate 已闭合。 | - | - |
| TP-02.01 | TP-02 | 2 | TP-01.03 | No | Done | `CALENDAR_BOUNDARY_MATRIX.md` 已新增；calendar/oracle tests `10 passed in 160.10s`。 | - | - |
| TP-02.02 | TP-02 | 2 | TP-01.03 | No | Done | `CALENDAR_PROVIDER_CONTRACT.md` 已新增；依赖/Oracle 角色检索通过。 | - | - |
| TP-02.03 | TP-02 | 2 | TP-01.03, TP-02.01, TP-02.02 | No | Done | `BASE_CHART_REGRESSION.md` 已新增；base-chart/API tests `40 passed, 1 skipped in 33.65s`。 | - | - |
| TP-03 | ROOT | 1 | TP-01.03 | No | Done | 证据化与高风险输出边界 gate 已闭合。 | - | - |
| TP-03.01 | TP-03 | 2 | TP-01.03 | No | Done | `RULE_ID_COVERAGE_AUDIT.md` 已新增；rule-depth/policy tests `44 passed in 61.80s`。 | - | - |
| TP-03.02 | TP-03 | 2 | TP-01.03 | No | Done | `REPORT_FIELD_CONTRACT.md` 已新增；API/capability tests `41 passed in 5.64s`。 | - | - |
| TP-03.03 | TP-03 | 2 | TP-01.03, TP-03.01, TP-03.02 | No | Done | `HIGH_RISK_OUTPUT_REGRESSION.md` 已新增；policy/statement tests `19 passed in 55.70s`。 | - | - |
| TP-04 | ROOT | 1 | TP-02.03, TP-03.02 | No | Done | 常规八字分析 evaluator gate 已闭合。 | - | - |
| TP-04.01 | TP-04 | 2 | TP-02.03, TP-03.02 | No | Done | `STRENGTH_MONTH_EVALUATOR.md` 已新增；rule-depth/golden tests `39 passed, 1 skipped in 88.40s`。 | - | - |
| TP-04.02 | TP-04 | 2 | TP-02.03, TP-03.02 | No | Done | `TEN_GOD_STRUCTURE_EVALUATOR.md` 已新增；rule-depth/API tests `61 passed in 65.23s`。 | - | - |
| TP-04.03 | TP-04 | 2 | TP-02.03, TP-03.02, TP-04.01, TP-04.02 | No | Done | `REGULAR_PATTERN_EVALUATOR.md` 已新增；rule-depth/statement tests `35 passed in 117.98s`。 | - | - |
| TP-05 | ROOT | 1 | TP-04.03 | No | Done | 高级格局 evaluator gate 已闭合。 | - | - |
| TP-05.01 | TP-05 | 2 | TP-04.03 | No | Done | `ADVANCED_PATTERN_RULE_MATRIX.md` 已新增；高级格局矩阵检索 PASS。 | - | - |
| TP-05.02 | TP-05 | 2 | TP-04.03 | No | Done | `ADVANCED_PATTERN_GOLDEN.md` 已新增；rule-depth/golden tests `39 passed, 1 skipped in 89.54s`。 | - | - |
| TP-05.03 | TP-05 | 2 | TP-04.03, TP-05.01, TP-05.02 | No | Done | `ADVANCED_PATTERN_EVALUATOR.md` 已新增；rule-depth/API tests `61 passed in 64.93s`。 | - | - |
| TP-06 | ROOT | 1 | TP-04.03 | No | Done | 合化成败 gate 已闭合。 | - | - |
| TP-06.01 | TP-06 | 2 | TP-04.03 | No | Done | `COMBINE_RELATION_CONDITION_CATALOG.md` 已新增；合化条件目录检索 PASS。 | - | - |
| TP-06.02 | TP-06 | 2 | TP-04.03, TP-06.01 | No | Done | `COMBINE_TRANSFORM_STATE_EVALUATOR.md` 已新增；rule-depth/API tests `61 passed in 64.93s`。 | - | - |
| TP-06.03 | TP-06 | 2 | TP-04.03, TP-06.02 | No | Done | `COMBINE_TRANSFORM_COUNTEREXAMPLE_MATRIX.md` 已新增；golden/rule-depth tests `39 passed, 1 skipped in 89.35s`。 | - | - |
| TP-07 | ROOT | 1 | TP-04.01, TP-04.03, TP-06.03 | No | Done | 用神策略矩阵、决策 evaluator、冲突 golden 均已闭合。 | - | - |
| TP-07.01 | TP-07 | 2 | TP-04.01, TP-04.03, TP-06.03 | No | Done | `YONGSHEN_STRATEGY_MATRIX.md` 已新增；rg gate PASS；rule-depth/API tests `61 passed in 64.97s`。 | - | - |
| TP-07.02 | TP-07 | 2 | TP-04.01, TP-04.03, TP-06.03, TP-07.01 | No | Done | `YONGSHEN_DECISION_EVALUATOR.md` 已新增；format gate PASS；rule-depth/API tests `61 passed in 75.53s`。 | - | - |
| TP-07.03 | TP-07 | 2 | TP-04.01, TP-04.03, TP-06.03, TP-07.02 | No | Done | `YONGSHEN_CONFLICT_GOLDEN.md` 已新增；format gate PASS；golden/rule-depth tests `39 passed, 1 skipped in 90.40s`。 | - | - |
| TP-08 | ROOT | 1 | TP-04.02, TP-05.03, TP-07.03 | No | Done | 岁运触发、专题联合评分、专题风险边界均已闭合。 | - | - |
| TP-08.01 | TP-08 | 2 | TP-04.02, TP-05.03, TP-07.03 | No | Done | `FORTUNE_TRIGGER_MATRIX.md` 已新增；rg gate PASS；rule-depth/API tests `61 passed in 64.77s`。 | - | - |
| TP-08.02 | TP-08 | 2 | TP-04.02, TP-05.03, TP-07.03, TP-08.01 | No | Done | `TOPIC_PROFILE_JOINT_SCORING.md` 已新增；format gate PASS；API/rule-depth tests `61 passed in 64.99s`。 | - | - |
| TP-08.03 | TP-08 | 2 | TP-04.02, TP-05.03, TP-07.03, TP-08.02 | No | Done | `TOPIC_RISK_BOUNDARY.md` 已新增；policy/statement tests `19 passed in 56.93s`；API/rule-depth tests `61 passed in 68.73s`。 | - | - |
| TP-09 | ROOT | 1 | TP-08.03 | No | Done | Golden shard、MingLi full、BaziQA 审查、failure taxonomy 均已闭合。 | - | - |
| TP-09.01 | TP-09 | 2 | TP-08.03 | No | Done | `GOLDEN_SHARD_DEEP_GATE.md` 已新增；shard 0/4 `10 passed in 629.63s`。 | - | - |
| TP-09.02 | TP-09 | 2 | TP-08.03 | No | Done | `MINGLI_FULL_EVALUATION_GATE.md` 已新增；full benchmark answered=160/160, correct=44, accuracy=27.50%, no answer leakage；回归 `12 passed, 1 skipped in 39.71s`。 | - | - |
| TP-09.03 | TP-09 | 2 | TP-08.03 | No | Done | `BAZIQA_ADMISSION_REVIEW.md` 已新增；BaziQA 判定为 future_candidate/evaluation_only，不进入 runtime 或正式 gate。 | - | - |
| TP-09.04 | TP-09 | 2 | TP-08.03, TP-09.02 | No | Done | `MINGLI_FAILURE_TAXONOMY.md` 已新增；10 类 failure class 有 owner、缺口类型、回炉方向、禁止路径；无单题 ID 示例泄漏。 | - | - |
| TP-10 | ROOT | 1 | TP-09.01, TP-09.03, TP-09.04 | No | Done | `FINAL_REVIEW.md` / `CLOSEOUT.md` 已新增；本地 quick/full gate PASS；Active BLOCK=0。 | - | - |
| TP-10.01 | TP-10 | 2 | TP-09.01, TP-09.03, TP-09.04 | No | Done | `EVALUATOR_SPLIT_FORTUNE.md` 已新增；fortune evaluator 单切片完成；目标回归 `70 passed, 1 skipped in 106.56s`。 | - | - |
| TP-10.02 | TP-10 | 2 | TP-09.01, TP-09.03, TP-09.04, TP-10.01 | No | Done | `REPORT_MARKDOWN_BOUNDARY_FINAL.md` 已新增；Web 不再泄漏 lifecycle/lifecycleGate；验证 `46 passed in 70.22s`。 | - | - |
| TP-10.03 | TP-10 | 2 | TP-09.01, TP-09.03, TP-09.04, TP-10.02 | No | Done | `FINAL_REVIEW.md` / `CLOSEOUT.md` 已新增；quick evidence `/tmp/fatecat-local-ci-20260616233736`，full evidence `/tmp/fatecat-local-ci-20260616233751`；Active BLOCK=0。 | - | - |

# Blockers
- 无

# Runtime State
- Active workflow state: 以 `TASK_PACKAGE_SET.json` / `TASK_EXECUTION_WAVE_PACKET.json` 为准。
- Approval state: 未记录即视为未授权。
- Resume rule: 继续任务前重新读取当前 packet、Recent Evidence、Blockers、Runtime State。
- Post-closeout addendum 2026-07-01: 已按用户要求补齐 ctext 八字典籍 TXT 语料，挂入 TP-01.02 resource boundary；新增/刷新 `五行精纪`、`滴天髓阐微`、`子平真诠评注`、`珞琭子三命消息赋注`、`兰台妙选`、`神峰通考`，`增补星平会海命学全书` 因 OCR 质量差登记为 blocked_until_manual_correction。
- Post-closeout evidence 2026-07-01: `domains/fate-analysis/data-products/classics/source_manifest.tsv` 与 `copyright_review.tsv` 已记录来源、hash 与使用边界；验证命令为 `bash scripts/check-source-hygiene.sh`。
- Stop condition: 发现 benchmark answer leakage，立即停止 benchmark 提升任务并回滚泄漏路径。
- Stop condition: 核心排盘结果与 oracle/golden 不一致且无法解释，停止相关 evaluator 迁移。
- Stop condition: 专家样本或资料 license 不清，相关规则只能停在 reference/beta，不得 production 化。
- Stop condition: 高风险专题出现现实处方或保证式话术，停止报告发布并补 policy regression。
- TP-01.01: status=Done; verifier_context=自审; evidence=`SCORECARD.md` gate PASS
- TP-01.02: status=Done; verifier_context=自审; evidence=`RESOURCE_MAP.md` gate PASS
- TP-01.03: status=Done; verifier_context=自审; evidence=`RULE_SOURCE_GAPS.md` gate PASS
- TP-02.01: status=Done; verifier_context=自审; evidence=`CALENDAR_BOUNDARY_MATRIX.md` gate PASS
- TP-02.02: status=Done; verifier_context=自审; evidence=`CALENDAR_PROVIDER_CONTRACT.md` gate PASS
- TP-02.03: status=Done; verifier_context=自审; evidence=`BASE_CHART_REGRESSION.md` gate PASS
- TP-03.01: status=Done; verifier_context=自审; evidence=`RULE_ID_COVERAGE_AUDIT.md` gate PASS
- TP-03.02: status=Done; verifier_context=自审; evidence=`REPORT_FIELD_CONTRACT.md` gate PASS
- TP-03.03: status=Done; verifier_context=自审; evidence=`HIGH_RISK_OUTPUT_REGRESSION.md` gate PASS
- TP-04.01: status=Done; verifier_context=自审; evidence=`STRENGTH_MONTH_EVALUATOR.md` gate PASS
- TP-04.02: status=Done; verifier_context=自审; evidence=`TEN_GOD_STRUCTURE_EVALUATOR.md` gate PASS
- TP-04.03: status=Done; verifier_context=自审; evidence=`REGULAR_PATTERN_EVALUATOR.md` gate PASS
- TP-05.01: status=Done; verifier_context=自审; evidence=`ADVANCED_PATTERN_RULE_MATRIX.md` gate PASS
- TP-05.02: status=Done; verifier_context=自审; evidence=`ADVANCED_PATTERN_GOLDEN.md` gate PASS
- TP-05.03: status=Done; verifier_context=自审; evidence=`ADVANCED_PATTERN_EVALUATOR.md` gate PASS
- TP-06.01: status=Done; verifier_context=自审; evidence=`COMBINE_RELATION_CONDITION_CATALOG.md` gate PASS
- TP-06.02: status=Done; verifier_context=自审; evidence=`COMBINE_TRANSFORM_STATE_EVALUATOR.md` gate PASS
- TP-06.03: status=Done; verifier_context=自审; evidence=`COMBINE_TRANSFORM_COUNTEREXAMPLE_MATRIX.md` gate PASS
- TP-07.01: status=Done; verifier_context=自审; evidence=`YONGSHEN_STRATEGY_MATRIX.md` gate PASS
- TP-07.02: status=Done; verifier_context=自审; evidence=`YONGSHEN_DECISION_EVALUATOR.md` gate PASS
- TP-07.03: status=Done; verifier_context=自审; evidence=`YONGSHEN_CONFLICT_GOLDEN.md` gate PASS
- TP-08.01: status=Done; verifier_context=自审; evidence=`FORTUNE_TRIGGER_MATRIX.md` gate PASS
- TP-08.02: status=Done; verifier_context=自审; evidence=`TOPIC_PROFILE_JOINT_SCORING.md` gate PASS
- TP-08.03: status=Done; verifier_context=自审; evidence=`TOPIC_RISK_BOUNDARY.md` gate PASS
- TP-09.01: status=Done; verifier_context=自审; evidence=`GOLDEN_SHARD_DEEP_GATE.md` gate PASS; shard 0/4 `10 passed in 629.63s`
- TP-09.02: status=Done; verifier_context=自审; evidence=`MINGLI_FULL_EVALUATION_GATE.md` gate PASS with accuracy WARN; answered=160/160; accuracy=27.50%; no answer leakage; generation runtime 5m45.770s
- TP-09.03: status=Done; verifier_context=自审; evidence=`BAZIQA_ADMISSION_REVIEW.md` gate PASS as future_candidate/evaluation_only
- TP-09.04: status=Done; verifier_context=自审; evidence=`MINGLI_FAILURE_TAXONOMY.md` gate PASS; failureClassCount=10
- TP-10.01: status=Done; verifier_context=自审; evidence=`EVALUATOR_SPLIT_FORTUNE.md` gate PASS; target regression `70 passed, 1 skipped in 106.56s`
- TP-10.02: status=Done; verifier_context=自审; evidence=`REPORT_MARKDOWN_BOUNDARY_FINAL.md` gate PASS; web/api/markdown regression `46 passed in 70.22s`
- TP-10.03: status=Done; verifier_context=自审; evidence=`FINAL_REVIEW.md` gate PASS; quick `50 passed in 8.81s`; full `183 passed, 1 skipped in 459.42s`; delivery smoke API/Bot dry-run/export smoke PASS
