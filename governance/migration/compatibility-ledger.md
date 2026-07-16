---
id: MIG-COMPATIBILITY-LEDGER
type: compatibility-ledger
status: active
owner: engineering
created: 2026-06-15
last_reviewed: 2026-07-16
review_cycle: P30D
---

# Compatibility Ledger

本账本只登记仍留在 active 路径里的兼容入口。旧 `scripts/project/` 兼容盒已退役；旧路径引用只允许保留在迁移账本、历史证据、负例测试和防回潮规则中。

| 兼容入口 | owner | 真实契约 | 保留原因 | 移除条件 |
| --- | --- | --- | --- | --- |
| `domains/experience-delivery/services/fatecat-delivery/src/bazi_calculator.py` | engineering | 历史裸模块导入 `from bazi_calculator import BaziCalculator` | Bot、API、旧回归测试和可能的外部脚本仍使用裸模块导入；实现已转发到 `fate_core.kernel.bazi_calculator` | 所有内部调用改为 `fate_core` 显式导入；发布迁移说明；外部调用方确认不再依赖裸模块路径 |
| `domains/fate-analysis/services/fate-core/src/fate_core/adapters/legacy_bazi.py` | engineering | `LegacyBaziInput`、`calculate_legacy_bazi`、`calculate_pure_analysis_raw` | pure-analysis、紫微真太阳时锚点和历史报告字段仍需同一兼容入口稳定输出 | 历法、四柱、强弱、格局、用神、岁运、神煞完成独立 kernel/provider 拆分，并由 golden/oracle 证明输出等价 |
| `infra/environments/local/.env.example` / `agent.env.example` 中的 `FATE_API_TOKEN` | engineering | 管理接口 token 的旧环境变量别名 | 已推荐 `FATE_API_ADMIN_TOKEN`，但本地部署和历史脚本可能仍读取旧名 | 运行入口、文档和部署模板全部使用 `FATE_API_ADMIN_TOKEN`；一个发布周期内无旧变量使用证据 |

## 防回潮规则

- active catalog 不得出现 `compatibility_source_root`、`temporary-compatibility-box` 或 `scripts/project/modules`。
- service.yaml 不得出现 `legacy_source_root` 或 `legacy_runtime_root`。
- 新八字规则不得写入 delivery wrapper、API、Web、Bot 或报告层。
- 保留兼容入口必须同时具备 owner、真实契约、保留原因和移除条件。
