import Foundation

@objcMembers
public class Tao: NSObject {
    public static var BIRTH_YEAR: Int = -2697

    private var _lunar: Lunar

    public var lunar: Lunar {
        get {
            _lunar
        }
    }

    public init(lunar: Lunar) {
        _lunar = lunar
    }

    public class func fromLunar(lunar: Lunar) -> Tao {
        Tao(lunar: lunar)
    }

    public class func fromYmdHms(year: Int, month: Int, day: Int, hour: Int = 0, minute: Int = 0, second: Int = 0) -> Tao {
        Tao(lunar: Lunar.fromYmdHms(lunarYear: year + BIRTH_YEAR, lunarMonth: month, lunarDay: day, hour: hour, minute: minute, second: second))
    }

    public var year: Int {
        get {
            _lunar.year - Tao.BIRTH_YEAR
        }
    }

    public var month: Int {
        get {
            _lunar.month
        }
    }

    public var day: Int {
        get {
            _lunar.day
        }
    }

    public var yearInChinese: String {
        get {
            let y = "\(year)"
            var s = ""
            for i in (0..<y.count) {
                s += LunarUtil.NUMBER[Int(y[y.index(y.startIndex, offsetBy: i)].asciiValue!) - 48]
            }
            return s
        }
    }

    public var monthInChinese: String {
        get {
            _lunar.monthInChinese
        }
    }

    public var dayInChinese: String {
        get {
            _lunar.dayInChinese
        }
    }

    public var festivals: [TaoFestival] {
        get {
            var l = [TaoFestival]()
            let f = TaoUtil.FESTIVAL["\(month)-\(day)"]
            if nil != f {
                for o in f! {
                    var remark = ""
                    if o.count > 1 {
                        remark = o[1]
                    }
                    l.append(TaoFestival(name: o[0], remark: remark))
                }
            }
            let jq = _lunar.jieQi
            if "冬至" == jq {
                l.append(TaoFestival(name: "元始天尊圣诞"))
            } else if "夏至" == jq {
                l.append(TaoFestival(name: "灵宝天尊圣诞"))
            }
            var name = TaoUtil.BA_JIE[jq]
            if nil != name {
                l.append(TaoFestival(name: name!))
            }
            name = TaoUtil.BA_HUI[_lunar.dayInGanZhi]
            if nil != name {
                l.append(TaoFestival(name: name!))
            }
            return l
        }
    }

    private func isDayIn(days: [String]) -> Bool {
        days.contains("\(month)-\(day)")
    }

    public var daySanHui: Bool {
        get {
            isDayIn(days: TaoUtil.SAN_HUI)
        }
    }

    public var daySanYuan: Bool {
        get {
            isDayIn(days: TaoUtil.SAN_YUAN)
        }
    }

    public var dayWuLa: Bool {
        get {
            isDayIn(days: TaoUtil.WU_LA)
        }
    }

    public var dayBaJie: Bool {
        get {
            nil != TaoUtil.BA_JIE[_lunar.jieQi]
        }
    }

    public var dayBaHui: Bool {
        get {
            nil != TaoUtil.BA_HUI[_lunar.dayInGanZhi]
        }
    }

    public var dayMingWu: Bool {
        get {
            "戊" == _lunar.dayGan
        }
    }

    public var dayAnWu: Bool {
        get {
            TaoUtil.AN_WU[abs(month) - 1] == _lunar.dayZhi
        }
    }

    public var dayWu: Bool {
        get {
            dayMingWu || dayAnWu
        }
    }

    public var dayTianShe: Bool {
        get {
            let mz = _lunar.monthZhi
            let dgz = _lunar.dayInGanZhi
            if "寅卯辰".contains(mz) {
                if "戊寅" == dgz {
                    return true
                }
            } else if "巳午未".contains(mz) {
                if "甲午" == dgz {
                    return true
                }
            } else if "申酉戌".contains(mz) {
                if "戊申" == dgz {
                    return true
                }
            } else if "亥子丑".contains(mz) {
                if "甲子" == dgz {
                    return true
                }
            }
            return false
        }
    }

    public override var description: String {
        get {
            "\(yearInChinese)年\(monthInChinese)月\(dayInChinese)"
        }
    }

    public var fullString: String {
        get {
            "道歷\(yearInChinese)年，天運\(_lunar.yearInGanZhi)年，\(_lunar.monthInGanZhi)月，\(_lunar.dayInGanZhi)日。\(monthInChinese)月\(dayInChinese)日，\(_lunar.timeZhi)時。"
        }
    }

}
