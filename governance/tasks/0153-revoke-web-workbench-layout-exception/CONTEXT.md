# Repo Evidence
- 起始状态：`main...origin/main`，工作树 clean。
- `/home/lenovo/.codex/Design.md` 明确禁止 CSS、视觉 class、复杂布局和依赖 JavaScript 的核心内容。
- 旧实现 `web_ui.py` 包含 `<style>`、黄金比例 grid、`web-production-*` class、三块 section 和控件布局 CSS。
- 旧测试 `assert_web_production_layout_html` 主动要求上述例外存在。
- 当前治理标准、Gate、module context、lesson、agent feedback 和 README/AGENTS 均登记了该例外。

# Constraints Matrix
- 用户最新指令优先：撤销历史布局授权，不保留兼容开关。
- 保持 `/web` GET、`/api/v1/report/jobs/web`、任务轮询、Markdown 复制和报告输出行为。
- 核心内容必须服务端直出；JavaScript 只能渐进增强。
- 页面继续遵守地区脱敏和北京示例白名单。
- 所有人工编辑使用 `apply_patch`，验证结果不得伪造。

# Change Boundary
- `domains/experience-delivery/services/fatecat-delivery/src/web_ui.py`
- `tests/regression/test_web_html.py`
- 根与 delivery 的 `AGENTS.md` / `README.md`
- Web 相关 standard、Gate、lesson、feedback、module context、DEBUG 和任务级 lesson
- 当前任务目录与治理索引

# Risk Matrix
- 高：只改 CSS 不改测试/治理，会留下自动恢复旧布局的回潮入口。
- 中：删除 form 外层布局时可能破坏 GET 回退或异步脚本的 form 绑定。
- 中：删除 section/class 时可能破坏测试定位；应改用稳定语义 id 和标题。
- 低：默认浏览器布局在移动端不做定制，但这是 Design.md 的明确目标。

# Assumptions and Falsification
- 假设：用户撤销的是整个三块工作台授权，而不是只取消一句文档说明。
- 证伪条件：用户明确要求保留任一 CSS、布局或视觉 class；当前没有该要求。
- 假设：异步任务和复制能力属于功能行为，应保留。
- 证伪条件：无 JavaScript GET 提交或服务端报告不再工作。

# Critical Ambiguities
- 无阻塞歧义；“取消这个授权”足以决定删除例外及其全部实现和治理依据。

# Debug Evidence Contract
- 调试模式: Optional
- 本任务是授权撤销后的行为变更和文档漂移修复，不需要新建独立 DEBUG.md。
- 历史 DEBUG 记录保留，并追加“授权已撤销”的当前状态说明。

# Future-Optimal / Ponytail Contract
- Target end state: 一个无 CSS、无视觉 class、无布局例外的服务端语义 HTML 页面。
- Real constraints: Web/API 行为、隐私规则、可访问性、无脚本回退和 Markdown 可复制性。
- Inertia constraints: 旧 `web-production-*` 命名、旧截图、旧测试和历史任务记录。
- Kill list: `<style>`、黄金比例变量、工作台 grid、布局 class、三块 section、双轨兼容开关。
- Selected ladder rung: 删除错误对象并复用浏览器原生 HTML；不新增依赖或抽象。
- Proof point: Web 回归测试和 quick CI 通过，源码与响应均无禁用项。
- Falsifier: 任一核心 Web 行为回归，或页面仍含 CSS/class/布局容器。
- Migration slice: 一次性删除内部布局实现并同步当前真相源；历史证据只标记撤销，不改写事实。
- Rejected short-term patches: 保留 CSS 配置开关、隐藏旧 class、并行维护 legacy/new 页面。

# Document-Driven Impact
- Operating model update: not needed；项目目的和服务边界未变。
- Toolchain model update: not needed；验证命令未变。
- Process update: not needed；仍使用现有 Web gate 和 quick CI。
- Source-of-truth updates: updated；Web 实现、测试、标准、Gate、module context、AGENTS/README。
- Contract/catalog/schema impact: not needed；HTTP/API 和 capability 契约未变。
- ADR impact: not needed；这是用户明确撤销临时例外，已有标准和 Gate 是正确 owner。

# Task Package Context Map
## TP-01
- 标题: 删除布局例外并恢复语义 HTML
- 类型: refactor
- 父节点: ROOT
- 子节点: 无
- 依赖节点: 无
- 目标: 删除 CSS、视觉 class 和布局容器，同时保持 Web 表单与报告行为。
- 输出: `web_ui.py`
- Verify: `.venv/bin/python -m pytest -q tests/regression/test_web_html.py`
- Gate: 页面无禁用项且 GET/异步/复制行为保留。

## TP-02
- 标题: 同步测试与长期真相源
- 类型: governance
- 父节点: ROOT
- 子节点: 无
- 依赖节点: TP-01
- 目标: 反转测试门禁，并更新所有当前文档与机器契约。
- 输出: Web regression、AGENTS/README、standard、Gate、module context、lesson、feedback、delivery registry。
- Verify: 活动真相源扫描与任务文档校验。
- Gate: 无活动真相源继续授权旧布局。

## TP-03
- 标题: 验证、审查和 closeout
- 类型: verification
- 父节点: ROOT
- 子节点: 无
- 依赖节点: TP-02
- 目标: 完成 lint/format、治理、quick CI、diff check 和独立审查。
- 输出: STATUS、ACCEPTANCE_CHECKLIST、review evidence。
- Verify: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0153-zero-beauty-web`
- Gate: 所有本地门禁通过或真实失败已记录。
