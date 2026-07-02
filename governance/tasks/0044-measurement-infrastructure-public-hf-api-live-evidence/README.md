# Task Overview
- Task ID: `0044`
- Slug: `measurement-infrastructure-public-hf-api-live-evidence`
- Objective: `把 live release gate 中已可通过的公开 Hugging Face Space/API 外部连通证据落成任务树 closeout：使用现有 live-release-gate 以 https://tradecatlabs-fatecat.hf.space 同时验证 production_api_live 与 hf_space_live，结合本地 local_ci、container、SBOM、provenance、rollback 证据，输出机器可读 gate JSON；记录 passed=7、pending=3 的真实结果，更新 roadmap 剩余缺口。范围不包含 Telegram Bot token、远端 GitHub Actions 当前 commit、clean git/提交推送或生产私有域名。`
- Status: `Done`

## In Scope
- 使用 `scripts/live-release-gate.sh` 验证公开 HF Space/API：`https://tradecatlabs-fatecat.hf.space`。
- 结合本地 quick CI、container、SBOM、provenance、rollback evidence。
- 记录 `passed=7,pending=3,failed=0` 的真实 gate 结果。
- 更新 roadmap 剩余缺口。

## Out of Scope
- 不提供 Telegram Bot token。
- 不执行远端 GitHub Actions。
- 不清理或提交当前 worktree。
- 不声明私有生产域名已验证。

## Task Package Tree
```text
ROOT
├── TP-01 外部连通证据执行
│   └── TP-01.01 运行 HF Space/API live gate
├── TP-02 证据归档
│   └── TP-02.01 记录 gate JSON 和剩余缺口
└── TP-03 closeout
    └── TP-03.01 更新 roadmap、生成 closeout、校验任务树
```

## Requirement Alignment
- 对齐 100% 基础设施目标：真实外部连通证据必须来自命令输出，不得写成推断。
- 对齐 live release gate：只把公开 HF/API 真实通过项计入 pass；Bot、远端 CI、clean git 继续 pending。

## Task Package Overview
| ID | Name | Status | Verify |
| --- | --- | --- | --- |
| TP-01.01 | HF Space/API live gate | Done | `live-release-gate.sh --api-url ... --hf-space-url ...` |
| TP-02.01 | 证据归档 | Done | `/tmp/fatecat-live-release-gate-public-hf-0043.json` |
| TP-03.01 | closeout | Done | task tree valid |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
