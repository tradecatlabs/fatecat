# Context

0090 接在 0089 current audit bundle 之后，处理测算基础设施“多交付面同源输出”缺口。

## Current Evidence

- `contracts/fate/delivery/registry.json` 已声明 FastAPI、Web、Telegram Bot 都应复用 `calculate_delivery_result` 与 `generate_full_report`。
- 临时探测发现 API 标准 Markdown 的 bazi 路径未显式传 `bazi_engine="capability"`，Web 已传入 capability，引起八字报告块和真太阳时秒级输出不同。
- 临时探测发现 Bot `_calc_and_save_report` 同样依赖 `calculate_delivery_result` 默认 legacy bazi 引擎。
- 紫微报告含 `inputTrace.asOf` / Markdown `运限日期`，跨 direct/job 秒级不同；这是运行时字段，不是盘面语义差异。

## Non-Claims

- 本任务不证明真实 Telegram Bot live 已通过。
- 本任务不证明 HF Space、公网 API、真实浏览器或真实移动端已通过。
- 本任务不证明 CLI JSON 输出与 Markdown 报告同源。
- 本任务不证明业务解释专业准确性，只证明同一输入在本地交付面上的标准 Markdown 语义一致。

## Privacy Boundary

- 固定样本只允许北京 / 测试用户。
- 证据 JSON 不保存完整 Markdown 正文。
- 证据 JSON 不保存真实 token、secret、DSN、webhook URL、生产日志或真实用户输入。
