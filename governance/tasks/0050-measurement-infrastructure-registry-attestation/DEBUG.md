# Debug Evidence

## 2026-07-02 Remote Container Workflow Failure

- Run: `https://github.com/tradecatlabs/fatecat/actions/runs/28579776942`
- Commit: `b23eca1f8b3cfe8df9bd6931b5a13abf4b1d17c3`
- Failed step: `Push main image`
- Observed evidence: image push succeeded and logged `digest: sha256:d6108a5d69e90279ed0c59ca0632aee865316ef976f18751da9d8a30b168507a`, then failed at `docker buildx imagetools inspect --format '{{.Digest}}'`.
- Root cause: `docker buildx imagetools inspect` template object exposes the digest under `Manifest.digest`, not a top-level `Digest` field on the runner.
- Fix: parse `--format '{{json .Manifest}}'` with Python and read `["digest"]`.
- Regression guard: `tests/regression/test_container_workflow_attestation.py` asserts the workflow uses `{{json .Manifest}}` and parses `json.load(sys.stdin)["digest"]`.
