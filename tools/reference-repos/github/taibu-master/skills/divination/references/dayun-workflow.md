# DaYun Workflow (固定顺序)

## 0. Input Check

- **⏰ 先获取当前时间**（用于定位当前大运步）
- 必要输入：`gender`, `birthYear`, `birthMonth`, `birthDay`, `birthHour`
- 可选输入：
  - `birthMinute` — 精确到分，默认 0
  - `calendarType` — `solar`(默认) / `lunar`
  - `isLeapMonth` — 仅 `calendarType=lunar` 有效，默认 false
- 调用工具：`dayun_calculate`

## 1. 大运数据层

- 遍历 `list[]`（最多 10 步大运），提取每步：
  - `startYear` → 大运起始年份
  - `ganZhi` → 大运干支
  - `stem` → 天干
  - `branch` → 地支
  - `tenGod` → 天干十神（相对日主）
  - `branchTenGod` → 地支主气十神
  - `hiddenStems[]` → 藏干明细（每项含 `stem`, `qiType`: 本气/中气/余气, `tenGod`）
  - `naYin` → 纳音
  - `diShi` → 地势（十二长生）
  - `shenSha[]` → 本步大运神煞

## 2. 大运节奏层（Mandatory）

- 标注天干十神与地支十神是否协调（有无截脚/盖头）
- 分析 `hiddenStems[]` 中的藏干十神：多重力量叠加还是互相牵制
- 参考 `naYin`（纳音）判断五行能量质感
- 参考 `diShi`（十二长生）判断日主在该运中的生旺死绝状态
- 关注 `shenSha[]` 中的吉凶神煞对该运的助力或阻碍

## 3. 当前大运定位（Mandatory）

- 根据用户 `birthYear` 和**当前年份**（从当前时间获取），计算年龄
- 在 `list[]` 中找到 `startYear <= 当前年份` 的最近一步 = 当前大运
- 输出当前大运的详细解读：
  - 十年主题定性（结合 `tenGod` + `branchTenGod` + `hiddenStems`）
  - 已过/剩余年数
  - 神煞影响（从 `shenSha[]` 解读）
  - 地势状态（从 `diShi` 解读日主状态）
  - 与原命盘喜用神的关系（帮身 or 克泄）

## 4. 关键转折点

- 识别大运切换年份（相邻两步 `startYear`）
- 标注十神由X转Y的转折（如由"正财"转"七杀"= 从稳定期进入挑战期）
- 对比相邻大运的 `shenSha[]` 变化
- 输出未来最近的转折时间和调整建议

## 5. 结论层

- 避免绝对化表述
- 每条判断绑定 `tenGod` / `branchTenGod` / `shenSha` / `diShi` 数据依据

## 6. Quick Template

1. 当前大运（干支 + 十神 + 纳音 + 地势 + 神煞 + 主题）
2. 下步大运预览（转折时间 + 新主题 + 神煞变化）
3. 十年节奏建议（守/攻/调整分段）
4. 行动建议（可执行）
