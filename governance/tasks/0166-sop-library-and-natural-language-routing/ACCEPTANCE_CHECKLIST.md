# Acceptance Checklist

# Global Standards
- [x] 一任务一 Markdown，未建立第二套运行时或命令 wrapper。
- [x] 所有状态和成熟度来自 tracked contract。
- [x] 外部副作用、隐私、密钥和删除操作均 fail closed。

# Task Package Checklists

## TP-01
- [x] 任务分类、状态来源和路由契约已锁定。
- Verify: registry、scripts 和历史任务盘点。
- Gate: 一个任务意图只对应一个 route key。

## TP-02
- [x] capability 独立 SOP 已落盘。
- Verify: capability 状态对照测试。
- Gate: planned capability fail closed。

## TP-03
- [x] 数据、评测与开发质量 SOP 已落盘。
- Verify: 成熟命令和固定路径存在性测试。
- Gate: 不新增第二套工具链。

## TP-04
- [x] 分发、生产、发布与审计 SOP 已落盘。
- Verify: 外部依赖和副作用边界审查。
- Gate: 不伪造 live、CI 或生产证据。

## TP-05
- [x] 机械校验、治理同步与审查完成。
- Verify: focused、task、governance、Quick CI 和 diff review。
- Gate: 本任务新增内容无 BLOCK。

## Structure
- [x] `governance/processes/sops/INDEX.md` 存在并覆盖全部 SOP。
- [x] 每份 SOP 对应一个任务目标。
- [x] 目录 AGENTS 与治理根索引已同步。

## Contract
- [x] 20 个必备章节全部存在。
- [x] route key 与 alias 全局唯一。
- [x] capability status 与 registry 一致。
- [x] 所有脚本和固定路径可解析。

## Safety
- [x] 外部连通项明确写为待外部执行。
- [x] 未投产能力 fail closed。
- [x] 密钥、隐私、版权和删除边界明确。

## Verification
- [x] focused SOP regression 通过。
- [x] governance strict/health 通过。
- [x] 当前 0166 task package strict 通过。
- [x] 全历史任务树已审计；163/165 合格，0090/0091 为既有旧模板遗留。
- [x] Quick CI 通过。
