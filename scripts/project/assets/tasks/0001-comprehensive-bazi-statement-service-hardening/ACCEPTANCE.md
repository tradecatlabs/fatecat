# Task-Level Acceptance
- 综合八字默认报告结构有快照测试，非八字体系统一不可进入默认输出。
- 节气/月令/立春/起运边界有可复现 regression 测试，并进入 acceptance 门禁。
- 核心八字结论包含可机读 evidence，且权重边界明确。
- Web、API、Bot 输出来自同一 report profile，复制 Markdown 与 API 返回一致。
- 隐私示例、脱敏规则、文档口径和 README/SKILL/playbook 完成同步。
- approved plan 已成功编译为递归任务树
- 叶子节点数量: 25
- 当前可立即执行叶子节点: TP-01.01, TP-02.01

# Validation Plan
- 运行新增 pytest：节气 golden、报告结构快照、隐私脱敏、输入契约、多端同源输出。
- 运行 `bash scripts/vendor-health.sh`、`bash scripts/check-source-hygiene.sh`、`bash scripts/check-privacy-fixtures.sh`。
- 运行 `bash scripts/acceptance.sh --with-dev`，确认导出包卫生与导出包 smoke 仍通过。
- 在任务执行完成后生成本地 Git Delivery Evidence；实时工作树快照不作为入库真相源，最终交付以 clean worktree、commit hash、acceptance 与 push 后 CI 为准。
- bugfix / regression / flaky 任务必须把 DEBUG.md 的回归证据串到 Recent Evidence
- TP-01.01 | Verify: 输出 schema 文档和来源哈希对照。 | Gate: 确认 raw 表不会进入导出包。
- TP-01.02 | Verify: fixture schema 校验和样本快照通过。 | Gate: 明确时区、容差、来源哈希。
- TP-01.03 | Verify: pytest 对 `lunar-python` 计算结果与 fixture 进行容差断言，并对抽样年份做 fixture 边界断言。 | Gate: 任何误差必须有容差解释。
- TP-01.04 | Verify: pytest 覆盖起运顺逆样本。 | Gate: 起运样本来源和预期值必须可追溯。
- TP-02.01 | Verify: 输出入口清单和默认块清单。 | Gate: 确认前端不应自行拼报告。
- TP-02.02 | Verify: 结构快照不含紫微、黄历、建除、六爻等块。 | Gate: 非八字体系统一保留为独立 capability 或未来登记。
- TP-02.03 | Verify: pytest 快照测试通过。 | Gate: 快照只断言结构，不绑定易变大段文本。
- TP-03.01 | Verify: schema 文档和测试 fixture 通过。 | Gate: 不改变现有公开输出，先兼容追加。
- TP-03.02 | Verify: 单元测试覆盖至少日主、五行喜忌、格局、干支关系。 | Gate: 辅助体系不得提升为核心权重。
- TP-03.03 | Verify: Markdown/API 快照覆盖 evidence 可见性。 | Gate: 面向用户显示克制，审计字段保留可机读。
- TP-04.01 | Verify: registry/profile 文件与文档一致。 | Gate: 不得宣称未来功能已生产。
- TP-04.02 | Verify: pytest 或静态配置测试通过。 | Gate: 称骨和神煞只作为辅助解释。
- TP-05.01 | Verify: API/Web/Bot 输入测试覆盖缺字段场景。 | Gate: 错误文案不泄露内部路径或真实样例。
- TP-05.02 | Verify: `check-privacy-fixtures.sh` 与 pytest 脱敏测试通过。 | Gate: 新增 fixture 必须符合白名单。
- TP-06.01 | Verify: 三端入口测试指向同一 profile。 | Gate: 不引入第二套 Markdown 拼装逻辑。
- TP-06.02 | Verify: 复制内容结构快照测试通过。 | Gate: 按钮/控件不影响报告内容。
- TP-07.01 | Verify: 来源表与可用范围文档完成。 | Gate: 版权不明资料只能作为 raw 复核来源。
- TP-07.02 | Verify: 规则索引 JSON/YAML schema 校验通过。 | Gate: 每条规则有来源、适用条件、禁用条件。
- TP-07.03 | Verify: evidence rule_id 与短依据测试通过。 | Gate: 规则引用是追溯层，不是新算法替换。
- TP-08.01 | Verify: 本地 pytest 全量通过。 | Gate: 测试不能依赖外部网络和真实凭证。
- TP-08.02 | Verify: acceptance 本地通过。 | Gate: 导出包仍不包含 raw、大文件、缓存、日志。
- TP-09.01 | Verify: README/SKILL 与输出结构一致。 | Gate: 不夸大生产能力。
- TP-09.02 | Verify: 文档路径和职责边界一致。 | Gate: 架构调整必须更新 AGENTS.md。
- TP-10.01 | Verify: 交付证据 JSON 生成。 | Gate: 不得伪造 CI 或测试结果。
- TP-10.02 | Verify: auto-tasks closeout 校验通过。 | Gate: 所有叶子项完成或明确延期。

