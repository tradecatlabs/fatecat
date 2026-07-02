# DEBUG - remote CI vendor snapshot drift

## Bug

GitHub Actions `FateCat Acceptance` run `28572173184` failed on commit `149fae97adc53ea3874d56db312cdd218bbbdf28` during `bash scripts/acceptance.sh --with-dev --output /tmp/fatecat-ci-acceptance`.

Failure phase:

```text
[acceptance] vendor health
vendor 快照完整性校验失败:
  - iztro sha256 mismatch
  - mingyu sha256 mismatch
  - taibu sha256 mismatch
  - ZhouYiLab sha256 mismatch
```

## Observations

- Remote run URL: `https://github.com/tradecatlabs/fatecat/actions/runs/28572173184`
- Container workflow for the same commit passed: `https://github.com/tradecatlabs/fatecat/actions/runs/28572173334`
- Local filesystem hashes matched `tools/reference-repos/vendor_sources.json`.
- Git-tracked hashes matched the remote CI actual hashes exactly:
  - `iztro`: `3817f93a677e0c63b353a94fa7275199f21582a36397edc2f90685b58aae9325`
  - `mingyu`: `beb51eec570c20dc60879c24ee4fed0d1a8eaf512d8f3a13394b65ccb0617124`
  - `taibu`: `354273a5c37b3f5a0f1a3db8e126cee4096b80273ed0464ea345600770c727d1`
  - `ZhouYiLab`: `e3a6529cecefa9147f96bb430836a2fb6a7510487a9d75de26395d6f68b67cdf`
- The mismatching local filesystem-only files were ignored by vendor project `.gitignore` rules, such as `iztro-main/lib`.

## Root Cause

`scripts/vendor-health.sh` computed snapshot hashes from the local filesystem. Some reference repositories contain ignored generated files that are present locally but absent from a clean GitHub Actions checkout. The manifest was updated against the local filesystem hash, so clean CI correctly reported a mismatch.

## Fix

- Prefer Git tracked files for snapshot hashing when the vendor path is inside the FateCat Git worktree.
- Fall back to filesystem hashing only for non-Git or unpacked external snapshots.
- Restore the four affected manifest hashes to the clean checkout values.
- Sync `contracts/fate/data-supply-chain/registry.json` because the data supply chain gate also locks the whole `vendor_sources.json` file hash.

## Regression Commands

```bash
bash scripts/clean-runtime.sh
bash scripts/vendor-health.sh
bash scripts/data-supply-chain-gate.sh --output-json /tmp/fatecat-data-supply-chain-gate-0046-fix.json
bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0046-fix
```
