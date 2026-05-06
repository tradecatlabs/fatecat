# FateCat Skill Reference Index

## Quick Links

- 上手与边界：`architecture.md`
- 标准执行链路：`execution-playbook.md`
- 生命周期阶段：`lifecycle.md`
- 阶段门禁：`stage-gates.md`
- 运维与加固：`ops-pack.md`
- 常用命令：`commands.md`
- 输入输出契约：`io-contract.md`
- 真实 Bot 验收：`live-bot-verification.md`
- 生产就绪门禁：`scripts/production-readiness.sh`
- 迁移与导出：`migration-plan.md`
- 故障排查：`troubleshooting.md`

## Reading Order

1. 先看 `architecture.md`，理解 `scripts/project/` 作为源码根，以及 `scripts/project/assets/docs/lifecycle/` 作为生命周期治理资产区的边界
2. 再看 `execution-playbook.md`，按统一顺序执行 `bootstrap -> preflight -> delivery-smoke -> analysis/serve`
3. 需要判断是否能进入下一阶段时，看 `stage-gates.md`
4. 要直接执行命令或发布验收时，看 `commands.md`
5. 需要对接上层系统时，看 `io-contract.md`
6. 要理解需求到退役的阶段链条时，看 `lifecycle.md`
7. 要验证真实 Telegram token、生产 API URL、CORS 与生产 token 时，运行 `scripts/production-readiness.sh`
8. 要验证真实 Telegram token 与 Bot API 连通性时，看 `live-bot-verification.md`
9. 要做独立 skill 分发时，看 `migration-plan.md`
10. 遇到启动或依赖异常时，看 `troubleshooting.md`

## Scope Notes

- 这里记录的是 skill 化视角下的操作材料，不重复 FateCat 全量 README
- 生命周期文档聚焦“如何推进阶段与沉淀资产”，不替代 `scripts/project/` 内业务设计细节
- 外部成熟算法仓库仍以 `scripts/project/assets/vendor/` 为真相源，不在此处转抄
