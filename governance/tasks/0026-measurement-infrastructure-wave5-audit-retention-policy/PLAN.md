# Planning Summary
本轮把审计日志与 retention policy 从“路线图缺口”推进为本地可验证 baseline：runtime 输出脱敏 audit_event，registry 登记 audit_log/retention 控制，测试证明关键动作有事件且不泄露原文。

# Lifecycle Gates
- SPEC：确认本任务只做本地 audit_event 和 retention baseline。
- PLAN：任务树、验收、风险和 out-of-scope 落盘。
- BUILD：实现 audit helper、runtime 接入、registry/schema。
- TEST：focused tests、secret scan、ruff、format、quick CI、diff check。
- REVIEW：检查 audit_event 不泄露敏感原文，不夸大为外部审计平台。
- SHIP：task validators、全任务树验证和 closeout packet 通过。
- 不得跳过 gate。

# Simplest Path
复用现有结构化 logger 和 requestId 上下文，只新增薄 helper；retention 先资源化现有 report job TTL、audit retention days metadata 和用户记录显式删除模式。

# Split Strategy
先实现 runtime audit event，再登记 SecurityControl，随后补测试、文档和任务 closeout。

# Execution Waves
| Wave | Nodes | Purpose |
| --- | --- | --- |
| Wave 1 | TP-01 | 缺口盘点和任务契约 |
| Wave 2 | TP-02 | runtime audit event |
| Wave 3 | TP-03 | registry/tests/docs |
| Wave 4 | TP-04 | 验证与 closeout |

# Runtime Workflow Contract
- audit event 通过服务 logger 输出 JSON：`event=audit_event`。
- focused test：`.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py -k 'audit_event or retention or security'`。
- audit payload 不保存 token、请求体、报告正文、姓名、出生地区、recordId、jobId 或 userId 原文。

# Next Executable Leaves
- TP-04.01：执行 focused tests、secret scan、ruff/format、quick CI 和 diff check。
- TP-04.02：回填 closeout 状态、全任务树验证和 closeout packet。

# Dependency Graph
```text
TP-01.01 -> TP-01.02 -> TP-02.01 -> TP-02.02 -> TP-03.01 -> TP-03.02 -> TP-03.03 -> TP-04.01 -> TP-04.02
```

# Rollback Protocol
- 恢复 `INDEX.md` 当前任务行
- 恢复本任务目录到初始化状态
- 恢复 `main.py` 中 audit_event helper 与调用点。
- 恢复 security schema/registry、tests、docs 和 AGENTS 的 audit/retention 改动。
- 不得影响其他任务目录
