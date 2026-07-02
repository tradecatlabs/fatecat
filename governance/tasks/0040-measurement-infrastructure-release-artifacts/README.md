# Task Overview
- Task ID: `0040`
- Slug: `measurement-infrastructure-release-artifacts`
- Objective: `把 0039 live release gate 中的 SBOM/provenance 从纯 pending 推进为本地可生成、可校验、可交给发布门禁消费的 release artifacts baseline：新增 release artifact 生成脚本，基于 pyproject、requirements lock、Dockerfile、关键 contracts/scripts 生成 CycloneDX 兼容 SBOM、SLSA/in-toto 风格 provenance 和 manifest，接入 live-release/public-release/local-ci、回归测试、文档、roadmap 和任务 closeout；不推送 registry、不声明远端 CI attestation、不伪造 container digest 或真实生产发布。`
- Status: `Done`

## In Scope
- 新增本地 release artifacts 生成器：SBOM、provenance、manifest。
- 将 artifacts 接入 public release gate、local-ci 和 live release gate 参数。
- 增加回归测试，验证 artifact 结构、校验模式和 live release gate 消费。
- 同步 release gate contract、delivery registry、scripts AGENTS、API 文档、roadmap 和任务 closeout。

## Out of Scope
- 不推送 container registry。
- 不生成 container digest、cosign signature、远端 CI attestation 或 GitHub release artifact。
- 不执行真实生产发布、HF live、Bot live 或 rollback drill。

## Task Package Tree
```text
TP-01 盘点 release artifact 缺口
  TP-01.01 读取 0039 gate、lockfile、Dockerfile 和现有供应链脚本
TP-02 Release artifact 生成器
  TP-02.01 新增 release-artifacts Python/shell 脚本
  TP-02.02 输出 SBOM、provenance 和 manifest，并支持 verify
TP-03 Gate 接入
  TP-03.01 接入 public-release/local-ci
  TP-03.02 确认 live-release-gate 可消费生成 artifact
TP-04 回归与文档
  TP-04.01 新增 release artifacts 回归测试
  TP-04.02 同步合同、AGENTS、API 文档和 roadmap
TP-05 验证与 closeout
  TP-05.01 运行本地验证、回填任务状态并生成 closeout
```

## Requirement Alignment
- 0039 已经要求 SBOM/provenance artifact；0040 把这两个项从“纯 pending”推进到“本地可生成且可校验”。
- 仍不把本地 artifact 冒充远端 CI attestation 或 registry signature。

## Task Package Overview
| Node | Status | Evidence |
| --- | --- | --- |
| TP-01.01 | Done | `rg -n "SBOM|provenance|release artifact"` 和 lockfile/Dockerfile 盘点 |
| TP-02.01 | Done | `scripts/release-artifacts.py`、`scripts/release-artifacts.sh` |
| TP-02.02 | Done | `/tmp/fatecat-release-artifacts-0040` 生成 3 个 JSON artifact |
| TP-03.01 | Done | `scripts/public-release-gate.sh`、`scripts/local-ci.sh` 已接入 |
| TP-03.02 | Done | `live-release-gate` 对 SBOM/provenance checks 返回 `pass` |
| TP-04.01 | Done | `tests/regression/test_release_artifacts.py` |
| TP-04.02 | Done | release gate contract、registry、AGENTS、API 文档、roadmap 已同步 |
| TP-05.01 | Done | 验证与 closeout |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
