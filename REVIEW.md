# FateCat 自审记录

审查时间：2026-06-17 HKT +0800

## 结论

当前仓库按“TradeCat Labs 实验室项目 / 免费公开 Web Markdown 工作台 / 用户可独立部署单实例”的口径为 `PASS`。

本轮不再把 GitHub Acceptance 当作默认验收来源；公开发布门禁已经收敛到本地脚本 `scripts/public-release-gate.sh`。GitHub Acceptance 与 Container workflow 仅保留手动触发，避免 push 自动跑远端验收。

外部托管口径：Hugging Face 官方免费 Space 的 `/health`、`/ready`、`/metrics` 已通过 live smoke；Telegram live Bot 不是免费 Web 工作台必需项，本轮保持 `SKIP`，不得描述为已验收。

## 当前证据

| 项目 | 证据 |
|---|---|
| 当前分支 | `main` |
| 当前发布目标 | 免费公开 Web 工作台 + HF Space 自助部署 |
| 公共服务运维手册 | `references/ops-pack.md` |
| 本地公开发布门禁 | `bash scripts/public-release-gate.sh --api-url https://tradecatlabs-fatecat.hf.space --skip-delivery-smoke --output /tmp/fatecat-public-release-20260617-final` -> `PASS` |
| quick CI | 门禁内执行 `scripts/local-ci.sh --profile quick` -> `PASS` |
| focused regression | `54 passed in 10.79s` |
| ruff lint / format | `All checks passed!`；`144 files already formatted` |
| mypy | `Success: no issues found in 50 source files` |
| source / privacy hygiene | `source hygiene ok`；`privacy fixtures ok` |
| public release policy | `public release policy ok` |
| delivery smoke | `bash scripts/public-release-gate.sh --api-url https://tradecatlabs-fatecat.hf.space --output /tmp/fatecat-public-release-20260617-rerun` 内本地 API `/health` smoke 通过 |
| HF live smoke | `https://tradecatlabs-fatecat.hf.space/health`、`/ready`、`/metrics` 通过 |
| Web/Gemini 隐私边界 | Web 页面说明 FateCat 不会自动发送报告到 Gemini；用户复制 Markdown 后自行打开 Gem |
| 默认存储口径 | HF Docker Space `FATE_RECORDS_ENABLED=0`；报告任务使用进程内有界队列，TTL 到期或 Space 重启后消失 |

## 本轮处理

- GitHub `FateCat Acceptance` workflow 改为 `workflow_dispatch` 手动触发，不再由 push / pull_request 自动运行。
- GitHub `FateCat Container` workflow 改为 `workflow_dispatch` 手动触发，只有显式选择 `push_image` 才推送 GHCR。
- 新增 `scripts/check-public-release-policy.sh`，检查公开发布策略是否回潮。
- `scripts/local-ci.sh --profile quick` 接入公开发布策略检查。
- 新增 `scripts/public-release-gate.sh`，串联 quick CI、发布策略、delivery smoke、生产 readiness 和可选 live API 验证。
- 修复 `scripts/production-readiness.sh` 在 `pipefail` 下 `curl | grep -q` 检查 `/metrics` 可能误报 `curl: (23)` 的问题。
- Web 页面元信息补充默认不写数据库、任务只在进程内短暂保留、不会自动发送报告到 Gemini 的说明。
- Web 异步提交脚本补充失败/过期/查询异常后的按钮状态恢复，避免用户看到按钮长期停在“生成中...”。
- API 回归补充“Markdown 报告任务不写记录存储”的测试。
- README、HF Space README 和 `docs/deployment/huggingface-space.md` 同步免费自部署、隐私和发布门禁口径。

## 当前门禁状态

| 门禁 | 状态 | 说明 |
|---|---|---|
| 免费 Web 工作台可用性 | PASS | `/web` 使用服务端 HTML + 异步任务生成 Markdown |
| HF 官方免费 Space live health | PASS | `/health`、`/ready`、`/metrics` live 验证通过 |
| 用户自助部署文档 | PASS | 覆盖 HF Duplicate Space、GitHub + HF 手动 workflow、hf CLI |
| 默认隐私 / 存储口径 | PASS | 免费 Space 默认 `FATE_RECORDS_ENABLED=0`；报告任务不写记录库 |
| GitHub 自动验收回潮 | PASS | acceptance/container workflow 均为手动触发；quick CI 有脚本检查 |
| 本地质量门禁 | PASS | quick CI、ruff、format、mypy、focused regression 通过 |
| live Telegram Bot | SKIP | 免费 Web 工作台不依赖 Bot token；真实 Bot 验收需另传生产 token |
| 高并发公共服务 | 非目标 | 当前目标是用户可独立部署单实例；多副本高并发需外部队列/网关/WAF |

## 仍需保持的边界

- 不把免费 HF Space 描述成高并发公共服务。
- 不默认保存用户出生信息或 Markdown 报告。
- 不自动把报告发送到 Gemini、Telegram 或其他第三方。
- 不在 `/web` 引入未经批准的前端样式或复杂前端框架。
- 不把高级八字推理描述成 100% 专业断法；基础排盘可用，高级格局、合化成败、用神冲突和岁运专题仍按规则证据层继续治理。

## 下一步

- 将本轮变更提交并推送到 `main`。
- 推送后用本地脚本重新部署 HF Space，并验证线上 `/web` 包含新的隐私说明与按钮状态脚本。
- 若后续要声明 Bot 或高并发服务生产可用，必须另行提供真实 Bot token、真实域名/网关策略、外部队列或多副本限流证据。
