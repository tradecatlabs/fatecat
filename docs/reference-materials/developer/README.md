# FateCat Developer Sandbox

FateCat 的开发者接入面以本地 OpenAPI、sandbox fixture 和最小 SDK 示例为基线。

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

## 示例

- `examples/curl-sandbox.sh`
- `examples/python-client.py`
- `examples/node-client.mjs`
- `examples/agent-tool-call.json`

本地验证：

```bash
bash scripts/developer-docs-smoke.sh \
  --output-json infra/runtime/local-state/exports/developer/docs-smoke.json \
  --openapi-json infra/runtime/local-state/exports/developer/openapi.json
```
