# meihua-divination

一个给 **OpenClaw** 用的中式玄学风 skill：参考 **梅花易数 / 象数 / 五行生克** 的思路，做成一个 **可复现、可解释、偏趋势分析** 的结构化断事工具。

它不是“想到哪断到哪”的玄学文案机，也不是完整古法排盘器。
它更像一个：

> **带中式玄学气质的、稳定输出的、适合 AI 使用的断事骨架。**

适合的问题类型：

- 事业 / 项目 / 决策
- 关系解读
- 当前运势 / 阶段气运
- 人设 / 性格 / 天赋倾向

仓库地址：<https://github.com/qiyan233/meihua-divination>

---

## 为什么做这个 skill

很多“玄学风” prompt 或 fortune-telling agent 都有两个常见问题：

1. **只有味道，没有骨架**：句子很像那么回事，但每次说法都飘。
2. **只有术语，没有落点**：一堆生克、动静、体用名词，最后却很难给出稳定可用的判断。

`meihua-divination` 想解决的是这两件事：

- 保留中式玄学语言的气质
- 但底层使用稳定、可复查的推理结构

它当前的定位不是“复刻古法全套梅花易数”，而是：

> **把适合 AI 使用的梅花易数式断事原则，蒸馏成一套能稳定工作的 skill。**

---

## 这个 skill 在做什么

核心工作流是：

1. 从用户问题里提取最小必要上下文
2. 用文本生成一个稳定 seed
3. 由 seed cast 出五个象位：
   - 主象
   - 客象
   - 阻象
   - 变象
   - 应象
4. 结合：
   - 五行生克
   - 动静
   - 强弱
   - 顺逆
5. 渲染成结构化阅读结果：
   - 总断
   - 断因
   - 断势
   - 断法
   - 签语

在深度模式里，还会体现：

- 近势 / 中势 / 后势
- 动静带来的显化快慢
- 主客阻变应之间的关系

---

## 设计取向

### 1. 中式玄学风，但底层讲逻辑

表层语言可以有“势、机、象、气、阻、应、生克、动静”的味道，
但底层不靠随机发散，而是靠稳定象位结构和规则。

### 2. 同一输入，尽量同一骨架

只要输入相同或接近，就应该得到接近的核心象位，而不是每次重新胡编一套。

### 3. 趋势分析，不做绝对神断

这个 skill 更适合：

- 看结构
- 看阻滞
- 看节奏
- 看后势
- 给应对建议

不适合：

- 精确预测某一天一定发生什么
- 生死、重病、官非定案
- 投资暴富承诺
- 赌博、诅咒、报复、暴力导向

### 4. 不做“完整古法排盘器”

本 skill **受梅花易数启发**，吸收了：

- 体为主，用为事
- 用为近应，互为中程，变为后势
- 不动不占，不因事不占
- 吉凶悔吝生乎动

但它没有实现：

- 全套起卦法
- 严格传统卦爻计算
- 完整旺衰时令体系
- 精确应期算法

这是有意为之。
目标不是复刻古法全貌，而是做一个 **现代 AI 可稳定调用的结构化 skill**。

---

## 适用环境

- OpenClaw
- 其他支持 Agent Skills / Skill-like workflow 的 AI 环境
- 本地脚本实验与 prompt workflow 研究

---

## 安装方式

### OpenClaw

把仓库克隆到你的 skills 目录，例如：

```bash
git clone https://github.com/qiyan233/meihua-divination.git ~/.openclaw/skills/meihua-divination
```

OpenClaw 会在任务匹配时读取其中的 `SKILL.md`。

如果你喜欢手动引用，也可以让 agent 在需要时直接读取：

- `SKILL.md`
- `references/*.md`
- `scripts/*.py`

### 本地实验

直接在仓库根目录运行 Python 脚本即可：

```bash
python3 scripts/generate_reading_seed.py --help
python3 scripts/cast_symbols.py --help
python3 scripts/render_reading.py --help
```

---

## 仓库结构

```text
meihua-divination/
├── SKILL.md
├── scripts/
│   ├── generate_reading_seed.py
│   ├── cast_symbols.py
│   ├── render_reading.py
│   └── smoke_test.sh
├── references/
│   ├── question-types.md
│   ├── symbol-system.md
│   ├── element-relations.md
│   ├── reasoning-patterns.md
│   ├── scenario-patterns.md
│   ├── traditional-meihua-notes.md
│   ├── output-style.md
│   ├── signature-lines.md
│   ├── examples.md
│   └── safety-boundaries.md
└── assets/
    ├── phrase-library.json
    └── templates/
```

---

## 核心文件说明

### `SKILL.md`
主入口。定义：

- skill 触发描述
- 工作流
- 输出结构
- 安全边界
- 资源地图

### `scripts/generate_reading_seed.py`
把：

- mode
- question
- context
- date

变成一个稳定 seed。

### `scripts/cast_symbols.py`
根据 seed 生成五个象位，并加入 mode bias：

- `career`
- `relationship`
- `fortune`
- `personality`
- `general`

### `scripts/render_reading.py`
核心渲染器。负责把：

- 问题
- 上下文
- 象位
- 生克关系
- 阶段走势

转成中文阅读结果。

