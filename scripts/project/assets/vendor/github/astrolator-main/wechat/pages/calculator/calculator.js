var app = getApp()
var pageData = {
    data: {
        tabs: [
            { title: 'Unit' },
            { title: 'Dynamics' },
            { title: 'General Relativity' },
            { title: 'Radiation' },
            { title: 'Accretion' },
        ],
        height: ["1050", "206", "1213", "412", "205"],
        minHeight: String(app.globalData.sysInfo.windowHeight - app.globalData.sysInfo.statusBarHeight - 259),
        activeTab: '0',
        scientific: app.globalData.scientific,
        precisionIndex: app.globalData.precisionIndex,
        lengthMain: app.globalData.lengthMain,
        lengthSub: app.globalData.lengthSub,
        massMain: app.globalData.massMain,
        massSub: app.globalData.massSub,
        powerMain: app.globalData.powerMain,
        powerSub: app.globalData.powerSub,
        name: ["orbit", "radius", "chirp", "precession", "peters", "photon", "eddinR", "eddinA"],
        inputNumber: [2, 1, 2, 3, 4, 1, 1, 2],
        indexNumber: [3, 2, 3, 4, 8, 4, 2, 2],
        orbitIndex0: '0',
        orbitIndex1: '9',
        orbitIndex2: '0',
        radiusIndex0: '0',
        radiusIndex1: '5',
        chirpIndex0: '0',
        chirpIndex1: '0',
        chirpIndex2: '0',
        precessionIndex0: '0',
        precessionIndex1: '0',
        PN: ["PN 1", "PN 2", "PN 1+2"],
        precessionIndex2: '0',
        precessionIndex3: '0',
        petersRange0: [app.globalData.length, app.globalData.time],
        petersRange1: [app.globalData.energy, app.globalData.time],
        petersIndex0: '0',
        petersIndex1: '0',
        petersIndex2: '0',
        petersIndex3: ['0', '0'],
        petersIndex4: '0',
        petersIndex5: ['0', '0'],
        petersIndex6: '0',
        petersIndex7: '0',
        photonRange: [
            ["Wavelength", "Frequency", "Energy", "Temperature"],
            app.globalData.length
        ],
        photonRangeDisplay: [
            app.globalData.length,
            app.globalData.frequency,
            app.globalData.energy,
            app.globalData.temperature
        ],
        photonIndex0: [0, 1],
        photonIndex1: '1',
        photonIndex2: '0',
        photonIndex3: '0',
        eddinRIndex0: '0',
        eddinRIndex1: '0',
        eddinARange: [app.globalData.mass, app.globalData.time],
        eddinAIndex0: '0',
        eddinAIndex1: [0, 0],
    },
    mixins: [require('../../utils/themeChanged')],
    onShow() {
        if (this.data.scientific != app.globalData.scientific || this.data.precisionIndex != app.globalData.precisionIndex) {
            var obj = { scientific: app.globalData.scientific, precisionIndex: app.globalData.precisionIndex }
            for (var i = 2; i < app.globalData.settings.length; ++i)
                obj[app.globalData.settings[i] + "Display"] = app.scientificDisplay(this.data[app.globalData.settings[i] + "Output"], app.globalData.settings[i], this.data[app.globalData.settings[i] + "Index1"])
            obj["orbitDisplay"] = app.scientificDisplay(this.data.orbitOutput, "time", this.data.orbitIndex2)
            obj["radiusDisplay"] = app.scientificDisplay(this.data.radiusOutput, "length", this.data.radiusIndex1)
            obj["chirpDisplay"] = app.scientificDisplay(this.data.chirpOutput, "mass", this.data.chirpIndex2)
            obj["precessionDisplay"] = app.scientificDisplay(this.data.precessionOutput, "angle", this.data.precessionIndex3)
            if (this.data.petersOutput.length != 0)
                obj["petersDisplay"] = [app.scientificDisplay(this.data.petersOutput[0], "length", this.data.petersIndex3[0]), app.scientificDisplay(this.data.petersOutput[1]), app.scientificDisplay(this.data.petersOutput[2], "energy", this.data.petersIndex5[0]),
                app.scientificDisplay(this.data.petersOutput[3], "energy", this.data.petersIndex6), app.scientificDisplay(this.data.petersOutput[4], "time", this.data.petersIndex7)]
            if (this.data.photonOutput.length != 0)
                obj["photonDisplay"] = [app.scientificDisplay(this.data.photonOutput[0], "length", this.data.photonIndex1), app.scientificDisplay(this.data.photonOutput[1], "frequency", this.data.photonIndex2), app.scientificDisplay(this.data.photonOutput[2], "energy", this.data.photonIndex3), app.scientificDisplay(this.data.photonOutput[3], "temperature")]
            obj["eddinRDisplay"] = app.scientificDisplay(this.data.eddinROutput, "power", this.data.eddinRIndex1)
            obj["eddinADisplay"] = app.scientificDisplay(this.data.eddinAOutput, "length", this.data.eddinAIndex2)
            this.setData(obj)
        }
    },
    onChange(e) { this.setData({ activeTab: e.detail.index }) },
    orbitCal() {
        if (this.data.orbitInput0 == 0 || this.data.orbitInput1 == 0)
            return this.setData({ orbitOutput: 0, orbitDisplay: '' })
        var output = 2 * Math.PI * (this.data.orbitInput1 / app.globalData.lengthRatio[this.data.orbitIndex1]) ** 1.5 / (app.globalData.G * this.data.orbitInput0 / app.globalData.massRatio[this.data.orbitIndex0]) ** 0.5
        this.setData({ orbitOutput: output, orbitDisplay: app.scientificDisplay(output, "time", this.data.orbitIndex2) })
    },
    radiusCal() {
        var output = this.data.radiusInput0 / app.globalData.massRatio[this.data.radiusIndex0] * 2 * app.globalData.G / app.globalData.c ** 2
        this.setData({ radiusOutput: output, radiusDisplay: app.scientificDisplay(output, "length", this.data.radiusIndex1) })
    },
    chirpCal() {
        if (this.data.chirpInput0 == '' || this.data.chirpInput1 == '')
            return this.setData({ chirpOutput: 0, chirpDisplay: '' })
        var M0 = Number(this.data.chirpInput0) / app.globalData.massRatio[this.data.chirpIndex0], M1 = Number(this.data.chirpInput1) / app.globalData.massRatio[this.data.chirpIndex1]
        var chirpOutput = (M0 * M1) ** 0.6 / (M0 + M1) ** 0.2
        this.setData({
            chirpOutput,
            chirpDisplay: app.scientificDisplay(chirpOutput, "mass", this.data.chirpIndex2)
        })
    },
    precessionCal() {
        if (this.data.precessionInput0 == 0 || this.data.precessionInput1 == 0 || this.data.precessionInput2 === '' || this.data.precessionInput2 > 1)
            return this.setData({ precessionOutput: 0, precessionDisplay: '' })
        var output = 0, coeff = app.globalData.G * this.data.precessionInput0 / app.globalData.massRatio[this.data.precessionIndex0] / app.globalData.c ** 2 / this.data.precessionInput1 * app.globalData.lengthRatio[this.data.precessionIndex1] / (1 - this.data.precessionInput2 ** 2)
        if (this.data.precessionIndex2 != 1)
            output += 6 * Math.PI * coeff
        if (this.data.precessionIndex2 != 0)
            output += Math.PI * (28 - this.data.precessionInput2 ** 2) * coeff ** 2 / 2
        this.setData({
            precessionOutput: output,
            precessionDisplay: app.scientificDisplay(output, "angle", this.data.precessionIndex3)
        })
    },
    petersCal() {
        if (this.data.petersInput0 == 0 || this.data.petersInput1 == 0 || this.data.petersInput2 == 0 || this.data.petersInput3 === '' || this.data.petersInput3 >= 1)
            return this.setData({ petersOutput: [], petersDisplay: [] })
        var m1 = this.data.petersInput0 / app.globalData.massRatio[this.data.petersIndex0], m2 = this.data.petersInput1 / app.globalData.massRatio[this.data.petersIndex1], a = this.data.petersInput2 / app.globalData.lengthRatio[this.data.petersIndex2], e = this.data.petersInput3
        var coeff = app.globalData.G ** 3 * m1 * m2 * (m1 + m2) / app.globalData.c ** 5 / a ** 3 / (1 - e ** 2) ** 2.5
        var output = [-64 / 5 * coeff / (1 - e ** 2) * (1 + 73 / 24 * e ** 2 + 37 / 96 * e ** 4) / app.globalData.timeRatio[this.data.petersIndex3[1]],
        -304 / 15 * e * coeff / a * (1 + 121 / 304 * e ** 2) / app.globalData.timeRatio[this.data.petersIndex4],
        -32 / 5 * app.globalData.G * m1 * m2 * coeff / a ** 2 / (1 - e ** 2) * (1 + 73 / 24 * e ** 2 + 37 / 96 * e ** 4) / app.globalData.timeRatio[this.data.petersIndex5[1]],
        -32 / 5 * app.globalData.G ** 0.5 * m1 * m2 / (m1 + m2) ** 0.5 * coeff / a ** 0.5 * (1 - e ** 2) ** 0.5 * (1 + 7 / 8 * e ** 2),
        5 / 64 / coeff * (1 - e ** 2) * a / (1 + 73 / 24 * e ** 2 + 37 / 96 * e ** 4)]
        this.setData({
            petersOutput: output,
            petersDisplay: [app.scientificDisplay(output[0], "length", this.data.petersIndex3[0]), app.scientificDisplay(output[1]), app.scientificDisplay(output[2], "energy", this.data.petersIndex5[0]),
            app.scientificDisplay(output[3], "energy", this.data.petersIndex6), app.scientificDisplay(output[4], "time", this.data.petersIndex7)]
        })
    },
    photonTypeChange(e) {
        if (e.detail.column == 0) {
            var photonRange = this.data.photonRange
            if (e.detail.value == 0)
                photonRange[1] = app.globalData.length
            else if (e.detail.value == 1)
                photonRange[1] = app.globalData.frequency
            else if (e.detail.value == 2)
                photonRange[1] = app.globalData.energy
            else
                photonRange[1] = app.globalData.temperature
            this.setData({ photonRange })
        }
    },
    photonCal() {
        var frequency
        if (this.data.photonInput0 == 0)
            return this.setData({ photonOutput: [], photonDisplay: [] })
        if (this.data.photonIndex0[0] == 0)
            frequency = app.globalData.c / this.data.photonInput0 * app.globalData.lengthRatio[this.data.photonIndex0[1]]
        else if (this.data.photonIndex0[0] == 1)
            frequency = this.data.photonInput0 / app.globalData.frequencyRatio[this.data.photonIndex0[1]]
        else if (this.data.photonIndex0[0] == 2)
            frequency = this.data.photonInput0 / app.globalData.energyRatio[this.data.photonIndex0[1]] / app.globalData.h
        else
            frequency = this.data.photonInput0 * app.globalData.k_B / app.globalData.energyRatio[this.data.photonIndex0[1]] / app.globalData.h
        var output = [app.globalData.c / frequency, frequency, app.globalData.h * frequency, app.globalData.h * frequency / app.globalData.k_B]
        this.setData({ photonOutput: output, photonDisplay: [app.scientificDisplay(output[0], "length", this.data.photonIndex1), app.scientificDisplay(output[1], "frequency", this.data.photonIndex2), app.scientificDisplay(output[2], "energy", this.data.photonIndex3), app.scientificDisplay(output[3], "temperature")] })
    },
    eddinRCal() {
        var output = 4 * Math.PI * app.globalData.G * app.globalData.m_p * app.globalData.c / app.globalData.sigma_T * this.data.eddinRInput0 / app.globalData.massRatio[this.data.eddinRIndex0]
        this.setData({ eddinROutput: output, eddinRDisplay: app.scientificDisplay(output, "power", this.data.eddinRIndex1[0]) })
    },
    eddinACal() {
        if (this.data.eddinAInput0 == 0 || this.data.eddinAInput1 == 0)
            return this.setData({ eddinAOutput: 0, eddinADisplay: '' })
        var output = 4 * Math.PI * app.globalData.G * app.globalData.m_p / app.globalData.c / app.globalData.sigma_T * this.data.eddinAInput0 / app.globalData.massRatio[this.data.eddinAIndex0] / this.data.eddinAInput1 / app.globalData.timeRatio[this.data.eddinAIndex1[1]]
        this.setData({ eddinAOutput: output, eddinADisplay: app.scientificDisplay(output, "mass", this.data.eddinAIndex1[0]) })
    }
}
for (var i = 2; i < app.globalData.settings.length; ++i) {
    (function (name) {
        pageData[name + "Change0"] = function (e) {
            var obj = {}
            obj[name + "Index0"] = e.detail.value
            this.setData(obj)
            this[name + "Cal"]()
        }
        pageData[name + "Change1"] = function (e) {
            var obj = {}
            obj[name + "Index1"] = e.detail.value
            this.setData(obj)
            this[name + "Cal"]()
        }
        pageData[name + "Cal"] = function (e) {
            var obj = {}
            var input = e == undefined ? this.data[name + "Input"] : e.detail.value
            obj[name + "Input"] = input
            obj[name + "Output"] = input == 0 ? 0 : (input /= app.globalData[name + "Ratio"][this.data[name + "Index0"]])
            obj[name + "Display"] = input == 0 ? '' : app.scientificDisplay(input, name, this.data[name + "Index1"])
            this.setData(obj)
        }
    })(app.globalData.settings[i])
    var n = app.globalData.settings[i]
    pageData.data[n] = app.globalData[n]
    pageData.data[n + "Input"] = ''
    pageData.data[n + "Index0"] = '0'
    pageData.data[n + "Index1"] = '1'
}
for (var i in pageData.data.name) {
    for (var j = 0; j < pageData.data.indexNumber[i]; ++j)
        (function (name, index) {
            pageData[name + "Change" + index] = function (e) {
                var obj = {}
                obj[name + "Index" + index] = e.detail.value
                this.setData(obj)
                this[name + "Cal"]()
            }
        })(pageData.data.name[i], j)
    for (var j = 0; j < pageData.data.inputNumber[i]; ++j) {
        (function (name, index) {
            pageData[name + "In" + index] = function (e) {
                var obj = {}
                obj[name + "Input" + index] = e.detail.value
                this.setData(obj)
                this[name + "Cal"]()
            }
        })(pageData.data.name[i], j)
        pageData.data[pageData.data.name[i] + "Input" + j] = ''
    }
}
Page(pageData)
