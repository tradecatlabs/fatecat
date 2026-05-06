import XCTest
@testable import LunarSwift

final class FestivalTests: XCTestCase {
    func test1() throws {
        let solar = Solar.fromYmdHms(year: 2020, month: 11, day: 26)
        XCTAssertEqual(solar.festivals, ["感恩节"])
    }

    func test2() throws {
        let solar = Solar.fromYmdHms(year: 2020, month: 6, day: 21)
        XCTAssertEqual(solar.festivals, ["父亲节"])
    }

}
