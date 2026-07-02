# Repo Evidence
- Docker daemon 可用：`docker version` 返回 client/server 29.1.3。
- `scripts/container-build.sh` 已能构建 `fatecat-delivery` 镜像。
- `scripts/container-smoke.sh` 已能启动容器并验证 `/health`、`/ready`、`/api/v1/bazi/pure-analysis`。
- `.github/workflows/container.yml` 已覆盖 CI 容器 build/smoke，并可在显式 `push_image` 时推送 GHCR。
- `scripts/live-release-gate.py` 当前只接受 `--container-digest sha256:<64 hex>`，缺构建/烟雾上下文。

# Constraints Matrix
| Constraint | Decision |
| --- | --- |
| 不伪造 registry digest | 本地 evidence 使用 imageId，RepoDigests 为空时明确标注 |
| 复用成熟能力 | 调用既有 container-build/container-smoke，不重写 Docker 构建流程 |
| 可机器校验 | live gate 校验 kind/status/imageId/smokeStatus/commit |
| CI 不应默认重建大镜像过多 | public-release 默认不强制 container evidence，使用显式 env 开启 |
| 不输出 secret | 不读取 registry token，不输出 Docker login 信息 |

# Change Boundary
- 可改：`scripts/container-release-evidence.*`、`scripts/live-release-gate.py`、`scripts/public-release-gate.sh`、`scripts/local-ci.sh`、delivery release gate/registry/docs、regression tests、0043 task docs。
- 禁改：真实 registry、GitHub Actions secrets、远端 CI 状态、Git 历史、生产服务。

# Risk Matrix
| Risk | Level | Mitigation |
| --- | --- | --- |
| 本地 imageId 被误解为 GHCR RepoDigest | medium | evidence `registryDigestPresent=false` 与 limitations 明确说明 |
| 容器 build 耗时 | medium | public-release 通过 env 显式开启，测试不默认构建 |
| 裸 digest 仍可传入 | low | 保留真实 registry digest 路径；新增 evidence path 更严格 |

# Assumptions and Falsification
- 假设：本地 container build+smoke+imageId 可作为仓库内 container release baseline。
- 反证：若 Docker 不可用、构建失败、smoke 失败或 imageId 不是 sha256，则 evidence 不能 pass。
- 假设：真实 live release 仍需要 registry RepoDigest 或远端 CI push 证据。
- 反证：若提供 GHCR RepoDigest，应通过 `--container-digest` 或后续 registry attestation 任务验证，不用本地 imageId 冒充。

- 调试模式: `Optional`

# Critical Ambiguities
- 无阻断歧义。真实 registry push 不在本任务范围。

# Debug Evidence Contract
- 本任务不是 bugfix；无需 `DEBUG.md`。若容器 build/smoke 失败，保留 container evidence JSON 和 Docker 输出摘要。

# Task Package Context Map
| Node | Context |
| --- | --- |
| TP-01.01 | Docker 可用，现有 build/smoke 脚本可复用 |
| TP-02.01 | 生成本地 container evidence JSON |
| TP-03.01 | live gate 校验 container JSON |
| TP-04.01 | public-release 可选接入，避免每次默认重建 |
| TP-05.01 | 真实构建/烟雾和 closeout |
