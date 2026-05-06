import Foundation

@objcMembers
public class SolarWeek: NSObject {
    private var _year: Int
    private var _month: Int
    private var _day: Int
    private var _start: Int

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

    public var day: Int {
        get {
            _day
        }
    }

    public var start: Int {
        get {
            _start
        }
    }

    public init(year: Int, month: Int, day: Int, start: Int) {
        _year = year
        _month = month
        _day = day
        _start = start
    }

    public init(date: Date, start: Int) {
        let calendar = Calendar.current
        _year = calendar.component(.year, from: date)
        _month = calendar.component(.month, from: date)
        _day = calendar.component(.day, from: date)
        _start = start
    }

    public convenience init(start: Int) {
        self.init(date: Date(), start: start)
    }

    public class func fromYmd(year: Int, month: Int, day: Int, start: Int) -> SolarWeek {
        SolarWeek(year: year, month: month, day: day, start: start)
    }

    public class func fromDate(date: Date, start: Int) -> SolarWeek {
        SolarWeek(date: date, start: start)
    }

    public var index: Int {
        get {
            var offset = Solar.fromYmdHms(year: _year, month: _month, day: 1).week - _start
            if offset < 0
            {
                offset += 7
            }
            return Int(ceil(Double(_day + offset) / Double(7)))
        }
    }

    public var indexInYear: Int {
        get {
            var offset = Solar.fromYmdHms(year: _year, month: 1, day: 1).week - _start
            if offset < 0
            {
                offset += 7
            }
            return Int(ceil(Double(SolarUtil.getDaysInYear(year: _year, month: _month, day: _day) + offset) / Double(7)))
        }
    }

    public var firstDay: Solar {
        get {
            let c = Solar.fromYmdHms(year: _year, month: _month, day: _day)
            var prev = c.week - _start
            if prev < 0
            {
                prev += 7
            }
            return c.next(days: -prev)
        }
    }

    public var firstDayInMonth: Solar? {
        get {
            for d in days {
                if d.month == _month {
                    return d
                }
            }
            return nil
        }
    }

    public var days: [Solar] {
        get {
            var l = [Solar]()
            let d = firstDay
            l.append(d)
            for i in (1..<7) {
                l.append(d.next(days: i))
            }
            return l
        }
    }

    public var daysInMonth: [Solar] {
        get {
            var l = [Solar]()
            for d in days {
                if d.month == _month {
                    l.append(d)
                }
            }
            return l
        }
    }

    public func next(weeks: Int, separateMonth: Bool) -> SolarWeek {
        if 0 == weeks {
            return SolarWeek(year: _year, month: _month, day: _day, start: _start)
        }
        var c = Solar.fromYmdHms(year: _year, month: _month, day: _day)
        if separateMonth {
            var n = weeks
            var week = SolarWeek(year: c.year, month: c.month, day: c.day, start: _start)
            var month = week.month
            let plus = n > 0
            while 0 != n
            {
                c = c.next(days: plus ? 7 : -7)
                week = SolarWeek(year: c.year, month: c.month, day: c.day, start: _start)
                var weekMonth = week.month
                if month != weekMonth
                {
                    let index = week.index
                    if plus
                    {
                        if 1 == index
                        {
                            let firstDay = week.firstDay
                            week = SolarWeek(year: firstDay.year, month: firstDay.month, day: firstDay.day, start: _start)
                            weekMonth = week.month
                        }
                        else
                        {
                            c = Solar(year: week.year, month: week.month, day: 1)
                            week = SolarWeek(year: c.year, month: c.month, day: c.day, start: _start)
                        }
                    }
                    else
                    {
                        if SolarUtil.getWeeksOfMonth(year: week.year, month: week.month, start: _start) == index
                        {
                            let lastDay = week.firstDay.next(days: 6)
                            week = SolarWeek(year: lastDay.year, month: lastDay.month, day: lastDay.day, start: _start)
                            weekMonth = week.month
                        }
                        else
                        {
                            c = Solar(year: week.year, month: week.month, day: SolarUtil.getDaysOfMonth(year: week.year, month: week.month))
                            week = SolarWeek(year: c.year, month: c.month, day: c.day, start: _start)
                        }
                    }
                    month = weekMonth
                }
                n -= plus ? 1 : -1
            }
            return week
        } else {
            c = c.next(days: weeks * 7)
            return SolarWeek(year: c.year, month: c.month, day: c.day, start: _start)
        }
    }

    public override var description: String {
        get {
            "\(_year).\(_month).\(index)"
        }
    }

    public var fullString: String {
        get {
            "\(_year)年\(_month)月第\(index)周"
        }
    }

}
