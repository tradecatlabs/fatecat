# AGENTS.md - Hugging Face Space

## 目录用途

`infra/huggingface-space/` 保存 FateCat 免费 Hugging Face Docker Space 的分发模板。这里的文件会被 `scripts/hf-space-deploy.sh` 复制到临时 Space bundle 根目录，再通过 `hf` CLI 上传到 `tradecatlabs/fatecat`。

## 目录结构

```text
infra/huggingface-space/
├── AGENTS.md
├── Dockerfile
├── README.md
├── THIRD_PARTY_NOTICES.md
└── .hfignore
```

## 职责边界

- `README.md`：Hugging Face Space 根 README，包含 `sdk: docker`、`app_port: 7860`、用户隐私说明、第三方分发边界和可选 Telegram Webhook 配置。
- `THIRD_PARTY_NOTICES.md`：完整 Space bundle 的第三方来源与许可证状态声明；NOASSERTION 快照不得被统一重标为 MIT。
- `Dockerfile`：HF Space 专用镜像入口，默认关闭记录存储和 Telegram Webhook，并监听 `7860`。
- `.hfignore`：Space repo 级别的额外忽略规则，防止运行态、缓存、secret、数据库和日志进入分发仓。
- 本目录不保存 token、secret、真实用户记录、构建产物或 Space 运行态。

## 依赖方向

- `infra/huggingface-space -> scripts/hf-space-deploy.sh`
- Space bundle 运行时依赖 `domains/`、`contracts/`、`infra/docker/entrypoint.delivery.sh`、`infra/environments/branding.json` 和必要 reference repos。
- 业务代码、命理规则和 Web UI 不在本目录实现。
- Telegram Webhook 与 Web/API 共用 delivery 进程；本目录只声明默认关闭的运行参数，不保存 Bot secret。
