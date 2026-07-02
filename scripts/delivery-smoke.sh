#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

target="api"
host="127.0.0.1"
port="8001"
startup_timeout="20"
response_file=""
log_file=""
child_pid=""
temp_env_created="0"
temp_env_file=""
placeholder_token="placeholder-token-for-skill-delivery-smoke"

usage() {
  cat <<'EOF'
用法:
  bash scripts/delivery-smoke.sh [--target api|bot] [--host <host>] [--port <port>]
                                 [--startup-timeout <seconds>]
                                 [--response-file <file>] [--log-file <file>]

说明:
  - 先执行 delivery preflight，再做一次可回收的交付层烟雾验证
  - target=api：启动 API，探测 /health，并可把响应写入文件
  - target=bot：启动 Bot，要求在宽限期内不提前崩溃；到时后主动停止进程
EOF
}

cleanup() {
  if [[ -n "${child_pid}" ]] && kill -0 "${child_pid}" 2>/dev/null; then
    kill "${child_pid}" >/dev/null 2>&1 || true
    wait "${child_pid}" >/dev/null 2>&1 || true
  fi
  if [[ "${temp_env_created}" == "1" && -n "${temp_env_file}" && -f "${temp_env_file}" ]]; then
    rm -f "${temp_env_file}"
  fi
}

trap cleanup EXIT

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target)
      [[ $# -ge 2 ]] || usage_error "--target 缺少参数"
      target="$2"
      shift 2
      ;;
    --host)
      [[ $# -ge 2 ]] || usage_error "--host 缺少参数"
      host="$2"
      shift 2
      ;;
    --port)
      [[ $# -ge 2 ]] || usage_error "--port 缺少参数"
      port="$2"
      shift 2
      ;;
    --startup-timeout)
      [[ $# -ge 2 ]] || usage_error "--startup-timeout 缺少参数"
      startup_timeout="$2"
      shift 2
      ;;
    --response-file)
      [[ $# -ge 2 ]] || usage_error "--response-file 缺少参数"
      response_file="$2"
      shift 2
      ;;
    --log-file)
      [[ $# -ge 2 ]] || usage_error "--log-file 缺少参数"
      log_file="$2"
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

case "${target}" in
  api|bot)
    ;;
  *)
    usage_error "--target 只支持 api 或 bot"
    ;;
esac

case "${startup_timeout}" in
  ''|*[!0-9]*)
    usage_error "--startup-timeout 必须是正整数秒"
    ;;
esac

runtime_root="$(resolve_runtime_root)"
config_dir="$(runtime_config_dir "${runtime_root}")"
env_file="${config_dir}/.env"
if [[ -z "${log_file}" ]]; then
  log_file="/tmp/fatecat-delivery-smoke-${target}-$(date +%Y%m%d%H%M%S).log"
fi
ensure_parent_dir "${log_file}"

if [[ -n "${response_file}" ]]; then
  ensure_parent_dir "${response_file}"
fi

if [[ ! -f "${env_file}" ]]; then
  template_file="${config_dir}/agent.env.example"
  if [[ ! -f "${template_file}" ]]; then
    template_file="${config_dir}/.env.example"
  fi
  [[ -f "${template_file}" ]] || die "缺少配置模板：${config_dir}/.env.example"
  cat > "${env_file}" <<EOF
# 该文件由 delivery-smoke.sh 自动生成，仅用于本地烟雾验证，脚本退出后会自动删除。
FATE_BOT_TOKEN=${placeholder_token}
FATE_ADMIN_USER_IDS=
FATE_BOT_PROXY_URL=
FATE_SERVICE_HOST=${host}
FATE_SERVICE_PORT=${port}
EOF
  temp_env_created="1"
  temp_env_file="${env_file}"
  echo "[delivery-smoke] 已生成临时 .env 用于烟雾验证"
fi

echo "[delivery-smoke] preflight mode=delivery"
bash "${script_dir}/preflight.sh" --mode delivery --bootstrap --pretty

case "${target}" in
  api)
    echo "[delivery-smoke] start api -> ${log_file}"
    FATE_SERVICE_HOST="${host}" FATE_SERVICE_PORT="${port}" bash "${script_dir}/serve-api.sh" > "${log_file}" 2>&1 &
    child_pid="$!"
    deadline=$((SECONDS + startup_timeout))
    while (( SECONDS < deadline )); do
      if ! kill -0 "${child_pid}" 2>/dev/null; then
        echo "[delivery-smoke] api 进程提前退出，日志如下：" >&2
        tail -n 40 "${log_file}" >&2 || true
        exit 1
      fi

      probe_output="$("${runtime_root}/.venv/bin/python" - "${host}" "${port}" <<'PY'
import json
import sys
import urllib.error
import urllib.request

host = sys.argv[1]
port = sys.argv[2]
url = f"http://{host}:{port}/health"
try:
    with urllib.request.urlopen(url, timeout=1.5) as response:
        body = response.read().decode("utf-8")
        if response.status != 200:
            raise SystemExit(1)
        print(body)
except (urllib.error.URLError, TimeoutError, OSError):
    raise SystemExit(1)
PY
      )" || true

      if [[ -n "${probe_output}" ]]; then
        if [[ -n "${response_file}" ]]; then
          printf '%s\n' "${probe_output}" > "${response_file}"
        fi
        echo "[delivery-smoke] api ready: http://${host}:${port}/health"
        exit 0
      fi

      sleep 1
    done

    echo "[delivery-smoke] api 在 ${startup_timeout}s 内未通过 /health 探测，日志如下：" >&2
    tail -n 40 "${log_file}" >&2 || true
    exit 1
    ;;
  bot)
    echo "[delivery-smoke] start bot -> ${log_file}"
    if ! FATE_BOT_DRY_RUN=1 bash "${script_dir}/serve-bot.sh" > "${log_file}" 2>&1; then
      echo "[delivery-smoke] bot dry-run 失败，日志如下：" >&2
      tail -n 60 "${log_file}" >&2 || true
      exit 1
    fi

    if [[ -n "${response_file}" ]]; then
      cat > "${response_file}" <<EOF
{"success":true,"target":"bot","mode":"dry-run","logFile":"${log_file}"}
EOF
    fi
    echo "[delivery-smoke] bot dry-run 初始化通过"
    exit 0
    ;;
esac
