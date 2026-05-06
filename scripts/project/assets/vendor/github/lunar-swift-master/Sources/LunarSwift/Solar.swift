import Foundation

@objcMembers
public class Solar: NSObject {
    public static var J2000: Double = 2451545

    private var _year: Int
    private var _month: Int
    private var _day: Int
    private var _hour: Int
    private var _minute: Int
    private var _second: Int

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

    public var hour: Int {
        get {
            _hour
        }
    }

    public var minute: Int {
        get {
            _minute
        }
    }

    public var second: Int {
        get {
            _second
        }
    }

    public init(year: Int, month: Int, day: Int, hour: Int = 0, minute: Int = 0, second: Int = 0) {
        if 1582 == year && 10 == month {
            if day > 4 && day < 15 {
                fatalError("wrong solar year \(year) month \(month) day \(day)")
            }
        }
        if month < 1 || month > 12 {
            fatalError("wrong month \(month)")
        }
        if day < 1 || day > 31 {
            fatalError("wrong day \(day)")
        }
        if hour < 0 || hour > 23 {
            fatalError("wrong hour \(hour)")
        }
        if minute < 0 || minute > 59 {
            fatalError("wrong minute \(minute)")
        }
        if second < 0 || second > 59 {
            fatalError("wrong second \(second)")
        }
        _year = year
        _month = month
        _day = day
        _hour = hour
        _minute = minute
        _second = second
    }

    public convenience init(date: Date) {
        let calendar = Calendar.current
        self.init(year: calendar.component(.year, from: date), month: calendar.component(.month, from: date), day: calendar.component(.day, from: date), hour: calendar.component(.hour, from: date), minute: calendar.component(.minute, from: date), second: calendar.component(.second, from: date))
    }

    public convenience override init() {
        self.init(date: Date())
    }

    public class func fromYmdHms(year: Int, month: Int, day: Int, hour: Int = 0, minute: Int = 0, second: Int = 0) -> Solar {
        Solar(year: year, month: month, day: day, hour: hour, minute: minute, second: second)
    }

    public class func fromDate(date: Date) -> Solar {
        Solar(date: date)
    }

    public class func fromJulianDay(julianDay: Double) -> Solar {
        var d = Int(julianDay + 0.5)
        var f = julianDay + 0.5 - Double(d)

        if d >= 2299161
        {
            let c = Int((Double(d) - 1867216.25) / 36524.25)
            d += 1 + c - Int(Double(c) / 4)
        }
        d += 1524
        var year = Int((Double(d) - 122.1) / 365.25)
        d -= Int(365.25 * Double(year))
        var month = Int(Double(d) / 30.601)
        d -= Int(30.601 * Double(month))
        var day = d
        if month > 13
        {
            month -= 13
            year -= 4715
        }
        else
        {
            month -= 1
            year -= 4716
        }
        f *= 24
        var hour = Int(f)

        f -= Double(hour)
        f *= 60
        var minute = Int(f)

        f -= Double(minute)
        f *= 60
        var second = Int(round(f))

        if second > 59
        {
            second -= 60
            minute += 1
        }
        if minute > 59
        {
            minute -= 60
            hour += 1
        }
        if hour > 23 {
            hour -= 24
            day += 1
        }
        return Solar(year: year, month: month, day: day, hour: hour, minute: minute, second: second)
    }

