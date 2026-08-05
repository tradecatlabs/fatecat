---
id: SOP-DATA-CLASSICS-BUILD
type: process
status: current
owner: data-governance
route_key: build_classics_dataset
route_aliases: ["清洗命理典籍", "重建典籍数据集", "验证 classics v3"]
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P60D
---

# 构建典籍派生数据集

## 任务定义
在不修改 canonical TXT 的前提下，将已登记典籍确定性清洗为可追溯 v3 内部数据集并验证完整性。

## 当前状态
内部 validated；canonical、curation policy、source/copyright manifest、cleaner 和 validator 已存在；公开训练许可仍依赖人工审查。

## 适用场景
典籍新增、curation policy 更新、语义分段或重复关系逻辑变更后的派生数据重建。

## 输入要求
canonical 目录、source manifest、copyright review、source-hash 绑定 curation policy 和 dataset contract。

## 前置条件
输入文件 hash 已登记；人工 review 未被自动改写；输出目录可原子替换。

## 默认工具链
`.venv/bin/python scripts/classics-dataset-clean.py`、`--validate-only`、`bash scripts/data-supply-chain-gate.sh`。

## 固定路径
输入 `domains/fate-analysis/data-products/classics/`；contract 位于 `contracts/fate/datasets/`；默认输出 `infra/runtime/local-state/exports/datasets/classics-clean-v3`。

## 成熟参数
`--min-passage-chars 200`、`--max-passage-chars 1200`；默认使用 `curation_policy.json`；验证优先 `--validate-only`。

## 分步执行流程
1. 计算 canonical 聚合 hash 和 policy hash。
2. 先验证现有 v3。
3. 在默认 ignored 输出目录执行完整构建。
4. 再执行 `--validate-only`。
5. 运行 focused tests、data gate并比较确定性 hash。

## 幂等与增量策略
同一 canonical/policy/contract 必须生成相同 artifact-list hash；当前采用确定性全量重建，不做有状态增量写。

## 限速与并发规则
单进程构建，禁止并发写同一输出；复杂度保持 O(total chars + records + document pairs)。

## 输出目录
`infra/runtime/local-state/exports/datasets/classics-clean-v3`，该目录 ignored，不提交派生正文。

## 命名规范
保持 contract 定义的固定文件名；数据集版本 `classics-clean-v3`，不得随意新建 v4。

## 质量验收门禁
classics/data-gate tests、build、validate-only、data supply-chain、确定性复跑、canonical hash 不变和 Quick CI。

## 失败处理
多标题、关系统计漂移、hash 不一致、权限放宽或 canonical 变化立即失败。

## 恢复与重试策略
删除失败的 ignored 输出，从同一输入重建；不得手改派生记录或修改 canonical 迎合 validator。

## 安全边界
版权 pending 内容不得公开训练/分发；cleaner 不代替作者、底本、缺卷和许可人工判断。

## 临时文件清理
失败后删除候选输出和临时索引；canonical TXT、manifest、policy 永不由清理流程改写。

## 运行记录登记
记录 canonical/policy/contract hash、文档/段落/切片数量、review summary、构建时长、RSS 和 gate。

## 明确禁止事项
- 禁止覆盖、删除或校勘 canonical TXT。
- 禁止自动删除重复正文。
- 禁止把派生数据集声明为版权已清。
