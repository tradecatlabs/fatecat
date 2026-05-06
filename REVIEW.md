# FateCat 自审记录

审查时间：2026-05-07 CST +0800

## 结论

本地仓库卫生、skill 包装装配、导出包 smoke 与第三方审计交接准备为 `PASS`。直接公网生产复用仍为 `WARN`，原因是真实 Bot、生产 API URL、CORS、真实凭证、远端 CI 与 legacy vendor 许可证复核仍需要外部环境或人工权限。

当前 worktree 已完成根目录治理：真实源码收进 `scripts/project/`，生命周期资产收进 `scripts/project/assets/docs/lifecycle/`，根目录只保留 skill 入口、脚本、参考文档、审计文档和 GitHub 配置。

## 当前证据

| 项目 | 证据 |
|---|---|
| 当前分支 | `main` |
| 本次迁移前远端 HEAD | `b6274e8 chore: harden source asset hygiene` |
| 当前目录形态 | 根 `project/` 已移除；根 `assets/` 已移除；源码根为 `scripts/project/` |
| 未跟踪非忽略文件 | `git ls-files --others --exclude-standard` 返回 `0` |
| 完整本地验收 | `bash scripts/acceptance.sh --with-dev` 在目录迁移后通过 |
| pytest | acceptance 内 `48 passed` |
| ruff | acceptance 内 `All checks passed!` |
| format | acceptance 内 `88 files already formatted` |
| mypy | acceptance 内 `Success: no issues found in 21 source files` |
| API smoke | acceptance 内通过 |
| Bot smoke | acceptance 内 dry-run 通过 |
| 源仓卫生 | `bash scripts/check-source-hygiene.sh` 返回 `source hygiene ok` |
| 隐私样例 | `bash scripts/check-privacy-fixtures.sh` 返回 `privacy fixtures ok`；vendor web 占位样例保持隔离 |
| 导出包卫生 | `bash scripts/check-export-hygiene.sh /tmp/fatecat-acceptance/export/fatecat` 返回 `export hygiene ok` |
| 空白字符检查 | `git diff --check` 与 `git diff --cached --check` 通过 |

## 本轮修复

- `project/` 移入 `scripts/project/`，满足根目录卫生要求。
- 根 `assets/lifecycle/` 移入 `scripts/project/assets/docs/lifecycle/`。
- 根脚本、CI、导出、live smoke、源仓卫生、隐私样例和文档路径同步到新目录结构。
- `scripts/common.sh` 统一以 `scripts/project/` 作为项目根，以 `scripts/project/assets/docs/lifecycle/` 作为生命周期资产根。
- 第一方 docs、tests、scripts 示例不再使用深圳、张三等非北京真实感样例，统一为北京 / 测试用户口径。
- `scripts/check-privacy-fixtures.sh` 保持第三方 vendor web 样例隔离，防止其进入第一方文档、测试、脚本或生产 Web 输出。
- `scripts/clean-runtime.sh` 默认清理根 `.history/`，并继续清理根输出、Python 缓存和工具缓存。

## 剩余风险

### 生产验证缺口

- 真实 `FATE_BOT_TOKEN` 尚未完成 Telegram Bot live 验证。
- 真实 webhook、生产服务器、生产 API URL、CORS allowlist、systemd / 容器部署与生产数据库权限仍需外部环境验证。
- 当前 owner/admin token 模型适合轻量 API 保护；若开放公网多租户，应接入成熟认证层，补齐 token 轮换、撤销、审计日志和限流。

### 供应链与 vendor

- `scripts/project/assets/vendor/` 保存完整外部源码快照，体积偏大是为了完整复用和审计。
- 部分 legacy vendor 资产仍需人工许可证复核；`vendor-health.sh` 能校验元数据和哈希，不能替代法律审计。
- 第三方 vendor web 样例可能包含原始 demo 占位数据。当前已被策略和测试隔离，公开再分发前仍建议审计人员复查。

### 交付状态

- 本次迁移涉及数千个文件，审查时应按目录迁移看待，而不是普通功能 diff。
- 远端 CI 只有在本次迁移 commit 推送后才是最终权威结果。

## 当前门禁

- 本地仓库卫生：PASS
- skill 包装装配：PASS
- 第三方审计准备：PASS，风险已记录
- 直接公网生产发布：WARN，需完成 live Bot、生产网络、真实凭证、远端 CI 与 legacy vendor 许可证审计
