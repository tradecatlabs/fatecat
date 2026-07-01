# Task Overview
- Task ID: `0008`
- Slug: `measurement-infrastructure-hardening`
- Objective: `继续把 FateCat 测算基础设施从协议骨架推进到开发者可接入、能力准入可拒绝、隐私与生产门禁可审计的基础设施硬化状态。`
- Status: `Done`

## In Scope
- 增强 capability registry 准入规则：生产能力必须有 passing testGate，planned 能力必须 blocked 且不可伪装为真实 provider。
- 增强 `/metadata` 开发者发现入口：OpenAPI、文档、能力、报告、隐私、生产门禁。
- 补测算基础设施 API 接入文档。
- 补 regression tests，锁定开发者入口和准入不变量。
- 跑本地 quick CI、governance strict、task docs validator 和 git hygiene。

## Out of Scope
- 不新增六爻、奇门、大六壬等业务体系实现。
- 不执行真实生产域名、真实 token、Bot live smoke。
- 不改变当前默认综合八字 Markdown profile。
- 不切换分支、不改写 Git 历史。

## Task Package Tree
```text
TP-01 developer-entrypoints
├── TP-01.01 metadata-dev-discovery
└── TP-01.02 api-guide-doc
TP-02 capability-admission
├── TP-02.01 registry-admission-rules
└── TP-02.02 admission-regression-tests
TP-03 verification-and-ship
├── TP-03.01 local-quality-gates
└── TP-03.02 git-control
```

## Requirement Alignment
- 用户目标：持续推进并完善“测算基础设施”定位。
- 工程目标：优先补基础设施契约、准入、文档和门禁，不堆新预测模块。
- 隐私目标：继续保持北京以外真实地区不得作为前端公开示例。
- 生产目标：本地门禁先收紧；外部连通验证明确后续执行。

## Task Package Overview
| Node | Scope | Proof |
| --- | --- | --- |
| TP-01 | 开发者发现和 API 接入文档 | `/metadata`、`/openapi.json`、`docs/reference-materials/operations/测算基础设施 API 接入.md` |
| TP-02 | 能力准入硬化 | `registry.py`、`test_capability_protocol.py` |
| TP-03 | 验证与版本控制 | pytest、ruff、mypy、quick CI、governance、git |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
