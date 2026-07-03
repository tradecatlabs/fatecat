# AGENTS.md - developer docs

## 目录用途

`docs/reference-materials/developer/` 保存开发者接入示例、SDK/package baseline、API changelog 和 sandbox 使用说明。这里是人类阅读入口，不是机器契约真相源。

## 目录结构

```text
developer/
├── AGENTS.md
├── API_CHANGELOG.md
├── PORTAL.md
├── README.md
├── SDK_PACKAGE_BASELINE.md
├── SDK_RELEASE_BASELINE.md
└── examples/
    ├── agent-tool-call.json
    ├── curl-sandbox.sh
    ├── node-client.mjs
    └── python-client.py
```

## 职责边界

- `README.md`：说明 OpenAPI、developer platform gate、sandbox fixture 和示例运行方式。
- `PORTAL.md`：本地 developer portal release baseline 的人类入口，聚合 API、契约、SDK 和验证命令；不声明公网门户上线。
- `API_CHANGELOG.md`：人类可读 API 变更记录；机器真相源在 `contracts/fate/developer/api-changelog.json`。
- `SDK_PACKAGE_BASELINE.md`：说明当前只有 installable examples 和 package baseline metadata，不声明 PyPI/npm SDK 已发布。
- `SDK_RELEASE_BASELINE.md`：说明本地 SDK release-readiness manifest、package candidates 和 publish 前置证据。
- `examples/`：保存最小 SDK 示例；不得保存真实 token、真实生产 URL、真实用户数据或报告正文。
- 机器可执行 sandbox fixture、sandbox token contract 和 API changelog 位于 `contracts/fate/developer/`。
- docs smoke 位于 `scripts/developer-docs-smoke.sh`，负责验证示例文件、OpenAPI 和 sandbox fixture；developer platform gate 位于 `scripts/developer-platform-gate.sh`，负责锁定 SDK/package、token 和 changelog 边界；developer portal gate 位于 `scripts/developer-portal-gate.sh`，负责锁定 portal、SDK release baseline 和 sandbox output snapshot。
