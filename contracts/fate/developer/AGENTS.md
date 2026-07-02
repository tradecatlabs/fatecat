# AGENTS.md - developer resources

## 目录用途

`contracts/fate/developer/` 是开发者接入资源的机器真相源。这里登记 developer platform baseline、SDK/package 发布边界、sandbox fixture、sandbox token contract、API changelog 和 docs/gate 期望，不保存真实 token、生产 URL、用户输入或报告正文。

## 目录结构

```text
developer/
├── AGENTS.md
├── api-changelog.json
├── developer-platform.json
├── sandbox-token-contract.json
└── sandbox.json
```

## 职责边界

- `developer-platform.json`：登记开发者平台 baseline、SDK/package 状态、sandbox、API changelog 和 validation gate；它不声明 PyPI/npm SDK 已发布。
- `api-changelog.json`：机器可读 API changelog 与兼容策略；breaking change 必须在这里登记迁移与兼容窗口。
- `sandbox-token-contract.json`：未来公网 sandbox token 的 claim、scope、rate limit 与负向证据边界；当前只是 contract，不发行真实 token。
- `sandbox.json`：登记本地可执行 sandbox fixture；fixture 只能使用北京、测试样本和公开 capability，不依赖真实凭证。
- docs smoke 脚本读取这里的 fixture，使用 FastAPI `TestClient` 验证 OpenAPI、示例文件和 sandbox 响应结构；developer platform gate 校验 SDK/package baseline、sandbox token contract 和 API changelog 的口径。
- 这里不保存 SDK 代码；人类可读示例放在 `docs/reference-materials/developer/examples/`。
- 这里不声明真实线上 sandbox token 服务；真实开发者门户和密钥发放属于后续生产任务。
