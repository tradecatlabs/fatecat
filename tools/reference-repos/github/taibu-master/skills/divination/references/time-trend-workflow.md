# Time Trend Workflow (固定顺序)

## 0. Input Check

- **⏰ 先获取当前时间**（用于日运日期和大运定位）
- 区分时间粒度：Daily (日运) vs Period (大运/流年)
- 每日运势 Inputs: `date` (默认今天), 可选 `birthYear` + `dayMaster` 或完整八字
- 大运计算 Inputs: `gender`, `birthYear`, `birthMonth`, `birthDay`, `birthHour` + 可选 `calendarType`, `isLeapMonth`, `birthMinute`
- 建议：对于每日运势，若用户未提供八字，仅输出通用黄历信息；若提供八字则输出个性化十神并推导幸运色/方位。

## 1. 每日运势 (Daily Fortune)

### 1.1 Tool Call
- Call `daily_fortune`
- Required Args: 无
- Optional Args: `date`, `dayMaster`, `birthYear`, `birthMonth`, `birthDay`, `birthHour`

### 1.2 Analysis
- **Almanac Context** (从 `almanac` 提取):
    - `lunarDate` / `lunarMonth` / `lunarDay` → 农历日期
    - `solarTerm` → 节气（如有）
    - `suitable[]` / `avoid[]` → 宜/忌
    - `chongSha` → 冲煞
    - `jishen[]` → 吉神宜趋
    - `xiongsha[]` → 凶煞宜忌
    - `pengZuBaiJi[]` → 彭祖百忌
    - 识别当天能量基调（如：破日、三合日、天赦日等）。
- **Day Info** (从 `dayInfo` 提取):
    - `stem` / `branch` / `ganZhi` → 日干支
- **Personalized Component** (if `dayMaster` provided):
    - Analyze `tenGod` (流日十神): e.g., 伤官日需防口舌，正财日利求财。
- **Lucky Color/Direction Derivation**:
    - 输出"依据 -> 结论"两段式：依据八字推导幸运颜色/幸运方位。

## 2. 大运分析 (DaYun Analysis)

### 2.1 Tool Call
- Call `dayun_calculate`
- Required Args: `gender`, `birthYear`, `birthMonth`, `birthDay`, `birthHour`
- Optional Args: `birthMinute`, `calendarType`(solar/lunar), `isLeapMonth`

### 2.2 Analysis
- **大运列表** (从 `list[]` 遍历):
    - `startYear` → 大运起始年份
    - `ganZhi` → 大运干支
    - `stem` / `branch` → 天干/地支
    - `tenGod` → 大运天干十神（相对日主）
    - `branchTenGod` → 大运地支主气十神
    - `hiddenStems[]` → 藏干明细（含 qiType/tenGod）
    - `naYin` → 纳音
    - `diShi` → 地势（十二长生）
    - `shenSha[]` → 神煞
- **DaYun Context (10-Year Macro)**:
    - 根据用户年龄定位当前大运步
    - 判断大运是帮身还是克泄，定十年基调
- **LiuNian Context (1-Year Trigger)**:
    - 结合当前年份干支与日主关系
    - Check for GanZhi interactions (He/Chong/Xing/Hai) with the natal chart.
    - Output `trend`: Favorable/Neutral/Unfavorable.
- **LiuYue Context (Monthly Fluctuation)**:
    - Only if specific monthly analysis is requested.
    - Identify specific months of opportunity or risk.

## 3. Synthesis Layer (Mandatory for Combined Queries)

- 当用户问"今年运势"时：
    1. 先看大运（底色）— from `dayun_calculate`.
    2. 再看流年干支（主事件）。
    3. 结合大运 `tenGod` 解释吉凶原因。
- 当用户问"明天运势"时：
    1. 先看流月（月环境）。
    2. 再看流日（日触发）— from `daily_fortune`.
    3. 给出具体宜忌。

## 4. Quick Template

1. **结论摘要**: (e.g., "中平偏吉，利事业，忌高风险投资")
2. **时间能量**:
    - 黄历/节气背景（from `almanac`）
    - 个性化十神 (e.g., "今日偏财主事"，from `tenGod`)
3. **关键指标**:
    - 大运趋势 (from `dayun_calculate` → `tenGod/branchTenGod`)
    - 日运趋势 (from `daily_fortune`)
4. **行动指南**:
    - 宜：...
    - 忌：...
    - 幸运锦囊 (Derived Color/Direction)
