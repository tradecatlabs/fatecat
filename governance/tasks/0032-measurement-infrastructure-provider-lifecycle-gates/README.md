# Task Overview
- Task ID: `0032`
- Slug: `measurement-infrastructure-provider-lifecycle-gates`
- Objective: `把 production provider 生命周期从基础 metadata 推进为本地可验证 gate：为 provider 增加 version lock、source/license/resource manifest、lifecycle/deprecation/promotion policy 和 health gate，新增 provider lifecycle smoke/check 脚本并接入 quick CI；不实现真实外部依赖探测、trace span、供应链许可证人工审计或新 provider。`
- Status: `Done`

## In Scope
- 扩展 production provider metadata，固定 `versionLock`、`lifecycle`、`sourcePolicy`、`licensePolicy`、`resourceManifest`、`promotionGate`、`deprecation`。
- 将 Provider/resource schema 的生命周期字段变成可测试契约。
- 新增 `provider-lifecycle-gate` 本地门禁，校验 production capability provider 覆盖、路径引用、vendor source 生产许可和版本锁。
- 将 `iztro` 从未来候选供应链提升为紫微 production dependency 登记。
- 接入 quick local-ci，并补 API/contract/provider lifecycle 回归测试。
- 同步 API 文档、100% 基础设施路线图、目录级 AGENTS 和任务 closeout。

## Out of Scope
- 不做真实外部依赖连通探测。
- 不接 OpenTelemetry trace span、collector 或 dashboard。
- 不做供应链许可证人工法律审计；本轮只做 manifest 与 SPDX 状态门禁。
- 不新增 provider、不改命理算法、不重写八字或紫微解释层。
- 不声明生产多租户、远端 CI、真实 token 或 Bot live smoke 已完成。

## Task Package Tree
```text
TP-01 现状审计与边界确认
  TP-01.01 盘点 provider metadata、schema、vendor manifest、roadmap 缺口
TP-02 provider lifecycle runtime baseline
  TP-02.01 扩展 ProviderMetadata 和 UsecaseProvider 生命周期字段
  TP-02.02 补 Provider/resource schema 生命周期契约
  TP-02.03 更新 iztro 供应链生产使用登记
TP-03 gate、测试与 CI
  TP-03.01 新增 provider lifecycle gate 脚本
  TP-03.02 新增 provider lifecycle 回归测试
  TP-03.03 接入 quick local-ci
TP-04 文档、任务包与 closeout
  TP-04.01 同步 docs/AGENTS/roadmap
  TP-04.02 跑验证门禁并生成 closeout packet
```

## Requirement Alignment
- 对齐 `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 的 D3/MI-04：provider 生命周期、版本锁、来源、许可、资源 manifest 和 promotion gate。
- 对齐测算基础设施定位：能力不能只是能算，还必须能被发现、复核、追溯、升级和退役。
- 对齐胶水原则：production provider 必须说明复用的成熟库、项目内 usecase、供应链 manifest 和许可边界。
- 对齐反夸大原则：本地 lifecycle gate 不等价于真实外部依赖可用性、法律审计或生产观测平台。

## Task Package Overview
| Package | Status | Evidence |
| --- | --- | --- |
| TP-01 | Done | 已盘点 `providers.py`、capability schema、vendor manifest、roadmap 和 API 文档。 |
| TP-02 | Done | `ProviderMetadata`、`provider.schema.json`、`resource.schema.json` 与 `vendor_sources.json` 已扩展。 |
| TP-03 | Done | provider lifecycle gate、focused tests 和 quick CI 已通过。 |
| TP-04 | Done | docs/AGENTS/roadmap 已同步；closeout packet 已生成。 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
