var app = getApp()
Page({
    data: {
        system: app.globalData.sysInfo.system,
        brand: app.globalData.sysInfo.brand,
        model: app.globalData.sysInfo.model,
        language: app.globalData.sysInfo.language,
        wechatVersion: app.globalData.sysInfo.version,
        SDKVersion: app.globalData.sysInfo.SDKVersion,
    },
    networkRename(res) {
        if (res.networkType == "wifi") {
            res.networkType = "Wi-Fi"
            wx.getConnectedWifi({
                success: (res) => {
                    this.setData({
                        ssid: res.wifi.SSID,
                        bssid: res.wifi.BSSID,
                        secure: res.wifi.secure ? "Secure" : "Not secure",
                        strength: 100 - res.wifi.signalStrength * (this.data.system.substring(0, 3) == "iOS" ? 100 : 1),
                        frequency: res.wifi.frequency
                    })
                },
            })
        }
        else if (res.networkType[1] == "g")
            res.networkType = res.networkType[0] + 'G'
        else
            res.networkType = res.networkType[0].toUpperCase() + res.networkType.substring(1)
        this.setData({ network: res.networkType })
    },
    onLoad() {
        wx.getBatteryInfo({
            success: (res) => {
                this.setData({
                    battery: res.level,
                    charging: res.isCharging ? "Charging" : "Not charging",
                })
            },
        })
        wx.getNetworkType({ success: (res) => this.networkRename(res) })
        wx.onNetworkStatusChange((res) => this.networkRename(res))
        wx.getScreenBrightness({ success: (res) => { this.setData({ brightness: res.value.toPrecision(2) * 100 }) } })
        wx.startAccelerometer()
        wx.startGyroscope()
        wx.startCompass()
        wx.onAccelerometerChange((res) => {
            this.setData({
                AccX: res.x.toPrecision(10),
                AccY: res.y.toPrecision(10),
                AccZ: res.z.toPrecision(10)
            })
        })
        wx.onGyroscopeChange((res) => {
            this.setData({
                GyroX: res.x.toPrecision(10),
                GyroY: res.y.toPrecision(10),
                GyroZ: res.z.toPrecision(10)
            })
        })
        wx.onCompassChange((res) => {
            this.setData({
                compassDir: res.direction,
                compassAcc: res.accuracy
            })
        })
    },
    onUnload() {
        wx.stopAccelerometer()
        wx.stopGyroscope()
        wx.stopCompass()
    },
    mixins: [require('../../../utils/themeChanged')]
})
