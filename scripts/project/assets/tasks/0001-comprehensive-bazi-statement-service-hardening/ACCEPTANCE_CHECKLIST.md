# Acceptance Checklist

# Global Standards
- [ ] 不得引入真实非北京地区前端示例。
- [ ] 不得把民俗辅助、神煞、称骨提升为核心格局/喜忌权重。
- [ ] 不得把未来功能登记写成已生产。
- [ ] 不得让 raw、大文件、缓存、日志或用户输出进入导出包。

# Task Package Checklists
## TP-01
- 标题: 节气 golden 回归
- 验收项:
  - [ ] fixture 不直接依赖 raw 文件运行。
  - [ ] 边界测试覆盖 t-1s/t/t+1s。
  - [ ] 起运至少覆盖顺逆、性别、阴阳年样本。
- Verify: pytest 新增节气 golden、月令边界、立春年界、起运样本测试。
- Gate: 节气时间 schema、时区、容差和 fixture 来源全部明确。
- 输出物:
  - [ ] 解析 1900-2030 交节时间表，建立节气、月令、立春年界和起运边界回归。
- 标准清单:
  - [ ] Verify: pytest 新增节气 golden、月令边界、立春年界、起运样本测试。
  - [ ] Gate: 节气时间 schema、时区、容差和 fixture 来源全部明确。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-01.01
- 标题: 盘点交节时间 raw 表
- 验收项:
  - [ ] 达成 `盘点交节时间 raw 表` 的 objective，且输出物可复核
- Verify: 输出 schema 文档和来源哈希对照。
- Gate: 确认 raw 表不会进入导出包。
- 输出物:
  - [ ] 读取 CSV/XLS/XLSX 字段、年份覆盖、时区和精度，产出 normalized schema 设计。
- 标准清单:
  - [ ] Verify: 输出 schema 文档和来源哈希对照。
  - [ ] Gate: 确认 raw 表不会进入导出包。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-01.02
- 标题: 构建节气 golden fixture
- 验收项:
  - [ ] 达成 `构建节气 golden fixture` 的 objective，且输出物可复核
- Verify: fixture schema 校验和样本快照通过。
- Gate: 明确时区、容差、来源哈希。
- 输出物:
  - [ ] 从 raw 表抽取可提交的小型标准化 fixture 或可复现生成脚本。
- 标准清单:
  - [ ] Verify: fixture schema 校验和样本快照通过。
  - [ ] Gate: 明确时区、容差、来源哈希。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检
  - [ ] 维护 `DEBUG.md` 并保留回归证据

### TP-01.03
- 标题: 节气与月令边界测试
- 验收项:
  - [ ] 达成 `节气与月令边界测试` 的 objective，且输出物可复核
- Verify: pytest 对 `lunar-python` 计算结果与 fixture 进行边界断言。
- Gate: 任何误差必须有容差解释。
- 输出物:
  - [ ] 用 golden fixture 锁定节气时刻、月令切换、立春年界和真太阳时入参边界。
- 标准清单:
  - [ ] Verify: pytest 对 `lunar-python` 计算结果与 fixture 进行边界断言。
  - [ ] Gate: 任何误差必须有容差解释。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检
  - [ ] 维护 `DEBUG.md` 并保留回归证据

### TP-01.04
- 标题: 起运边界回归
- 验收项:
  - [ ] 达成 `起运边界回归` 的 objective，且输出物可复核
- Verify: pytest 覆盖起运顺逆样本。
- Gate: 起运样本来源和预期值必须可追溯。
- 输出物:
  - [ ] 建立 `yun.getStartSolar()` 样本回归，锁定起运年月日时分秒。
- 标准清单:
  - [ ] Verify: pytest 覆盖起运顺逆样本。
  - [ ] Gate: 起运样本来源和预期值必须可追溯。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检
  - [ ] 维护 `DEBUG.md` 并保留回归证据

## TP-02
- 标题: 综合八字输出结构锁定
- 验收项:
  - [ ] 达成 `综合八字输出结构锁定` 的 objective，且输出物可复核
- Verify: 报告结构快照测试通过。
- Gate: 默认输出目录与 profile 契约一致。
- 输出物:
  - [ ] 固定默认 Markdown 块，确保非综合八字体系不混入默认报告。
