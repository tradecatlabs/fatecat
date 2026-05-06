import XCTest
@testable import LunarSwift

final class FotoTests: XCTestCase {
    func test1() throws {
        let foto = Foto.fromLunar(lunar: Lunar.fromYmdHms(lunarYear: 2021, lunarMonth: 10, lunarDay: 14))
        XCTAssertEqual(foto.fullString, "二五六五年十月十四 (三元降) (四天王巡行)")
    }
    
    func test2() throws {
        let foto = Foto.fromLunar(lunar: Lunar.fromYmdHms(lunarYear: 2021, lunarMonth: 3, lunarDay: 16))
        XCTAssertEqual(foto.otherFestivals[0], "准提菩萨圣诞")
    }

}
