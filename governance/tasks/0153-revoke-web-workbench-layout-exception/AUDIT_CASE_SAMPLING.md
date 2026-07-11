# Audit Case Sampling Decision

- Source: governance/tasks/0153-revoke-web-workbench-layout-exception
- Fixed Problem: 用户撤销 `/web` 三块工作台授权后，代码、测试和多个长期真相源仍共同要求该例外存在，形成“历史授权覆盖当前要求”的文档与门禁漂移。
- Decision: no-case
- Case ID: -
- Case Path: -
- Root Cause Class: stale-exception-and-source-of-truth-drift
- Trigger Signals: 用户撤销授权；实现仍含 `<style>`/布局 class；测试仍正向断言旧例外；AGENTS/README/standard/module context 仍声明旧授权有效。
- Evidence: `tests/regression/test_web_html.py::assert_zero_beauty_semantic_html`；`.venv/bin/python -m pytest -q tests/regression/test_web_html.py`；`python3 governance/tools/validate_governance_package.py --strict`；`bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0153-zero-beauty-web`。
- No-Case Reason: 不新建审计案例；该问题的审计问题、证据要求和机械阻断已经由现有 `LESSON-0001`、`AF-0001` 与 `GATE-0001` 完整承载，本轮直接更新既有 Gate，避免重复治理对象。

## Reusable Audit Questions

- 用户撤销或收紧授权后，代码、测试、文档和机器契约是否全部同步？
- 回归测试是在保护当前规则，还是仍在保护已经失效的历史例外？
- 历史记录是否被清楚标记为历史，而没有继续作为当前执行入口？

## Evidence Required

- 当前渲染响应的禁用项扫描。
- 目标回归测试和全局 quick CI 的新鲜通过证据。
- 活动 source-of-truth 扫描与 governance strict 结果。
