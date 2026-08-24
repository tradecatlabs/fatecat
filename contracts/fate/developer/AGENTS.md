# AGENTS.md - developer resources

## 目录用途

`contracts/fate/developer/` 是开发者接入资源的机器真相源。这里登记 developer platform baseline、SDK/package 发布边界、sandbox fixture、sandbox token contract、API changelog 和 docs/gate 期望，不保存真实 token、生产 URL、用户输入或报告正文。

## 目录结构

```text
developer/
├── AGENTS.md
├── api-changelog.json
├── developer-portal.json
├── developer-platform.json
├── public-client-distribution.json
├── public-server-distribution.json
├── sandbox-access-gateway.json
├── sandbox-output-snapshot.json
├── sandbox-token-contract.json
├── sdk-release-baseline.json
└── sandbox.json
```

## 职责边界

- `developer-platform.json`：登记开发者平台 baseline、SDK/package 状态、sandbox、API changelog 和 validation gate；它不声明 PyPI/npm SDK 已发布。
- `developer-portal.json`：登记本地 developer portal release baseline、人类入口、机器契约和外部未上线边界；它不声明公网门户已上线。
- `sdk-release-baseline.json`：登记 SDK release-readiness package candidates、smoke commands、未发布边界和未来 registry publish 证据要求。
- `public-client-distribution.json`：公开 Python HTTP 客户端与服务端运行时隔离边界、归档 allowlist 和 clean-room 门禁。
- `public-server-distribution.json`：公开 HF/轻量服务端运行包的有界分发决定；对非 SPDX 快照只记录发布负责人明确审批，不推断或改写上游许可证，也不放开 package registry 发布。
- `sandbox-access-gateway.json`：登记本地可执行 sandbox gateway 的 scope、端点、限流、审计和门禁口径；它不声明公网 token issuer、revocation service 或生产 API key 服务已上线。
- `sandbox-output-snapshot.json`：登记 sandbox fixture 的脱敏固定输出 hash 和结构断言；只保存摘要，不保存完整响应正文。
- `api-changelog.json`：机器可读 API changelog 与兼容策略；breaking change 必须在这里登记迁移与兼容窗口。
- `sandbox-token-contract.json`：未来公网 sandbox token 的 claim、scope、rate limit 与负向证据边界；当前只接入本地 gateway baseline，不发行真实公网 token。
- `sandbox.json`：登记本地可执行 sandbox fixture；fixture 只能使用北京、测试样本和公开 capability，不依赖真实凭证。
- docs smoke 脚本读取这里的 fixture，使用 FastAPI `TestClient` 验证 OpenAPI、示例文件和 sandbox 响应结构；developer platform gate 校验 SDK/package baseline、sandbox token contract 和 API changelog 的口径。
- developer portal gate 读取这里的 portal、SDK release baseline 和 snapshot，验证 SDK smoke、fixed snapshot digest、changelog 和 no-overclaim 边界。
- 这里不保存 SDK 代码；人类可读示例放在 `docs/reference-materials/developer/examples/`。
- 这里不声明真实线上 sandbox token 服务；真实开发者门户和密钥发放属于后续生产任务。