- 标准清单:
  - [ ] Verify: 报告结构快照测试通过。
  - [ ] Gate: 默认输出目录与 profile 契约一致。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-02.01
- 标题: 审计当前 report profile
- 验收项:
  - [ ] 达成 `审计当前 report profile` 的 objective，且输出物可复核
- Verify: 输出入口清单和默认块清单。
- Gate: 确认前端不应自行拼报告。
- 输出物:
  - [ ] 定位 Web/API/Bot 当前使用的报告 profile 和 Markdown 拼装入口。
- 标准清单:
  - [ ] Verify: 输出入口清单和默认块清单。
  - [ ] Gate: 确认前端不应自行拼报告。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-02.02
- 标题: 锁定综合八字默认块
- 验收项:
  - [ ] 达成 `锁定综合八字默认块` 的 objective，且输出物可复核
- Verify: 结构快照不含紫微、黄历、建除、六爻等块。
- Gate: 非八字体系统一保留为独立 capability 或未来登记。
- 输出物:
  - [ ] 将默认块限定为综合八字核心、动态运势、辅助解释、称骨民俗附录。
- 标准清单:
  - [ ] Verify: 结构快照不含紫微、黄历、建除、六爻等块。
  - [ ] Gate: 非八字体系统一保留为独立 capability 或未来登记。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-02.03
- 标题: 报告结构快照测试
- 验收项:
  - [ ] 达成 `报告结构快照测试` 的 objective，且输出物可复核
- Verify: pytest 快照测试通过。
- Gate: 快照只断言结构，不绑定易变大段文本。
- 输出物:
  - [ ] 新增 Markdown 结构快照和块可见性测试。
- 标准清单:
  - [ ] Verify: pytest 快照测试通过。
  - [ ] Gate: 快照只断言结构，不绑定易变大段文本。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-03
- 标题: 八字核心证据化
- 验收项:
  - [ ] 达成 `八字核心证据化` 的 objective，且输出物可复核
- Verify: 核心结论 evidence schema 测试通过。
- Gate: 证据字段来源必须可追溯，不编造典籍引用。
- 输出物:
  - [ ] 为日主、旺衰、调候、格局、用神、干支关系等核心结论补 evidence 字段。
- 标准清单:
  - [ ] Verify: 核心结论 evidence schema 测试通过。
  - [ ] Gate: 证据字段来源必须可追溯，不编造典籍引用。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-03.01
- 标题: 定义 evidence schema
- 验收项:
  - [ ] 达成 `定义 evidence schema` 的 objective，且输出物可复核
- Verify: schema 文档和测试 fixture 通过。
- Gate: 不改变现有公开输出，先兼容追加。
- 输出物:
  - [ ] 定义 source、basis、weight、visibility、risk、rule_id 等字段。
- 标准清单:
  - [ ] Verify: schema 文档和测试 fixture 通过。
  - [ ] Gate: 不改变现有公开输出，先兼容追加。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-03.02
- 标题: 核心结论 evidence mapper
- 验收项:
  - [ ] 达成 `核心结论 evidence mapper` 的 objective，且输出物可复核
- Verify: 单元测试覆盖至少日主、五行喜忌、格局、干支关系。
- Gate: 辅助体系不得提升为核心权重。
- 输出物:
  - [ ] 把月令、藏干、透干、五行、合冲刑害、调候、神煞、称骨映射为证据来源。
- 标准清单:
  - [ ] Verify: 单元测试覆盖至少日主、五行喜忌、格局、干支关系。
  - [ ] Gate: 辅助体系不得提升为核心权重。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-03.03
- 标题: 证据渲染与可见性
- 验收项:
  - [ ] 达成 `证据渲染与可见性` 的 objective，且输出物可复核
- Verify: Markdown/API 快照覆盖 evidence 可见性。
- Gate: 面向用户显示克制，审计字段保留可机读。
- 输出物:
  - [ ] 确定 evidence 在 API、Markdown、Web 中的默认显示/隐藏策略。
- 标准清单:
  - [ ] Verify: Markdown/API 快照覆盖 evidence 可见性。
  - [ ] Gate: 面向用户显示克制，审计字段保留可机读。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-04
