# Bazi Workflow (固定顺序)

## 0. Input Check

- **⏰ 先获取当前时间**（用于大运流年定位）
- 必要输入：`gender`, `birthYear`, `birthMonth`, `birthDay`, `birthHour`
- 可选输入：
  - `birthMinute` — 精确到分，默认 0
  - `calendarType` — `solar`(默认) / `lunar`；用户给农历日期时必须设为 `lunar`
  - `isLeapMonth` — 仅 `calendarType=lunar` 有效，工具会校验该年该月是否真为闰月
  - `birthPlace` — 出生地点（可选，记录用途）
- 若用户只给四柱：先用 `bazi_pillars_resolve` 反查候选时间，经用户确认后再用 `bazi`（利用候选的 `nextCall` 参数，补充 `gender`）
- 缺少关键信息时先补齐，不进入结论阶段

## 1. 盘面基础层

- 从 output 提取：
  - `dayMaster` → 日主天干
  - `fourPillars.year/month/day/hour` → 四柱干支
  - 每柱 `hiddenStems[]` → 藏干（含 `qiType`: 本气/中气/余气 + `tenGod`: 相对日主十神）
  - 每柱 `shenSha[]` → 分柱神煞
  - 每柱 `kongWang.isKong` → 是否入空亡
  - `kongWang`(全局) → 旬名 + 空亡地支
- 明确季节/月令背景（月柱地支 → 旺衰环境）

## 2. 身强/身弱判定层（Mandatory）

- 依据月令、通根、透干、帮扶/克泄耗综合评估
- 参考 `fourPillars` 各柱 `diShi`（十二长生）辅助判断
- 输出：`身强` / `身弱` / `中和偏强` / `中和偏弱` / `从格` 等
- 给出3条以内关键证据

## 3. 喜用神判定层（Mandatory）

- 先定格局平衡目标，再定用神，最后给喜神/忌神
- 参考 `fourPillars` 各柱 `naYin`（纳音）辅助五行分析
- 输出结构：
  - 用神（主调节五行）
  - 喜神（辅助五行）
  - 忌神（加剧失衡）

## 4. 人生主题层

- 从十神组合提炼：事业、财务、关系、健康、学习/表达
- 参考 `relations[]` 中的地支刑害合冲关系
- 每个主题给 `趋势 + 原因 + 行动点`

## 5. 大运流年层（Mandatory）

- 调用 `dayun_calculate` 获取大运列表
  - 需要相同的 `gender` + `birth*` 参数
  - Output: `list[]`（每步大运含 `startYear`, `ganZhi`, `stem`, `branch`, `tenGod`, `branchTenGod`, `hiddenStems[]`, `naYin`, `diShi`, `shenSha[]`）
- 根据当前年份定位当前大运步，参考 `diShi`（地势）和 `shenSha[]`（神煞）辅助判断
- 先看大运（10年基调），再看流年（年度触发），再看流月（短期波动）
- 输出近3年节奏建议（守/攻/调整）

## 6. 结论表达层

- 结论避免"宿命绝对化"
- 用概率和条件表达：
  - 推荐：`若A持续，则B概率上升`
  - 避免：`你一定会...`

## 7. Quick Template

1. 结论摘要（身强弱 + 喜用神 + 当前运势）
2. 核心依据（3-6个盘面证据）
3. 分项解读（事业/财务/关系/健康）
4. 大运流年窗口（近/中/远）
5. 行动建议（可执行）