### `scripts/smoke_test.sh`
快速回归测试脚本。每次改逻辑或改文风后，先跑它看结果有没有明显崩掉。

### `references/reasoning-patterns.md`
核心断事逻辑，包含：

- 主客阻变应怎么读
- 近势 / 中势 / 后势怎么拆
- 生克不要机械背表
- 动静怎么看显化快慢

### `references/scenario-patterns.md`
高频真实问题的场景化规则库，比如：

- 辞职单干
- 合作接单
- 项目卡住
- 主动联系
- 暧昧推进
- 复合
- 最近不顺
- 自耗型人格

### `assets/phrase-library.json`
中文断语词库。控制：

- 总断
- 断势
- 断法
- 风险提醒
- 签语

---

## 快速上手

### 1）生成稳定 seed

```bash
python3 scripts/generate_reading_seed.py \
  --mode career \
  --question '我要不要辞职做自己的项目' \
  --context '现在工作稳定但很消耗，手里有一个想做半年的产品方向，还没验证过付费。' \
  --date '2026-03-16'
```

示例输出：

```text
c0161ff9a8949369
```

### 2）查看 cast 出来的象位

```bash
python3 scripts/cast_symbols.py \
  --seed c0161ff9a8949369 \
  --mode career \
  --json
```

### 3）直接渲染完整阅读结果

```bash
python3 scripts/render_reading.py \
  --mode career \
  --question '我要不要辞职做自己的项目' \
  --context '现在工作稳定但很消耗，手里有一个想做半年的产品方向，还没验证过付费。' \
  --date '2026-03-16' \
  --style standard
```

支持三种风格：

- `quick`
- `standard`
- `deep`

例如：

```bash
python3 scripts/render_reading.py \
  --mode relationship \
  --question '我该不该主动联系他' \
  --context '之前聊得不错，但最近冷下来了。我怕不联系就断掉，联系又怕显得太主动。' \
  --date '2026-03-16' \
  --style deep
```

---

## 一条典型输出长什么样

典型结构：

- 总断
- 断因
- 断势
- 断法
- 签语

深度模式还会带：

- 问题归类
- 主象 / 客象 / 阻象 / 变象 / 应象
- 生克与动静
- 近势 / 中势 / 后势
- 显化快慢

它不是追求“神秘到看不懂”，而是追求：

> **有玄学味，但不胡；有判断感，但不飘。**

---

## 当前支持的问题模式

### 事业 / 项目 / 决策
例子：

- 我要不要辞职单干
- 这个合作该不该接
- 这个项目是不是方向错了

### 关系解读
例子：

- 我该不该主动联系他
- 这段关系还能不能推进
- 我和前任还有没有续头

### 当前运势 / 阶段气运
例子：

- 为什么最近总觉得不顺
- 这个月适不适合做大动作
- 最近是不是该先收口

### 人设 / 性格 / 天赋倾向
例子：

- 我适合什么路子
- 我是不是容易自耗
- 我这种人适合什么节奏

---

## 已吸收的传统原则

这个 skill 当前明确吸收并改写了这些原则：

- **体为主，用为事**
- **用为近应，互为中程，变为后势**
- **不动不占，不因事不占**
- **吉凶悔吝生乎动**

在具体实现里，它们被改写成：

- 主象 ≈ 体
- 客象 ≈ 用 / 近势
- 阻象 ≈ 中程卡点（现代扩展）
- 变象 ≈ 后势
- 应象 ≈ 更合适的应法

---

## 安全边界

本 skill 不做绝对结论，尤其避免：

- 死亡 / 寿命判断
- 重病诊断
- 法律有罪无罪断言
- 保证投资收益
- 赌博结果
- 诅咒 / 报复 / 暴力导向建议

如果用户问的是高风险问题，应该退回到：

- 情势解读
- 风险提醒
- 情绪状态
- 实际建议

而不是假装自己在“代天断命”。

---

## 测试

跑 smoke test：

```bash
bash scripts/smoke_test.sh
```

它会快速检查四个核心模式：

- career
- relationship
- fortune
- personality

如果你改了：

- 断语库
- 场景规则
- render 逻辑
- mode bias

建议先跑一遍再提交。

---

## Roadmap

如果你想把这个 skill 继续做成真正的“精品”，后面的高价值方向包括：

### 1. 补更多 worked examples
按模式补 12～20 个高质量案例。

### 2. 补更细的场景规则
例如：

- 合作谈判
- 断复合但设边界
- 是否适合搬家 / 换城市
- 内容创作瓶颈
- 创业者节奏失衡

### 3. 继续加强 renderer
例如：

- 更细的近 / 中 / 后势语料
- 更强的 mode-specific 判断
- 更像中文断事的句法层

### 4. 做 release / package
把它打包成 `.skill` 分发文件。

---

## English TL;DR

`meihua-divination` is an OpenClaw skill for Chinese-style symbolic readings inspired by **Meihua Yishu**.
It is designed to be:

- deterministic
- explainable
- trend-oriented
- safe for AI-assisted divination-style outputs

It does **not** try to be a full traditional hexagram engine.
Instead, it adapts a few stable principles into a structured workflow for:

- career / project decisions
- relationship readings
- current fortune / phase analysis
- personality / tendency readings

---

## License

暂未声明。若准备长期公开分发，建议补一个明确 license。
