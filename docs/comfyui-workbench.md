# FateCat ComfyUI 节点流工作台

## 定位

ComfyUI 是 FateCat 本地测算工作的正式前端与编排入口（运行于 WSL2，端口 8189）。
现有 FastAPI Web 工作台（`/web`）保留为公开轻量入口（HF Space），不承载新功能扩展。

通用迁移蓝图见 pdf 项目 `docs/comfyui-migration-blueprint.md`，标准作业流程见
`docs/sop/comfyui-frontend-migration.md`。

本方案只使用 ComfyUI 官方允许的扩展和数据接口：

- `custom_nodes/` 下的自定义 Python 节点。
- 保存到仓库的 Workflow JSON。
- ComfyUI App Mode 配置（`extra.linearMode` / `extra.linearData`）。

不修改 ComfyUI 核心代码、前端代码、依赖、样式或文件组织。

## 节点

### FateCatValidate

校验出生参数：字段完整性、出生地区可解析、时间口径归一化。

输入（与 Web 表单契约一致）：

- `birth_date`、`birth_time`、`birth_place`、`location_id`（候选 ID，可空）
- `gender`（male/female）、`report_system`（bazi/ziwei）、`name`（可空）
- `time_basis`（beijing_time/local_civil/utc）、`fold_choice`（空/earlier/later）

输出：

- `title`（姓名或"未命名命主"）
- `count`（当前可用报告体系数）
- `valid`（布尔）
- `message`（校验结果）

### FateCatProduce

一键生产 Markdown 报告并落盘。复用 `web_report_service.build_web_report_result`，
不重新实现命理算法。长任务运行在独立线程，按阶段上报进度；可在 ComfyUI 中取消，
取消后 history 记录 `execution_interrupted`。

输出：

- `run_id`（每次生产生成新的不可变 run id）
- `markdown_path`、`manifest_path`
- `markdown`（完整 Markdown 文本，可连接内置 `SaveText` 展示）

### FateCatPreview

生产前静态命盘简表预览图（四柱/紫微十二宫），输出 `IMAGE` 与 `preview_path`，
不写入正式 runs 目录。

## 部署

```bash
bash scripts/setup_comfyui_wsl.sh /home/lenovo/.projects/cat/fatecat
```

脚本只做三件事：

1. 把 `comfyui/fatecat_comfyui` 复制到 ComfyUI 的 `custom_nodes/fatecat_comfyui`。
2. 把三个 Workflow JSON 复制到 `user/default/workflows/`。
3. 把 FateCat 以 editable 方式安装进 ComfyUI 的 Python 环境。

启动（WSL2，端口 8189，独立数据库避免与 8188 的 pdf 实例冲突）：

```bash
export FATECAT_REPO=/home/lenovo/.projects/cat/fatecat
cd /home/lenovo/projects/ComfyUI/ComfyUI
setsid nohup ../.venv/bin/python main.py --listen 127.0.0.1 --port 8189 \
  --database-url /home/lenovo/projects/ComfyUI/ComfyUI/user/fatecat-comfyui.db \
  > /home/lenovo/fatecat-comfyui.log 2>&1 < /dev/null &
```

浏览器打开 `http://127.0.0.1:8189` 即可使用 App Mode 参数面板。

## 生产路径

```text
infra/runtime/local-state/comfyui/runs/{run_id}/report.md
infra/runtime/local-state/comfyui/manifests/{run_id}.json
infra/runtime/local-state/comfyui/previews/fatecat-preview-*.png
```

仓库提供三个 Workflow 模板：

- `comfyui/workflows/fatecat_production.json`：一键生产并保存 Markdown 与 manifest 路径。
- `comfyui/workflows/fatecat_validate.json`：仅校验出生参数。
- `comfyui/workflows/fatecat_preview.json`：生产前静态命盘简表预览。

## HF Space 边界

HF 免费 Space（docker sdk，单端口 7860）暂不内嵌 ComfyUI：

- ComfyUI 前端不支持子路径挂载（无 base path 配置，asset/WebSocket 相对路径），
  在 HF 的 `/comfy/*` 代理下不可靠。
- CPU torch 依赖会使免费 Space 镜像接近构建上限。
- 官方 ComfyUI Space 模板为固定 UI，无法挂载 FateCat 业务节点。

因此 HF Space 继续运行 FastAPI `/web` 作为公开轻量入口（legacy），
ComfyUI 承载本地正式生产控制面。

## 冲突规则

如果 ComfyUI 的现有扩展接口、Workflow 或 App Mode 无法承载某项需求，
不修改 ComfyUI 框架，而是停止并报告冲突。
