import Foundation

@objcMembers
public class EightChar: NSObject {
    public static var MONTH_ZHI: [String] = ["", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥", "子", "丑"]
    public static var CHANG_SHENG: [String] = ["长生", "沐浴", "冠带", "临官", "帝旺", "衰", "病", "死", "墓", "绝", "胎", "养"]
    public static var CHANG_SHENG_OFFSET: [String: Int] = [
        "甲": 1,
        "丙": 10,
        "戊": 10,
        "庚": 7,
        "壬": 4,
        "乙": 6,
        "丁": 9,
        "己": 9,
        "辛": 0,
        "癸": 3
    ]

    public var sect: Int
    private var _lunar: Lunar

    public var lunar: Lunar {
        get {
            _lunar
        }
    }

    public init(lunar: Lunar) {
        sect = 2
        _lunar = lunar
    }

    public class func fromLunar(lunar: Lunar) -> EightChar {
        EightChar(lunar: lunar)
    }

    public var year: String {
        get {
            _lunar.yearInGanZhiExact
        }
    }

    public var yearGan: String {
        get {
            _lunar.yearGanExact
        }
    }

    public var yearZhi: String {
        get {
            _lunar.yearZhiExact
        }
    }

    public var yearHideGan: [String] {
        get {
            LunarUtil.ZHI_HIDE_GAN[yearZhi]!
        }
    }

    public var yearWuXing: String {
        get {
            LunarUtil.WU_XING_GAN[yearGan]! + LunarUtil.WU_XING_ZHI[yearZhi]!
        }
    }

    public var yearNaYin: String {
        get {
            LunarUtil.NAYIN[year]!
        }
    }

    public var month: String {
        get {
            _lunar.monthInGanZhiExact
        }
    }

    public var monthGan: String {
        get {
            _lunar.monthGanExact
        }
    }

    public var monthZhi: String {
        get {
            _lunar.monthZhiExact
        }
    }

    public var monthHideGan: [String] {
        get {
            LunarUtil.ZHI_HIDE_GAN[monthZhi]!
        }
    }

    public var monthWuXing: String {
        get {
            LunarUtil.WU_XING_GAN[monthGan]! + LunarUtil.WU_XING_ZHI[monthZhi]!
        }
    }

    public var monthNaYin: String {
        get {
            LunarUtil.NAYIN[month]!
        }
    }

    public var day: String {
        get {
            2 == sect ? lunar.dayInGanZhiExact2 : lunar.dayInGanZhiExact
        }
    }

    public var dayGan: String {
        get {
            2 == sect ? _lunar.dayGanExact2 : lunar.dayGanExact
        }
    }

    public var dayGanIndex: Int {
        get {
            2 == sect ? _lunar.dayGanIndexExact2 : lunar.dayGanIndexExact
        }
    }

    public var dayZhi: String {
        get {
            2 == sect ? _lunar.dayZhiExact2 : lunar.dayZhiExact
        }
    }

    public var dayZhiIndex: Int {
        get {
            2 == sect ? _lunar.dayZhiIndexExact2 : lunar.dayZhiIndexExact
        }
    }

    public var dayHideGan: [String] {
        get {
            LunarUtil.ZHI_HIDE_GAN[dayZhi]!
        }
    }

    public var dayWuXing: String {
        get {
            LunarUtil.WU_XING_GAN[dayGan]! + LunarUtil.WU_XING_ZHI[dayZhi]!
        }
    }

    public var dayNaYin: String {
        get {
            LunarUtil.NAYIN[day]!
        }
    }

    public var time: String {
        get {
            _lunar.timeInGanZhi
        }
    }

    public var timeGan: String {
        get {
            _lunar.timeGan
        }
    }

    public var timeZhi: String {
        get {
            _lunar.timeZhi
        }
    }

    public var timeHideGan: [String] {
        get {
            LunarUtil.ZHI_HIDE_GAN[timeZhi]!
        }
    }

    public var timeWuXing: String {
        get {
            LunarUtil.WU_XING_GAN[timeGan]! + LunarUtil.WU_XING_ZHI[timeZhi]!
        }
    }

    public var timeNaYin: String {
        get {
            LunarUtil.NAYIN[time]!
        }
    }

    public func getYun(gender: Int, sect: Int = 1) -> Yun {
        Yun(eightChar: self, gender: gender, sect: sect)
    }

    public var yearXun: String {
        get {
            _lunar.yearXunExact
        }
    }

    public var yearXunKong: String {
        get {
            _lunar.yearXunKongExact
        }
    }

    public var monthXun: String {
        get {
            _lunar.monthXunExact
        }
    }

    public var monthXunKong: String {
        get {
            _lunar.monthXunKongExact
        }
    }

    public var dayXun: String {
        get {
            2 == sect ? _lunar.dayXunExact2 : _lunar.dayXunExact
        }
    }

    public var dayXunKong: String {
        get {
            2 == sect ? _lunar.dayXunKongExact2 : _lunar.dayXunKongExact
        }
    }

    public var timeXun: String {
        get {
            _lunar.timeXun
        }
    }

    public var timeXunKong: String {
        get {
            _lunar.timeXunKong
        }
    }

    private func getDiShi(zhiIndex: Int) -> String {
        var index = EightChar.CHANG_SHENG_OFFSET[dayGan]! + (dayGanIndex % 2 == 0 ? zhiIndex : -zhiIndex)
        if index >= 12 {
            index -= 12
        }
        if index < 0 {
            index += 12
        }
        return EightChar.CHANG_SHENG[index]
    }

    public var yearDiShi: String {
        get {
            getDiShi(zhiIndex: _lunar.yearZhiIndexExact)
        }
    }

    public var monthDiShi: String {
        get {
            getDiShi(zhiIndex: _lunar.monthZhiIndexExact)
        }
    }

    public var dayDiShi: String {
        get {
            getDiShi(zhiIndex: _lunar.dayZhiIndex)
        }
    }

    public var timeDiShi: String {
        get {
            getDiShi(zhiIndex: _lunar.timeZhiIndex)
        }
    }

    private func getShiShenZhi(zhi: String) -> [String] {
        let hideGan = LunarUtil.ZHI_HIDE_GAN[zhi]!
        var l = [String]()
        for gan in hideGan {
            l.append(LunarUtil.SHI_SHEN[dayGan + gan]!)
        }
        return l
    }

    public var yearShiShenGan: String {
        get {
            LunarUtil.SHI_SHEN[dayGan + yearGan]!
        }
    }

    public var monthShiShenGan: String {
        get {
            LunarUtil.SHI_SHEN[dayGan + monthGan]!
        }
    }

    public var dayShiShenGan: String {
        get {
            "日主"
        }
    }

    public var timeShiShenGan: String {
        get {
            LunarUtil.SHI_SHEN[dayGan + timeGan]!
        }
    }

    public var yearShiShenZhi: [String] {
        get {
            getShiShenZhi(zhi: yearZhi)
        }
    }

    public var monthShiShenZhi: [String] {
        get {
            getShiShenZhi(zhi: monthZhi)
        }
    }

    public var dayShiShenZhi: [String] {
        get {
            getShiShenZhi(zhi: dayZhi)
        }
    }

    public var timeShiShenZhi: [String] {
        get {
            getShiShenZhi(zhi: timeZhi)
        }
    }

    public var taiYuan: String {
        get {
            var ganIndex = _lunar.monthGanIndexExact + 1
            if ganIndex >= 10 {
                ganIndex -= 10
            }
            var zhiIndex = _lunar.monthZhiIndexExact + 3
            if zhiIndex >= 12 {
                zhiIndex -= 12
            }
            return LunarUtil.GAN[ganIndex + 1] + LunarUtil.ZHI[zhiIndex + 1]
        }
    }

    public var taiYuanNaYin: String {
        get {
            LunarUtil.NAYIN[taiYuan]!
        }
    }

    public var taiXi: String {
        get {
            let ganIndex = (2 == sect) ? lunar.dayGanIndexExact2 : lunar.dayGanIndexExact
            let zhiIndex = (2 == sect) ? lunar.dayZhiIndexExact2 : lunar.dayZhiIndexExact
            return LunarUtil.HE_GAN_5[ganIndex] + LunarUtil.HE_ZHI_6[zhiIndex]
        }
    }

    public var taiXiNaYin: String {
        get {
            LunarUtil.NAYIN[taiXi]!
        }
    }

    public var mingGong: String {
        get {
            var monthZhiIndex = 0
            var timeZhiIndex = 0
            for i in (0..<EightChar.MONTH_ZHI.count) {
                if monthZhi == EightChar.MONTH_ZHI[i] {
                    monthZhiIndex = i
                    break
                }
            }
            for i in (0..<EightChar.MONTH_ZHI.count) {
                let zhi = EightChar.MONTH_ZHI[i]
                if timeZhi == zhi {
                    timeZhiIndex = i
                    break
                }
            }
            var offset = monthZhiIndex + timeZhiIndex
            offset = (offset >= 14 ? 26 : 14) - offset
            var ganIndex = (_lunar.yearGanIndexExact + 1) * 2 + offset
            while (ganIndex > 10) {
                ganIndex -= 10
            }
            return LunarUtil.GAN[ganIndex] + EightChar.MONTH_ZHI[offset]
        }
    }

    public var mingGongNaYin: String {
        get {
            LunarUtil.NAYIN[mingGong]!
        }
    }

    public var shenGong: String {
        get {
            var monthZhiIndex = 0
            var timeZhiIndex = 0
            for i in (0..<EightChar.MONTH_ZHI.count) {
                if monthZhi == EightChar.MONTH_ZHI[i] {
                    monthZhiIndex = i
                    break
                }
            }
            for i in (0..<LunarUtil.ZHI.count) {
                let zhi = LunarUtil.ZHI[i]
                if timeZhi == zhi {
                    timeZhiIndex = i
                    break
                }
            }
            var offset = monthZhiIndex + timeZhiIndex
            if offset > 12 {
                offset -= 12
            }
            var ganIndex = (_lunar.yearGanIndexExact + 1) * 2 + offset
            while (ganIndex > 10) {
                ganIndex -= 10
            }
            return LunarUtil.GAN[ganIndex] + EightChar.MONTH_ZHI[offset]
        }
    }

    public var shenGongNaYin: String {
        get {
            LunarUtil.NAYIN[shenGong]!
        }
    }
}
