---
id: SOP-DIST-CONTAINER-BUILD-SMOKE
type: process
status: current
owner: platform
route_key: build_smoke_container
route_aliases: ["构建 Docker 镜像", "运行容器 smoke", "验证 delivery image"]
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P60D
---

# 构建并验证容器镜像

## 任务定义
构建 FateCat delivery image，启动一次性容器并验证健康、就绪和八字 API，然后自动回收。

## 当前状态
本地 Docker build/smoke 成熟；registry push/attestation 需独立发布授权。

## 适用场景
Dockerfile、生产依赖、entrypoint、delivery 或容器发布候选变更。

## 输入要求
image tag；可选 Dockerfile/progress/host/port/startup timeout/skip-build。

## 前置条件
Docker daemon 可用；目标端口空闲；本地源码门禁至少 quick 通过。

## 默认工具链
`bash scripts/container-build.sh --image fatecat-delivery:local --progress plain`，随后 `container-smoke.sh --skip-build`。

## 固定路径
`infra/docker/Dockerfile.delivery`、`entrypoint.delivery.sh`、container build/smoke scripts、`compose.yaml`。

## 成熟参数
默认 image `fatecat-delivery:local`；smoke 默认临时容器，覆盖 `/health` 和 `/api/v1/bazi/pure-analysis`；CI startup timeout 90 秒。

## 分步执行流程
1. 运行 quick gate。
2. 构建明确 tag。
3. smoke 使用唯一端口并 `--skip-build`。
4. 检查容器日志、health、ready、API。
5. 验证无残留容器后记录 image ID/hash。

## 幂等与增量策略
相同 build context/lock 应可重建；验收使用新 tag 或明确覆盖 local tag，不复用未知镜像。

## 限速与并发规则
构建由 Docker 控制；smoke 端口唯一；同机并行需不同 tag/port且资源有界。

## 输出目录
Docker image store；smoke 临时文件 `/tmp/fatecat-container-*`；release artifact 另行生成。

## 命名规范
本地 `fatecat-delivery:<short-sha>`；registry `ghcr.io/<owner>/fatecat-delivery:<tag>`。

## 质量验收门禁
build exit 0、healthcheck、container smoke、生产依赖 lock、无残留和 Quick CI。

## 失败处理
构建层、启动、health 或 API 失败时保留日志，停止/删除容器并 block。

## 恢复与重试策略
修复 Dockerfile/dependency/app 后重建；仅 registry/network 瞬时错误有限重试。

## 安全边界
不 bake secret；非 root/最小依赖按 Dockerfile contract；不映射未授权 host 路径。

## 临时文件清理
自动删除 smoke 容器；删除失败 tag/cache前确认不被其他任务使用。

## 运行记录登记
记录 commit、Dockerfile/lock hash、image ID/tag/size、smoke 和日志摘要。

## 明确禁止事项
- 禁止跳过 smoke 推送。
- 禁止在镜像层写 token/.env。
- 禁止把本地 image ID 当 registry digest。
