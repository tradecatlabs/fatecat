# Task-Level Acceptance

- `contracts/fate/evaluations/core-quality-corpus.json` 存在，登记 5 个八字/紫微核心语料分片。
- `contracts/fate/evaluations/report-diff-policy.json` 存在，定义 report profile 结构 diff、体系隔离和隐私边界。
- 紫微基础 golden cases 至少 4 个，均为北京/测试样本/匿名 fixture。
- 八字/紫微核心质量语料 gate 可本地执行并输出机器可读 JSON。
- `scripts/local-ci.sh --profile quick` 执行新 gate 并在 summary artifact 记录路径。
- evaluation registry 可发现 `dataset.bazi_ziwei_core_quality_corpus` 和 `run.core_quality_corpus_gate`。
- 回归测试覆盖 gate、registry、runner 和 API 发现层。

# Validation Plan

| Item | Command | Expected |
| --- | --- | --- |
| JSON syntax | `python3 -m json.tool <file>` | 语法通过 |
| Gate | `bash scripts/core-quality-corpus-gate.sh --output-json /tmp/fatecat-core-quality-corpus-gate.json` | status=passed |
| Focused tests | `.venv/bin/python -m pytest -q tests/regression/test_core_quality_corpus_gate.py tests/regression/test_bazi_ziwei_l4_golden_smoke.py tests/regression/test_evaluation_runner.py` | passed |
| API/protocol tests | `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py::test_evaluation_resources_are_discoverable_and_linked tests/regression/test_capability_protocol.py::test_evaluation_registry_resources_are_traceable_and_do_not_pollute_production_inputs` | passed |
| Static checks | `ruff check` / `ruff format --check` / `git diff --check` | passed |
| Local release gate | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0066` | passed |

# Task Package Acceptance

| Node ID | Verify | Gate |
| --- | --- | --- |
| TP-01.01 | `rg` / `sed` / JSON summary | 当前 fixture、registry、local-ci 和 L4 smoke 差距明确 |
| TP-02.01 | JSON syntax + gate | corpus manifest 可机器读取 |
| TP-02.02 | JSON syntax + policy assertions | report diff policy 锁结构和隐私边界 |
| TP-03.01 | L4 golden smoke | 紫微基础样本达到 4 个且均为北京/测试样本 |
| TP-03.02 | gate CLI | `status=passed` 且 `totalCaseCount>=325` |
| TP-03.03 | runner/API tests | required run 可发现，quick CI 生成 artifact |
| TP-04.01 | docs diff + focused tests | AGENTS/README/roadmap 不夸大 |
| TP-04.02 | local-ci + task validators | 本地 gate、quick CI 和任务文档校验通过 |

# Review Gate

- BLOCK if any sample uses real non-Beijing place, real name, secret, token, DSN or production path.
- BLOCK if report policy allows non-bazi systems inside default bazi report.
- BLOCK if production provider reads golden fixture.
- WARN if corpus remains engineering-only and not expert-reviewed; this is expected and documented.

# Runtime Verification Gate

- Gate output must include privacyBoundary and productionBoundary.
- Manifest must remain evaluation-only.
- local-ci quick must include `coreQualityCorpusGate` artifact path.

# Ship Readiness

- Local focused validation: passed.
- quick local-ci: passed.
- Commit/push: handled by Git delivery step after this task closeout.
- Remote CI current commit: handled by Git delivery step after push.

# Anti-Goals

- 不得修改生产算法来迎合 fixture。
- 不得虚构专家验收、外部 benchmark 或 live smoke。
- 不得把新增样本称为真实命例。
