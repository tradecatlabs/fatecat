import Foundation

@objcMembers
public class SolarMonth: NSObject {
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

    public class func fromYm(year: Int, month: Int) -> SolarMonth {
        SolarMonth(year: year, month: month)
    }

    public class func fromDate(date: Date) -> SolarMonth {
        SolarMonth(date: date)
    }

    public var days: [Solar] {
        var l = [Solar]()
        let d = Solar(year: _year, month: _month, day: 1)
        l.append(d)
        let days = SolarUtil.getDaysOfMonth(year: _year, month: _month)
        for i in (1..<days) {
            l.append(d.next(days: i))
        }
        return l
    }

    public func getWeeks(start: Int) -> [SolarWeek] {
        var l = [SolarWeek]()
        var week = SolarWeek.fromYmd(year: _year, month: _month, day: 1, start: start)
        while true {
            l.append(week)
            week = week.next(weeks: 1, separateMonth: false)
            let firstDay = week.firstDay
            if firstDay.year > _year || firstDay.month > _month {
                break
            }
        }
        return l
    }

    public func next(months: Int) -> SolarMonth {
        var n = 1
        var m = months
        if months < 0 {
            n = -1
            m = -months
        }
        var y = _year + m / 12 * n
        m = _month + m % 12 * n
        if m > 12 {
            m -= 12
            y += 1
        } else if m < 1 {
            m += 12
            y -= 1
        }
        return SolarMonth.fromYm(year: y, month: m)
    }

    public override var description: String {
        "\(_year)-\(_month)"
    }

    public var fullString: String {
        get {
            "\(_year)年\(_month)月"
        }
    }

}
