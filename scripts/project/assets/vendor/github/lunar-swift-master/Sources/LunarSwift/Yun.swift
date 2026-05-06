import Foundation

@objcMembers
public class Yun: NSObject {
    private var _gender: Int = 0
    private var _startYear: Int = 0
    private var _startMonth: Int = 0
    private var _startDay: Int = 0
    private var _startHour: Int = 0
    private var _forward: Bool = false
    private var _lunar: Lunar

    public var gender: Int {
        get {
            _gender
        }
    }

    public var startYear: Int {
        get {
            _startYear
        }
    }

    public var startMonth: Int {
        get {
            _startMonth
        }
    }

    public var startDay: Int {
        get {
            _startDay
        }
    }

    public var startHour: Int {
        get {
            _startHour
        }
    }

    public var forward: Bool {
        get {
            _forward
        }
    }

    public var lunar: Lunar {
        get {
            _lunar
        }
    }

    public init(eightChar: EightChar, gender: Int, sect: Int = 1) {
        _lunar = eightChar.lunar
        _gender = gender
        // 阳
        let yang = 0 == _lunar.yearGanIndexExact % 2
        // 男
        let man = 1 == gender
        _forward = (yang && man) || (!yang && !man)

        // 上节
        let prev = _lunar.prevJie
        // 下节
        let next = _lunar.nextJie
        // 出生日期
        let current = _lunar.solar
        // 阳男阴女顺推，阴男阳女逆推
        let start = _forward ? current : prev.solar
        let end = _forward ? next.solar : current

        var year: Int
        var month: Int
        var day: Int
        var hour = 0

        if 2 == sect {
            var minutes = end.subtractMinute(solar: start)
            year = Int(minutes / 4320)
            minutes -= year * 4320
            month = Int(minutes / 360)
            minutes -= month * 360
            day = Int(minutes / 12)
            minutes -= day * 12
            hour = minutes * 2
        } else {
            let endTimeZhiIndex = (end.hour == 23)
                    ? 11
                    : LunarUtil.getTimeZhiIndex(hm: String(format: "%02d:%02d", end.hour, end.minute))
            let startTimeZhiIndex = (start.hour == 23)
                    ? 11
                    : LunarUtil.getTimeZhiIndex(hm: String(format: "%02d:%02d", start.hour, start.minute))
            // 时辰差
            var hourDiff = endTimeZhiIndex - startTimeZhiIndex
            // 天数差
            var dayDiff = end.subtract(solar: start)
            if hourDiff < 0 {
                hourDiff += 12
                dayDiff -= 1
            }
            let monthDiff = Int(hourDiff * 10 / 30)
            month = dayDiff * 4 + monthDiff
            day = hourDiff * 10 - monthDiff * 30
            year = month / 12
            month = month - year * 12
        }
        _startYear = year
        _startMonth = month
        _startDay = day
        _startHour = hour
    }

    public var startSolar: Solar {
        get {
            var solar = _lunar.solar
            solar = solar.nextYear(years: _startYear)
            solar = solar.nextMonth(months: _startMonth)
            solar = solar.next(days: _startDay)
            return solar.nextHour(hours: _startHour)
        }
    }

    public func getDaYun(n: Int = 10) -> [DaYun] {
        var l = [DaYun]()
        for i in (0..<n) {
            l.append(DaYun(yun: self, index: i))
        }
        return l
    }

}
