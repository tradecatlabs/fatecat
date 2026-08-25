# AGENTS.md - 八字数学形式化文档

## 目录用途

本目录保存八字数学形式化的人类可读规范、构建流程和维护规则。它解释对象、函数、关系、Profile、不确定性、证据和证明义务，但不作为生产运行时机器契约。

## 职责边界

- `README.md`：文档地图、范围、里程碑和完成定义。
- `FORMAL_SPEC.md`：数学对象、基础语义和证明义务。
- `BUILD.md`：从来源到规范、契约、实现、fixture、gate 和 evidence 的构建顺序。
- `MAINTENANCE.md`：版本、变更分类、兼容、Golden、依赖升级和故障维护规则。
- 可执行 schema、Profile、有限映射和规则必须进入 `contracts/fate/`。
- 生产算法必须进入 `domains/fate-analysis/services/fate-core/`。
- Golden 和测试必须进入 canonical data-products 与 tests，不得嵌在 Markdown 中充当运行数据。

## 修改纪律

- 修改任一数学定义前，必须读取本目录全部当前文档。
- 新定义必须声明定义域、值域、Profile 依赖、无定义条件和证明义务。
- 新规则必须声明来源、适用条件、不适用条件、证据、冲突策略和风险边界。
- 不得把现有实现行为自动提升为数学定义；先记录差异，再决定规范。
- 不得把 oracle、benchmark 或多数实现一致写成真理证明。
- 不得用分数掩盖离散候选、unknown 或 conflict。
- 不得宣称形式化、测试或 evidence 证明了命理预测的科学有效性。
- 文档新增计划能力时必须标记 draft/planned，不得包装为已落地 production。

## 同步要求

语义变更必须同步检查：

- 本目录文档地图和版本。
- `contracts/fate/` 对应机器契约。
- `fate-core` 实现和 engine version。
- Golden、性质测试、边界矩阵和回归。
- Evidence schema、规则引用和多端语义一致性。

文档澄清不改变行为时，也应明确标记为非语义变更。

## 验证

至少执行：

```bash
bash scripts/check-structure.sh
bash scripts/check-source-hygiene.sh
bash scripts/local-ci.sh --profile quick
```

仅修改草案文档时，可以先执行结构、链接和 source hygiene；进入机器契约或实现后必须运行对应 focused tests 和 quick gate。
