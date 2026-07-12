# FateCat 自审记录

审查时间：2026-07-13 HKT +0800

## 结论

当前工作树正在完成“测算基础设施基础加固”。本地实现已覆盖独立分发闭包、综合八字单一生产入口、Telegram 渠道降级、自动 quick CI、供应链卫生、治理上下文和性能基线；在最终提交、远端 quick CI 与线上部署复验完成前，交付状态为 `WARN`。

公开 Skill 分发状态为 `BLOCK`：内部 lite 运行包可以构建和验收，但当前运行依赖 `bazi-1`、`sxwnl` 缺少可确认的上游分发许可证。`scripts/public-release-gate.sh` 会机械拒绝把这些资产标记为可公开分发，不得用本地测试通过替代法律授权。

## 当前证据

| 项目 | 当前事实与证据 |
|---|---|
| 基线提交 | `acd17d7f5ba901320a3f1e579c5b26d5ee8c0980`；本轮最终提交待生成 |
| Python 分发 | `scripts/package-distribution-smoke.sh` 在仓库外虚拟环境安装 wheel 并执行 capability CLI；wheel 约 200 KiB，sdist 约 166 KiB |
| wheel 能力边界 | 可独立发现 capability 与包内契约；综合八字、紫微实际计算仍依赖未打入 wheel 的 vendor 引擎 |
| lite 运行包 | 导出约 34 MiB、2665 个文件；排除 `infra/runtime/local-state/`、无关媒体、文档型 reference assets 和 vendor 构建产物 |
| 综合八字入口 | Web、API、Bot 与 CLI 均通过 `CapabilityExecutor`；旧 `/api/v1/bazi/simple` 和 `/calculate` 只保留弃用兼容 URL |
| Telegram readiness | Telegram 未就绪时 `/ready` 仍可返回核心服务 ready，同时通过 `degradedSurfaces` 和渠道状态暴露故障 |
| Telegram 重试 | 30 秒起步的有界指数退避，默认上限 900 秒并支持抖动；配置和状态均可观测 |
| 自动 CI | `.github/workflows/quick.yml` 覆盖 pull request 与 `main` push；Acceptance、Container、HF deploy 继续保持手动或受控触发 |
| vendor 卫生 | 测试进程设置 `PYTHONDONTWRITEBYTECODE=1`，并在测试后再次执行 `vendor-health.sh` |
| 性能基线 | 本地三次 warm smoke：八字约 464 ms，紫微约 121 ms；这是开发机回归预算，不是生产 p95/p99 |
| 治理 | module context、代码评审标准、context map 和 strict governance 校验已补齐 |
| 运维手册 | `references/ops-pack.md`；SLO、指标、上线、回滚、降级和证据采集命令可复核 |

## 门禁状态

| 门禁 | 状态 | 说明 |
|---|---|---|
| 本地定向回归 | PASS | 分发、入口一致性、Telegram、workflow、供应链测试已执行 |
| 本地全量 pytest | PASS | `639 passed, 1 skipped in 456.16s` |
| ruff / format / mypy | PASS | ruff、全仓 format check、fate_core mypy 均通过 |
| quick CI | PASS | 本地 `446 passed`；GitHub run `29205516109` 对应 `8e0874b1...` 通过 |
| 内部 lite 运行包 | PASS | 可导出、可做卫生检查和纯分析 smoke |
| 公开 Skill 分发 | BLOCK | `bazi-1`、`sxwnl` 缺少可确认分发许可证 |
| HF Space 线上版本 | PENDING | 线上仍需在最终提交部署后复验 `/health`、`/ready`、`/metrics`、`/web` |
| Telegram live Bot | PENDING | 外部连通验证待执行，需要真实 token、webhook 与 Telegram API |
| 专业命理评审 | PENDING | 外部专家命例、MingLi-Bench、no-leak 签字不能由仓库内测试替代 |

## 当前边界

- FateCat wheel 当前是协议与编排分发物，不是包含所有闭源或许可证不明引擎的独立计算套件。
- 综合八字 capability 只有一个公开生产编排入口；核心内部仍复用 `BaziCalculator` 作为成熟遗留计算适配器，不再由 delivery 选择双引擎。
- Telegram 是可降级交付面；其失败不得拖垮 Web/API，也不得被 readiness 隐藏。
- Web 正常展示用户选择的出生地区；默认不把报告写入数据库，也不自动发送给 Gemini 或 Telegram。
- 免费 HF Space 只定位为单实例公开工作台，不宣称高并发、多副本、持久队列或生产 SLO。

## 剩余动作

1. 在最终工作树执行全量 pytest、ruff、format、mypy、quick CI、治理 strict 与任务 closeout。
2. 按语义切分提交并推送 `main`，确认远端 `quick.yml` 对应最终提交通过。
3. 部署 HF Space 后复验公开端点；真实 Telegram、外部数据库、专家评审继续明确标记为“外部连通验证待执行”。
4. 在获得明确许可证或替换为可分发引擎前，不发布包含受阻 vendor 的公共 Skill 包。
