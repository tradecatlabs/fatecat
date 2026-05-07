# 外部依赖库

> FateCat 使用的外部成熟仓库说明

## 目录结构

```text
assets/vendor/
├── github/    # GitHub 开源仓库快照
└── web/       # 网页资源与抓取结果
```

## 依赖库清单

### 必需依赖

| 库名 | 目录 | 语言 | 用途 | 来源 |
|------|------|------|------|------|
| lunar-python | `assets/vendor/github/lunar-python-master` | Python | 核心历法计算 | https://github.com/6tail/lunar-python |
| bazi-1 | `assets/vendor/github/bazi-1-master` | Python | 八字神煞格局 | https://github.com/nicktaobo/bazi-1 |
| sxwnl | `assets/vendor/github/sxwnl-master` | JavaScript | 寿星万年历 | https://github.com/nicktaobo/sxwnl |
| paipan | `assets/vendor/github/paipan-master` | JavaScript | 真太阳时与早晚子时 | GitHub |

### 扩展依赖

| 库名 | 目录 | 语言 | 用途 | 来源 |
|------|------|------|------|------|
| MingLi-Bench | `assets/vendor/github/MingLi-Bench-main` | Python/JSON | 八字与紫微斗数 LLM 推理评测基准 | https://github.com/DestinyLinker/MingLi-Bench |
| fortel-ziweidoushu | `assets/vendor/github/fortel-ziweidoushu-main` | TypeScript | 紫微斗数 | https://github.com/fortelzhao/fortel-ziweidoushu |
| iztro | `assets/vendor/github/iztro-main` | TypeScript | 紫微斗数 | https://github.com/SylarLong/iztro |
| dantalion | `assets/vendor/github/dantalion-master` | TypeScript | 现代八字分析 | https://github.com/nicktaobo/dantalion |
| mikaboshi | `assets/vendor/github/mikaboshi-main` | Rust | 风水罗盘 | https://github.com/nicktaobo/mikaboshi |
| Chinese-Divination | `assets/vendor/github/Chinese-Divination-master` | Python | 六爻/梅花 | GitHub |
| Iching | `assets/vendor/github/Iching-master` | Python | 易经系统 | GitHub |
| holiday-calendar | `assets/vendor/github/holiday-and-chinese-almanac-calendar-main` | ICS | 黄历数据 | GitHub |
| chinese-calendar | `assets/vendor/github/chinese-calendar-master` | Python | 农历转换 | https://github.com/LKI/chinese-calendar |
| js_astro | `assets/vendor/github/js_astro-master` | JavaScript | 天文计算 | GitHub |

## 使用方式

所有外部库路径统一通过 `_paths.py` 管理：

```python
from _paths import (
    LUNAR_PYTHON_DIR,
    BAZI_1_DIR,
    SXWNL_DIR,
    IZTRO_DIR,
    DANTALION_DIR,
    PAIPAN_DIR,
)
```

## 分发与治理

- `vendor_sources.json` 是 vendor 来源与分发边界的真相源。
- 当前仓库保留 vendor 快照，以保证离线 smoke、导出包和 GitHub Actions 能复现。
- Benchmark 类 vendor 只作为评测与参考资产，默认不接入生产运行链路。
- 后续若切换到 release artifact、Git LFS、submodule 或按需下载，必须先保证 `scripts/vendor-health.sh` 通过。

## 维护规则

1. `assets/vendor/` 默认只读
2. 不复制外部库源码到服务目录二次维护
3. 所有集成层放在 `services/telegram/src/*_integration.py`
4. 缺失依赖时，优先补 vendor 快照，而不是重写算法

## 安装/更新

统一下载脚本：

```bash
./scripts/download_libs.sh
```

Node.js 依赖示例：

```bash
cd assets/vendor/github/sxwnl-master && npm install
cd assets/vendor/github/iztro-main && npm install
cd assets/vendor/github/dantalion-master/packages/dantalion-core && npm install && npm run build
```

Rust 依赖示例：

```bash
cd assets/vendor/github/mikaboshi-main && cargo build --release
```
