# Ziwei Workflow (固定顺序)

## 0. Input Check

- **⏰ 先获取当前时间**（用于大限定位）
- 必要输入：`gender`, `birthYear`, `birthMonth`, `birthDay`, `birthHour`
- 可选输入：
  - `birthMinute` — 精确到分，默认 0
  - `calendarType` — `solar`(默认) / `lunar`；用户给农历日期时必须设为 `lunar`
  - `isLeapMonth` — 仅 `calendarType=lunar` 有效，默认 false
- 输出需包含：命宫、身宫、十二宫主星、大限信息

## 1. 命盘骨架层

- 从 output 提取：
  - `soul` → 命主
  - `body` → 身主
  - `fiveElement` → 五行局（决定起运岁数和紫微星布局）
  - `fourPillars` → 四柱干支
  - `solarDate` / `lunarDate` → 日期确认
  - `zodiac` / `sign` → 属相/星座
- 先看命宫/身宫定位（人格驱动力 + 行为模式）
- 再看主星组合与四化分布（在 `palaces[].majorStars[].mutagen` 中查找禄/权/科/忌）

## 2. 宫位主题层（Mandatory）

- 遍历 `palaces[]`，重点关注：
  - 每宫 `name` → 宫名
  - `majorStars[]` → 主星（含 `brightness`: 庙/旺/得/利/平/不/陷 + `mutagen`: 四化）
  - `minorStars[]` → 辅星（含亮度和四化）
  - `adjStars[]` → 杂曜
  - `isBodyPalace` → 是否身宫
- 必查宫位：
  - 命宫（底层性格与稳定倾向）
  - 官禄宫（事业模式）
  - 财帛宫（财富机制）
  - 夫妻宫（关系机制）
  - 疾厄宫（身心压力点）

## 3. 大限层（Mandatory）

- 使用 `decadalList[]` 数据定位当前大限：
  - `startAge` / `endAge` → 年龄范围
  - `heavenlyStem` → 大限天干
  - `palace.name` → 大限所在宫名
  - `palace.earthlyBranch` → 大限地支
- 根据用户年龄计算当前处于哪步大限
- 先看当前大限宫位与主导星曜
- 判断该十年主题：扩张/沉淀/转型/防守
- 再映射到事业、关系、财务优先级

## 4. 冲突与补偿层

- 找到优势结构（可放大）
- 找到结构性短板（需补偿）
- 给出"可执行补偿策略"，避免空泛标签

## 5. 结论层

- 输出风格：结构化而非玄学散文
- 每条建议对应至少一个宫位或星曜依据

## 6. Quick Template

1. 命盘主轴（命宫/身宫 + 主星 + 四化）
2. 当前十年主题（大限 + 宫位）
3. 三大优先事项（事业/关系/财务）
4. 风险与补偿动作（具体执行）
