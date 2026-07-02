# Task-Level Acceptance

- AsyncEvent schema 存在，并声明 required fields、CloudEvents required context、event domains、delivery semantics 和隐私不变量。
- Event registry 登记 job、webhook、evaluation、release 四个事件域，至少包含 5 个事件。
- AsyncAPI 风格文档存在，版本为 `3.1.0`，包含 channels、operations、messages 和 examples。
- 每个示例均为 synthetic CloudEvent，包含 `id/source/specversion/type/data`。
- Delivery registry 和 resource schema 链接 AsyncEvent。
- Gate CLI 可输出 `kind=fatecat.event_contract_gate` 的 JSON，且 status 为 passed。
- Gate 强制 webhook delivery 仍为 `requires_real_receiver`，不声明公网 live delivery 已完成。
- Gate summary、registry、examples、docs 不包含真实 webhook URL、token、secret、password、用户输入、出生地区、报告正文或生产日志。
- quick local CI 包含 `eventContractGate` artifact。
- 文档明确本轮不实现外部 broker、事件订阅端或真实公网 webhook live delivery。

# Validation Plan

| 验证项 | 命令 | 期望 |
| --- | --- | --- |
| JSON syntax | `python3 -m json.tool contracts/fate/delivery/events.json` 等 | pass |
| syntax | `python3 -m py_compile scripts/event-contract-gate.py` | pass |
| shell syntax | `bash -n scripts/event-contract-gate.sh scripts/local-ci.sh` | pass |
| gate CLI | `bash scripts/event-contract-gate.sh --output-json /tmp/fatecat-event-contract-gate.json` | pass |
| focused tests | `.venv/bin/python -m pytest -q tests/regression/test_event_contract_gate.py tests/regression/test_capability_protocol.py -k "async_event or event_contract"` | pass |
| ruff | `.venv/bin/python -m ruff check ... && .venv/bin/python -m ruff format --check ...` | pass |
| secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0063.json` | pass |
| task docs | `validate_task_docs.py --phase closeout` | pass |
| task tree | `validate_tasks_tree.py --phase auto` | pass |
| quick local CI | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0063` | pass |

# Review Gate

| 维度 | Gate |
| --- | --- |
| 正确性 | Registry、AsyncAPI 文档和 examples 对事件类型、message、channel、operation 一致。 |
| 安全 | 不保存真实 webhook URL、secret、token、password、用户输入、出生地区、报告正文或生产日志。 |
| 架构 | AsyncEvent 是 delivery/event 资源，不污染命理核心和 runtime 投递实现。 |
| 性能 | 只新增静态 gate，无 runtime hot path 影响。 |
| 可维护 | Gate 使用标准库 Python，local-ci 可重复执行。 |
| 不夸大 | 文档和 gate limits 明确 contract baseline 不等于外部 broker 或 live webhook 已生产。 |

# Runtime Verification Gate

- 本地可验证：schema/registry/AsyncAPI/examples/gate/test/local-ci。
- 外部连通验证待执行：真实公网 webhook receiver、外部 broker、事件订阅端、生产投递日志、第三方消费者兼容性。

# Ship Readiness

- TODO 全部勾选。
- STATUS 全节点 Done。
- 验证命令写入 Recent Evidence。
- 工作树提交推送后应 clean。

# Task Package Acceptance

- 0063 任务文档无占位符。
- `INDEX.md` 0063 状态同步。
- `ACCEPTANCE_CHECKLIST.md` 覆盖所有叶子节点。

# Anti-Goals

- 不实现真实公网 webhook live delivery。
- 不连接外部 broker 或消息队列。
- 不声明事件平台、事件订阅、生产 at-least-once 或 exactly-once 已完成。
