# Acceptance Checklist

# Global Standards

- [x] Scope maps to `MI-100.B.01` and advances the 100% infrastructure task tree.
- [x] New objects have existence justification: they bridge live summary producers to 0123 live proof gate.
- [x] Mature existing scripts are reused; no new external live smoke implementation is invented.
- [x] Privacy boundary excludes URL/token/secret/DSN/webhook secret/report body/user input.
- [x] Targeted tests pass.
- [x] Ruff check and format check pass.
- [x] Secret scan passes.
- [x] Quick local CI passes.
- [ ] Commit/push and remote CI observation complete.

# Task Package Checklists

## TP-01

- [x] Supported categories confirmed.
- [x] Existing live summary producers identified.
- Verify: supported categories match closure gate and category runbooks.
- Gate: no production credential is required for this local slice.

## TP-02

- [x] Contract added.
- [x] Python assembler added.
- [x] Shell wrapper added.
- [x] Pending/live/rejected tests added.
- Verify: contract/script/wrapper files exist and targeted tests cover pending/live/rejected paths.
- Gate: assembler only adapts existing summaries and does not implement new live network calls.

## TP-03

- [x] local-ci generates bundle.
- [x] live proof gate receives bundle.
- [x] AGENTS files updated.
- [x] Bot runbook command corrected.
- Verify: regression tests assert local-ci and AGENTS wiring.
- Gate: local-ci generated bundle is the only new live proof input passed to 0123.

## TP-04

- [x] Targeted pytest initial run passed: 19 passed.
- [x] Ruff check initial run passed.
- [x] Ruff format check passed after formatting.
- [x] Secret scan passed.
- [x] Quick local CI passed.
- Verify: targeted pytest, ruff, secret scan and quick local CI commands complete successfully.
- Gate: generated evidence remains pending without real live summaries and contains no URL/secret output.

## TP-05

- [ ] Git commit created.
- [ ] Push completed.
- [ ] Remote Acceptance observed.
- [ ] Remote Container observed if triggered.
- Verify: git log, git status, gh run view for triggered workflows.
- Gate: current pushed commit has remote CI evidence or failure is fixed before closeout.
