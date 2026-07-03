# Acceptance Checklist

# Global Standards
- [x] 只使用当前 `main` HEAD。
- [x] 不把 workflow 配置存在当作 run 通过。
- [x] 不把 older SHA run 当作 current HEAD evidence。
- [x] 不推送 GHCR image，不声明 digest/attestation。
- [x] 远端 run 未完成或失败时如实报告。

# Task Package Checklists
## TP-01.01
- [x] Current HEAD and workflows inspected.
- [x] Verify: `git status --short --branch && git rev-parse HEAD && sed -n '1,80p' .github/workflows/acceptance.yml && sed -n '1,120p' .github/workflows/container.yml`
- [x] Gate: worktree clean before dispatch.

## TP-01.02
- [x] Existing remote run absence recorded before dispatch.
- [x] Verify: `head_sha="$(git rev-parse HEAD)"; gh run list --commit "$head_sha" --limit 20 --json databaseId,headSha,status,conclusion,workflowName,url,createdAt,event`
- [x] Gate: empty list is missing evidence, not pass.

## TP-02.01
- [x] Acceptance workflow dispatched after task package push.
- [x] Verify: `gh workflow run acceptance.yml --ref main -f reason=current-remote-ci-evidence-0107`
- [x] Gate: command exits 0 and later run appears for current headSha.

## TP-02.02
- [x] Container workflow dispatched after task package push with `push_image=false`.
- [x] Verify: `gh workflow run container.yml --ref main -f push_image=false`
- [x] Gate: command exits 0 and no GHCR push is requested.

## TP-03.01
- [x] Poll loop reaches terminal state or records timeout.
- [x] Verify: `head_sha="$(git rev-parse HEAD)"; gh run list --commit "$head_sha" --limit 20 --json databaseId,headSha,status,conclusion,workflowName,url,createdAt,event`
- [x] Gate: missing/queued/in_progress cannot pass.

## TP-03.02
- [x] Run SHA/conclusion verified.
- [x] Verify: `gh run view <run-id> --json headSha,status,conclusion,url,workflowName,event`
- [x] Gate: `headSha` equals `git rev-parse HEAD`; `status=completed`; `conclusion=success`.

## TP-04.01
- [x] Task docs validator and placeholder scan pass.
- [x] Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0107-measurement-infrastructure-current-remote-ci-evidence-refresh --phase decompose`
- [x] Gate: no placeholders remain.

## TP-04.02
- [x] Task package committed/pushed before dispatch.
- [x] Verify: `git status --short --branch && git log -1 --oneline`
- [x] Gate: no post-evidence commit is made.
