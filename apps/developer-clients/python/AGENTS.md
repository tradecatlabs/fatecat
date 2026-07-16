# AGENTS.md - Python public client

## 目录用途

该目录是 `fatecat-client` 的独立 Python 分发根，只提供远程 HTTP 调用能力。

## 目录结构

```text
python/
├── .gitignore
├── AGENTS.md
├── LICENSE
├── README.md
├── pyproject.toml
└── src/fatecat_client/
    ├── __init__.py
    ├── client.py
    └── py.typed
```

## 职责边界

- `client.py`：URL、超时、JSON、HTTP 错误和公开端点的薄适配。
- `__init__.py`：稳定公共导出和版本号。
- 包运行依赖必须保持为空；标准库足以完成 HTTP 客户端职责。
- 禁止加入本地排盘、vendor、典籍、服务端配置、token 默认值或用户样本。
