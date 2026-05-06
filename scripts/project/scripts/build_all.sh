#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FATE_BIN="$ROOT/.venv/bin/fatecat"

echo "Building FateCat project entrypoint..."

if [[ ! -x "$FATE_BIN" ]]; then
    echo "缺少 CLI 入口: $FATE_BIN" >&2
    echo "请先在 skill 根目录执行 bash scripts/bootstrap.sh，或在 scripts/project 根目录执行 scripts/setup/bootstrap_fatecat.sh deps" >&2
    exit 1
fi

"$FATE_BIN" --help >/dev/null

dockerfiles=()
while IFS= read -r dockerfile; do
    dockerfiles+=("$dockerfile")
done < <(find "$ROOT/modules" -mindepth 2 -maxdepth 2 -name Dockerfile -print)

if [[ "${#dockerfiles[@]}" -eq 0 ]]; then
    echo "未发现模块 Dockerfile；当前项目构建以 pyproject/fatecat CLI 为准。"
else
    command -v docker >/dev/null 2>&1 || {
        echo "发现 Dockerfile，但缺少 docker 命令" >&2
        exit 1
    }
    for dockerfile in "${dockerfiles[@]}"; do
        module="$(dirname "$dockerfile")"
        name="$(basename "$module")"
        echo "Building $name..."
        docker build -t "$name:latest" "$module"
    done
fi

echo "Build complete!"
