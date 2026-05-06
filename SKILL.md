---
name: fatecat
description: "FateCat 执行型命理排盘 skill：安装并校验当前仓库，执行纯分析排盘，输出 JSON / Markdown，启动 Web / API / Telegram 交付层，并在发布前运行仓库卫生与生产就绪门禁。Use when 用户要求排盘、生成报告、启动 Web/API/Bot、验收 skill、导出 bundle、检查生产可用性。"
---

# fatecat Skill

把 FateCat 从“仓库已存在”推进到“依赖就绪、健康通过、能真实执行排盘并交付结果”。本 skill 只编排当前仓库能力，不重写命理算法，不用文档替代真实命令证据。

## When to Use This Skill

Trigger when any of these applies:
- 用户要生成八字 / 紫微等命理排盘结果，且结果需要落到 JSON 或 Markdown 文件。
- 用户要打开 Web HTML 页面录入出生日期、时间、地区、姓名并复制 Markdown。
- 用户要启动或验收 FastAPI、Telegram Bot、CLI 或 Agent 交付入口。
- 用户要首次安装仓库、修复虚拟环境、检查 `pure` / `delivery` 健康状态。
- 用户要发布、导出、审计、检查仓库卫生、检查隐私样例或验证 skill bundle。
- 用户要求“能不能生产复用”“上线前检查”“完整验收”“live Bot smoke”。

## Not For / Boundaries

- 不在 `scripts/project/assets/vendor/` 内魔改第三方算法源码；vendor 默认只读，除非任务明确是供应链治理。
- 不在根目录创建第二套业务源码；真实源码根固定为 `scripts/project/`。
- 不把缺少真实 token、真实 API URL、生产 CORS、远程服务器权限的 dry-run 说成生产 live 验证。
- 不在缺少 `birthDateTime`、`gender`、`longitude`、`latitude` 时直接执行纯分析。
- 不把未来功能塞回默认综合八字报告；黄历、六爻、梅花、奇门、大六壬、风水、姓名合婚等必须走独立体系契约。
- 不向用户前端展示除北京以外的真实地区样例；第一方示例统一使用北京 / 测试用户口径。

## Quick Reference

### 1. 确认仓库位置

```bash
test -f SKILL.md && test -d scripts/project && test -d references
```

### 2. 首次安装运行时

```bash
bash scripts/bootstrap.sh --with-dev
```

### 3. 标准纯分析预检

```bash
bash scripts/preflight.sh --mode pure --bootstrap --pretty
```

### 4. 预检并生成样例输出

```bash
bash scripts/preflight.sh --mode pure --bootstrap --smoke --output-file output/preflight-sample.json --pretty
```

### 5. 用输入文件生成 JSON

```bash
mkdir -p output
bash scripts/pure-analysis.sh --input-file input.json --output-file output/result.json --pretty
```

### 6. 用 JSON 字符串生成 JSON

```bash
mkdir -p output
bash scripts/pure-analysis.sh \
  --input-json '{"birthDateTime":"1990-01-01 08:00:00","gender":"男","longitude":116.4074,"latitude":39.9042,"birthPlace":"北京市","name":"测试用户"}' \
  --output-file output/result.json \
  --pretty
```

### 7. 启动 Web / API 前验收

```bash
bash scripts/preflight.sh --mode delivery --bootstrap --pretty
bash scripts/delivery-smoke.sh --target api
bash scripts/serve-api.sh
```

Web 地址：

```text
http://127.0.0.1:8001/web
```

### 8. 启动 Telegram Bot 前验收

```bash
bash scripts/preflight.sh --mode delivery --bootstrap --pretty
bash scripts/delivery-smoke.sh --target bot --startup-timeout 8
bash scripts/serve-bot.sh
```

### 9. 发布前完整验收

```bash
bash scripts/acceptance.sh --with-dev
```

### 10. 清理本地运行态

```bash
bash scripts/clean-runtime.sh
```

彻底重建虚拟环境时才加：

```bash
bash scripts/clean-runtime.sh --venv
```

### 11. 导出 lite skill 包并检查卫生

```bash
rm -rf /tmp/fatecat-export
bash scripts/export-runtime.sh --output-parent /tmp/fatecat-export --mode lite
bash scripts/check-export-hygiene.sh /tmp/fatecat-export/fatecat
```

### 12. 生产就绪门禁

```bash
bash scripts/production-readiness.sh --api-url https://your-domain.example --require-live-bot
```

没有真实生产 URL、CORS allowlist、API token 和 Telegram token 时，只能记录为“外部连通验证待执行”。

### 13. 校验当前 skill

