# Acceptance Checklist

- [x] `bash scripts/retention-cleanup-smoke.sh --output-json /tmp/fatecat-retention-cleanup-smoke-0091.json --pretty`
- [x] `python3 -m pytest -q tests/regression/test_retention_cleanup.py`
- [x] `python3 -m pytest -q tests/regression/test_production_security_gate.py`
- [x] `python3 -m ruff check domains/experience-delivery/services/fatecat-delivery/src/retention_cleanup.py scripts/retention-cleanup.py scripts/retention-cleanup-smoke.py tests/regression/test_retention_cleanup.py scripts/production-security-gate.py tests/regression/test_production_security_gate.py`
- [x] `python3 -m ruff format --check domains/experience-delivery/services/fatecat-delivery/src/retention_cleanup.py scripts/retention-cleanup.py scripts/retention-cleanup-smoke.py tests/regression/test_retention_cleanup.py scripts/production-security-gate.py tests/regression/test_production_security_gate.py`
- [x] `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0091.json`
- [x] `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0091-pass`
- [ ] commit pushed
- [ ] remote acceptance/container CI checked

## External Pending

- [ ] Production scheduler / cron / worker retention cleanup live evidence.
- [ ] Postgres production cleanup live evidence.
- [ ] External SIEM / WORM retention proof.
- [ ] Real production deletion audit proof refs.
