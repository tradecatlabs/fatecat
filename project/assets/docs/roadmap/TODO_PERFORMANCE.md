# 性能优化 Todo（按易→难）

1. 阻塞下沉到线程池  
   - 将 sxwnl/iztro/fortel/js_astro 子进程调用、`BaziCalculator.calculate()`、`db.save_record` 包装为 `asyncio.to_thread(...)`，在 handler 中 `await`。  
   - 目标：释放事件循环，提高单实例并发。

2. 超时与错误标记  
   - 统一子进程调用 timeout=10s；超时/异常不终止整体，结果中标注“模块超时/失败”。  
   - 防止单模块卡死拖垮请求。

3. 并行外部模块  
   - sxwnl / iztro / astro 等独立步骤使用 `asyncio.gather` 并行（内部仍在线程池）。  
   - 预期减少整体耗时。

4. DB 写入异步化  
   - `db.save_record` 放入 `asyncio.to_thread`。  
   - 如并发继续升高，再切换异步数据库或后台队列。

5. 耗时日志与基线  
   - 在排盘开始/结束与各模块调用前后打印耗时（ms）到 `/tmp/telegram-bot.log`，跟踪 P50/P95/P99。

6. 预热  
   - 启动时自动跑一次排盘，预加载依赖/编译，降低首个请求冷启动。

7. 可选进阶  
   - 长驻 Node worker（持久子进程）替代每次冷启动。  
   - 部署 webhook 或多实例；需要更大吞吐时引入任务队列异步返回。
