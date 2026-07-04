# Task Overview
- Task ID: `0149`
- Slug: `measurement-infrastructure-core-quality-human-review-intake`
- Objective: `执行 0148 后续 0149：把八字/紫微专家评审、外部 benchmark 聚合和 no-leak signoff 从自然语言待办推进为机器可执行 intake gate、本地 CI 接线和 certification 阻断输入；真实专家评审与外部 benchmark 仍需脱敏 evidence bundle，不能伪造完成。`
- Status: `Blocked`

## In Scope
- 新增 core quality human review contract，定义外部专家评审、外部 benchmark 聚合和 no-leak signoff 的脱敏 evidence bundle。
- 新增 `core-quality-human-review-gate`，默认无证据时保持 blocked，具备脱敏 bundle 时只校验结构、commit、hash、rubric dimensions、aggregate benchmark 和隐私边界。
- 将 gate 接入 evaluation registry、local-ci summary、certification core_quality domain、AGENTS 文档和 roadmap。
- 新增回归测试覆盖 pending、accepted、raw URL、敏感片段、commit mismatch、缺 rubric dimension、CLI 和 wiring。

## Out of Scope
- 不生成或伪造专家评审结论。
- 不保存专家姓名、联系方式、真实用户命例、真实出生地、题目、选项、答案、逐题预测、完整报告正文、token、secret、DSN 或 URL。
- 不把 MingLi-Bench 或任何 benchmark 明细注入 production provider。
- 不声明八字/紫微专业能力 100%、预测准确率 100% 或 FateCat 已完成 100% 测算基础设施。
- 不关闭 0144-0147 的外部 live proof，也不替代最终第三方审计。

## Task Package Tree
```text
0149-measurement-infrastructure-core-quality-human-review-intake
├── TP-01 质量域缺口识别
│   └── TP-01.01 核查 core corpus、rubric、MingLi-Bench 与 certification 现状
├── TP-02 专家/benchmark/no-leak intake gate
│   ├── TP-02.01 新增 contract、gate 和 shell wrapper
│   └── TP-02.02 补隐私与反伪造负例
├── TP-03 基础设施接线
│   ├── TP-03.01 接入 evaluation registry、local-ci summary 与 AGENTS
│   └── TP-03.02 接入 certification core_quality domain
├── TP-04 外部人工证据闭合
│   ├── TP-04.01 收集专家 rubric disposition bundle
│   └── TP-04.02 收集 external benchmark aggregate 与 no-leak signoff
└── TP-05 验证与交付
    ├── TP-05.01 运行窄测试、local-ci 和任务文档校验
    └── TP-05.02 提交、推送并触发远端 Acceptance
```

## Requirement Alignment
| Requirement | Alignment |
| --- | --- |
| 0148 next node | 0149 对应 Core quality human review/external benchmark。 |
| 不伪造证据 | 默认 gate 输出 blocked；没有脱敏 bundle 不会写 accepted。 |
| 专家评审 | contract 要求完整 rubric dimensions disposition，但不保存专家身份或报告正文。 |
| 外部 benchmark | 只接收 aggregate artifact hash、sampleCount、accuracy 和 no-per-question-leak，不保存题目/答案/逐题结果。 |
| no-leak | noLeakReview 必须 `passed`、forbiddenFragmentsFound 必须为 0。 |
| certification | `core_quality` domain 必须看到该 gate；无外部人工证据时 certification 不能 passed。 |

## Task Package Overview
| TP | Name | Status | Evidence |
| --- | --- | --- | --- |
| TP-01 | 质量域缺口识别 | Done | 现有 core corpus/rubric/MingLi-Bench 已核查，缺 human review intake |
| TP-02 | 专家/benchmark/no-leak intake gate | Done | contract、Python gate、shell wrapper 已新增 |
| TP-03 | 基础设施接线 | Done | registry、local-ci、certification、AGENTS、roadmap 已接线 |
| TP-04 | 外部人工证据闭合 | Blocked | 需要真实脱敏专家评审和 benchmark evidence bundle |
| TP-05 | 验证与交付 | In Progress | 窄测试已发现 roadmap wiring 缺口并已修复，完整验证待跑 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
