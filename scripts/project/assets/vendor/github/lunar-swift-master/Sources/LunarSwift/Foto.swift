import Foundation

@objcMembers
public class Foto: NSObject {
    public static var DEAD_YEAR: Int = -543

    private var _lunar: Lunar

    public var lunar: Lunar {
        get {
            _lunar
        }
    }

    public init(lunar: Lunar) {
        _lunar = lunar
    }

    public class func fromLunar(lunar: Lunar) -> Foto {
        Foto(lunar: lunar)
    }

    public class func fromYmdHms(year: Int, month: Int, day: Int, hour: Int = 0, minute: Int = 0, second: Int = 0) -> Foto {
        Foto(lunar: Lunar.fromYmdHms(lunarYear: year + DEAD_YEAR - 1, lunarMonth: month, lunarDay: day, hour: hour, minute: minute, second: second))
    }

    public var year: Int {
        get {
            let sy = _lunar.solar.year
            var y = sy - Foto.DEAD_YEAR
            if sy == _lunar.year {
                y += 1
            }
            return y
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

    public var festivals: [FotoFestival] {
        get {
            var l = [FotoFestival]()
            let f = FotoUtil.FESTIVAL["\(abs(month))-\(day)"]
            if nil != f {
                for o in f! {
                    var result = ""
                    var everyMonth = false
                    var remark = ""
                    let size = o.count
                    if size > 1 {
                        result = o[1]
                    }
                    if size > 2 && "true" == o[2] {
                        everyMonth = true
                    }
                    if size > 3 {
                        remark = o[3]
                    }
                    l.append(FotoFestival(name: o[0], result: result, everyMonth: everyMonth, remark: remark))
                }
            }
            return l
        }
    }
    
    public var otherFestivals: [String] {
        get {
            var l = [String]()
            //获取几月几日对应的节日
            let fs = FotoUtil.OTHER_FESTIVAL["\(month)-\(day)"]
            if nil != fs {
                for f in fs! {
                    l.append(f)
                }
            }
            return l
        }
    }

    public var monthZhai: Bool {
        get {
            1 == month || 5 == month || 9 == month
        }
    }

    public var dayYangGong: Bool {
        get {
            for o in festivals {
                if "杨公忌" == o.name {
                    return true
                }
            }
            return false
        }
    }

    public var dayZhaiShuoWang: Bool {
        get {
            1 == day || 15 == day
        }
    }

    public var dayZhaiSix: Bool {
        get {
            if 8 == day || 14 == day || 15 == day || 23 == day || 29 == day || 30 == day {
                return true
            } else if 28 == day {
                let m = LunarMonth.fromYm(lunarYear: _lunar.year, lunarMonth: _lunar.month)
                return nil != m && 30 != m!.dayCount
            }
            return false
        }
    }

    public var dayZhaiTen: Bool {
        get {
            1 == day || 8 == day || 14 == day || 15 == day || 18 == day || 23 == day || 24 == day || 28 == day || 29 == day || 30 == day
        }
    }

    public var dayZhaiGuanYin: Bool {
        get {
            let k = "\(month)-\(day)"
            for v in FotoUtil.DAY_ZHAI_GUAN_YIN {
                if k == v {
                    return true
                }
            }
            return false
        }
    }

    public var xiu: String {
        get {
            FotoUtil.getXiu(month: month, day: day)
        }
    }

    public var xiuLuck: String {
        get {
            LunarUtil.XIU_LUCK[xiu]!
        }
    }

    public var xiuSong: String {
        get {
            LunarUtil.XIU_SONG[xiu]!
        }
    }

    public var zheng: String {
        get {
            LunarUtil.ZHENG[xiu]!
        }
    }

    public var animal: String {
        get {
            LunarUtil.ANIMAL[xiu]!
        }
    }

    public var gong: String {
        get {
            LunarUtil.GONG[xiu]!
        }
    }

    public var shou: String {
        get {
            LunarUtil.SHOU[gong]!
        }
    }

    public override var description: String {
        get {
            "\(yearInChinese)年\(monthInChinese)月\(dayInChinese)"
        }
    }

    public var fullString: String {
        get {
            var s = description
            for f in festivals {
                s += " (\(f.description))"
            }
            return s
        }
    }

}
