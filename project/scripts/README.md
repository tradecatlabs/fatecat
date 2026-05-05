# Scripts Directory

本目录是原项目级工具区。生产入口已经收敛到 skill 根目录的 `scripts/`：

- 安装与验收：在 skill 根目录运行 `bash scripts/bootstrap.sh --with-dev`、`bash scripts/acceptance.sh --with-dev`
- API / Bot 启动：在 skill 根目录运行 `bash scripts/serve-api.sh`、`bash scripts/serve-bot.sh`
- 项目级 `setup/` 脚本仅保留兼容用途，必须通过 `pyproject.toml` 生成的 `fatecat` CLI 入口执行，不再直接绕到 `modules/telegram/start.py`
- `download_libs.sh` 会写入 vendor 研究素材，默认禁止执行；只有显式设置 `FATECAT_ALLOW_VENDOR_DOWNLOAD=1` 才会下载

## 📁 目录结构

### 📊 reports/
报告生成脚本
- `generate_complete_output.py` - 兼容输出测试脚本
- `generate_full_report.py` - legacy 字段报告生成器
- `generate_user_report.py` - 用户友好的排版报告生成器
- `扩展功能具体内容.py` - 扩展功能具体内容展示

### 🔧 setup/
环境配置脚本
- `setup_external_env.sh` - 可选外部环境依赖安装脚本；只安装/构建已存在的 vendor 项目，不生成替代源码
- `bootstrap_fatecat.sh` - 项目级兼容自举脚本；按 `pyproject.toml` 安装 `fatecat` CLI 后启动模块

### 🧰 compatibility
兼容脚本
- `generate_bazi.sh` - 通过 `fatecat pure-analysis` 生成 JSON
- `test_all.sh` - 运行项目根测试与 Telegram 模块测试
- `build_all.sh` - 验证 `fatecat` CLI，并在存在 Dockerfile 时构建镜像
- `deploy.sh` - 仅在存在真实 Kubernetes manifests 时部署；否则明确失败，避免伪上线
- `start_all.sh` - 通过 `fatecat serve both` 后台启动 Bot + API

## 🚀 使用方法

### 生成报告
```bash
cd scripts/reports
python3 generate_user_report.py
```

### 配置环境
```bash
cd scripts/setup
chmod +x setup_external_env.sh
./setup_external_env.sh

chmod +x bootstrap_fatecat.sh
./bootstrap_fatecat.sh deps
```
