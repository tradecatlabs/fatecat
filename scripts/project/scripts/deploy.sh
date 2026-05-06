#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
K8S_DIR="$ROOT/infrastructure/kubernetes"

echo "Deploying FateCat project..."

cd "$ROOT"
"$ROOT/scripts/build_all.sh"

if [[ ! -d "$K8S_DIR" ]]; then
    echo "未找到 Kubernetes manifests: $K8S_DIR" >&2
    echo "当前 skill 仓库默认生产入口是根目录 scripts/serve-api.sh、scripts/serve-bot.sh 与 scripts/acceptance.sh；没有 k8s manifests 时不执行伪部署。" >&2
    exit 1
fi

command -v kubectl >/dev/null 2>&1 || {
    echo "缺少 kubectl，无法部署 Kubernetes manifests" >&2
    exit 1
}

kubectl apply -f "$K8S_DIR"

echo "Deployment complete!"
