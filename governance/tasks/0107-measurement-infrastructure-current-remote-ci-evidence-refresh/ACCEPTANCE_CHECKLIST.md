# Acceptance Checklist

# Global Standards
- [ ] 只使用当前 `main` HEAD。
- [ ] 不把 workflow 配置存在当作 run 通过。
- [ ] 不把 older SHA run 当作 current HEAD evidence。
- [ ] 不推送 GHCR image，不声明 digest/attestation。
- [ ] 远端 run 未完成或失败时如实报告。

# Task Package Checklists
## TP-01.01
- [ ] Current HEAD and workflows inspected.
- [ ] Verify: `git status --short --branch && git rev-parse HEAD && sed -n '1,80p' .github/workflows/acceptance.yml && sed -n '1,120p' .github/workflows/container.yml`
- [ ] Gate: worktree clean before dispatch.

## TP-01.02
- [ ] Existing remote run absence recorded before dispatch.
- [ ] Verify: `gh run list --commit HEAD --limit 20 --json databaseId,headSha,status,conclusion,workflowName,url,createdAt,event`
- [ ] Gate: empty list is missing evidence, not pass.

## TP-02.01
- [ ] Acceptance workflow dispatched after task package push.
- [ ] Verify: `gh workflow run acceptance.yml --ref main -f reason=current-remote-ci-evidence-0107`
- [ ] Gate: command exits 0 and later run appears for current headSha.

## TP-02.02
- [ ] Container workflow dispatched after task package push with `push_image=false`.
- [ ] Verify: `gh workflow run container.yml --ref main -f push_image=false`
- [ ] Gate: command exits 0 and no GHCR push is requested.

## TP-03.01
- [ ] Poll loop reaches terminal state or records timeout.
- [ ] Verify: `gh run list --commit HEAD --limit 20 --json databaseId,headSha,status,conclusion,workflowName,url,createdAt,event`
- [ ] Gate: missing/queued/in_progress cannot pass.

## TP-03.02
- [ ] Run SHA/conclusion verified.
- [ ] Verify: `gh run view <run-id> --json headSha,status,conclusion,url,workflowName,event`
- [ ] Gate: `headSha` equals `git rev-parse HEAD`; `status=completed`; `conclusion=success`.

## TP-04.01
- [ ] Task docs validator and placeholder scan pass.
- [ ] Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0107-measurement-infrastructure-current-remote-ci-evidence-refresh --phase decompose`
- [ ] Gate: no placeholders remain.

## TP-04.02
- [ ] Task package committed/pushed before dispatch.
- [ ] Verify: `git status --short --branch && git log -1 --oneline`
- [ ] Gate: no post-evidence commit is made.
