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
config_dir="$(runtime_config_dir "${runtime_root}")"
env_file="${config_dir}/.env"
env_rel="${env_file#${runtime_root}/}"

if git -C "${runtime_root}" ls-files --error-unmatch "${env_rel}" >/dev/null 2>&1; then
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


def assert_int_setting(name: str, default: int, minimum: int, maximum: int | None = None) -> int:
    raw = value(name)
    text = raw or str(default)
    try:
        parsed = int(text)
    except ValueError:
        fail(f"{name} 必须是整数")
    if parsed < minimum:
        fail(f"{name} 必须 >= {minimum}")
    if maximum is not None and parsed > maximum:
        fail(f"{name} 必须 <= {maximum}")
    suffix = "默认值" if not raw else "显式配置"
    ok(f"{name}={parsed} ({suffix})")
    return parsed


cors = value("FATE_CORS_ALLOW_ORIGINS")
if not cors:
    fail("FATE_CORS_ALLOW_ORIGINS 为空；公网生产必须配置明确 allowlist")
origins = [item.strip() for item in cors.split(",") if item.strip()]
if "*" in origins:
    fail("FATE_CORS_ALLOW_ORIGINS 不允许包含 *")
ok(f"CORS allowlist 已配置 {len(origins)} 项")

admin_tokens = [value("FATE_API_TOKEN"), value("FATE_API_ADMIN_TOKEN")]
user_tokens_raw = value("FATE_API_USER_TOKENS")
records_enabled = value("FATE_RECORDS_ENABLED").lower() not in {"0", "false", "no", "off"}
has_auth = any(admin_tokens) or bool(user_tokens_raw)
if records_enabled and not has_auth:
    fail("记录接口已启用但缺少鉴权 token：FATE_API_TOKEN/FATE_API_ADMIN_TOKEN/FATE_API_USER_TOKENS 至少配置一个")
if not records_enabled:
    ok("FATE_RECORDS_ENABLED 已关闭；当前按无状态公共服务验收")

for token_name, token in (("FATE_API_TOKEN", admin_tokens[0]), ("FATE_API_ADMIN_TOKEN", admin_tokens[1])):
    if records_enabled and token:
        assert_real_secret(token_name, token)

if records_enabled and user_tokens_raw:
    user_pairs = [item.strip() for item in user_tokens_raw.split(",") if item.strip()]
    if not user_pairs:
        fail("FATE_API_USER_TOKENS 格式为空")
    allowed_record_scopes = {"record.read", "record.list", "record.write", "record.delete"}
    for pair in user_pairs:
        parts = pair.split(":", 2)
        if len(parts) not in {2, 3}:
            fail("FATE_API_USER_TOKENS 必须使用 user_id:token 或 user_id:token:record.read|record.list 格式")
        user_id, token = parts[0].strip(), parts[1].strip()
        if not user_id or not token:
            fail("FATE_API_USER_TOKENS 必须使用 user_id:token 或 user_id:token:record.read|record.list 格式")
        if len(parts) == 3:
            scopes = {item.strip() for item in parts[2].split("|") if item.strip()}
            if not scopes:
                fail("FATE_API_USER_TOKENS scoped token 必须至少包含一个 record scope")
            invalid_scopes = scopes - allowed_record_scopes
            if invalid_scopes:
                fail(f"FATE_API_USER_TOKENS 包含未知 record scope: {','.join(sorted(invalid_scopes))}")
        assert_real_secret(f"FATE_API_USER_TOKENS[{user_id}]", token)
    ok(f"用户级 API token 已配置 {len(user_pairs)} 项")
elif records_enabled:
    ok("未配置用户级 API token；当前只使用 admin token")

public_multi_tenant = value("FATE_PUBLIC_MULTI_TENANT").lower() in {"1", "true", "yes"}
if public_multi_tenant:
    for required in ("FATE_OIDC_ISSUER", "FATE_OIDC_AUDIENCE", "FATE_OIDC_JWKS_URL"):
        if not value(required):
            fail(f"FATE_PUBLIC_MULTI_TENANT=1 时必须配置 {required}")
    if value("FATE_OIDC_JWKS_URL").startswith("http://"):
        fail("FATE_OIDC_JWKS_URL 在公网多租户生产中必须使用 HTTPS")
    ok("公网多租户身份已声明外部 OIDC/IdP 配置")
