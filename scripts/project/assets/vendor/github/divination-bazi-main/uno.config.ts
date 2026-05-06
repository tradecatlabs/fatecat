import {
    defineConfig, // https://github.com/antfu/unocss/blob/main/src/types/config.ts
    // 预设 attributify
    presetAttributify, // https://unocss.dev/preset/attributify
    // 预设 icon
    presetIcons, // https://unocss.dev/preset/icons
    // 预设 typography
    presetTypography, // https://unocss.dev/preset/typography
    // 预设 preset
    presetUno, //  https://unocss.dev/preset/uno
    // 预设 web-font
    presetWebFonts, // https://unocss.dev/preset/web-fonts
    // 自动导入指令
    transformerDirectives, // https://github.com/antfu/unocss/blob/main/src/transformers/directives.ts
} from "unocss";

export default defineConfig({
    //  自定义配置
    shortcuts: {
        "border-base": "border-gray-200 dark:border-gray-500",
        "bg-active": "bg-gray:10",
        "flex-center": "flex items-center justify-center",
        "card-size": "w-120px h-164px",
        "bg-mask": "bg-white-80 dark:bg-black-30",
    },
    //  额外选项
    rules: [
        [/^t-a-(\d+)$/, ([, d]) => ({transition: `all 0.${d}s linear`})],
        [
            /^bg-white-(\d+)$/,
            ([, d]) => ({"background-color": `rgb(255 255 255 / ${d}%)`}),
        ],
        [
            /^bg-black-(\d+)$/,
            ([, d]) => ({"background-color": `rgb(0 0 0 / ${d}%)`}),
        ],
        [/^l-s-(\d+)$/, ([, d]) => ({"letter-spacing": `${d}px`})],
    ],
    //  主题
    theme: {
        colors: {
            primary: {
                DEFAULT: "#00DC82",
            },
        },
    },
    //  预设
    presets: [
        presetUno(),
        presetIcons(),
        presetAttributify(),
        presetWebFonts({
            provider: "bunny",
            fonts: {
                sans: "DM Sans",
                mono: "DM Mono",
                ping: "PingFangMedium"
            },
        }),
        presetTypography(),
    ],
    //  交互
    transformers: [transformerDirectives()],
});
