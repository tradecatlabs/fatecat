# taibu-core

TaiBu 的命理术数算法核心库。

它提供两类能力：

- 各术数的算法、类型，以及规范化 text/json 输出
- MCP 工具定义、输入校验、执行入口与统一响应适配

## 工具列表

| 工具 | 说明 |
|------|------|
| `bazi` | 八字排盘 |
| `bazi_pillars_resolve` | 八字四柱反推出生时间候选 |
| `bazi_dayun` | 大运、小运、流年链路计算 |
| `ziwei` | 紫微斗数排盘 |
| `ziwei_horoscope` | 紫微运限 |
| `ziwei_flying_star` | 紫微飞星与四化落宫分析 |
| `liuyao` | 六爻排卦与分析 |
| `meihua` | 梅花易数起卦与断卦 |
| `tarot` | 塔罗抽牌 |
| `almanac` | 黄历与择日信息 |
| `astrology` | 西方占星命盘与流运 |
| `qimen` | 奇门遁甲排盘 |
| `taiyi` | 太乙九星观测 |
| `daliuren` | 大六壬排盘 |
| `xiaoliuren` | 小六壬占测 |

## 安装

```bash
npm install taibu-core
```

如需使用 GitHub Packages 镜像包，请改用 `@hhszzzz/taibu-core`。npmjs 主包名仍然是 `taibu-core`。

## Quick Start

### 直接使用某个术数

```ts
import { calculateBazi, toBaziText, toBaziJson } from 'taibu-core/bazi';

const chart = calculateBazi({
  gender: 'male',
  birthYear: 1990,
  birthMonth: 1,
  birthDay: 15,
  birthHour: 9,
});

const text = toBaziText(chart);
const json = toBaziJson(chart);
```

### 按 MCP 工具名执行

```ts
import { executeTool, renderToolResult } from 'taibu-core/mcp';

const result = await executeTool('qimen', {
  year: 2026,
  month: 3,
  day: 19,
  hour: 21,
  minute: 30,
  timezone: 'Asia/Shanghai',
});

const rendered = renderToolResult('qimen', result);
```

## 选择入口

- `taibu-core`
  - 根入口，聚合常用术数能力与类型
- `taibu-core/mcp`
  - MCP 工具执行与输出适配
- `taibu-core/<domain>`
  - 某个术数的算法、类型、`to*Text()`、`to*Json()`

当前 domain 子路径包括：

- `taibu-core/bazi`
- `taibu-core/bazi-dayun`
- `taibu-core/bazi-pillars-resolve`
- `taibu-core/astrology`
- `taibu-core/almanac`
- `taibu-core/liuyao`
- `taibu-core/meihua`
- `taibu-core/ziwei`
- `taibu-core/ziwei-horoscope`
- `taibu-core/ziwei-flying-star`
- `taibu-core/qimen`
- `taibu-core/taiyi`
- `taibu-core/daliuren`
- `taibu-core/tarot`
- `taibu-core/xiaoliuren`

额外公开的共享子路径：

- `taibu-core/utils`
- `taibu-core/timezone-utils`
- `taibu-core/data/hexagrams`
- `taibu-core/data/shensha`

## 包结构

- `domains/`
  - 各术数 domain 的算法、本领域类型，以及 canonical text/json 输出
- `mcp/`
  - MCP 工具定义、schema、执行与统一 payload 适配
- `shared/`
  - 跨 domain 复用的公共工具
- `data/`
  - 干支、神煞、卦象文本等基础数据

## 输出约定

`taibu-core/mcp` 的 `renderToolResult(...)` 和 `buildToolSuccessPayload(...)` 使用统一输出契约：

- `content`
  - 始终返回 canonical text，适合直接阅读
- `structuredContent`
  - 当工具声明了 `outputSchema` 时返回 canonical JSON，适合程序消费

也就是说：

- 如果你是人类阅读场景，读 `content`
- 如果你是 schema 驱动场景，读 `structuredContent`

## Related Packages

- [`taibu-mcp`](https://www.npmjs.com/package/taibu-mcp)
  - 适合本地 `stdio` MCP Server 场景

## License

`taibu-core` 使用 `MIT` 许可证，详见当前目录下的 `LICENSE` 文件。
