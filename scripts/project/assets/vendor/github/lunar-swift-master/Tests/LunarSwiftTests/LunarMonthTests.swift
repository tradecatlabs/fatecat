import XCTest
@testable import LunarSwift

final class LunarMonthTests: XCTestCase {
    func test1() throws {
        let month = LunarMonth.fromYm(lunarYear: 2023, lunarMonth: 1)!
        XCTAssertEqual(month.index, 1)
        XCTAssertEqual(month.ganZhi, "甲寅")
    }
    
    func test2() throws {
        let month = LunarMonth.fromYm(lunarYear: 2023, lunarMonth: -2)!
        XCTAssertEqual(month.index, 3)
        XCTAssertEqual(month.ganZhi, "乙卯")
    }
    
    func test3() throws {
        let month = LunarMonth.fromYm(lunarYear: 2023, lunarMonth: 12)!
        XCTAssertEqual(month.index, 13)
        XCTAssertEqual(month.ganZhi, "乙丑")
    }

}
