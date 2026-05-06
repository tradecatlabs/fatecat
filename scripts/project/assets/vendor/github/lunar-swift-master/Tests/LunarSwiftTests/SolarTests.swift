import XCTest
@testable import LunarSwift

final class SolarTests: XCTestCase {
    func test1() throws {
        let solar = Solar.fromYmdHms(year: 2019, month: 5, day: 1)
        XCTAssertEqual(solar.fullString, "2019-05-01 00:00:00 星期三 (劳动节) 金牛座")
        XCTAssertEqual(solar.lunar.description, "二〇一九年三月廿七")
    }

    func test2() throws {
        XCTAssertEqual(Solar.fromYmdHms(year: 2020, month: 5, day: 24, hour: 13).lunar.description, "二〇二〇年闰四月初二")
    }

    func test3() throws {
        XCTAssertEqual(Solar.fromYmdHms(year: 11, month: 1, day: 1).lunar.description, "一〇年腊月初八")
    }

    func test4() throws {
        XCTAssertEqual(Solar.fromYmdHms(year: 11, month: 3, day: 1).lunar.description, "一一年二月初八")
    }

    func test5() throws {
        XCTAssertEqual(Solar.fromYmdHms(year: 26, month: 4, day: 13).lunar.description, "二六年三月初八")
    }

    func test6() throws {
        XCTAssertEqual(Solar.fromYmdHms(year: 2022, month: 3, day: 28).festivals[0], "全国中小学生安全教育日")
    }

    func test7() throws {
        XCTAssertEqual(Solar.fromYmdHms(year: 2022, month: 1, day: 31).next(days: 1).description, "2022-02-01")
    }

    func test8() throws {
        XCTAssertEqual(Solar.fromYmdHms(year: 2022, month: 1, day: 1).next(days: 365).description, "2023-01-01")
    }

    func test9() throws {
        XCTAssertEqual(Solar.fromYmdHms(year: 1582, month: 10, day: 4).next(days: 1).description, "1582-10-15")
    }

    func test10() throws {
        XCTAssertEqual(Solar.fromYmdHms(year: 1582, month: 10, day: 15).next(days: -1).description, "1582-10-04")
    }

    func test11() throws {
        XCTAssertEqual(Solar.fromYmdHms(year: 1582, month: 10, day: 15).next(days: -5).description, "1582-09-30")
    }

    func test12() throws {
        XCTAssertEqual(Solar.fromYmdHms(year: 1991, month: 5, day: 12).lunar.dayInGanZhi, "壬午")
    }
    
    func test13() throws {
        XCTAssertEqual(Solar.fromYmdHms(year: 2023, month: 8, day: 31).nextMonth(months: 1).description, "2023-09-30")
    }
    
    func test14() throws {
        XCTAssertEqual(Solar.fromYmdHms(year: 2023, month: 8, day: 31).nextMonth(months: 2).description, "2023-10-31")
    }
    
    func test15() throws {
        XCTAssertEqual(Solar.fromYmdHms(year: 2023, month: 8, day: 31).nextMonth(months: 6).description, "2024-02-29")
    }
    
    func test16() throws {
        XCTAssertEqual(Solar.fromYmdHms(year: 2023, month: 8, day: 31).nextYear(years: 2).description, "2025-08-31")
    }

}
