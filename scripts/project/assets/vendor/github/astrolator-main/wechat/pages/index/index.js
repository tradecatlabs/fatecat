var app = getApp()
Page({
    data: {
        angle: app.globalData.angle,
        angleIndex: app.globalData.angleIndex,
        length: app.globalData.length,
        lengthMain: app.globalData.lengthMain,
        lengthSub: app.globalData.lengthSub,
        lengthIndex: app.globalData.lengthIndex,
        time: app.globalData.time,
        timeIndex: app.globalData.timeIndex,
        twoRedshift: false,
        redshift0: 0.5,
        redshift0Plus: 1.5,
        redshift1: 1,
        redshift1Plus: 2,
        angleLengthRange: [
            ["Angle", "Length"],
            app.globalData.angle
        ],
        angleLengthRangeDisplay: [
            app.globalData.angle,
            app.globalData.length
        ],
        angleLengthIndex0: [0, 0],
        angleLengthIndex1: '0',
        angleLengthIndex2: '0',
        angleLengthInput: ''
    },
    mixins: [require('../../utils/themeChanged')],
    onLoad: function () {
        var hubble = wx.getStorageSync("hubble")
        var matter = wx.getStorageSync("matter")
        var lambda = wx.getStorageSync("lambda")
        this.setData({
            hubble,
            hubbleDisplay: hubble,
            matter,
            matterDisplay: matter,
            lambda,
            lambdaDisplay: lambda,
            curvature: Math.abs(1 - matter - lambda) < 1e-13 ? 0 : 1 - matter - lambda,
            curvatureDisplay: Math.abs(1 - matter - lambda) < 1e-13 ? app.scientificDisplay(0) : app.scientificDisplay(1 - matter - lambda)
        })
    },
    onShow() {
        if (this.data.scientific != app.globalData.scientific || this.data.precisionIndex != app.globalData.precisionIndex)
            this.setData({
                curvatureDisplay: app.scientificDisplay(this.data.curvature),
                redshift0Hubble: app.scientificDisplay(this.data.hubble * Math.sqrt(this.data.matter * this.data.redshift0Plus ** 3 + this.data.curvature * this.data.redshift0Plus ** 2 + this.data.lambda)),
                redshift1Hubble: app.scientificDisplay(this.data.hubble * Math.sqrt(this.data.matter * this.data.redshift1Plus ** 3 + this.data.curvature * this.data.redshift1Plus ** 2 + this.data.lambda)),
                angleDisplay: app.scientificDisplay(this.data.angleOutput, "angle", app.globalData.angleIndex),
                lengthDisplay: app.scientificDisplay(this.data.lengthOutput, "length", app.globalData.lengthIndex)
            })
        if (this.data.scientific != app.globalData.scientific || this.data.precisionIndex != app.globalData.precisionIndex || this.data.lengthIndex != app.globalData.lengthIndex)
            this.setData({
                comoving1Display: app.scientificDisplay(this.data.comoving1, "length", app.globalData.lengthIndex),
                comoving0Display: app.scientificDisplay(this.data.comoving0, "length", app.globalData.lengthIndex),
                angularDisplay: app.scientificDisplay(this.data.angular, "length", app.globalData.lengthIndex),
                luminosityDisplay: app.scientificDisplay(this.data.luminosity, "length", app.globalData.lengthIndex),
                comovingDifference: app.scientificDisplay(this.data.comoving1 - this.data.comoving0, "length", app.globalData.lengthIndex)
            })
        if (this.data.scientific != app.globalData.scientific || this.data.precisionIndex != app.globalData.precisionIndex || this.data.timeIndex != app.globalData.timeIndex)
            this.setData({
                ageDisplay: app.scientificDisplay(this.data.age, "time", app.globalData.timeIndex),
                redshiftAge0Display: app.scientificDisplay(this.data.redshiftAge0, "time", app.globalData.timeIndex),
                redshiftAge1Display: app.scientificDisplay(this.data.redshiftAge1, "time", app.globalData.timeIndex),
                lookbackTime0Display: app.scientificDisplay(this.data.lookbackTime0, "time", app.globalData.timeIndex),
                lookbackTime1Display: app.scientificDisplay(this.data.lookbackTime1, "time", app.globalData.timeIndex), timeDifference: app.scientificDisplay(this.data.lookbackTime1 - this.data.lookbackTime0, "time", app.globalData.timeIndex),
            })
        this.setData({
            scientific: app.globalData.scientific,
            precisionIndex: app.globalData.precisionIndex,
            lengthIndex: app.globalData.lengthIndex,
            timeIndex: app.globalData.timeIndex
        })
    },
    timeCalculation(redshift) {
        if (redshift == 0)
            return 0
        var time = 0, ratio = (redshift == Infinity ? 100 : 1000000 / redshift)
        if (this.data.curvature == 0)
            if (redshift == Infinity)
                if (this.data.matter == 0)
                    time = Infinity
                else if (this.data.lambda == 0)
                    time = 2 * app.globalData.Mpc2km / 3 / Math.sqrt(this.data.matter) / this.data.hubble
                else
                    time = app.globalData.Mpc2km / 3 / Math.sqrt(this.data.lambda) * Math.log((Math.sqrt(1 / this.data.lambda) + 1) / (Math.sqrt(1 / this.data.lambda) - 1)) / this.data.hubble
            else
                if (this.data.matter == 0)
                    time = app.globalData.Mpc2km / this.data.hubble / Math.sqrt(this.data.lambda) * Math.log(redshift + 1)
                else if (this.data.lambda == 0)
                    time = 2 * app.globalData.Mpc2km / 3 / Math.sqrt(this.data.matter) / this.data.hubble * (1 - (redshift + 1) ** -1.5)
                else
                    time = app.globalData.Mpc2km / 3 / Math.sqrt(this.data.lambda) / this.data.hubble * (Math.log((Math.sqrt(1 / this.data.lambda) + 1) / (Math.sqrt(1 / this.data.lambda) - 1)) - Math.log((Math.sqrt(1 + this.data.matter * (redshift + 1) ** 3 / this.data.lambda) + 1) / (Math.sqrt(1 + this.data.matter * (redshift + 1) ** 3 / this.data.lambda) - 1)))
        else {
            for (var i = 0; i < 1000000; ++i)
                time += app.globalData.Mpc2km / this.data.hubble * (1 / (ratio + i) / Math.sqrt(this.data.matter * (1 + i / ratio) ** 3 + this.data.curvature * (1 + i / ratio) ** 2 + this.data.lambda) + 4 / (ratio + i + 0.5) / Math.sqrt(this.data.matter * (1 + (i + 0.5) / ratio) ** 3 + this.data.curvature * (1 + (i + 0.5) / ratio) ** 2 + this.data.lambda) + 1 / (ratio + i + 1) / Math.sqrt(this.data.matter * (1 + (i + 1) / ratio) ** 3 + this.data.curvature * (1 + (i + 1) / ratio) ** 2 + this.data.lambda)) / 6
        }
        return time
    },
    distanceCalculation(redshift) {
        if (redshift == 0)
            return 0
        var distance = 0, ratio = (redshift == Infinity ? 100 : 1000000 / redshift)
        for (var i = 0; i < 1000000; ++i)
            distance += app.globalData.Mpc2km / this.data.hubble * app.globalData.c / ratio * (1 / Math.sqrt(this.data.matter * (1 + i / ratio) ** 3 + this.data.curvature * (1 + i / ratio) ** 2 + this.data.lambda) + 4 / Math.sqrt(this.data.matter * (1 + (i + 0.5) / ratio) ** 3 + this.data.curvature * (1 + (i + 0.5) / ratio) ** 2 + this.data.lambda) + 1 / Math.sqrt(this.data.matter * (1 + (i + 1) / ratio) ** 3 + this.data.curvature * (1 + (i + 1) / ratio) ** 2 + this.data.lambda)) / 6
        return distance
    },
    setHubble(e) {
        this.setData({
            hubble: Number(e.detail.value),
            showBasicResult: false
        })
    },
    setMatter(e) {
        this.setData({
            matter: Number(e.detail.value),
            curvature: Math.abs(1 - e.detail.value - this.data.lambda) < 1e-13 ? 0 : 1 - e.detail.value - this.data.lambda,
            curvatureDisplay: Math.abs(1 - e.detail.value - this.data.lambda) < 1e-13 ? app.scientificDisplay(0) : app.scientificDisplay(1 - e.detail.value - this.data.lambda),
            showBasicResult: false
        })
    },
    setLambda(e) {
        this.setData({
            lambda: Number(e.detail.value),
            curvature: Math.abs(1 - this.data.matter - e.detail.value) < 1e-13 ? 0 : 1 - this.data.matter - e.detail.value,
            curvatureDisplay: Math.abs(1 - this.data.matter - e.detail.value) < 1e-13 ? app.scientificDisplay(0) : app.scientificDisplay(1 - this.data.matter - e.detail.value),
            showBasicResult: false
        })
    },
    obsData() {
        var _this = this
        wx.navigateTo({
            url: 'observation/observation?hubble=' + this.data.hubble + '&matter=' + this.data.matter + '&lambda=' + this.data.lambda + '&curvature=' + this.data.curvature,
            events: {
                recData(data) {
                    _this.setData({
                        hubble: data.hubble,
                        hubbleDisplay: data.hubble,
                        matter: data.matter,
                        matterDisplay: data.matter,
                        lambda: data.lambda,
                        lambdaDisplay: data.lambda,
                        curvature: data.curvature,
                        curvatureDisplay: app.scientificDisplay(data.curvature),
                        showBasicResult: false
                    })
                },
            }
        })
        wx.setStorageSync("hubble", this.data.hubble)
        wx.setStorageSync("matter", this.data.matter)
        wx.setStorageSync("lambda", this.data.lambda)
    },
    startBasicCalculation() {
        if (this.data.showBasicResult || this.data.hubble <= 0 || this.data.matter < 0 || this.data.lambda < 0)
            return
        if (this.data.matter == 0)
            this.setData({ matterDisplay: '0' })
        if (this.data.lambda == 0)
            this.setData({ lambdaDisplay: '0' })
        this.setData({ basicLoading: true })
        wx.setStorageSync("hubble", this.data.hubble)
        wx.setStorageSync("matter", this.data.matter)
        wx.setStorageSync("lambda", this.data.lambda)
        var age = this.timeCalculation(Infinity)
        this.setData({
            age,
            ageDisplay: app.scientificDisplay(age, "time", app.globalData.timeIndex),
            basicLoading: false,
            showBasicResult: true,
            showRedshiftResult: false
        })
    },
    twoRedshiftChange(e) { this.setData({ twoRedshift: e.detail.value, showRedshiftResult: !e.detail.value && this.data.showRedshiftResult }) },
    setRedshift(e) {
        var obj = { showRedshiftResult: false }
        obj["redshift" + e.target.id] = e.detail.value
        obj["redshift" + e.target.id + "Plus"] = 1 + Number(e.detail.value)
        this.setData(obj)
    },
    startRedshiftCalculation() {
        if (this.data.showRedshiftResult || this.data.redshift0 <= 0 || this.data.redshift1 <= 0)
            return
        this.setData({ redshiftLoading: true })
        var lookbackTime1 = this.timeCalculation(Number(this.data.redshift1)), comoving1 = this.distanceCalculation(Number(this.data.redshift1)), angular
        if (this.data.curvature == 0)
            angular = comoving1 / this.data.redshift1Plus
        else if (this.data.curvature < 0)
            angular = Math.sin(comoving1 * this.data.hubble / app.globalData.Mpc2km / app.globalData.c * Math.sqrt(-this.data.curvature)) * app.globalData.c / Math.sqrt(-this.data.curvature) / this.data.hubble * app.globalData.Mpc2km / this.data.redshift1Plus
        else
            angular = Math.sinh(comoving1 * this.data.hubble / app.globalData.Mpc2km / app.globalData.c * Math.sqrt(this.data.curvature)) * app.globalData.c / Math.sqrt(this.data.curvature) / this.data.hubble * app.globalData.Mpc2km / this.data.redshift1Plus
        this.setData({
            redshiftAge1: this.data.age - lookbackTime1,
            redshiftAge1Display: app.scientificDisplay(this.data.age - lookbackTime1, "time", app.globalData.timeIndex),
            lookbackTime1,
            lookbackTime1Display: app.scientificDisplay(lookbackTime1, "time", app.globalData.timeIndex),
            redshift1Hubble: app.scientificDisplay(this.data.hubble * Math.sqrt(this.data.matter * this.data.redshift1Plus ** 3 + this.data.curvature * this.data.redshift1Plus ** 2 + this.data.lambda)),
            comoving1,
            comoving1Display: app.scientificDisplay(comoving1, "length", app.globalData.lengthIndex),
            angular,
            angularDisplay: app.scientificDisplay(angular, "length", app.globalData.lengthIndex),
            luminosity: angular * this.data.redshift1Plus ** 2,
            luminosityDisplay: app.scientificDisplay(angular * this.data.redshift1Plus ** 2, "length", app.globalData.lengthIndex),
        })
        if (this.data.twoRedshift) {
            var lookbackTime0 = this.timeCalculation(Number(this.data.redshift0)), comoving0 = this.distanceCalculation(Number(this.data.redshift0))
            this.setData({
                redshiftAge0: this.data.age - lookbackTime0,
                redshiftAge0Display: app.scientificDisplay(this.data.age - lookbackTime0, "time", app.globalData.timeIndex),
                lookbackTime0,
                lookbackTime0Display: app.scientificDisplay(lookbackTime0, "time", app.globalData.timeIndex),
                timeDifference: app.scientificDisplay(lookbackTime1 - lookbackTime0, "time", app.globalData.timeIndex),
                redshift0Hubble: app.scientificDisplay(this.data.hubble * Math.sqrt(this.data.matter * this.data.redshift0Plus ** 3 + this.data.curvature * this.data.redshift0Plus ** 2 + this.data.lambda)),
                comoving0,
                comoving0Display: app.scientificDisplay(comoving0, "length", app.globalData.lengthIndex),
                comovingDifference: app.scientificDisplay(comoving1 - comoving0, "length", app.globalData.lengthIndex)
            })
        }
        this.setData({
            redshiftLoading: false,
            showRedshiftResult: true,
            angleDisplay: '',
            lengthDisplay: ''
        })
    },
    angleLengthTypeChange(e) {
        if (e.detail.column == 0) {
            var angleLengthRange = this.data.angleLengthRange
            angleLengthRange[1] = e.detail.value ? app.globalData.length : app.globalData.angle
            this.setData({ angleLengthRange })
        }
    },
    angleLengthChange(e) {
        var obj = {}
        obj["angleLengthIndex" + e.target.id] = e.detail.value
        this.setData(obj)
        this.angleLengthCal()
    },
    angleLengthCal(e) {
        var input = e == undefined ? this.data.angleLengthInput : e.detail.value
        if (this.data.angleLengthIndex0[0] == 0) {
            var angleOutput = (input / app.globalData.angleRatio[this.data.angleLengthIndex0[1]])
            var lengthOutput = angleOutput * this.data.angular
        }
        else {
            var lengthOutput = (input / app.globalData.lengthRatio[this.data.angleLengthIndex0[1]])
            var angleOutput = lengthOutput / this.data.angular
        }
        this.setData({
            angleLengthInput: input,
            angleOutput,
            angleDisplay: angleOutput == 0 ? '' : app.scientificDisplay(angleOutput, "angle", this.data.angleLengthIndex1),
            lengthOutput,
            lengthDisplay: lengthOutput == 0 ? '' : app.scientificDisplay(lengthOutput, "length", this.data.angleLengthIndex2)
        })
    }
})
