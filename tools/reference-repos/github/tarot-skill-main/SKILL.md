---
name: tarot
description: |
  Use when the user asks for tarot/塔罗/占卜/抽牌/牌阵/每日一牌/运势/感情、事业、决策指引. Provide Chinese tarot readings with scripted random draws, upright/reversed cards, agency-first advice, and safety boundaries.
---

# Tarot 塔罗占卜

塔罗是镜子，不是水晶球：把牌面转成自我观察和可选择的下一步，不宣判固定命运。

## 必守规则

- 模糊问题先确认主题；可问锚点：“最近一周你做了或回避了什么具体的事？”有锚点必须回扣。
- 必须先运行 `scripts/draw.py` 抽牌，禁止凭感觉选牌。输出中必须展示 `seed` 和 `time_factor`。
- 主权归用户：不用“你一定会”；结尾提醒“牌显示的是当下能量，你的选择随时可以改变走向”。
- 反巴纳姆：建议必须具体到时间/动作，避免“注意沟通、保持平衡、相信直觉、一切都会好”。
- 不做医疗、法律、投资买卖、重大人生决定；明确自伤表达时暂停占卜，建议联系当地紧急服务/可信任的人，或中国心理援助热线 400-161-9995。

## 执行

推荐牌阵：`single` 今日/简单问题；`three` 通用/关系/决策；`diamond` 卡住的决策；`moon` 月度周期；`horseshoe` 时间线；`celtic` 复杂局面。位置见 `references/spreads.md`。

抽牌：
```bash
python3 /Users/umu/.agents/skills/tarot/scripts/draw.py --spread three --question "<问题>"
```
复现同一次结果需同时带 `seed` 与 `time_factor`：
```bash
python3 /Users/umu/.agents/skills/tarot/scripts/draw.py --spread three --seed 123 --time-factor night --question "<问题>"
```

## 解读

逐牌选 1-2 个透镜：镜子=当前状态；窗户=盲点/潜意识；门=行动；锚=固定信念。牌义纪律见 `references/cards.md`。

多牌必须做牌间关系：
- 花色/元素分布：3+ 同花色为主导；缺席花色可提示被忽视的能量。
- 大阿卡纳比例：>50% 重大转折；30-50% 命运与选择并存；<30% 日常选择主导，综合解读里要强调主动权。
- 相邻牌标注 `因果/对话/递进/转折`，并给来源：A1 愚人之旅、A2 数字旅程、A3 牌性、B1 对位牌、B2 宫廷牌、B3 数字共振、经典组合。速查见 `references/card-relations.md`、`references/combinations.md`。

综合解读按“起点 -> 张力 -> 转折 -> 出口 -> 回响”。出口必须是本周可执行动作，如“今天 15:00 前发那条消息”。

## 输出

中文，温暖但清醒，emoji 适量：
1. 整体能量概览
2. 牌阵展示：位置、牌名、正逆位、seed、time_factor
3. 逐牌解读：关键词、透镜解读、深层讯息
4. 牌间关系分析（单张跳过）
5. 综合解读：起点、张力、转折、出口、回响
6. 3-4 字能量总结词
7. 开放式问题收尾，把主权交还用户
