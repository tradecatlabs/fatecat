//
//  Calendar.swift
//  Chinendar
//
//  Created by Leo Liu on 9/21/21.
//

import Foundation
import CelestialSystem

extension Calendar {
    static let utcCalendar: Self = {
        var cal = Calendar(identifier: .iso8601)
        cal.timeZone = TimeZone(abbreviation: "UTC")!
        return cal
    }()

    func startOfDay(for day: Date, apparent: Bool, location: GeoLocation?) -> Date {
        let startToday = startOfDay(for: day)
        if let location, apparent {
            let apparentStart = dayStart(around: startToday, at: location)
            if apparentStart <= day {
                return apparentStart
            } else {
                return dayStart(around: self.date(byAdding: .day, value: -1, to: startToday)!, at: location)
            }
        } else {
            return startToday
        }
    }

    private func dayStart(around time: Date, at loc: GeoLocation, iteration: Int = 0) -> Date {
        let solarSystem = SolarSystem(time: time, lat: loc.lat, lon: loc.lon, targets: .sun)
        let planet = solarSystem.planets.sun
        let offset = Double.pi
        let timeUntilMidnight = SolarSystem.normalize(radian: planet.loc.ra - solarSystem.localSiderialTime! + offset)

        let dTime = timeUntilMidnight / Double.pi * 43082.04
        if abs(dTime) < 1 {
            return time
        } else {
            return dayStart(around: time + dTime, at: loc, iteration: iteration + 1)
        }
    }
}

// MARK: ChineseCalendar
struct ChineseCalendar: Sendable, Equatable {
    static let updateInterval: CGFloat = 14.4 // Seconds
    static let monthChinese = ["正月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "冬月", "臘月" ]
    static let monthChineseLocalized: [LocalizedStringResource] = ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10", "M11", "M12" ]
    static let monthChineseCompact = ["㋀", "㋁", "㋂", "㋃", "㋄", "㋅", "㋆", "㋇", "㋈", "㋉", "㋊", "㋋"]
    static let dayChinese = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十", "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"]
    static let dayChineseLocalized: [LocalizedStringResource] = ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12", "D13", "D14", "D15", "D16", "D17", "D18", "D19", "D20", "D21", "D22", "D23", "D24", "D25", "D26", "D27", "D28", "D29", "D30"]
    static let dayChineseCompact = ["㏠", "㏡", "㏢", "㏣", "㏤", "㏥", "㏦", "㏧", "㏨", "㏩", "㏪", "㏫", "㏬", "㏭", "㏮", "㏯", "㏰", "㏱", "㏲", "㏳", "㏴", "㏵", "㏶", "㏷", "㏸", "㏹", "㏺", "㏻", "㏼", "㏽"]
    static let terrestrialBranches = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    static let terrestrialBranchesLocalized: [LocalizedStringResource] = ["TB0", "TB1", "TB2", "TB3", "TB4", "TB5", "TB6", "TB7", "TB8", "TB9", "TB10", "TB11"]
    static let subHourName = ["初", "正"]
    static let subHourNameLocalized: [LocalizedStringResource] = ["H_prelude", "H_proper"]
    static let chineseNumbers = ["初", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "十一", "十二", "十三", "十四", "十五", "十六"]
    static let chineseNumbersLocalized: [LocalizedStringResource] = ["N0", "N1", "N2", "N3", "N4", "N5", "N6", "N7", "N8", "N9", "N10", "N11", "N12", "N13", "N14", "N15", "N16"]
    static let evenSolarTermChinese = ["冬　至", "大　寒", "雨　水", "春　分", "穀　雨", "小　滿", "夏　至", "大　暑", "處　暑", "秋　分", "霜　降", "小　雪"]
    static let oddSolarTermChinese = ["小　寒", "立　春", "驚　蟄", "清　明", "立　夏", "芒　種", "小　暑", "立　秋", "白　露", "寒　露", "立　冬", "大　雪"]
    static let leapLabel = "閏"
    static let leapLabelLocalized: LocalizedStringResource = "LEAP"
    static let alternativeMonthName = ["閏正月": "閏一月"]
    static let dayTimeName = (midnight: "夜中", sunrise: "日出", noon: "日中", sunset: "日入")
    static let moonTimeName = (moonrise: "月出", highMoon: "月中", moonset: "月入")
    static let moonPhases = (newmoon: "朔", fullmoon: "望")
    static let planetNames = (mercury: "辰星", venus: "太白", mars: "熒惑", jupiter: "歲星", saturn: "填星", moon: "太陰")
    static let holidays = [ChineseDate(month: 1, day: 1): "元旦", ChineseDate(month: 1, day: 15): "上元", ChineseDate(month: 2, day: 2): "春社",
                           ChineseDate(month: 3, day: 3): "上巳", ChineseDate(month: 5, day: 5): "端午", ChineseDate(month: 7, day: 7): "七夕",
                           ChineseDate(month: 7, day: 15): "中元", ChineseDate(month: 9, day: 9): "重陽", ChineseDate(month: 8, day: 15): "中秋",
                           ChineseDate(month: 10, day: 15): "下元", ChineseDate(month: 12, day: 8): "臘祭", ChineseDate(month: 12, day: 1, reverseCount: true): "除夕"]
    static let start: Date = {
        var components = DateComponents()
        components.year = 1901
        components.month = 12
        components.day = 23
        components.timeZone = TimeZone.gmt
        return Calendar.utcCalendar.date(from: components)!
    }()
    static let end: Date = {
        var components = DateComponents()
        components.year = 2999
        components.month = 12
        components.day = 20
        components.timeZone = TimeZone.gmt
        return Calendar.utcCalendar.date(from: components)!
    }()

    private let _compact: Bool
    private var _globalMonth: Bool = false
    private var _apparentTime: Bool = false
    private var _largeHour: Bool = false
    private var _time: Date = .distantPast
    private var _calendar: Calendar = .utcCalendar
    private var _location: GeoLocation?
    private var _year: Int = 0
    private var _numberOfMonths: Int = 0
    private var _yearLength: Double = 0
    private var _solarTerms: [Date] = []
    private var _evenSolarTerms: [Date] = []
    private var _oddSolarTerms: [Date] = []
    private var _moonEclipses: [Date] = []
    private var _fullMoons: [Date] = []
    private var _month: Int = -1
    private var _preciseMonth: Int = -1
    private var _leapMonth: Int = -1
    private var _day: Int = -1
    private var _planets: Planets<NamedPosition>!
    private var _sunTimes: [DateType: Solar<NamedDate?>] = [:]
    private var _moonTimes: [DateType: Lunar<NamedDate?>] = [:]
    private var _startHour: Date = .distantPast
    private var _endHour: Date = .distantFuture
    private var _hourNames: [NamedHour] = []
    private var _hourNamesInCurrentHour: [NamedHour] = []
    private var _subhours: [Date] = []
    private var _subhourMinors: [Date] = []
    private var _hour: Hour = Hour(hour: -1, format: .full)
    private var _quarter: SubHour = SubHour(majorTick: -1, minorTick: -1)

    init(time: Date = .now, timezone: TimeZone? = nil, location: GeoLocation? = nil, compact: Bool = false, globalMonth: Bool = false, apparentTime: Bool = false, largeHour: Bool = false) {
        let boundedTime: Date
        if time < ChineseCalendar.start {
            print("Time must be after \(ChineseCalendar.start).")
            boundedTime = ChineseCalendar.start
        } else if time > ChineseCalendar.end {
            print("Time must be before \(ChineseCalendar.end).")
            boundedTime = ChineseCalendar.end
        } else {
            boundedTime = time
        }
        self._compact = compact
        self._time = boundedTime
        var calendar = Calendar.current
        calendar.timeZone = timezone ?? calendar.timeZone
        self._calendar = calendar
        self._location = location
        self._globalMonth = globalMonth
        self._apparentTime = apparentTime
        self._largeHour = largeHour
        updateYear()
        updateDate()
        updateHour()
        updateSubHour()
        updatePlanets()
    }

    mutating func update(time: Date = .now, timezone: TimeZone? = nil, location: GeoLocation?? = Optional(nil), globalMonth: Bool? = nil, apparentTime: Bool? = nil, largeHour: Bool? = nil) {
        guard time >= ChineseCalendar.start && time <= ChineseCalendar.end else { return }
        let oldTimezone = _calendar.timeZone
        let oldLocation = _location
        let oldGlobalMonth = _globalMonth
        let oldApparentTime = _apparentTime
        _time = time
        _calendar.timeZone = timezone ?? _calendar.timeZone
        _location = location ?? _location
        _globalMonth = globalMonth ?? _globalMonth
        _apparentTime = apparentTime ?? _apparentTime
        _largeHour = largeHour ?? _largeHour

        if (_location == nil && oldLocation != nil) || (_location != nil && oldLocation == nil) {
            updateYear()
        } else if let newLocation = _location, let oldLocation = oldLocation,
                  sqrt(pow(newLocation.lat - oldLocation.lat, 2) + pow(newLocation.lon - oldLocation.lon, 2)) > 1 {
            updateYear()
        } else if timezone != oldTimezone || oldGlobalMonth != _globalMonth || oldApparentTime != _apparentTime {
            updateYear()
        } else {
            let year = _calendar.component(.year, from: time)
            if !(((year == _year) && (_solarTerms[24] > time)) || ((year == _year - 1) && (_solarTerms[0] <= time))) {
                updateYear()
            }
        }
        updateDate()
        updateHour()
        updateSubHour()
        updatePlanets()
    }
}

// MARK: Basic Properties
extension ChineseCalendar {
    var currentDayInYear: Double {
        _solarTerms[0].distance(to: _time) / _yearLength
    }

