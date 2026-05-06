import XCTest
@testable import LunarSwift

final class FuTests: XCTestCase {
    func test1() throws {
        let fu = Solar.fromYmdHms(year: 2011, month: 7, day: 14).lunar.fu
        XCTAssertEqual(fu!.description, "初伏")
        XCTAssertEqual(fu!.fullString, "初伏第1天")
    }

}
