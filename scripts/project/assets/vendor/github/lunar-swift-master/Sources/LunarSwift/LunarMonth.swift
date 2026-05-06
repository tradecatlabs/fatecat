import Foundation

@objcMembers
public class LunarMonth: NSObject {
    private var _year: Int
    private var _month: Int
    private var _dayCount: Int
    private var _index: Int
    private var _zhiIndex: Int
    private var _firstJulianDay: Double

    public var year: Int {
        _year
    }

    public var month: Int {
        _month
    }

    public var dayCount: Int {
        _dayCount
    }

    public var index: Int {
        _index
    }

    public var zhiIndex: Int {
        _zhiIndex
    }

    public var ganIndex: Int {
        let offset = (LunarYear.fromYear(lunarYear: _year).ganIndex + 1) % 5 * 2
        return (abs(_month) - 1 + offset) % 10
    }

    public var firstJulianDay: Double {
        _firstJulianDay
    }

    public init(lunarYear: Int, lunarMonth: Int, dayCount: Int, firstJulianDay: Double, index: Int) {
        _year = lunarYear
        _month = lunarMonth
        _dayCount = dayCount
        _firstJulianDay = firstJulianDay
        _index = index
        _zhiIndex = (abs(lunarMonth) - 1 + LunarUtil.BASE_MONTH_ZHI_INDEX) % 12
    }

    public class func fromYm(lunarYear: Int, lunarMonth: Int) -> LunarMonth? {
        LunarYear.fromYear(lunarYear: lunarYear).getMonth(lunarMonth: lunarMonth)
    }

    public var leap: Bool {
        _month < 0
    }

    override public var description: String {
        var r = ""
        if leap {
            r = "闰"
        }
        let m = abs(_month)
        return "\(_year)年\(r)\(LunarUtil.MONTH[m])月(\(_dayCount))天"
    }

    public var gan: String {
        LunarUtil.GAN[ganIndex + 1]
    }

    public var zhi: String {
        LunarUtil.ZHI[_zhiIndex + 1]
    }

    public var ganZhi: String {
        "\(gan)\(zhi)"
    }

    public var positionXi: String {
        LunarUtil.POSITION_XI[ganIndex + 1]
    }

    public var positionXiDesc: String {
        LunarUtil.POSITION_DESC[positionXi]!
    }

    public var positionYangGui: String {
        LunarUtil.POSITION_YANG_GUI[ganIndex + 1]
    }

    public var positionYangGuiDesc: String {
        LunarUtil.POSITION_DESC[positionYangGui]!
    }

    public var positionYinGui: String {
        LunarUtil.POSITION_YIN_GUI[ganIndex + 1]
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
        (1 == sect ? LunarUtil.POSITION_FU : LunarUtil.POSITION_FU_2)[ganIndex + 1]
    }

    public func getPositionFuDesc(sect: Int) -> String {
        LunarUtil.POSITION_DESC[getPositionFu(sect: sect)]!
    }

    public var positionCai: String {
        LunarUtil.POSITION_CAI[ganIndex + 1]
    }

    public var positionCaiDesc: String {
        LunarUtil.POSITION_DESC[positionCai]!
    }

    public var nineStar: NineStar {
        let index = LunarYear.fromYear(lunarYear: _year).zhiIndex % 3
        let m = abs(_month)
        let monthZhiIndex = (13 + m) % 12
        var n = 27 - index * 3
        if monthZhiIndex < LunarUtil.BASE_MONTH_ZHI_INDEX {
            n -= 3
        }
        return NineStar(index: (n - monthZhiIndex) % 9 - 1)
    }
}
