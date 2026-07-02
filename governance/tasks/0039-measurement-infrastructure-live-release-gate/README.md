# Task Overview
- Task ID: `0039`
- Slug: `measurement-infrastructure-live-release-gate`
- Objective: `把测算基础设施最后一段发布准入收束为可审计的 live release gate：新增 release evidence 契约、live release gate 脚本、外部证据 JSON 输出、真实 API/HF Space/Bot/远端 CI/container digest/SBOM-provenance 的机器可读验收口径，并接入 public-release/local-ci、delivery registry、roadmap、AGENTS 与任务 closeout；没有真实外部域名、token、HF/CI 权限时只标注外部连通验证待执行，不伪造 live 通过。`
- Status: `Done`

## In Scope
- 新增 ReleaseGate 资源契约和 release evidence schema。
- 新增 `scripts/live-release-gate.py` / `scripts/live-release-gate.sh`，输出机器可读 JSON。
- 将 live release gate 接入 `scripts/public-release-gate.sh` 和 `scripts/local-ci.sh --profile quick` 的本地合同检查。
- 在 `/surfaces` 交付面 registry 响应中暴露 `releaseGate` 元信息。
- 增加回归测试，覆盖本地合同通过、`shipGate=blocked`、`--require-live` 缺证据失败。
- 同步 delivery/scripts AGENTS、API 接入文档、100% roadmap 和任务 closeout。

## Out of Scope
- 不连接真实生产 API、Hugging Face Space、Telegram Bot、GitHub Actions、registry 或 SIEM。
- 不生成真实 SBOM/provenance artifact。
- 不执行真实 rollback drill。
- 不提交、不推送、不伪造远端 CI 或 live smoke 结果。

## Task Package Tree
```text
TP-01 盘点发布证据缺口
  TP-01.01 对齐现有 production-readiness/public-release/local-ci/HF/Bot/container 脚本
TP-02 ReleaseGate 契约
  TP-02.01 新增 release-gate schema 与 contract
  TP-02.02 接入 delivery registry 与 resource schema
TP-03 Live release gate 执行器
  TP-03.01 新增 live-release-gate Python/shell 脚本
  TP-03.02 接入 public-release/local-ci
TP-04 回归与 API 暴露
  TP-04.01 增加 release gate 回归测试
  TP-04.02 暴露 /surfaces releaseGate 元信息
TP-05 文档与 closeout
  TP-05.01 同步 AGENTS、API 文档、roadmap
  TP-05.02 运行验证、回填任务文档并生成 closeout packet
```

## Requirement Alignment
- 目标要求“100% 基础设施”不能靠口号，0039 将最终发布证据压成机器可读 gate。
- 真实外部项没有凭证时必须标注 `externalConnectivity` 和 `shipGate=blocked`。
- 本地可验证部分以脚本、contract、tests、local-ci 集成和任务 closeout 证明。

## Task Package Overview
| Node | Status | Evidence |
| --- | --- | --- |
| TP-01.01 | Done | `sed`/`rg` 盘点 `production-readiness.sh`、`public-release-gate.sh`、`local-ci.sh`、`live-bot-smoke.sh`、`container-release.sh`、HF workflow |
| TP-02.01 | Done | `contracts/fate/delivery/schemas/release-gate.schema.json`、`contracts/fate/delivery/release-gate.json` |
| TP-02.02 | Done | `contracts/fate/delivery/registry.json`、`contracts/fate/capabilities/schemas/resource.schema.json` |
| TP-03.01 | Done | `scripts/live-release-gate.py`、`scripts/live-release-gate.sh` |
| TP-03.02 | Done | `scripts/public-release-gate.sh`、`scripts/local-ci.sh` |
| TP-04.01 | Done | `tests/regression/test_live_release_gate.py` 与联动回归 |
| TP-04.02 | Done | `domains/experience-delivery/services/fatecat-delivery/src/main.py::_delivery_surface_registry_payload` |
| TP-05.01 | Done | `contracts/fate/delivery/AGENTS.md`、`scripts/AGENTS.md`、API 接入文档、100% roadmap |
| TP-05.02 | Done | 本地验证通过；closeout packet 待生成后作为最终证据 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
