# Execution Checklist
[x] TP-01.01 | P0 | 建立动态复现与影响矩阵 | Verify: 运行匿名八字报告重复扫描和关系输出探针，并把命令与摘要写入 DEBUG.md | Gate: 所有已报告症状都有可重复输入、输出和源码调用链 | Parallelizable: No
[x] TP-01.02 | P0 | 定义章节所有权与 canonical 关系契约 | Verify: 人工审查所有权表与现有 pure_analysis/profile/evidence 契约的字段映射 | Gate: 后续实现不需要自行猜测字段归属或关系语义 | Parallelizable: No
[x] TP-02.01 | P0 | 先写关系正确性失败测试 | Verify: 定向 pytest 在旧实现上按预期失败，失败原因与 DEBUG.md 一致 | Gate: 测试能区分真正自刑、方向关系和错误自关联 | Parallelizable: No
[x] TP-02.02 | P0 | 实现 canonical 关系模型与兼容投影 | Verify: 关系定向测试、八字 statement golden 与 evidence 回归通过 | Gate: 计算结果不存在双真相源、自关联或无依据关系 | Parallelizable: No
[x] TP-03.01 | P0 | 先写全报告唯一性失败测试 | Verify: 定向 pytest 在旧报告实现上按预期失败，并对紫微基线通过 | Gate: 测试检查语义所有权而非绑定整份易变长文本快照 | Parallelizable: Yes
[x] TP-03.02 | P0 | 按所有权重构报告渲染 | Verify: 标准报告结构测试、唯一性测试和匿名报告语义 diff 通过 | Gate: 默认综合八字 Markdown 不含完全重复块或无所有权字段 | Parallelizable: Yes
[x] TP-04.01 | P1 | 审计公开字段依赖与迁移边界 | Verify: rg/contract/profile/catalog 扫描结果与 API 回归契约对齐 | Gate: 兼容决策有证据、版本策略和移除条件 | Parallelizable: Yes
[x] TP-04.02 | P1 | 同步 profile、证据与文档契约 | Verify: contract/profile/evidence/文档回归与多端语义测试通过 | Gate: 代码、契约、测试和文档对 canonical/compat 的表述一致 | Parallelizable: No
[x] TP-05.01 | P0 | 补齐唯一性与关系门禁 | Verify: pytest 运行新增门禁并通过故障注入负例 | Gate: 原问题的任一旧实现回潮都会使测试失败 | Parallelizable: No
[x] TP-05.02 | P0 | 执行多端回归与性能验证 | Verify: 定向回归、bash scripts/local-ci.sh --profile quick 与最小 benchmark | Gate: 正确性、兼容性、性能和多端一致性全部通过 | Parallelizable: No
[x] TP-06.01 | P0 | 执行修复后专项审查与案例采样 | Verify: auto-review 专项路由、审计采样 strict 校验与 governance strict | Gate: 修复没有以新的兼容双轨或过度抽象替代旧问题 | Parallelizable: No
[x] TP-06.02 | P0 | 生成 closeout 与 Git 交付交接 | Verify: validate_task_docs --phase closeout 与 build_task_closeout --audit-case-sampling-required | Gate: 任务证据完整、工作树边界清晰且可安全交付 | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
