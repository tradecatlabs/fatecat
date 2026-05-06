import Foundation

@objcMembers
public class LunarTime: NSObject {
    private var _ganIndex: Int
    private var _zhiIndex: Int
    private var _lunar: Lunar

    public var ganIndex: Int {
        _ganIndex
    }

    public var zhiIndex: Int {
        _zhiIndex
    }

    public var lunar: Lunar {
        _lunar
    }

    public init(lunarYear: Int, lunarMonth: Int, lunarDay: Int, hour: Int = 0, minute: Int = 0, second: Int = 0) {
        _lunar = Lunar.fromYmdHms(lunarYear: lunarYear, lunarMonth: lunarMonth, lunarDay: lunarDay, hour: hour, minute: minute, second: second)
        _zhiIndex = LunarUtil.getTimeZhiIndex(hm: String(format: "%02d:%02d", hour, minute))
        _ganIndex = (_lunar.dayGanIndexExact % 5 * 2 + _zhiIndex) % 10
    }

    public class func fromYmdHms(lunarYear: Int, lunarMonth: Int, lunarDay: Int, hour: Int = 0, minute: Int = 0, second: Int = 0) -> LunarTime {
        LunarTime(lunarYear: lunarYear, lunarMonth: lunarMonth, lunarDay: lunarDay, hour: hour, minute: minute, second: second)
    }

    public var gan: String {
        LunarUtil.GAN[_ganIndex + 1]
    }

    public var zhi: String {
        LunarUtil.ZHI[_zhiIndex + 1]
    }

    public var ganZhi: String {
        "\(gan)\(zhi)"
    }

    public var shengXiao: String {
        LunarUtil.SHENG_XIAO[_zhiIndex + 1]
    }

    public var naYin: String {
        LunarUtil.NAYIN[ganZhi]!
    }

    public var positionXi: String {
        LunarUtil.POSITION_XI[_ganIndex + 1]
    }

    public var positionXiDesc: String {
        LunarUtil.POSITION_DESC[positionXi]!
    }

    public var positionYangGui: String {
        LunarUtil.POSITION_YANG_GUI[_ganIndex + 1]
    }

    public var positionYangGuiDesc: String {
        LunarUtil.POSITION_DESC[positionYangGui]!
    }

    public var positionYinGui: String {
        LunarUtil.POSITION_YIN_GUI[_ganIndex + 1]
    }

    public var positionYinGuiDesc: String {
        LunarUtil.POSITION_DESC[positionYinGui]!
    }

    public var positionFu: String {
        getPositionFu(sect: 2)
    }

    public var positionFuDesc: String {
        getPositionFuDesc(sect: 2)
    }

    public func getPositionFu(sect: Int) -> String {
        (1 == sect ? LunarUtil.POSITION_FU : LunarUtil.POSITION_FU_2)[_ganIndex + 1]
    }

    public func getPositionFuDesc(sect: Int) -> String {
        LunarUtil.POSITION_DESC[getPositionFu(sect: sect)]!
    }

    public var positionCai: String {
        LunarUtil.POSITION_CAI[_ganIndex + 1]
    }

    public var positionCaiDesc: String {
        LunarUtil.POSITION_DESC[positionCai]!
    }

    public var tianShen: String {
        LunarUtil.TIAN_SHEN[(_zhiIndex + LunarUtil.ZHI_TIAN_SHEN_OFFSET[_lunar.dayZhiExact]!) % 12 + 1]
    }

    public var tianShenType: String {
        LunarUtil.TIAN_SHEN_TYPE[tianShen]!
    }

    public var tianShenLuck: String {
        LunarUtil.TIAN_SHEN_TYPE_LUCK[tianShenType]!
    }

    public var yi: [String] {
        LunarUtil.getTimeYi(dayGanZhi: _lunar.dayInGanZhiExact, timeGanZhi: ganZhi)
    }

    public var ji: [String] {
        LunarUtil.getTimeJi(dayGanZhi: _lunar.dayInGanZhiExact, timeGanZhi: ganZhi)
    }

    public var chong: String {
        LunarUtil.CHONG[_zhiIndex]
    }

    public var sha: String {
        LunarUtil.SHA[zhi]!
    }

    public var chongShengXiao: String {
        for i in 0 ..< LunarUtil.ZHI.count {
            if LunarUtil.ZHI[i] == chong {
                return LunarUtil.SHENG_XIAO[i]
            }
        }
        return ""
    }

    public var chongGan: String {
        LunarUtil.CHONG_GAN[_ganIndex]
    }

    public var chongGanTie: String {
        LunarUtil.CHONG_GAN_TIE[_ganIndex]
    }

    public var chongDesc: String {
        "(\(chongGan)\(chong))\(chongShengXiao)"
    }

    override public var description: String {
        "\(ganZhi)"
    }

    public var xun: String {
        LunarUtil.getXun(ganZhi: ganZhi)
    }

    public var xunKong: String {
        LunarUtil.getXunKong(ganZhi: ganZhi)
    }

    public var nineStar: NineStar {
        let solarYmd = lunar.solar.ymd
        let jieQi = lunar.jieQiTable
        let asc = solarYmd >= jieQi["冬至"]!.ymd && solarYmd < jieQi["夏至"]!.ymd
        var start = asc ? 7 : 3
        if "子午卯酉".contains(lunar.dayZhi) {
            start = asc ? 1 : 9
        } else if "辰戌丑未".contains(lunar.dayZhi) {
            start = asc ? 4 : 6
        }
        var index = asc ? start + _zhiIndex - 1 : start - _zhiIndex - 1
        if index > 8 {
            index -= 9
        }
        if index < 0 {
            index += 9
        }
        return NineStar(index: index)
    }

    public var minHm: String {
        let hour = lunar.hour
        if hour < 1 {
            return "00:00"
        } else if hour > 22 {
            return "23:00"
        }
        return String(format: "%02d:00", hour % 2 == 0 ? hour - 1 : hour)
    }

    public var maxHm: String {
        let hour = lunar.hour
        if hour < 1 {
            return "00:59"
        } else if hour > 22 {
            return "23:59"
        }
        return String(format: "%02d:59", hour % 2 == 0 ? hour : hour + 1)
    }
}