    public class func fromBaZi(yearGanZhi: String, monthGanZhi: String, dayGanZhi: String, timeGanZhi: String, sect: Int = 2, baseYear: Int = 1900) -> [Solar] {
        let sec = (1 == sect) ? 1 : 2
        var l = [Solar]()
        // 月地支距寅月的偏移值
        var m = LunarUtil.find(name: String(monthGanZhi.suffix(1)), names: LunarUtil.ZHI, offset: -1) - 2
        if m < 0 {
            m += 12
        }
        // 月天干要一致
        if (((LunarUtil.find(name: String(yearGanZhi.prefix(1)), names: LunarUtil.GAN, offset: -1) + 1) * 2 + m) % 10 != LunarUtil.find(name: String(monthGanZhi.prefix(1)), names: LunarUtil.GAN, offset: -1)) {
            return l
        }
        // 1年的立春是辛酉，序号57
        var y = LunarUtil.getJiaZiIndex(ganZhi: yearGanZhi) - 57
        if y < 0 {
            y += 60
        }
        y += 1
        // 节令偏移值
        m *= 2
        // 时辰地支转时刻，子时按零点算
        let h = LunarUtil.find(name: String(timeGanZhi.suffix(1)), names: LunarUtil.ZHI, offset: -1) * 2
        var hours = [Int]()
        hours.append(h)
        if 0 == h && 2 == sec {
            hours.append(23)
        }
        let startYear = baseYear - 1
        
        // 结束年
        let endYear = Calendar.current.component(.year, from: Date())
        
        while y <= endYear {
            if y >= startYear {
                // 立春为寅月的开始
                let jieQiTable = Lunar.fromYmdHms(lunarYear: y, lunarMonth: 1, lunarDay: 1).jieQiTable
                // 节令推移，年干支和月干支就都匹配上了
                var solarTime = jieQiTable[Lunar.JIE_QI_IN_USE[4 + m]]!
                if solarTime.year >= baseYear {
                    // 日干支和节令干支的偏移值
                    var d = LunarUtil.getJiaZiIndex(ganZhi: dayGanZhi) - LunarUtil.getJiaZiIndex(ganZhi: solarTime.lunar.dayInGanZhiExact2)
                    if d < 0 {
                        d += 60
                    }
                    if d > 0 {
                        // 从节令推移天数
                        solarTime = solarTime.next(days: d)
                    }
                    for hour in hours {
                        var mi = 0
                        var s = 0
                        if d == 0 && hour == solarTime.hour {
                            // 如果正好是节令当天，且小时和节令的小时数相等的极端情况，把分钟和秒钟带上
                            mi = solarTime.minute
                            s = solarTime.second
                        }
                        // 验证一下
                        var solar = Solar.fromYmdHms(year: solarTime.year, month: solarTime.month, day: solarTime.day, hour: hour, minute: mi, second: s)
                        if d == 30 {
                            solar = solar.nextHour(hours: -1)
                        }
                        let lunar = solar.lunar
                        let dgz = (2 == sect) ? lunar.dayInGanZhiExact2 : lunar.dayInGanZhiExact
                        if lunar.yearInGanZhiExact == yearGanZhi && lunar.monthInGanZhiExact == monthGanZhi && dgz == dayGanZhi && lunar.timeInGanZhi == timeGanZhi
                        {
                            l.append(solar)
                        }
                    }
                }
            }
            y += 60
        }
        return l
    }

    public var leapYear: Bool {
        get {
            SolarUtil.isLeapYear(year: _year)
        }
    }

    public var week: Int {
        get {
            (Int(julianDay + 0.5) + 7000001) % 7
        }
    }

    public var weekInChinese: String {
        get {
            SolarUtil.WEEK[week]
        }
    }

    public var xingZuo: String {
        get {
            var index = 11
            let y = _month * 100 + _day
            if y >= 321 && y <= 419 {
                index = 0
            } else if y >= 420 && y <= 520 {
                index = 1
            } else if y >= 521 && y <= 621 {
                index = 2
            } else if y >= 622 && y <= 722 {
                index = 3
            } else if y >= 723 && y <= 822 {
                index = 4
            } else if y >= 823 && y <= 922 {
                index = 5
            } else if y >= 923 && y <= 1023 {
                index = 6
            } else if y >= 1024 && y <= 1122 {
                index = 7
            } else if y >= 1123 && y <= 1221 {
                index = 8
            } else if y >= 1222 || y <= 119 {
                index = 9
            } else if y <= 218 {
                index = 10
            }
            return SolarUtil.XING_ZUO[index]
        }
    }