else:
    print("[production-readiness] WARN: 未启用 FATE_PUBLIC_MULTI_TENANT；当前身份按 scoped token baseline 验收，不等于生产 OIDC/IdP 已完成")

siem_enabled = value("FATE_AUDIT_SIEM_EXPORT_ENABLED").lower() in {"1", "true", "yes"}
if siem_enabled:
    for required in ("FATE_AUDIT_SIEM_ENDPOINT", "FATE_AUDIT_SIEM_DESTINATION", "FATE_AUDIT_IMMUTABILITY_MODE"):
        if not value(required):
            fail(f"FATE_AUDIT_SIEM_EXPORT_ENABLED=1 时必须配置 {required}")
    assert_real_secret("FATE_AUDIT_SIEM_ENDPOINT", value("FATE_AUDIT_SIEM_ENDPOINT"))
    immutability_mode = value("FATE_AUDIT_IMMUTABILITY_MODE")
    if immutability_mode not in {"append_only", "worm", "external_siem"}:
        fail("FATE_AUDIT_IMMUTABILITY_MODE 必须是 append_only/worm/external_siem")
    ok("外部 SIEM/不可变审计存储准入配置已声明")
else:
    print("[production-readiness] WARN: 未启用 FATE_AUDIT_SIEM_EXPORT_ENABLED；外部 SIEM/不可变审计存储验证待执行")

record_retention_days = assert_int_setting("FATE_RECORD_RETENTION_DAYS", 0, 0, 3650)
auto_cleanup_enabled = value("FATE_RECORD_RETENTION_AUTO_CLEANUP_ENABLED").lower() in {"1", "true", "yes"}
if record_retention_days > 0 and not auto_cleanup_enabled:
    fail("FATE_RECORD_RETENTION_DAYS>0 时必须启用 FATE_RECORD_RETENTION_AUTO_CLEANUP_ENABLED 并提供清理器实现")
if auto_cleanup_enabled:
    delete_mode = value("FATE_RECORD_RETENTION_DELETE_MODE")
    if delete_mode not in {"tombstone_then_purge", "hard_delete"}:
        fail("FATE_RECORD_RETENTION_DELETE_MODE 必须是 tombstone_then_purge/hard_delete")
    ok("记录按时间自动清理策略已声明")
else:
    ok("记录 retention 当前为显式删除 baseline")

bot_token = value("FATE_BOT_TOKEN")
if bot_token:
    assert_real_secret("FATE_BOT_TOKEN", bot_token)
    ok("FATE_BOT_TOKEN 已配置为非占位值")
else:
    print("[production-readiness] WARN: 未配置 FATE_BOT_TOKEN；Bot live 验收无法执行")

assert_int_setting("FATE_MAX_REQUEST_BYTES", 1_048_576, 1024, 10 * 1024 * 1024)
assert_int_setting("FATE_REQUEST_TIMEOUT_SECONDS", 30, 1, 120)
assert_int_setting("FATE_MAX_INFLIGHT_CALCULATIONS", 2, 1, 64)
assert_int_setting("FATE_REPORT_JOB_QUEUE_SIZE", 20, 1, 10_000)
assert_int_setting("FATE_REPORT_JOB_WORKERS", 1, 1, 64)
assert_int_setting("FATE_REPORT_JOB_TTL_SECONDS", 1800, 60, 86_400)
assert_int_setting("FATE_REPORT_JOB_MAX_ATTEMPTS", 1, 1, 10)
assert_int_setting("FATE_REPORT_JOB_ATTEMPT_TIMEOUT_SECONDS", 0, 0, 3_600)
assert_int_setting("FATE_REPORT_JOB_RETRY_BACKOFF_SECONDS", 0, 0, 300)
assert_int_setting("FATE_WEBHOOK_TIMEOUT_SECONDS", 5, 1, 30)
assert_int_setting("FATE_WEBHOOK_MAX_ATTEMPTS", 1, 1, 10)
assert_int_setting("FATE_WEBHOOK_RETRY_BACKOFF_SECONDS", 0, 0, 300)
rate_limit = assert_int_setting("FATE_RATE_LIMIT_PER_MINUTE", 120, 0, 10_000)
if rate_limit == 0:
    fail("FATE_RATE_LIMIT_PER_MINUTE=0 会关闭公网限流")

