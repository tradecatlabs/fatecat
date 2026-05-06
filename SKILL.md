---
name: fatecat
description: "FateCat 执行型命理排盘 skill：基于当前仓库完成依赖安装、健康检查、纯分析执行、JSON 文件输出，以及 API/Bot 交付前检查。Use when 你要让 agent 调用这个仓库生成命理排盘结果文件，或在上线前完成首次安装、配置检查、生产可用性校验。"
---

# fatecat Skill

这个 skill 的职责不是在文档层重写命理算法，而是指导 agent 直接调用当前仓库，把 FateCat 从“未安装 / 未配置 / 未校验”推进到“依赖就绪 / 健康通过 / 可以执行命理排盘并输出文件”的可运行状态。

## When to Use This Skill

Trigger when any of these applies:
- 你要让 agent 基于当前仓库执行一次命理排盘，并把结果写入 JSON 文件
- 你要在首次接手仓库时完成依赖安装、虚拟环境准备、CLI 入口修复
- 你要在正式执行任务前检查 `pure` 或 `delivery` 模式是否健康
- 你要在生产前确认配置、依赖、入口命令、输出文件链路全部打通
- 你要启动 FateCat 的 API 或 Bot 交付层，但必须先走前置检查
- 你要给后续 agent 留下一套“先检查、再执行、最后验收”的标准运行手册

## Not For / Boundaries

- 这个 skill 不重写 `scripts/project/assets/vendor/` 下的外部算法仓库，也不允许用文档替代真实执行结果。
- 当前 FateCat 源码真相源在 `scripts/project/`；根目录的 `scripts/` 只是包装入口，不能在根目录再发明第二套运行时。
- 纯命理排盘最少需要：`birthDateTime`、`gender`、`longitude`、`latitude`；缺一项都不应冒然执行。
- `delivery` 模式依赖 `scripts/project/assets/config/.env` 等真实配置；没有配置时只能停在检查阶段，不能假装“可生产”。
- 真正的生产可用，必须以健康检查、一次真实输出、必要时 API/Bot 启动验证为准；不能只看文档或只跑 `--help`。

## Quick Reference

### 0. 仓库定位

```bash
pwd
```

期望当前目录是 skill 根目录，且存在 `scripts/project/`、`scripts/`、`SKILL.md`。

### 1. 首次安装运行时

```bash
bash scripts/bootstrap.sh
```

如果要连开发依赖一起装：

```bash
bash scripts/bootstrap.sh --with-dev
```

### 2. 检查 CLI 是否可用

```bash
scripts/project/.venv/bin/fatecat --help
```

### 3. 检查纯分析健康状态

```bash
bash scripts/health.sh --mode pure --json --pretty
```

### 3.5 一键执行标准预检

```bash
bash scripts/preflight.sh --mode pure --bootstrap --smoke --pretty
```

如果要检查交付层但暂不执行排盘：

```bash
bash scripts/preflight.sh --mode delivery --bootstrap --pretty
```

### 4. 检查交付层健康状态

```bash
bash scripts/health.sh --mode delivery --json --pretty
```

### 4.5 执行完整 skill 验收

```bash
bash scripts/acceptance.sh --with-dev
```

完整验收会覆盖 shell 语法、strict skill 校验、纯分析 smoke、vendor health、源仓卫生门禁、隐私示例门禁、全量 pytest、ruff、format、`fate_core` mypy、API 与 Bot dry-run 交付层 smoke、导出包卫生检查，以及导出后的 lite skill 包独立 smoke。

### 5. 用 JSON 字符串直接执行排盘

```bash
mkdir -p output
bash scripts/pure-analysis.sh \
  --input-json '{"birthDateTime":"1990-01-01 08:00:00","gender":"男","longitude":116.4074,"latitude":39.9042,"birthPlace":"北京市","name":"测试样本"}' \
  --output-file output/bazi-result.json \
  --pretty
```

### 6. 用输入文件执行排盘

```bash
mkdir -p output
bash scripts/pure-analysis.sh \
  --input-file input.json \
  --output-file output/bazi-result.json \
  --pretty
```

### 7. 启动 API 前先做 delivery 检查

```bash
bash scripts/preflight.sh --mode delivery --bootstrap --pretty
bash scripts/delivery-smoke.sh --target api
bash scripts/serve-api.sh
```

API 启动后可打开原生 HTML Web 报告页：

```text
http://127.0.0.1:8001/web
```

如果当前仓库里还没有真实 `scripts/project/assets/config/.env`，`delivery-smoke.sh` 会自动注入一份临时 smoke 配置，脚本退出后自动删除。

### 8. 启动 Bot 前先做 delivery 检查

```bash
bash scripts/preflight.sh --mode delivery --bootstrap --pretty
bash scripts/delivery-smoke.sh --target bot --startup-timeout 8
bash scripts/serve-bot.sh
```

