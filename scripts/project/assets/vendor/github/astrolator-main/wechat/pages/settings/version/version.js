Page({
    data: {
        line: ["dashed", "dotted", "solid"],
        color: ["var(--weui-ORANGE)", "var(--weui-BLUE)", "var(--weui-TEXTGREEN)", "var(--weui-FG-1)"],
        version: [{
            name: "Roadmap",
            detail: ["Worker (打工人): 创建 Worker 进程，提升计算效率与计算精度；", "Plotly.js: 为计算器加入简单的作图功能，本来是计划用 Plotly.js 的，但官方的 js 文件有好几个 MB，小程序分包限制上限是2MB，暂时还没着手解决这个问题（也许用 Canvas 自己画？）；", "i18n: 等基本功能完善后再处理吧（需要这个小程序的人也都能看懂英语不是）；", "无障碍访问。"]
        }, {
            name: "IN PROGRESS",
            detail: ["优化光谱数据页面（已隐藏）"]
        }, {
            name: "0.16 (2020.11)",
            detail: ["完成弯曲宇宙计算，双红移计算，增加宇宙学参数自定义/删除功能。"]
        }, {
            name: "0.15 (2020.11)",
            detail: ["完成宇宙学观测参数传递。"]
        }, {
            name: "0.14 (2020.11)",
            detail: ["修改小程序名，整理计算页面，升级外观。"]
        }, {
            name: "0.13 (2020.10)",
            detail: ["增加单位换算页功能。"]
        }, {
            name: "0.12 (2020.10)",
            detail: ["优化 WEUI 组件代码。"]
        }, {
            name: "0.11 (2020.10)",
            detail: ["测试共动距离计算。"]
        }, {
            name: "0.10 (2020.10)",
            detail: ["新增版本更新后的更新记录提醒。"]
        }, {
            name: "0.9 (2020.10)",
            detail: ["完成科学计数法显示，优化单位换算、显示过程。"]
        }, {
            name: "0.8 (2020.10)",
            detail: ["完成平坦宇宙时间计算，并优化单位换算代码结构，优化全局设置更改自动刷新机制。"]
        }, {
            name: "0.7 (2020.10)",
            detail: ["加入客服链接与反馈按钮，删除邮箱。"]
        }, {
            name: "0.6 (2020.10)",
            detail: ["加入 Acronym 页面。"]
        }, {
            name: "0.5 (2020.10)",
            detail: ["实现单位转换页功能。"]
        }, {
            name: "0.4 (2020.10)",
            detail: ["增加设置本地保存功能。"]
        }, {
            name: "0.3 (2020.10)",
            detail: ["实现夜间模式。"]
        }, {
            name: "0.2 (2019)",
            detail: ["加入 WEUI 组件。"]
        }, {
            name: "0.1 (2018)",
            detail: ["完成小程序外观框架。"]
        }]
    },
    mixins: [require('../../../utils/themeChanged')]
})
