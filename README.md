# FateCat

<p align="center">
  <img src="./project/assets/docs/fatecat-readme-banner.svg" alt="FateCat Banner" width="100%">
</p>

**FateCat 现已整理为标准单-skill 仓库：根目录负责 skill 包装、生命周期治理与交付脚本，真实业务源码位于 `project/`。**

它的目标没有变：把专业命理排盘结果收敛成 AI / Agent 可稳定消费的结构化输入，再交给 CLI、FastAPI、Telegram Bot 或上层自动化系统继续使用。

## 仓库现在是什么

当前根仓库承担 4 个职责：

- 单-skill 仓库入口：`SKILL.md` 定义 agent 如何接手、安装、检查、执行
- 生命周期治理层：`assets/lifecycle/`、`references/`、根脚本负责需求到运维的标准化闭环
- 统一执行包装层：根 `scripts/` 把源码仓库常用动作封成稳定入口
- 可导出 bundle 源：可把当前 skill 连同最小运行时导出为独立交付包

真实业务源码与运行时真相源在：

- `project/modules/fate_core/`：纯命理分析内核
- `project/modules/telegram/`：Telegram / FastAPI / 报告交付层
- `project/assets/`：配置、schema、字段 profile、外部成熟算法与数据资产
- `project/runtime/`：数据库与运行态产物

## FateCat 解决什么问题

FateCat 不是让 AI 直接“脑补排盘”，而是把“排盘”和“解释”拆开：

1. 专业排盘系统或成熟算法负责结构化计算
2. FateCat 负责统一字段、统一输出、统一交付入口
3. AI / Agent 只基于稳定 JSON 做解释、总结与后续任务

这样做主要是为了解决三类老问题：

- 直接让 AI 排盘：容易胡编乱造、字段漂移、前后不一致
- 外部命理仓库分散：调用方式不同、依赖不同、输出结构不同
- 交付入口多：CLI、Bot、API、Agent 往往各写一套，最后越维护越散

推荐链路：

```text
TradeCat / 专业排盘
        ↓
FateCat pure-analysis 输出稳定 JSON
        ↓
AI / Agent 基于结构化字段做分析
        ↓
Telegram / API / 自动化系统继续交付
```

## 快速开始

### 1. 首次准备运行时

```bash
bash scripts/bootstrap.sh --with-dev
```

如果只需要最小运行时，不装开发依赖：

```bash
bash scripts/bootstrap.sh
```

### 2. 先做标准预检

纯分析链路：

```bash
bash scripts/preflight.sh --mode pure --bootstrap --pretty
```

交付链路：

```bash
bash scripts/preflight.sh --mode delivery --bootstrap --pretty
```

### 3. 执行一次命理排盘并输出文件

```bash
mkdir -p output
bash scripts/pure-analysis.sh \
  --input-json '{"birthDateTime":"1990-01-01 08:00:00","gender":"男","longitude":116.4074,"latitude":39.9042,"birthPlace":"北京市","name":"测试样本"}' \
  --output-file output/bazi-result.json \
  --pretty
```

### 4. 做完整验收

```bash
bash scripts/acceptance.sh --with-dev
```

完整验收会覆盖 shell 语法、strict skill 校验、纯分析 smoke、全量 pytest、ruff、format、`fate_core` mypy、API 与 Bot dry-run 交付层 smoke，以及导出后的 lite skill 包独立 smoke。

### 5. 做交付层烟雾验证

验证 API：

```bash
bash scripts/delivery-smoke.sh --target api
```

验证 Bot 启动链路：

```bash
bash scripts/delivery-smoke.sh --target bot --startup-timeout 8
```

说明：

- 如果仓库里没有真实 `project/assets/config/.env`，`delivery-smoke.sh` 会自动生成临时 smoke 配置并在退出后删除
- Bot smoke 默认走 dry-run，只验证配置加载、handler 装配、入口链路与依赖健康，不会真的连接 Telegram

## 常用命令

