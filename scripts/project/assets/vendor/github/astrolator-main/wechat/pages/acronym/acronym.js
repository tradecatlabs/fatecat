import { items } from 'acronymData'
Page({
    data: {
        inputShowed: false,
        category: '',
        explanation: '',
        showContentDialog: false,
        buttons: [{ text: "Copy" }, { text: "OK" }]
    },
    mixins: [require('../../utils/themeChanged')],
    onLoad() {
        this.getAcronyms()
    },
    onChoose(e) {
        this.setData({
            category: e.detail.item.category,
            explanation: e.detail.item.explanation,
            showContentDialog: true
        })
    },
    getAcronyms() {
        items.sort((a1, a2) => { return a1.acronym.localeCompare(a2.acronym) })
        // 添加首字母
        const map = new Map()
        for (const item of items) {
            const alpha = item.acronym[0].toUpperCase()
            if ('0' <= alpha && alpha <= '9')
                alpha = 'a'
            if (!map.has(alpha))
                map.set(alpha, [])
            map.get(alpha).push({ name: item.acronym, category: item.category, explanation: item.explanation })
        }
        const list = []
        for (const key of map.keys())
            list.push({ alpha: key, subItems: map.get(key) })
        this.setData({ list })
    },
    copyExplanation(e) {
        this.setData({ showContentDialog: false })
        if (e.detail.index == '0')
            wx.setClipboardData({ data: this.data.explanation })
    },
    copyWebAddress: function () { wx.setClipboardData({ data: "https://en.wikipedia.org/wiki/List_of_astronomy_acronyms" }) }
})
