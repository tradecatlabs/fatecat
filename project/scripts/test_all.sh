#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY_BIN="$ROOT/.venv/bin/python"

if [[ ! -x "$PY_BIN" ]]; then
    echo "缺少虚拟环境 Python: $PY_BIN" >&2
    echo "请先在 skill 根目录执行 bash scripts/bootstrap.sh --with-dev" >&2
    exit 1
fi

echo "Running FateCat project tests..."
cd "$ROOT"
"$PY_BIN" -m pytest -q tests modules/telegram/tests

echo "All tests passed!"
