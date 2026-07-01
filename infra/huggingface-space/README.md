---
title: FateCat
emoji: 🧭
colorFrom: gray
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
license: mit
short_description: TradeCat Labs FateCat measurement infrastructure workbench.
---

# FateCat Web Markdown Workbench

FateCat 是面向 Agent 与应用开发者的测算基础设施，提供统一的能力协议、可复现计算核心、证据化解释层和多端交付接口。这个 Space 提供免费的 Web 工作台，用于生成服务端 Markdown 测算报告。

## 入口

- Web 工作台：`/web`
- 健康检查：`/health`
- Markdown API：`POST /api/v1/report/markdown`
- 异步报告任务：`POST /api/v1/report/jobs`、`GET /api/v1/report/jobs/{job_id}`
- 免费 AI 分析入口：项目归属块中的 `Gemini Gem` 外链；用户复制 Markdown 报告后自行打开分析。

## 自助部署

普通用户可以在 Hugging Face 页面右上角选择 `Duplicate this Space`，复制到自己的账号或组织下直接使用。想从 GitHub fork 持续更新自己的 Space，可以在 fork 仓库里设置 `HF_TOKEN` secret，然后手动运行 `Deploy Hugging Face Space` workflow。

完整步骤见 GitHub 仓库内的 `docs/deployment/huggingface-space.md`。

## 使用流程

1. 打开 `/web`。
2. 填写出生参数并生成 Markdown 报告。
3. 复制 Markdown 输出。
4. 打开项目归属块中的 `免费 AI 分析入口（Gemini Gem）`。
5. 自行粘贴 Markdown 进行 AI 分析。

FateCat 不会自动把用户输入或报告发送给 Gemini。

## 隐私说明

- 免费公开 Space 默认不保存用户记录：`FATE_RECORDS_ENABLED=0`。
- 免费公开 Space 使用进程内有界任务队列：默认 1 个 worker、最多 20 个等待任务、结果 30 分钟后过期；队列内容不写入数据库。
- Space 重启或结果 TTL 到期后，进程内任务结果会消失。
- 请勿输入真实姓名；建议使用昵称或空白姓名。
- 报告会回显你提交的出生时间和姓名；出生地区只公开北京，非北京地区显示为“已填写（非北京地区已隐藏）”。
- 该 Space 运行在 Hugging Face 托管环境，请不要提交任何敏感身份信息。

## 免责声明

本项目及 AI 分析结果仅供传统文化研究、算法测试与娱乐参考。命理学非精密科学，命运掌握在自己手中。使用者因轻信或误读本程序结果而产生的任何心理、财务及生活决策后果，本项目及开发者概不负责。
