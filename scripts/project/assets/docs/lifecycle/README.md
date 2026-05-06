# FateCat 生命周期资产

这里存放的是 skill 级生命周期治理资产，不是业务源码。

## 使用方式

1. 执行 `bash scripts/init-lifecycle-pack.sh --name <slug>`
2. 按阶段填写生成的 `00-context.md` 到 `07-retirement.md`
3. 用 `bash scripts/lifecycle-status.sh` 查看完成状态
4. 在交付前或事故后执行 `bash scripts/collect-ops-bundle.sh --output <dir>`

## 阶段文件

- `00-context.md`：背景、范围、参与方
- `01-requirements.md`：需求、验收、约束
- `02-prototype.md`：最小验证路径
- `03-iteration.md`：迭代计划与缺口
- `04-mature-refactor.md`：成熟方案替换
- `05-production-hardening.md`：生产加固
- `06-operations.md`：运维入口与故障策略
- `07-retirement.md`：退役与归档
