---
id: CTX-SCRIPTS
type: module-context
status: current
owner: developer-platform
created: 2026-07-13
last_reviewed: 2026-07-13
code_path: scripts
---

# Scripts Context

## 模块职责

- 提供可重复的 bootstrap、测试、构建、导出、部署、审计和发布门禁入口。
- 脚本只编排 domains、contracts、infra 和平台工具，不复制业务计算逻辑。
- 所有输出必须写入显式运行目录或 `/tmp`，并携带当前 commit 与真实状态。

## 关键入口

- `scripts/local-ci.sh --profile quick`：PR/main push 的自动快速门禁真相源。
- `scripts/acceptance.sh --with-dev`：完整本地验收。
- `scripts/package-distribution-smoke.sh`：仓库外 wheel 安装闭包。
- `scripts/export-runtime.sh` + `check-export-hygiene.sh`：Skill 导出与卫生预算。
- `scripts/current-release-proof.sh`：当前提交远端发布证明聚合。

## 禁止事项

- 禁止脚本吞掉失败或把 pending 写成 passed。
- 禁止 denylist 整仓导出绕过体积、文件数和运行态检查。
- 禁止未经对账把上传超时直接判定为远端失败或成功。
