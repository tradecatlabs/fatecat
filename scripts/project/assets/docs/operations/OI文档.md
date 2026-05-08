# FateCat API / Bot 文档

> 最后更新: 2026-05-06

## 概述

FateCat 八字排盘系统 API / Bot 接口规范，基于当前 skill 化后的标准报告契约与 `fate_core` / Telegram 交付层实现。

### 🎯 当前状态
- **标准报告**: 默认输出免责声明、赞助支持、标题、第一卷先天命格、第二卷后天运路与第三卷民俗建议，第三卷包含袁天罡称骨。紫微斗数通过 `report_system` / Web 控件 / API `options.reportSystem` / Bot 确认页按钮独立输出，不与综合八字混排；黄历/择日已作为 `almanac` 独立 capability 提供 CLI/API 结构化输出，六爻、梅花、奇门、大六壬、风水九星、姓名合婚等仍登记为独立待实现体系。
- **前端地区展示**: 非北京类真实出生地区只参与经纬度解析和后端计算，Web/Bot/Markdown 展示层统一隐藏。
- **未来功能**: 退出标准报告的扩展能力统一登记在 `assets/fate/future_features.json`，后续必须按独立输入契约、输出模板与测试重新进入生产。
- **结构化输出**: API / pure-analysis 优先依赖字段 profile 和结构化 JSON，不要求 TXT 报告承载全部历史字段。
- **产物**: 每次排盘落地 2 份 TXT（常规版 + `-ai分析版`），并推送到 Telegram。
- **恢复能力**: 发送/拉取更新内置重试，健康检查 3 次失败自动退出，由外层 `run_with_retry` 复活。

---

## 📥 输入 (Request)

### Bot 输入格式
```
文本输入: 日期 时间（公历） 地点 姓名
按钮选择: 性别 (乾造/坤造)
地点必须命中 china_coordinates.csv，否则退回主菜单
```

### API 输入格式
```json
{
  "name": "测试用户",                      // 姓名 (可选)
  "gender": "male",                        // 性别: male/female
  "birthDate": "1990-01-01",               // 出生日期 (公历)
  "birthTime": "08:00",                    // 出生时间 (HH:MM)
  "birthPlace": "北京市",                   // 地点名称 (支持省市区)
  "options": {
    "useTrueSolarTime": true,              // 真太阳时修正 (默认true)
    "calendarType": "solar",               // 历法: solar(公历)
    "reportSystem": "bazi"                 // 当前可用: bazi/ziwei
  }
}
```

---

## 📤 输出 (Response)

### Bot 产物（Telegram）
- 说明消息：Markdown 代码块列出两个文件名，附常用 AI 链接，内联按钮「🎲 重新排盘」。
- 附件：`modules/telegram/output/txt/` 下两份 TXT 作为 media group 发送（无 caption，避免 Markdown 解析错误）。
- 文件命名：`YYYY-MM-DD-HH:MM-地点-姓名-性别.txt` 与同名 `-ai分析版.txt`（前者纯报告，后者在首部拼接 `src/prompts/快速版.md`）。

### API / 内部调用返回

