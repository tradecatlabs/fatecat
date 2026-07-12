# 出生地点目录数据产品

该目录提供 Web、API 与 Agent 共用的出生地点真相源。行政区身份、WGS84 坐标、IANA 时区、来源版本和坐标精度均为稳定字段；原始下载文件不进入 Git。

## 文件

- `sources.lock.json`：锁定来源 URL、版本、许可证和 SHA256。
- `location_catalog.ndjson.gz`：确定性压缩的运行时目录，由构建脚本生成。
- `manifest.json`：记录产物 hash、记录数量、精度分布与许可边界。

## 构建

```bash
python -m pip install 'opencc-python-reimplemented==0.1.7'
python scripts/build-location-catalog.py
```

构建脚本会下载锁定来源并校验 hash。上游日更文件发生变化时必须先人工复核，再更新锁文件；禁止静默接受新 hash。

## 数据边界

- 中国大陆现行行政区代码和层级来自 `Administrative-divisions-of-China` 的固定提交；撤销代码不进入生产目录。
- 全球地点、坐标和 IANA 时区来自 GeoNames。
- 所有坐标统一声明为 WGS84。
- `district_centroid` 表示区县中心点；无法可靠匹配区县坐标时使用 `parent_centroid`，不得宣称为精确出生地址。
- 目录只解析地点事实，不决定用户输入的是当地民用时间、北京时间还是 UTC。

## 许可

- GeoNames 数据：CC BY 4.0，分发时必须保留署名。
- `Administrative-divisions-of-China`：SPDX `WTFPL`（许可证正文为 Version 2）。

本数据产品不包含问真八字客户端数据，也不复制其地区、GMT 或手工夏令时表。
