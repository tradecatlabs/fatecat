---
id: SOP-DIST-PACKAGE-VERIFY
type: process
status: current
owner: developer-platform
route_key: verify_distribution_package
route_aliases: ["检查分发包", "运行 package smoke", "验证独立安装包"]
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P60D
---

# 验证独立分发包

## 任务定义
构建 sdist/wheel，从 sdist 重建 wheel，在 clean venv 安装并验证协议级 CLI 能力。

## 当前状态
package distribution smoke 已成熟；wheel 只承载协议/CLI，不宣称捆绑 provider assets。

## 适用场景
pyproject、package data、CLI、依赖或公开分发边界变更后。

## 输入要求
可选第一个位置参数作为输出根；可选 wheel/sdist 大小预算环境变量。

## 前置条件
开发 venv 包含 `build`；源码卫生通过；输出根可被脚本安全删除。

## 默认工具链
`bash scripts/package-distribution-smoke.sh /tmp/fatecat-package-distribution-smoke`。

## 固定路径
`pyproject.toml`、package source、`scripts/package-distribution-smoke.sh`、contracts。

## 成熟参数
wheel 最大 1 MiB，sdist 最大 2 MiB；输出参数是位置参数，不支持 `--help` 或命名 flag。

## 分步执行流程
1. 确认输出路径是专用临时目录。
2. 构建 sdist/wheel。
3. 从 sdist clean rebuild wheel。
4. 新建 clean venv，`--no-deps` 安装。
5. 运行 `fatecat capabilities --pretty` 并验证 distribution metadata。

## 幂等与增量策略
每次脚本先删除输出根后全量构建；不得增量复用旧 dist/venv。

## 限速与并发规则
同一输出根单进程；多个 package smoke 使用不同目录；不并发写 dist。

## 输出目录
默认 `/tmp/fatecat-package-distribution-smoke`。

## 命名规范
artifact 名由 Python packaging version 决定；证据目录带 commit/UTC。

## 质量验收门禁
sdist/wheel 完整、预算内、sdist 可重建、clean venv 安装、CLI 成功、bazi/ziwei 可发现、providerAssetsAvailable=false。

## 失败处理
构建、预算、重建、安装或 CLI 任一失败即 block；不得手工替换 dist。

## 恢复与重试策略
修复 package config/data 后从空目录重跑；网络依赖问题与包错误分开记录。

## 安全边界
artifact 不包含 provider 私有资产、raw、secret、数据库、日志或用户数据。

## 临时文件清理
删除 output venv、解压源和失败 dist；审计所需 artifact 复制到受控 release 目录。

## 运行记录登记
记录 commit、package version、artifact hash/size、clean install 和 CLI smoke。

## 明确禁止事项
- 禁止把位置参数误写成 `--output`。
- 禁止绕过大小预算。
- 禁止把协议 wheel 宣称为完整算法包。
