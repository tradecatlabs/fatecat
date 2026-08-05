# Task-Level Acceptance
- 每个独立任务一个 Markdown SOP，不合并多个目标。
- 每份 SOP 包含任务定义、适用场景、输入要求、前置条件、默认工具链、固定路径、成熟参数、分步执行流程、幂等与增量策略、限速与并发规则、输出目录、命名规范、质量验收门禁、失败处理、恢复与重试策略、安全边界、临时文件清理、运行记录登记和明确禁止事项。
- 总索引覆盖全部 SOP，route key 和 route alias 全局唯一。
- tracked 脚本、contract 和固定路径存在。
- planned capability 显式标记状态、验证缺口和投产门禁。

# Validation Plan
```bash
.venv/bin/python -m pytest -q tests/regression/test_sop_library.py
python3 governance/tools/rebuild_governance_index.py --project-root .
python3 governance/tools/validate_governance_package.py --project-root . --strict
python3 governance/tools/governance_health_report.py --project-root . --strict
bash scripts/local-ci.sh --profile quick
```

# Review Gate
- Correctness：命令、参数、路径和状态与 tracked 真相源一致。
- Architecture：`governance/processes/sops/` 是唯一 SOP 真相源。
- Safety：外部副作用、密钥、隐私、版权和删除操作 fail closed。
- Ponytail：不新增重复 wrapper、运行时或生成框架。

# Runtime Verification Gate
- focused regression 必须验证 SOP 数量、章节、路由唯一性、capability 状态和脚本路径。
- governance strict 与 health 必须通过本任务新增资产校验。
- Quick CI 必须证明新增测试未破坏仓库默认快速门禁。
- 外部 live、生产 token、数据库、Bot 和公网 webhook 不属于本任务运行时验证。

# Ship Readiness
- 所有 TP 节点 Done。
- 工作树 diff 通过 `git diff --check`。
- SOP 索引与文件集合完全相等。
- 不存在 planned capability 可生产执行的表述。
- 不自动 commit、push 或 deploy；版本交付需用户单独授权。

# Task Package Acceptance
| Node | Acceptance |
| --- | --- |
| TP-01 | 分类、状态来源和唯一路由契约锁定 |
| TP-02 | capability SOP 完整且 planned 能力 fail closed |
| TP-03 | 数据、评测和开发质量 SOP 复用现有工具 |
| TP-04 | 分发、生产、发布和审计 SOP 明确外部边界 |
| TP-05 | focused、task、governance、Quick CI 和 review 完成 |

# Anti-Goals
- 不以 SOP 文档证明外部 live 已通过。
- 不把 planned capability 写成可执行能力。
- 不把一次性历史任务逐条复制为长期流程。
- 不自动执行 push、deploy、delete 或真实生产请求。
