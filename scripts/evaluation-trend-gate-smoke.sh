#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

runtime_root="$(resolve_runtime_root)"
output_dir="${runtime_root}/infra/runtime/local-state/exports/evaluations/trend-gate-smoke"

usage() {
  cat <<'EOF'
用法:
  bash scripts/evaluation-trend-gate-smoke.sh [--output-dir <dir>]

说明:
  生成两条脱敏 EvaluationRun summary history fixture，验证 trend gate renderer 和
  policy，不执行重型评测，不访问公网。
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --output-dir)
      [[ $# -ge 2 ]] || usage_error "--output-dir 缺少参数"
      output_dir="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      usage_error "未知参数: $1"
      ;;
  esac
done

history_dir="${output_dir}/history"
summary_one="${history_dir}/20260703T000000Z-passed.json"
summary_two="${history_dir}/20260703T010000Z-passed.json"
trend_json="${output_dir}/trend-gate.json"
mkdir -p "${history_dir}"

cat > "${summary_one}" <<'JSON'
{
  "schemaVersion": 1,
  "generatedAt": "2026-07-03T00:00:00Z",
  "registry": "contracts/fate/evaluations/registry.json",
  "gitCommit": "synthetic-baseline",
  "selection": {"runIds": [], "allLocal": false, "allLocalRequired": true, "allowReferenceRepo": false},
  "dryRun": false,
  "summary": {"total": 1, "passed": 1, "failed": 0, "skipped": 0, "planned": 0, "status": "passed"},
  "runs": [
    {
      "runId": "run.solar_terms_golden",
      "name": "synthetic",
      "runType": "golden_regression",
      "gateType": "required",
      "releaseRequired": true,
      "localAvailability": "tracked_in_repo",
      "datasetIds": ["dataset.solar_terms_1900_2030"],
      "status": "passed",
      "commands": [{"command": ".venv/bin/python -m pytest -q tests/regression/test_solar_terms_golden.py", "exitCode": 0, "durationMs": 1, "stdoutTail": "", "stderrTail": ""}]
    }
  ]
}
JSON

cat > "${summary_two}" <<'JSON'
{
  "schemaVersion": 1,
  "generatedAt": "2026-07-03T01:00:00Z",
  "registry": "contracts/fate/evaluations/registry.json",
  "gitCommit": "synthetic-current",
  "selection": {"runIds": [], "allLocal": false, "allLocalRequired": true, "allowReferenceRepo": false},
  "dryRun": false,
  "summary": {"total": 1, "passed": 1, "failed": 0, "skipped": 0, "planned": 0, "status": "passed"},
  "runs": [
    {
      "runId": "run.solar_terms_golden",
      "name": "synthetic",
      "runType": "golden_regression",
      "gateType": "required",
      "releaseRequired": true,
      "localAvailability": "tracked_in_repo",
      "datasetIds": ["dataset.solar_terms_1900_2030"],
      "status": "passed",
      "commands": [{"command": ".venv/bin/python -m pytest -q tests/regression/test_solar_terms_golden.py", "exitCode": 0, "durationMs": 1, "stdoutTail": "", "stderrTail": ""}]
    }
  ]
}
JSON
cp "${summary_two}" "${history_dir}/latest.json"

bash "${script_dir}/evaluation-trend-gate.sh" \
  --history-dir "${history_dir}" \
  --output-json "${trend_json}"

python3 - "$trend_json" <<'PY'
import json
import sys
from pathlib import Path

payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
assert payload["status"] == "passed"
assert payload["summaryCount"] >= 2
assert not payload["trendFindings"]
print(json.dumps({"status": "passed", "trendGate": sys.argv[1], "summaryCount": payload["summaryCount"]}, ensure_ascii=False))
PY
