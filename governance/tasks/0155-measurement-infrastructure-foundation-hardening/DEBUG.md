# Debug Record

## Bug

- 标题：测算基础设施分发、交付和治理闭环存在多个可复现断点。
- 症状：wheel 不能在仓库外运行；HF 核心 readiness 被 Telegram 渠道故障拖垮；导出包混入运行态；综合八字存在双生产引擎；测试污染 reference repo。
- 首次发现位置 / 时间：2026-07-13 全仓审查。

## Environment

- 仓库 / 模块：FateCat `main`，基线 `acd17d7`。
- 运行环境：Ubuntu / Python 3.12 / HF Space CPU Basic。
- 依赖 / 版本：以 `requirements.lock.txt`、`requirements-runtime.lock.txt` 和 `pyproject.toml` 为准。
- 配置差异：本地未启用真实生产凭证；HF 已启用 Telegram Webhook，但公开状态为 `not_ready`。

## Reproduction

1. 构建 wheel，在仓库外干净虚拟环境安装后执行 `fatecat capabilities --pretty`。
2. 请求 HF `/health` 与 `/ready`，对比核心存活和 Telegram 渠道状态。
3. 执行 lite export 并检查嵌套 exports、媒体、reference assets、文件数和体积。
4. 对同一输入调用 legacy 与 capability 八字路径，比较 normalized payload。
5. 运行会导入 reference repo 的测试，再执行 vendor-health。

## Observations

- O1：wheel CLI 因无法定位企业仓库根目录失败。
- O2：HF `/health=200`，`/ready=503`，Telegram 启动失败按固定 30 秒持续增长。
- O3：导出脚本采用整仓 denylist rsync，未排除 `infra/runtime/local-state/exports/`。
- O4：legacy 与 capability 八字结果字段集合不同。
- O5：测试后 reference repo 内出现 `__pycache__` / `*.pyc`。

## Hypotheses

### H1: （ROOT HYPOTHESIS）运行时边界没有按可独立分发对象定义

- Supports：wheel 查找企业仓库根、skill 整仓复制、delivery 双引擎和渠道健康耦合都依赖开发仓库形状。
- Conflicts：现有本地 quick CI 多次通过，说明源码仓内路径能工作。
- Test：建立 clean-room 分发 smoke、单引擎 parity 和分层 readiness 后检查所有症状是否同时消失。

### H2: 现有门禁执行顺序和检查集合存在灯下黑

- Supports：vendor-health 在测试前通过，测试后出现污染；export hygiene 未检查嵌套 exports 和预算。
- Conflicts：source hygiene、基础 export smoke 本身能够发现其已覆盖的违规项。
- Test：将门禁移动到副作用之后，并加入已确认缺失的规则验证。

### H3: 外部环境单点故障是全部问题的共同根因

- Supports：HF Telegram 确实依赖外部网络和 token。
- Conflicts：wheel、导出、双引擎和 vendor 污染可以在完全离线环境复现。
- Test：禁用所有外部调用后重复本地分发与引擎实验；若仍失败则拒绝该假设。

## Experiments

### E1

- Hypothesis: H1
- Change: 暂不修改代码，使用仓库外 venv 运行构建后的 wheel。
- Expected: 若分发边界错误，CLI 会尝试定位源码仓库并失败。
- Result: CLI 报告无法定位企业仓库根目录。
- Verdict: confirmed
- Revert: 实验只写 `/tmp`，无需回滚。

## Root Cause

- 当前已确认主因是开发仓库边界被复用为运行时边界；其他门禁缺口进一步掩盖了问题。

## Fix

- 以独立分发闭包、单一 capability 引擎、分层渠道健康和副作用后卫生门禁替换错误边界。

## Regression Evidence

- 测试：clean-room、parity、readiness、vendor、全量 pytest 和 quick CI。
- 结果：首轮全量 pytest 为 `638 passed, 1 skipped, 1 failed`，唯一失败为 `REVIEW.md` 缺少既有运维手册引用；修复并定向通过后，最终全量重跑为 `639 passed, 1 skipped`。本地 quick 为 `446 passed`，GitHub run `29205516109` 通过。
- 备注：外部专家/live 证据不由本地实验替代。

### Vendor 字节码污染补充实验

- 现象：`vendor-health.sh` 发现 `bazi-1-master` 与 `lunar-python-master` 下存在 2026-07-13 02:29 生成的 `__pycache__`。
- 根因：新增性能 smoke 可被独立调用，但最初只依赖上层 `local-ci.sh` 设置 `PYTHONDONTWRITEBYTECODE=1`；此前直接运行 smoke 已污染 vendor。文件时间早于本轮全量 pytest，pytest 的进程级禁写配置并非该批文件来源。
- 修复：`core-performance-smoke.sh` 与 `package-distribution-smoke.sh` 自身设置 `PYTHONDONTWRITEBYTECODE=1`，不再依赖调用方隐式环境。
- 回归：清理缓存后直接运行两个脚本，再执行 `vendor-health.sh`；任何 vendor 字节码均视为失败。

## Failed Nodes

- TP-01 至 TP-07 尚未执行完成。

## First Invalid Node

- TP-01：当前 wheel 与 skill 分发闭包无效。

## Upstream Lineage

- `pyproject.toml`、路径发现、导出脚本与运行资源契约。

## Downstream Blast Radius

- CLI/SDK 分发、HF 部署包、公开 API、Bot 渠道、发布证明和第三方审计。

## Lowest Common Refinement Ancestor

- FateCat 可独立分发与交付基础设施边界。

## Repair Boundary

- packaging/export、delivery orchestration、Telegram lifecycle、CI、vendor hygiene、governance/docs 和测试。

## Frozen Nodes

- 八字/紫微命理规则结论、新体系开发和真实外部证据提交。

## Invalidated Nodes

- 当前 wheel 独立运行声明、当前 lite skill 精简声明、当前提交 release proof。

## Reverification Required

- clean-room wheel、lite export、入口 parity、Telegram readiness、vendor post-test、quick CI、governance strict 和远端 CI。
