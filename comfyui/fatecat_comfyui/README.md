# FateCat ComfyUI 节点包

FateCat 测算工作台的 ComfyUI 控制面接入包。ComfyUI 只作为只读控制面，
业务计算全部复用 FateCat 现有能力（`fate-core` + `fatecat-delivery`）。

## 节点

| 节点 | 职责 | 输出 |
| --- | --- | --- |
| `FateCatValidate` | 校验出生参数、地区可解析、时间口径归一化 | `title`、`count`、`valid`、`message` |
| `FateCatProduce` | 一键生产 Markdown 报告并落盘 | `run_id`、`markdown_path`、`manifest_path`、`markdown` |
| `FateCatPreview` | 生产前静态命盘简表预览图 | `IMAGE`、`preview_path` |

所有业务参数显式进入 `INPUT_TYPES`，临时覆盖不写回源配置。

## 产物路径

```text
{REPO_ROOT}/infra/runtime/local-state/comfyui/runs/{run_id}/report.md
{REPO_ROOT}/infra/runtime/local-state/comfyui/manifests/{run_id}.json
{REPO_ROOT}/infra/runtime/local-state/comfyui/previews/fatecat-preview-*.png
```

## 运行要求

- 依赖：ComfyUI 0.30.x；FateCat 已以 editable 方式安装到 ComfyUI Python 环境。
- 环境变量 `FATECAT_REPO` 指向 FateCat 仓库根目录（默认自动向上探测）。

## 边界

- 不修改 ComfyUI 核心代码、前端代码、依赖、样式或文件组织。
- 长任务运行在独立线程，生产串行执行，阶段边界检查取消。
- 每次生产生成新的不可变 `run_id`，不覆盖历史产物。
