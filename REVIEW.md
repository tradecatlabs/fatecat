# FateCat Self Review

审查时间：2026-05-06 HKT +0800

## Verdict

`WARN` for repository handoff, `BLOCK` for direct public production exposure.

当前分支代码、测试、导出包与远端 CI 已经通过交付门禁，可以进入后续人工审计与工程修复；但仍不能直接宣称公网生产可复用。主要阻断项集中在 API 记录接口鉴权、异常信息暴露、旧部署打包脚本 secret 泄露风险，以及真实 Telegram / webhook / 生产环境未验证。

## Current State

| Item | Evidence |
|---|---|
| Branch | `main` |
| HEAD | `e4d10c8c27cb97acdc45a22417fdcb06b495439b` |
| Commit | `feat: separate report system outputs` |
| Remote | `origin/main` |
| Local vs remote | `HEAD == origin/main` before this review commit |
| GitHub Actions | success, `https://github.com/tukuaiai/fatecat/actions/runs/25406755173` |
| Local acceptance | `bash scripts/acceptance.sh --with-dev` passed |
| pytest | `36 passed in 7.44s` in full acceptance |
| ruff | `All checks passed!`; `87 files already formatted` |
| mypy | `Success: no issues found in 21 source files` |
| API smoke | passed, `http://127.0.0.1:8001/health` |
| Bot smoke | dry-run passed |
| Export smoke | passed |
| Export hygiene | `export hygiene ok` before and after exported smoke |

## Recently Landed

- 默认 Markdown 报告拆成独立体系：`bazi`、`ziwei`、`jianchu`、`bone`。
- Web `/web` 新增 `reportSystem` 控件，每次只输出一个体系。
- 默认 `bazi` 不再混排紫微、建除十二神、袁天罡称骨。
- README、功能状态、架构图、审计提示词与 Web 测试已同步新契约。

## Findings

### FC-SR-001: API 记录读写接口仍无鉴权

- Severity: blocker for public production
- Evidence:
  - `project/modules/telegram/src/main.py:47` CORS 当前为 `allow_origins=["*"]`。
  - `project/modules/telegram/src/main.py:218-260` 通过 query 参数 `user_id` 保存记录。
  - `project/modules/telegram/src/main.py:310-331` 读取、列出、删除记录接口没有鉴权、owner 校验或 admin 校验。
- Impact:
  - 如果 API 暴露公网，姓名、出生日期、出生时间、出生地区、经纬度、完整命理结果可能被非授权读取或删除。
- Recommended fix:
  - 引入统一认证依赖；`user_id` 从认证上下文获取，不信任 query 参数。
  - `GET /records/{id}`、`GET /user/{user_id}/records`、`DELETE /records/{id}` 增加 owner/admin 校验。
  - CORS 改为配置 allowlist，生产默认不使用 `*`。

### FC-SR-002: API 异常响应仍会暴露内部错误文本

- Severity: major
- Evidence:
  - `project/modules/telegram/src/main.py:87-95` 全局异常处理返回 `str(exc)`。
  - `project/modules/telegram/src/main.py:183-184`、`270-275`、`300-305` 将异常文本进入 API 响应。
- Impact:
  - 可能向调用方暴露内部路径、依赖错误、数据库错误、第三方库错误或实现细节。
- Recommended fix:
  - 对外返回稳定错误码和泛化文案。
  - 详细异常只写服务端日志，并带 request id。
  - 对业务错误定义受控异常类型。

### FC-SR-003: 默认 bazi 输出已分离，但计算层仍会运行紫微扩展

- Severity: performance / architecture major
- Evidence:
  - `project/modules/telegram/src/web_ui.py:128` Web 仍以 `calculator.calculate(hide=REPORT_HIDE)` 计算完整结果。
  - `project/modules/telegram/src/report_generator.py:66-79` `DEFAULT_HIDE` 没有设置 `extensions=True`。
  - `project/modules/telegram/src/bazi_calculator.py:514-537` 未隐藏 `extensions` 时会执行 `sxwnl` 和 `ziwei`。
- Impact:
  - 默认 `bazi` 不显示紫微，但仍为每次 Web 报告支付紫微计算成本。
  - 后续如果紫微 vendor 缺失，可能影响本应只需要八字的输出。
- Recommended fix:
  - 根据 `reportSystem` 构造计算 hide：`bazi/jianchu/bone` 默认 `extensions=True`，`ziwei` 才开启紫微所需扩展。
  - 长期拆分为 `calculate_bazi_result` 与 `calculate_ziwei_result`，避免呈现层过滤替代计算契约。

### FC-SR-004: Web 已支持体系切换，API/Bot 仍无同等选择入口