# Review Gate
- 默认报告不得混入紫微、黄历、六爻、梅花、奇门、大六壬、西方占星、塔罗、铁板神数。
- 每个新增测试必须有失败时能定位的断言与 fixture 来源。
- 每个证据字段必须可追溯到已有计算结果、规则索引或明确辅助体系。

# Ship Readiness
- `bash scripts/acceptance.sh --with-dev` 通过。
- GitHub Actions 通过。
- 任务 TODO 全部完成，STATUS 无 blocker。
- README/SKILL/playbook 与当前生产能力边界一致。

# Task Package Acceptance
## TP-01
- 标题: 节气 golden 回归
- 验收标准:
  - fixture 不直接依赖 raw 文件运行。
  - 边界测试覆盖 fixture t-1s 与 fixture 容差窗口后的柱切换。
  - 起运至少覆盖顺逆、性别、阴阳年样本。
- Verify: pytest 新增节气 golden、月令边界、立春年界、起运样本测试。
- Gate: 节气时间 schema、时区、容差和 fixture 来源全部明确。
- 输出物: 无

### TP-01.01
- 标题: 盘点交节时间 raw 表
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 输出 schema 文档和来源哈希对照。
- Gate: 确认 raw 表不会进入导出包。
- 输出物: 无

### TP-01.02
- 标题: 构建节气 golden fixture
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: fixture schema 校验和样本快照通过。
- Gate: 明确时区、容差、来源哈希。
- 输出物: 无

### TP-01.03
- 标题: 节气与月令边界测试
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: pytest 对 `lunar-python` 计算结果与 fixture 进行容差断言，并对抽样年份做 fixture 边界断言。
- Gate: 任何误差必须有容差解释。
- 输出物: 无

### TP-01.04
- 标题: 起运边界回归
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: pytest 覆盖起运顺逆样本。
- Gate: 起运样本来源和预期值必须可追溯。
- 输出物: 无

## TP-02
- 标题: 综合八字输出结构锁定
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 报告结构快照测试通过。
- Gate: 默认输出目录与 profile 契约一致。
- 输出物: 无

### TP-02.01
- 标题: 审计当前 report profile
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 输出入口清单和默认块清单。
- Gate: 确认前端不应自行拼报告。
- 输出物: 无

### TP-02.02
- 标题: 锁定综合八字默认块
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 结构快照不含紫微、黄历、建除、六爻等块。
- Gate: 非八字体系统一保留为独立 capability 或未来登记。
- 输出物: 无

### TP-02.03
- 标题: 报告结构快照测试
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: pytest 快照测试通过。
- Gate: 快照只断言结构，不绑定易变大段文本。
- 输出物: 无

## TP-03
- 标题: 八字核心证据化
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 核心结论 evidence schema 测试通过。
- Gate: 证据字段来源必须可追溯，不编造典籍引用。
- 输出物: 无

### TP-03.01
- 标题: 定义 evidence schema
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: schema 文档和测试 fixture 通过。
- Gate: 不改变现有公开输出，先兼容追加。
- 输出物: 无

### TP-03.02
- 标题: 核心结论 evidence mapper
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 单元测试覆盖至少日主、五行喜忌、格局、干支关系。
- Gate: 辅助体系不得提升为核心权重。
- 输出物: 无

### TP-03.03
- 标题: 证据渲染与可见性
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: Markdown/API 快照覆盖 evidence 可见性。
- Gate: 面向用户显示克制，审计字段保留可机读。
- 输出物: 无

## TP-04
- 标题: 权重与边界治理
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: profile/registry 测试确认非八字体系统一默认关闭。
- Gate: 神煞、称骨不得参与核心格局和喜忌判断。
- 输出物: 无