```bash
/home/lenovo/.codex/skills/auto-skill/scripts/validate-skill.sh /home/lenovo/.projects/fatecat --strict
```

## Execution Logic

1. 先定位目标：纯分析输出文件走 `pure`；Web / API / Bot 走 `delivery`；发布交付走 `acceptance`；公网生产走 `production-readiness`。
2. 再补运行时：优先 `bash scripts/preflight.sh --mode <pure|delivery> --bootstrap --pretty`，不要手工拼散命令。
3. 再验输入：排盘必须有出生时间、性别、经纬度；前端示例必须使用北京 / 测试用户。
4. 再执行目标命令：生成文件、启动服务、导出 bundle 或跑门禁。
5. 最后复核证据：退出码、输出文件、健康检查、smoke 日志、导出包卫生、Git 状态。

## Examples

### Example 1: 首次接手仓库

- Input: 用户说“先检查这个 skill 能不能跑”。
- Steps:
  1. `bash scripts/preflight.sh --mode pure --bootstrap --pretty`
  2. `scripts/project/.venv/bin/fatecat --help`
  3. 必要时执行 `bash scripts/acceptance.sh --with-dev`
- Expected output / acceptance:
  - 虚拟环境创建成功。
  - CLI 可执行。
  - `pure` 健康检查通过。

### Example 2: 生成排盘 JSON

- Input: 用户给出出生时间、性别、经纬度、姓名，要求保存结果。
- Steps:
  1. 检查字段包含 `birthDateTime`、`gender`、`longitude`、`latitude`。
  2. `bash scripts/preflight.sh --mode pure --bootstrap --pretty`
  3. `bash scripts/pure-analysis.sh --input-file input.json --output-file output/result.json --pretty`
- Expected output / acceptance:
  - 命令退出码为 0。
  - `output/result.json` 存在且可解析。
  - 输出不是空文件、报错栈或模型臆造文本。

### Example 3: 启动 Web HTML 页面

- Input: 用户要浏览器输入出生日期、出生时间、出生地区、姓名，并复制 Markdown。
- Steps:
  1. `bash scripts/preflight.sh --mode delivery --bootstrap --pretty`
  2. `bash scripts/delivery-smoke.sh --target api`
  3. `bash scripts/serve-api.sh`
- Expected output / acceptance:
  - API smoke 通过。
  - `/web` 可访问。
  - 页面输出 Markdown，可复制。

### Example 4: 发布前完整门禁

- Input: 用户说“提交前检查到能交付”。
- Steps:
  1. `bash scripts/clean-runtime.sh`
  2. `bash scripts/acceptance.sh --with-dev`
  3. `git status --short --branch`
- Expected output / acceptance:
  - acceptance 全部通过。
  - 未跟踪非忽略文件为 0。
  - 没有运行态、缓存、真实 `.env` 或数据库文件混入版本控制。

## References

- `references/index.md`: 文档导航。
- `references/execution-playbook.md`: 标准执行顺序、模式判断和失败处理。
- `references/commands.md`: 命令入口与使用场景。
- `references/io-contract.md`: 输入输出契约。
- `references/architecture.md`: 根 skill、包装脚本与 `scripts/project/` 的职责边界。
- `references/ops-pack.md`: 运维包、delivery smoke 与生产边界。
- `references/live-bot-verification.md`: 真实 Telegram token 验证。
- `references/stage-gates.md`: 从可运行到可生产的阶段门禁。
- `references/troubleshooting.md`: 常见失败与修复路径。
- `references/migration-plan.md`: 当前目录迁移与根卫生口径。

## Maintenance

- Sources:
  - `scripts/bootstrap.sh`
  - `scripts/preflight.sh`
  - `scripts/health.sh`
  - `scripts/pure-analysis.sh`
  - `scripts/delivery-smoke.sh`
  - `scripts/export-runtime.sh`
  - `scripts/acceptance.sh`
  - `scripts/project/modules/fate_core/src/fate_core/cli.py`
  - `scripts/project/modules/telegram/src/web_ui.py`
  - `scripts/project/modules/telegram/src/main.py`
- Quality gate:
  - `/home/lenovo/.codex/skills/auto-skill/scripts/validate-skill.sh /home/lenovo/.projects/fatecat --strict`
  - `bash scripts/preflight.sh --mode pure --bootstrap --pretty`
  - `bash scripts/acceptance.sh --with-dev`
- Last updated: 2026-05-07
- Known limits:
  - `delivery-smoke` 的 Bot 检查默认是 dry-run，不等于 Telegram live。
  - 生产 live 验证必须依赖真实外部 URL、token、CORS 与网络权限。
  - vendor 体积偏大是完整复用外部源码快照的取舍，不能无门禁删除。
