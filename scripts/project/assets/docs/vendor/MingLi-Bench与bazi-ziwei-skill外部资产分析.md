# MingLi-Bench 与 bazi-ziwei skill 外部资产分析

## 来源

| 资产 | 本地位置 | 来源 | 当前用途 |
| --- | --- | --- | --- |
| MingLi-Bench | `scripts/project/assets/vendor/github/MingLi-Bench-main` | https://github.com/DestinyLinker/MingLi-Bench | 命理 LLM 推理评测基准 |
| bazi-ziwei-mingli-skill-v8.5.zip | `scripts/project/assets/data/classics/raw/bazi-ziwei-mingli-skill-v8.5.zip` | https://drive.google.com/file/d/1Hp42pDlI-o-DpbfeVI04YfDjnkDa319Z/view?usp=sharing | 外部分发包来源归档与方法论参考 |

## MingLi-Bench 盘点

- 许可：MIT。
- 快照：`dd45b4d45516dfb657fce8c56d03f9653cc33dfc`。
- 资产体量：129 个快照文件，快照哈希 `72a96b6edcee068ec9d93c9c306ae2e78bc611509fd5f8c8fae12d7469ed6c8f`。
- 数据：`data/data.json` 含 160 道标准化选择题，`data/fortune_api_results.json` 含 32 个预计算八字/紫微盘。
- 能力：支持 OpenAI、OpenRouter、Anthropic、Google、DeepSeek、豆包等模型 API；可按年份、类别、样本量、选项打乱和是否注入预排盘执行评测。
- 本地验证：`PYTHONPATH=. python3 -m mingli_bench.cli --stats` 可正常读取数据，统计年份为 2022-2025。

## bazi-ziwei skill zip 盘点

- 许可：包内 `LICENSE` 为 MIT，但包内典籍、PDF、电子书、知识图谱和案例资料仍需逐项版权与来源复核。
- 压缩包：62186087 bytes，sha256 `25f54a5a67c6cfa079848741c4ba227de40da59e733404f2db4631f31b213ac8`。
- 解压体量：62 个文件，约 115985448 bytes。
- 内容：`books/`、`core/`、`cases/`、`lightrag/merged.json`、`scripts/`、安装文档与伦理说明。
- 知识图谱：`lightrag/merged.json` 含 45895 个 entities 与 108184 个 relationships。
- 分发边界：当前只作为 raw 来源归档，不进入 Git 与 skill 导出包，业务代码不得直接依赖。

## 风险与边界

- MingLi-Bench 含公开 benchmark 的出生信息与预计算命盘，只能作为评测输入，不得作为前端示例或用户默认展示内容。
- Drive zip 声称部分典籍为公共领域、部分为原创笔记，但该说法仍需人工版权复核；在复核前不得晋升为发布资产。
- Drive zip 内 setup 脚本会创建本地 skill 链接，Level 2 会调用外部 LLM API 和 `knowledge-mcp`，当前不得在生产环境自动执行。
- 敏感信息扫描仅发现 API key 变量名、代码参数和占位符 `LLM_API_KEY=sk-your-openai-key-here`，未发现真实密钥；静态站点压缩 JS 存在误报，需要按文件类型过滤。

## 后续建议

- 将 MingLi-Bench 包装成 FateCat 的离线 benchmark runner，先做本地 dry-run 和 prompt 生成测试，再接真实 API。
- 对 Drive zip 的 `core/` 方法论笔记进行人工复核后，提炼为小型结构化规则，不直接复制大段文本进入生产输出。
- 对 `books/` 与 `lightrag/merged.json` 建立版权状态表，只有通过复核的条目才能进入可发布检索资产。
- 所有示例输入继续遵守前端隐私规则，不在用户界面展示非北京真实地区。
