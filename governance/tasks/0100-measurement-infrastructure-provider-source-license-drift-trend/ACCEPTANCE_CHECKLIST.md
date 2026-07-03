# Acceptance Checklist

# Global Standards
- [x] Scope is provider/source/license trend gate only.
- [x] Existing provider drift scanner is reused.
- [x] External live and legal review are explicitly out of scope.
- [x] Baseline stores metadata and fingerprints only.
- [x] Focused tests pass.
- [x] quick local-ci passes.
- [x] Task closeout updated.

# Task Package Checklists
## TP-01 SPEC
Verify: existing scanner and roadmap inspected.
Gate: do not duplicate provider runtime.

- [x] TP-01.01 读取 provider drift scanner、contract、provider schema、local-ci 和路线图。
- [x] TP-01.02 定义 trend gate 与 baseline 边界。

## TP-01.01 读取 provider drift scanner、contract、provider schema、local-ci 和路线图
Verify: source files and docs inspected.
Gate: existing scanner remains source of lower-level truth.

- [x] `scripts/provider-drift-scanner.py` read.
- [x] `contracts/fate/capabilities/provider-drift-contract.json` read.
- [x] `scripts/local-ci.sh` provider section read.

## TP-01.02 定义 trend gate 与 baseline 边界
Verify: PLAN/CONTEXT record target boundary.
Gate: external provider live and legal review are out of scope.

- [x] Tracked baseline selected.
- [x] Fingerprint comparison selected.
- [x] External live overclaim rejected.

## TP-02 BUILD
Verify: new contract/baseline/script/wiring exist.
Gate: baseline and report JSON parse and initial gate passes.

- [x] TP-02.01 新增 provider drift baseline 与 trend contract。
- [x] TP-02.02 新增 provider drift trend gate script。
- [x] TP-02.03 接入 local-ci、AGENTS、provider schema、docs。

## TP-02.01 新增 provider drift baseline 与 trend contract
Verify: JSON files parse.
Gate: baseline contains provider/source/license/vendor fingerprints.

- [x] `provider-drift-baseline.json` added.
- [x] `provider-drift-trend-contract.json` added.

## TP-02.02 新增 provider drift trend gate script
Verify: gate command runs.
Gate: current baseline produces `status=passed` and `findingCount=0`.

- [x] `provider-drift-trend-gate.py` added.
- [x] `provider-drift-trend-gate.sh` added.

## TP-02.03 接入 local-ci、AGENTS、provider schema、docs
Verify: wiring assertions in regression test.
Gate: quick CI invokes trend gate after scanner.

- [x] `scripts/local-ci.sh` updated.
- [x] `contracts/fate/capabilities/AGENTS.md` updated.
- [x] `scripts/AGENTS.md` updated.
- [x] `tests/AGENTS.md` updated.
- [x] operations docs and roadmap updated.

## TP-03 TEST
Verify: focused tests and lint/format pass.
Gate: negative cases fail as intended.

- [x] TP-03.01 增加 trend gate positive/negative tests。
- [x] TP-03.02 运行 focused tests、ruff、format、task validator。

## TP-03.01 增加 trend gate positive/negative tests
Verify: test file exists and covers positive/negative cases.
Gate: missing provider/license/vendor/scanner failures are asserted.

- [x] Positive test added.
- [x] Missing provider negative test added.
- [x] License regression negative test added.
- [x] Vendor hash drift negative test added.
- [x] Failed scanner report negative test added.

## TP-03.02 运行 focused tests、ruff、format、task validator
Verify: command outputs recorded in STATUS.
Gate: all validations pass before closeout.

- [x] Provider drift trend gate smoke executed after latest formatting.
- [x] Focused pytest executed after latest formatting.
- [x] Ruff check and format check executed.
- [x] Task docs validator executed.

## TP-04 SHIP
Verify: task docs closeout and git delivery evidence.
Gate: remote CI not overclaimed if current commit run is not observed.

- [x] TP-04.01 回填 closeout 状态。
- [x] TP-04.02 提交并推送。

## TP-04.01 回填 closeout 状态
Verify: README/STATUS/ACCEPTANCE/TODO/checklist updated.
Gate: no placeholders and closeout validator passes.

- [x] Task docs updated to Done.
- [x] Closeout validation executed.

## TP-04.02 提交并推送
Verify: git status clean and origin/main aligned.
Gate: only 0100 scoped files are staged.

- [x] Commit created.
- [x] Push completed.