replicas = assert_int_setting("FATE_DEPLOYMENT_REPLICAS", 1, 1, 100)
rate_limit_backend = (value("FATE_RATE_LIMIT_BACKEND") or "memory").lower()
allowed_rate_limit_backends = {"memory", "gateway", "redis", "waf", "external"}
if rate_limit_backend not in allowed_rate_limit_backends:
    fail("FATE_RATE_LIMIT_BACKEND 必须是 memory/gateway/redis/waf/external")
if replicas > 1 and rate_limit_backend == "memory":
    fail("多副本公网部署不能使用单进程 memory 限流；请改用 gateway/redis/waf/external")
if rate_limit_backend == "memory":
    ok("当前使用单实例内存限流；仅适合单副本或前置网关已限流场景")
else:
    ok(f"已声明外部限流后端：{rate_limit_backend}")

report_job_store = (value("FATE_REPORT_JOB_STORE") or "memory").lower()
allowed_report_job_stores = {"memory", "sqlite"}
if report_job_store not in allowed_report_job_stores:
    fail("FATE_REPORT_JOB_STORE 必须是 memory/sqlite")
if replicas > 1 and report_job_store in {"memory", "sqlite"}:
    fail("多副本公网部署不能使用本地 report job store；请先接入外部队列/数据库任务系统")
if report_job_store == "sqlite":
    db_path = value("FATE_REPORT_JOB_DB_PATH") or "infra/runtime/local-state/database/report_jobs.sqlite"
    if not db_path.endswith((".sqlite", ".sqlite3", ".db")):
        fail("FATE_REPORT_JOB_DB_PATH 应使用 .sqlite/.sqlite3/.db 文件路径")
    ok("已启用 SQLite report job store；仅适合单副本本地持久化")
else:
    ok("当前使用内存 report job store；仅适合单副本或无跨重启任务查询要求场景")

webhooks_enabled = value("FATE_REPORT_JOB_WEBHOOKS_ENABLED").lower() in {"1", "true", "yes"}
if webhooks_enabled:
    ok("已显式启用 report job webhook callback")
    if not value("FATE_WEBHOOK_ALLOWED_HOSTS"):
        print("[production-readiness] WARN: 未配置 FATE_WEBHOOK_ALLOWED_HOSTS；应用层会拒绝内网/本机 URL，但公网生产建议配置接收端 allowlist")
    if value("FATE_WEBHOOK_ALLOW_HTTP").lower() in {"1", "true", "yes"}:
        fail("公网生产不应开启 FATE_WEBHOOK_ALLOW_HTTP；callback URL 应使用 HTTPS")
else:
    ok("report job webhook callback 默认关闭")

if value("FATE_EDGE_BODY_LIMIT_ENABLED").lower() in {"1", "true", "yes"}:
    ok("已声明反向代理/CDN 层请求体上限；应用层仍保留流式兜底限制")
else:
    print("[production-readiness] WARN: 未声明 FATE_EDGE_BODY_LIMIT_ENABLED；公网最好在 Nginx/Traefik/Cloudflare 层限制请求体")

if value("FATE_TRUST_PROXY_HEADERS").lower() in {"1", "true", "yes"}:
    ok("已启用可信反向代理头解析；必须确保只有可信代理能访问服务直连端口")
else:
    print("[production-readiness] WARN: 未启用 FATE_TRUST_PROXY_HEADERS；反向代理后限流会按代理 IP 聚合")

if value("FATE_ENABLE_HSTS").lower() in {"1", "true", "yes"}:
    ok("已启用应用层 HSTS 响应头")
else:
    print("[production-readiness] WARN: 未启用 FATE_ENABLE_HSTS；若由反向代理设置 HSTS，可忽略此项")

ok("生产配置静态门禁通过")
PY

if [[ -n "${api_url}" ]]; then
  echo "[production-readiness] live API health: ${api_url}/health"
  curl -fsS "${api_url}/health" >/dev/null
  echo "[production-readiness] OK: live API health 通过"
  echo "[production-readiness] live API readiness: ${api_url}/ready"
  curl -fsS "${api_url}/ready" >/dev/null
  echo "[production-readiness] OK: live API readiness 通过"
  echo "[production-readiness] live API metrics: ${api_url}/metrics"
  metrics_file="$(mktemp)"
  trap 'rm -f "${metrics_file}"' EXIT
  curl -fsS "${api_url}/metrics" -o "${metrics_file}"
  grep -q 'fatecat_requests_total' "${metrics_file}"
  echo "[production-readiness] OK: live API metrics 通过"
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
