# Planning Summary
把安全能力从静态发现推进到本地可执行 smoke：用最小脚本直接调用现有 FastAPI app，不引入新安全框架，不创建虚假的生产验证；用 JSON summary、回归测试和 quick CI 把当前安全边界固化。

# Lifecycle Gates
- SPEC：确认只覆盖本地可验证安全控制，生产外部验证保持待执行。
- PLAN：任务树、验收、风险和 out-of-scope 落盘。
- BUILD：实现 smoke、registry metadata、AGENTS 说明。
- TEST：focused tests、ruff、format、quick CI、diff check。
- REVIEW：检查输出不泄露 token/secret/DSN，不夸大为生产安全体系完成。
- SHIP：task validators、全任务树验证和 closeout packet 通过。
- 不得跳过 gate。

# Simplest Path
复用现有 FastAPI `TestClient`、现有安全控制和现有文件门禁脚本；自研代码只做编排、断言和 JSON summary 输出。

# Split Strategy
先盘点并回填任务契约，再实现脚本和 metadata，随后同步测试、文档、quick CI，最后集中跑门禁与 closeout。

# Execution Waves
| Wave | Nodes | Purpose |
| --- | --- | --- |
| Wave 1 | TP-01 | 任务契约和缺口盘点 |
| Wave 2 | TP-02 | smoke 实现和 registry 登记 |
| Wave 3 | TP-03 | 测试、文档和 quick CI |
| Wave 4 | TP-04 | 验证、状态和 closeout |

# Runtime Workflow Contract
- smoke 默认命令：`bash scripts/security-smoke.sh --output-json infra/runtime/local-state/exports/security/smoke.json`。
- 测试命令：`.venv/bin/python -m pytest -q tests/regression/test_security_smoke.py tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py -k 'security or smoke'`。
- 测试内可使用 `--skip-file-gates`，但正式 CLI smoke 默认串联文件门禁。
- 输出 JSON 只保留检查名、状态、时间戳、scope 和 summary，不记录真实请求体、报告正文或密钥值。

# Next Executable Leaves
- TP-04.01：执行 smoke、focused tests、ruff/format、quick CI 和 diff check。
- TP-04.02：回填 closeout 状态、全任务树验证和 closeout packet。

# Dependency Graph
```text
TP-01.01 -> TP-01.02 -> TP-02.01 -> TP-02.02 -> TP-03.01 -> TP-03.02 -> TP-03.03 -> TP-04.01 -> TP-04.02
```

# Rollback Protocol
- 恢复 `INDEX.md` 当前任务行
- 恢复本任务目录到初始化状态
- 删除 `scripts/security-smoke.py`、`scripts/security-smoke.sh` 和 `tests/regression/test_security_smoke.py`
- 恢复 security registry、AGENTS、quick CI、contract/API tests、docs 和 roadmap 对 security smoke 的新增引用
- 不得影响其他任务目录
