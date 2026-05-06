module.exports = {
    onShow() {
        this.setData({ theme: getApp().globalData.theme })
    }
};
