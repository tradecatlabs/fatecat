---
id: SOP-DATA-SUANZHUN-CRAWL
type: process
status: current
owner: data-governance
route_key: crawl_suanzhun_corpus
route_aliases: ["抓取算准网", "增量更新研究语料", "校验抓取完整性"]
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P30D
---

# 抓取算准网研究语料

## 任务定义
按可恢复、可审计和限速策略增量抓取算准网基础/典籍栏目，生成仅供本地研究的结构化语料。

## 当前状态
抓取器和完整性验证已投用；语料为 research only，版权人工审查前不得进入 canonical 或公开分发。

## 适用场景
初次抓取、断点续跑、资源刷新或已有 corpus 完整性校验。

## 输入要求
输出目录、网络许可；可选外部媒体白名单。不得传通配主机或关闭 URL 安全校验。

## 前置条件
安装 `.[data]`；确认目标站点可访问和抓取用途；磁盘空间足够；无并发 crawler 占用同一 SQLite。

## 默认工具链
`.venv/bin/python scripts/suanzhun-corpus-crawl.py` 和 `tests/regression/test_suanzhun_corpus_crawl.py`。

## 固定路径
默认输出 `infra/runtime/local-state/exports/suanzhun-corpus`；状态真相源 `crawl.sqlite3`；逻辑记录 `records/documents.ndjson`。

## 成熟参数
delay 0.35 秒、timeout 20 秒、max attempts 4、单次最多 10000 页面/资源、页面 10 MiB、资源 50 MiB。

## 分步执行流程
1. 先运行 `--validate-only` 判断可恢复状态。
2. 正常增量运行，不加 `--force-refresh`。
3. 仅资源缺失时用 `--refresh-resources`。
4. 外部媒体需显式 `--allow-external-media --external-media-host <host>`。
5. 完成后再次 validate-only并核对 completeness/hash。

## 幂等与增量策略
`crawl.sqlite3` 驱动断点续跑；已完成页面默认跳过；force refresh 只在来源变化已确认时使用。

## 限速与并发规则
单 crawler、请求间隔至少 0.35 秒；禁止并发翻页和无界下载；尊重 timeout/attempt/size 上限。

## 输出目录
固定 local-state corpus 目录；不得提交 HTML、媒体、SQLite 或正文记录。

## 命名规范
保持抓取器固定目录结构；外部证据以 `completeness.json`、`files.sha256` 和 manifest 为准。

## 质量验收门禁
focused crawler tests、validate-only、页序列 `1..N`、原始详情 href 完整扫描和文件 hash 全部通过。

## 失败处理
HTTP、DNS、size、hash 或安全校验失败时记录队列状态并停止该资源，不跳过为成功。

## 恢复与重试策略
依赖 SQLite 状态续跑；单请求最多 4 次；结构性失败修复 parser/白名单后再运行，不无限重试。

## 安全边界
防 SSRF；外部媒体逐主机白名单；版权未审查不得公开、训练或并入 canonical。

## 临时文件清理
清理未完成临时响应；保留 SQLite 状态以恢复；彻底重建前先备份 completeness/hash。

## 运行记录登记
记录开始/结束、参数、页面/资源成功失败数、延迟、重试、completeness、files hash 和版权状态。

## 明确禁止事项
- 禁止去掉限速和大小上限。
- 禁止用通配外部主机。
- 禁止把抓取完成等同可公开使用。
