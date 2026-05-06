var app = getApp()
Page({
    data: {
        height: String(app.globalData.sysInfo.windowHeight - 350),
        android: app.globalData.sysInfo.system.substring(0, 3) != "iOS"
    },
    mixins: [require('../../utils/themeChanged')]
})
