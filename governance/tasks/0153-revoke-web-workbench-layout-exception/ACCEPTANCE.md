# Task-Level Acceptance
- `/web` 响应不含 `<style>`、外部 CSS、`style=`、`class=`、`@media`、`main`、`section` 或无必要 `div`。
- 页面有唯一明确 `h1`，使用原生 GET form/fieldset/label/input/select/button。
- 无 JavaScript 时仍能 GET 提交并由服务端返回错误或完整报告。
- 异步任务提交/轮询和 Markdown 复制仍作为渐进增强保留。
- 八字和紫微输出、隐私脱敏、错误提示与报告结构回归通过。
- 所有当前真相源明确“2026-07-12 授权已撤销，当前无例外”。

# Validation Plan
- `.venv/bin/python -m pytest -q tests/regression/test_web_html.py`
- `.venv/bin/ruff check domains/experience-delivery/services/fatecat-delivery/src/web_ui.py tests/regression/test_web_html.py`
- `.venv/bin/ruff format --check domains/experience-delivery/services/fatecat-delivery/src/web_ui.py tests/regression/test_web_html.py`
- `python3 governance/tools/rebuild_governance_index.py --project-root .`
- `python3 governance/tools/validate_governance_package.py --project-root . --strict`
- `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0153-zero-beauty-web`
- `git diff --check`

# Review Gate
- correctness：表单、报告、异步状态、复制与错误路径未回归。
- architecture：Web UI 不计算命理规则，服务层边界未变化。
- test-quality：测试断言外部语义和禁止项，不锁定已删除的视觉实现。
- document-drift：实现、测试、标准、Gate、module context、AGENTS/README 同步。
- ponytail-complexity：净删除，无新依赖、配置、兼容层或双轨页面。

# Runtime Verification Gate
- 目标测试必须全部通过。
- quick CI 必须通过，或真实失败必须记录并修复后重跑。
- 源码与渲染响应的禁用项扫描必须无匹配。

# Ship Readiness
- 本地代码和治理 closeout 完成后可进入版本控制交付。
- 当前用户未要求 commit/push，因此 Git 交付明确留待后续授权。

# Task Package Acceptance
- TP-01：实现无 CSS/class/布局容器且目标测试通过。
- TP-02：测试和全部当前真相源同步，无活动文档继续授权旧布局。
- TP-03：目标测试、lint/format、治理、quick CI、diff check 和独立审查完成。

# Anti-Goals
- 不保留视觉兼容开关。
- 不把 CSS 移到外部文件规避检测。
- 不删除异步任务、复制或服务端回退能力来简化页面。
- 不篡改已完成历史任务证据。