    var currentDayInMonth: Double {
        if _globalMonth {
            let monthLength = _moonEclipses[_preciseMonth].distance(to: _moonEclipses[_preciseMonth + 1])
            return _moonEclipses[_preciseMonth].distance(to: _time) / monthLength
        } else {
            let monthStart = calendar.startOfDay(for: _moonEclipses[_month], apparent: apparentTime, location: location)
            let monthEnd = calendar.startOfDay(for: _moonEclipses[_month + 1], apparent: apparentTime, location: location)
            return monthStart.distance(to: _time) / monthStart.distance(to: monthEnd)
        }
    }

    var currentHourInDay: Double {
        startOfDay.distance(to: _time) / startOfDay.distance(to: startOfNextDay)
    }

    var subhourInHour: Double {
        startOfLargeHour.distance(to: _time) / startOfLargeHour.distance(to: endOfLargeHour)
    }

    var apparentTime: Bool {
        _apparentTime && _location != nil
    }
    var globalMonth: Bool {
        _globalMonth
    }
    var largeHour: Bool {
        _largeHour
    }

    var monthString: String {
        let month = (isLeapMonth ? Self.leapLabel : "") + Self.monthChinese[nominalMonth-1]
        return Self.alternativeMonthName[month] ?? month
    }
    var monthStringLocalized: LocalizedStringResource {
        if isLeapMonth {
            let month: LocalizedStringResource = "LEAP\(Self.leapLabelLocalized)MONTH\(Self.monthChineseLocalized[nominalMonth-1])"
            return month
        } else {
            return Self.monthChineseLocalized[nominalMonth-1]
        }
    }

    var dayString: String {
        let chinese_day = Self.dayChinese[_day]
        if chinese_day.count > 1 {
            return chinese_day
        } else {
            return "\(chinese_day)日"
        }
    }
    var dayStringLocalized: LocalizedStringResource {
        "\(Self.dayChineseLocalized[_day])DAY"
    }

    var dateString: String {
        "\(monthString)\(dayString)"
    }
    var dateStringLocalized: LocalizedStringResource {
        "MONTH\(monthStringLocalized)DAY\(dayStringLocalized)"
    }

    var timeString: String {
        let _hour_string = _hour.string
        let _quarter_string = _quarter.string
        if _hour_string.count < 2 && _hour_string.count + _quarter_string.count < 5 {
            return "\(_hour_string)時\(_quarter_string)"
        } else {
            return "\(_hour_string)\(_quarter_string)"
        }
    }
    var timeStringLocalized: LocalizedStringResource {
        "HOUR\(_hour.stringLocalized)QUARTER\(_quarter.stringLocalized)"
    }

    var hourString: String {
        let _hour_string = _hour.string
        if _hour_string.count < 2 {
            return "\(_hour_string)時"
        } else {
            return _hour_string
        }
    }
    var hourStringLocalized: LocalizedStringResource {
        _hour.stringLocalized
    }

    var quarterString: String {
        _quarter.string
    }
    var quarterStringLocalized: LocalizedStringResource {
        _quarter.stringLocalized
    }

    var shortQuarterString: String {
        _quarter.shortString
    }
    var shortQuarterStringLocalized: LocalizedStringResource {
        _quarter.shortStringLocalized
    }

    var calendar: Calendar {
        return _calendar
    }

    var evenSolarTerms: [Double] {
        var evenSolarTermsPositions = _evenSolarTerms.map { _solarTerms[0].distance(to: $0) / _yearLength as Double }
        evenSolarTermsPositions = evenSolarTermsPositions.filter { ($0 < 1) && ($0 > 0) }
        return [0] + evenSolarTermsPositions
    }

    var oddSolarTerms: [Double] {
        var oddSolarTermsPositions = _oddSolarTerms.map { _solarTerms[0].distance(to: $0) / _yearLength as Double }
        oddSolarTermsPositions = oddSolarTermsPositions.filter { ($0 < 1) && ($0 > 0) }
        return oddSolarTermsPositions
    }

    var solarTerms: [NamedDate] {
        var terms = [NamedDate]()
        for i in 0..<_solarTerms.count {
            let name: String
            if (i %% 2) == 0 {
                name = Self.evenSolarTermChinese[(i / 2) %% Self.evenSolarTermChinese.count]
            } else {
                name = Self.oddSolarTermChinese[(i / 2) %% Self.oddSolarTermChinese.count]
            }
            terms.append(NamedDate(name: name, date: _solarTerms[i]))
        }
        return terms
    }

    var moonPhases: [NamedDate] {
        var phases = [NamedDate]()
        for i in 0..<max(_moonEclipses.count, _fullMoons.count) {
            if i < _moonEclipses.count {
                phases.append(NamedDate(name: Self.moonPhases.newmoon, date: _moonEclipses[i]))
            }
            if i < _fullMoons.count {
                phases.append(NamedDate(name: Self.moonPhases.fullmoon, date: _fullMoons[i]))
            }
        }
        return phases
    }

    var monthNames: [String] {
        var names = [String]()
        let all_names = _compact ? Self.monthChineseCompact : Self.monthChinese
        for i in 0..<_numberOfMonths {
            let name = if _leapMonth >= 0 && i > _leapMonth {
                all_names[(i - 3) %% 12]
            } else if _leapMonth >= 0 && i == _leapMonth {
                Self.leapLabel + all_names[(i - 3) %% 12]
            } else {
                all_names[(i - 2) %% 12]
            }
            names.append(Self.alternativeMonthName[name] ?? name)
        }
        return names
    }

    var location: GeoLocation? {
        _location
    }

    var timezone: Int {
        _calendar.timeZone.secondsFromGMT(for: _time)
    }

    var year: Int {
        _year
    }

    var month: Int {
        _month
    }

    var preciseMonth: Int {
        _globalMonth ? _preciseMonth : _month
    }

    var nominalMonth: Int {
        let inLeapMonth = _leapMonth >= 0 && _month >= _leapMonth
        return ((_month + (inLeapMonth ? 0 : 1) - 3) %% 12) + 1
    }
    var leapMonth: Int? {
        if _leapMonth >= 0 {
            _leapMonth
        } else {
            nil
        }
    }

    var isLeapMonth: Bool {
        _leapMonth >= 0 && _month == _leapMonth
    }

    var day: Int {
        _day + 1
    }

    var hour: Int {
        switch _hour.format {
        case .full:
            _hour.hour * 2
        case .partial(index: let index):
            (_hour.hour * 2 + index - 1) %% 24
        }
    }

    var quarterMajor: Int {
        _quarter.majorTick
    }

    var quarterMinor: Int {
        _quarter.minorTick
    }

    var time: Date {
        _time
    }

    var subquarter: Double {
        startOfDay.distance(to: time) / 144
    }

    var numberOfMonths: Int {
        _numberOfMonths
    }

    var numberOfDaysInMonth: Int {
        let month = _globalMonth ? _preciseMonth : _month
        let monthStartDate = _calendar.startOfDay(for: _moonEclipses[month], apparent: apparentTime, location: location)
        let monthEndDate = _calendar.startOfDay(for: _moonEclipses[month + 1], apparent: apparentTime, location: location)
        return Int(round(monthStartDate.distance(to: monthEndDate) / 86400))
    }

    var maxQuarterMajor: Int {
        let startOfDay = startOfDay
        let hourStart = startOfDay.distance(to: startOfHour)
        let hourEnd = startOfDay.distance(to: startOfNextHour) - 1
        return Int(hourEnd /% 864) - Int(hourStart /% 864) + 1
    }