    public var festivals: [String] {
        get {
            var l = [String]()
            //获取几月几日对应的节日
            var f = SolarUtil.FESTIVAL["\(_month)-\(_day)"]
            if nil != f {
                l.append(f!)
            }
            //计算几月第几个星期几对应的节日
            let weeks = Int(ceil(Double(_day) / 7))
            let key = "\(_month)-\(weeks)-\(week)"
            //星期几，0代表星期天
            f = SolarUtil.WEEK_FESTIVAL[key]
            if nil != f {
                l.append(f!)
            }
            if _day + 7 > SolarUtil.getDaysOfMonth(year: _year, month: _month) {
                f = SolarUtil.WEEK_FESTIVAL["\(_month)-0-\(week)"]
                if nil != f {
                    l.append(f!)
                }
            }
            return l
        }
    }

    public var otherFestivals: [String] {
        get {
            var l = [String]()
            //获取几月几日对应的节日
            let fs = SolarUtil.OTHER_FESTIVAL["\(_month)-\(_day)"]
            if nil != fs {
                for f in fs! {
                    l.append(f)
                }
            }
            return l
        }
    }

    public var lunar: Lunar {
        get {
            Lunar.fromSolar(solar: self)
        }
    }

    public var julianDay: Double {
        get {
            var y: Int = _year
            var m: Int = _month
            let d: Double = Double(_day) + ((Double(_second) / Double(60) + Double(_minute)) / Double(60) + Double(_hour)) / Double(24)
            var n: Int = 0
            let g: Bool = y * 372 + m * 31 + Int(d) >= 588829
            if m <= 2 {
                m += 12
                y -= 1
            }
            if g {
                n = Int(Double(y) / Double(100))
                n = 2 - n + Int(Double(n) / Double(4))
            }
            return Double(Int(Double(365.25) * Double(y + 4716))) + Double(Int(Double(30.6001) * Double(m + 1))) + d + Double(n) - Double(1524.5)
        }
    }

    public func isBefore(solar: Solar) -> Bool {
        SolarUtil.isBefore(ay: _year, am: _month, ad: _day, ah: _hour, ai: _minute, ac: _second, by: solar.year, bm: solar.month, bd: solar.day, bh: solar.hour, bi: solar.minute, bc: solar.second)
    }

    public func isAfter(solar: Solar) -> Bool {
        SolarUtil.isAfter(ay: _year, am: _month, ad: _day, ah: _hour, ai: _minute, ac: _second, by: solar.year, bm: solar.month, bd: solar.day, bh: solar.hour, bi: solar.minute, bc: solar.second)
    }

    public func subtract(solar: Solar) -> Int {
        SolarUtil.getDaysBetween(ay: solar.year, am: solar.month, ad: solar.day, by: _year, bm: _month, bd: _day)
    }

    public func subtractMinute(solar: Solar) -> Int {
        var days = subtract(solar: solar)
        let cm = _hour * 60 + _minute
        let sm = solar.hour * 60 + solar.minute
        var m = cm - sm
        if m < 0 {
            m += 1440
            days -= 1
        }
        m += days * 1440
        return m
    }

    public func nextYear(years: Int) -> Solar {
        let y = _year + years
        var d = _day
        if 1582 == y && 10 == _month {
            if d > 4 && d < 15 {
                d += 10
            }
        } else if 2 == _month {
            if d > 28 {
                if !SolarUtil.isLeapYear(year: y) {
                    d = 28
                }
            }
        }
        return Solar.fromYmdHms(year: y, month: _month, day: d, hour: _hour, minute: _minute, second: _second)
    }

    public func nextMonth(months: Int) -> Solar {
        let month = SolarMonth.fromYm(year: _year, month: _month).next(months: months)
        let y = month.year
        let m = month.month
        var d = _day
        if 1582 == y && 10 == m {
            if d > 4 && d < 15 {
                d += 10
            }
        } else {
            let maxDay = SolarUtil.getDaysOfMonth(year: y, month: m)
            if d > maxDay {
                d = maxDay
            }
        }
        return Solar.fromYmdHms(year: y, month: m, day: d, hour: _hour, minute: _minute, second: _second)
    }

