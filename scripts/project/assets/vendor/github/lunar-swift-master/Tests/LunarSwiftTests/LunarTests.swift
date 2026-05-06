import XCTest
@testable import LunarSwift

final class LunarTests: XCTestCase {
    func test1() throws {
        let lunar = Lunar.fromYmdHms(lunarYear: 2019, lunarMonth: 3, lunarDay: 27)
        XCTAssertEqual(lunar.description, "二〇一九年三月廿七")
        XCTAssertEqual(lunar.solar.fullString, "2019-05-01 00:00:00 星期三 (劳动节) 金牛座")
    }

    func test2() throws {
        XCTAssertEqual(Solar.fromYmdHms(year: 1, month: 1, day: 1, hour: 12).lunar.description, "〇年冬月十八")
    }

    func test3() throws {
        XCTAssertEqual(Solar.fromYmdHms(year: 9999, month: 12, day: 31, hour: 12).lunar.description, "九九九九年腊月初二")
    }

    func test4() throws {
        XCTAssertEqual(Lunar.fromYmdHms(lunarYear: 1905, lunarMonth: 1, lunarDay: 1, hour: 12).solar.description, "1905-02-04")
    }

    func test5() throws {
        XCTAssertEqual(Lunar.fromYmdHms(lunarYear: 2038, lunarMonth: 12, lunarDay: 29, hour: 12).solar.description, "2039-01-23")
    }

    func test6() throws {
        let lunar = Lunar.fromYmdHms(lunarYear: 2020, lunarMonth: -4, lunarDay: 2, hour: 13)
        XCTAssertEqual(lunar.description, "二〇二〇年闰四月初二")
        XCTAssertEqual(lunar.solar.description, "2020-05-24")
    }

    func test7() throws {
        let lunar = Lunar.fromYmdHms(lunarYear: 2020, lunarMonth: 12, lunarDay: 10, hour: 13)
        XCTAssertEqual(lunar.description, "二〇二〇年腊月初十")
        XCTAssertEqual(lunar.solar.description, "2021-01-22")
    }

    func test8() throws {
        XCTAssertEqual(Lunar.fromYmdHms(lunarYear: 1500, lunarMonth: 1, lunarDay: 1, hour: 12).solar.description, "1500-01-31")
    }

    func test9() throws {
        XCTAssertEqual(Lunar.fromYmdHms(lunarYear: 1500, lunarMonth: 12, lunarDay: 29, hour: 12).solar.description, "1501-01-18")
    }

    func test10() throws {
        XCTAssertEqual(Solar.fromYmdHms(year: 1582, month: 10, day: 4, hour: 12).lunar.description, "一五八二年九月十八")
    }

    func test11() throws {
        XCTAssertEqual(Solar.fromYmdHms(year: 1582, month: 10, day: 15, hour: 12).lunar.description, "一五八二年九月十九")
    }

    func test12() throws {
        XCTAssertEqual(Lunar.fromYmdHms(lunarYear: 2021, lunarMonth: 12, lunarDay: 29).festivals[0], "除夕")
    }

    func test13() throws {
        XCTAssertEqual(Lunar.fromYmdHms(lunarYear: 2020, lunarMonth: 12, lunarDay: 30).festivals[0], "除夕")
    }

    func test14() throws {
        XCTAssertEqual(Solar.fromYmdHms(year: 2022, month: 1, day: 31).lunar.festivals[0], "除夕")
    }

    func test15() throws {
        XCTAssertEqual(Lunar.fromYmdHms(lunarYear: 2033, lunarMonth: -11, lunarDay: 1).solar.description, "2033-12-22")
    }

    func test16() throws {
        XCTAssertEqual(Solar.fromYmdHms(year: 1990, month: 10, day: 8).lunar.monthInGanZhiExact, "乙酉")
    }

    func test17() throws {
        XCTAssertEqual(Solar.fromYmdHms(year: 1990, month: 10, day: 9).lunar.monthInGanZhiExact, "丙戌")
    }

    func test18() throws {
        XCTAssertEqual(Solar.fromYmdHms(year: 1990, month: 10, day: 8).lunar.monthInGanZhi, "丙戌")
    }

    func test19() throws {
        XCTAssertEqual(Lunar.fromYmdHms(lunarYear: 37, lunarMonth: -12, lunarDay: 1).monthInChinese, "闰腊")
    }

    func test20() throws {
        XCTAssertEqual(Solar.fromYmdHms(year: 5553, month: 1, day: 22).lunar.description, "五五五二年闰腊月初二")
    }

    func test21() throws {
        XCTAssertEqual(Solar.fromYmdHms(year: 7013, month: 12, day: 24).lunar.description, "七〇一三年闰冬月初四")
    }

    func test22() throws {
        XCTAssertEqual(Solar.fromYmdHms(year: 4, month: 2, day: 10).lunar.yearShengXiao, "鼠")
    }

    func test23() throws {
        XCTAssertEqual(Solar.fromYmdHms(year: 4, month: 2, day: 9).lunar.yearShengXiao, "猪")
    }