    var maxQuarterMinor: Int {
        let startOfDay = startOfDay
        let hourStart = startOfDay.distance(to: startOfHour)
        let hourEnd = startOfDay.distance(to: startOfNextHour) - 1
        let current = startOfDay.distance(to: _time)
        if Int(current /% 864) <= Int(hourStart /% 864) {
            let startRemainder = (hourStart /% 864 + 1.0) * 864.0 - hourStart - 1
            return Int(startRemainder /% 144) + 1
        } else if Int(current /% 864) >= Int(hourEnd /% 864) {
            return Int((hourEnd %% 864.0) /% 144) + 1
        } else {
            return 6
        }
    }

    var lunarHoliday: String? {
        for holiday in Self.holidays.keys where self.equals(date: holiday) {
            return Self.holidays[holiday]
        }
        return nil
    }

    var lunarHolidays: [NamedDate] {
        Self.holidays.compactMap { chineseDate, name in
            if let date = self.find(chineseDate: chineseDate) {
                NamedDate(name: name, date: date.time)
            } else {
                nil
            }
        }.sorted {
            $0.date < $1.date
        }
    }

    var holidays: [String] {
        var holidays: [String] = []
        if let holiday = self.lunarHoliday {
            holidays.append(holiday)
        }
        for solarTerm in self.eventInDay.oddSolarTerm {
            holidays.append(solarTerm.name)
        }
        for solarTerm in self.eventInDay.evenSolarTerm {
            holidays.append(solarTerm.name)
        }
        for moon in self.eventInDay.eclipse {
            holidays.append(moon.name)
        }
        for moon in self.eventInDay.fullMoon {
            holidays.append(moon.name)
        }
        return holidays
    }
}

// MARK: Celestial Events
extension ChineseCalendar {
    func nextHours(count: Int) -> [Date] {
        let startOfDay = startOfDay
        let aHourSec = startOfDay.distance(to: startOfNextDay) / (_largeHour ? 12 : 24)
        let aHoutInt = _largeHour ? 2 : 1
        var tickTime = time
        var i = 0
        var hours = [Date]()
        while i < count {
            if tickTime > time {
                hours.append(tickTime)
                i += 1
            }
            if apparentTime {
                let hoursPast = floor(startOfDay.distance(to: tickTime) / aHourSec)
                tickTime = startOfDay + (hoursPast + 1) * aHourSec + 1
            } else {
                var components = _calendar.dateComponents([.timeZone, .year, .month, .day, .hour], from: tickTime)
                components.hour = components.hour.map { hour in
                    (hour / aHoutInt + 1) * aHoutInt
                }
                if let newTime = _calendar.date(from: components) {
                    tickTime = newTime
                }
            }
        }
        return hours
    }

    func nextQuarters(count: Int) -> [Date] {
        var tickTime = startOfDay - 864 * 6
        var i = 0
        var quarters = [Date]()
        let quartersInHour = _largeHour ? 8 : 4
        let hours = nextHours(count: count / quartersInHour + 1)
        var j = 0
        while i < count && j < hours.count {
            if tickTime > time {
                if tickTime > hours[j] {
                    if tickTime > hours[j] + 16 {
                        quarters.append(hours[j])
                    }
                    j += 1
                }
                if j >= hours.count || tickTime < hours[j] - 16 {
                    quarters.append(tickTime)
                    i += 1
                }
            }
            tickTime += 864
        }
        return quarters
    }

    var planetPosition: Planets<NamedPosition> {
        _planets
    }

    var eventInMonth: CelestialEvent {
        let monthStart: Date
        let monthLength: Double
        if _globalMonth {
            monthStart = _moonEclipses[_preciseMonth]
            monthLength = _moonEclipses[_preciseMonth].distance(to: _moonEclipses[_preciseMonth + 1])
        } else {
            monthStart = _calendar.startOfDay(for: _moonEclipses[_month], apparent: apparentTime, location: location)
            let monthEnd = _calendar.startOfDay(for: _moonEclipses[_month + 1], apparent: apparentTime, location: location)
            monthLength = monthStart.distance(to: monthEnd)
        }
        var event = CelestialEvent()
        if !_globalMonth {
            event.eclipse = _moonEclipses.map { date in
                NamedPosition(name: Self.moonPhases.newmoon, pos: monthStart.distance(to: date) / monthLength)
            }.filter { $0.pos >= 0 && $0.pos < 1 }
        }
        event.fullMoon = _fullMoons.map { date in
            NamedPosition(name: Self.moonPhases.fullmoon, pos: monthStart.distance(to: date) / monthLength)
        }.filter { $0.pos >= 0 && $0.pos < 1 }
        event.evenSolarTerm = _evenSolarTerms.enumerated().map { offset, date in
            let name = String(Self.evenSolarTermChinese[(offset - 1) %% Self.evenSolarTermChinese.count].replacingOccurrences(of: "　", with: ""))
            return NamedPosition(name: name, pos: monthStart.distance(to: date) / monthLength)
        }.filter { $0.pos >= 0 && $0.pos < 1 }
        event.oddSolarTerm = _oddSolarTerms.enumerated().map { offset, date in
            let name = String(Self.oddSolarTermChinese[(offset - 1) %% Self.oddSolarTermChinese.count].replacingOccurrences(of: "　", with: ""))
            return NamedPosition(name: name, pos: monthStart.distance(to: date) / monthLength)
        }.filter { $0.pos >= 0 && $0.pos < 1 }
        return event
    }

    var eventInDay: CelestialEvent {
        let startOfDay = startOfDay
        let lengthOfDay = startOfDay.distance(to: startOfNextDay)
        var event = CelestialEvent()
        event.eclipse = _moonEclipses.map { date in
            NamedPosition(name: Self.moonPhases.newmoon, pos: startOfDay.distance(to: date) / lengthOfDay)
        }.filter { $0.pos >= 0 && $0.pos < 1 }
        event.fullMoon = _fullMoons.map { date in
            NamedPosition(name: Self.moonPhases.fullmoon, pos: startOfDay.distance(to: date) / lengthOfDay)
        }.filter { $0.pos >= 0 && $0.pos < 1 }
        event.evenSolarTerm = _evenSolarTerms.enumerated().map { offset, date in
            let name = String(Self.evenSolarTermChinese[(offset - 1) %% Self.evenSolarTermChinese.count].replacingOccurrences(of: "　", with: ""))
            return NamedPosition(name: name, pos: startOfDay.distance(to: date) / lengthOfDay)
        }.filter { $0.pos >= 0 && $0.pos < 1 }
        event.oddSolarTerm = _oddSolarTerms.enumerated().map { offset, date in
            let name = String(Self.oddSolarTermChinese[(offset - 1) %% Self.oddSolarTermChinese.count].replacingOccurrences(of: "　", with: ""))
            return NamedPosition(name: name, pos: startOfDay.distance(to: date) / lengthOfDay)
        }.filter { $0.pos >= 0 && $0.pos < 1 }
        return event
    }

    var eventInHour: CelestialEvent {
        var event = CelestialEvent()
        let hourLength = startOfLargeHour.distance(to: endOfLargeHour)
        event.eclipse = _moonEclipses.map { date in
            NamedPosition(name: Self.moonPhases.newmoon, pos: startOfLargeHour.distance(to: date) / hourLength)
        }.filter { $0.pos >= 0 && $0.pos < 1 }
        event.fullMoon = _fullMoons.map { date in
            NamedPosition(name: Self.moonPhases.fullmoon, pos: startOfLargeHour.distance(to: date) / hourLength)
        }.filter { $0.pos >= 0 && $0.pos < 1 }
        event.evenSolarTerm = _evenSolarTerms.enumerated().map { offset, date in
            let name = String(Self.evenSolarTermChinese[(offset - 1) %% Self.evenSolarTermChinese.count].replacingOccurrences(of: "　", with: ""))
            return NamedPosition(name: name, pos: startOfLargeHour.distance(to: date) / hourLength)
        }.filter { $0.pos >= 0 && $0.pos < 1 }
        event.oddSolarTerm = _oddSolarTerms.enumerated().map { offset, date in
            let name = String(Self.oddSolarTermChinese[(offset - 1) %% Self.oddSolarTermChinese.count].replacingOccurrences(of: "　", with: ""))
            return NamedPosition(name: name, pos: startOfLargeHour.distance(to: date) / hourLength)
        }.filter { $0.pos >= 0 && $0.pos < 1 }
        return event
    }

    static func solarTermName(for index: Int) -> String? {
        guard (0..<24).contains(index) else { return nil }
        if index %% 2 == 0 {
            return Locale.translate(Self.evenSolarTermChinese[index / 2])
        } else {
            return Locale.translate(Self.oddSolarTermChinese[index / 2])
        }
    }

