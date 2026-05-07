# Execution Checklist
[ ] TP-01.01 | P0 | 盘点交节时间 raw 表 | Verify: 输出 schema 文档和来源哈希对照。 | Gate: 确认 raw 表不会进入导出包。 | Parallelizable: No
[ ] TP-01.02 | P0 | 构建节气 golden fixture | Verify: fixture schema 校验和样本快照通过。 | Gate: 明确时区、容差、来源哈希。 | Parallelizable: No
[ ] TP-01.03 | P0 | 节气与月令边界测试 | Verify: pytest 对 `lunar-python` 计算结果与 fixture 进行边界断言。 | Gate: 任何误差必须有容差解释。 | Parallelizable: No
[ ] TP-01.04 | P0 | 起运边界回归 | Verify: pytest 覆盖起运顺逆样本。 | Gate: 起运样本来源和预期值必须可追溯。 | Parallelizable: No
[ ] TP-02.01 | P0 | 审计当前 report profile | Verify: 输出入口清单和默认块清单。 | Gate: 确认前端不应自行拼报告。 | Parallelizable: No
[ ] TP-02.02 | P0 | 锁定综合八字默认块 | Verify: 结构快照不含紫微、黄历、建除、六爻等块。 | Gate: 非八字体系统一保留为独立 capability 或未来登记。 | Parallelizable: No
[ ] TP-02.03 | P0 | 报告结构快照测试 | Verify: pytest 快照测试通过。 | Gate: 快照只断言结构，不绑定易变大段文本。 | Parallelizable: No
[ ] TP-03.01 | P0 | 定义 evidence schema | Verify: schema 文档和测试 fixture 通过。 | Gate: 不改变现有公开输出，先兼容追加。 | Parallelizable: No
[ ] TP-03.02 | P0 | 核心结论 evidence mapper | Verify: 单元测试覆盖至少日主、五行喜忌、格局、干支关系。 | Gate: 辅助体系不得提升为核心权重。 | Parallelizable: No
[ ] TP-03.03 | P1 | 证据渲染与可见性 | Verify: Markdown/API 快照覆盖 evidence 可见性。 | Gate: 面向用户显示克制，审计字段保留可机读。 | Parallelizable: Yes
[ ] TP-04.01 | P0 | 独立体系 capability 边界 | Verify: registry/profile 文件与文档一致。 | Gate: 不得宣称未来功能已生产。 | Parallelizable: Yes
[ ] TP-04.02 | P1 | 权重策略测试 | Verify: pytest 或静态配置测试通过。 | Gate: 称骨和神煞只作为辅助解释。 | Parallelizable: Yes
[ ] TP-05.01 | P0 | 输入 schema 与错误响应 | Verify: API/Web/Bot 输入测试覆盖缺字段场景。 | Gate: 错误文案不泄露内部路径或真实样例。 | Parallelizable: Yes
[ ] TP-05.02 | P0 | 隐私与示例脱敏回归 | Verify: `check-privacy-fixtures.sh` 与 pytest 脱敏测试通过。 | Gate: 新增 fixture 必须符合白名单。 | Parallelizable: Yes
[ ] TP-06.01 | P0 | 报告 profile 单一真相源 | Verify: 三端入口测试指向同一 profile。 | Gate: 不引入第二套 Markdown 拼装逻辑。 | Parallelizable: No
[ ] TP-06.02 | P0 | Markdown 复制一致性 | Verify: 复制内容结构快照测试通过。 | Gate: 按钮/控件不影响报告内容。 | Parallelizable: No
[ ] TP-07.01 | P1 | 典籍来源与版权边界审计 | Verify: 来源表与可用范围文档完成。 | Gate: 版权不明资料只能作为 raw 复核来源。 | Parallelizable: Yes
[ ] TP-07.02 | P1 | 小型规则索引种子 | Verify: 规则索引 JSON/YAML schema 校验通过。 | Gate: 每条规则有来源、适用条件、禁用条件。 | Parallelizable: Yes
[ ] TP-07.03 | P1 | 规则引用接入 evidence | Verify: evidence rule_id 与短依据测试通过。 | Gate: 规则引用是追溯层，不是新算法替换。 | Parallelizable: Yes
[ ] TP-08.01 | P0 | pytest 门禁扩展 | Verify: 本地 pytest 全量通过。 | Gate: 测试不能依赖外部网络和真实凭证。 | Parallelizable: No
[ ] TP-08.02 | P0 | acceptance 脚本更新 | Verify: acceptance 本地通过。 | Gate: 导出包仍不包含 raw、大文件、缓存、日志。 | Parallelizable: No
[ ] TP-09.01 | P1 | README/SKILL 生产边界更新 | Verify: README/SKILL 与输出结构一致。 | Gate: 不夸大生产能力。 | Parallelizable: Yes
[ ] TP-09.02 | P1 | playbook 与架构文档更新 | Verify: 文档路径和职责边界一致。 | Gate: 架构调整必须更新 AGENTS.md。 | Parallelizable: Yes
[ ] TP-10.01 | P0 | 生成交付证据 | Verify: 交付证据 JSON 生成。 | Gate: 不得伪造 CI 或测试结果。 | Parallelizable: No
[ ] TP-10.02 | P0 | 任务 closeout | Verify: auto-tasks closeout 校验通过。 | Gate: 所有叶子项完成或明确延期。 | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
