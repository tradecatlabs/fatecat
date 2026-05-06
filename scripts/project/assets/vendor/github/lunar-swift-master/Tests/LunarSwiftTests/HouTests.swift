import XCTest
@testable import LunarSwift

final class HouTests: XCTestCase {
    func test1() throws {
        let lunar = Solar.fromYmdHms(year: 2023, month: 3, day: 21).lunar
        XCTAssertEqual(lunar.hou.description, "春分 初候")
        XCTAssertEqual(lunar.wuHou.description, "玄鸟至")
    }
}
