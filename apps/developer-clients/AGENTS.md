# AGENTS.md - developer clients

## 目录用途

`apps/developer-clients/` 承载面向应用开发者的远程 API 客户端，不承载测算算法、服务端运行时、vendor 资产或内部证据规则。

## 目录结构

```text
developer-clients/
├── AGENTS.md
└── python/
    ├── AGENTS.md
    ├── LICENSE
    ├── README.md
    ├── pyproject.toml
    └── src/fatecat_client/
```

## 职责边界

- `python/`：可独立构建、安装的 Python HTTP 客户端。
- 客户端只能依赖公开 HTTP 契约，不得导入 `fate_core`、delivery 服务或 `tools/reference-repos`。
- 发布许可和归档允许范围由 `contracts/fate/developer/public-client-distribution.json` 定义。

## 依赖方向

- `apps/developer-clients -> public HTTP API + contracts/fate/developer`
- 禁止 `domains -> apps/developer-clients`。
