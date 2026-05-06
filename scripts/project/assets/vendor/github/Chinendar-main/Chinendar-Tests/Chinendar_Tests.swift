//
//  Chinendar_Tests.swift
//  Chinendar-Tests
//
//  Created by Leo Liu on 9/26/24.
//

import Testing
import Foundation

extension Date {
    static func from(year: Int, month: Int, day: Int, hour: Int, minute: Int, timezone: TimeZone?) -> Date? {
        var dateComponents = DateComponents()
        dateComponents.year = year
        dateComponents.month = month
        dateComponents.day = day
        dateComponents.hour = hour
        dateComponents.minute = minute
        if let timezone {
            dateComponents.timeZone = timezone
        }
        return Calendar(identifier: .iso8601).date(from: dateComponents)
    }

    static func from(year: Int, month: Int, day: Int, hour: Int=0, minute: Int=0) -> Date {
        Date.from(year: year, month: month, day: day, hour: hour, minute: minute, timezone: TimeZone(identifier: "America/New_York")!)!
    }
}

struct Chinendar_Tests {
    let timeZone = TimeZone(identifier: "America/New_York")!
    let location = GeoLocation(lat: 40, lon: -74)

    @Test("Find date, Month 11 before winter solstice", arguments: [
        (ChineseCalendar.ChineseDate(month: 11, day: 20), Date.from(year: 2024, month: 12, day: 20)),
        (ChineseCalendar.ChineseDate(month: 11, day: 21), Date.from(year: 2024, month: 12, day: 21)),
        (ChineseCalendar.ChineseDate(month: 11, day: 22), Date.from(year: 2024, month: 12, day: 22))

    ])
    func find_1(chineseDate: ChineseCalendar.ChineseDate, targetDate: Date) async throws {
        let testDate = Date.from(year: 2024, month: 12, day: 20, hour: 0, minute: 0, timezone: timeZone)!
        let chineseCalendar = ChineseCalendar(time: testDate, timezone: timeZone, location: location, globalMonth: true, apparentTime: false, largeHour: true)
        let start = chineseCalendar.find(chineseDate: chineseDate)?.time ?? .distantPast
        let calendar = chineseCalendar.calendar
        #expect(calendar.isDate(start, equalTo: targetDate, toGranularity: .day))
    }

    @Test("Find date, Month 11 after winter solstice", arguments: [
        (ChineseCalendar.ChineseDate(month: 11, day: 20), Date.from(year: 2024, month: 12, day: 20)),
        (ChineseCalendar.ChineseDate(month: 11, day: 21), Date.from(year: 2024, month: 12, day: 21)),
        (ChineseCalendar.ChineseDate(month: 11, day: 22), Date.from(year: 2024, month: 12, day: 22))

    ])
    func find_2(chineseDate: ChineseCalendar.ChineseDate, targetDate: Date) async throws {
        let testDate = Date.from(year: 2024, month: 12, day: 22, hour: 0, minute: 0, timezone: timeZone)!
        let chineseCalendar = ChineseCalendar(time: testDate, timezone: timeZone, location: location, globalMonth: true, apparentTime: false, largeHour: true)
        let start = chineseCalendar.find(chineseDate: chineseDate)?.time ?? .distantPast
        let calendar = chineseCalendar.calendar
        #expect(calendar.isDate(start, equalTo: targetDate, toGranularity: .day))
    }

    @Test("Previous year in Chinendar", arguments: [
        (Date.from(year: 2024, month: 12, day: 20), Date.from(year: 2023, month: 12, day: 31)),
        (Date.from(year: 2024, month: 12, day: 21), Date.from(year: 2024, month: 1, day: 1)),
        (Date.from(year: 2024, month: 2, day: 9), Date.from(year: 2023, month: 1, day: 21))

    ])
    func prevYear(testDate: Date, targetDate: Date) async throws {
        let chineseCalendar = ChineseCalendar(time: testDate, timezone: timeZone, location: location, globalMonth: true, apparentTime: false, largeHour: true)
        let start = chineseCalendar.previousYear() ?? .distantPast
        let calendar = chineseCalendar.calendar
        #expect(calendar.isDate(start, equalTo: targetDate, toGranularity: .day))
    }

    @Test("Next year in Chinendar", arguments: [
        (Date.from(year: 2023, month: 12, day: 31), Date.from(year: 2024, month: 12, day: 20)),
        (Date.from(year: 2024, month: 1, day: 1), Date.from(year: 2024, month: 12, day: 21)),
        (Date.from(year: 2023, month: 1, day: 21), Date.from(year: 2024, month: 2, day: 9))

    ])
    func nextYear(testDate: Date, targetDate: Date) async throws {
        let chineseCalendar = ChineseCalendar(time: testDate, timezone: timeZone, location: location, globalMonth: true, apparentTime: false, largeHour: true)
        let start = chineseCalendar.nextYear() ?? .distantPast
        let calendar = chineseCalendar.calendar
        #expect(calendar.isDate(start, equalTo: targetDate, toGranularity: .day))
    }

