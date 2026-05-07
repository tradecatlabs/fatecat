# Task Status
- Overall Status: `Done`
- Completed At: `2026-05-07`
- Current Branch: `main`

# Next Executable Leaves
- 无；全部叶子任务已完成。

# Task Package Status Table
| Node ID | Parent | Depth | Depends On | Ready | Status | Recent Evidence | Blocker | Unblock Needed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | - | No | Done | test_solar_terms_golden.py；acceptance 通过 |  |  |
| TP-01.01 | TP-01 | 2 | - | No | Done | solar_terms README/source_manifest；raw 未进导出包 |  |  |
| TP-01.02 | TP-01 | 2 | TP-01.01 | No | Done | golden/solar_terms_1900_2030.json；fixture schema 测试 |  |  |
| TP-01.03 | TP-01 | 2 | TP-01.02 | No | Done | 月令/立春边界测试通过 |  |  |
| TP-01.04 | TP-01 | 2 | TP-01.02 | No | Done | yun.getStartSolar 起运样本测试通过 |  |  |
| TP-02 | ROOT | 1 | - | No | Done | test_branding_support.py 结构快照 |  |  |
| TP-02.01 | TP-02 | 2 | - | No | Done | report_generator/main/web_ui 调用链审计并记录 |  |  |
| TP-02.02 | TP-02 | 2 | TP-02.01 | No | Done | 默认块不含紫微/黄历/建除/六爻 |  |  |
| TP-02.03 | TP-02 | 2 | TP-02.02 | No | Done | Markdown heading contract 测试通过 |  |  |
| TP-03 | ROOT | 1 | TP-02 | No | Done | analysisEvidence 已进入 JSON/profile |  |  |
| TP-03.01 | TP-03 | 2 | - | No | Done | evidence_schema.json + policy tests |  |  |
| TP-03.02 | TP-03 | 2 | TP-03.01 | No | Done | BaziCalculator._calc_analysis_evidence |  |  |
| TP-03.03 | TP-03 | 2 | TP-03.02 | No | Done | Markdown 不渲染 analysisEvidence，JSON 可用 |  |  |
| TP-04 | ROOT | 1 | TP-02 | No | Done | weight_policy.json |  |  |
| TP-04.01 | TP-04 | 2 | - | No | Done | prediction_systems.py + 功能状态文档 |  |  |
| TP-04.02 | TP-04 | 2 | TP-04.01 | No | Done | test_fate_policy_assets.py |  |  |
| TP-05 | ROOT | 1 | TP-02 | No | Done | 隐私与输入测试通过 |  |  |
| TP-05.01 | TP-05 | 2 | - | No | Done | Web/API 缺字段测试既有覆盖 |  |  |
| TP-05.02 | TP-05 | 2 | - | No | Done | check-privacy-fixtures.sh 通过 |  |  |
| TP-06 | ROOT | 1 | TP-02, TP-05 | No | Done | Web/API 共用 generate_full_report |  |  |
| TP-06.01 | TP-06 | 2 | - | No | Done | main.py/web_ui.py 均调用 report_generator |  |  |
| TP-06.02 | TP-06 | 2 | TP-06.01 | No | Done | Web Markdown 复制结构测试通过 |  |  |
| TP-07 | ROOT | 1 | TP-03 | No | Done | classics_rule_index.json |  |  |
| TP-07.01 | TP-07 | 2 | - | No | Done | classics README/source_manifest 边界文档 |  |  |
| TP-07.02 | TP-07 | 2 | TP-07.01 | No | Done | 规则索引种子 JSON |  |  |
| TP-07.03 | TP-07 | 2 | TP-07.02 | No | Done | evidence ruleIds 接入 |  |  |
| TP-08 | ROOT | 1 | TP-01, TP-02, TP-05, TP-06 | No | Done | pytest/acceptance 门禁通过 |  |  |
| TP-08.01 | TP-08 | 2 | - | No | Done | 全量 pytest 59 passed |  |  |
| TP-08.02 | TP-08 | 2 | TP-08.01 | No | Done | acceptance.sh --with-dev 通过 |  |  |
| TP-09 | ROOT | 1 | TP-02, TP-04 | No | Done | README/SKILL/playbook/docs 同步 |  |  |
| TP-09.01 | TP-09 | 2 | - | No | Done | 生产边界文档更新 |  |  |
| TP-09.02 | TP-09 | 2 | TP-09.01 | No | Done | AGENTS/README/docs map 更新 |  |  |
| TP-10 | ROOT | 1 | TP-03, TP-04, TP-07, TP-08, TP-09 | No | Done | 交付证据与 closeout 完成 |  |  |
| TP-10.01 | TP-10 | 2 | - | No | Done | GIT_DELIVERY_EVIDENCE.json |  |  |
| TP-10.02 | TP-10 | 2 | TP-10.01 | No | Done | TODO/STATUS/CLOSEOUT 已回填 |  |  |

# Blockers
- 无阻塞项。

# Verification Evidence
| 验证项 | 命令 | 结果 |
| --- | --- | --- |
| 任务树结构校验 | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_tasks_tree.py --tasks-dir scripts/project/assets/tasks --phase auto` | 通过 |
| Targeted pytest | `cd scripts/project && .venv/bin/python -m pytest -q tests/test_fate_policy_assets.py tests/test_solar_terms_golden.py` | 10 passed |
| Full pytest | `cd scripts/project && .venv/bin/python -m pytest -q tests modules/telegram/tests` | 59 passed |
| Ruff check | `cd scripts/project && RUFF_CACHE_DIR=/tmp/fatecat-ruff-cache .venv/bin/python -m ruff check .` | 通过 |
| Ruff format | `cd scripts/project && RUFF_CACHE_DIR=/tmp/fatecat-ruff-cache .venv/bin/python -m ruff format --check .` | 91 files already formatted |
| MyPy | `cd scripts/project && .venv/bin/python -m mypy -p fate_core` | Success |
| Source hygiene | `bash scripts/check-source-hygiene.sh` | 通过 |
| Privacy fixtures | `bash scripts/check-privacy-fixtures.sh` | 通过 |
| Acceptance | `bash scripts/acceptance.sh --with-dev` | 通过；输出目录 /tmp/fatecat-acceptance |
| Git delivery evidence | `python3 /home/lenovo/.codex/skills/auto-github/scripts/capture_delivery_evidence.py --out /tmp/fatecat-git-delivery-evidence.json` | 本地可再生成；入库文件仅保留证据生成说明，避免实时工作树快照 self-blocking |

# Residual External Unknowns
- 真实生产 API 域名、CORS allowlist、API token：外部连通验证待执行。
- 真实 Telegram Bot token 与 Bot API live smoke：外部连通验证待执行。
- GitHub Actions 需要 push 后以远端最新 run 为准；本地 acceptance 已通过。

# Notes
- `assets/data/calendar/solar_terms/golden/solar_terms_1900_2030.json` 是测试 fixture，不替换生产 `lunar-python`。
- raw 交节表与 `lunar-python` 在部分历史区间存在约 1 小时时区/DST 口径差异，fixture 已通过 `toleranceSeconds=3660` 显式记录。
- raw 表不进入 Git 与导出包；重新生成 golden 需要按 `source_manifest.tsv` 取得同哈希本地 raw 文件。
