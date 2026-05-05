#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

output_dir=""

usage() {
  cat <<'EOF'
用法:
  bash scripts/collect-ops-bundle.sh --output <dir>
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --output)
      [[ $# -ge 2 ]] || usage_error "--output 缺少参数"
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

if [[ -z "${output_dir}" ]]; then
  usage >&2
  exit 2
fi

bundle_root="$(mkdir -p "${output_dir}" && cd "${output_dir}" && pwd)"
runtime_root="$(resolve_runtime_root)"
git_rev="$(git -C "${skill_root}" rev-parse HEAD 2>/dev/null || echo unknown)"
generated_at="$(date '+%Y-%m-%dT%H:%M:%S%z')"

mkdir -p "${bundle_root}/skill"
cp "${skill_root}/SKILL.md" "${bundle_root}/skill/SKILL.md"
cp "${skill_root}/README.md" "${bundle_root}/skill/README.md"
cp "${skill_root}/references/index.md" "${bundle_root}/skill/references-index.md"
cp "${skill_root}/references/ops-pack.md" "${bundle_root}/skill/ops-pack.md"

cat > "${bundle_root}/metadata.txt" <<EOF
generated_at=${generated_at}
skill_root=${skill_root}
project_root=${runtime_root}
git_rev=${git_rev}
EOF

bootstrap_state="not-ready"
if fatecat_bin="$(resolve_fatecat_bin "${runtime_root}" 2>/dev/null)"; then
  bootstrap_state="ready"
  bash "${script_dir}/health.sh" --mode pure --json > "${bundle_root}/health-pure.json" || true
  "${fatecat_bin}" --help > "${bundle_root}/fatecat-help.txt" || true
fi

if [[ -f "${runtime_root}/assets/config/.env.example" ]]; then
  cp "${runtime_root}/assets/config/.env.example" "${bundle_root}/env.example"
fi

latest_pack_path="$(latest_lifecycle_pack || true)"
if [[ -n "${latest_pack_path}" ]]; then
  bash "${script_dir}/lifecycle-status.sh" --pack "${latest_pack_path}" > "${bundle_root}/lifecycle-status.txt"
else
  cat > "${bundle_root}/lifecycle-status.txt" <<EOF
未发现根级生命周期包。
如需沉淀阶段状态，请先执行：
bash scripts/init-lifecycle-pack.sh --name <slug>
EOF
fi

cat > "${bundle_root}/SUMMARY.md" <<EOF
# FateCat Ops Bundle

- 生成时间：${generated_at}
- git 版本：${git_rev}
- project 根：${runtime_root}
- bootstrap 状态：${bootstrap_state}

## 包内文件

- \`metadata.txt\`：基本元信息
- \`health-pure.json\`：纯分析健康检查结果
- \`fatecat-help.txt\`：CLI 帮助输出
- \`lifecycle-status.txt\`：最近生命周期包状态
- \`env.example\`：配置模板
- \`skill/\`：skill 入口与运维说明副本

## 恢复入口

- 安装环境：\`bash scripts/bootstrap.sh\`
- 标准预检：\`bash scripts/preflight.sh --mode pure --bootstrap --pretty\`
- 仓库验收：\`bash scripts/acceptance.sh --with-dev\`
- API 烟雾验证：\`bash scripts/delivery-smoke.sh --target api\`
- Bot 烟雾验证：\`bash scripts/delivery-smoke.sh --target bot --startup-timeout 8\`
- API 启动：\`bash scripts/serve-api.sh\`
- Bot 启动：\`bash scripts/serve-bot.sh\`

## 说明

- 如果缺少 \`health-pure.json\` 或 \`fatecat-help.txt\`，通常表示还未 bootstrap，或 \`.venv/bin/fatecat\` 已失效。
- 当前 bundle 只沉淀 repo 内能证明的证据，不自动创建外部守护器。
EOF

echo "运维包已生成: ${bundle_root}"
