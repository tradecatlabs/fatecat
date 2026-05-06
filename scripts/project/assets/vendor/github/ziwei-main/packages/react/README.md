<img src="https://raw.githubusercontent.com/lzm0x219/ziwei/refs/heads/main/.github/splash.react.png" alt="@ziweijs/react" />

[![NPM Version](https://img.shields.io/npm/v/%40ziweijs%2Freact)](https://www.npmjs.com/package/%40ziweijs%2Freact)
[![NPM Downloads](https://img.shields.io/npm/dm/%40ziweijs%2Freact?cacheSeconds=360000)](https://www.npmjs.com/package/%40ziweijs%2Freact)
[![GitHub License](https://img.shields.io/github/license/lzm0x219/ziwei?style=flat)](https://github.com/lzm0x219/ziwei/blob/main/LICENSE)
[![Formatted with Biome](https://img.shields.io/badge/Formatted_with-Biome-60a5fa?style=flat&logo=biome)](https://biomejs.dev/)

## 简介

`@ziweijs/react` 是基于 `@ziweijs/core` 构建的 React 组件，帮助你在 Web 项目中快速渲染北派紫微斗数命盘。库内置高分辨率的命盘栅格、十四主星 + 辅星布置、四化/自化标识等元素，并针对 React 的状态管理和上下文系统做了封装。

## 特性

- 🌓 **React 就绪**：默认导出 `<ZiWei />` 组件，传入姓名、阳历时间与性别即可绘制完整命盘。
- 🎨 **自适应布局**：所有尺寸、字体、颜色均通过 `ConfigContext` 驱动，轻松自定义皮肤。
- 🌏 **多语言**：与 `@ziweijs/core` 的 `i18n` 体系一致，支持 `zh-CN`/`zh-Hant` 等语言切换。
- ⚛️ **hooks/工具集**：提供 `RuntimeContainer`、配置上下文等工具，方便拓展自定义 UI。

## 截图
<img src="https://raw.githubusercontent.com/lzm0x219/ziwei/refs/heads/main/.github/react-ziwei.png" alt="@ziweijs/react" />

## 安装

```bash
pnpm add @ziweijs/react @ziweijs/core react react-dom
```

> React 19.2+ 为 peer 依赖，请确保项目已升级。

## 快速上手

```tsx
import ZiWei from "@ziweijs/react";

export default function Demo() {
  return (
    <div style={{ width: 720 }}>
      <ZiWei
        name="张三"
        gender="male"
        language="zh-CN"
        date="1990-05-21T10:30:00+08:00"
        width={720}
        height={720}
      />
    </div>
  );
}
```

组件会调用 `@ziweijs/core` 的 `bySolar` 逻辑解析 ISO 字符串（含时区），完成紫微命盘排盘后渲染 SVG。

## Props

| 属性    | 类型                  | 说明                                    |
| ------- | --------------------- | --------------------------------------- |
| `name`  | `string`              | 命主姓名，仅用于展示。                  |
| `gender`| `GenderKey`           | 性别（`male`/`female`）。               |
| `date`  | `string`              | 阳历时间，推荐使用 `YYYY-MM-DDTHH:mm:ssZ`。 |
| `language` | `Language`        | 可选，命盘文案语言，默认 `zh-CN`。      |
| `width`/`height` | `number`    | 画布尺寸，默认 600。                    |

更多样式可通过 `ConfigContext` 配合 `RuntimeContainer` 覆写，详见 `packages/react/src/context`。

## 本地开发

```bash
pnpm install
pnpm dev --filter @ziweijs/react
```

- 组件源代码：`packages/react/src`
- Playground：`packages/react/playground`
- 排盘核心：`@ziweijs/core`（workspace 依赖）

## 状态

🚧 积极开发中...

## 版权

本项目根据 [MIT](https://github.com/lzm0x219/ziwei/blob/main/LICENSE) 开源许可证条款授权使用。
