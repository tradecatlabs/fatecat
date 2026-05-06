# FateCat Skill 故障排查

## 默认止血动作

如果你还不确定问题属于依赖、入口、配置还是输入，先执行：

```bash
bash scripts/preflight.sh --mode pure --bootstrap --pretty
```

如果你怀疑开发依赖没装全，执行：

```bash
bash scripts/preflight.sh --mode pure --with-dev --pretty
```

## `strict skill 校验失败，提示目录名不匹配`

- 原因：`SKILL.md` frontmatter 里的 `name` 是 `fatecat`，但你把 bundle 导出到了别的 basename，例如 `fatecat-skill-bundle`
- 处理：优先使用 `bash scripts/export-runtime.sh --output-parent /tmp/export-lite --mode lite`，让脚本自动创建 `/tmp/export-lite/fatecat`

## `.venv/bin/pytest` 或 `pip` 仍指向旧路径`

- 原因：仓库被移动过路径，旧虚拟环境脚本残留；单看 `.venv/bin/python` 仍可能“像是活着”
- 处理：执行 `bash scripts/bootstrap.sh --with-dev`，它会重建含旧 shebang 的虚拟环境；然后再跑 `bash scripts/acceptance.sh --with-dev`

## `配置文件不存在`

- 原因：`scripts/project/assets/config/.env` 缺失
- 处理：先复制 `scripts/project/assets/config/.env.example` 或 `scripts/project/assets/config/agent.env.example`

## `未设置 FATE_BOT_TOKEN`

- 原因：你在执行 `delivery` 检查或启动 Bot，但没有配置 token
- 处理：补齐 `scripts/project/assets/config/.env` 后再执行 `bash scripts/preflight.sh --mode delivery --bootstrap --pretty`

## `缺少必需依赖`

- 原因：`scripts/project/assets/vendor/` 下的运行依赖不完整
- 处理：先在仓库根目录完成完整 checkout，不要裁剪 vendor

## `找不到 runtime root`

- 原因：`scripts/project/` 缺失或被误删
- 处理：恢复该目录，或重新从版本库 checkout 当前 skill 仓库

## `导出 bundle 启动后提示缺少虚拟环境`

- 原因：导出脚本会主动排除 `.venv/`
- 处理：进入导出目录后执行 `bash scripts/bootstrap.sh`

## `导出目录里仍然有敏感文件`

- 原因：手工复制绕过了导出脚本
- 处理：删除导出目录，重新使用 `export-runtime.sh`

## `bundle 体积过大`

- 原因：使用了完整导出模式，或 `scripts/project/assets/docs/lifecycle/packs/` 已累积大量历史沉淀
- 处理：优先改用 `bash scripts/export-runtime.sh --output-parent /tmp/export-lite --mode lite`

## `未发现生命周期包`

- 原因：还没有执行 `bash scripts/init-lifecycle-pack.sh --name <slug>`
- 处理：先初始化一个生命周期包，再执行 `lifecycle-status.sh`

## `运维包缺少 health 结果`

- 原因：还没有执行 `bootstrap.sh`，或者 `.venv/bin/fatecat` 已失效
- 处理：先执行 `bash scripts/bootstrap.sh`，再重新运行 `collect-ops-bundle.sh`

## `delivery` 说通过了，但 API/Bot 一启动就挂

- 原因：`health --mode delivery` 只能证明配置和文件存在，不等于启动链路一定可起
- 处理：在真正上线前追加 `bash scripts/delivery-smoke.sh --target api`，或对 Bot 执行 `bash scripts/delivery-smoke.sh --target bot --startup-timeout 8`

## `delivery-smoke` 为什么会临时创建 `.env`

- 原因：项目把 `scripts/project/assets/config/.env` 设为 delivery 硬前提，但本地 smoke 不应该逼你把真实密钥写进仓库
- 处理：脚本会在缺少真实配置时自动生成一份临时 smoke `.env`，用于 delivery preflight 和 API/Bot smoke；脚本结束后自动删除

## `自动救活没有真正启用`

- 原因：当前 skill 只提供 repo 内的健康检查、重启命令和运维证据打包，没有直接替你安装 systemd、supervisor、容器编排或外部告警
- 处理：按 `references/ops-pack.md` 中的边界说明，把仓库内 runbook 接到目标环境的守护体系
