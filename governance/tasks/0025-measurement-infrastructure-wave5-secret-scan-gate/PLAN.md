# Planning Summary
本轮把 IMP-10 的“专用 secret scanner”从路线图缺口落成最小可用本地门禁。实现不引入外部服务，先用 stdlib scanner 覆盖高置信 secret 模式和 generic assignment，高风险命中阻断 quick CI；云端/成熟工具扫描后续再作为供应链增强。

# Lifecycle Gates
- SPEC：确认只做本地 secret scanner，不替代生产凭证审计。
- PLAN：任务树、验收、风险和 out-of-scope 落盘。
- BUILD：实现 scanner、allowlist、registry/schema、quick CI。
- TEST：scanner CLI、focused tests、ruff、format、quick CI、diff check。
- REVIEW：检查输出不泄露疑似密钥原文，不误宣称生产安全 100%。
- SHIP：task validators、全任务树验证和 closeout packet 通过。
- 不得跳过 gate。

# Simplest Path
复用 `git ls-files --cached --others --exclude-standard` 获取当前可提交候选文件，用 Python stdlib 正则、熵值、allowlist 和 JSON 输出实现门禁；不新增长期第三方依赖。

# Split Strategy
先实现 scanner 和 allowlist，再登记 SecurityControl、补测试和 quick CI，最后更新文档与任务 closeout。

# Execution Waves
| Wave | Nodes | Purpose |
| --- | --- | --- |
| Wave 1 | TP-01 | 缺口盘点和任务契约 |
| Wave 2 | TP-02 | scanner 与 allowlist |
| Wave 3 | TP-03 | registry/tests/docs/CI |
| Wave 4 | TP-04 | 验证与 closeout |

# Runtime Workflow Contract
- scanner 默认命令：`bash scripts/secret-scan.sh --output-json infra/runtime/local-state/exports/security/secret-scan.json`。
- 测试命令：`.venv/bin/python -m pytest -q tests/regression/test_secret_scan.py tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py -k 'secret or security'`。
- 输出 JSON 不保存疑似密钥原文；发现 finding 时返回非零退出码。

# Next Executable Leaves
- TP-04.01：执行 scanner、focused tests、ruff/format、quick CI 和 diff check。
- TP-04.02：回填 closeout 状态、全任务树验证和 closeout packet。

# Dependency Graph
```text
TP-01.01 -> TP-01.02 -> TP-02.01 -> TP-02.02 -> TP-03.01 -> TP-03.02 -> TP-03.03 -> TP-04.01 -> TP-04.02
```

# Rollback Protocol
- 恢复 `INDEX.md` 当前任务行
- 恢复本任务目录到初始化状态
- 删除 `scripts/secret-scan.py`、`scripts/secret-scan.sh` 和 `tests/regression/test_secret_scan.py`
- 恢复 security registry/schema/AGENTS、scripts/local-ci、scripts/AGENTS、API 文档和 roadmap 中的 secret scan 改动
- 不得影响其他任务目录
