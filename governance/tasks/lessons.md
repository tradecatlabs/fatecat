# 执行教训

## 2026-04-14

- 大体量 `git push` 必须默认放到后台持久会话执行，前台继续推进校验、文档或其他实现，不允许阻塞在上传进度上。

## 2026-06-15

- FateCat Web HTML 变更前必须读取 `/home/lenovo/.codex/Design.md`，不能把一般前端审美凌驾于项目明确设计契约之上。

## 2026-07-12

- `/web` 三块工作台授权已撤销，当前不存在 CSS、视觉 class、颜色、圆角、卡片、响应式布局或装饰性容器例外。任何 `/web` 变更必须用 `tests/regression/test_web_html.py::assert_zero_beauty_semantic_html` 和 `bash scripts/local-ci.sh --profile quick` 证明禁用项没有回潮。
- 开发环境中存在可选依赖不能证明生产环境具备同一行为。凡可选 extra 会改变用户可见输出，必须进入运行依赖和运行锁，并用精简生产镜像对比本地输出；本次 `tabulate` 缺少 `widechars/wcwidth` 导致 HF 与本地中文 psql 表格不一致。
- 用户明确地区交互形态时，后端 capability 不能等价映射为前端控件；Web 只暴露用户最终确认的最小交互，本轮最终是单输入框模糊搜索与完整路径候选，地区模式、时区口径和 DST 等能力保留在 API/后端。