- 标题: 权重与边界治理
- 验收项:
  - [ ] 达成 `权重与边界治理` 的 objective，且输出物可复核
- Verify: profile/registry 测试确认非八字体系统一默认关闭。
- Gate: 神煞、称骨不得参与核心格局和喜忌判断。
- 输出物:
  - [ ] 固定八字核心、动态运势、辅助体系、民俗附录的权重层级。
- 标准清单:
  - [ ] Verify: profile/registry 测试确认非八字体系统一默认关闭。
  - [ ] Gate: 神煞、称骨不得参与核心格局和喜忌判断。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-04.01
- 标题: 独立体系 capability 边界
- 验收项:
  - [ ] 达成 `独立体系 capability 边界` 的 objective，且输出物可复核
- Verify: registry/profile 文件与文档一致。
- Gate: 不得宣称未来功能已生产。
- 输出物:
  - [ ] 把紫微、黄历择日、占事、西方体系、铁板神数等声明为独立或未来 capability。
- 标准清单:
  - [ ] Verify: registry/profile 文件与文档一致。
  - [ ] Gate: 不得宣称未来功能已生产。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-04.02
- 标题: 权重策略测试
- 验收项:
  - [ ] 达成 `权重策略测试` 的 objective，且输出物可复核
- Verify: pytest 或静态配置测试通过。
- Gate: 称骨和神煞只作为辅助解释。
- 输出物:
  - [ ] 为核心/辅助/民俗权重边界添加测试和文档说明。
- 标准清单:
  - [ ] Verify: pytest 或静态配置测试通过。
  - [ ] Gate: 称骨和神煞只作为辅助解释。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-05
- 标题: 输入契约与隐私治理
- 验收项:
  - [ ] 达成 `输入契约与隐私治理` 的 objective，且输出物可复核
- Verify: 输入缺字段、地区脱敏、前端示例白名单测试通过。
- Gate: 不得在用户前端显示真实非北京地区样例。
- 输出物:
  - [ ] 加固姓名、性别、出生日期、时间、地区的必填/可选规则和隐私示例治理。
- 标准清单:
  - [ ] Verify: 输入缺字段、地区脱敏、前端示例白名单测试通过。
  - [ ] Gate: 不得在用户前端显示真实非北京地区样例。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-05.01
- 标题: 输入 schema 与错误响应
- 验收项:
  - [ ] 达成 `输入 schema 与错误响应` 的 objective，且输出物可复核
- Verify: API/Web/Bot 输入测试覆盖缺字段场景。
- Gate: 错误文案不泄露内部路径或真实样例。
- 输出物:
  - [ ] 明确缺字段、格式错误、地区解析失败的服务响应，不生成半残报告。
- 标准清单:
  - [ ] Verify: API/Web/Bot 输入测试覆盖缺字段场景。
  - [ ] Gate: 错误文案不泄露内部路径或真实样例。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-05.02
- 标题: 隐私与示例脱敏回归
- 验收项:
  - [ ] 达成 `隐私与示例脱敏回归` 的 objective，且输出物可复核
- Verify: `check-privacy-fixtures.sh` 与 pytest 脱敏测试通过。
- Gate: 新增 fixture 必须符合白名单。
- 输出物:
  - [ ] 统一北京/测试用户示例，禁止真实非北京地区进入前端样例和报告 fixture。
- 标准清单:
  - [ ] Verify: `check-privacy-fixtures.sh` 与 pytest 脱敏测试通过。
  - [ ] Gate: 新增 fixture 必须符合白名单。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检
  - [ ] 维护 `DEBUG.md` 并保留回归证据

## TP-06
- 标题: Web/API/Bot 同源输出
- 验收项:
  - [ ] 达成 `Web/API/Bot 同源输出` 的 objective，且输出物可复核
- Verify: Web/API/Bot smoke 和快照测试确认输出同源。
- Gate: 前端不得自行拼装报告块。
- 输出物:
  - [ ] 确保三端调用同一 report profile，Markdown 复制内容与 API 返回一致。
- 标准清单:
  - [ ] Verify: Web/API/Bot smoke 和快照测试确认输出同源。
  - [ ] Gate: 前端不得自行拼装报告块。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-06.01
