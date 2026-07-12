# Acceptance Checklist

# Global Standards
- [ ] 不以本地证据替代外部 live 或人工专业审核
- [ ] planned capability 继续拒绝执行
- [ ] 不泄露 token、secret、DSN、用户出生资料或完整报告正文
- [ ] 不保留 legacy/capability 双轨生产行为

# Task Package Checklists
## TP-01
- 标题: 建立可独立分发闭包
- 验收项:
  - [ ] CLI 不再依赖企业仓库根
  - [ ] 导出包不含 infra/runtime/local-state
  - [ ] 包预算可机械验证
- Verify: wheel clean-room smoke + export runtime smoke + size/file-count gate
- Gate: 独立安装和精简导出全部通过
- 输出物:
  - [ ] 包内资源闭包
  - [ ] allowlist/明确分发清单
  - [ ] 分发回归测试
- 标准清单:
  - [ ] Verify: wheel clean-room smoke + export runtime smoke + size/file-count gate
  - [ ] Gate: 独立安装和精简导出全部通过
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-02
- 标题: 统一综合八字生产引擎
- 验收项:
  - [ ] 达成 `统一综合八字生产引擎` 的 objective，且输出物可复核
- Verify: Web/API/Bot normalized semantic parity tests
- Gate: 不存在默认 legacy 生产路径
- 输出物:
  - [ ] 单引擎编排
  - [ ] 弃用契约
  - [ ] 语义一致性测试
- 标准清单:
  - [ ] Verify: Web/API/Bot normalized semantic parity tests
  - [ ] Gate: 不存在默认 legacy 生产路径
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-03
- 标题: 隔离 Telegram 渠道就绪状态
- 验收项:
  - [ ] 达成 `隔离 Telegram 渠道就绪状态` 的 objective，且输出物可复核
- Verify: Telegram lifecycle/readiness/metrics tests
- Gate: 核心 API 可用且渠道故障明确可见
- 输出物:
  - [ ] 分层 readiness
  - [ ] 指数退避
  - [ ] 错误观测与回归测试
- 标准清单:
  - [ ] Verify: Telegram lifecycle/readiness/metrics tests
  - [ ] Gate: 核心 API 可用且渠道故障明确可见
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-04
- 标题: 补齐自动 CI 与发布证明
- 验收项:
  - [ ] 达成 `补齐自动 CI 与发布证明` 的 objective，且输出物可复核
- Verify: workflow regression + action syntax + current release proof
- Gate: 最终提交拥有真实远端 quick CI 证据
- 输出物:
  - [ ] 自动 quick workflow
  - [ ] 受控 release workflow
  - [ ] 当前提交证据
- 标准清单:
  - [ ] Verify: workflow regression + action syntax + current release proof
  - [ ] Gate: 最终提交拥有真实远端 quick CI 证据
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-05
- 标题: 加固供应链与 vendor 卫生
- 验收项:
  - [ ] 达成 `加固供应链与 vendor 卫生` 的 objective，且输出物可复核
- Verify: vendor health before/after tests + distribution policy gate
- Gate: reference repo 只读且禁止资产不进入发行物
- 输出物:
  - [ ] pycache 防污染
  - [ ] 分发策略门禁
  - [ ] 供应链证据
- 标准清单:
  - [ ] Verify: vendor health before/after tests + distribution policy gate
  - [ ] Gate: reference repo 只读且禁止资产不进入发行物
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-06
- 标题: 恢复治理真相源
- 验收项:
  - [ ] 达成 `恢复治理真相源` 的 objective，且输出物可复核
- Verify: governance context bundle + strict validation + document drift review
- Gate: 治理路由不再 BLOCK 且事实与实现一致
- 输出物:
  - [ ] 评审标准
  - [ ] module contexts
  - [ ] 事实文档和任务状态同步
- 标准清单:
  - [ ] Verify: governance context bundle + strict validation + document drift review
  - [ ] Gate: 治理路由不再 BLOCK 且事实与实现一致
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检

## TP-07
- 标题: 性能、质量与交付收口
- 验收项:
  - [ ] 达成 `性能、质量与交付收口` 的 objective，且输出物可复核
- Verify: quick CI + performance baseline + task review + closeout + remote CI
- Gate: 本地实现无 BLOCK；外部人工/live 门禁真实保留
- 输出物:
  - [ ] 性能基线
  - [ ] 审查结论
  - [ ] 提交推送与远端证据
- 标准清单:
  - [ ] Verify: quick CI + performance baseline + task review + closeout + remote CI
  - [ ] Gate: 本地实现无 BLOCK；外部人工/live 门禁真实保留
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检
