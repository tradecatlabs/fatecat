# Task-Level Acceptance
- wheel 在仓库外干净虚拟环境中安装并执行 CLI smoke
- lite skill 导出不包含运行态导出、无关媒体或禁止分发 reference assets，并满足体积/文件数预算
- Web/API/Bot 的综合八字生产路径均通过 capability executor
- Telegram 未就绪不再误判核心 Web/API 不可用，重试有界退避且错误类型可观测
- quick CI 自动覆盖 pull_request 与 main push，重型发布流程保持明确触发边界
- vendor 测试后无 pycache 污染，供应链分发策略可机械检查
- 治理 strict、任务 closeout、quick CI 和任务级 review 通过
- approved plan 已成功编译为递归任务树
- 叶子节点数量: 7
- 当前可立即执行叶子节点: 无；TP-04 与 TP-07 正在执行 Git/CI/closeout。

# Validation Plan
- 仓库外 wheel install smoke
- lite export hygiene/smoke/size gate
- 八字入口语义一致性回归
- Telegram readiness/retry 单元与集成回归
- workflow schema/trigger 回归
- vendor before/after pollution gate
- bash scripts/local-ci.sh --profile quick
- governance strict 与任务 closeout 校验
- TP-01 | Verify: wheel clean-room smoke + export runtime smoke + size/file-count gate | Gate: 独立安装和精简导出全部通过
- TP-02 | Verify: Web/API/Bot normalized semantic parity tests | Gate: 不存在默认 legacy 生产路径
- TP-03 | Verify: Telegram lifecycle/readiness/metrics tests | Gate: 核心 API 可用且渠道故障明确可见
- TP-04 | Verify: workflow regression + action syntax + current release proof | Gate: 最终提交拥有真实远端 quick CI 证据
- TP-05 | Verify: vendor health before/after tests + distribution policy gate | Gate: reference repo 只读且禁止资产不进入发行物
- TP-06 | Verify: governance context bundle + strict validation + document drift review | Gate: 治理路由不再 BLOCK 且事实与实现一致
- TP-07 | Verify: quick CI + performance baseline + task review + closeout + remote CI | Gate: 本地实现无 BLOCK；外部人工/live 门禁真实保留

# Review Gate
- 分发闭包不依赖源码仓库路径
- 核心计算不存在双生产引擎
- 渠道降级不掩盖故障也不拖垮核心 readiness
- 发布声明只引用当前 commit 的真实证据

# Runtime Verification Gate
- [ ] 每个 tool/action 结果都有可回指证据或明确未执行原因。
- [ ] 高风险动作没有由 worker/agent 自我批准；审批状态可追踪。
- [ ] compaction / resume 后目标、计划、修改文件、审批状态和验证项未丢失。
- [ ] verifier / 自审已检查关键发现是否有证据支持。
- [ ] closeout 明确 coverage gaps、failed packets 和 unresolved questions。
- [ ] TP-01: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [ ] TP-02: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [ ] TP-03: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [ ] TP-04: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [ ] TP-05: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [ ] TP-06: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [ ] TP-07: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据

# Ship Readiness
- 本地所有门禁必须通过后才提交
- 远端 quick CI 必须对应最终提交
- 外部 live 和人工专业审核保持 pending/blocked，除非真实证据到位

# Task Package Acceptance
## TP-01
- 标题: 建立可独立分发闭包
- 验收标准:
  - CLI 不再依赖企业仓库根
  - 导出包不含 infra/runtime/local-state
  - 包预算可机械验证
- Verify: wheel clean-room smoke + export runtime smoke + size/file-count gate
- Gate: 独立安装和精简导出全部通过
- 输出物: 包内资源闭包；allowlist/明确分发清单；分发回归测试

## TP-02
- 标题: 统一综合八字生产引擎
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: Web/API/Bot normalized semantic parity tests
- Gate: 不存在默认 legacy 生产路径
- 输出物: 单引擎编排；弃用契约；语义一致性测试

## TP-03
- 标题: 隔离 Telegram 渠道就绪状态
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: Telegram lifecycle/readiness/metrics tests
- Gate: 核心 API 可用且渠道故障明确可见
- 输出物: 分层 readiness；指数退避；错误观测与回归测试

## TP-04
- 标题: 补齐自动 CI 与发布证明
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: workflow regression + action syntax + current release proof
- Gate: 最终提交拥有真实远端 quick CI 证据
- 输出物: 自动 quick workflow；受控 release workflow；当前提交证据

## TP-05
- 标题: 加固供应链与 vendor 卫生
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: vendor health before/after tests + distribution policy gate
- Gate: reference repo 只读且禁止资产不进入发行物
- 输出物: pycache 防污染；分发策略门禁；供应链证据

## TP-06
- 标题: 恢复治理真相源
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: governance context bundle + strict validation + document drift review
- Gate: 治理路由不再 BLOCK 且事实与实现一致
- 输出物: 评审标准；module contexts；事实文档和任务状态同步

## TP-07
- 标题: 性能、质量与交付收口
- 验收标准:
  - 达成当前节点 objective，且输出物可复核
- Verify: quick CI + performance baseline + task review + closeout + remote CI
- Gate: 本地实现无 BLOCK；外部人工/live 门禁真实保留
- 输出物: 性能基线；审查结论；提交推送与远端证据

# Anti-Goals
- 不得修改 `governance/tasks/` 以外路径
- 不得虚构证据
- 不得越权补全未确认信息
