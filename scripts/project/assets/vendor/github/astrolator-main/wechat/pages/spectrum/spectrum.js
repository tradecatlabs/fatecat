import { list } from 'spectrumData'
Page({
    data: {
        inputShowed: false,
        name: '',
        wavelength: '',
        showContentDialog: false,
        buttons: [{ text: "Copy" }, { text: "OK" }]
    },
    mixins: [require('../../utils/themeChanged')],
    onLoad() {
        this.setData({ list })
    },
    search(value) {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                resolve([{ text: '搜索结果', value: 1 }, { text: '搜索结果2', value: 2 }])
            }, 200)
        })
    },
    selectResult(e) { console.log('select result', e.detail) },
    onChoose(e) {
        this.setData({
            name: e.detail.item.name,
            wavelength: e.detail.item.wavelength,
            showContentDialog: true
        })
    },
    copyWavelength(e) {
        this.setData({ showContentDialog: false })
        if (e.detail.index == '0')
            wx.setClipboardData({ data: this.data.wavelength })
    }
})
