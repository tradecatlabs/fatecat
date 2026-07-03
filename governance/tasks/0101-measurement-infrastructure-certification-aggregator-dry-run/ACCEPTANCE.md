# Task-Level Acceptance
- certification aggregator 能读取 local-ci output dir 并输出机器可读 summary。
- 缺少 required evidence 时输出 `failed`，不得默默跳过。
- 外部 live、release 或 audit 未闭合时输出 `blocked` 或 `pending`，且 `canClaim100Percent=false`。
- 只有所有分域 `passed` 时，`--require-certified` 才返回 0 并允许 `canClaim100Percent=true`。
- 输出不得包含真实 token、secret、DSN、私钥、报告正文、出生地区或命理报告章节。

# Validation Plan
| Scope | Command | Expected |
| --- | --- | --- |
| Aggregator smoke | `bash scripts/measurement-infrastructure-certification.sh --evidence-dir /tmp/fatecat-local-ci-0100-final --output-json /tmp/fatecat-certification-0101-rerun.json` | 当前 dry-run evidence 输出 `blocked`，不声明 100%。 |
| Focused tests | `.venv/bin/python -m pytest -q tests/regression/test_measurement_infrastructure_certification.py tests/regression/test_current_audit_bundle.py tests/regression/test_current_release_proof.py` | Regression passed。 |
| Lint/format | `.venv/bin/ruff check scripts/measurement-infrastructure-certification.py tests/regression/test_measurement_infrastructure_certification.py && .venv/bin/ruff format --check scripts/measurement-infrastructure-certification.py tests/regression/test_measurement_infrastructure_certification.py` | Ruff passed。 |
| Quick CI | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0101-final` | 本地 quick CI passed，并生成 certification artifact。 |
| Secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0101-final.json` | findingCount=0。 |
| Task docs | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0101-measurement-infrastructure-certification-aggregator-dry-run --phase closeout` | ok=true。 |

# Review Gate
- 检查 `DOMAIN_SPECS` 是否覆盖 contract required evidence。
- 检查 blocked/pending/failed 优先级：missing > failed > blocked > pending > passed。
- 检查 forbidden fragments 防护和 secret scan。
- 检查 local-ci summary artifact 是否包含 certification output 和关键 upstream evidence 路径。

# Runtime Verification Gate
- 本任务本地验证必须至少覆盖合成 full pass、blocked dry-run、missing evidence fail 和 `--require-certified` reject。
- 真实外部 live 不在本任务执行；所有真实生产系统均为外部连通验证待执行。

# Ship Readiness
- [x] closeout validator passed。
- [x] quick local-ci passed。
- [x] secret scan passed。
- [x] commit pushed to `origin/main`。
- [x] 远端 CI 对当前 commit 的状态如实记录；未观察到则不得写通过。

# Task Package Acceptance
## TP-01 certification 需求和契约边界
Acceptance: 100% certification 的语义被限定为证据聚合，不替代外部 live 或第三方审计。

### TP-01.01 盘点 local-ci 现有 gate evidence 与不可声明边界
Verify: `rg -n "current audit bundle|live release gate|provider drift trend" scripts/local-ci.sh`

Gate: release、audit、provider、security、runtime、developer、SRE 和 core quality 的 evidence 来源明确；non-claims 已写入 contract。

### TP-01.02 定义 certification contract、必备证据和分域状态
Verify: `cat contracts/fate/audit/measurement-infrastructure-certification.json`

Gate: contract 包含 required evidence files、required output fields、allowed statuses、forbidden fragments、privacy boundary 和 release boundary。

## TP-02 certification aggregator 实现与接线
Acceptance: 聚合器以只读方式消费 local-ci evidence，输出可复核 JSON。

### TP-02.01 实现 CLI/wrapper、分域聚合、blocked/pending/failed 语义
Verify: `bash scripts/measurement-infrastructure-certification.sh --evidence-dir /tmp/fatecat-local-ci-0100-final --output-json /tmp/fatecat-certification-0101.json`

Gate: 当前 dry-run 输出 `blocked`，`canClaim100Percent=false`，缺 evidence 输出 `failed`。

### TP-02.02 接入 local-ci summary、AGENTS、API 文档和 roadmap
Verify: `rg -n "measurement-infrastructure-certification|certification aggregator" scripts/local-ci.sh scripts/AGENTS.md contracts/fate/audit/AGENTS.md tests/AGENTS.md`

Gate: `scripts/local-ci.sh` 会生成 `measurement-infrastructure-certification.json`，summary artifacts 可追踪。

## TP-03 验证与审查
Acceptance: 本地可执行验证覆盖主要状态转换和集成路径。

### TP-03.01 增加 regression tests
Verify: `.venv/bin/python -m pytest -q tests/regression/test_measurement_infrastructure_certification.py`

Gate: blocked、missing、require-certified、synthetic passed 均有覆盖。

### TP-03.02 执行 gate smoke、focused tests、ruff、quick local-ci 和 secret scan
Verify: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0101-final`

Gate: quick local-ci、secret scan、ruff 和 focused pytest 通过。

## TP-04 closeout 与版本控制
Acceptance: 文档、任务索引、版本控制和远端状态一致。

### TP-04.01 同步任务文档、INDEX 和验收清单
Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0101-measurement-infrastructure-certification-aggregator-dry-run --phase closeout`

Gate: closeout validator passed。

### TP-04.02 提交、推送并记录远端状态
Verify: `git status --short --branch && git ls-remote origin refs/heads/main`

Gate: 本地 HEAD 与 origin/main 匹配，或如实说明远端 CI 未覆盖当前 commit。

# Anti-Goals
- 不得只修改 `governance/tasks/` 而不落地 code gate。
- 不得虚构证据
- 不得越权补全未确认信息
- 不得把 blocked/pending 外部连通状态改写成 passed。
