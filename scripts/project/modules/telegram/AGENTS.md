# AGENTS.md - telegram

## 目录用途

`modules/telegram/` 是 FateCat 的交付层：负责 Telegram Bot、FastAPI、Web HTML 报告页、标准 Markdown 报告生成与遗留计算装配。

## 目录结构

```text
telegram/
├── AGENTS.md
├── scripts/
├── src/
│   ├── _paths.py
│   ├── bot.py
│   ├── main.py
│   ├── web_ui.py
│   ├── prediction_systems.py
│   ├── report_generator.py
│   ├── bazi_calculator.py
│   ├── db_v2.py
│   └── *_integration.py
├── start.py
└── tests/
```

## 职责边界

- `src/main.py`：FastAPI 入口，只挂载 API / Web 路由并维持响应模型。
- `src/web_ui.py`：原生 HTML Web 报告页，只负责输入表单、字段校验、Markdown 呈现与复制增强。
- `src/prediction_systems.py`：预测体系注册表，区分当前可用体系与未来待实现体系。
- `src/bot.py`：Telegram Bot 交互流程与文件交付。
- `src/report_generator.py`：标准 Markdown 报告结构真相源。
- `src/bazi_calculator.py`：遗留排盘能力总装配器；新增字段契约优先进入 `fate_core`。
- `src/*_integration.py`：外部成熟库胶水层，禁止在这里重造底层算法。

## 依赖方向

- `main.py -> web_ui.py + prediction_systems.py + bazi_calculator.py + report_generator.py + location.py`
- `bot.py -> prediction_systems.py + bazi_calculator.py + report_generator.py`
- `telegram -> modules/fate_core + assets/* + runtime/*`
- 禁止 `modules/fate_core` 反向依赖 `telegram`
