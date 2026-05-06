import Foundation

@objcMembers
public class SolarHalfYear: NSObject {
    public static var MONTH_COUNT = 6

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

    public class func fromYm(year: Int, month: Int) -> SolarHalfYear {
        SolarHalfYear(year: year, month: month)
    }

    public class func fromDate(date: Date) -> SolarHalfYear {
        SolarHalfYear(date: date)
    }

    public var index: Int {
        get {
            Int(ceil(Double(_month) / Double(SolarHalfYear.MONTH_COUNT)))
        }
    }

    public var months: [SolarMonth] {
        var l = [SolarMonth]()
        let offset = index - 1
        for i in (0..<SolarHalfYear.MONTH_COUNT) {
            l.append(SolarMonth(year: _year, month: SolarHalfYear.MONTH_COUNT * offset + i + 1))
        }
        return l
    }

    public func next(halfYears: Int) -> SolarHalfYear {
        let m = SolarMonth.fromYm(year: _year, month: _month).next(months: halfYears * SolarHalfYear.MONTH_COUNT)
        return SolarHalfYear.fromYm(year: m.year, month: m.month)
    }

    public override var description: String {
        "\(_year).\(index)"
    }

    public var fullString: String {
        get {
            "\(_year)年\(1 == index ? "上" : "下")半年"
        }
    }

}
