import XCTest
@testable import LunarSwift

final class LiuYaoTests: XCTestCase {
    func test1() throws {
        XCTAssertEqual(Solar.fromYmdHms(year: 2020, month: 12, day: 11).lunar.liuYao, "赤口")
    }

}