    mutating func getSunTimes(for dateType: DateType) -> Solar<NamedDate?> {
        if let existing = _sunTimes[dateType] {
            return existing
        }
        var event = Solar<NamedDate?>(midnight: nil, sunrise: nil, noon: nil, sunset: nil)
        if let location {
            let (start, end) = getStartEnd(type: dateType)
            let mid = start + start.distance(to: end) / 2
            if !apparentTime {
                if let midnight = meridianTime(around: start, at: location, type: .midnight), midnight >= start && midnight < end {
                    event.midnight = .init(name: Self.dayTimeName.midnight, date: midnight)
                } else if let midnight = meridianTime(around: end, at: location, type: .midnight), midnight >= start && midnight < end {
                    event.midnight = .init(name: Self.dayTimeName.midnight, date: midnight)
                }
                if let noon = meridianTime(around: mid, at: location, type: .noon), noon >= start && noon < end {
                    event.noon = .init(name: Self.dayTimeName.noon, date: noon)
                }
            }
            if let sunrise = riseSetTime(around: mid, at: location, type: .sunrise), sunrise >= start && sunrise < end {
                event.sunrise = .init(name: Self.dayTimeName.sunrise, date: sunrise)
            }
            if let sunset = riseSetTime(around: mid, at: location, type: .sunset), sunset >= start && sunset < end {
                event.sunset = .init(name: Self.dayTimeName.sunset, date: sunset)
            }
        }
        _sunTimes[dateType] = event
        return event
    }

    mutating func getMoonTimes(for dateType: DateType) -> Lunar<NamedDate?> {
        if let existing = _moonTimes[dateType] {
            return existing
        }
        var event = Lunar<NamedDate?>(moonrise: nil, highMoon: nil, moonset: nil)
        if let location {
            let (start, end) = getStartEnd(type: dateType)
            if let moonrise = riseSetTime(around: start, at: location, type: .moonrise), moonrise >= start && moonrise < end {
                event.moonrise = .init(name: Self.moonTimeName.moonrise, date: moonrise)
            } else if let moonrise = riseSetTime(around: end, at: location, type: .moonrise), moonrise >= start && moonrise < end {
                event.moonrise = .init(name: Self.moonTimeName.moonrise, date: moonrise)
            }
            if let highMoon = meridianTime(around: start, at: location, type: .highMoon), highMoon >= start && highMoon < end {
                event.highMoon = .init(name: Self.moonTimeName.highMoon, date: highMoon)
            } else if let highMoon = meridianTime(around: end, at: location, type: .highMoon), highMoon >= start && highMoon < end {
                event.highMoon = .init(name: Self.moonTimeName.highMoon, date: highMoon)
            }
            if let moonset = riseSetTime(around: start, at: location, type: .moonset), moonset >= start && moonset < end {
                event.moonset = .init(name: Self.moonTimeName.moonset, date: moonset)
            } else if let moonset = riseSetTime(around: end, at: location, type: .moonset), moonset >= start && moonset < end {
                event.moonset = .init(name: Self.moonTimeName.moonset, date: moonset)
            }
        }
        _moonTimes[dateType] = event
        return event
    }

    var sunMoonPositions: DailyEvent {
        mutating get {
            var dailyEvent = DailyEvent()
            if location != nil {
                let start = startOfDay
                let end = startOfNextDay
                // sun
                let sunEvent = getSunTimes(for: .current)
                dailyEvent.solar = Solar<NamedPosition?>(midnight: nil, sunrise: nil, noon: nil, sunset: nil)
                dailyEvent.solar.midnight = sunEvent.midnight?.toPositionBetween(start: start, end: end)
                dailyEvent.solar.sunrise = sunEvent.sunrise?.toPositionBetween(start: start, end: end)
                dailyEvent.solar.noon = sunEvent.noon?.toPositionBetween(start: start, end: end)
                dailyEvent.solar.sunset = sunEvent.sunset?.toPositionBetween(start: start, end: end)
                // moon
                let moonEvent = getMoonTimes(for: .current)
                dailyEvent.lunar = Lunar<NamedPosition?>(moonrise: nil, highMoon: nil, moonset: nil)
                dailyEvent.lunar.moonrise = moonEvent.moonrise?.toPositionBetween(start: start, end: end)
                dailyEvent.lunar.highMoon = moonEvent.highMoon?.toPositionBetween(start: start, end: end)
                dailyEvent.lunar.moonset = moonEvent.moonset?.toPositionBetween(start: start, end: end)
            }
            return dailyEvent
        }
    }

    var sunMoonSubhourPositions: DailyEvent {
        mutating get {
            var dailyEvent = DailyEvent()
            if location != nil {
                let start = startOfLargeHour
                let end = endOfLargeHour
                // sun
                let sunEvent = getSunTimes(for: .current)
                dailyEvent.solar = Solar<NamedPosition?>(midnight: nil, sunrise: nil, noon: nil, sunset: nil)
                dailyEvent.solar.midnight = sunEvent.midnight?.toPositionBetween(start: start, end: end)
                dailyEvent.solar.sunrise = sunEvent.sunrise?.toPositionBetween(start: start, end: end)
                dailyEvent.solar.noon = sunEvent.noon?.toPositionBetween(start: start, end: end)
                dailyEvent.solar.sunset = sunEvent.sunset?.toPositionBetween(start: start, end: end)
                // moon
                let moonEvent = getMoonTimes(for: .current)
                dailyEvent.lunar = Lunar<NamedPosition?>(moonrise: nil, highMoon: nil, moonset: nil)
                dailyEvent.lunar.moonrise = moonEvent.moonrise?.toPositionBetween(start: start, end: end)
                dailyEvent.lunar.highMoon = moonEvent.highMoon?.toPositionBetween(start: start, end: end)
                dailyEvent.lunar.moonset = moonEvent.moonset?.toPositionBetween(start: start, end: end)
            }
            return dailyEvent
        }
    }
}

// MARK: Chinese Date
extension ChineseCalendar {
    var startOfLargeHour: Date {
        _startHour
    }

    var endOfLargeHour: Date {
        _endHour
    }

    var startOfHour: Date {
        return _hourNames.last {
            $0.hour <= self.time
        }!.hour
    }

    var startOfNextHour: Date {
        _hourNames.first {
            $0.hour > self.time
        }!.hour
    }

    var startOfDay: Date {
        _calendar.startOfDay(for: _time, apparent: apparentTime, location: location)
    }

    var startOfNextDay: Date {
        let nextDay = startOfDay + 86400 * 1.5
        return _calendar.startOfDay(for: nextDay, apparent: apparentTime, location: location)
    }

    var chineseDate: ChineseDate {
        ChineseDate(month: nominalMonth, day: day, leap: isLeapMonth)
    }
    var chineseTime: ChineseTime {
        ChineseTime(hour: hour, quarter: quarterMajor, subQuarter: quarterMinor)
    }
    var chineseDateTime: ChineseDateTime {
        ChineseDateTime(date: chineseDate, time: chineseTime)
    }

    func find(chineseDate: ChineseDate) -> ChineseCalendar? {
        guard (1...12).contains(chineseDate.month) && (1...30).contains(chineseDate.day) else {
            return nil
        }
        var chineseCalendar = self
        if chineseCalendar.month >= chineseCalendar.numberOfMonths {
            chineseCalendar.update(time: chineseCalendar._solarTerms[24] + 1)
        }
        if chineseDate.leap && chineseCalendar._numberOfMonths < 13 {
            return nil
        }
        let monthIndex = chineseDate.monthIndex(in: chineseCalendar) - 1
        chineseCalendar.update(time: chineseCalendar._moonEclipses[monthIndex])

        guard chineseCalendar.nominalMonth == chineseDate.month && chineseCalendar.isLeapMonth == chineseDate.leap else {
            return nil
        }

        var targetDay = chineseDate.day
        if targetDay > chineseCalendar.numberOfDaysInMonth {
            targetDay = chineseCalendar.numberOfDaysInMonth
        }
        if chineseDate.reverseCount {
            targetDay = chineseCalendar.numberOfDaysInMonth + 1 - targetDay
        }
        if targetDay != chineseCalendar.day,
           let newDate = chineseCalendar.calendar.date(byAdding: .day, value: targetDay - chineseCalendar.day, to: chineseCalendar.time) {
            chineseCalendar.update(time: newDate)
        }
        guard chineseCalendar.equals(date: chineseDate) else { return nil }
        return chineseCalendar
    }

