import XCTest
@testable import LunarSwift

final class ShuJiuTests: XCTestCase {
    func test1() throws {
        let shuJiu = Solar.fromYmdHms(year: 2021, month: 3, day: 5).lunar.shuJiu
        XCTAssertEqual(shuJiu!.description, "九九")
        XCTAssertEqual(shuJiu!.fullString, "九九第3天")
    }

}
