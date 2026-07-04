# AGENTS.md - evaluation resources

## 目录用途

`contracts/fate/evaluations/` 是测算基础设施的评测资源真相源。这里登记 golden fixture、benchmark 数据集和本地评测运行入口，只做发现、审计和发布门禁说明，不保存运行时结果库。

## 目录结构

```text
evaluations/
├── AGENTS.md
├── core-quality-corpus.json
├── diff-policy.json
├── mingli-bench-gate.json
├── professional-quality-rubric.json
├── report-diff-policy.json
├── registry.json
├── trend-policy.json
└── schemas/
    ├── dataset.schema.json
    └── evaluation-run.schema.json
```

## 职责边界

- `registry.json`：登记 Dataset 与 EvaluationRun 资源，记录路径、用途、命令、本地可验证性、隐私和风险边界。
- `core-quality-corpus.json`：登记八字/紫微核心质量语料、最小样本数量、覆盖标签、隐私边界和 release gate，不保存真实用户命例。
- `professional-quality-rubric.json`：定义八字/紫微专业质量评审维度、证据要求、人工复核边界和禁止宣称；只作 evaluation-only 契约，不证明真实命例准确率。
- `diff-policy.json`：定义本地 Evaluation summary diff 的失败阈值和隐私边界；只比较状态与命令结果，不解析标准答案。
- `trend-policy.json`：定义 EvaluationRun 历史趋势门禁策略；拒绝最新失败、连续失败、缺失 required run 和失败命令，不保存命令输出、benchmark 标准答案或报告正文。
- `mingli-bench-gate.json`：定义 MingLi-Bench 离线 benchmark 聚合门禁报告契约；只允许输出 stats、baseline 汇总和 license/usage/no-leak 边界。
- `report-diff-policy.json`：定义 production report 的 summary-only 结构 diff 策略；锁门禁、标题结构、体系隔离和禁止保存完整报告正文，不锁完整自然语言断语。
- `schemas/dataset.schema.json`：定义 Dataset 资源字段，覆盖 golden、benchmark、classics、calendar 和 rule registry 等数据资产。
- `schemas/evaluation-run.schema.json`：定义 EvaluationRun 资源字段，覆盖本地回归、release gate、offline benchmark 和后续外部评测。
- `scripts/run-evaluations.sh`：本地 EvaluationRun 执行入口；读取本 registry，输出机器可读 summary JSON。
- `scripts/core-quality-corpus-gate.sh`：核心质量语料门禁；校验 `core-quality-corpus.json`、`report-diff-policy.json`、`professional-quality-rubric.json`、registry 链接、匿名样本数量、覆盖标签、summary-only 报告 diff 策略和北京测试样本隐私边界。
- `scripts/mingli-bench-gate.sh`：MingLi-Bench 离线聚合门禁；复用 core corpus gate 与 FateCat baseline runner，只写聚合 summary，不写题目、出生信息、标准答案或逐题结果。
- `scripts/compare-evaluations.sh`：本地 Evaluation summary diff 入口；读取两个 summary JSON 和 `diff-policy.json` 判定是否回归。
- `scripts/evaluation-trend-gate.sh`：本地 EvaluationRun 历史趋势门禁入口；读取 `trend-policy.json` 与 history/latest summary，输出 summary-only trend gate JSON。
- `scripts/evaluation-dashboard.sh`：本地 Evaluation dashboard 渲染入口；把 summary/diff 输出为静态 HTML artifact，不渲染命令输出 tail、标准答案或报告正文。
- `scripts/evaluation-dashboard-smoke.sh`：本地 dashboard dry-run smoke；作为 `run.evaluation_dashboard_smoke` 登记并进入本地必跑集合。
- `scripts/evaluation-trend-gate-smoke.sh`：本地 trend gate synthetic smoke；生成脱敏 history fixture 验证趋势门禁，不执行重型评测、不访问公网。
- `scripts/evaluation-nightly.sh`：本地 nightly 包装入口；执行 releaseRequired 评测、history/latest、diff 和 dashboard artifact，供 GitHub scheduled workflow 调用。
- 这里不保存 golden 大文件内容，不保存 MingLi-Bench 标准答案明细，不保存真实用户样例。
- evaluation-only 资源不得被 production provider 读取；生产逻辑只能通过明确的数据产品或 provider 输入契约读取允许的数据。
- runner 只能执行白名单命令：`bash scripts/*.sh` 与 `python -m pytest`；不得使用 `shell=True`、旧路径 fallback、真实 secret 或生产外部连通。
