# Task-Level Acceptance
- 所有模板占位符均已回填
- 叶子节点数量：12
- 当前可立即执行叶子节点：无；12 个叶子节点全部完成

# Validation Plan
- 匿名八字动态重复扫描：标题计数、连续 Markdown 表格 hash、字段所有权检查。
- 关系边界测试：单辰、辰辰、巳寅、子辰、无关系样本和成熟 provider 对照。
- `tests/regression/test_bazi_statement_golden.py`：结构化关系与证据回归。
- `tests/regression/test_branding_support.py`：标准块、神煞和全报告唯一性回归。
- 多端 normalized semantic parity 与紫微独立报告回归。
- 报告生成耗时、行数和字节数前后 benchmark。
- `bash scripts/local-ci.sh --profile quick`。
- `python3 governance/tools/validate_governance_package.py --strict` 与任务文档校验。

# Review Gate
- correctness：不存在单支自刑、对称重复、冲突结果或唯一信息丢失。
- architecture：计算内部只有一个关系事实源，兼容字段只做投影。
- test-quality：失败测试先于修复，且不以整份易变长文本快照替代语义断言。
- performance：去重和规范化不引入重复全量扫描或显著耗时退化。
- future-optimal-drift：禁止通过新的 wrapper 或双轨算法保留错误概念。
- document-drift：结构、profile、evidence 与文档口径一致。

# Runtime Verification Gate
- 本任务不新增运行时服务、数据库或外部调用。
- 运行验证限定为本地确定性报告、现有多端语义测试和 quick CI。
- 无需生产 live；不得把本地报告样本写入日志或提交真实用户资料。

# Ship Readiness
- 所有 P0 正确性与唯一性门禁通过。
- DEBUG.md 通过 conclude 校验，REVIEW 无 BLOCK。
- API 兼容边界、回滚方式和残余弃用项明确。
- 任务 closeout 与审计案例采样通过 strict 校验。
- 后续提交必须只包含 0160 任务相关改动，并由 auto-github 获取真实远端 CI 证据。

# Final Evidence
- 隔离副本：`/tmp/fatecat-0160-final-PhEZGQ`，仅应用 0160 明确文件清单。
- `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0160-final`：PASS，468 passed；ruff、format、mypy、L4 golden、多端 semantic diff、性能与供应链门禁通过。
- `validate_governance_package.py --strict`：exit 0，仅两个运行态目录建议 WARN，无 BLOCK。
- principle gate、项目审计案例 strict、审计采样 strict 与 DEBUG conclude：PASS。
- commit、push、远端 CI 与生产 live 未执行；外部连通验证待执行。

# Task Package Acceptance
## TP-01
- 验收: `确认缺陷基线与目标契约` 达到其 objective，且依赖关系保持一致

### TP-01.01
- 验收: `建立动态复现与影响矩阵` 达到其 objective，且依赖关系保持一致

### TP-01.02
- 验收: `定义章节所有权与 canonical 关系契约` 达到其 objective，且依赖关系保持一致

## TP-02
- 验收: `收敛干支关系计算真相源` 达到其 objective，且依赖关系保持一致

### TP-02.01
- 验收: `先写关系正确性失败测试` 达到其 objective，且依赖关系保持一致

### TP-02.02
- 验收: `实现 canonical 关系模型与兼容投影` 达到其 objective，且依赖关系保持一致

## TP-03
- 验收: `收敛报告章节字段所有权` 达到其 objective，且依赖关系保持一致

### TP-03.01
- 验收: `先写全报告唯一性失败测试` 达到其 objective，且依赖关系保持一致

### TP-03.02
- 验收: `按所有权重构报告渲染` 达到其 objective，且依赖关系保持一致

## TP-04
- 验收: `治理兼容字段与机器契约` 达到其 objective，且依赖关系保持一致

### TP-04.01
- 验收: `审计公开字段依赖与迁移边界` 达到其 objective，且依赖关系保持一致

### TP-04.02
- 验收: `同步 profile、证据与文档契约` 达到其 objective，且依赖关系保持一致

## TP-05
- 验收: `建立防复发质量门禁` 达到其 objective，且依赖关系保持一致

### TP-05.01
- 验收: `补齐唯一性与关系门禁` 达到其 objective，且依赖关系保持一致

### TP-05.02
- 验收: `执行多端回归与性能验证` 达到其 objective，且依赖关系保持一致

## TP-06
- 验收: `审查、治理与交付收口` 达到其 objective，且依赖关系保持一致

### TP-06.01
- 验收: `执行修复后专项审查与案例采样` 达到其 objective，且依赖关系保持一致

### TP-06.02
- 验收: `生成 closeout 与 Git 交付交接` 达到其 objective，且依赖关系保持一致

# Anti-Goals
- 不得修改 0160 明确业务、契约、测试、文档与项目审计案例之外的路径
- 不得虚构证据
- 不得混入 0159 或其他并发任务改动
- 不得把本地验证写成已完成 commit、push、远端 CI 或生产 live
