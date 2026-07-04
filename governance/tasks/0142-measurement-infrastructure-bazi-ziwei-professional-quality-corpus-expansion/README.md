# Task Overview
- Task ID: `0142`
- Slug: `measurement-infrastructure-bazi-ziwei-professional-quality-corpus-expansion`
- Objective: `执行 0141 后续 0142：扩展八字/紫微核心质量匿名 corpus、补 professional quality rubric、提高 core-quality gate 对样本数量/覆盖标签/报告 diff/rubric 的约束，并用回归测试证明该质量证据只作为 evaluation/release gate，不进入 production provider、不保存真实用户资料、不宣称专业能力 100%。`
- Status: `Done`

## In Scope

- 扩展综合八字陈述服务匿名 golden 样本，覆盖更多季节、时辰、格局/证据链组合。
- 扩展紫微基础盘面与规则深度匿名 golden 样本，把最小样本线从 8 提升到 12。
- 新增八字/紫微 professional quality rubric 契约，明确评审维度、证据类型、人工复核边界和禁止宣称。
- 加固 `core-quality-corpus` manifest、report diff policy、evaluation registry 与门禁脚本。
- 同步数据供应链 registry 中被修改 fixture/registry 的 selected sha，保持 source hygiene。
- 更新回归测试和目录说明，证明该语料只用于 evaluation/release gate，不进入 production provider。

## Out of Scope

- 不新增真实命例、真实用户姓名、真实非北京地区样例或生产数据。
- 不修改八字/紫微 production provider 算法，不把 golden fixture 用作运行时断语来源。
- 不声明八字/紫微专业能力 100%、预测准确率 100% 或真实专家评审已完成。
- 不执行 production API、HF Space、Bot、webhook、OIDC、SIEM、OTel、Vault/KMS 或第三方审计 live 验证。
- 不引入新依赖、新外部仓库或新运行时服务。

## Task Package Tree

```text
TP-01 evaluation contract and rubric
TP-02 bazi/ziwei anonymous corpus expansion
TP-03 gate and regression hardening
TP-04 documentation closeout
TP-05 validation and release handoff
```

## Requirement Alignment

| Requirement | Implementation |
| --- | --- |
| 执行 0141 后续质量切片 | 创建并完成 `0142-measurement-infrastructure-bazi-ziwei-professional-quality-corpus-expansion`。 |
| 扩展八字/紫微核心语料 | `statement_cases.json` 增至 8；紫微基础与规则深度样本增至 12。 |
| 增加专业质量准入 | 新增 `contracts/fate/evaluations/professional-quality-rubric.json`。 |
| 强化本地门禁 | `scripts/core-quality-corpus-gate.py` 校验 rubric、policy、registry、样本数量与覆盖标签。 |
| 不混入生产 | manifest/rubric/tests 均声明 `evaluation_only`、不保存真实资料、不作为 production provider 输入。 |
| 不伪造 100% | rubric 和测试保留 human review required 与 forbidden claims。 |

## Task Package Overview

| TP | 名称 | 状态 | 产物 |
| --- | --- | --- | --- |
| TP-01 | evaluation 契约与 rubric | Done | `professional-quality-rubric.json`、manifest/policy/registry 接线 |
| TP-02 | 匿名 corpus 扩容 | Done | 八字陈述 8 例、紫微基础 12 例、紫微规则深度 12 例 |
| TP-03 | 门禁与测试加固 | Done | core-quality gate、pytest regression、L4 smoke 阈值更新 |
| TP-04 | 文档 closeout | Done | evaluations AGENTS、0142 任务包、INDEX 同步 |
| TP-05 | 验证与交付 | Done | JSON parse、core-quality gate、data supply chain gate、L4 smoke、53 项回归通过 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
