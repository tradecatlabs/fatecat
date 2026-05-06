var app = getApp()
Page({
    data: {
        add: false,
        addData: wx.getStorageSync("addData"),
        name: '',
        obsData: [{
            name: "Planck18",
            hubble: 67.66,
            matter: 0.3111,
            lambda: 0.6889,
            curvature: 0
        }, {
            name: "Planck15",
            hubble: 67.7,
            matter: 0.307,
            lambda: 0.693,
            curvature: 0
        }, {
            name: "Planck13",
            hubble: 67.8,
            matter: 0.307,
            lambda: 0.693,
            curvature: 0
        }, {
            name: "WMAP9",
            hubble: 69.3,
            matter: 0.287,
            lambda: 0.713,
            curvature: 0
        }, {
            name: "WMAP7",
            hubble: 70.4,
            matter: 0.272,
            lambda: 0.728,
            curvature: 0
        }, {
            name: "WMAP5",
            hubble: 70.2,
            matter: 0.277,
            lambda: 0.723,
            curvature: 0
        }, {
            name: "Simple Flat",
            hubble: 70,
            matter: 0.3,
            lambda: 0.7,
            curvature: 0
        }]
    },
    mixins: [require('../../../utils/themeChanged')],
    onLoad(e) {
        this.setData({
            hubble: Number(e.hubble),
            hubbleDisplay: e.hubble,
            matter: Number(e.matter),
            matterDisplay: e.matter,
            lambda: Number(e.lambda),
            lambdaDisplay: e.lambda,
            curvature: Number(e.curvature),
            curvatureDisplay: app.scientificDisplay(Number(e.curvature)),
        })
    },
    onPullDownRefresh() {
        this.setData({ add: true })
        wx.stopPullDownRefresh()
    },
    setName(e) {
        this.setData({ name: e.detail.value })
    },
    setHubble(e) {
        this.setData({ hubble: Number(e.detail.value) })
    },
    setMatter(e) {
        this.setData({
            matter: Number(e.detail.value),
            curvature: Math.abs(1 - e.detail.value - this.data.lambda) < 1e-13 ? 0 : 1 - e.detail.value - this.data.lambda,
            curvatureDisplay: Math.abs(1 - e.detail.value - this.data.lambda) < 1e-13 ? app.scientificDisplay(0) : app.scientificDisplay(1 - e.detail.value - this.data.lambda)
        })
    },
    setLambda(e) {
        this.setData({
            lambda: Number(e.detail.value),
            curvature: Math.abs(1 - this.data.matter - e.detail.value) < 1e-13 ? 0 : 1 - this.data.matter - e.detail.value,
            curvatureDisplay: Math.abs(1 - this.data.matter - e.detail.value) < 1e-13 ? app.scientificDisplay(0) : app.scientificDisplay(1 - this.data.matter - e.detail.value)
        })
    },
    saveData() {
        if (this.data.hubble <= 0 || this.data.matter < 0 || this.data.lambda < 0)
            return
        this.setData({
            add: false,
            addData: [{ name: this.data.name == '' ? "Para " + this.data.addData.length : this.data.name, hubble: this.data.hubble, matter: this.data.matter, lambda: this.data.lambda, curvature: this.data.curvature }].concat(this.data.addData)
        })
        wx.setStorageSync("addData", this.data.addData)
    },
    slideButtonTap(e) {
        var addData = this.data.addData
        addData.splice(e.target.id, 1)
        this.setData({ addData })
        wx.setStorageSync("addData", addData)
    },
    useAddData(e) {
        this.getOpenerEventChannel().emit("recData", this.data.addData[e.currentTarget.id])
        wx.navigateBack()
    },
    useObsData(e) {
        this.getOpenerEventChannel().emit("recData", this.data.obsData[e.currentTarget.id])
        wx.navigateBack()
    }
});
