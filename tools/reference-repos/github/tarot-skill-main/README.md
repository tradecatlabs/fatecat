# 🔮 Tarot Skill

AI 塔罗占卜 Agent Skill，为 Cursor / Claude Code / OpenClaw 等 AI agent 提供专业级塔罗解读能力。

## 特性

- **78 张完整牌义**：韦特 + 托特 + 现代心理塔罗三大系统融合，每张大阿卡纳含心理原型与托特视角
- **6 种牌阵**：单张 / 三牌阵 / 五牌阵 / 月亮牌阵 / 马蹄形 / 凯尔特十字
- **牌间关系理论体系**：愚人之旅 / 数字旅程 / 牌性（Elemental Dignities）/ 对位牌 / 宫廷牌关系网 / 生命之树，覆盖所有可能的牌对组合
- **真随机抽牌脚本**：Python 脚本 `scripts/draw.py`，密码学安全随机源，位置权重、时段因子、正逆位概率全内置
- **解读方法论**：四维透镜模型 / 牌间关系推理 / 叙事弧串联 / 反巴纳姆检验
- **语言约束与安全边界**：禁用巴纳姆废话清单、自伤信号处理协议

## 文件结构

```
SKILL.md                        # 主技能文档（工作流 + 解读方法论 + 输出格式）
references/
  cards.md                      # 78 张牌义（~1100 行）
  card-relations.md             # 牌间关系理论体系（6 套理论 / 2 层架构）
  combinations.md               # 经典牌间组合 + 花色集中/密度规则
  spreads.md                    # 6 种牌阵布局与解读顺序
scripts/
  draw.py                       # 真随机抽牌脚本（Python 3）
```

## 快速使用

### 作为 Agent Skill 安装

将本仓库内容放入 agent 的 skills 目录：

```bash
# Cursor
cp -r . ~/.cursor/skills/tarot/

# Claude Code
cp -r . ~/.claude/skills/tarot/

# OpenClaw agents
cp -r . ~/.agents/skills/tarot/
```

### 抽牌脚本

```bash
# 单张今日指引
python3 scripts/draw.py --spread single

# 三牌阵 + 问题
python3 scripts/draw.py --spread three --question "事业方向"

# 凯尔特十字
python3 scripts/draw.py --spread celtic --question "感情"

# 指定种子复现
python3 scripts/draw.py --spread three --question "事业" --seed 42
```

## 许可

MIT
