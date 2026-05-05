# FateCat 标准输出复查提示词

## 任务目标

基于当前仓库事实复查 FateCat 标准报告、结构化 API 输出与 skill 交付门禁，不使用历史“全功能隐藏块”口径。

## 必查项

1. 标准 Markdown 报告顺序：
   - 免责声明
   - `## 赞助支持`
   - `# 命理排盘报告：{姓名}`
   - 第一卷到第四卷
2. 标准报告不得输出：
   - 健康预警
   - 出生日黄历
   - 第五卷：学术参数
   - 六爻 / 梅花 / 数字起卦 / 奇门 / 大六壬
   - 风水 / 天文 / 高级历法 / 择日 / 易经
   - 姓名合婚 / 系统附录
3. 未来功能登记：
   - 所有退役块必须能在 `assets/fate/future_features.json` 找到候选项。
4. 验收证据：
   - `scripts/acceptance.sh --with-dev`
   - API delivery smoke
   - Bot dry-run
   - lite export smoke

## 输出形式

只输出复查报告：

- 结论：PASS / WARN / BLOCK
- 证据
- 问题项
- 建议修复顺序

禁止承诺未经真实测试证明的线上行为。
