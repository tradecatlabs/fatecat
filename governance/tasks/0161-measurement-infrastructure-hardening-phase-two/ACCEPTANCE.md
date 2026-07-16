# Task-Level Acceptance
- 公开报告只包含允许字段，机器规则 ID、provider/source 编码和内部调试元数据不能泄露，但结构化证据仍可查询
- 冷启动 benchmark 有可重复命令，完整报告语义和输出规模不变，性能相对基线获得可测收益
- 独立 fixture/benchmark 与引擎自生成 golden 明确分级，缺少外部专家签字时不能输出已认证结论
- capability registry、schema、executor 和 API 对成熟度与可执行性的判断一致
- 异步任务 metrics 能区分排队、执行、成功、失败、过期和结果大小
- 公开客户端包不包含受限运行时资产，受限服务端包继续被 release gate 阻止
- quick CI、定向性能/契约测试、治理 strict、任务 closeout 和最终 review 通过，工作树干净
- approved plan 已成功编译为递归任务树
- 叶子节点数量: 8
- 当前可立即执行叶子节点: TP-01

# Validation Plan
- 多样本公开 Markdown 泄露扫描和结构化证据保留测试
- 冷进程与热进程 benchmark、输出语义等价和完整月份计数测试
- 独立准确性 runner 的 schema、来源、重复执行和失败门禁测试
- capability registry/schema/executor/API 契约测试
- 异步任务状态与 Prometheus metrics 测试
- 公开客户端 clean-room install/smoke 和受限资产缺失证明
- bash scripts/local-ci.sh --profile quick 与治理/任务 strict 校验
- bugfix / regression / flaky 任务必须把 DEBUG.md 的回归证据串到 Recent Evidence
- TP-01 | Verify: 公开报告契约测试与多样本回归通过 | Gate: 公开输出只含允许字段，结构化证据无损
- TP-02 | Verify: 冷/热 benchmark 与结果等价测试 | Gate: 月份数量和语义完全一致，冷启动获得稳定收益
- TP-03 | Verify: 独立 runner schema/source/failure tests | Gate: 不能用自产 fixture 通过独立门禁，缺专家证据时状态明确 pending
- TP-04 | Verify: registry schema 与 executor/API 契约测试 | Gate: planned 拒绝执行，validated 不再被误报 production
- TP-05 | Verify: 行为快照、复杂度检查和定向回归 | Gate: 职责边界清晰，未新增无消费者抽象
- TP-06 | Verify: report job lifecycle metrics tests 与 /metrics smoke | Gate: 固定低基数标签覆盖全部终态
- TP-07 | Verify: clean-room install/smoke + archive content inspection + restricted gate negative test | Gate: 公开闭包无未知许可证资产且仍可调用生产 API
- TP-08 | Verify: quick CI + governance/task strict + auto-review + git status | Gate: 无 BLOCK、无未解释失败、无未提交文件

# Review Gate
- 不触碰第 1 项专业断语
- 完整报告输出范围不变且核心结果无差异
- 所有公开字段、生命周期、指标和分发边界具有机器契约
- 没有以兼容焦虑保留永久双轨或以自洽测试冒充独立证明

# Runtime Verification Gate
- [x] 每个 tool/action 结果都有可回指证据或明确未执行原因。
- [x] 高风险动作没有由 worker/agent 自我批准；审批状态可追踪。
- [x] compaction / resume 后目标、计划、修改文件、审批状态和验证项未丢失。
- [x] verifier / 自审已检查关键发现是否有证据支持。
- [x] closeout 明确 coverage gaps、failed packets 和 unresolved questions。
- [x] TP-01: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [x] TP-02: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [x] TP-03: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [x] TP-04: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [x] TP-05: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [x] TP-06: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [x] TP-07: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [x] TP-08: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据

# Ship Readiness
- 所有本地门禁和任务 closeout 通过后形成语义提交
- 远端 CI/生产部署若未由用户要求则不伪造完成状态
- 人类专家和外部 live 继续列为待执行

# Task Package Acceptance
## TP-01
- 标题: 建立公开报告字段允许契约
- 验收标准:
  - 机器标识不出现在 Markdown
  - 用户字段不被误删
  - 结构化 evidence 保留
- Verify: 公开报告契约测试与多样本回归通过
- Gate: 公开输出只含允许字段，结构化证据无损
- 输出物: 公开字段契约；投影/验证薄层；泄露回归测试

## TP-02
- 标题: 优化完整八字冷启动热路径
- 验收标准:
  - 不减少数据范围
  - 不手写新的历法算法
  - 性能证据可重复
- Verify: 冷/热 benchmark 与结果等价测试
- Gate: 月份数量和语义完全一致，冷启动获得稳定收益
- 输出物: 热路径优化；benchmark；等价回归

## TP-03
- 标题: 建立独立准确性评测入口
- 验收标准:
  - 来源和 hash 可追溯
  - 失败退出码可靠
  - 不宣称专家认证
- Verify: 独立 runner schema/source/failure tests
- Gate: 不能用自产 fixture 通过独立门禁，缺专家证据时状态明确 pending
- 输出物: 独立评测 runner；fixture manifest；可选 acceptance gate

## TP-04
- 标题: 统一 capability 生命周期语义
- 验收标准:
  - 无永久双状态真相源
  - 公共兼容边界明确
- Verify: registry schema 与 executor/API 契约测试
- Gate: planned 拒绝执行，validated 不再被误报 production
- 输出物: 统一 registry 字段；迁移契约；一致性测试

## TP-05
- 标题: 收敛核心与报告职责复杂度
- 验收标准:
  - 超长函数显著收缩
  - 无双轨计算
  - 输出一致
- Verify: 行为快照、复杂度检查和定向回归
- Gate: 职责边界清晰，未新增无消费者抽象
- 输出物: 小职责 helper/模块；行为保持测试；AGENTS/module context 同步

## TP-06
- 标题: 补齐异步报告端到端指标
- 验收标准:
  - 可计算 queue/runtime p95
  - 失败/过期可见
  - 无 PII 标签
- Verify: report job lifecycle metrics tests 与 /metrics smoke
- Gate: 固定低基数标签覆盖全部终态
- 输出物: job metrics；observability contract；回归测试

## TP-07
- 标题: 建立许可证安全的公开客户端闭包
- 验收标准:
  - unknown license 不被改写
  - 客户端无服务端隐式 import
  - 可独立安装
- Verify: clean-room install/smoke + archive content inspection + restricted gate negative test
- Gate: 公开闭包无未知许可证资产且仍可调用生产 API
- 输出物: 公开客户端包；distribution manifest；许可证门禁测试

## TP-08
- 标题: 全量验证、审查与仓库卫生收口
- 验收标准:
  - 第 1 项保持外部待审
  - 本地证据完整
  - 文档与实现一致
- Verify: quick CI + governance/task strict + auto-review + git status
- Gate: 无 BLOCK、无未解释失败、无未提交文件
- 输出物: REVIEW；closeout packet；语义提交；干净工作树

# Anti-Goals
- 不得修改任务范围之外的专业断语、新预测体系或 Web 视觉设计
- 不得虚构证据
- 不得越权补全未确认信息
