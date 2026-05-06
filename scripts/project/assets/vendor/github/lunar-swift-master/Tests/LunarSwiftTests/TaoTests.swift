import XCTest
@testable import LunarSwift

final class TaoTests: XCTestCase {
    func test1() throws {
        let tao = Tao.fromLunar(lunar: Lunar.fromYmdHms(lunarYear: 2021, lunarMonth: 10, lunarDay: 17, hour: 18))
        XCTAssertEqual(tao.description, "四七一八年十月十七")
        XCTAssertEqual(tao.fullString, "道歷四七一八年，天運辛丑年，己亥月，癸酉日。十月十七日，酉時。")
    }

}
