# Task Overview
- Task ID: `0021`
- Slug: `measurement-infrastructure-wave4-evaluation-runner`
- Objective: `把 EvaluationRun 从资源发现推进到本地可执行 runner：读取 contracts/fate/evaluations/registry.json，按 run id 或本地必跑集合执行安全白名单命令，输出机器可读 summary JSON，并补测试、文档、路线图和任务 closeout。`
- Status: `In Progress`

## In Scope
- 新增 `scripts/run-evaluations.py` 与 `scripts/run-evaluations.sh`，读取 `contracts/fate/evaluations/registry.json` 执行 EvaluationRun。
- 支持 `--run-id`、`--all-local-required`、`--all-local`、`--dry-run` 与 `--output-json`。
- runner 必须白名单命令、禁止 `shell=True`、默认跳过 `requires_reference_repo`。
- 补充 contract/API/runner 回归测试，并把 runner 纳入 quick CI focused tests。
- 更新 API 接入文档、100% 路线图、scripts/AGENTS、evaluations/AGENTS 与任务 closeout。

## Out of Scope
- 不建立持久化 EvaluationRun 历史数据库。
- 不做跨 commit diff、dashboard、nightly 调度或远端 CI 状态同步。
- 不执行外部模型 API、真实公网服务、真实 Bot live smoke 或需要 secret 的评测。
- 不把 MingLi-Bench 标准答案、用户样例或生产日志写入 registry、docs、tests 或 summary。
- 不修改八字、紫微、黄历、Web/API/Bot 的报告生成逻辑。

## Task Package Tree
```text
TP-01 EvaluationRun 执行需求盘点
  TP-01.01 盘点 registry、golden、benchmark 和现有评测脚本
  TP-01.02 回填任务契约与文档字段
TP-02 本地 runner 落地
  TP-02.01 新增 Python runner 与 bash wrapper
  TP-02.02 实现选择器、命令白名单、dry-run 和 summary JSON
  TP-02.03 在 registry/schema/AGENTS 中登记 runner 边界
TP-03 回归测试与 quick CI 接入
  TP-03.01 新增 runner 单元/契约测试
  TP-03.02 更新 capability/API contract tests
  TP-03.03 把 runner 测试纳入 quick CI focused tests
TP-04 文档与路线图同步
  TP-04.01 更新 API 接入文档
  TP-04.02 更新 100% 基础设施路线图 checklist
TP-05 验证收口
  TP-05.01 执行 runner dry-run、focused tests、实际 solar_terms run 和 quick CI
  TP-05.02 回填 closeout 状态和验证证据
```

## Requirement Alignment
- 用户目标：把 FateCat 推进为“测算基础设施”，不是功能清单合集。
- 本任务切片：落实 IMP-08 Evaluation 与 Golden 的最小可执行 runner，使 registry 中的 EvaluationRun 不止能发现，也能本地复现。
- 基础设施同构依据：CI runner、Kubernetes controller、OpenAI Evals 的共同模式都是“资源声明 + 受控执行 + 机器可读结果”。
- 完成口径：本地可执行、命令可审计、输出可归档；扩展评测、历史趋势和外部 live eval 仍作为后续任务。

## Task Package Overview
| Node | Type | Purpose | Gate |
| --- | --- | --- | --- |
| TP-01 | SPEC | 确认现有 EvaluationRun 与命令边界 | 不遗漏 required/optional 和 reference repo 边界 |
| TP-02 | BUILD | 建立本地 runner 和协议登记 | 白名单命令、无 shell=True、summary JSON 可读 |
| TP-03 | TEST | 覆盖 runner 与 contract 断言 | dry-run、安全拒绝、API/registry 口径一致 |
| TP-04 | DOC | 同步接入文档与路线图 | 不夸大为 dashboard/nightly/外部 eval |
| TP-05 | SHIP | 执行门禁并回填证据 | runner 实跑和 quick CI 有真实输出 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