    @Test("Previous month in Chinendar", arguments: [
        (Date.from(year: 2024, month: 12, day: 20), Date.from(year: 2024, month: 11, day: 20)),
        (Date.from(year: 2024, month: 12, day: 21), Date.from(year: 2024, month: 11, day: 21)),
        (Date.from(year: 2024, month: 2, day: 9), Date.from(year: 2024, month: 1, day: 11)),
        (Date.from(year: 2024, month: 1, day: 11), Date.from(year: 2023, month: 12, day: 12))

    ])
    func prevMonth(testDate: Date, targetDate: Date) async throws {
        let chineseCalendar = ChineseCalendar(time: testDate, timezone: timeZone, location: location, globalMonth: true, apparentTime: false, largeHour: true)
        let start = chineseCalendar.previousMonth() ?? .distantPast
        let calendar = chineseCalendar.calendar
        #expect(calendar.isDate(start, equalTo: targetDate, toGranularity: .day))
    }

    @Test("Next month in Chinendar", arguments: [
        (Date.from(year: 2024, month: 11, day: 20), Date.from(year: 2024, month: 12, day: 20)),
        (Date.from(year: 2024, month: 11, day: 21), Date.from(year: 2024, month: 12, day: 21)),
        (Date.from(year: 2024, month: 1, day: 11), Date.from(year: 2024, month: 2, day: 9)),
        (Date.from(year: 2023, month: 12, day: 12), Date.from(year: 2024, month: 1, day: 11))

    ])
    func nextMonth(testDate: Date, targetDate: Date) async throws {
        let chineseCalendar = ChineseCalendar(time: testDate, timezone: timeZone, location: location, globalMonth: true, apparentTime: false, largeHour: true)
        let start = chineseCalendar.nextMonth() ?? .distantPast
        let calendar = chineseCalendar.calendar
        #expect(calendar.isDate(start, equalTo: targetDate, toGranularity: .day))
    }

    @Test("Date conversion", arguments: [
        (TimeZone(identifier: "America/New_York")!, GeoLocation(lat: 40, lon: -74), false, "九月八日巳時七刻四"),
        (TimeZone(identifier: "Asia/Seoul")!, GeoLocation(lat: 40, lon: 135), false, "九月八日子時二刻五"),
        (TimeZone(identifier: "Asia/Shanghai")!, GeoLocation(lat: 40, lon: 116), false, "九月七日亥時七刻四"),
        (TimeZone(identifier: "Asia/Shanghai")!, GeoLocation(lat: 34.52, lon: 108.94), true, "九月七日亥時五刻三")
    ])
    func dateString(timezone: TimeZone, location: GeoLocation, apparentTime: Bool, targetString: String) async throws {
        let testDate = Date.from(year: 2024, month: 10, day: 9, hour: 11, minute: 43, timezone: timeZone)!
        let chineseCalendar = ChineseCalendar(time: testDate, timezone: timezone, location: location, globalMonth: true, apparentTime: apparentTime, largeHour: true)
        #expect("\(chineseCalendar.dateString)\(chineseCalendar.timeString)" == targetString)
    }

    @Test("Find date, Month 11 before winter solstice", arguments: [
        (ChineseCalendar.ChineseDate(month: 8, day: 15), Date.from(year: 2025, month: 10, day: 5)),
        (ChineseCalendar.ChineseDate(month: 12, day: 8), Date.from(year: 2026, month: 1, day: 25)),
        (ChineseCalendar.ChineseDate(month: 12, day: 30), Date.from(year: 2026, month: 2, day: 16)),
        (ChineseCalendar.ChineseDate(month: 1, day: 1), Date.from(year: 2026, month: 2, day: 17))

    ])
    func find_next(chineseDate: ChineseCalendar.ChineseDate, targetDate: Date) async throws {
        let testDate = Date.from(year: 2025, month: 1, day: 29, hour: 0, minute: 0, timezone: timeZone)!
        let chineseCalendar = ChineseCalendar(time: testDate, timezone: timeZone, location: location, globalMonth: true, apparentTime: false, largeHour: true)
        let chineseDateTime = ChineseCalendar.ChineseDateTime(date: chineseDate, time: .init())
        let start = chineseCalendar.findNext(chineseDateTime: chineseDateTime) ?? .distantPast
        let calendar = chineseCalendar.calendar
        #expect(calendar.isDate(start, equalTo: targetDate, toGranularity: .day))
    }

}
