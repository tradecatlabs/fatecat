import XCTest
@testable import LunarSwift

final class EightCharTests: XCTestCase {
    func test1() throws {
        let solar = Solar.fromYmdHms(year: 2005, month: 12, day: 23, hour: 8, minute: 37)
        let lunar = solar.lunar
        let eightChar = lunar.eightChar
        XCTAssertEqual(eightChar.year, "乙酉")
        XCTAssertEqual(eightChar.month, "戊子")
        XCTAssertEqual(eightChar.day, "辛巳")
        XCTAssertEqual(eightChar.time, "壬辰")
    }

    func test2() throws {
        let solar = Solar.fromYmdHms(year: 1988, month: 2, day: 15, hour: 23, minute: 30)
        let lunar = solar.lunar
        let eightChar = lunar.eightChar
        XCTAssertEqual(eightChar.year, "戊辰")
        XCTAssertEqual(eightChar.month, "甲寅")
        XCTAssertEqual(eightChar.day, "庚子")
        XCTAssertEqual(eightChar.time, "戊子")

        eightChar.sect = 1
        XCTAssertEqual(eightChar.year, "戊辰")
        XCTAssertEqual(eightChar.month, "甲寅")
        XCTAssertEqual(eightChar.day, "辛丑")
        XCTAssertEqual(eightChar.time, "戊子")
    }
    
    func test3() throws {
        let solar = Solar.fromYmdHms(year: 2023, month: 1, day: 1, hour: 13, minute: 30)
        let lunar = solar.lunar
        let yun = lunar.eightChar.getYun(gender: 1, sect: 2)
        let startYear = yun.startYear
        let startMonth = yun.startMonth
        let startDay = yun.startDay
        let startTime = yun.startHour
        XCTAssertEqual("\(startYear)\(startMonth)\(startDay)\(startTime)", "151720")
        
        let timeShiShenZhi = lunar.eightChar.timeShiShenZhi.joined(separator: " ")
        XCTAssertEqual(timeShiShenZhi, "比肩 偏印 七杀")
    }
    
    func test4() throws {
        let solar = Solar.fromYmdHms(year: 1982, month: 1, day: 29, hour: 6)
        let lunar = solar.lunar
        let eightChar = lunar.eightChar
        XCTAssertEqual(eightChar.year, "辛酉")
        XCTAssertEqual(eightChar.month, "辛丑")
        XCTAssertEqual(eightChar.day, "壬子")
        XCTAssertEqual(eightChar.time, "癸卯")
    }
    
    func test5() throws {
        let solar = Solar.fromYmdHms(year: 1994, month: 12, day: 6, hour: 2)
        let lunar = solar.lunar
        let eightChar = lunar.eightChar
        XCTAssertEqual(eightChar.shenGong, "丁丑")
    }
    
    func test6() throws {
        let solars = Solar.fromBaZi(yearGanZhi: "甲辰", monthGanZhi: "丙寅", dayGanZhi: "己亥", timeGanZhi: "戊辰")
        var actual = [String]()
        for solar in solars {
            actual.append(solar.ymdhms)
        }
        
        var expected = [String]()
        expected.append("1904-03-06 07:00:00")
        expected.append("1964-02-20 08:00:00")
        expected.append("2024-02-05 08:00:00")
        XCTAssertEqual(actual, expected)
    }
    
    func test7() throws {
        let lunar = Lunar.fromYmdHms(lunarYear: 1981, lunarMonth: 9, lunarDay: 3, hour: 18)
        XCTAssertEqual(lunar.eightChar.yearShiShenZhi.joined(separator: " "), "比肩")
        XCTAssertEqual(lunar.eightChar.monthShiShenZhi.joined(separator: " "), "比肩")
        XCTAssertEqual(lunar.eightChar.dayShiShenZhi.joined(separator: " "), "伤官 正财")
        XCTAssertEqual(lunar.eightChar.timeShiShenZhi.joined(separator: " "), "比肩")
    }
    
    func test8() throws {
        let eightChar = Solar.fromYmdHms(year: 1989, month: 2, day: 5, hour: 22, minute: 30).lunar.eightChar
        let daYun = eightChar.getYun(gender: 1).getDaYun()
        XCTAssertEqual(daYun[1].startAge, 1)
        let liuNian = daYun[1].getLiuNian()
        XCTAssertEqual(liuNian[0].age, 1)
    }

}
