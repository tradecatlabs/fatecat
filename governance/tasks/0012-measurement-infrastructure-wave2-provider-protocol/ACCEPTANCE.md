# Task-Level Acceptance
- 生产 capability 不再由 executor 内部函数表直接执行，而是通过 provider registry 查找 provider object。
- provider object 至少提供 `validate`、`calculate`、`metadata`、`health`。
- `bazi`、`ziwei`、`almanac`、`meihua` 四个 production capability 均可执行，现有输出结构不退化。
- planned capability 继续拒绝执行。
- API metadata 暴露 provider 元信息和 health，不泄露敏感信息。
- 局部 AGENTS、100% 计划和任务文档同步。

# Validation Plan
- `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py -k 'capability or provider or metadata or openapi or error or report_job'`
- `ruff check` / `ruff format --check` 覆盖修改的 Python 文件和测试。
- `mypy domains/fate-analysis/services/fate-core/src/fate_core`
- `bash scripts/local-ci.sh --profile quick`
- `python3 governance/tools/validate_governance_package.py --project-root . --strict`
- `validate_task_docs.py --phase closeout`
- `validate_tasks_tree.py --phase auto`
- `git diff --check`

# Review Gate
- Provider 协议不得引入未使用的大抽象。
- Executor 不得重新出现 capability if/else 或散落函数路由。
- planned gate、默认 bazi gate、risk policy 和 evidence policy 不得被削弱。
- 文档不能声明跨进程 job store、webhook、SDK、生产实测已完成。

# Runtime Verification Gate
- 本轮只验证本地进程内 provider 协议。
- 外部连通验证待执行：真实域名、token、Bot live smoke、webhook 回调。

# Ship Readiness
- 任务可 closeout 的条件：代码、测试、文档、任务容器和 diff 卫生均有真实命令证据。

# Task Package Acceptance
| Node | Acceptance |
| --- | --- |
| TP-01.01 | Provider 协议可被类型检查和测试消费。 |
| TP-01.02 | Production provider registry 覆盖现有 production capabilities。 |
| TP-02.01 | Executor 通过 provider registry 执行，不再内置 handler 表。 |
| TP-02.02 | Metadata/health/error context 可审计。 |
| TP-03.01 | Regression 覆盖 provider protocol 和现有 API 行为。 |
| TP-03.02 | AGENTS/路线图/任务文档口径一致。 |
| TP-04.01 | 本地门禁通过。 |
| TP-04.02 | 任务树 closeout 通过。 |

# Anti-Goals
- 不得修改八字、紫微、黄历、梅花算法结论。
- 不得虚构证据
- 不得越权补全未确认信息
