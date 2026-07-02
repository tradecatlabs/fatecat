# AGENTS.md - developer docs

## 目录用途

`docs/reference-materials/developer/` 保存开发者接入示例、SDK 片段和 sandbox 使用说明。这里是人类阅读入口，不是机器契约真相源。

## 目录结构

```text
developer/
├── AGENTS.md
├── README.md
└── examples/
    ├── agent-tool-call.json
    ├── curl-sandbox.sh
    ├── node-client.mjs
    └── python-client.py
```

## 职责边界

- `README.md`：说明 OpenAPI、sandbox fixture 和示例运行方式。
- `examples/`：保存最小 SDK 示例；不得保存真实 token、真实生产 URL、真实用户数据或报告正文。
- 机器可执行 sandbox fixture 位于 `contracts/fate/developer/sandbox.json`。
- docs smoke 位于 `scripts/developer-docs-smoke.sh`，负责验证示例文件、OpenAPI 和 sandbox fixture。