```json
{
  "success": true,
  "data": {
    // 四柱八字
    "fourPillars": {
      "year":  { "stem": "庚", "branch": "午", "fullName": "庚午", "nayin": "路旁土" },
      "month": { "stem": "辛", "branch": "巳", "fullName": "辛巳", "nayin": "白蜡金" },
      "day":   { "stem": "庚", "branch": "辰", "fullName": "庚辰", "nayin": "白蜡金" },
      "hour":  { "stem": "癸", "branch": "未", "fullName": "癸未", "nayin": "杨柳木" }
    },
    
    // 藏干
    "hiddenStems": {
      "year":  ["己", "丁"], "month": ["丙", "庚", "戊"],
      "day":   ["戊", "乙", "癸"], "hour":  ["己", "丁", "乙"]
    },
    
    // 十神
    "tenGods": {
      "year":  { "stem": "比肩", "branch": ["正财", "伤官"] },
      "month": { "stem": "劫财", "branch": ["食神", "比肩", "正财"] },
      "day":   { "stem": "日主", "branch": ["正财", "偏印", "正印"] },
      "hour":  { "stem": "伤官", "branch": ["正财", "伤官", "偏印"] }
    },
    
    // 十二长生
    "twelveGrowth": { "year": "沐浴", "month": "长生", "day": "养", "hour": "冠带" },
    
    // 五行统计
    "fiveElements": {
      "wood":  { "count": 2, "percentage": 13.3, "chineseName": "木" },
      "fire":  { "count": 3, "percentage": 20.0, "chineseName": "火" },
      "earth": { "count": 4, "percentage": 26.7, "chineseName": "土" },
      "metal": { "count": 4, "percentage": 26.7, "chineseName": "金" },
      "water": { "count": 2, "percentage": 13.3, "chineseName": "水" }
    },
    
    // 五行状态
    "wuxingState": {
      "wood": {"state": "囚", "chineseName": "木"}, 
      "fire": {"state": "相", "chineseName": "火"},
      "earth": {"state": "死", "chineseName": "土"},
      "metal": {"state": "旺", "chineseName": "金"},
      "water": {"state": "休", "chineseName": "水"}
    },
    
    // 日主信息
    "dayMaster": {
      "stem": "庚", "element": "metal", "elementCn": "金",
      "yinYang": "阴", "strength": "偏旺", "selfSitting": "正财"
    },
    
    // 特殊宫位
    "specialPalaces": {
      "taiYuan": { "pillar": "壬申", "nayin": "剑锋金" },
      "taiXi":   { "pillar": "乙酉", "nayin": "泉中水" },
      "mingGong": { "pillar": "辛巳", "nayin": "白蜡金" },
      "shenGong": { "pillar": "己丑", "nayin": "霹雳火" }
    },
    
    // 空亡信息
    "voidInfo": {
      "year":  { "xun": "甲午", "kong": ["辰", "巳"] },
      "month": { "xun": "甲午", "kong": ["辰", "巳"] },
      "day":   { "xun": "甲午", "kong": ["申", "酉"] },
      "hour":  { "xun": "甲午", "kong": ["申", "酉"] }
    },
    
    // 神煞 (21种)
    "spirits": {
      "auspicious": ["天乙贵人", "文昌贵人", "天德贵人"],
      "inauspicious": ["羊刃", "劫煞"],
      "special": ["驿马", "桃花", "华盖"],
      "byPillar": {
        "year": ["天乙贵人", "驿马"],
        "month": ["文昌贵人"],
        "day": ["华盖"],
        "hour": ["桃花"]
      }
    },
    
    // 干支关系
    "ganzhiRelations": {
      "ganHe": [], "ganChong": [],
      "zhiHe": [], "zhiChong": [], "zhiXing": [], "zhiHai": [], "zhiPo": []
    },
    
    // 大运
    "majorFortune": {
      "direction": "顺行", "startAge": 7, "startYear": 1998,
      "startDetail": "1年6月15天",
      "pillars": [
        { "age": 8, "startYear": 1998, "stem": "壬", "branch": "午", "fullName": "壬午", "shishen": "伤官" }
      ]
    },
    
    // 流年
    "annualFortune": [
      { "year": 2025, "stem": "甲", "branch": "辰", "fullName": "甲辰", "shishen": "偏财" }
    ],
    
    // 流月
    "monthlyFortune": [
      { "month": 1, "stem": "戊", "branch": "寅", "fullName": "戊寅", "shishen": "偏印" }
    ],
    
    // 小运
    "xiaoYun": [
      { "age": 1, "stem": "甲", "branch": "申", "fullName": "甲申", "shishen": "偏财" }
    ],
    
    // 称骨算命
    "boneWeight": { "weight": 4.2, "weightCn": "4两2钱", "text": "早年运道未曾亨..." },
    
    // 命卦
    "mingGua": { "guaNum": 9, "guaName": "离", "direction": "南", "group": "东四命" },
    
    // 格局判断 (10种)
    "geju": { "patterns": ["建禄格"], "main": "建禄格" },
    
    // 用神分析
    "yongShen": {
      "tiaoHou": {"xi": ["水"], "ji": ["火"]},
      "hasXi": true, "hasJi": false,
      "note": "庚金生于巳月，火旺金弱，宜用水调候"
    },
    
    // 出生信息
    "birthInfo": {
      "solar": "1990-05-15 14:30", "trueSolarTime": "1990-05-15 14:16",
      "lunar": "一九九〇年四月廿一", "lunarCn": "庚午年四月廿一",
      "zodiac": "马", "constellation": "金牛座", "xingXiu": "角宿东方角木蛟"
    },
    
    // 节气详情
    "jieqiDetail": {
      "prevJieQi": {"name": "立夏", "date": "1990-05-05", "daysAfter": 10},
      "nextJieQi": {"name": "小满", "date": "1990-05-21", "daysBefore": 6}
    },
    
    // 人元司令
    "siling": {
      "current": "丙", "daysFromJieqi": 10,
      "detail": [{"gan": "丙", "days": 7, "range": "1-7日"}]
    },
    
    // 交运时间
    "jiaoYun": {
      "startYear": 1, "startMonth": 6, "startDay": 15,
      "startDate": "1998-11-30", "jiaoJieQi": "大雪"
    },
    
    // 黄历信息
    "huangLi": {
      "yi": ["祭祀", "祈福"], "ji": ["嫁娶", "安葬"],
      "jiShen": ["天德", "月德"], "xiongSha": ["五鬼", "死符"],
      "pengZu": "庚不经络 辰不哭泣", "chong": "冲狗", "sha": "煞南"
    }
  }
}
```

