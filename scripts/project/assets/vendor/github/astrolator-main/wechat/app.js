require('./utils/Mixins.js')
App({
    globalData: {
        sysInfo: wx.getSystemInfoSync(),
        theme: wx.getSystemInfoSync().theme,
        version: "0.16.210401",
        G: 6.6743e-11,
        c: 299792458,
        h: 6.62607004e-34,
        k_B: 1.380649e-23,
        m_p: 1.6726219e-27,
        sigma_T: 6.65245872e-29,
        Mpc2km: 3.085677581491367e19,
        settings: ["language", "precision", "angle", "length", "time", "frequency", "mass", "energy", "power"],
        language: ["English", "简体中文 #TODO", "繁体中文 #TODO", "日本語 #TODO"],
        scientific: wx.getStorageSync("scientific"),
        precision: ["1 digit", "2 digits", "3 digits", "4 digits", "5 digits", "6 digits", "7 digits", "8 digits", "9 digits", "10 digits", "11 digits", "12 digits", "13 digits"],
        angle: ["rad", "deg", "mas"],
        angleRatio: [1, 180 / Math.PI, 6.48e8 / Math.PI],
        length: ["pc", "Å", "nm", "cm", "m", "km", "R_earth", "R_jup", "R_sun", "AU", "lyr", "kpc", "Mpc", "Gpc"],
        lengthMain: ["pc", "Å", "nm", "cm", "m", "km", "R", "R", "R", "AU", "lyr", "kpc", "Mpc", "Gpc"],
        lengthSub: ['', '', '', '', '', '', "earth", "jup", "sun", '', '', '', '', ''],
        lengthRatio: [3.240779289444365e-17, 1e10, 1e9, 100, 1, 1e-3, 1.56786504e-7, 1.3987579e-8, 1.43740118e-9, 6.684587122268445e-12, 1.0570008340246154e-16, 3.240779289444365e-20, 3.240779289444365e-23, 3.240779289444365e-26],
        time: ["yr", "s", "min", "hr", "day", "kyr", "Myr", "Gyr"],
        timeRatio: [3.168808781402895e-8, 1, 0.016666666666666667, 0.0002777777777777778, 1.1574074074074073e-5, 3.168808781402895e-11, 3.168808781402895e-14, 3.168808781402895e-17],
        frequency: ["Hz", "nHz", "μHz", "mHz", "kHz", "MHz", "GHz"],
        frequencyRatio: [1, 1e9, 1e6, 1e3, 1e-3, 1e-6, 1e-9],
        mass: ["M_sun", "m_e", "m_p", "g", "kg", "M_earth", "M_jup"],
        massMain: ["M", "m", "m", "g", "kg", "M", "M"],
        massSub: ["sun", "e", "p", '', '', "earth", "jup"],
        massRatio: [5.029144215870041e-31, 1.09776911e+30, 5.97863741e+26, 1000, 1, 1.6744338440202266e-25, 5.268358048799663e-28],
        energy: ["erg", "eV", "J"],
        energyRatio: [1e7, 6.241509074460763e+18, 1],
        power: ["L_sun", "erg/s", "W"],
        powerMain: ["L", "erg/s", "W"],
        powerSub: ["sun", '', ''],
        powerRatio: [2.612330198537095e-27, 1e7, 1],
        temperature: ["K"],
        temperatureRatio: [1],
        temperatureIndex: 0
    },
    onLaunch: function () {
        var version = wx.getStorageSync("version")
        if (version == '') {
            wx.setStorageSync("language", 0)
            wx.setStorageSync("precision", 5)
            wx.setStorageSync("angle", 0)
            wx.setStorageSync("length", 0)
            wx.setStorageSync("time", 0)
            wx.setStorageSync("frequency", 0)
            wx.setStorageSync("mass", 0)
            wx.setStorageSync("energy", 0)
            wx.setStorageSync("power", 0)
            wx.setStorageSync("version", this.globalData.version)
            wx.setStorageSync("hubble", 67.74)
            wx.setStorageSync("matter", 0.3089)
            wx.setStorageSync("lambda", 0.6911)
            wx.setStorageSync("curvature", 0)
            wx.setStorageSync("addData", [])
            wx.navigateTo({ url: "/pages/welcome/welcome" })
        }
        else if (this.globalData.version != version) {
            wx.setStorageSync("version", this.globalData.version)
            wx.navigateTo({ url: "/pages/settings/version/version" })
        }
        this.globalData.languageIndex = wx.getStorageSync("language")
        this.globalData.precisionIndex = wx.getStorageSync("precision")
        this.globalData.angleIndex = wx.getStorageSync("angle")
        this.globalData.lengthIndex = wx.getStorageSync("length")
        this.globalData.timeIndex = wx.getStorageSync("time")
        this.globalData.frequencyIndex = wx.getStorageSync("frequency")
        this.globalData.massIndex = wx.getStorageSync("mass")
        this.globalData.energyIndex = wx.getStorageSync("energy")
        this.globalData.powerIndex = wx.getStorageSync("power")
    },
    onThemeChange(res) {
        this.globalData.theme = res.theme
        var pages = getCurrentPages()
        for (var i = 0; i < pages.length; ++i)
            pages[i].setData({ theme: res.theme })
    },
    scientificDisplay(value, type = "number", index = 0) {
        if (value == undefined || value === '')
            return ''
        if (type != "number")
            value *= this.globalData[`${type}Ratio`][index]
        if (this.globalData.scientific == 0)
            return Number(value).toPrecision(this.globalData.precisionIndex + 1)
        return Number(value).toExponential(this.globalData.precisionIndex)
    }
})
