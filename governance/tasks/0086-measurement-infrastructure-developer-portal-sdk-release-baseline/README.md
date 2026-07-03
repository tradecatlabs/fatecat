# Task Overview
- Task ID: `0086`
- Slug: `measurement-infrastructure-developer-portal-sdk-release-baseline`
- Objective: `把 developer portal、SDK release-readiness baseline、sandbox fixed output snapshot 和 portal gate 落成本地可执行的开发者接入基础设施切片。`
- Status: `Done`

## In Scope

- 新增 developer portal 机器契约和人类入口文档。
- 新增 SDK release-readiness manifest，锁定 package candidates、local smoke 和未发布边界。
- 新增 sandbox fixed output snapshot，只保存 canonical digest 和结构断言，不保存完整响应正文。
- 新增 developer portal gate，复用 OpenAPI/docs/platform/sandbox 现有能力，并接入 quick CI。
- 更新 API changelog、AGENTS、操作文档和 roadmap 口径。

## Out of Scope

- 不发布 PyPI/npm SDK。
- 不上线公网 developer portal。
- 不发行公网 sandbox token。
- 不保存真实 token、生产 URL、真实用户数据、非北京真实地区或报告正文。

## Task Package Tree
```text
TP-01 SPEC: 复核 developer platform 现状与 0086 缺口
  TP-01.01 复核 0067 baseline、sandbox、examples、docs smoke 和 roadmap
TP-02 PLAN: 定义 release baseline 边界
  TP-02.01 设计 portal / SDK release / snapshot / no-overclaim contract
TP-03 BUILD: 落地机器契约和文档
  TP-03.01 新增 developer portal、SDK release baseline、sandbox snapshot 和文档
TP-04 BUILD: 落地 gate 与 CI
  TP-04.01 新增 developer-portal-gate.py/.sh
  TP-04.02 接入 local-ci、tests、AGENTS、docs 和 changelog
TP-05 TEST/SHIP: 验证与交付
  TP-05.01 运行 syntax、gate、focused pytest 和 quick CI
  TP-05.02 明确提交、推送和远端 CI 由外层交付流汇报
```

## Requirement Alignment
| Requirement | Implementation |
| --- | --- |
| developer portal | `developer-portal.json` + `PORTAL.md` |
| SDK/package smoke | `sdk-release-baseline.json` + `developer-portal-gate.py` |
| fixed output snapshot | `sandbox-output-snapshot.json` + digest recomputation |
| no live overclaim | gate summary reports `externalPortalLive=false`、`publishedSdkPackages=0`、`liveSandboxTokenService=false` |
| local CI | `local-ci.sh` runs `developer-portal-gate.sh` and focused regression |

## Task Package Overview
| Node ID | Title | Status | Acceptance |
| --- | --- | --- | --- |
| TP-01 | SPEC | Done | existing developer baseline and 0086 gap inspected |
| TP-01.01 | 复核现状 | Done | developer contracts/docs/scripts inspected |
| TP-02 | PLAN | Done | release baseline and no-overclaim boundaries defined |
| TP-02.01 | contract design | Done | portal/sdk/snapshot boundary defined |
| TP-03 | BUILD | Done | contracts and docs added |
| TP-03.01 | contracts/docs | Done | machine and human entries exist |
| TP-04 | BUILD | Done | gate and wiring added |
| TP-04.01 | gate | Done | developer portal gate smoke passed |
| TP-04.02 | wiring | Done | local-ci/tests/AGENTS/docs/changelog updated |
| TP-05 | TEST/SHIP | Done | quick CI passed; remote CI handled by outer delivery flow |
| TP-05.01 | validation | Done | syntax、gate、focused pytest、quick CI passed |
| TP-05.02 | delivery boundary | Done | task snapshot does not pre-claim remote CI |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md

## Key Deliverables

- `contracts/fate/developer/developer-portal.json`
- `contracts/fate/developer/sdk-release-baseline.json`
- `contracts/fate/developer/sandbox-output-snapshot.json`
- `docs/reference-materials/developer/PORTAL.md`
- `docs/reference-materials/developer/SDK_RELEASE_BASELINE.md`
- `scripts/developer-portal-gate.py`
- `scripts/developer-portal-gate.sh`
- `tests/regression/test_developer_portal_gate.py`
