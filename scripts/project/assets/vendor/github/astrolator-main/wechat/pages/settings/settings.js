var app = getApp()
var pageData = {
    data: {
        scientific: app.globalData.scientific,
        lengthMain: app.globalData.lengthMain,
        lengthSub: app.globalData.lengthSub,
        massMain: app.globalData.massMain,
        massSub: app.globalData.massSub,
        powerMain: app.globalData.powerMain,
        powerSub: app.globalData.powerSub,
        version: app.globalData.version
    },
    mixins: [require('../../utils/themeChanged')],
    scientificChange(e) {
        this.setData({ scientific: e.detail.value })
        app.globalData.scientific = e.detail.value
        wx.setStorageSync("scientific", e.detail.value)
    }
}
for (var i in app.globalData.settings) {
    (function (name) {
        pageData[name + "Change"] = function (e) {
            var obj = {}
            obj[name + "Index"] = e.detail.value
            this.setData(obj)
            app.globalData[name + "Index"] = Number(e.detail.value)
            wx.setStorageSync(name, Number(e.detail.value))
        }
    })(app.globalData.settings[i])
    pageData.data[app.globalData.settings[i]] = app.globalData[app.globalData.settings[i]]
    pageData.data[app.globalData.settings[i] + "Index"] = app.globalData[app.globalData.settings[i] + "Index"]
}
Page(pageData)
