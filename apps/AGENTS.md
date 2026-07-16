# AGENTS.md - apps

## 目录用途

`apps/` 承载用户体验入口与渠道壳层，只表达用户如何进入 FateCat，不承载命理领域规则、数据库写入或平台通用能力。

## 目录结构

```text
apps/
├── AGENTS.md
└── developer-clients/
    └── python/
```

## 职责边界

- Web、Bot、CLI 等体验壳层如果独立成产品入口，优先落在这里。
- 领域计算、能力协议和报告事实源不放在 `apps/`，应进入 `domains/` 或 `contracts/`。
- 当前生产交付服务仍登记在 `domains/experience-delivery/services/fatecat-delivery/`，`apps/` 暂不承载 active runtime。
- `developer-clients/`：公开远程 API 客户端；不得携带服务端计算核心或受限 vendor 资产。

## 依赖方向

- `apps -> domains/*/services/* + contracts/*`
- 禁止 `domains` 反向依赖 `apps`。
