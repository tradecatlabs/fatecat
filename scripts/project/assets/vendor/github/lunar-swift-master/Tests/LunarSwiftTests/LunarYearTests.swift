import XCTest
@testable import LunarSwift

final class LunarYearTests: XCTestCase {
    func test1() throws {
        XCTAssertEqual(LunarYear(lunarYear: 2023).dayCount, 384)
    }

}
