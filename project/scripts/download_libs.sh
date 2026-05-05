#!/usr/bin/env bash
# 下载八字排盘相关开源库到 assets/vendor/github/

set -euo pipefail

if [[ "${FATECAT_ALLOW_VENDOR_DOWNLOAD:-0}" != "1" ]]; then
    echo "该脚本会向 project/assets/vendor/github 写入外部仓库快照，默认禁止在生产整理流程中执行。" >&2
    echo "若确实要补齐 vendor 研究素材，请显式设置 FATECAT_ALLOW_VENDOR_DOWNLOAD=1 后再运行。" >&2
    exit 1
fi

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_DIR="$ROOT/assets/vendor/github"
mkdir -p "$TARGET_DIR"
cd "$TARGET_DIR"

download_repo() {
    local repo="$1"
    local name
    name=$(echo "$repo" | sed 's/.*\///')
    
    if [ -d "${name}-main" ] || [ -d "${name}-master" ] || [ -d "$name" ]; then
        echo "⏭️  跳过 $repo (已存在)"
        return
    fi
    
    echo "📥 下载 $repo ..."
    
    # 尝试 main 分支
    if curl -sL "https://github.com/$repo/archive/refs/heads/main.zip" -o temp.zip 2>/dev/null && unzip -t temp.zip >/dev/null 2>&1; then
        unzip -q temp.zip && rm temp.zip
        echo "✅ $name-main"
    # 尝试 master 分支
    elif curl -sL "https://github.com/$repo/archive/refs/heads/master.zip" -o temp.zip 2>/dev/null && unzip -t temp.zip >/dev/null 2>&1; then
        unzip -q temp.zip && rm temp.zip
        echo "✅ $name-master"
    else
        rm -f temp.zip
        echo "❌ 失败: $repo"
    fi
}

echo "=========================================="
echo "开始下载八字排盘相关开源库"
echo "=========================================="

# ⭐ 高度符合 - 6tail/lunar 系列
download_repo "6tail/lunar-python"
download_repo "6tail/lunar-java"
download_repo "6tail/lunar-javascript"
download_repo "6tail/lunar-go"
download_repo "6tail/lunar-php"
download_repo "6tail/lunar-csharp"
download_repo "6tail/lunar-swift"

# ⭐ 高度符合 - 其他核心库
download_repo "SylarLong/iztro"
download_repo "warrially/BaziGo"
download_repo "alvamind/bazi-calculator-by-alvamind"
download_repo "tommitoan/bazica"

# 🟡 紫微斗数
download_repo "SylarLong/react-iztro"
download_repo "airicyu/fortel-ziweidoushu"
download_repo "cubshuang/ZiWeiDouShu"
download_repo "lzm0x219/ziwei"
download_repo "fxp/misc-ziweidoushu"
download_repo "skirby359/tzuwei"

# 🔶 部分符合
download_repo "CrystalMarch/bazi"
download_repo "china-testing/bazi"
download_repo "meimeitao/bazi"
download_repo "cautionsign/bazi-1"
download_repo "SmallTeddyGames/divination-bazi"
download_repo "sxin0/Bazi_Hehun"
download_repo "zhaolandelong/bazi-name"
download_repo "SandroBasta/BaziCalculator"
download_repo "l2yao/Iching"

# 📚 历法/日历
download_repo "ytliu0/ChineseCalendar"
download_repo "wolfhong/LunarCalendar"
download_repo "magiclen/chinese-lunisolar-calendar"
download_repo "lhttjdr/calendar"
download_repo "LEOYoon-Tsaw/ChineseTime"
download_repo "golang-module/carbon"
download_repo "Lofanmi/chinese-calendar-golang"
download_repo "messense/rust-lunardate"
download_repo "ngobach/amlich.rs"
download_repo "LKI/chinese-calendar"
download_repo "yize/chinese-workday"

# 🔮 寿星天文历
download_repo "sxwnl/sxwnl-cpp"
download_repo "iceplumblossom/sxwnl"
download_repo "sxwnl/sxwnl.github.io"

# 🎴 周易/六爻
download_repo "volcanofly/Chinese-Divination"
download_repo "player2point0/i-ching-calculator"
download_repo "shuishang/nhyai"

# 🌏 风水
download_repo "minagawah/mikaboshi"
download_repo "Tai-Zhou/astrolator"
download_repo "astsakai/js_astro"

# 🔗 其他
download_repo "schummar/bazi"
download_repo "mawentao/bazi"
download_repo "kiddx01/lunar"
download_repo "zqzess/holiday-and-chinese-almanac-calendar"
download_repo "MenoData/Time4J"

# 🌟 真太阳时/早晚子时
download_repo "hkargc/paipan"
download_repo "hkargc/JavaScript-For-Paipan"
download_repo "liujiawm/paipan"

# 💎 高质量专业库
download_repo "yhj1024/Manseryeok"
download_repo "kurone-kito/dantalion"
download_repo "airicyu/Fortel"
download_repo "0x219/ziwei.js"
download_repo "liumulingyu/zhouyi"

echo ""
echo "=========================================="
echo "下载完成！"
echo "=========================================="
ls -la
