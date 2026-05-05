# AGENTS.md - FateCat 开发指南

> AI Agent 操作手册 | 最后更新: 2026-04-20

## 项目概述

FateCat 是命理分析仓库，定位为：

- `assets/`：静态资产真相源
- `runtime/`：运行态数据
- `modules/fate_core/`：纯命理分析内核
- `modules/telegram/`：Telegram / API 交付层
- `skills/`：面向 Agent 的可复用技能封装层

本仓库已经移除旧的 `libs/`、顶层 `docs/`、顶层 `deploy/` 组织方式。

---

## 目录结构

```text
fatecat/
├── Makefile
├── pyproject.toml
├── assets/
│   ├── AGENTS.md
│   ├── config/                    # 配置模板与配置文件
│   ├── data/                      # 静态数据
│   ├── database/                  # schema 等静态数据库资产
│   ├── deploy/                    # 打包部署脚本与 Agent 自举脚本
│   ├── docs/                      # 文档与历史记录
│   ├── fate/                      # 字段 profile / 未来功能登记
│   └── vendor/                    # 外部成熟仓库，只读
├── runtime/
│   ├── AGENTS.md
│   └── database/                  # SQLite 实库等运行态数据
├── modules/
│   ├── fate_core/                 # 纯分析内核
│   └── telegram/
│       ├── src/
│       │   ├── _paths.py          # 统一路径真相源
│       │   ├── bot.py             # Telegram Bot
│       │   ├── main.py            # FastAPI 入口
│       │   ├── db_v2.py           # 数据库访问层
│       │   ├── bazi_calculator.py # 遗留总装配器
│       │   └── *_integration.py   # 外部库胶水层
│       ├── scripts/
│       ├── output/
│       └── start.py
├── skills/
│   ├── AGENTS.md
│   └── fatecat/                   # FateCat skill 外壳与导出脚本
├── .venv/bin/fatecat              # 安装后可用的统一 CLI
├── scripts/
└── tests/
```

---

## 路径与配置约束

### 配置文件

统一配置路径：

```text
assets/config/.env
assets/config/.env.example
assets/config/branding.json
```

必需变量：

```env
FATE_BOT_TOKEN=xxx
FATE_ADMIN_USER_IDS=xxx
FATE_SERVICE_HOST=0.0.0.0
FATE_SERVICE_PORT=8001
```

### 强制规则

- ❌ 禁止在仓库根目录或 `modules/telegram/` 下创建 `.env`
- ❌ 禁止硬编码绝对路径
- ❌ 禁止把运行态 `.db` 放回 `assets/database/`
- ❌ 禁止修改 `assets/vendor/` 下外部库源码
- ✅ 所有路径统一经由 `modules/telegram/src/_paths.py`

---

## 模块边界

### `assets/`

- `config/`：配置模板与配置文件
- `data/`：静态 CSV / 数据文件
- `database/`：数据库 schema；不放运行态实库
- `deploy/`：部署与打包脚本
- `docs/`：架构文档、故障记录、说明文档
- `fate/`：输出字段 profile 真相源与标准报告退役能力的新功能候选表
- `vendor/`：外部成熟仓库与网页资源，只读

### `runtime/`

- 只放运行态结果
- 当前主要内容是 `runtime/database/bazi/bazi.db`
- 不放文档、脚本、配置模板

### `modules/fate_core/`

- 负责纯命理分析能力
- 允许依赖 `assets/fate/` 中的字段 profile
- 禁止依赖 Telegram / FastAPI / Bot UI

### `modules/telegram/`

- 负责 Bot / API / 报告交付
- 允许调用 `fate_core` 与外部成熟仓库
- 不负责定义字段 profile 真相源

### `skills/`