说明：Bot smoke 默认走 dry-run 装配验证，证明 import、配置加载、handler 挂载和 CLI 启动链路全部可用，但不会真的连接 Telegram。

## Execution Logic

### Phase 1. 首次接手 / 依赖准备

必须先做：
1. 确认当前目录是 skill 根目录，且 `scripts/project/pyproject.toml` 存在。
2. 执行 `bash scripts/bootstrap.sh`。
3. 执行 `scripts/project/.venv/bin/fatecat --help`，确认 CLI 入口健康。
4. 若仓库刚迁移过路径或执行器报错，再执行 `bash scripts/acceptance.sh --with-dev` 做一次全链路验收。

更推荐直接执行：

```bash
bash scripts/preflight.sh --mode pure --bootstrap --pretty
```

完成定义：
- `scripts/project/.venv/bin/fatecat` 可执行
- `fatecat` 至少暴露 `pure-analysis`、`health`、`serve`

### Phase 2. 配置与前置检查

执行前必须判断目标模式：
- 只做排盘文件输出：走 `pure` 模式检查
- 要启动 API/Bot：走 `delivery` 模式检查

纯分析检查：

```bash
bash scripts/health.sh --mode pure --json --pretty
```

交付层检查：

```bash
bash scripts/health.sh --mode delivery --json --pretty
```

完成定义：
- 输出中没有阻断性错误
- 需要 `delivery` 时，配置文件和交付层依赖已就绪
- 推荐优先使用统一入口：`bash scripts/preflight.sh --mode <pure|delivery> --bootstrap --pretty`

### Phase 3. 输入验收

在真正执行命理排盘前，agent 必须确认：
- 出生时间格式可解析
- 性别值符合 FateCat CLI 接受范围：`male` / `female` / `男` / `女`
- 经度、纬度存在且是数字
- 若要写文件，目标目录存在或可创建

如果用户只给自然语言描述，没有给坐标，这个 skill 应先停在“收集输入”或“查地理坐标”阶段，不应直接执行。

### Phase 4. 执行命理排盘并输出文件

标准执行路径：

```bash
mkdir -p output
bash scripts/pure-analysis.sh \
  --input-json '{"birthDateTime":"1990-01-01 08:00:00","gender":"男","longitude":116.4074,"latitude":39.9042,"birthPlace":"北京市","name":"测试样本"}' \
  --output-file output/bazi-result.json \
  --pretty
```

如果需要把“预检 + 样例输出”一步完成，优先用：

```bash
bash scripts/preflight.sh \
  --mode pure \
  --bootstrap \
  --smoke \
  --output-file output/preflight-sample.json \
  --pretty
```

完成定义：
- 命令退出码为 0
- 输出文件存在
- 输出 JSON 可读取
- 顶层至少能看到 `success`、`data`、`profile` 等结果字段

### Phase 5. 生产前确认

若目标是“确保可以生产后开始任务”，最少还要补这三步：
1. 再跑一次目标模式的 `health`
2. 保留一份真实输出文件作为验收样本
3. 跑完整 `acceptance.sh --with-dev`，同时验证源码仓库 API/Bot 入口和导出包
4. 如果走交付层，再启动一次目标 API 或 Bot 验证真实入口链路

推荐验收顺序：
1. `bash scripts/bootstrap.sh`
2. `bash scripts/preflight.sh --mode pure --bootstrap --smoke --output-file output/preflight-sample.json --pretty`
3. `bash scripts/pure-analysis.sh ... --output-file ...`
4. 若要上线交付层：`bash scripts/preflight.sh --mode delivery --bootstrap --pretty`
5. `bash scripts/delivery-smoke.sh --target api`
6. `bash scripts/delivery-smoke.sh --target bot --startup-timeout 8`
7. `bash scripts/serve-api.sh` 或 `bash scripts/serve-bot.sh`

## Common Patterns

### Pattern 1. 首次初始化并验证 CLI

```bash
bash scripts/bootstrap.sh && scripts/project/.venv/bin/fatecat --help
```

### Pattern 2. 纯分析生产前检查

```bash
bash scripts/preflight.sh --mode pure --bootstrap --pretty
```

### Pattern 3. 交付层生产前检查

```bash
bash scripts/preflight.sh --mode delivery --bootstrap --pretty
```

### Pattern 3.5. 交付层烟雾验证

```bash
bash scripts/delivery-smoke.sh --target api
bash scripts/delivery-smoke.sh --target bot --startup-timeout 8
```

### Pattern 4. 直接落文件

```bash
mkdir -p output && bash scripts/pure-analysis.sh --input-file input.json --output-file output/result.json --pretty
```

### Pattern 5. 一步完成预检和烟雾输出

