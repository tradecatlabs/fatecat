---
id: SOP-DIST-HF-SPACE-DEPLOY
type: process
status: current
owner: platform
route_key: deploy_huggingface_space
route_aliases: ["更新 HF Space", "部署 Hugging Face", "同步 Space 生产"]
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P30D
---

# 部署 Hugging Face Space

## 任务定义
生成最小 Docker Space bundle，并在明确目标、身份和授权下创建或更新 Hugging Face Space。

## 当前状态
本地 hf CLI 与 GitHub workflow 部署入口成熟；真实部署需要 HF token 和远端权限。

## 适用场景
官方/用户 Space 更新、dry-run bundle 审查或 GitHub workflow 手动部署。

## 输入要求
Space ID、bundle dir、commit message、token 来源、visibility、是否 prune；不得在命令文本暴露 token。

## 前置条件
Git clean且目标 commit 已通过 public release gate；`hf auth whoami` 身份与目标 owner 一致或显式授权 mismatch。

## 默认工具链
先 `bash scripts/hf-space-deploy.sh --dry-run --bundle-dir /tmp/fatecat-hf-space`，再用 `--space ... --prune-remote` 部署。

## 固定路径
`scripts/hf-space-deploy.sh`、`infra/huggingface-space/`、`docs/deployment/huggingface-space.md`、workflow `hf-space-deploy.yml`。

## 成熟参数
官方默认 `tradecatlabs/fatecat`；free Space port 7860、inflight 1、queue 20、worker 1、TTL 1800、records disabled。

## 分步执行流程
1. 运行 public release gate 和 Git 状态检查。
2. 生成 dry-run bundle并审计文件/hash。
3. 验证 hf identity、目标和 visibility。
4. 执行上传；仅需要时 `--prune-remote`。
5. 等待 build，验证 `/health`、`/ready`、`/metrics`、`/web` 和版本。

## 幂等与增量策略
bundle 从当前 commit 全量生成；同 commit 可重复上传；prune 只删除 bundle 外远端文件且需明确授权。

## 限速与并发规则
同一 Space 一次只部署一个 commit；等待 build 完成后再触发下一次；不并发 prune。

## 输出目录
本地 bundle `/tmp/fatecat-hf-space`；远端 `spaces/<owner>/<name>`；部署证据写 local-state exports。

## 命名规范
commit message `deploy FateCat from <source> <sha>`；证据 `hf-deploy-<space-slug>-<short-sha>.json`。

## 质量验收门禁
bundle hygiene、HF upload commit、Space build running、线上端点、GEO audit、本地/线上版本和 HTML 语义一致。

## 失败处理
身份、token、upload、build 或 endpoint 失败时停止；不覆盖到其他 owner/Space。

## 恢复与重试策略
瞬时上传/build 可在同 bundle 有限重试；代码失败修复新 commit；必要时部署上一已验证 commit。

## 安全边界
HF token 只来自 secret；public Space 不存用户数据库；日志不输出 token/报告；prune 是高风险副作用。

## 临时文件清理
验证后删除 bundle和 hf 临时 cache；保留 deployment commit/hash 和 live evidence。

## 运行记录登记
记录 source commit、Space ID、visibility、bundle hash、HF commit、build状态、端点和回滚版本。

## 明确禁止事项
- 禁止直接同步整个 monorepo 到 Space 根。
- 禁止未检查身份使用 `--allow-auth-mismatch`。
- 禁止部署成功前宣称线上已更新。