    func test24() throws {
        XCTAssertEqual(Lunar.fromYmdHms(lunarYear: 1518, lunarMonth: 1, lunarDay: 1).solar.ymd, "1518-02-10")
    }

    func test25() throws {
        XCTAssertEqual(Lunar.fromYmdHms(lunarYear: 793, lunarMonth: 1, lunarDay: 1).solar.ymd, "0793-02-15")
    }

    func test26() throws {
        XCTAssertEqual(Lunar.fromYmdHms(lunarYear: 2025, lunarMonth: -6, lunarDay: 1).solar.ymd, "2025-07-25")
    }

    func test27() throws {
        XCTAssertEqual(Lunar.fromYmdHms(lunarYear: 2025, lunarMonth: 6, lunarDay: 1).solar.ymd, "2025-06-25")
    }

    func test28() throws {
        XCTAssertEqual(Lunar.fromYmdHms(lunarYear: 41, lunarMonth: 1, lunarDay: 1).solar.ymd, "0041-02-20")
    }

    func test29() throws {
        XCTAssertEqual(Lunar.fromYmdHms(lunarYear: 1537, lunarMonth: 1, lunarDay: 1).solar.ymd, "1537-02-10")
    }

    func test30() throws {
        XCTAssertEqual(Solar.fromYmdHms(year: 2021, month: 11, day: 27).lunar.dayYi, ["嫁娶", "祭祀", "祈福", "求嗣", "开光", "出行", "解除", "出火", "拆卸", "进人口", "入宅", "移徙", "安床", "栽种", "动土", "修造", "纳畜", "入殓", "安葬", "立碑", "除服", "成服"])
    }

    func test31() throws {
        XCTAssertEqual(Solar.fromYmdHms(year: 2023, month: 3, day: 17).lunar.dayJiShen, ["月德", "天愿", "六合", "金堂"])
    }

    func test32() throws {
        XCTAssertEqual(Solar.fromYmdHms(year: 2023, month: 3, day: 17).lunar.dayXiongSha, ["月煞", "月虚", "四击", "天牢"])
    }
    
    func test33() throws {
        XCTAssertEqual(Solar.fromYmdHms(year: 2023, month: 10, day: 14).lunar.dayJiShen, ["阴德", "续世", "明堂"])
        XCTAssertEqual(Solar.fromYmdHms(year: 2023, month: 10, day: 14).lunar.dayXiongSha, ["游祸", "天贼", "血忌", "重日"])
        
        XCTAssertEqual(Solar.fromYmdHms(year: 2023, month: 11, day: 11).lunar.dayJiShen, ["母仓", "时阳", "生气", "圣心", "除神", "鸣吠"])
        
        XCTAssertEqual(Solar.fromYmdHms(year: 2024, month: 2, day: 10).lunar.dayJiShen, ["守日", "天巫", "福德", "六仪", "金堂", "金匮"])
        XCTAssertEqual(Solar.fromYmdHms(year: 2024, month: 2, day: 10).lunar.dayXiongSha, ["厌对", "招摇", "九空", "九坎", "九焦", "复日"])
    }
    
    func test34() throws {
        XCTAssertEqual(Solar.fromYmdHms(year: 2023, month: 11, day: 14).lunar.dayJiShen, ["官日", "天马", "吉期", "要安", "鸣吠对"])
        XCTAssertEqual(Solar.fromYmdHms(year: 2023, month: 11, day: 14).lunar.dayXiongSha, ["大时", "大败", "咸池", "触水龙", "白虎"])
    }
    
    func test36() throws {
        XCTAssertEqual(Solar.fromYmdHms(year: 2023, month: 11, day: 14).lunar.dayJiShen, ["官日", "天马", "吉期", "要安", "鸣吠对"])
        XCTAssertEqual(Solar.fromYmdHms(year: 2023, month: 11, day: 14).lunar.dayXiongSha, ["大时", "大败", "咸池", "触水龙", "白虎"])
    }
    
    func test35() throws {
        XCTAssertEqual(Solar.fromYmdHms(year: 2022, month: 4, day: 5).lunar.dayJi, ["出火", "入宅", "安葬", "伐木"])
    }
    
    func test37() throws {
        XCTAssertEqual(Solar.fromYmdHms(year: 2021, month: 11, day: 27).lunar.dayYi, ["嫁娶", "祭祀", "祈福", "求嗣", "开光", "出行", "解除", "出火", "拆卸", "进人口", "入宅", "移徙", "安床", "栽种", "动土", "修造", "纳畜", "入殓", "安葬", "立碑", "除服", "成服"])
    }
    
    func test38() throws {
        XCTAssertEqual(Solar.fromYmdHms(year: 2025, month: 2, day: 7).lunar.dayYi, ["嫁娶", "祭祀", "祈福", "出行", "解除", "出火", "拆卸", "动土", "入宅", "移徙", "安床", "上梁", "栽种", "纳畜", "破土", "启钻", "安葬"])
        XCTAssertEqual(Solar.fromYmdHms(year: 2025, month: 2, day: 7).lunar.dayJi, ["开市", "立券", "理发", "作灶"])
    }

}