- 标题: 报告 profile 单一真相源
- 验收项:
  - [ ] 达成 `报告 profile 单一真相源` 的 objective，且输出物可复核
- Verify: 三端入口测试指向同一 profile。
- Gate: 不引入第二套 Markdown 拼装逻辑。
- 输出物:
  - [ ] 收敛 Web、API、Bot 调用链路到同一 report profile 或同一 renderer。
- 标准清单:
  - [ ] Verify: 三端入口测试指向同一 profile。
  - [ ] Gate: 不引入第二套 Markdown 拼装逻辑。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-06.02
- 标题: Markdown 复制一致性
- 验收项:
  - [ ] 达成 `Markdown 复制一致性` 的 objective，且输出物可复核
- Verify: 复制内容结构快照测试通过。
- Gate: 按钮/控件不影响报告内容。
- 输出物:
  - [ ] 保证 Web 复制 Markdown 与 API/Bot 产物结构一致。
- 标准清单:
  - [ ] Verify: 复制内容结构快照测试通过。
  - [ ] Gate: 按钮/控件不影响报告内容。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-07
- 标题: 八字典籍引用层
- 验收项:
  - [ ] 达成 `八字典籍引用层` 的 objective，且输出物可复核
- Verify: 规则索引 schema、样本引用和版权边界测试通过。
- Gate: 不复制大段原文，不引用版权未复核资料。
- 输出物:
  - [ ] 从已整理典籍中提炼格局、调候、用神规则索引，支持结论可追溯。
- 标准清单:
  - [ ] Verify: 规则索引 schema、样本引用和版权边界测试通过。
  - [ ] Gate: 不复制大段原文，不引用版权未复核资料。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-07.01
- 标题: 典籍来源与版权边界审计
- 验收项:
  - [ ] 达成 `典籍来源与版权边界审计` 的 objective，且输出物可复核
- Verify: 来源表与可用范围文档完成。
- Gate: 版权不明资料只能作为 raw 复核来源。
- 输出物:
  - [ ] 盘点《渊海子平》《三命通会》《子平真诠》《滴天髓》《穷通宝鉴》可用文本与来源状态。
- 标准清单:
  - [ ] Verify: 来源表与可用范围文档完成。
  - [ ] Gate: 版权不明资料只能作为 raw 复核来源。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-07.02
- 标题: 小型规则索引种子
- 验收项:
  - [ ] 达成 `小型规则索引种子` 的 objective，且输出物可复核
- Verify: 规则索引 JSON/YAML schema 校验通过。
- Gate: 每条规则有来源、适用条件、禁用条件。
- 输出物:
  - [ ] 先提炼格局、调候、用神的结构化规则索引种子。
- 标准清单:
  - [ ] Verify: 规则索引 JSON/YAML schema 校验通过。
  - [ ] Gate: 每条规则有来源、适用条件、禁用条件。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-07.03
- 标题: 规则引用接入 evidence
- 验收项:
  - [ ] 达成 `规则引用接入 evidence` 的 objective，且输出物可复核
- Verify: evidence rule_id 与短依据测试通过。
- Gate: 规则引用是追溯层，不是新算法替换。
- 输出物:
  - [ ] 把可用规则索引接入 evidence，不改变核心算法判断。
- 标准清单:
  - [ ] Verify: evidence rule_id 与短依据测试通过。
  - [ ] Gate: 规则引用是追溯层，不是新算法替换。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-08
- 标题: 质量门禁加固
- 验收项:
  - [ ] 达成 `质量门禁加固` 的 objective，且输出物可复核
- Verify: `bash scripts/acceptance.sh --with-dev` 覆盖新增门禁并通过。
- Gate: 新增门禁失败时输出可定位原因。
- 输出物:
  - [ ] 把新增回归测试、隐私测试、结构测试和导出包卫生纳入 acceptance。
- 标准清单:
  - [ ] Verify: `bash scripts/acceptance.sh --with-dev` 覆盖新增门禁并通过。
  - [ ] Gate: 新增门禁失败时输出可定位原因。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-08.01
- 标题: pytest 门禁扩展
- 验收项:
  - [ ] 达成 `pytest 门禁扩展` 的 objective，且输出物可复核
