# AGENTS.md - developer resources

## 目录用途

`contracts/fate/developer/` 是开发者接入资源的机器真相源。这里登记 sandbox fixture、OpenAPI 导出边界和 docs smoke 期望，不保存真实 token、生产 URL、用户输入或报告正文。

## 目录结构

```text
developer/
├── AGENTS.md
└── sandbox.json
```

## 职责边界

- `sandbox.json`：登记本地可执行 sandbox fixture；fixture 只能使用北京、测试样本和公开 capability，不依赖真实凭证。
- docs smoke 脚本读取这里的 fixture，使用 FastAPI `TestClient` 验证 OpenAPI、示例文件和 sandbox 响应结构。
- 这里不保存 SDK 代码；人类可读示例放在 `docs/reference-materials/developer/examples/`。
- 这里不声明真实线上 sandbox token 服务；真实开发者门户和密钥发放属于后续生产任务。
