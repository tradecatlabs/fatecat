#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

require_live_bot="0"
api_url=""
skip_bootstrap="0"

usage() {
  cat <<'EOF'
用法:
  bash scripts/production-readiness.sh [--require-live-bot] [--api-url <url>] [--skip-bootstrap]

说明:
  - 检查生产配置是否具备最小安全边界：API 鉴权、CORS allowlist、真实 token 口径、.env 不入库
  - --require-live-bot 会调用 scripts/live-bot-smoke.sh，真实连接 Telegram Bot API
  - --api-url 会请求 <url>/health，验证已部署 API 的 live health
  - 不传真实凭证时不会伪造线上通过；需要外部环境的项会直接失败或标注未执行
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --require-live-bot)
      require_live_bot="1"
      shift
      ;;
    --api-url)
      [[ $# -ge 2 ]] || usage_error "--api-url 缺少参数"
      api_url="${2%/}"
      shift 2
      ;;
    --skip-bootstrap)
      skip_bootstrap="1"
      shift
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

if [[ "${skip_bootstrap}" != "1" ]]; then
  bash "${script_dir}/bootstrap.sh" >/dev/null
fi

runtime_root="$(resolve_runtime_root)"
env_file="${runtime_root}/assets/config/.env"

if git -C "${runtime_root}" ls-files --error-unmatch assets/config/.env >/dev/null 2>&1; then
  die "生产 .env 已进入 Git 跟踪，必须移除并轮换所有相关凭证"
fi

"${runtime_root}/.venv/bin/python" - "${env_file}" <<'PY'
from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import dotenv_values

env_path = Path(sys.argv[1])
file_values = dotenv_values(env_path) if env_path.exists() else {}


def value(name: str) -> str:
    return (os.getenv(name) or file_values.get(name) or "").strip()


def fail(message: str) -> None:
    print(f"[production-readiness] FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def ok(message: str) -> None:
    print(f"[production-readiness] OK: {message}")


def assert_real_secret(name: str, secret: str) -> None:
    if not secret:
        fail(f"缺少 {name}")
    lowered = secret.lower()
    blocked = ("placeholder", "smoke", "your_", "change-me", "changeme", "你的token", "测试")
    if any(marker in lowered for marker in blocked):
        fail(f"{name} 看起来是占位值")


cors = value("FATE_CORS_ALLOW_ORIGINS")
if not cors:
    fail("FATE_CORS_ALLOW_ORIGINS 为空；公网生产必须配置明确 allowlist")
origins = [item.strip() for item in cors.split(",") if item.strip()]
if "*" in origins:
    fail("FATE_CORS_ALLOW_ORIGINS 不允许包含 *")
ok(f"CORS allowlist 已配置 {len(origins)} 项")

admin_tokens = [value("FATE_API_TOKEN"), value("FATE_API_ADMIN_TOKEN")]
user_tokens_raw = value("FATE_API_USER_TOKENS")
has_auth = any(admin_tokens) or bool(user_tokens_raw)
if not has_auth:
    fail("缺少 API 记录接口鉴权 token：FATE_API_TOKEN/FATE_API_ADMIN_TOKEN/FATE_API_USER_TOKENS 至少配置一个")

for token_name, token in (("FATE_API_TOKEN", admin_tokens[0]), ("FATE_API_ADMIN_TOKEN", admin_tokens[1])):
    if token:
        assert_real_secret(token_name, token)

if user_tokens_raw:
    user_pairs = [item.strip() for item in user_tokens_raw.split(",") if item.strip()]
    if not user_pairs:
        fail("FATE_API_USER_TOKENS 格式为空")
    for pair in user_pairs:
        user_id, sep, token = pair.partition(":")
        if not sep or not user_id.strip() or not token.strip():
            fail("FATE_API_USER_TOKENS 必须使用 user_id:token,user_id2:token2 格式")
        assert_real_secret(f"FATE_API_USER_TOKENS[{user_id.strip()}]", token.strip())
    ok(f"用户级 API token 已配置 {len(user_pairs)} 项")
else:
    ok("未配置用户级 API token；当前只使用 admin token")

bot_token = value("FATE_BOT_TOKEN")
if bot_token:
    assert_real_secret("FATE_BOT_TOKEN", bot_token)
    ok("FATE_BOT_TOKEN 已配置为非占位值")
else:
    print("[production-readiness] WARN: 未配置 FATE_BOT_TOKEN；Bot live 验收无法执行")

ok("生产配置静态门禁通过")
PY

if [[ -n "${api_url}" ]]; then
  echo "[production-readiness] live API health: ${api_url}/health"
  curl -fsS "${api_url}/health" >/dev/null
  echo "[production-readiness] OK: live API health 通过"
else
  echo "[production-readiness] SKIP: 未提供 --api-url，外部 API 连通验证待执行"
fi

if [[ "${require_live_bot}" == "1" ]]; then
  echo "[production-readiness] live Bot smoke"
  bash "${script_dir}/live-bot-smoke.sh"
else
  echo "[production-readiness] SKIP: 未提供 --require-live-bot，真实 Bot 连通验证待执行"
fi

echo "[production-readiness] done"
