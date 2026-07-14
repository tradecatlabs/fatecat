# AGENTS.md - fate_core kernel

## 目录用途

`fate_core/kernel/` 承载命理核心算法与项目内稳定胶水层；这里是领域计算所有权位置，不承载 HTTP、Bot、Web 或 Markdown 交付逻辑。

## 目录结构

```text
kernel/
├── AGENTS.md
├── __init__.py
├── bone_weight.py
├── bazi_calculator.py
├── ming_gua.py
├── projector.py
└── solar_time.py
```

## 职责边界

- `bazi_calculator.py`：八字 legacy 核心实现的 fate-core 归属位置；复用 `lunar-python`、`bazi-1` 等成熟来源，保持历史字段兼容。
- `bone_weight.py`：以整数“钱”维护版本化称骨权重、闰月策略、输入校验、男女解释边界和构成明细；男女共用计算表，只输出民俗附录数据，不参与核心格局判断。
- `ming_gua.py`：命卦计算；只承载年份、性别到命卦结果的纯函数。
- `solar_time.py`：真太阳时边界；封装 paipan-master Node 脚本调用、JSON 解析和历史简化公式公开函数。
- `projector.py`：按 profile 裁剪结构化结果，不计算命理事实。
- `__init__.py`：保持无副作用包初始化；上层必须显式导入 `bazi_calculator` 或 `projector` 子模块。

## 依赖方向

- 允许依赖 `fate_core.support`、已声明生产依赖和治理登记过的 reference repo。
- 禁止依赖 FastAPI、Telegram Bot、Web HTML、数据库和报告渲染。
- 若仍需读取 delivery 迁移窗口内的辅助模块，必须通过明确迁移计划收敛，不能新增新的 delivery 反向依赖。