```bash
bash scripts/bootstrap.sh --with-dev
bash scripts/preflight.sh --mode pure --bootstrap --pretty
bash scripts/preflight.sh --mode pure --bootstrap --smoke --output-file output/preflight-sample.json --pretty
bash scripts/preflight.sh --mode delivery --bootstrap --pretty
bash scripts/pure-analysis.sh --input-file input.json --output-file output/result.json --pretty
bash scripts/acceptance.sh --with-dev
bash scripts/delivery-smoke.sh --target api
bash scripts/delivery-smoke.sh --target bot --startup-timeout 8
bash scripts/clean-runtime.sh --dry-run
bash scripts/collect-ops-bundle.sh --output /tmp/fatecat-ops-bundle
bash scripts/export-runtime.sh --output-parent /tmp/fatecat-export --mode lite
```

## 输入输出心智模型

执行 `pure-analysis` 时，最少要给这几项：

- `birthDateTime`
- `gender`
- `longitude`
- `latitude`

`gender` 接受 `male` / `female` / `男` / `女`，内部统一归一为 `male` / `female`，输出展示层会翻译回中文。

输出结果是稳定 JSON，顶层会保留这类字段：

- `success`
- `profile`
- `data`
- `disclaimer`
- `branding`

如果你要把结果继续喂给 AI，优先让 AI 只依赖结构化字段，而不是让它自己重新算盘。稳定字段契约与更完整示例见 [references/io-contract.md](references/io-contract.md)。

## 单-skill 仓库结构

```text
fatecat/
├── AGENTS.md                  # 仓库架构与协作约束
├── SKILL.md                   # skill 入口定义
├── README.md                  # 根仓库导航与快速使用说明
├── assets/
│   └── lifecycle/             # 生命周期模板与治理资产
├── references/                # skill 参考文档
├── scripts/                   # 根级包装脚本、预检、验收、导出、运维
└── project/                   # 真实业务源码与运行时真相源
    ├── assets/
    ├── modules/
    ├── runtime/
    ├── tests/
    └── README.md
```

根目录与 `project/` 的边界要保持清楚：

- 根目录不再放第二套业务源码
- 要改业务逻辑，进入 `project/`
- 要改 skill 运行手册、验收链路、导出流程、生命周期包装，改根目录

## 关键路径与配置约束

统一配置位置：

```text
project/assets/config/.env
project/assets/config/.env.example
```

几个硬约束：

- 不要在根目录再创建 `.env`
- 不要把业务源码塞回根 `scripts/` 或 `references/`
- 不要修改 `project/assets/vendor/` 下的外部成熟算法源码
- 运行态数据留在 `project/runtime/`，不要回灌到静态资产目录

如果只跑纯分析，通常不强制要求 Telegram token；如果要启动真实 Bot，则需要填写 `project/assets/config/.env` 中的交付配置。

## 推荐阅读顺序

- [SKILL.md](SKILL.md)：agent 如何接手、预检、执行、验收
- [references/index.md](references/index.md)：参考文档导航
- [references/execution-playbook.md](references/execution-playbook.md)：标准执行链路
- [references/commands.md](references/commands.md)：命令速查
- [references/ops-pack.md](references/ops-pack.md)：运维与加固
- [project/README.md](project/README.md)：原项目级产品说明与更细的业务背景

## 什么时候改哪里

- 改命理分析能力：`project/modules/fate_core/`
- 改 Bot / API / 报告交付：`project/modules/telegram/`
- 改字段 profile / schema / 数据资产：`project/assets/`
- 改 skill 入口、预检、验收、导出、生命周期包装：根 `scripts/`、`references/`、`SKILL.md`

## 生产前最低门槛

如果目标是“这个 skill 可以被 agent 稳定执行”，最低要满足：

1. `bash scripts/bootstrap.sh` 能成功
2. `bash scripts/preflight.sh --mode pure --bootstrap --pretty` 能通过
3. 至少产出过一份真实 JSON 结果文件
4. 若涉及交付层，`bash scripts/delivery-smoke.sh --target api` 与 `--target bot --startup-timeout 8` 都应通过；只上线单一入口时才只验目标入口
5. 发布前跑一次 `bash scripts/acceptance.sh --with-dev`，确认源码仓库 API/Bot 入口与导出后的 lite skill 包都能通过 smoke

## 免责声明

本项目及 AI 分析结果仅供传统文化研究、算法测试与娱乐参考。命理学非精密科学，命运掌握在自己手中。使用者因轻信或误读本程序结果而产生的任何心理、财务及生活决策后果，本开源项目及开发者概不负责。
