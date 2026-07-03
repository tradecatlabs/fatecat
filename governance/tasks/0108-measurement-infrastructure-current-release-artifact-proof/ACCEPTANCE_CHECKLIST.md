# Acceptance Checklist

# Global Standards
- [x] 只使用 final `main` HEAD。
- [x] 远端 CI 和 release proof 必须绑定 final HEAD。
- [x] Container release 必须显式 `push_image=true`。
- [x] Dry-run rollback 不能写成真实生产回滚。
- [x] 不输出 GitHub token、registry token、secret、DSN、报告正文或生产日志正文。

# Task Package Checklists
## TP-01.01
- [x] Pre-0108 release proof gap recorded.
- [x] Verify: `bash scripts/current-release-proof.sh --output-json /tmp/fatecat-current-release-proof-pre0108.json --acceptance-run-id <0107-acceptance> --container-run-id <0107-container>`
- [x] Gate: missing release artifact/digest/attestation/rollback proves 0108 is needed.

## TP-01.02
- [x] Container workflow release path inspected.
- [x] Verify: `sed -n '1,140p' .github/workflows/container.yml`
- [x] Gate: workflow contains release artifacts upload, GHCR push, actions/attest and attestation verify under `inputs.push_image`.

## TP-02.01
- [x] 0108 task package committed and pushed before dispatch.
- [x] Verify: `git status --short --branch && git log -1 --oneline`
- [x] Gate: no uncommitted files before dispatch.

## TP-02.02
- [x] Final HEAD clean before dispatch.
- [x] Verify: `git rev-parse HEAD`
- [x] Gate: final HEAD is the SHA used in all later run detail checks.

## TP-03.01
- [x] Acceptance dispatched for final HEAD.
- [x] Verify: `gh workflow run acceptance.yml --ref main -f reason=current-release-proof-0108-final`
- [x] Gate: run appears with final `headSha`.

## TP-03.02
- [x] Container release dispatched for final HEAD with `push_image=true`.
- [x] Verify: `gh workflow run container.yml --ref main -f push_image=true`
- [x] Gate: run appears with final `headSha`.

## TP-04.01
- [x] Both workflows reach terminal success.
- [x] Verify: `head_sha="$(git rev-parse HEAD)"; gh run list --commit "$head_sha" --limit 20 --json databaseId,headSha,status,conclusion,workflowName,url,createdAt,event`
- [x] Gate: Acceptance and Container both completed success.

## TP-04.02
- [x] Artifacts/digest/attestation verified.
- [x] Verify: `bash scripts/current-release-proof.sh --require-current-release ...`
- [x] Gate: release artifacts, registry digest and attestation checks pass.

## TP-05.01
- [x] Rollback dry-run evidence generated.
- [x] Verify: `bash scripts/rollback-drill.sh --output-json /tmp/fatecat-rollback-drill-0108.json --release-artifacts-dir <artifacts-dir>`
- [x] Gate: rollback evidence status is passed and `productionRollbackExecuted=false`.

## TP-05.02
- [x] Aggregated current release proof passes.
- [x] Verify: `bash scripts/current-release-proof.sh --require-current-release --rollback-evidence-path /tmp/fatecat-rollback-drill-0108.json --output-json /tmp/fatecat-current-release-proof-0108.json`
- [x] Gate: `proofGate.status=pass`.