```bash
bash scripts/preflight.sh --mode pure --bootstrap --smoke --output-file output/preflight.json --pretty
```

### Pattern 6. 用命令行参数直接执行

```bash
scripts/project/.venv/bin/fatecat pure-analysis \
  --birth-datetime '1990-01-01 08:00:00' \
  --gender 男 \
  --longitude 116.4074 \
  --latitude 39.9042 \
  --birth-place 北京市 \
  --output-file output/result.json \
  --pretty
```

## Examples

### Example 1: 首次接手仓库并确认可执行

- Input: 一个刚拉下来的 FateCat skill 仓库，需要先确认能不能跑
- Steps:
  1. 执行 `bash scripts/preflight.sh --mode pure --bootstrap --pretty`
  2. 若仓库刚迁移过目录，再执行 `bash scripts/acceptance.sh --with-dev`
  3. 必要时再执行 `scripts/project/.venv/bin/fatecat --help`
- Expected output / acceptance:
  - 虚拟环境成功创建
  - CLI 帮助正常显示
  - `pure` 健康检查通过，没有阻断性错误

### Example 2: 生成一份命理排盘 JSON 文件

- Input: 用户给出出生时间、性别、经纬度，要求保存结果文件
- Steps:
  1. 先执行 `bash scripts/preflight.sh --mode pure --bootstrap --pretty`
  2. 创建输出目录：`mkdir -p output`
  3. 执行：
     `bash scripts/pure-analysis.sh --input-json '{"birthDateTime":"1990-01-01 08:00:00","gender":"男","longitude":116.4074,"latitude":39.9042,"birthPlace":"北京市"}' --output-file output/bazi-result.json --pretty`
- Expected output / acceptance:
  - 命令成功结束
  - `output/bazi-result.json` 存在
  - 文件中有结构化命理结果，而不是空文件或报错栈

### Example 3: 上线前验证 API 交付层

- Input: 已经能做纯分析，现在要确认 API 入口达到可生产前状态
- Steps:
  1. 确认 `scripts/project/assets/config/.env` 等交付层配置已准备
  2. 执行 `bash scripts/preflight.sh --mode delivery --bootstrap --pretty`
  3. 执行 `bash scripts/serve-api.sh`
- Expected output / acceptance:
  - `delivery` 健康检查通过
  - API 进程成功启动
  - 不再出现缺配置、缺入口、缺依赖这类启动即失败问题

### Example 4: agent 的标准执行顺序

- Input: 用户说“开始做排盘，先确保环境没问题”
- Steps:
  1. `bash scripts/preflight.sh --mode pure --bootstrap --pretty`
  2. 检查输入字段是否完整
  3. `bash scripts/pure-analysis.sh ... --output-file ... --pretty`
  4. 读取输出文件并向用户汇报
- Expected output / acceptance:
  - agent 不会跳过安装与检查直接开跑
  - 每次真实执行前，都有前置健康证据
  - 结果文件与口头汇报一致

## References

- `references/index.md`: 总导航
- `references/execution-playbook.md`: 标准执行链路与决策顺序
- `references/commands.md`: 仓库脚本与命令入口
- `references/io-contract.md`: 输入输出契约
- `references/troubleshooting.md`: 常见失败模式与修复方向
- `references/ops-pack.md`: 运维包与健康检查边界
- `references/stage-gates.md`: 从“能跑”到“可生产”的阶段门禁

## Maintenance

- Sources:
  - `scripts/bootstrap.sh`
  - `scripts/preflight.sh`
  - `scripts/health.sh`
  - `scripts/pure-analysis.sh`
  - `scripts/serve-api.sh`
  - `scripts/serve-bot.sh`
  - `scripts/common.sh`
  - `scripts/project/modules/fate_core/src/fate_core/cli.py`
  - `scripts/project/modules/telegram/src/main.py`
- Verification path:
  - `bash scripts/bootstrap.sh`
  - `bash scripts/preflight.sh --mode pure --bootstrap --pretty`
  - `scripts/project/.venv/bin/fatecat --help`
  - `scripts/project/.venv/bin/fatecat pure-analysis --help`
  - `scripts/project/.venv/bin/fatecat health --help`
  - `bash scripts/health.sh --mode pure --json --pretty`
  - `bash scripts/pure-analysis.sh --input-json '{"birthDateTime":"1990-01-01 08:00:00","gender":"男","longitude":116.4074,"latitude":39.9042}' --output-file /tmp/fatecat-sample.json --pretty`
- Last updated: 2026-04-20
- Known limits:
  - 纯分析可以在无交付层配置时运行，但 `delivery` 模式不行
  - 生产可用性最终取决于真实配置、真实依赖和一次真实执行结果
  - 本 skill 只规定仓库内的标准运行路径，不替代外部部署系统的职责