### TP-04.01
- 标题: 独立体系 capability 边界
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: registry/profile 文件与文档一致。
- Gate: 不得宣称未来功能已生产。
- 输出物: 无

### TP-04.02
- 标题: 权重策略测试
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: pytest 或静态配置测试通过。
- Gate: 称骨和神煞只作为辅助解释。
- 输出物: 无

## TP-05
- 标题: 输入契约与隐私治理
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 输入缺字段、地区脱敏、前端示例白名单测试通过。
- Gate: 不得在用户前端显示真实非北京地区样例。
- 输出物: 无

### TP-05.01
- 标题: 输入 schema 与错误响应
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: API/Web/Bot 输入测试覆盖缺字段场景。
- Gate: 错误文案不泄露内部路径或真实样例。
- 输出物: 无

### TP-05.02
- 标题: 隐私与示例脱敏回归
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: `check-privacy-fixtures.sh` 与 pytest 脱敏测试通过。
- Gate: 新增 fixture 必须符合白名单。
- 输出物: 无

## TP-06
- 标题: Web/API/Bot 同源输出
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: Web/API/Bot smoke 和快照测试确认输出同源。
- Gate: 前端不得自行拼装报告块。
- 输出物: 无

### TP-06.01
- 标题: 报告 profile 单一真相源
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 三端入口测试指向同一 profile。
- Gate: 不引入第二套 Markdown 拼装逻辑。
- 输出物: 无

### TP-06.02
- 标题: Markdown 复制一致性
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 复制内容结构快照测试通过。
- Gate: 按钮/控件不影响报告内容。
- 输出物: 无

## TP-07
- 标题: 八字典籍引用层
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 规则索引 schema、样本引用和版权边界测试通过。
- Gate: 不复制大段原文，不引用版权未复核资料。
- 输出物: 无

### TP-07.01
- 标题: 典籍来源与版权边界审计
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 来源表与可用范围文档完成。
- Gate: 版权不明资料只能作为 raw 复核来源。
- 输出物: 无

### TP-07.02
- 标题: 小型规则索引种子
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 规则索引 JSON/YAML schema 校验通过。
- Gate: 每条规则有来源、适用条件、禁用条件。
- 输出物: 无

### TP-07.03
- 标题: 规则引用接入 evidence
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: evidence rule_id 与短依据测试通过。
- Gate: 规则引用是追溯层，不是新算法替换。
- 输出物: 无

## TP-08
- 标题: 质量门禁加固
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: `bash scripts/acceptance.sh --with-dev` 覆盖新增门禁并通过。
- Gate: 新增门禁失败时输出可定位原因。
- 输出物: 无

### TP-08.01
- 标题: pytest 门禁扩展
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 本地 pytest 全量通过。
- Gate: 测试不能依赖外部网络和真实凭证。
- 输出物: 无

### TP-08.02
- 标题: acceptance 脚本更新
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: acceptance 本地通过。
- Gate: 导出包仍不包含 raw、大文件、缓存、日志。
- 输出物: 无

## TP-09
- 标题: 服务化文档同步
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 文档口径与 profile/registry 一致。
- Gate: 不得把未来能力写成已实现。
- 输出物: 无

### TP-09.01
- 标题: README/SKILL 生产边界更新
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: README/SKILL 与输出结构一致。
- Gate: 不夸大生产能力。
- 输出物: 无

### TP-09.02
- 标题: playbook 与架构文档更新
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 文档路径和职责边界一致。
- Gate: 架构调整必须更新 AGENTS.md。
- 输出物: 无

## TP-10
- 标题: 交付控制与 closeout
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: Git status clean、CI 通过、Task Closeout Packet 生成。
- Gate: 无 blocker，无未提交实现改动。
- 输出物: 无

### TP-10.01
- 标题: 生成交付证据
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: 交付证据 JSON 生成。
- Gate: 不得伪造 CI 或测试结果。
- 输出物: 无

### TP-10.02
- 标题: 任务 closeout
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: auto-tasks closeout 校验通过。
- Gate: 所有叶子项完成或明确延期。
- 输出物: 无

# Anti-Goals
- 不得修改 `assets/tasks/` 以外路径
- 不得虚构证据
- 不得越权补全未确认信息
