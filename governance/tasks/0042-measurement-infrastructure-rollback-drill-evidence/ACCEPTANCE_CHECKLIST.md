# Acceptance Checklist

# Global Standards
- [x] 文件路径具体，命令可复现。
- [x] 测试结果来自真实执行输出。
- [x] 不输出 token、secret、password、DSN 或私钥。
- [x] 文档说明本任务只覆盖 dry-run rollback drill。

# Task Package Checklists
## TP-01.01
- [x] rollback gate 和相关脚本/文档已盘点。
- Verify: `rg -n "rollback/回滚"`。
- Gate: 缺口来自真实文件。

## TP-02.01
- [x] rollback drill evidence 生成器完成。
- Verify: `bash scripts/rollback-drill.sh --output-json <path>`。
- Gate: JSON 字段完整。

## TP-03.01
- [x] live gate 校验 rollback JSON 内容。
- Verify: pytest pass/fail。
- Gate: 空 JSON/错误 mode/productionRollbackExecuted=true 不通过。

## TP-04.01
- [x] public-release 默认路径生成并传递 rollback evidence。
- Verify: public-release final live gate。
- Gate: rollback check 为 pass。

## TP-05.01
- [x] targeted tests、public-release、task tree validation、closeout 全部完成。
- Verify: closeout packet。
- Gate: 任务树有效。
