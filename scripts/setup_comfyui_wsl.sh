#!/usr/bin/env bash
set -euxo pipefail

REPO_WIN="${1:-/home/lenovo/.projects/cat/fatecat}"
COMFY_HOME="${HOME}/projects/ComfyUI"
COMFY_CUSTOM_NODES="${COMFY_HOME}/ComfyUI/custom_nodes"
COMFY_WORKFLOWS="${COMFY_HOME}/ComfyUI/user/default/workflows"

mkdir -p "${COMFY_CUSTOM_NODES}" "${COMFY_WORKFLOWS}"

cp -r "${REPO_WIN}/comfyui/fatecat_comfyui" "${COMFY_CUSTOM_NODES}/fatecat_comfyui"
cp "${REPO_WIN}"/comfyui/workflows/*.json "${COMFY_WORKFLOWS}/"

"${COMFY_HOME}/.venv/bin/python" -m pip install -e "${REPO_WIN}" --quiet

echo "FateCat ComfyUI 节点包与 Workflow 已部署到 ${COMFY_HOME}。"
echo "重启 ComfyUI 后生效；启动命令示例（需 export FATECAT_REPO）："
echo "  export FATECAT_REPO=${REPO_WIN}"
echo "  cd ${COMFY_HOME}/ComfyUI && setsid nohup ../.venv/bin/python main.py --listen 127.0.0.1 --port 8189 --database-url ${COMFY_HOME}/ComfyUI/user/fatecat-comfyui.db > ${HOME}/fatecat-comfyui.log 2>&1 < /dev/null &"
