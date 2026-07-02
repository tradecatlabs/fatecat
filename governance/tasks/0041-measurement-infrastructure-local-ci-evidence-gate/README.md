# Task Overview
- Task ID: `0041`
- Slug: `measurement-infrastructure-local-ci-evidence-gate`
- Objective: `把 live release gate 中的 evidence.local_ci_quick 从仅检查 summary 文件存在推进为可校验的本地 quick CI 证据：让 local-ci 生成机器可读 summary JSON，记录 profile、status、commit、startedAt/finishedAt、关键 artifact 路径和 live gate summary；让 live-release-gate 校验 summary 内容必须证明 profile=quick 且 status=passed 且 commit 匹配当前 HEAD；让 public-release-gate 在执行 local-ci quick 时把该 summary 传给 live gate；补回归测试、任务文档和 closeout。范围不包含远端 CI、真实生产 API/HF/Bot、container digest、rollback drill 或清理当前脏工作树。`
- Status: `Done`

## In Scope
- `scripts/local-ci.sh` 生成机器可读 quick CI summary JSON。
- `scripts/live-release-gate.py` 校验 local CI summary 内容，而不是只检查路径存在。
- `scripts/public-release-gate.sh` 在执行 local-ci quick 时把 summary JSON 传给 live gate。
- 回归测试覆盖 pass、缺失、错误 profile、错误 commit、public-release 接线。
- 同步 release gate 契约、脚本文档、roadmap 与任务 closeout。

## Out of Scope
- 不调用远端 GitHub Actions。
- 不做真实生产 API/HF Space/Telegram Bot live smoke。
- 不生成或验证 container registry digest。
- 不执行 rollback drill。
- 不清理或提交当前脏工作树。

## Task Package Tree
```text
ROOT
├── TP-01 现状与证据缺口确认
│   └── TP-01.01 确认 local-ci 已跑但 live gate 仍 pending 的原因
├── TP-02 local-ci summary 生成
│   └── TP-02.01 输出 local-ci-summary.json 并保留 summary.txt
├── TP-03 live gate 校验增强
│   └── TP-03.01 校验 summary profile/status/commit/artifact
├── TP-04 public-release 接线
│   └── TP-04.01 传递 local-ci quick summary 到 live gate
└── TP-05 验证与收口
    └── TP-05.01 回归测试、quick 验证、任务树 closeout
```

## Requirement Alignment
- 对齐 100% 测算基础设施目标：发布准入证据必须机器可读、可复核、不可凭文件存在冒充通过。
- 对齐 0039 live release gate：`evidence.local_ci_quick` 是 required evidence，必须有真实本地 CI 证据。
- 对齐 0040 release artifacts：本地可生成证据应自动接入 public release gate。
- 明确边界：本任务只推进本地 quick CI 证据，不伪造外部 live release 证据。

## Task Package Overview
| ID | Name | Status | Verify |
| --- | --- | --- | --- |
| TP-01.01 | 现状与证据缺口确认 | Done | `rg local_ci_summary scripts tests` |
| TP-02.01 | local-ci summary 生成 | Done | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0041` 产生 JSON |
| TP-03.01 | live gate 校验增强 | Done | pytest 覆盖 pass/fail 分支 |
| TP-04.01 | public-release 接线 | Done | public-release 默认路径最终 live gate `passed=3,pending=7` |
| TP-05.01 | 验证与收口 | Done | quick CI、task docs、closeout |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
