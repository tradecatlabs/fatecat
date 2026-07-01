# tools/reference-repos

`tools/reference-repos/` 是 FateCat 的第三方命理与历法参考仓库快照层。这里保存的是供应链证据，不是业务源码目录。

## 目录结构

```text
tools/reference-repos/
├── AGENTS.md
├── README.md
├── vendor_sources.json
├── github/
└── web/
```

## 真相源

`vendor_sources.json` 是 vendor 来源、用途、许可、分发边界和快照 hash 的真相源。

核心字段：

| 字段 | 含义 |
| --- | --- |
| `usageRole` | 当前项目允许的用途：`production_dependency`、`oracle_only`、`evaluation_only`、`reference_only`、`future_candidate` |
| `productionUseAllowed` | 是否允许进入生产运行链路 |
| `licenseStatus` | 许可证状态；生产依赖必须是 `spdx`；`missing_upstream_license` 与 `license_file_unreviewed` 必须人工复核 |
| `distributionAllowed` | 当前快照是否允许随仓库或导出包分发 |
| `auditRequired` | 是否必须人工复核后才能扩大用途 |
| `snapshotSha256` | 快照完整性校验值 |

## 当前边界

| 仓库 | 角色 | 生产链路 |
| --- | --- | --- |
| `lunar-python` | 主历法底座 | 允许；已在 Python 依赖文件显式声明 |
| `bazi-1` | 八字规则与资料参考 | 不允许作为新增生产依赖扩散；缺少上游 LICENSE |
| `sxwnl` | 节气/历法离线 oracle | 不进入主生产链；缺少上游 LICENSE |
| `bazica` | Go 八字排盘 oracle | 不进入 Python 主链 |
| `bazi-calculator-by-alvamind` | TypeScript 基础结构参考 | 不进入生产链；本地快照无独立 LICENSE 文件 |
| `MingLi-Bench` | 离线评测基准 | 不进入请求链路，不默认调用模型 API runner |
| `iztro` / `dantalion` | 未来候选能力 | 启用前必须重新完成架构、许可和验收 |
| 玄学 Skills collection | 参考/候选能力 | 不进入生产链路；只用于 capability 设计、交互流程和算法候选对照 |
| `legacyUnreviewedSnapshots` | 历史未审快照 | 只保留供应链证据；不得进入生产、公开分发或新增功能依据 |

## 玄学 Skills collection

2026-07-01 拉取并登记以下 GitHub 快照，全部位于 `tools/reference-repos/github/`，并已写入 `vendor_sources.json`：

| ID | 路径 | 用途 | 当前边界 |
| --- | --- | --- | --- |
| `Numerologist_skills` | `github/Numerologist_skills-main` | 奇门遁甲、紫微斗数 Skill 流程参考 | 缺 LICENSE，仅参考 |
| `mingyu` | `github/mingyu-main` | 八字、紫微、奇门、六爻、梅花、大六壬综合接口候选 | MIT，未来候选 |
| `bazi-skill-jinchenma94` | `github/bazi-skill-jinchenma94-main` | 对话式八字 Skill 工作流参考 | MIT，仅参考 |
| `bazi-skill-gaoxin492` | `github/bazi-skill-gaoxin492-main` | 长期命盘存档和复盘参考 | 缺 LICENSE，仅参考 |
| `horosa-skill` | `github/horosa-skill-main` | 本地离线术数能力层候选 | AGPL，需复核 |
| `yinyuan-skills` | `github/yinyuan-skills-main` | 姻缘、合婚、生肖配对、求签参考 | 缺 LICENSE，仅参考 |
| `Master-skill` | `github/Master-skill-main` | 佛学和文化典籍 Skill 参考 | MIT，仅参考 |
| `fengshui.skill` | `github/fengshui.skill-main` | 风水、阳宅、空间类 capability 参考 | 缺 LICENSE，仅参考 |
| `cyber-fortune-telling` | `github/cyber-fortune-telling-main` | 每日运势、娱乐应用形态参考 | 缺 LICENSE，仅参考 |
| `tarot-skill` | `github/tarot-skill-main` | 塔罗抽牌和牌阵 Skill 参考 | 缺 LICENSE，仅参考 |
| `taibu` | `github/taibu-master` | 六爻、梅花、周易综合引擎候选 | AGPL/自定义边界，已剔除 node_modules |
| `meihua-yishu` | `github/meihua-yishu-main` | 梅花易数体系 Skill 参考 | CC-BY-NC-SA，已剔除 venv |
| `meihua-divination` | `github/meihua-divination-main` | 梅花易数结构化表达对照 | 缺 LICENSE，仅参考 |
| `ZhouYiLab` | `github/ZhouYiLab-main` | 周易综合计算引擎候选 | MIT，未来候选 |

## 维护规则

1. 不在 `tools/reference-repos/github/*` 内魔改第三方源码。
2. 新增快照必须登记到 `vendor_sources.json`，并补齐来源、用途、许可、hash 和风险说明。
3. 已评估候选放入 `optionalFutureFeatures`；来源、许可或价值未复核的历史目录放入 `legacyUnreviewedSnapshots`。
4. 缺少独立 LICENSE、许可证未复核或 `licenseStatus=missing_upstream_license` / `license_file_unreviewed` 的材料不得标为 `production_dependency`。
5. Benchmark 类仓库只作为离线评测资产，不默认调用外部模型、云 API 或生产服务。
6. `tools/reference-repos/` 不允许残留 `.git`、`node_modules`、虚拟环境、pycache、`.DS_Store`、日志、数据库或断链 symlink。
7. 清理运行态污染后再更新 manifest：

```bash
bash scripts/clean-runtime.sh
```

8. 更新 manifest 后运行：

```bash
bash scripts/vendor-health.sh
python3 -m pytest -q tests/regression/test_fate_policy_assets.py
```

## 使用方式

服务代码只能通过 adapter、manifest 或明确的路径常量读取这里的资产。新增生产依赖必须优先走包管理器声明，并用测试证明不会隐式依赖 vendor 快照。

Ponytail evidence：existence 来自离线 smoke、oracle 对照和 license manifest；owner 是 tradecatlabs/fate-core supply-chain boundary；verification 是 `bash scripts/vendor-health.sh`；ceiling 是生产依赖优先进入包管理器，vendor 快照不作为通用代码仓。
