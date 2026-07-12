# 地点与时区基础设施审查

## 结论

- 任务范围：PASS
- 未处理 BLOCK：0
- 外部连通：离线地点运行时不依赖外部连通；生产部署实测不在本任务范围内。

## 证据

- 当前 quick CI：`443 passed`，证据目录 `/tmp/fatecat-local-ci-20260712103339`。
- 数据供应链：`172` 项检查通过。
- 干净生产依赖环境：新建 venv 安装、`pip check`、timezonefinder 和 zoneinfo smoke 通过。
- 治理严格校验：PASS，`0` issues。
- 单输入框模糊候选、地点目录、时区与 API 定向回归：`118 passed`。
- 移动端 Chrome 实测：390x844 视口输入“西安长安”返回完整候选并绑定 `cn:610116`；重新编辑清空旧 ID；未重选时阻止提交；有效选择异步提交 HTTP 202；页面脚本错误 0。
- 暖模糊搜索性能：500 次查询平均 `4.393 ms`，p95 `5.671 ms`，p99 `10.562 ms`，最大 `11.540 ms`。
- 导出包：lite export、两次 hygiene 和导出包 pure preflight smoke 通过。
- 暖查询性能：500 次搜索，平均 `1.443 ms`，p95 `2.459 ms`，p99 `4.273 ms`，最大 `6.078 ms`。

## 审计案例消费

- CASE-0002：构建器下载有 120 秒显式超时；构建属于离线维护，不在请求链路。刷新失败时继续保留已跟踪目录。
- CASE-0003：TODO、STATUS、checklist 和新鲜 CI 证据在 closeout 前保持一致。
- CASE-0005：没有自研地理或时区引擎；复用 GeoNames、IANA tzdb、timezonefinder、SQLite 和原生 HTML。
- CASE-0006：Web/API 为 FastAPI 同步 handler，由线程池执行；生产请求只做本地索引读取，无网络调用；`/ready` 在就绪前验证索引。
- CASE-0004：参考站仅用于交互研究，明确排除其数据和视觉实现。

## 审查项

- PASS correctness：审查中发现并移除退役行政区代码 `cn:350403`，回归锁定现行 `cn:350404`。
- PASS reliability：catalog hash、进程文件锁、临时 SQLite 构建和原子替换保护索引创建。
- PASS privacy/security：catalog 不含用户记录；日志和指标不持久化用户提交地点或坐标。
- PASS architecture：canonical gzip、runtime SQLite、协议、解析器和交付面职责分离；旧 CSV fallback 已删除。
- PASS test quality：覆盖全量目录、稳定 ID、重名、行政层级后缀模糊匹配、WGS84、时区、DST gap/fold、Web 候选 ID 失效/一致性、无脚本降级、API 冲突和跨交付面一致性。

## 剩余风险

- 行政区与 GeoNames 是固定快照，不是实时政府登记；刷新仍需人工审计。
- 109 个国内记录使用 `parent_centroid`，不得表示为精确出生地址。
- GeoNames `cities1000` 不覆盖全部小型地点；用户可提交 WGS84 直接坐标。
- 当前没有独立的历史行政区名称版本化查询产品。

## 扫描器说明

`scan_principle_gates.py --git-mode working --strict` 对工作树中既有或无关文档里的“兼容/迁移”等关键词产生 BLOCK/WARN，包括 API 兼容策略和安全 token 迁移文本。这些 finding 没有定位到本任务的地点实现缺陷，因此未虚报扫描全绿；本任务的目标终态、存在性、proof、falsifier 和迁移证据已记录在 `CONTEXT.md` 并完成人工复核。
