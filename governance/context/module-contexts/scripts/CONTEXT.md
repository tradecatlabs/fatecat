---
id: CTX-SCRIPTS
type: module-context
status: current
owner: developer-platform
created: 2026-07-13
last_reviewed: 2026-07-15
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
- `scripts/suanzhun-corpus-crawl.py`：算准网“基础/典籍”研究语料递归抓取、详情分页逐页存证、逻辑文章聚合、增量恢复、资源落盘和独立完整性校验；输出限定在忽略的本地 export，验证入口为离线回归与 `--validate-only`。

## 禁止事项

- 禁止脚本吞掉失败或把 pending 写成 passed。
- 禁止 denylist 整仓导出绕过体积、文件数和运行态检查。
- 禁止未经对账把上传超时直接判定为远端失败或成功。
- 禁止把外部抓取语料直接写入 canonical 数据产品、提交 Git 或跳过 robots/版权复核边界。
- 禁止仅以分类器已接受的 frontier 验证抓取完整性；详情分页必须另用原始 href 扫描与 `1..N` 物理页序列交叉闭合。