    public func nextDay(days: Int) -> Solar {
        var y = _year
        var m = _month
        var d = _day
        if 1582 == y && 10 == m {
            if d > 4 {
                d -= 10
            }
        }
        if days > 0 {
            d += days
            var daysInMonth = SolarUtil.getDaysOfMonth(year: y, month: m)
            while d > daysInMonth {
                d -= daysInMonth
                m += 1
                if m > 12 {
                    m = 1
                    y += 1
                }
                daysInMonth = SolarUtil.getDaysOfMonth(year: y, month: m)
            }
        } else if days < 0 {
            while d+days <= 0 {
                m -= 1
                if m < 1 {
                    m = 12
                    y -= 1
                }
                d += SolarUtil.getDaysOfMonth(year: y, month: m)
            }
            d += days
        }
        if 1582 == y && 10 == m {
            if d > 4 {
                d += 10
            }
        }
        return Solar.fromYmdHms(year: y, month: m, day: d, hour: _hour, minute: _minute, second: _second)
    }

    public func next(days: Int, onlyWorkday: Bool = false) -> Solar {
        if !onlyWorkday {
            return nextDay(days: days)
        }
        var solar = Solar.fromYmdHms(year: _year, month: _month, day: _day, hour: _hour, minute: _minute, second: _second)
        if days != 0 {
            var rest = days
            var add = 1
            if days < 0 {
                rest = -days
                add = -1
            }
            while rest > 0 {
                solar = solar.nextDay(days: add)
                var work = true
                let holiday = HolidayUtil.getHolidayByYmd(year: solar.year, month: solar.month, day: solar.day)
                if nil == holiday {
                    let week = solar.week
                    if 0 == week || 6 == week {
                        work = false
                    }
                } else {
                    work = holiday!.work
                }
                if work {
                    rest -= 1
                }
            }
        }
        return solar
    }

    public func nextHour(hours: Int) -> Solar {
        let h = _hour + hours
        var n = 1
        var hour = h
        if h < 0 {
            n = -1
            hour = -h
        }
        var days = hour / 24 * n
        hour = (hour % 24) * n
        if hour < 0 {
            hour += 24
            days -= 1
        }
        let o = next(days: days)
        return Solar.fromYmdHms(year: o.year, month: o.month, day: o.day, hour: hour, minute: o.minute, second: o.second)
    }
    
    public func getSalaryRate() -> Int {
        // 元旦节
        if _month == 1 && _day == 1 {
            return 3
        }
        // 劳动节
        if _month == 5 && _day == 1 {
            return 3
        }
        // 国庆
        if _month == 10 && _day >= 1 && _day <= 3 {
            return 3
        }
        // 春节
        if lunar.month == 1 && lunar.day >= 1 && lunar.day <= 3 {
            return 3
        }
        // 端午
        if lunar.month == 5 && lunar.day == 5 {
            return 3
        }
        // 中秋
        if lunar.month == 8 && lunar.day == 15 {
            return 3
        }
        // 清明
        if "清明" == lunar.jieQi {
            return 3
        }
        let holiday = HolidayUtil.getHolidayByYmd(year: _year, month: _month, day: _day)
        if holiday != nil {
            // 法定假日非上班
            if !holiday!.work {
                return 2
            }
        } else {
            // 周末
            if week == 6 || week == 0 {
                return 2
            }
        }
        // 工作日
        return 1
    }

    public var ymd: String {
        get {
            String(format: "%04d-%02d-%02d", _year, _month, _day)
        }
    }

    public var ymdhms: String {
        get {
            String(format: "%04d-%02d-%02d %02d:%02d:%02d", _year, _month, _day, _hour, _minute, _second)
        }
    }

    public override var description: String {
        get {
            "\(ymd)"
        }
    }

    public var fullString: String {
        get {
            var s  = "\(ymdhms)"
            if leapYear {
                s += " 闰年"
            }
            s += " 星期\(weekInChinese)"
            for i in festivals {
                s += " (\(i))"
            }
            for i in otherFestivals {
                s += " (\(i))"
            }
            s += " \(xingZuo)座"
            return s
        }
    }

}