- 负责把 FateCat 能力封装成 Agent 可消费的 skill 入口
- `skills/fatecat/SKILL.md` 只承载触发规则、边界、命令模式与引用导航
- `skills/fatecat/scripts/` 放包装脚本与导出脚本，不在仓库内复制整份运行时代码
- 如需独立分发 skill，优先通过导出脚本物化 `fatecat_runtime/`，避免在源仓库里自嵌套复制

---

## `_paths.py` 使用规范

统一从 `_paths.py` 获取路径：

```python
from _paths import (
    REPO_ROOT,
    CONFIG_DIR,
    ENV_FILE,
    BAZI_SCHEMA_PATH,
    BAZI_DB_PATH,
    CHINA_COORDS_CSV,
    LUNAR_PYTHON_DIR,
    get_env_file,
    ensure_dirs,
    startup_check,
)
```

禁止这样做：

```python
load_dotenv("/home/xxx/.env")
sys.path.insert(0, "/path/to/project/assets/vendor")
```

---

## 数据库约束

- schema：`assets/database/bazi/schema_v2.sql`
- 实库：`runtime/database/bazi/bazi.db`
- 访问层：`modules/telegram/src/db_v2.py`

这三个位置职责必须分离：

1. schema 属于静态资产
2. `.db` 属于运行态
3. Python 访问层属于模块代码

---

## 开发规则

### 允许修改

- `modules/fate_core/`
- `modules/telegram/src/`
- `modules/telegram/scripts/`
- `assets/fate/`
- `assets/docs/`
- `assets/deploy/`
- `assets/database/` 中的 schema
- `Makefile`、`pyproject.toml`

### 禁止修改

- `assets/vendor/github/`
- `assets/vendor/web/`
- `assets/config/.env`

### 新功能落点

- 纯命理分析：优先进入 `modules/fate_core/`
- 交付层接口：进入 `modules/telegram/`
- 输出字段配置：先改 `assets/fate/`
- 部署变更：改 `assets/deploy/`
- Skill 封装与 Agent 入口：进入 `skills/fatecat/`

---

## 启动与检查

启动前默认执行：

1. `ensure_dirs()`：确保运行目录存在
2. `check_dependencies()`：检查配置与外部依赖
3. `db.ensure_db()`：初始化数据库表

常用命令：

```bash
make install
make lint
make test
make start
make stop
make status
make bootstrap-openclaw
make bootstrap-harness
.venv/bin/fatecat health --mode pure --json
.venv/bin/fatecat pure-analysis --input-json '{"birthDateTime":"1990-01-01 08:00:00","gender":"男","longitude":116.4074,"latitude":39.9042}'
```

---

## 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| `未设置 FATE_BOT_TOKEN` | 配置缺失 | 编辑 `assets/config/.env` |
| `no such table: records` | 数据库未初始化 | 启动模块或执行 `db.ensure_db()` |
| `配置文件不存在` | `.env` 缺失 | `cp assets/config/.env.example assets/config/.env` |
| `缺少必需依赖` | 外部库不完整 | 检查 `assets/vendor/github/` |

日志位置：

```bash
tail -f modules/telegram/output/logs/bot.log
cat modules/telegram/output/logs/nohup.out
```

---

## 架构变更记录

### 2026-04-14

- 顶层 `docs/` 合并到 `assets/docs/`
- 顶层 `deploy/` 合并到 `assets/deploy/`
- 旧 `libs/` 拆分为：
  - `assets/data/`
  - `assets/database/`
  - `assets/vendor/`
  - `runtime/database/`
- 配置统一收敛到 `assets/config/`
- 路径真相源修正为仓库内自洽，不再指向外部 TradeCat 目录

### 2026-04-20

- 新增顶层 `skills/` 作为 Agent 技能封装层
- 新增 `skills/fatecat/`，用 skill 外壳包装 FateCat 能力
- 新增 `skills/fatecat/scripts/fatecat_runtime/` 作为嵌入式运行时镜像
- skill 包装脚本采用“双运行时”策略：未 bootstrap 镜像前先回退到源仓库，镜像就绪后优先使用嵌入式 runtime