    func find(chineseTime: ChineseTime) -> Date? {
        let chineseCalendar = self
        let startOfDay = chineseCalendar.startOfDay

        var distance: Double = 0
        var distanceCap: Double = 0
        let step = chineseCalendar.largeHour ? 2 : 1
        if chineseCalendar.apparentTime {
            let endOfDay = chineseCalendar.startOfNextDay
            distance = startOfDay.distance(to: endOfDay) * Double(chineseTime.smallHour) / 24.0
            distanceCap = startOfDay.distance(to: endOfDay) * Double(chineseTime.smallHour + step) / 24.0
        } else {
            var targetTime = chineseCalendar._calendar.date(byAdding: .day, value: chineseTime.smallHour /% 24, to: startOfDay)!
            targetTime = chineseCalendar._calendar.date(bySetting: .hour, value: chineseTime.smallHour %% 24, of: targetTime)!
            distance = startOfDay.distance(to: targetTime)

            var targetTimeNext = chineseCalendar._calendar.date(byAdding: .day, value: (chineseTime.smallHour + step) /% 24, to: startOfDay)!
            targetTimeNext = chineseCalendar._calendar.date(bySetting: .hour, value: (chineseTime.smallHour + step) %% 24, of: targetTimeNext)!
            distanceCap = startOfDay.distance(to: targetTimeNext)
        }

        let newQuarterDistance = (distance /% 864 + Double(chineseTime.quarter)) * 864.0
        distance = min(distanceCap - 1, max(distance, newQuarterDistance))
        distanceCap = min(distanceCap, newQuarterDistance + 864.0)

        let newQuarterMinorDistance = (distance /% 144 + Double(chineseTime.subQuarter)) * 144.0
        distance = min(distanceCap - 1, max(distance, newQuarterMinorDistance))

        return startOfDay + max(0, distance)
    }

    func find(chineseDateTime: ChineseDateTime) -> Date? {
        let date = find(chineseDate: chineseDateTime.date)
        return date?.find(chineseTime: chineseDateTime.time)
    }

    func findNext(chineseDateTime: ChineseDateTime) -> Date? {
        if let date = find(chineseDateTime: chineseDateTime), date > self.time {
            return date
        } else {
            var nextDate = self
            nextDate.update(time: nextDate._solarTerms[24] + 1)
            return nextDate.find(chineseDateTime: chineseDateTime)
        }
    }

    func nextMonth() -> Date? {
        var datetime = chineseDateTime
        let monthIndex = datetime.date.monthIndex(in: self)
        var chineseCalendar = self
        if monthIndex < chineseCalendar.numberOfMonths {
            datetime.date.update(monthIndex: monthIndex + 1, in: chineseCalendar)
        } else {
            if chineseCalendar.month >= chineseCalendar.numberOfMonths {
                chineseCalendar.update(time: chineseCalendar._solarTerms[24] + 1)
            }
            chineseCalendar.update(time: chineseCalendar._solarTerms[24] + 1)
            datetime.date.update(monthIndex: 1, in: chineseCalendar)
        }
        return chineseCalendar.find(chineseDateTime: datetime)
    }
    func previousMonth() -> Date? {
        var chineseCalendar = self
        var datetime = chineseDateTime
        let monthIndex = datetime.date.monthIndex(in: chineseCalendar)
        if monthIndex > 1 {
            datetime.date.update(monthIndex: monthIndex - 1, in: chineseCalendar)
        } else {
            if chineseCalendar.month >= chineseCalendar.numberOfMonths {
                chineseCalendar.update(time: chineseCalendar._moonEclipses[chineseCalendar.numberOfMonths] - 100000)
            } else {
                chineseCalendar.update(time: chineseCalendar._moonEclipses[0] - 100000)
            }
            datetime.date.update(monthIndex: chineseCalendar.numberOfMonths, in: chineseCalendar)
        }
        return chineseCalendar.find(chineseDateTime: datetime)
    }

    func nextYear() -> Date? {
        var chineseCalendar = self
        var datetime = chineseDateTime
        if chineseCalendar.month >= chineseCalendar.numberOfMonths {
            chineseCalendar.update(time: chineseCalendar._solarTerms[24] + 1)
        }
        chineseCalendar.update(time: chineseCalendar._solarTerms[24] + 1)

        if let date = chineseCalendar.find(chineseDateTime: datetime) {
            return date
        } else if datetime.date.leap {
            datetime.date.leap = false
        }
        return chineseCalendar.find(chineseDateTime: datetime)
    }
    func previousYear() -> Date? {
        var chineseCalendar = self
        var datetime = chineseDateTime
        if chineseCalendar.month >= chineseCalendar.numberOfMonths {
            chineseCalendar.update(time: chineseCalendar._moonEclipses[chineseCalendar.numberOfMonths] - 100000)
        } else {
            chineseCalendar.update(time: chineseCalendar._moonEclipses[0] - 100000)
        }
        if let date = chineseCalendar.find(chineseDateTime: datetime) {
            return date
        } else if chineseDate.leap {
            datetime.date.leap = false
        }
        return chineseCalendar.find(chineseDateTime: datetime)
    }

    func monthLabel(monthIndex: Int) -> String {
        let dummyChineseDate = ChineseCalendar.ChineseDate(monthIndex: monthIndex, in: self)
        if dummyChineseDate.leap {
            return String(localized: "LEAP_MONTH\(ChineseCalendar.monthChineseLocalized[dummyChineseDate.month-1])")
        } else {
            return String(localized: ChineseCalendar.monthChineseLocalized[dummyChineseDate.month-1])
        }
    }

    func hourName(hour: Int) -> String {
        if largeHour {
            return String(localized: "\(ChineseCalendar.terrestrialBranchesLocalized[hour / 2])HOUR")
        } else {
            return String(localized: "\(ChineseCalendar.terrestrialBranchesLocalized[((hour + 1) %% 24) / 2])HOUR,PRELUDE/PROPER\(ChineseCalendar.subHourNameLocalized[(hour + 1) %% 2])")

        }
    }
}

// MARK: Ticks
extension ChineseCalendar {
    var monthTicks: Ticks {
        let months = self.monthNames
        var ticks = Ticks()
        var monthDivides: [Double]
        if _globalMonth {
            monthDivides = _moonEclipses.map { _solarTerms[0].distance(to: $0) / _yearLength }
        } else {
            monthDivides = _moonEclipses.map { _solarTerms[0].distance(to: _calendar.startOfDay(for: $0, apparent: apparentTime, location: location)) / _yearLength }
        }
        monthDivides = monthDivides.filter { $0 > 0 && $0 <= 1 }
        guard months.count == monthDivides.count else { return ticks }
        var previousMonthDivide = 0.0
        var monthNames = [Ticks.TickName]()
        let minMonthLength: Double = (_compact ? 0.009 : 0.006)
        for i in 0..<monthDivides.count {
            let position = (monthDivides[i] + previousMonthDivide) / 2
            if position - previousMonthDivide > minMonthLength * Double(months[i].count) {
                monthNames.append(Ticks.TickName(
                    pos: position,
                    name: months[i],
                    active: previousMonthDivide <= currentDayInYear
                ))
            }
            previousMonthDivide = monthDivides[i]
        }
        if let lastDivide = monthDivides.last, lastDivide < 1 {
            let position = (1 + previousMonthDivide) / 2
            if position - previousMonthDivide > minMonthLength * Double(months[0].count) {
                monthNames.append(Ticks.TickName(
                    pos: position,
                    name: months[0],
                    active: previousMonthDivide <= currentDayInYear
                ))
            }
        } else {
            _ = monthDivides.popLast()
        }

        ticks.majorTicks = [0] + monthDivides
        ticks.majorTickNames = monthNames
        ticks.minorTicks = _fullMoons.map { _solarTerms[0].distance(to: $0) / _yearLength }.filter { ($0 < 1) && ($0 > 0) }
        return ticks
    }

    var dayTicks: Ticks {
        var ticks = Ticks()

        let monthStart: Date
        let monthEnd: Date
        var date: Date
        if _globalMonth {
            monthStart = _moonEclipses[_preciseMonth]
            monthEnd = _moonEclipses[_preciseMonth + 1]
            date = _calendar.startOfDay(for: monthStart, apparent: apparentTime, location: location)
        } else {
            monthStart = _calendar.startOfDay(for: _moonEclipses[_month], apparent: apparentTime, location: location)
            monthEnd = _calendar.startOfDay(for: _moonEclipses[_month + 1], apparent: apparentTime, location: location)
            date = monthStart
        }

        var dayDivides = [Date]()
        while date < monthEnd {
            if apparentTime {
                date += 86400 * 1.5
                date = _calendar.startOfDay(for: date, apparent: apparentTime, location: location)
            } else {
                date = _calendar.date(byAdding: .day, value: 1, to: date)!
            }
            dayDivides.append(date)
        }
        let majorTicks: [Double] = dayDivides.map { monthStart.distance(to: $0) / monthStart.distance(to: monthEnd) }.filter { $0 > 0 && $0 < 1 }

        let allDayNames: [String]
        if _compact {
            allDayNames = Self.dayChineseCompact.slice(to: numberOfDaysInMonth) + [Self.dayChineseCompact[0]]
        } else {
            allDayNames = Self.dayChinese.slice(to: numberOfDaysInMonth) + [Self.dayChinese[0]]
        }

        var dayNames = [Ticks.TickName]()
        var previousDayDivide = 0.0
        let minDayLength = (_compact ? 0.009 : 0.006)
        for i in 0..<majorTicks.count {
            let position = (majorTicks[i] + previousDayDivide) / 2
            if position - previousDayDivide > minDayLength * Double(allDayNames[i].count) {
                dayNames.append(Ticks.TickName(
                    pos: position,
                    name: allDayNames[i],
                    active: previousDayDivide <= currentDayInMonth
                ))
            }
            previousDayDivide = majorTicks[i]
        }
        let position = (1 + previousDayDivide) / 2
        if position - previousDayDivide > minDayLength * Double(allDayNames[majorTicks.count].count) {
            dayNames.append(Ticks.TickName(
                pos: position,
                name: allDayNames[majorTicks.count],
                active: previousDayDivide <= currentDayInMonth
            ))
        }
        ticks.majorTicks = [0] + majorTicks
        ticks.majorTickNames = dayNames
        return ticks
    }

