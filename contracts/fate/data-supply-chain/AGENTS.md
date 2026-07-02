# AGENTS.md - contracts/fate/data-supply-chain

## 目录用途

`contracts/fate/data-supply-chain/` 定义 FateCat 数据、典籍、vendor、benchmark 与导出边界的机器契约。这里登记供应链资产的来源、分层、许可状态、运行期资格和验证命令，不保存原始大文件、用户数据或运行态产物。

## 目录结构

```text
contracts/fate/data-supply-chain/
├── AGENTS.md
├── registry.json
└── schemas/
    └── data-supply-chain.schema.json
```

## 职责边界

- `registry.json`：供应链资产注册表，覆盖 raw/canonical/derived/reference/export/runtime 分层。
- `schemas/data-supply-chain.schema.json`：注册表字段、枚举和不变量的轻量契约。
- 本目录只描述资产与政策，不复制书籍全文、vendor 源码或 benchmark 数据。
- 生产运行资格必须由 `productionEligibility`、`licensePolicy` 和 `exportPolicy` 同时约束。

## 依赖方向

- `contracts/fate/data-supply-chain -> domains/fate-analysis/data-products + tools/reference-repos + contracts/fate/evaluations`
- `scripts/data-supply-chain-gate.py -> contracts/fate/data-supply-chain/registry.json`
- 禁止把 `raw/`、外部分发包或未复核资料声明为 production input。
