# 外部算法强制复用与替换方案（2025-12-17）

## 背景
- 生产事故：身强/身弱判定出现自相矛盾，根因是同时使用自写与外部口径。已紧急统一强弱判定为 bazi-1 `weakStrong`。
- 规范要求：核心判定必须复用外部原生算法，禁止自写替代口径；若无外部实现需明示“例外”。

## 现存自写/混合点（需处理）
1. **用神**：`_calc_yongshen` 依赖本地静态表 `TIAOHOU`。
2. **神煞简表**：`_calc_spirits` 为手写映射，再与外部全量合并。
3. **格局**：`_calc_geju` 使用本地 `JIANLU/YANGREN_POS` 等表，无外部 API。
4. **真太阳时**：`_calc_true_solar_time` 自写；可能与外部天文实现不一致。
5. **旺衰表**：`WUXING_STATE` 静态表，暂无外部替代接口。

## 可直接复用的外部资源
- **bazi-1**：`datas.py` 中 `tiaohous`（调候用神表）、`year_shens/month_shens/day_shens/g_shens`（神煞全量表）。
- **lunar-python / sxwnl**：历法与真太阳时接口（待验证使用方式）。

## 执行方案（按优先级）
### P1 立刻落地（消除红线）
1. 用神数据外部化  ✅ 已完成  
   - 动作：移除本地 `TIAOHOU`，改为 `from datas import tiaohous as TIAOHOU`。  
   - 逻辑：`_calc_yongshen` 保持现有判定流程，仅替换数据源。  
2. 神煞纯外部化  ✅ 已完成  
   - 动作：报告直接使用 `_calc_all_spirits` 结果；移除 `_calc_spirits` 简表与合并逻辑，确保单一口径。  
3. 真太阳时外部化  ✅ 已完成  
   - 动作：新增 Node 桥接 `scripts/true_solar_time.js` 调用 paipan-master `zty()`；`_calc_true_solar_time` 优先走外部算法，失败回退旧公式。

### P2 调研后落地
3. 真太阳时外部化  
   - 动作：调研 `true_solar_time.py` 或 lunar-python/sxwnl 原生接口；若精度更高，则替换 `_calc_true_solar_time`。

### P3 决策/标注
4. 格局  
   - 外部库无现成 API。选项：  
     - A) 保留本地实现，并在文档注明“无外部实现的例外”；或  
     - B) 封装 bazi-1 CLI 逻辑为可调用函数，再切换调用。  
5. 旺衰表  
   - 若找不到外部接口，保留并在文档注明“静态口径，无外部替代”。

## 交付物
- 代码改动：按上述步骤提交 PR。  
- 文档：更新根目录事故记录/AGENTS.md，标明已外部化的模块与保留的例外。  
- 验证：随机 10 份排盘回归，确认报告不再混出口径。
