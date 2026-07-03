# FateCat Developer Sandbox

FateCat 的开发者接入面以本地 OpenAPI、sandbox fixture、最小 SDK 示例、SDK/package baseline、sandbox token contract 和 API changelog 为基线。

机器契约入口：

```text
contracts/fate/developer/developer-platform.json
```

本地开发者门户基线：

```text
docs/reference-materials/developer/PORTAL.md
contracts/fate/developer/developer-portal.json
```

## OpenAPI

```bash
bash scripts/export-openapi.sh \
  --output infra/runtime/local-state/exports/developer/openapi.json
```

## Sandbox

Sandbox fixture 位于：

```text
contracts/fate/developer/sandbox.json
```

这些 fixture 只使用北京和测试样本，不依赖真实 token、真实用户或生产域名。

未来公网 sandbox token 的 claim、scope 和负向证据边界位于：

```text
contracts/fate/developer/sandbox-token-contract.json
```

当前仓库只定义 token contract，不发行真实 sandbox token。

## 示例

- `examples/curl-sandbox.sh`
- `examples/python-client.py`
- `examples/node-client.mjs`
- `examples/agent-tool-call.json`

SDK/package 口径位于：

```text
docs/reference-materials/developer/SDK_PACKAGE_BASELINE.md
```

当前只是 installable examples 和 package baseline metadata，不声明 PyPI/npm SDK 已发布。

SDK release-readiness baseline：

```text
docs/reference-materials/developer/SDK_RELEASE_BASELINE.md
contracts/fate/developer/sdk-release-baseline.json
```

该 baseline 会通过本地 gate 校验 SDK 示例、snapshot 和 portal wiring，但仍不声明 PyPI/npm 已发布。

API changelog：

```text
contracts/fate/developer/api-changelog.json
docs/reference-materials/developer/API_CHANGELOG.md
```

本地验证：

```bash
bash scripts/developer-docs-smoke.sh \
  --output-json infra/runtime/local-state/exports/developer/docs-smoke.json \
  --openapi-json infra/runtime/local-state/exports/developer/openapi.json
```

开发者平台 gate：

```bash
bash scripts/developer-platform-gate.sh \
  --output-json infra/runtime/local-state/exports/developer/developer-platform-gate.json
```

开发者门户与 SDK release baseline gate：

```bash
bash scripts/developer-portal-gate.sh \
  --output-json infra/runtime/local-state/exports/developer/developer-portal-gate.json
```
