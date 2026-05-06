import Foundation

@objcMembers
public class SolarSeason: NSObject {
    public static var MONTH_COUNT = 3

    private var _year: Int
    private var _month: Int

    public var year: Int {
        get {
            _year
        }
    }

    public var month: Int {
        get {
            _month
        }
    }

    public init(year: Int, month: Int) {
        _year = year
        _month = month
    }

    public init(date: Date) {
        let calendar = Calendar.current
        _year = calendar.component(.year, from: date)
        _month = calendar.component(.month, from: date)
    }

    public convenience override init() {
        self.init(date: Date())
    }

    public class func fromYm(year: Int, month: Int) -> SolarSeason {
        SolarSeason(year: year, month: month)
    }

    public class func fromDate(date: Date) -> SolarSeason {
        SolarSeason(date: date)
    }

    public var index: Int {
        get {
            Int(ceil(Double(_month) / Double(SolarSeason.MONTH_COUNT)))
        }
    }

    public var months: [SolarMonth] {
        get {
            var l = [SolarMonth]()
            let offset = index - 1
            for i in (0..<SolarSeason.MONTH_COUNT) {
                l.append(SolarMonth(year: _year, month: SolarSeason.MONTH_COUNT * offset + i + 1))
            }
            return l
        }
    }

    public func next(seasons: Int) -> SolarSeason {
        let m = SolarMonth.fromYm(year: _year, month: _month).next(months: seasons * SolarSeason.MONTH_COUNT)
        return SolarSeason.fromYm(year: m.year, month: m.month)
    }

    public override var description: String {
        get {
            "\(_year).\(index)"
        }
    }

    public var fullString: String {
        get {
            "\(_year)年\(index)季度"
        }
    }

}
