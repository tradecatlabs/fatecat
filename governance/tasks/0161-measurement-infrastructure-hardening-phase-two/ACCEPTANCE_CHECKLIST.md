# Acceptance Checklist

# Global Standards
- [x] 所有结论来自真实命令和文件证据，不伪造外部专家、生产或许可证结论
- [x] 公共 API 兼容性、完整报告输出、隐私边界和确定性计算不能因优化退化
- [x] 新增模块必须有单一职责和直接消费者，不建立通用框架或双轨真相源
- [x] 性能结论必须区分冷启动、热路径和渲染耗时，并记录硬件与样本

# Task Package Checklists
## TP-01
- 标题: 建立公开报告字段允许契约
- 验收项:
  - [x] 机器标识不出现在 Markdown
  - [x] 用户字段不被误删
  - [x] 结构化 evidence 保留
- Verify: 公开报告契约测试与多样本回归通过
- Gate: 公开输出只含允许字段，结构化证据无损
- 输出物:
  - [x] 公开字段契约
  - [x] 投影/验证薄层
  - [x] 泄露回归测试
- 标准清单:
  - [x] Verify: 公开报告契约测试与多样本回归通过
  - [x] Gate: 公开输出只含允许字段，结构化证据无损
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-02
- 标题: 优化完整八字冷启动热路径
- 验收项:
  - [x] 不减少数据范围
  - [x] 不手写新的历法算法
  - [x] 性能证据可重复
- Verify: 冷/热 benchmark 与结果等价测试
- Gate: 月份数量和语义完全一致，冷启动获得稳定收益
- 输出物:
  - [x] 热路径优化
  - [x] benchmark
  - [x] 等价回归
- 标准清单:
  - [x] Verify: 冷/热 benchmark 与结果等价测试
  - [x] Gate: 月份数量和语义完全一致，冷启动获得稳定收益
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-03
- 标题: 建立独立准确性评测入口
- 验收项:
  - [x] 来源和 hash 可追溯
  - [x] 失败退出码可靠
  - [x] 不宣称专家认证
- Verify: 独立 runner schema/source/failure tests
- Gate: 不能用自产 fixture 通过独立门禁，缺专家证据时状态明确 pending
- 输出物:
  - [x] 独立评测 runner
  - [x] fixture manifest
  - [x] 可选 acceptance gate
- 标准清单:
  - [x] Verify: 独立 runner schema/source/failure tests
  - [x] Gate: 不能用自产 fixture 通过独立门禁，缺专家证据时状态明确 pending
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检
  - [x] 维护 `DEBUG.md` 并保留回归证据

## TP-04
- 标题: 统一 capability 生命周期语义
- 验收项:
  - [x] 无永久双状态真相源
  - [x] 公共兼容边界明确
- Verify: registry schema 与 executor/API 契约测试
- Gate: planned 拒绝执行，validated 不再被误报 production
- 输出物:
  - [x] 统一 registry 字段
  - [x] 迁移契约
  - [x] 一致性测试
- 标准清单:
  - [x] Verify: registry schema 与 executor/API 契约测试
  - [x] Gate: planned 拒绝执行，validated 不再被误报 production
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-05
- 标题: 收敛核心与报告职责复杂度
- 验收项:
  - [x] 超长函数显著收缩
  - [x] 无双轨计算
  - [x] 输出一致
- Verify: 行为快照、复杂度检查和定向回归
- Gate: 职责边界清晰，未新增无消费者抽象
- 输出物:
  - [x] 小职责 helper/模块
  - [x] 行为保持测试
  - [x] AGENTS/module context 同步
- 标准清单:
  - [x] Verify: 行为快照、复杂度检查和定向回归
  - [x] Gate: 职责边界清晰，未新增无消费者抽象
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-06
- 标题: 补齐异步报告端到端指标
- 验收项:
  - [x] 可计算 queue/runtime p95
  - [x] 失败/过期可见
  - [x] 无 PII 标签
- Verify: report job lifecycle metrics tests 与 /metrics smoke
- Gate: 固定低基数标签覆盖全部终态
- 输出物:
  - [x] job metrics
  - [x] observability contract
  - [x] 回归测试
- 标准清单:
  - [x] Verify: report job lifecycle metrics tests 与 /metrics smoke
  - [x] Gate: 固定低基数标签覆盖全部终态
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-07
- 标题: 建立许可证安全的公开客户端闭包
- 验收项:
  - [x] unknown license 不被改写
  - [x] 客户端无服务端隐式 import
  - [x] 可独立安装
- Verify: clean-room install/smoke + archive content inspection + restricted gate negative test
- Gate: 公开闭包无未知许可证资产且仍可调用生产 API
- 输出物:
  - [x] 公开客户端包
  - [x] distribution manifest
  - [x] 许可证门禁测试
- 标准清单:
  - [x] Verify: clean-room install/smoke + archive content inspection + restricted gate negative test
  - [x] Gate: 公开闭包无未知许可证资产且仍可调用生产 API
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-08
- 标题: 全量验证、审查与仓库卫生收口
- 验收项:
  - [x] 第 1 项保持外部待审
  - [x] 本地证据完整
  - [x] 文档与实现一致
- Verify: quick CI + governance/task strict + auto-review + git status
- Gate: 无 BLOCK、无未解释失败、无未提交文件
- 输出物:
  - [x] REVIEW
  - [x] closeout packet
  - [x] 语义提交
  - [x] 干净工作树
- 标准清单:
  - [x] Verify: quick CI + governance/task strict + auto-review + git status
  - [x] Gate: 无 BLOCK、无未解释失败、无未提交文件
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检
