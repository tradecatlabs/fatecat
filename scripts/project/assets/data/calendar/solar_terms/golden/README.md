# 节气 Golden Fixture

本目录存放从本地 raw 交节时间表提炼出的轻量回归 fixture。

## 文件

| 文件 | 说明 |
| --- | --- |
| `solar_terms_1900_2030.json` | 1900-2030 年 24 节气时间表，供测试交叉校验 `lunar-python` 节气、月令和立春年界边界。 |

## 使用边界

- fixture 是测试资产，不是生产历法算法替换源。
- 运行期节气计算仍复用 `lunar-python`。
- raw 表保留在 `../raw/`，不进入 Git 和导出包；本目录只保存清洗后的轻量 JSON。
- `scripts/build_solar_terms_golden.py` 需要本地 raw CSV 才能重新生成 fixture；第三方审计需要按 `../source_manifest.tsv` 复核 raw 文件哈希。
- 误差容差记录在 JSON 的 `toleranceSeconds`。当前 raw 表与 `lunar-python` 在 1940 年代等历史区间存在约 1 小时时区/DST 口径差异；测试失败必须先判断是来源表差异、上游库差异还是项目逻辑回归。
