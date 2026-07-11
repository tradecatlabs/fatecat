# Acceptance Checklist

# Global Standards
- [x] 用户最新撤销指令已作为当前最高项目需求。
- [x] 目标结构遵守 `/home/lenovo/.codex/Design.md`。
- [x] 不新增依赖、配置、前端框架或视觉资产。
- [x] 目标测试、lint、format、治理校验、quick CI 和 diff check 全部通过。
- [x] 独立 review 给出 PASS，或所有 BLOCK/WARN 已处理。

# Task Package Checklists
## TP-01
- Verify: `.venv/bin/python -m pytest -q tests/regression/test_web_html.py`
- Gate: 页面无 CSS/class/布局容器且 Web 核心行为保留。
- [x] 删除 `_render_workspace_style` 和所有 CSS。
- [x] 删除 `web-production-*` class、三块 section 和布局 div。
- [x] 恢复唯一 `h1`、原生 GET form 和 fieldset。
- [x] 保留异步提交、轮询、复制和服务端回退。

## TP-02
- Verify: 活动真相源扫描和 delivery registry 回归。
- Gate: 当前文档与机器契约均不再授权旧布局。
- [x] 反转 Web 测试门禁为无例外零美化断言。
- [x] 更新根与 delivery AGENTS/README。
- [x] 更新 standard、Gate、module context、lesson、agent feedback 和任务级 lesson。
- [x] 历史 DEBUG 标注授权已撤销。
- [x] 确认活动真相源无旧授权残留。

## TP-03
- Verify: governance strict、quick CI、lint/format、diff check 和 auto-review。
- Gate: 所有本地门禁通过，review 无未处理 BLOCK/WARN。
- [x] 目标 Web 回归首次通过。
- [x] 完成 lint/format、治理 strict、quick CI 和 diff check。
- [x] 完成 review 路由和独立审查。
- [x] 更新 STATUS/TODO 为最终证据。