    var hourTicks: Ticks {
        let startOfDay = startOfDay
        let startOfNextDay = startOfNextDay
        var ticks = Ticks()
        var hourDivides = [Double]()
        var quarterTick = [Double]()
        var quarter = 0.0
        while quarter < 1.0 {
            quarterTick.append(quarter)
            quarter += 864 / startOfDay.distance(to: startOfNextDay)
        }
        quarterTick = Array(Set(quarterTick).subtracting(hourDivides)).sorted()
        var hourNames = [Ticks.TickName]()
        var hourStart = startOfDay

        for namedHour in _hourNames {
            if namedHour.hour >= startOfDay && namedHour.hour < startOfNextDay {
                let dividePos = startOfDay.distance(to: namedHour.hour) / startOfDay.distance(to: startOfNextDay)
                if !namedHour.longName.isEmpty {
                    hourDivides.append(dividePos)
                }
                if _largeHour || !namedHour.shortName.isEmpty {
                    if _largeHour {
                        hourStart = namedHour.hour
                    }
                    hourNames.append(Ticks.TickName(
                        pos: dividePos,
                        name: namedHour.shortName,
                        active: hourStart <= _time
                    ))
                } else {
                    if !namedHour.longName.isEmpty {
                        hourStart = namedHour.hour
                    }
                }
            }
        }
        ticks.majorTicks = hourDivides
        ticks.majorTickNames = hourNames
        ticks.minorTicks = quarterTick
        return ticks
    }

    var subhourTicks: Ticks {
        let startHour = startOfLargeHour
        let endHour = endOfLargeHour
        var ticks = Ticks()
        var subHourTicks = Set<Double>()
        var majorTickNames = [String]()
        for namedHour in _hourNamesInCurrentHour {
            majorTickNames.append(namedHour.longName)
            let distPos = startHour.distance(to: namedHour.hour) / startHour.distance(to: endHour)
            if distPos >= 0.0 && distPos < 1.0 {
                subHourTicks.insert(distPos)
            }
        }

        let majorTicks = subHourTicks
        for tickTime in _subhours {
            let distPos = startHour.distance(to: tickTime) / startHour.distance(to: endHour)
            if distPos >= 0.0 && distPos < 1.0 {
                subHourTicks.insert(distPos)
            }
        }

        let minimumSubhourLength = _compact ? 0.045 : 0.03
        var subHourNames = [Ticks.TickName]()
        var count = 1
        var j = 0
        let subHourTick = Array(subHourTicks).sorted()
        for i in 0..<subHourTick.count {
            if majorTicks.contains(subHourTick[i]) {
                subHourNames.append(Ticks.TickName(
                    pos: subHourTick[i],
                    name: majorTickNames[j],
                    active: subHourTick[i] <= subhourInHour
                ))
                j += 1
                count = 1
            } else {
                if min((subHourTick[i] - subHourTick[(i - 1) %% subHourTick.count]) %% 1.0, (subHourTick[(i + 1) %% subHourTick.count] - subHourTick[i]) %% 1.0) > minimumSubhourLength {
                    subHourNames.append(Ticks.TickName(
                        pos: subHourTick[i],
                        name: Self.chineseNumbers[count],
                        active: subHourTick[i] <= subhourInHour
                    ))
                }
                count += 1
            }
        }

        var subQuarterTicks = Set<Double>()
        for tickTime in _subhourMinors {
            subQuarterTicks.insert(startHour.distance(to: tickTime) / startHour.distance(to: endHour))
        }
        subQuarterTicks = subQuarterTicks.subtracting(subHourTicks)
        let subQuarterTick = Array(subQuarterTicks).sorted()

        ticks.majorTicks = subHourTick
        ticks.majorTickNames = subHourNames
        ticks.minorTicks = subQuarterTick
        return ticks
    }
}

// MARK: Nested Structs
extension ChineseCalendar {
    struct ChineseTime: Hashable, Equatable, Codable {
        var largeHour: Int = 0
        var hourProper: Bool = true
        var quarter: Int = 0
        var subQuarter: Int = 0

        var smallHour: Int {
            get {
                (largeHour * 2 - (hourProper ? 0 : 1)) %% 24
            } set {
                largeHour = ((newValue + 1) /% 2) %% 12
                hourProper = newValue.isMultiple(of: 2)
            }
        }
    }

    struct ChineseDate: Hashable, Equatable, Codable {
        var month: Int = 1
        var day: Int = 1
        var leap = false
        var reverseCount = false
    }

    struct ChineseDateTime: Hashable, Equatable, Codable {
        var date: ChineseDate
        var time: ChineseTime
    }

    struct Hour: Equatable {
        enum HourFormat: Equatable {
            case full
            case partial(index: Int)
        }
        var hour: Int
        var format: HourFormat
        var string: String {
            guard (0..<ChineseCalendar.terrestrialBranches.count).contains(hour) else { return "" }
            switch format {
            case .full:
                return ChineseCalendar.terrestrialBranches[hour]
            case .partial(let index):
                guard (0..<ChineseCalendar.subHourName.count).contains(index) else { return "" }
                return "\(ChineseCalendar.terrestrialBranches[hour])\(ChineseCalendar.subHourName[index])"
            }
        }
        var stringLocalized: LocalizedStringResource {
            guard (0..<ChineseCalendar.terrestrialBranchesLocalized.count).contains(hour) else { return "" }
            switch format {
            case .full:
                return "\(ChineseCalendar.terrestrialBranchesLocalized[hour])HOUR"
            case .partial(let index):
                guard (0..<ChineseCalendar.subHourNameLocalized.count).contains(index) else { return "" }
                return "\(ChineseCalendar.terrestrialBranchesLocalized[hour])HOUR,PRELUDE/PROPER\(ChineseCalendar.subHourNameLocalized[index])"
            }
        }
    }
    struct SubHour: Equatable {
        var majorTick: Int
        var minorTick: Int
        var shortString: String {
            guard (0..<ChineseCalendar.chineseNumbers.count).contains(majorTick) else { return "" }
            return "\(ChineseCalendar.chineseNumbers[majorTick])刻"
        }
        var shortStringLocalized: LocalizedStringResource {
            guard (0..<ChineseCalendar.chineseNumbersLocalized.count).contains(majorTick) else { return "" }
            return "\(ChineseCalendar.chineseNumbersLocalized[majorTick])QUARTER"
        }
        var string: String {
            guard (0..<ChineseCalendar.chineseNumbers.count).contains(majorTick) && (0..<ChineseCalendar.chineseNumbers.count).contains(minorTick) else { return "" }
            var str = "\(ChineseCalendar.chineseNumbers[majorTick])刻"
            if minorTick > 0 {
                str += ChineseCalendar.chineseNumbers[minorTick]
            }
            return str
        }
        var stringLocalized: LocalizedStringResource {
            guard (0..<ChineseCalendar.chineseNumbersLocalized.count).contains(majorTick) && (0..<ChineseCalendar.chineseNumbersLocalized.count).contains(minorTick) else { return "" }
            if minorTick > 0 {
                return "\(ChineseCalendar.chineseNumbersLocalized[majorTick])QUARTER_AND\(ChineseCalendar.chineseNumbersLocalized[minorTick])"
            } else {
                return "\(ChineseCalendar.chineseNumbersLocalized[majorTick])QUARTER"
            }
        }
    }

    struct NamedHour: Equatable {
        let hour: Date
        let shortName: String
        let longName: String
    }

    struct NamedPosition: NamedPoint {
        let name: String
        let pos: Double
    }

    struct NamedDate: Equatable, Codable {
        let name: String
        let date: Date
        func toPositionBetween(start: Date, end: Date) -> NamedPosition? {
            guard date >= start && date < end else { return nil }
            let position = start.distance(to: date) / start.distance(to: end)
            return NamedPosition(name: name, pos: position)
        }
    }

