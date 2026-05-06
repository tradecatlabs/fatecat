#!/bin/bash
# FateCat 外部环境搭建脚本
# 用于搭建 Node.js、Rust 等外部依赖环境

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
VENDOR_GITHUB_DIR="$ROOT/assets/vendor/github"

echo "🚀 FateCat 外部环境搭建开始"
echo "═══════════════════════════════════════════════════════════════"
echo "说明：该脚本只安装/构建已存在的外部依赖，不会在 vendor 目录内生成 package.json 或 Cargo.toml。"

install_node_repo() {
    local repo="$1"
    local label="$2"

    if ! command -v npm >/dev/null 2>&1; then
        echo "⚠️ 未找到 npm，跳过 $label"
        return
    fi

    if [ ! -d "$repo" ]; then
        echo "⚠️ 外部仓库不存在，跳过 $label: $repo"
        return
    fi

    cd "$repo"
    if [ -f "package.json" ]; then
        npm install
        echo "✅ $label Node.js 依赖安装完成"
    else
        echo "⚠️ $label 缺少 package.json，跳过；请补齐原始 vendor 仓库，不在此处生成替代项目"
    fi
}

# 1. 安装Node.js依赖包
echo "📦 1. 安装Node.js依赖包..."
install_node_repo "$VENDOR_GITHUB_DIR/sxwnl-master" "寿星万年历"

# 2. 编译Rust项目
echo "🦀 2. 编译Rust项目..."
if [ ! -d "$VENDOR_GITHUB_DIR/mikaboshi-main" ]; then
    echo "⚠️ 风水罗盘外部仓库不存在，跳过"
elif ! command -v cargo >/dev/null 2>&1; then
    echo "⚠️ 未找到 cargo，跳过风水罗盘 Rust 构建"
else
    cd "$VENDOR_GITHUB_DIR/mikaboshi-main"
    if [ -f "Cargo.toml" ]; then
        cargo build --release
        echo "✅ 风水罗盘Rust项目编译完成"
    else
        echo "⚠️ 风水罗盘缺少 Cargo.toml，跳过；请补齐原始 vendor 仓库，不在此处 cargo init"
    fi
fi

# 3. 安装天文计算库
echo "🌟 3. 安装天文计算库..."
install_node_repo "$VENDOR_GITHUB_DIR/js_astro-master" "天文计算库"

# 4. 创建Python绑定
echo "🐍 4. 创建Python绑定..."
if [ -x "$ROOT/.venv/bin/pip" ]; then
    "$ROOT/.venv/bin/pip" install nodejs cffi pycparser
else
    echo "⚠️ 未找到项目虚拟环境，跳过 Python 绑定依赖安装；请先执行 skill 根目录 scripts/bootstrap.sh"
fi

# 5. 测试环境
echo "🧪 5. 测试外部环境..."
python3 -c "
import subprocess
import sys

print('测试Node.js环境:')
try:
    result = subprocess.run(['node', '--version'], capture_output=True, text=True)
    print(f'✅ Node.js: {result.stdout.strip()}')
except:
    print('❌ Node.js测试失败')

print('测试Rust环境:')
try:
    result = subprocess.run(['rustc', '--version'], capture_output=True, text=True)
    print(f'✅ Rust: {result.stdout.strip()}')
except:
    print('❌ Rust测试失败')

print('测试Python环境:')
print(f'✅ Python: {sys.version.split()[0]}')
"

echo "═══════════════════════════════════════════════════════════════"
echo "🎉 FateCat 外部环境检查完成！"
echo "   Node.js / Rust / Python 状态以上方日志为准"
echo "   缺失的外部 vendor 项目会被跳过，不会自动生成替代源码"
echo "═══════════════════════════════════════════════════════════════"
