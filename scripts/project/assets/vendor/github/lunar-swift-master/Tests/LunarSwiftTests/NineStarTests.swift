@testable import LunarSwift
import XCTest

final class NineStarTests: XCTestCase {
    func test1() throws {
        let lunar = Solar.fromYmdHms(year: 1985, month: 2, day: 19).lunar
        XCTAssertEqual(lunar.yearNineStar.number, "六")
    }

    func test2() throws {
        let lunar = Solar.fromYmdHms(year: 2022, month: 1, day: 1).lunar
        XCTAssertEqual(lunar.yearNineStar.description, "六白金开阳")
    }

    func test3() throws {
        let lunar = Solar.fromYmdHms(year: 2033, month: 1, day: 1).lunar
        XCTAssertEqual(lunar.yearNineStar.description, "四绿木天权")
    }
}
