# Task Overview
- Task ID: `0043`
- Slug: `measurement-infrastructure-container-release-evidence`
- Objective: `把 live release gate 中的 evidence.container_digest 从裸 sha256 字符串推进为本地可生成、可校验、可交给发布门禁消费的 container release evidence baseline：新增 container-release-evidence 脚本，复用既有 container-build/container-smoke，记录 image、imageId sha256、RepoDigests、build/smoke status、pushExecuted=false、commit 和限制说明；让 live-release-gate 校验 container evidence JSON 内容，同时保留 --container-digest 作为真实 registry digest 输入；让 public-release-gate 可生成并传递本地 container evidence；补回归测试、文档、任务 closeout。范围不包含真实 registry push、GHCR RepoDigest、远端 CI 或清理当前脏工作树。`
- Status: `Done`

## In Scope
- 新增 `scripts/container-release-evidence.py` 与 `scripts/container-release-evidence.sh`。
- 复用 `scripts/container-build.sh` 和 `scripts/container-smoke.sh`，生成本地 container evidence JSON。
- `live-release-gate.py` 支持 `--container-evidence-path` 内容校验，同时保留 `--container-digest`。
- `public-release-gate.sh` 可选生成并传递本地 container evidence。
- 回归测试、文档、任务 closeout。

## Out of Scope
- 不 push registry。
- 不声明 GHCR RepoDigest 已存在。
- 不执行远端 CI。
- 不清理或提交当前脏工作树。

## Task Package Tree
```text
ROOT
├── TP-01 现状与边界确认
│   └── TP-01.01 盘点 container gate 和已有容器脚本
├── TP-02 container evidence 生成
│   └── TP-02.01 新增 container-release-evidence 脚本
├── TP-03 live gate 校验
│   └── TP-03.01 校验 container evidence JSON 内容
├── TP-04 发布门禁接入
│   └── TP-04.01 public-release/local-ci 文档契约接入
└── TP-05 验证与 closeout
    └── TP-05.01 运行容器 smoke、pytest 和任务树 closeout
```

## Requirement Alignment
- 对齐 0039 live release gate：`evidence.container_digest` 是 required evidence，不应只接受裸字符串而缺构建/烟雾上下文。
- 对齐基础设施目标：容器发布物必须可构建、可烟雾、可追溯 commit。
- 对齐安全边界：本地 image ID baseline 不等于 registry RepoDigest。

## Task Package Overview
| ID | Name | Status | Verify |
| --- | --- | --- | --- |
| TP-01.01 | container 现状盘点 | Done | `docker version` 与脚本阅读 |
| TP-02.01 | container evidence 生成器 | Done | `bash scripts/container-release-evidence.sh --output-json /tmp/fatecat-container-release-0043.json` |
| TP-03.01 | live gate 内容校验 | Done | pytest pass/fail |
| TP-04.01 | public-release 接入 | Done | final live gate container pass |
| TP-05.01 | 验证 closeout | Done | task tree valid |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