- Severity: product consistency medium
- Evidence:
  - `project/modules/telegram/src/main.py:106-123` `/web` 支持 `reportSystem`。
  - `project/modules/telegram/src/main.py:163-277` JSON API 仍只有 bazi 计算接口。
  - `project/modules/telegram/src/bot.py:901-904` Bot 仍直接 `generate_full_report(result, hide=REPORT_HIDE)`，没有用户选择体系。
- Impact:
  - Web 能单独切换紫微/建除/称骨，但 Telegram 与 API 用户无法选择同样的 Markdown 体系。
- Recommended fix:
  - API 增加报告体系参数或新增 `/api/v1/report/markdown`。
  - Bot 增加结果页按钮：正宗八字、紫微、建除、称骨。

### FC-SR-005: 旧部署打包脚本可能携带本地 `.env`

- Severity: critical if used for deployment
- Evidence:
  - `project/assets/deploy/pack.sh:21-23` 复制整个 `assets/`。
  - `project/assets/deploy/pack.sh:26-30` 只清理 `node_modules`、`__pycache__`、`*.pyc`、`*.db`，没有清理 `.env`、`.key`、`.pem`、credential JSON。
- Impact:
  - 若开发机或部署机存在 `project/assets/config/.env`，Bot token 可能进入 tarball。
- Recommended fix:
  - 废弃该脚本，统一调用根 `scripts/export-runtime.sh`。
  - 或复用 `scripts/check-export-hygiene.sh` denylist，打包后强制检查。

### FC-SR-006: vendor 来源、license、完整性元数据不足

- Severity: major
- Evidence:
  - `project/assets/vendor/vendor_sources.json:4-83` 只有 id、path、source、purpose；缺少 license、commit/tag、sha256、retrievedAt。
  - `project/assets/vendor/README.md:21` 的 `sxwnl` 来源与 manifest `project/assets/vendor/vendor_sources.json:18-20` 不一致。
- Impact:
  - 第三方审计无法只凭仓库文件确认 vendor 许可、版本和完整性。
- Recommended fix:
  - 为每个 vendor 增加 license、commit/tag、sha256、retrievedAt、distributionAllowed。
  - `scripts/vendor-health.sh` 校验这些元数据和 LICENSE 文件。

### FC-SR-007: Python lockfile 未参与默认 bootstrap

- Severity: reliability / reproducibility major
- Evidence:
  - `project/pyproject.toml:16-33` 使用 `>=` 版本范围。
  - `project/requirements.lock.txt:1-35` 已存在固定版本。
  - `scripts/bootstrap.sh:39-43` 安装时没有使用 lockfile 或 constraints。
- Impact:
  - CI 和本地环境会随 PyPI 最新解析结果变化，长期可能出现非确定性失败。
- Recommended fix:
  - bootstrap / CI 改为使用 constraints：`pip install -c project/requirements.lock.txt -e '.[dev]'`。
  - 或迁移到 `uv sync --locked` / pip-tools 统一锁定。

### FC-SR-008: live Bot、webhook、生产部署仍未验证

- Severity: blocker for production release
- Evidence:
  - 本地 acceptance 只覆盖 Bot dry-run。
  - `references/live-bot-verification.md` 明确真实验收需要 `FATE_BOT_TOKEN=<real-token> bash scripts/live-bot-smoke.sh`。
- Impact:
  - 不能声明真实 Telegram Bot API、webhook/轮询、生产网络、systemd/container、数据库权限已经可用。
- Recommended fix:
  - 使用真实 token 执行 `scripts/live-bot-smoke.sh`。
  - 在生产目标机验证 API health、Bot get_me、服务重启、日志脱敏、数据库权限和备份。

## Optimization Backlog

1. 将报告体系选择下沉为统一 contract：Web、API、Bot 共享 `reportSystem` 枚举。
2. 按体系拆计算 profile：默认 bazi 不再计算紫微；ziwei 独立计算紫微。
3. 给 `generate_full_report` 增加 golden snapshot，覆盖四种体系的 heading 和禁入块。
4. 废弃旧 `project/assets/deploy/pack.sh`，避免与根导出链路形成两套发布路径。
5. 增强 vendor manifest 与 vendor-health，补 license / commit / hash / source consistency。
6. 将 bootstrap 与 CI 切到 lockfile/constraints，减少依赖漂移。
7. 增加生产安全模式：鉴权、CORS allowlist、错误脱敏、记录接口开关。
8. 增加 live-smoke 交接模板，明确哪些验证必须由真实凭证和生产环境完成。

## Current Gate

- Local engineering gate: PASS
- GitHub Actions gate: PASS for `e4d10c8`
- Third-party audit readiness: PASS with known risks documented
- Public production release: BLOCK until FC-SR-001, FC-SR-005 and FC-SR-008 are addressed or explicitly risk-accepted
