# 月老 · 姻缘测算 Skills

> Claude Code 姻缘测算技能 —— 赛博月老，用中华传统术数帮你算姻缘

## 功能概览

六大测算模式，覆盖各种感情需求：

| 模式 | 命令 | 说明 | 需要的信息 |
|------|------|------|-----------|
| 八字合婚 | `/yinyuan` 选1 | 看两个人的八字配不配 | 双方出生日期+时间+性别 |
| 生肖配对 | `/yinyuan` 选2 | 用生肖看合不合 | 双方生肖或出生年份 |
| 紫微夫妻宫 | `/yinyuan` 选3 | 看命盘里的婚姻格局 | 出生日期+时间+性别 |
| 求签问姻缘 | `/yinyuan` 选4 | 抽一支姻缘签 | 想问的问题 |
| 桃花运势 | `/yinyuan` 选5 | 看近期的感情运势 | 生肖+当前感情状态 |
| 红线测算 | `/yinyuan` 选6 | 综合分析正缘特征和时间 | 出生日期+时间+你的期待 |

## 设计理念

**不再依赖 AI 玄学幻觉**，而是通过严格的 Prompt 约束 + 结构化知识库 (References) 的架构方式，让姻缘测算过程透明可控、有据可依。

核心原则：
- 娱乐为主，理性参考
- 不说宿命，不制造焦虑
- 先问清需求再测算
- 有据可依的传统文化知识

## 文件结构

```
yinyuan-skills/
├── SKILL.md                          # 主技能文件
├── README.md                         # 本文件
└── references/                       # 知识参考库
    ├── bazi-matching.md              # 八字合婚规则
    ├── zodiac-compatibility.md       # 生肖配对表
    ├── ziwei-marriage.md             # 紫微夫妻宫解读
    ├── fortune-sticks.md             # 100签姻缘签诗系统
    └── taohua-luck.md                # 桃花运势体系
```

## 使用方式

在 Claude Code 中加载 SKILL.md 后，直接说：

- "帮我测姻缘"
- "我和XX配不配"
- "什么时候能遇到对的人"
- "求一支姻缘签"
- "看看我最近的桃花"

或者直接 `/yinyuan` 进入选择界面。

## 致谢

灵感来源：
- [colleague-skill](https://github.com/titanwings/colleague-skill) — 多模式交互架构
- [boss-skill](https://github.com/nicepkg/boss-skill) — 趣味化产品设计
- [Numerologist_skills](https://github.com/FANzR-arch/Numerologist_skills) — 术数工程化方法论

---

*姻缘天注定，幸福自己争。祝各位早日觅得良缘！*
