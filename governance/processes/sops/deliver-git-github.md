---
id: SOP-REL-GIT-GITHUB-DELIVER
type: process
status: current
owner: engineering
route_key: deliver_git_github
route_aliases: ["提交 Git", "推送 GitHub", "检查 Actions"]
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P60D
---

# 提交并推送 GitHub

## 任务定义
在当前分支完成 Git preflight、选择性暂存、验证、语义提交、push 和 GitHub CI/PR 状态确认。

## 当前状态
Git/GitHub 流程成熟；远端操作依赖认证和网络，提交/push 不等于实现正确或生产发布。

## 适用场景
用户明确要求提交、推送、PR、CI 或交付证据；不用于 HF Space 部署。

## 输入要求
交付范围、commit message、是否 push/PR；当前 branch/upstream/remote；真实验证结果。

## 前置条件
运行 `git status --short --branch`；审阅 diff；确认无无关改动、secret、runtime 产物和未完成门禁。

## 默认工具链
auto-github preflight，`git diff`、选择性 `git add`、`git commit`、`git push`、`gh run list` 和 delivery evidence。

## 固定路径
当前 worktree、`.git/`、`.github/workflows/`；交付证据输出 `/tmp/git-delivery-evidence.json`。

## 成熟参数
保持当前分支；单人默认 commit+push；PR 仅在流程要求/用户指定；禁止自动 rebase/reset/amend 已推送历史。

## 分步执行流程
1. 检查 branch/upstream/status/remote/diff。
2. 运行目标质量门禁和 secret/source hygiene。
3. 只暂存本任务文件，复核 cached diff。
4. 创建语义清晰 commit。
5. push 当前分支，查询当前 SHA 对应 CI/PR并生成交付证据。

## 幂等与增量策略
已提交文件不重复 commit；新改动创建新 commit；push 同一 SHA 幂等；不得改写已推送历史。

## 限速与并发规则
同一分支单 operator提交；等待 CI 后再追加修复；不并发 push 相互覆盖。

## 输出目录
Git commit/remote；临时 delivery evidence `/tmp`；必要时纳入任务 closeout。

## 命名规范
commit 使用 `<type>: <中文动作与对象>`；分支沿用当前分支；PR 标题与 commit 主题一致。

## 质量验收门禁
cached diff准确、门禁真实通过、commit存在、远端 SHA一致、CI链接/状态可证、docs sync已记录。

## 失败处理
认证、non-fast-forward、CI或 Git dirty 异常时停止并分析，不 force push或吞失败。

## 恢复与重试策略
网络/认证修复后重推同一 commit；CI失败新 commit修复；冲突需人工明确策略。

## 安全边界
不提交 secret、env、用户数据、raw和 ignored runtime；远端删除/force push需单独明确授权。

## 临时文件清理
删除临时 PR body/delivery evidence副本；保留任务需要的 closeout证据。

## 运行记录登记
记录 branch、commit SHA/message、push remote、PR/CI URL/status、验证和 docs sync。

## 明确禁止事项
- 禁止 `git add .` 盲目纳入无关文件。
- 禁止破坏性 reset/checkout/force push。
- 禁止把 push 或绿 CI 等同生产部署完成。
