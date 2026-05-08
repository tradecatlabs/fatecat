# Task Status
- Overall Status: `Done`

# Next Executable Leaves
- 当前无待执行叶子；30 个叶子任务均已完成并进入 closeout。

# Task Package Status Table
| Node ID | Parent | Depth | Depends On | Ready | Status | Recent Evidence | Blocker | Unblock Needed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | - | No | Done | 本地 acceptance 通过：88 passed；ruff、format、mypy、API/Bot dry-run、导出包 smoke/hygiene 通过。 |  |  |
| TP-01.01 | TP-01 | 2 | - | No | Done | 本地 acceptance 通过：88 passed；ruff、format、mypy、API/Bot dry-run、导出包 smoke/hygiene 通过。 |  |  |
| TP-01.02 | TP-01 | 2 | - | No | Done | 本地 acceptance 通过：88 passed；ruff、format、mypy、API/Bot dry-run、导出包 smoke/hygiene 通过。 |  |  |
| TP-01.03 | TP-01 | 2 | TP-01.01, TP-01.02 | No | Done | 本地 acceptance 通过：88 passed；ruff、format、mypy、API/Bot dry-run、导出包 smoke/hygiene 通过。 |  |  |
| TP-02 | ROOT | 1 | TP-01.01, TP-01.02, TP-01.03 | No | Done | 本地 acceptance 通过：88 passed；ruff、format、mypy、API/Bot dry-run、导出包 smoke/hygiene 通过。 |  |  |
| TP-02.01 | TP-02 | 2 | TP-01.01, TP-01.02, TP-01.03 | No | Done | 本地 acceptance 通过：88 passed；ruff、format、mypy、API/Bot dry-run、导出包 smoke/hygiene 通过。 |  |  |
| TP-02.02 | TP-02 | 2 | TP-01.01, TP-01.02, TP-01.03 | No | Done | 本地 acceptance 通过：88 passed；ruff、format、mypy、API/Bot dry-run、导出包 smoke/hygiene 通过。 |  |  |
| TP-02.03 | TP-02 | 2 | TP-01.01, TP-01.02, TP-01.03 | No | Done | 本地 acceptance 通过：88 passed；ruff、format、mypy、API/Bot dry-run、导出包 smoke/hygiene 通过。 |  |  |
| TP-02.04 | TP-02 | 2 | TP-01.01, TP-01.02, TP-01.03 | No | Done | 本地 acceptance 通过：88 passed；ruff、format、mypy、API/Bot dry-run、导出包 smoke/hygiene 通过。 |  |  |
| TP-02.05 | TP-02 | 2 | TP-01.01, TP-01.02, TP-01.03 | No | Done | 本地 acceptance 通过：88 passed；ruff、format、mypy、API/Bot dry-run、导出包 smoke/hygiene 通过。 |  |  |
| TP-03 | ROOT | 1 | TP-02.01, TP-02.02, TP-02.03, TP-02.04, TP-02.05 | No | Done | 本地 acceptance 通过：88 passed；ruff、format、mypy、API/Bot dry-run、导出包 smoke/hygiene 通过。 |  |  |
| TP-03.01 | TP-03 | 2 | TP-02.01, TP-02.02, TP-02.03, TP-02.04, TP-02.05 | No | Done | 本地 acceptance 通过：88 passed；ruff、format、mypy、API/Bot dry-run、导出包 smoke/hygiene 通过。 |  |  |
| TP-03.02 | TP-03 | 2 | TP-02.01, TP-02.02, TP-02.03, TP-02.04, TP-02.05 | No | Done | 本地 acceptance 通过：88 passed；ruff、format、mypy、API/Bot dry-run、导出包 smoke/hygiene 通过。 |  |  |
| TP-03.03 | TP-03 | 2 | TP-02.01, TP-02.02, TP-02.03, TP-02.04, TP-02.05 | No | Done | 本地 acceptance 通过：88 passed；ruff、format、mypy、API/Bot dry-run、导出包 smoke/hygiene 通过。 |  |  |
| TP-03.04 | TP-03 | 2 | TP-02.01, TP-02.02, TP-02.03, TP-02.04, TP-02.05 | No | Done | 本地 acceptance 通过：88 passed；ruff、format、mypy、API/Bot dry-run、导出包 smoke/hygiene 通过。 |  |  |
| TP-03.05 | TP-03 | 2 | TP-02.01, TP-02.02, TP-02.03, TP-02.04, TP-02.05 | No | Done | 本地 acceptance 通过：88 passed；ruff、format、mypy、API/Bot dry-run、导出包 smoke/hygiene 通过。 |  |  |
| TP-04 | ROOT | 1 | TP-01.01, TP-01.02, TP-01.03 | No | Done | 本地 acceptance 通过：88 passed；ruff、format、mypy、API/Bot dry-run、导出包 smoke/hygiene 通过。 |  |  |
| TP-04.01 | TP-04 | 2 | TP-01.01, TP-01.02, TP-01.03 | No | Done | 本地 acceptance 通过：88 passed；ruff、format、mypy、API/Bot dry-run、导出包 smoke/hygiene 通过。 |  |  |
| TP-04.02 | TP-04 | 2 | TP-01.01, TP-01.02, TP-01.03, TP-04.01 | No | Done | 本地 acceptance 通过：88 passed；ruff、format、mypy、API/Bot dry-run、导出包 smoke/hygiene 通过。 |  |  |
| TP-04.03 | TP-04 | 2 | TP-01.01, TP-01.02, TP-01.03, TP-04.01 | No | Done | 本地 acceptance 通过：88 passed；ruff、format、mypy、API/Bot dry-run、导出包 smoke/hygiene 通过。 |  |  |
| TP-04.04 | TP-04 | 2 | TP-01.01, TP-01.02, TP-01.03, TP-04.01 | No | Done | 本地 acceptance 通过：88 passed；ruff、format、mypy、API/Bot dry-run、导出包 smoke/hygiene 通过。 |  |  |
| TP-04.05 | TP-04 | 2 | TP-01.01, TP-01.02, TP-01.03, TP-04.02, TP-04.03, TP-04.04 | No | Done | 本地 acceptance 通过：88 passed；ruff、format、mypy、API/Bot dry-run、导出包 smoke/hygiene 通过。 |  |  |
| TP-05 | ROOT | 1 | TP-04.01, TP-04.02, TP-04.03, TP-04.04, TP-04.05 | No | Done | 本地 acceptance 通过：88 passed；ruff、format、mypy、API/Bot dry-run、导出包 smoke/hygiene 通过。 |  |  |
| TP-05.01 | TP-05 | 2 | TP-04.01, TP-04.02, TP-04.03, TP-04.04, TP-04.05 | No | Done | 本地 acceptance 通过：88 passed；ruff、format、mypy、API/Bot dry-run、导出包 smoke/hygiene 通过。 |  |  |
| TP-05.02 | TP-05 | 2 | TP-04.01, TP-04.02, TP-04.03, TP-04.04, TP-04.05 | No | Done | 本地 acceptance 通过：88 passed；ruff、format、mypy、API/Bot dry-run、导出包 smoke/hygiene 通过。 |  |  |
| TP-05.03 | TP-05 | 2 | TP-04.01, TP-04.02, TP-04.03, TP-04.04, TP-04.05 | No | Done | 本地 acceptance 通过：88 passed；ruff、format、mypy、API/Bot dry-run、导出包 smoke/hygiene 通过。 |  |  |
| TP-05.04 | TP-05 | 2 | TP-04.01, TP-04.02, TP-04.03, TP-04.04, TP-04.05, TP-05.01, TP-05.02, TP-05.03 | No | Done | 本地 acceptance 通过：88 passed；ruff、format、mypy、API/Bot dry-run、导出包 smoke/hygiene 通过。 |  |  |
| TP-06 | ROOT | 1 | TP-03.01, TP-03.02, TP-03.03, TP-03.04, TP-03.05, TP-05.01, TP-05.02, TP-05.03, TP-05.04 | No | Done | 本地 acceptance 通过：88 passed；ruff、format、mypy、API/Bot dry-run、导出包 smoke/hygiene 通过。 |  |  |
| TP-06.01 | TP-06 | 2 | TP-03.01, TP-03.02, TP-03.03, TP-03.04, TP-03.05, TP-05.01, TP-05.02, TP-05.03, TP-05.04 | No | Done | 本地 acceptance 通过：88 passed；ruff、format、mypy、API/Bot dry-run、导出包 smoke/hygiene 通过。 |  |  |
| TP-06.02 | TP-06 | 2 | TP-03.01, TP-03.02, TP-03.03, TP-03.04, TP-03.05, TP-05.01, TP-05.02, TP-05.03, TP-05.04, TP-06.01 | No | Done | 本地 acceptance 通过：88 passed；ruff、format、mypy、API/Bot dry-run、导出包 smoke/hygiene 通过。 |  |  |
| TP-06.03 | TP-06 | 2 | TP-03.01, TP-03.02, TP-03.03, TP-03.04, TP-03.05, TP-05.01, TP-05.02, TP-05.03, TP-05.04, TP-06.01 | No | Done | 本地 acceptance 通过：88 passed；ruff、format、mypy、API/Bot dry-run、导出包 smoke/hygiene 通过。 |  |  |
| TP-06.04 | TP-06 | 2 | TP-03.01, TP-03.02, TP-03.03, TP-03.04, TP-03.05, TP-05.01, TP-05.02, TP-05.03, TP-05.04, TP-06.01 | No | Done | 本地 acceptance 通过：88 passed；ruff、format、mypy、API/Bot dry-run、导出包 smoke/hygiene 通过。 |  |  |
| TP-07 | ROOT | 1 | TP-06.01, TP-06.02, TP-06.03, TP-06.04 | No | Done | 本地 acceptance 通过：88 passed；ruff、format、mypy、API/Bot dry-run、导出包 smoke/hygiene 通过。 |  |  |
| TP-07.01 | TP-07 | 2 | TP-06.01, TP-06.02, TP-06.03, TP-06.04 | No | Done | 本地 acceptance 通过：88 passed；ruff、format、mypy、API/Bot dry-run、导出包 smoke/hygiene 通过。 |  |  |
| TP-07.02 | TP-07 | 2 | TP-06.01, TP-06.02, TP-06.03, TP-06.04 | No | Done | 本地 acceptance 通过：88 passed；ruff、format、mypy、API/Bot dry-run、导出包 smoke/hygiene 通过。 |  |  |
| TP-07.03 | TP-07 | 2 | TP-06.01, TP-06.02, TP-06.03, TP-06.04, TP-07.01, TP-07.02 | No | Done | 本地 acceptance 通过：88 passed；ruff、format、mypy、API/Bot dry-run、导出包 smoke/hygiene 通过。 |  |  |
| TP-07.04 | TP-07 | 2 | TP-06.01, TP-06.02, TP-06.03, TP-06.04, TP-07.03 | No | Done | 本地 acceptance 通过：88 passed；ruff、format、mypy、API/Bot dry-run、导出包 smoke/hygiene 通过。 |  |  |

# Blockers
- 当前无任务树落盘阻塞项。
