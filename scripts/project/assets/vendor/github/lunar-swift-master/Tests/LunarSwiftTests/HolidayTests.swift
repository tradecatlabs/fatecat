import XCTest
@testable import LunarSwift

final class HolidayTests: XCTestCase {
    func test1() throws {
        let holiday = HolidayUtil.getHolidayByYmd(year: 2021, month: 6, day: 14)
        XCTAssertEqual(holiday!.description, "2021-06-14 端午节 2021-06-14")
    }

    func test2() throws {
        let holiday = HolidayUtil.getHolidayByYmd(year: 2016, month: 10, day: 4)
        XCTAssertEqual(holiday!.target, "2016-10-01")
    }
    
    func test3() throws {
        let holiday = HolidayUtil.getHolidayByYmd(year: 2024, month: 10, day: 4)
        XCTAssertEqual(holiday!.target, "2024-10-01")
    }
}