    struct CelestialEvent: Equatable {
        var eclipse = [NamedPosition]()
        var fullMoon = [NamedPosition]()
        var oddSolarTerm = [NamedPosition]()
        var evenSolarTerm = [NamedPosition]()
    }

    struct DailyEvent: Equatable {
        var solar = Solar<NamedPosition?>(midnight: nil, sunrise: nil, noon: nil, sunset: nil)
        var lunar = Lunar<NamedPosition?>(moonrise: nil, highMoon: nil, moonset: nil)
    }

    enum DateType {
        case current, previous, next
    }

    struct Ticks: Equatable {
        struct TickName: NamedPoint {
            var pos: Double = 0.0
            var name: String = ""
            var active: Bool = false
        }

        var majorTicks = [Double]()
        var majorTickNames = [TickName]()
        var minorTicks = [Double]()
    }
}

extension ChineseCalendar.ChineseDate {
    func monthIndex(in chineseCalendar: ChineseCalendar) -> Int {
        if let leapMonth = chineseCalendar.leapMonth,
           (month + 1) %% 12 >= leapMonth || (leap && (month + 1) %% 12 == leapMonth - 1) {
            return (month + 2) %% 13 + 1
        } else {
            return (month + 1) %% 12 + 1
        }
    }

    mutating func update(monthIndex: Int? = nil, in chineseCalendar: ChineseCalendar) {
        if let monthIndex {
            month = (monthIndex - 3) %% 12 + 1
            leap = false
            if let leapMonth = chineseCalendar.leapMonth {
                if monthIndex >= leapMonth + 1 {
                    if monthIndex == leapMonth + 1 {
                        leap = true
                    }
                    month = (month - 2) %% 12 + 1
                }
            }
        }
    }

    init(month: Int? = nil, day: Int? = nil, leap: Bool? = nil, reverseCount: Bool? = nil) {
        self.init()
        self.month ?= month
        self.day ?= day
        self.leap ?= leap
        self.reverseCount ?= reverseCount
    }

    init(monthIndex: Int, day: Int? = nil, reverseCount: Bool? = nil, in chineseCalendar: ChineseCalendar) {
        self.init()
        self.update(monthIndex: monthIndex, in: chineseCalendar)
    }
}

extension ChineseCalendar.ChineseTime {
    init(hour: Int? = nil, quarter: Int? = nil, subQuarter: Int? = nil) {
        self.init()
        self.smallHour ?= hour
        self.quarter ?= quarter
        self.subQuarter ?= subQuarter
    }
}

// MARK: Mutating Updates - Private
private extension ChineseCalendar {
    mutating func updateYear() {
        var year = calendar.component(.year, from: time)
        var solarTerms = SolarLunarData(year: year + 1).solarTerms
        if solarTerms[0] <= time {
            year += 1
            solarTerms += SolarLunarData(year: year + 1).solarTerms[0...4]
        } else {
            var solarTermsCurrentYear = SolarLunarData(year: year).solarTerms
            solarTermsCurrentYear += solarTerms[0...4]
            solarTerms = solarTermsCurrentYear
        }

        let previousYearSolarTerms = SolarLunarData(year: year - 1).solarTerms
        let moonPhases = SolarLunarData(year: year - 1).moonPhases + SolarLunarData(year: year).moonPhases + SolarLunarData(year: year + 1).moonPhases
        var eclipse = moonPhases.slice(from: SolarLunarData(year: year - 1).firstLunarPhase == .newMoon ? 0 : 1, step: 2)
        var fullMoon = moonPhases.slice(from: SolarLunarData(year: year - 1).firstLunarPhase == .fullMoon ? 0 : 1, step: 2)
        var start: Int?, end: Int?
        for i in 0..<eclipse.count {
            let eclipseDate: Date
            if _globalMonth {
                eclipseDate = eclipse[i]
            } else {
                eclipseDate = calendar.startOfDay(for: eclipse[i], apparent: apparentTime, location: location)
            }
            if start == nil, eclipseDate >= solarTerms[0] {
                start = i - 1
            }
            if end == nil, eclipseDate > solarTerms[24] {
                end = i
            }
        }
        eclipse = eclipse.slice(from: start!, to: end! + 2)
        fullMoon = fullMoon.filter { $0 < eclipse.last! && $0 > eclipse[0] }
        let evenSolarTerms = solarTerms.slice(step: 2)

        var i = 0
        var j = 0
        var count = 0
        var solaticeInMonth = [Int]()
        var monthCount = Set<Date>()
        while i + 1 < eclipse.count, j < evenSolarTerms.count {
            let thisEclipse: Date
            let nextEclipse: Date
            if _globalMonth {
                thisEclipse = eclipse[i]
                nextEclipse = eclipse[i + 1]
            } else {
                thisEclipse = calendar.startOfDay(for: eclipse[i], apparent: apparentTime, location: location)
                nextEclipse = calendar.startOfDay(for: eclipse[i + 1], apparent: apparentTime, location: location)
            }
            if thisEclipse <= evenSolarTerms[j], nextEclipse > evenSolarTerms[j] {
                count += 1
                j += 1
            } else {
                solaticeInMonth.append(count)
                count = 0
                i += 1
            }
            if thisEclipse > solarTerms[0], thisEclipse <= solarTerms[24] {
                monthCount.insert(thisEclipse)
            }
        }

        var leapMonth = -1
        if monthCount.count > 12 {
            for i in 0..<solaticeInMonth.count {
                if solaticeInMonth[i] == 0, leapMonth < 0 {
                    leapMonth = i
                    break
                }
            }
        }

        _solarTerms = Array(solarTerms[0...24])
        _yearLength = solarTerms[0].distance(to: solarTerms[24])
        var evenSolar = solarTerms.slice(from: 0, step: 2)
        evenSolar.insert(previousYearSolarTerms[previousYearSolarTerms.count - 2], at: 0)
        _evenSolarTerms = evenSolar
        var oddSolar = solarTerms.slice(from: 1, step: 2)
        oddSolar.insert(previousYearSolarTerms[previousYearSolarTerms.count - 1], at: 0)
        _oddSolarTerms = oddSolar
        _moonEclipses = eclipse
        _fullMoons = fullMoon
        _leapMonth = leapMonth
        _year = year
        _numberOfMonths = monthCount.count
    }

    mutating func updateDate() {
        var i = 0
        while i < _moonEclipses.count - 1 {
            let startOfEclipse = _calendar.startOfDay(for: _moonEclipses[i], apparent: apparentTime, location: location)
            let startOfDate = _calendar.startOfDay(for: _time, apparent: apparentTime, location: location)
            if startOfEclipse > startOfDate {
                break
            }
            i += 1
        }
        var j = 0
        while j < _moonEclipses.count - 1 {
            if _moonEclipses[j] > _time {
                break
            }
            j += 1
        }
        let previousEclipse = _calendar.startOfDay(for: _moonEclipses[i - 1], apparent: apparentTime, location: location)
        let startOfDate = _calendar.startOfDay(for: _time, apparent: apparentTime, location: location)
        let dateDiff = Int(round(previousEclipse.distance(to: startOfDate) / 86400))
        _month = i - 1
        _preciseMonth = j - 1
        _day = dateDiff
    }

