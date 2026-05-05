# FateCat Skill 执行手册

## 目标

把 FateCat 的标准操作收敛成一条稳定、可复用、低分叉的执行链路：

1. 先修好运行时
2. 再做模式检查
3. 再验输入
4. 最后执行排盘或启动交付层

优先使用统一入口：

```bash
bash scripts/preflight.sh --mode pure --bootstrap --pretty
```

## 标准顺序

### 场景 A：只做纯命理排盘并输出文件

```bash
bash scripts/preflight.sh --mode pure --bootstrap --pretty
mkdir -p output
bash scripts/pure-analysis.sh --input-file input.json --output-file output/result.json --pretty
```

验收：
- `preflight` 成功结束
- `output/result.json` 存在
- 输出 JSON 可读取

### 场景 B：需要先证明环境可跑，再留一份样例输出

```bash
bash scripts/preflight.sh \
  --mode pure \
  --bootstrap \
  --smoke \
  --output-file output/preflight-sample.json \
  --pretty
```

验收：
- `health` 成功
- 自动生成一份样例 JSON
- 后续 agent 可直接复用这份路径和结构做进一步验证

### 场景 C：准备启动 API 或 Bot

```bash
bash scripts/preflight.sh --mode delivery --bootstrap --pretty
bash scripts/delivery-smoke.sh --target api
bash scripts/serve-api.sh
```

或：

```bash
bash scripts/preflight.sh --mode delivery --bootstrap --pretty
bash scripts/delivery-smoke.sh --target bot --startup-timeout 8
bash scripts/serve-bot.sh
```

验收：
- `delivery` 模式健康检查通过
- 入口命令启动时不再卡在缺依赖或缺配置
- API smoke 通过 `/health` 探测
- Bot smoke 至少通过 dry-run 装配验证
- 发布前总验收使用 `bash scripts/acceptance.sh --with-dev`，默认同时覆盖 API 与 Bot dry-run

## 决策规则

### 什么时候用 `bootstrap.sh`

- 首次接手仓库
- `.venv/bin/fatecat` 不存在
- `.venv/bin/fatecat` 指向旧路径
- `.venv/bin/pytest`、`pip` 等入口仍指向旧路径
- 需要补装 `dev` 依赖

### 什么时候直接用 `preflight.sh`

- 绝大多数日常执行前
- 你不想手工拆成 `bootstrap + health`
- 你要留下前置检查证据

### 什么时候加 `--smoke`

- 你要证明“不是只会检查，而是真的能产出结果”
- 你要在交接、上线前、排障后补一份样例输出

### 什么时候只做 `health`

- 你明确不想生成样例文件
- 你当前只想判断 pure / delivery 是否具备下一步条件
- 你还没准备做 API/Bot 的真实启动验证

## 输入策略

### 推荐

- 有标准请求时：优先 `--input-file`
- 临时试跑时：可以 `--input-json`
- 不给输入但要做烟雾验证时：允许 `preflight.sh --smoke` 使用内置样例

### 不推荐

- 用户没给经纬度就直接执行纯分析
- 交付层未配置 `.env` 就宣称“可生产”
- 只跑 `--help` 就认定环境已准备完成

## 常见失败切面

### `fatecat` 入口失效

处理：

```bash
bash scripts/preflight.sh --mode pure --bootstrap --pretty
```

### `.venv/bin/pytest` 指向旧路径

处理：

```bash
bash scripts/bootstrap.sh --with-dev
bash scripts/acceptance.sh --with-dev
```

### 纯分析缺字段

处理：
- 回到输入验收阶段
- 确认 `birthDateTime`、`gender`、`longitude`、`latitude`

### delivery 检查失败

处理：
- 检查 `project/assets/config/.env`
- 补齐交付层依赖后重新执行 `preflight.sh --mode delivery`

## 推荐输出证据

至少保留其一：
- `preflight` 的标准输出
- 一份 `output/*.json` 样例文件
- `health --json --pretty` 的结果文件

## 结论

如果 agent 想提高复用、稳定和效率，默认动作应该是：

```bash
bash scripts/preflight.sh --mode pure --bootstrap --pretty
```

然后再进入真正的任务执行。这样比每次手动拼接 `bootstrap`、`health`、`pure-analysis` 更稳定，也更容易交接。 