- Verify: 本地 pytest 全量通过。
- Gate: 测试不能依赖外部网络和真实凭证。
- 输出物:
  - [ ] 把节气、起运、报告结构、隐私、同源输出测试纳入现有 pytest 目录。
- 标准清单:
  - [ ] Verify: 本地 pytest 全量通过。
  - [ ] Gate: 测试不能依赖外部网络和真实凭证。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-08.02
- 标题: acceptance 脚本更新
- 验收项:
  - [ ] 达成 `acceptance 脚本更新` 的 objective，且输出物可复核
- Verify: acceptance 本地通过。
- Gate: 导出包仍不包含 raw、大文件、缓存、日志。
- 输出物:
  - [ ] 必要时更新 acceptance/preflight，确保新增门禁在本地和 CI 运行。
- 标准清单:
  - [ ] Verify: acceptance 本地通过。
  - [ ] Gate: 导出包仍不包含 raw、大文件、缓存、日志。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-09
- 标题: 服务化文档同步
- 验收项:
  - [ ] 达成 `服务化文档同步` 的 objective，且输出物可复核
- Verify: 文档口径与 profile/registry 一致。
- Gate: 不得把未来能力写成已实现。
- 输出物:
  - [ ] 更新 README、SKILL、execution playbook 和架构文档，明确当前生产边界。
- 标准清单:
  - [ ] Verify: 文档口径与 profile/registry 一致。
  - [ ] Gate: 不得把未来能力写成已实现。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-09.01
- 标题: README/SKILL 生产边界更新
- 验收项:
  - [ ] 达成 `README/SKILL 生产边界更新` 的 objective，且输出物可复核
- Verify: README/SKILL 与输出结构一致。
- Gate: 不夸大生产能力。
- 输出物:
  - [ ] 明确当前生产服务只支持综合八字默认报告，其他体系为独立或未来 capability。
- 标准清单:
  - [ ] Verify: README/SKILL 与输出结构一致。
  - [ ] Gate: 不夸大生产能力。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-09.02
- 标题: playbook 与架构文档更新
- 验收项:
  - [ ] 达成 `playbook 与架构文档更新` 的 objective，且输出物可复核
- Verify: 文档路径和职责边界一致。
- Gate: 架构调整必须更新 AGENTS.md。
- 输出物:
  - [ ] 同步 execution playbook、AGENTS.md 和相关架构文档。
- 标准清单:
  - [ ] Verify: 文档路径和职责边界一致。
  - [ ] Gate: 架构调整必须更新 AGENTS.md。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-10
- 标题: 交付控制与 closeout
- 验收项:
  - [ ] 达成 `交付控制与 closeout` 的 objective，且输出物可复核
- Verify: Git status clean、CI 通过、Task Closeout Packet 生成。
- Gate: 无 blocker，无未提交实现改动。
- 输出物:
  - [ ] 完成版本控制、推送、CI、任务 closeout 和交付证据归档。
- 标准清单:
  - [ ] Verify: Git status clean、CI 通过、Task Closeout Packet 生成。
  - [ ] Gate: 无 blocker，无未提交实现改动。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-10.01
- 标题: 生成交付证据
- 验收项:
  - [ ] 达成 `生成交付证据` 的 objective，且输出物可复核
- Verify: 交付证据 JSON 生成。
- Gate: 不得伪造 CI 或测试结果。
- 输出物:
  - [ ] 捕获 git delivery evidence、验证命令结果和剩余风险。
- 标准清单:
  - [ ] Verify: 交付证据 JSON 生成。
  - [ ] Gate: 不得伪造 CI 或测试结果。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

### TP-10.02
- 标题: 任务 closeout
- 验收项:
  - [ ] 达成 `任务 closeout` 的 objective，且输出物可复核
- Verify: auto-tasks closeout 校验通过。
- Gate: 所有叶子项完成或明确延期。
- 输出物:
  - [ ] 完成 TODO/STATUS，生成 Task Closeout Packet 并沉淀后续事项。
- 标准清单:
  - [ ] Verify: auto-tasks closeout 校验通过。
  - [ ] Gate: 所有叶子项完成或明确延期。
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检
