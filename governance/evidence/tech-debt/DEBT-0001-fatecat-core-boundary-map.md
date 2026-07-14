---
id: DEBT-0001
type: tech-debt
status: active
owner: engineering
last_reviewed: 2026-07-13
---

# FateCat 核心大文件职责边界图

## 背景

本记录服务 `governance/tasks/0001-quality-standards-100` 的 `TP-05.01`。当前系统已经具备企业级目录，但领域算法、报告渲染、交付编排和 Web 呈现仍集中在少数大文件中。短期不做大爆炸重写，先把边界写清楚，后续改动按任务树小步迁移。

## 边界矩阵

| 文件 | 当前行数 | 保留职责 | 迁出职责 | 禁止新增职责 | 承接任务 |
|---|---:|---|---|---|---|
| `domains/fate-analysis/services/fate-core/src/fate_core/kernel/bazi_calculator.py` | 2514 | 八字 legacy 核心实现的当前归属位置、历史字段兼容、成熟库编排 | 已迁出称骨、命卦、真太阳时边界；后续继续按四柱、强弱、关系、格局、用神、岁运、神煞拆成更小 kernel/provider 模块 | Web/API/Bot/报告专属分支、确定性断语扩展、未登记规则源 | `TP-07.01` 后续维护 |
| `domains/fate-analysis/services/fate-core/src/fate_core/kernel/bone_weight.py` | 327 | 版本化整数称骨权重、严格输入校验、闰月策略、男女解释边界和构成明细 | 当前只接入已固定来源的 7.1 男女歌诀边界；其余男女歌诀只有完成全表来源校定后才可接入 | 核心格局判断、报告渲染、Web/Bot/API 逻辑、7.2 伪可达、未经校定的传本混入 | `TP-07.01` |
| `domains/fate-analysis/services/fate-core/src/fate_core/kernel/ming_gua.py` | 39 | 命卦计算纯函数 | 无；保持独立、无 IO、无交付依赖 | 八字格局、报告渲染、Web/Bot/API 逻辑 | `TP-07.01` |
| `domains/fate-analysis/services/fate-core/src/fate_core/kernel/solar_time.py` | 103 | 真太阳时脚本调用、JSON 解析和历史简化公开函数 | 后续若引入天文级 provider，应在此模块后面扩展，不回灌 `BaziCalculator` | Web/Bot/API 逻辑、双口径 fallback | `TP-07.01` |
| `domains/experience-delivery/services/fatecat-delivery/src/bazi_calculator.py` | 30 | 公开裸模块导入兼容导出，仅转发 `fate_core.kernel.bazi_calculator` | 无；删除需先确认外部裸模块调用方全部退役 | 命理规则、路径解析、vendor 注入、报告/接口逻辑 | `TP-07.03` |
| `domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_pure_analysis.py` | 1003 | pure-analysis 用例编排、profile 投影、证据拼装薄层 | benchmark 构建、rule depth 拼装、topic profile、证据归一化继续拆到 fate-core 内部模块 | 交付层渲染、Bot 文案、Web HTML、外部 IO 副作用 | `TP-05` / `TP-07.01` |
| `domains/experience-delivery/services/fatecat-delivery/src/report_generator.py` | 1933 | Markdown 报告模板兼容、报告系统路由 | 已迁出 Markdown 基础表格/转义工具；后续可继续迁出八字/紫微章节生成器、品牌页脚、证据摘要、报告系统 registry | 新命理计算、API 鉴权、Web 表单状态、Bot 队列逻辑 | `TP-07.02` |
| `domains/experience-delivery/services/fatecat-delivery/src/bot.py` | 1178 | Telegram 会话、按钮、发送重试、Bot 交付编排 | 已迁出进度展示配置；后续迁出输入解析、队列背压策略、报告生成任务、结果发送队列 | 命理规则、API 路由、Web HTML、数据库 schema | `TP-07.02` |
| `domains/experience-delivery/services/fatecat-delivery/src/main.py` | 2611 | FastAPI 路由、公共服务护栏、观测指标、记录接口 | 已迁出 env/CORS、报告任务和计算服务；后续拆分 auth、metrics、rate limit、records 与路由组 | 命理算法、报告模板、Bot 状态、HTML 大片段 | `TP-07.02` |
| `domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py` | 2589 | 内存报告任务、TTL、队列、状态与跨表面报告编排 | 应按任务存储、执行器、清理器和状态投影拆分 | 命理规则、HTML、API 鉴权、永久数据存储 | `TP-07.02` |
| `domains/experience-delivery/services/fatecat-delivery/src/web_ui.py` | 750 | 原生 HTML 表单渲染、服务端 Markdown 输出、页面元信息 | 已迁出 Web 表单输入/结果模型；后续迁出输入解析、工作台数据构建、报告 panel、branding panel、元信息 panel 分组 | 自定义复杂前端框架、违背 `Design.md` 的视觉美化、命理算法 | `TP-07.02` |

## 目标终态

- `fate-core` 是命理能力真相源，delivery 只负责 Web/API/Bot/Markdown 交付。
- `BaziCalculator` 核心归属 `fate_core.kernel.bazi_calculator`；公开交付面统一通过 `CapabilityExecutor`，delivery 裸模块只保留未登记外部调用的迁移兼容入口。
- 报告生成只读结构化结果，不再产生或修正命理结论。
- Web 页面保持原生 HTML 和服务端直出 Markdown，不引入重前端。
- Bot 队列、公共 API 限流和生产防护归交付层，不进入领域核心。

## 最小迁移顺序

1. `TP-07.01`：继续拆 `BaziCalculator` 的稳定领域边界，保持 golden/API 输出不变。
2. `TP-07.02`：继续收敛 delivery 层 API/Web/Bot/报告边界。
3. `TP-07.03`：清退没有真实外部契约的 legacy/compat shim。
4. `TP-07.04`：用 local-ci quick、catalog、operability 和任务文档校验证明长期维护性闭环。

## Future-Optimal 迁移约束

- target end state: `CapabilityExecutor` 是公开计算入口，领域规则位于独立 kernel/provider，delivery 只拥有渠道和呈现。
- real constraints: 旧 API URL、既有 JSON/Markdown 契约和未登记的裸模块调用方需要可验证迁移窗口；不能以删除兼容入口破坏真实外部契约。
- inertia constraints: 大文件形状、旧模块名和“拆起来麻烦”不构成保留错误边界的理由。
- kill list: delivery 双引擎选择、交付层命理规则、没有真实调用证据的永久兼容 shim、围绕旧概念新增 wrapper。
- proof point: Web/API/Bot/CLI 全部通过 capability executor，入口语义回归通过，delivery 不再导入 `BaziCalculator`。
- falsifier: 任一公开入口可绕过 executor，或移除兼容入口后真实契约测试失败且没有迁移路径。
- migration slice: 本轮先移除双生产路径并保留弃用 URL；后续按调用证据删除裸模块 shim，再逐步拆分核心大文件。

## 审查规则

- 新八字规则不得落进 `domains/experience-delivery/services/fatecat-delivery/src/`。
- 新 Web 页面行为必须继续遵守 `governance/architecture-gates/rules/GATE-0001-Web-HTML-禁止自定义前端样式.md`。
- 任一拆分任务必须用现有 golden/regression 测试证明外部行为不变。
- 如果任务只为了减少行数而改变公共输出，必须拒绝。
