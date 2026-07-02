# Task-Level Acceptance
- `scripts/bazi-ziwei-l4-golden-smoke.sh --profile quick` 可本地执行并输出 JSON summary。
- summary 覆盖八字矩阵、八字规则深度、八字断语、紫微 golden、紫微规则深度和 Markdown profile gate。
- quick summary 明确 `availableCaseCount` 与 `executedCaseCount`，避免把代表样本误写成全量执行。
- smoke 通过 `CapabilityExecutor` 执行 bazi/ziwei，不旁路 provider 协议。
- Markdown gate 通过真实 `/api/v1/report/markdown` TestClient 调用验证。
- quick local-ci 包含 L4 golden smoke 和 pytest。
- docs/AGENTS/roadmap 明确本轮不是全文断语 golden、真实命例大 corpus 或专业能力 100%。

# Validation Plan
| 验证项 | 命令 | 状态 |
| --- | --- | --- |
| L4 golden quick smoke | `bash scripts/bazi-ziwei-l4-golden-smoke.sh --profile quick --output-json /tmp/fatecat-bazi-ziwei-l4.json` | Passed; 65 checks |
| smoke JSON parse | `python3 -m json.tool /tmp/fatecat-bazi-ziwei-l4.json` | Passed |
| focused pytest | `.venv/bin/python -m pytest -q tests/regression/test_bazi_ziwei_l4_golden_smoke.py` | Passed; 2 passed |
| ruff check | `.venv/bin/python -m ruff check scripts/bazi-ziwei-l4-golden-smoke.py tests/regression/test_bazi_ziwei_l4_golden_smoke.py` | Passed |
| ruff format check | `.venv/bin/python -m ruff format --check scripts/bazi-ziwei-l4-golden-smoke.py tests/regression/test_bazi_ziwei_l4_golden_smoke.py` | Passed |
| quick local-ci | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-bazi-ziwei-l4` | Passed; 108 passed |

# Review Gate
- 检查 smoke 是否走 `CapabilityExecutor` 和 Markdown API，而不是直接读 fixture 后自判。
- 检查 quick/full 是否区分代表执行与可用样本总量。
- 检查 artifact 是否只保存摘要，不保存完整报告正文。
- 检查文档是否标注真实命例、全文 diff、生产 live smoke 仍待后续。

# Runtime Verification Gate
- 已通过 quick smoke。
- focused pytest、ruff、format 和 quick local-ci 已通过；task validator、tree validator 待执行。
- 外部连通验证待执行：真实公网 API、真实 token、Bot、webhook、生产 provider 远端依赖。

# Ship Readiness
- 当前本地验证已通过；closeout validator 和 closeout packet 作为最终收口证据。
- 任务完成后可进入 `0035-measurement-infrastructure-data-supply-chain`，继续补 manifest、许可、来源和 corpus 分级。

# Task Package Acceptance
| Package | Acceptance |
| --- | --- |
| TP-02 | smoke script、quick/full profile 与 local-ci hook 落地。 |
| TP-03 | smoke、focused tests、ruff、format、quick CI 通过。 |
| TP-04 | docs/AGENTS/roadmap 同步且 closeout packet 生成。 |

# Anti-Goals
- 不新增真实命例。
- 不做全文断语 golden diff。
- 不宣称八字/紫微专业能力 100%。
- 不做真实公网 live smoke。
- 不新增其他预测体系。
