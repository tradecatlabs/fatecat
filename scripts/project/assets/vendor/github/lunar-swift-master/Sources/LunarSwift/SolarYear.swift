import Foundation

@objcMembers
public class SolarYear: NSObject {
    public static var MONTH_COUNT = 12

    private var _year: Int

    public var year: Int {
        get {
            _year
        }
    }

    public init(year: Int) {
        _year = year
    }

    public init(date: Date) {
        _year = Calendar.current.component(.year, from: date)
    }

    public convenience override init() {
        self.init(date: Date())
    }

    public class func fromYear(year: Int) -> SolarYear {
        SolarYear(year: year)
    }

    public class func fromDate(date: Date) -> SolarYear {
        SolarYear(date: date)
    }

    public var months: [SolarMonth] {
        get {
            var l = [SolarMonth]()
            let m = SolarMonth(year: _year, month: 1)
            l.append(m)
            for i in (1..<SolarYear.MONTH_COUNT) {
                l.append(m.next(months: i))
            }
            return l
        }
    }

    public func next(years: Int) -> SolarYear {
        SolarYear.fromYear(year: _year + years)
    }

    public override var description: String {
        get {
            "\(_year)"
        }
    }

    public var fullString: String {
        get {
            "\(_year)年"
        }
    }

}