---

## 🎯 核心输出字段说明

| 字段 | 必须 | 说明 | 当前实现 |
|------|:----:|------|----------|
| fourPillars | ✅ | 四柱干支+纳音+五行 | 已接入标准输出 |
| hiddenStems | ✅ | 地支藏干 | 已接入标准输出 |
| tenGods | ✅ | 十神关系 | 已接入标准输出 |
| twelveGrowth | ✅ | 十二长生 | 已接入标准输出 |
| fiveElements | ✅ | 五行统计+百分比 | 已接入标准输出 |
| wuxingState | ✅ | 五行旺相休囚死 | 已接入标准输出 |
| dayMaster | ✅ | 日主信息+强弱 | 已接入标准输出 |
| specialPalaces | ✅ | 胎元/胎息/命宫/身宫 | 已接入标准输出 |
| voidInfo | ✅ | 空亡信息 | 已接入标准输出 |
| spirits | ✅ | 神煞 | 已接入标准输出 |
| ganzhiRelations | ✅ | 干支关系 | 已接入标准输出 |
| majorFortune | ✅ | 大运+十神 | 已接入标准输出 |
| annualFortune | ✅ | 流年+十神 | 已接入标准输出 |
| monthlyFortune | ✅ | 流月 | 已接入标准输出 |
| xiaoYun | ✅ | 小运 | 已接入标准输出 |
| boneWeight | ✅ | 称骨算命 | 已接入标准输出 |
| mingGua | ✅ | 命卦 | 已接入标准输出 |
| geju | ✅ | 格局判断 | 已接入标准输出 |
| yongShen | ✅ | 用神分析 | 已接入标准输出 |
| birthInfo | ✅ | 出生信息 | 已接入标准输出 |
| jieqiDetail | ✅ | 节气详情 | 已接入标准输出 |
| siling | ✅ | 人元司令 | 已接入标准输出 |
| jiaoYun | ✅ | 交运时间 | 已接入结构化输出 |
| huangLi | 否 | 黄历信息 | 已退役出八字标准报告；独立 `almanac` capability 提供择日输出 |

---

## 📊 当前实现状态

### ✅ 标准报告生产字段
当前默认 `bazi` 综合八字报告覆盖基础资料、四柱、五行、日主、格局用神、节气司令、干支关系、八字岁运趋势与袁天罡称骨。紫微斗数通过 `report_system=ziwei` 独立输出；黄历择日通过 `/api/v1/capabilities/almanac` 独立执行；其他体系通过 `GET /api/v1/report/systems` 或 `GET /api/v1/capabilities` 查询状态，未实现前不得混入综合八字。

### 🟡 可优化
- **五行力量评分**: 当前为简化算法，可提取 bazi-1-master 的精确量化
- **扩展功能**: 健康、建除十二神细分、占卜、风水、天文、历法、易经、姓名合婚与系统附录必须按 `assets/fate/future_features.json` 或 capability 协议重新设计后再进入生产；黄历/择日当前只有 `almanac` 基础结构化能力，不代表完整择日学派全部生产化。

---

## 🔧 技术实现

### 核心依赖
- `lunar-python`: 历法计算
- `china_coordinates.csv`: 3199条经纬度数据
- 真太阳时: 经度时差修正

### 输入解析支持
```
1990-05-15 14:30
1990/5/15 14:30
1990年5月15日 14点30分
19900515 1430
1990-05-15 14:30 北京市 测试用户
```

### 地点支持
- 省市区县级精确匹配
- 模糊搜索: "北京"、"北京市"
- 自动经纬度获取

---

## 🚀 使用示例

### Python 调用
```python
from bazi_calculator import BaziCalculator
from datetime import datetime

calc = BaziCalculator(
    birth_dt=datetime(1990, 5, 15, 14, 30),
    gender="male",
    longitude=114.1
)
result = calc.calculate()
```

### Bot 调用
```
输入: 1990-01-01 08:00 北京市 测试用户
选择: ♂ 乾造(男)
输出: 默认综合八字报告与结构化 JSON；紫微体系在确认页单独选择
```

### API 调用
```bash
curl -X POST "http://localhost:8001/api/v1/report/markdown" \
  -H "Content-Type: application/json" \
  -d '{"name":"测试用户","gender":"male","birthDate":"1990-01-01","birthTime":"08:00:00","birthPlace":{"name":"北京市","longitude":116.4074,"latitude":39.9042,"timezone":"Asia/Shanghai"},"options":{"useTrueSolarTime":true,"calendarType":"solar","reportSystem":"bazi"}}'
```