    mutating func updateHour() {
        let startOfDay = startOfDay
        let startOfNextDay = startOfNextDay
        var tempStartHour: Date?
        var tempEndHour: Date?
        var hour = if apparentTime {
            startOfDay - 2 * startOfDay.distance(to: startOfNextDay) / 24
        } else {
            _calendar.date(byAdding: .hour, value: -2, to: startOfDay)!
        }
        let end = if apparentTime {
            startOfNextDay + 2 * startOfDay.distance(to: startOfNextDay) / 24
        } else {
            _calendar.date(byAdding: .hour, value: 2, to: startOfNextDay)!
        }
        _hourNames = []
        var prevHourName = ""
        var prevOffsetHourName = ""
        var prevLongName = ""
        while hour < end {
            let hourIndex = if apparentTime {
                Int(round(startOfDay.distance(to: hour) / startOfDay.distance(to: startOfNextDay) * 24))
            } else {
                _calendar.component(.hour, from: hour)
            }
            let hourName = Self.terrestrialBranches[(hourIndex /% 2) %% 12]
            let offsetHourName = Self.terrestrialBranches[((hourIndex + 1) /% 2) %% 12]
            if !_largeHour || hourName != prevHourName {
                let shortName = if hourName != prevHourName {
                    ChineseCalendar.terrestrialBranches[(hourIndex /% 2) %% 12]
                } else {
                    ""
                }
                let longName: String
                if _largeHour {
                    if hourName != prevHourName {
                        longName = Self.terrestrialBranches[(hourIndex /% 2) %% 12]
                    } else {
                        longName = ""
                    }
                } else {
                    let name = Self.terrestrialBranches[((hourIndex + 1) /% 2) %% 12] + Self.subHourName[(hourIndex + 1) %% 2]
                    if name != prevLongName {
                        prevLongName = name
                        longName = name
                    } else {
                        longName = ""
                    }
                }
                _hourNames.append(NamedHour(hour: hour, shortName: shortName, longName: longName))
            }
            if hour <= _time {
                if _largeHour {
                    _hour = Hour(hour: (hourIndex /% 2) %% 12, format: .full)
                } else {
                    _hour = Hour(hour: ((hourIndex + 1) /% 2) %% 12, format: .partial(index: (hourIndex + 1) %% 2))
                }
            }
            let changeOfHour = if _largeHour {
                hourName != prevHourName
            } else {
                offsetHourName != prevOffsetHourName
            }
            if changeOfHour, hour <= _time {
                tempStartHour = hour
            }
            if changeOfHour, hour > _time, tempEndHour == nil {
                tempEndHour = hour
            }
            if apparentTime {
                hour += startOfDay.distance(to: startOfNextDay) / 24
            } else {
                hour = _calendar.date(byAdding: .hour, value: 1, to: hour)!
            }
            prevHourName = hourName
            prevOffsetHourName = offsetHourName
        }
        _startHour = tempStartHour!
        _endHour = tempEndHour!
        _sunTimes = [:]
        _moonTimes = [:]
    }

    mutating func updateSubHour() {
        _hourNamesInCurrentHour = []
        _subhours = []
        _subhourMinors = []

        var currentSmallHour = startOfLargeHour
        for namedHour in _hourNames {
            if !namedHour.longName.isEmpty && namedHour.hour >= startOfLargeHour && namedHour.hour < endOfLargeHour {
                _hourNamesInCurrentHour.append(namedHour)
                if namedHour.hour <= _time {
                    currentSmallHour = namedHour.hour
                }
            }
        }

        var majorTickCount = 0
        var tickTime = startOfDay - 864 * 6
        var currentSubhour = currentSmallHour
        while tickTime < endOfLargeHour - 16 {
            if tickTime > startOfLargeHour + 16 {
                _subhours.append(tickTime)
            }
            if tickTime > currentSmallHour && time >= tickTime {
                currentSubhour = tickTime
                majorTickCount += 1
            }
            tickTime += 864
        }

        var minorTickCount = 0
        tickTime = startOfDay - 864 * 6
        while tickTime < endOfLargeHour {
            if tickTime > startOfLargeHour {
                _subhourMinors.append(tickTime)
            }
            if tickTime > currentSubhour && time >= tickTime {
                minorTickCount += 1
            }
            tickTime += 144
        }
        _quarter = SubHour(majorTick: majorTickCount, minorTick: minorTickCount)
    }

    mutating func updatePlanets() {
        let solarSystem = SolarSystem(time: _time, lat: location?.lat, lon: location?.lon, targets: .all)
        let offset = currentDayInYear - solarSystem.planets.sun.loc.ra / Double.pi / 2
        let planets = Planets<NamedPosition>(
            moon: .init(name: Self.planetNames.moon, pos: ((solarSystem.planets.moon.loc.ra) / Double.pi / 2 + offset) %% 1.0),
            mercury: .init(name: Self.planetNames.mercury, pos: ((solarSystem.planets.mercury.loc.ra) / Double.pi / 2 + offset) %% 1.0),
            venus: .init(name: Self.planetNames.venus, pos: ((solarSystem.planets.venus.loc.ra) / Double.pi / 2 + offset) %% 1.0),
            mars: .init(name: Self.planetNames.mars, pos: ((solarSystem.planets.mars.loc.ra) / Double.pi / 2 + offset) %% 1.0),
            jupiter: .init(name: Self.planetNames.jupiter, pos: ((solarSystem.planets.jupiter.loc.ra) / Double.pi / 2 + offset) %% 1.0),
            saturn: .init(name: Self.planetNames.saturn, pos: ((solarSystem.planets.saturn.loc.ra) / Double.pi / 2 + offset) %% 1.0)
        )
        _planets = planets
    }

    func getStartEnd(type: DateType) -> (start: Date, end: Date) {
        let start: Date
        let end: Date
        switch type {
        case .current:
            start = startOfDay
            end = startOfNextDay
        case .previous:
            end = startOfDay
            start = _calendar.startOfDay(for: end - 3600, apparent: apparentTime, location: location)
        case .next:
            start = startOfNextDay
            end = _calendar.startOfDay(for: start + 90000, apparent: apparentTime, location: location)
        }
        return (start: start, end: end)
    }

    func equals(date: ChineseDate) -> Bool {
        let effectiveDay = min(date.day, numberOfDaysInMonth)
        let dayMatch = if date.reverseCount {
            effectiveDay == numberOfDaysInMonth - day + 1
        } else {
            effectiveDay == day
        }
        return date.leap == isLeapMonth && date.month == nominalMonth && dayMatch
    }
}

// MARK: Planet Model - Private
private extension ChineseCalendar {
    enum RiseSetType {
        case sunrise, sunset, moonrise, moonset
    }
    enum MeridianType {
        case noon, midnight, highMoon, lowMoon
    }

    func riseSetTime(around time: Date, at loc: GeoLocation, type: RiseSetType, iteration: Int = 0) -> Date? {
        let solarSystem: SolarSystem
        let planet: SolarSystem.Planet
        switch type {
        case .sunrise, .sunset:
            solarSystem = SolarSystem(time: time, lat: loc.lat, lon: loc.lon, targets: .sun)
            planet = solarSystem.planets.sun
        case .moonrise, .moonset:
            solarSystem = SolarSystem(time: time, lat: loc.lat, lon: loc.lon, targets: .sunMoon)
            planet = solarSystem.planets.moon
        }
        let timeUntilNoon = SolarSystem.normalize(radian: planet.loc.ra - solarSystem.localSiderialTime!)
        let solarHeight = -planet.diameter / 2 - SolarSystem.aeroAdj
        let localHourAngle = (sin(solarHeight) - sin(loc.lat / 180 * Double.pi) * sin(planet.loc.decl)) / (cos(loc.lat / 180 * Double.pi) * cos(planet.loc.decl))

        if abs(localHourAngle) < 1 || iteration < 3 {
            let netTime = switch type {
            case .sunrise, .moonrise:
                timeUntilNoon - acos(min(1, max(-1, localHourAngle)))
            case .sunset, .moonset:
                timeUntilNoon + acos(min(1, max(-1, localHourAngle)))
            }
            let dTime = netTime / Double.pi * 43082.04
            if abs(dTime) < 14.4 && abs(localHourAngle) < 1 {
                return time
            } else {
                return riseSetTime(around: time + dTime, at: loc, type: type, iteration: iteration + 1)
            }
        } else {
            return nil
        }
    }

    func meridianTime(around time: Date, at loc: GeoLocation, type: MeridianType, iteration: Int = 0) -> Date? {
        let solarSystem: SolarSystem
        let planet: SolarSystem.Planet
        switch type {
        case .noon, .midnight:
            solarSystem = SolarSystem(time: time, lat: loc.lat, lon: loc.lon, targets: .sun)
            planet = solarSystem.planets.sun
        case .highMoon, .lowMoon:
            solarSystem = SolarSystem(time: time, lat: loc.lat, lon: loc.lon, targets: .sunMoon)
            planet = solarSystem.planets.moon
        }
        let offset = switch type {
        case .noon, .highMoon:
            0.0
        case .midnight, .lowMoon:
            Double.pi
        }
        let timeUntilNoon = SolarSystem.normalize(radian: planet.loc.ra - solarSystem.localSiderialTime! + offset)

        let dTime = timeUntilNoon / Double.pi * 43082.04
        if abs(dTime) < 14.4 {
            let latInRadian = loc.lat * Double.pi / 180
            let localHourAngle = solarSystem.localSiderialTime! - planet.loc.ra
            let solarHeightSin = sin(latInRadian) * sin(planet.loc.decl) + cos(latInRadian) * cos(planet.loc.decl) * cos(localHourAngle)
            let solarHeight = asin(solarHeightSin)
            let solarHeightMin = -planet.diameter / 2 - SolarSystem.aeroAdj
            switch type {
            case .noon, .highMoon:
                if solarHeight >= solarHeightMin {
                    return time
                } else {
                    return nil
                }
            case .midnight, .lowMoon:
                if solarHeight < solarHeightMin {
                    return time
                } else {
                    return nil
                }
            }
        } else {
            return meridianTime(around: time + dTime, at: loc, type: type, iteration: iteration + 1)
        }
    }
}
