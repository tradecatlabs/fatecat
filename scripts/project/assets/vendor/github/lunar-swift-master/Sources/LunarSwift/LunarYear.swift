import Foundation

@objcMembers
public class LunarYear: NSObject {
    public static var YUAN: [String] = ["下", "上", "中"]
    public static var YUN: [String] = ["七", "八", "九", "一", "二", "三", "四", "五", "六"]
    private static var LEAP_11: [Int] = [75, 94, 170, 265, 322, 398, 469, 553, 583, 610, 678, 735, 754, 773, 849, 887, 936, 1050, 1069, 1126, 1145, 1164, 1183, 1259, 1278, 1308, 1373, 1403, 1441, 1460, 1498, 1555, 1593, 1612, 1631, 1642, 2033, 2128, 2147, 2242, 2614, 2728, 2910, 3062, 3244, 3339, 3616, 3711, 3730, 3825, 4007, 4159, 4197, 4322, 4341, 4379, 4417, 4531, 4599, 4694, 4713, 4789, 4808, 4971, 5085, 5104, 5161, 5180, 5199, 5294, 5305, 5476, 5677, 5696, 5772, 5791, 5848, 5886, 6049, 6068, 6144, 6163, 6258, 6402, 6440, 6497, 6516, 6630, 6641, 6660, 6679, 6736, 6774, 6850, 6869, 6899, 6918, 6994, 7013, 7032, 7051, 7070, 7089, 7108, 7127, 7146, 7222, 7271, 7290, 7309, 7366, 7385, 7404, 7442, 7461, 7480, 7491, 7499, 7594, 7624, 7643, 7662, 7681, 7719, 7738, 7814, 7863, 7882, 7901, 7939, 7958, 7977, 7996, 8034, 8053, 8072, 8091, 8121, 8159, 8186, 8216, 8235, 8254, 8273, 8311, 8330, 8341, 8349, 8368, 8444, 8463, 8474, 8493, 8531, 8569, 8588, 8626, 8664, 8683, 8694, 8702, 8713, 8721, 8751, 8789, 8808, 8816, 8827, 8846, 8884, 8903, 8922, 8941, 8971, 9036, 9066, 9085, 9104, 9123, 9142, 9161, 9180, 9199, 9218, 9256, 9294, 9313, 9324, 9343, 9362, 9381, 9419, 9438, 9476, 9514, 9533, 9544, 9552, 9563, 9571, 9582, 9601, 9639, 9658, 9666, 9677, 9696, 9734, 9753, 9772, 9791, 9802, 9821, 9886, 9897, 9916, 9935, 9954, 9973, 9992]
    private static var LEAP_12: [Int] = [37, 56, 113, 132, 151, 189, 208, 227, 246, 284, 303, 341, 360, 379, 417, 436, 458, 477, 496, 515, 534, 572, 591, 629, 648, 667, 697, 716, 792, 811, 830, 868, 906, 925, 944, 963, 982, 1001, 1020, 1039, 1058, 1088, 1153, 1202, 1221, 1240, 1297, 1335, 1392, 1411, 1422, 1430, 1517, 1525, 1536, 1574, 3358, 3472, 3806, 3988, 4751, 4941, 5066, 5123, 5275, 5343, 5438, 5457, 5495, 5533, 5552, 5715, 5810, 5829, 5905, 5924, 6421, 6535, 6793, 6812, 6888, 6907, 7002, 7184, 7260, 7279, 7374, 7556, 7746, 7757, 7776, 7833, 7852, 7871, 7966, 8015, 8110, 8129, 8148, 8224, 8243, 8338, 8406, 8425, 8482, 8501, 8520, 8558, 8596, 8607, 8615, 8645, 8740, 8778, 8835, 8865, 8930, 8960, 8979, 8998, 9017, 9055, 9074, 9093, 9112, 9150, 9188, 9237, 9275, 9332, 9351, 9370, 9408, 9427, 9446, 9457, 9465, 9495, 9560, 9590, 9628, 9647, 9685, 9715, 9742, 9780, 9810, 9818, 9829, 9848, 9867, 9905, 9924, 9943, 9962, 10000]
    private static var YMC: [Int] = [11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    private static var CACHE_YEAR: LunarYear?

    private var _year: Int
    private var _ganIndex: Int
    private var _zhiIndex: Int
    private var _months: [LunarMonth]
    private var _jieQiJulianDays: [Double]

    public var year: Int {
        _year
    }

    public var ganIndex: Int {
        _ganIndex
    }

    public var zhiIndex: Int {
        _zhiIndex
    }

    public var months: [LunarMonth] {
        _months
    }

    public var monthsInYear: [LunarMonth] {
        var l: [LunarMonth] = []
        for m in _months {
            if m.year == _year {
                l.append(m)
            }
        }
        return l
    }

    public var dayCount: Int {
        var n = 0
        for m in _months {
            if m.year == _year {
                n += m.dayCount
            }
        }
        return n
    }
    
    public var leapMonth: Int {
        for m in _months {
            if m.year == _year && m.leap {
                return abs(m.month)
            }
        }
        return 0
    }

    public var jieQiJulianDays: [Double] {
        _jieQiJulianDays
    }

    public var gan: String {
        LunarUtil.GAN[_ganIndex + 1]
    }

    public var zhi: String {
        LunarUtil.ZHI[_zhiIndex + 1]
    }

    public var ganZhi: String {
        "\(gan)\(zhi)"
    }
    
    public var yuan: String {
        "\(LunarYear.YUAN[((_year + 2696) / 60) % 3])元"
    }
    
    public var yun: String {
        "\(LunarYear.YUN[((year + 2696) / 20) % 9])运"
    }
    
    public var positionXi: String {
        "\(LunarUtil.POSITION_XI[_ganIndex + 1])"
    }
    
    public var positionXiDesc: String {
        LunarUtil.POSITION_DESC[positionXi]!
    }
    
    public var positionYangGui: String {
        "\(LunarUtil.POSITION_YANG_GUI[_ganIndex + 1])"
    }
    
    public var positionYangGuiDesc: String {
        LunarUtil.POSITION_DESC[positionYangGui]!
    }
    
    public var positionYinGui: String {
        "\(LunarUtil.POSITION_YIN_GUI[_ganIndex + 1])"
    }
    
    public var positionYinGuiDesc: String {
        LunarUtil.POSITION_DESC[positionYinGui]!
    }
    
    public var positionCai: String {
        "\(LunarUtil.POSITION_CAI[_ganIndex + 1])"
    }
    
    public var positionCaiDesc: String {
        LunarUtil.POSITION_DESC[positionCai]!
    }
    
    public func getPositionFu(sect: Int) -> String {
        let index = _ganIndex + 1
        if 1 == sect {
            return LunarUtil.POSITION_FU[index]
        }
        return LunarUtil.POSITION_FU_2[index]
    }
    
    public func getPositionFuDesc(sect: Int) -> String {
        LunarUtil.POSITION_DESC[getPositionFu(sect: sect)]!
    }
    
    public var positionFu: String {
        getPositionFu(sect: 2)
    }
    
    public var positionFuDesc: String {
        getPositionFuDesc(sect: 2)
    }
    
    public var positionTaiSui: String {
        "\(LunarUtil.POSITION_TAI_SUI_YEAR[_zhiIndex])"
    }
    
    public var positionTaiSuiDesc: String {
        LunarUtil.POSITION_DESC[positionTaiSui]!
    }

    public init(lunarYear: Int) {
        _year = lunarYear
        _months = [LunarMonth]()
        let offset = lunarYear - 4
        var yearGanIndex = offset % 10
        var yearZhiIndex = offset % 12
        if yearGanIndex < 0 {
            yearGanIndex += 10
        }
        if yearZhiIndex < 0 {
            yearZhiIndex += 12
        }
        _ganIndex = yearGanIndex
        _zhiIndex = yearZhiIndex
        // 节气
        var jq = [Double]()
        // 合朔，即每月初一
        var hs = [Double]()
        // 每月天数，长度15
        var dayCounts = [Int]()
        var months = [Int]()

        let currentYear = _year
        
        var jd: Double = floor((Double(currentYear) - Double(2000)) * Double(365.2422) + Double(180))
        // 355是2000.12冬至，得到较靠近jd的冬至估计值
        var w: Double = floor((jd - Double(355) + Double(183)) / Double(365.2422)) * Double(365.2422) + Double(355)
        if ShouXingUtil.calcQi(pjd: w) > jd {
            w -= Double(365.2422)
        }
        // 25个节气时刻(北京时间)，从冬至开始到下一个冬至以后
        for i in 0 ..< 26 {
            jq.append(ShouXingUtil.calcQi(pjd: w + Double(15.2184) * Double(i)))
        }
        _jieQiJulianDays = [Double]()
        // 从上年的大雪到下年的立春
        for i in 0 ..< Lunar.JIE_QI_IN_USE.count {
            if i == 0 {
                jd = ShouXingUtil.qiAccurate2(jd: jq[0] - Double(15.2184))
            } else if i <= 26 {
                jd = ShouXingUtil.qiAccurate2(jd: jq[i - 1])
            } else {
                jd = ShouXingUtil.qiAccurate2(jd: jq[25] + Double(15.2184) * Double(i - 26))
            }
            _jieQiJulianDays.append(jd + Solar.J2000)
        }

            // 冬至前的初一，今年"首朔"的日月黄经差w
        w = ShouXingUtil.calcShuo(pjd: jq[0])
        if w > jq[0] {
            w -= Double(29.53)
        }
            // 递推每月初一
        for i in 0 ..< 16 {
            hs.append(ShouXingUtil.calcShuo(pjd: w + Double(29.5306) * Double(i)))
        }
        // 每月
        for i in 0 ..< 15 {
            dayCounts.append(Int(hs[i + 1] - hs[i]))
            months.append(i)
        }

        let prevYear: Int = currentYear - 1
        var leapIndex: Int = 16
        if LunarYear.LEAP_11.contains(currentYear) {
            leapIndex = 13
        } else if LunarYear.LEAP_12.contains(currentYear) {
            leapIndex = 14
        } else if hs[13] <= jq[24] {
            var i = 1
            while hs[i + 1] > jq[2 * i] && i < 13 {
                i += 1
            }
            leapIndex = i
        }
        if leapIndex < 15 {
            for i in leapIndex ..< 15 {
                months[i] -= 1
            }
        }

        var fm: Int = -1
        var index: Int = -1
        var y: Int = prevYear
        for i in 0 ..< 15 {
            let dm: Double = hs[i] + Solar.J2000
            let v2: Int = months[i]
            var mc: Int = LunarYear.YMC[v2 % 12]
            if 1724360 <= dm && dm < 1729794 {
                mc = LunarYear.YMC[(v2 + 1) % 12]
            } else if 1807724 <= dm && dm < 1808699 {
                mc = LunarYear.YMC[(v2 + 1) % 12]
            } else if dm == 1729794 || dm == 1808699 {
                mc = 12
            }
            if fm == -1 {
                fm = mc
                index = mc
            }
            if mc < fm {
                y += 1
                index = 1
            }
            fm = mc
            if i == leapIndex {
                mc = -mc
            } else if dm == 1729794 || dm == 1808699 {
                mc = -11
            }
            _months.append(LunarMonth(lunarYear: y, lunarMonth: mc, dayCount: dayCounts[i], firstJulianDay: hs[i] + Solar.J2000, index: index))
            index += 1
        }
    }

    public class func fromYear(lunarYear: Int) -> LunarYear {
        var y: LunarYear
        if nil == CACHE_YEAR || CACHE_YEAR!.year != lunarYear {
            y = LunarYear(lunarYear: lunarYear)
            CACHE_YEAR = y
        } else {
            y = CACHE_YEAR!
        }
        return y
    }

    public func getMonth(lunarMonth: Int) -> LunarMonth? {
        for m in _months {
            if m.year == _year && m.month == lunarMonth {
                return m
            }
        }
        return nil
    }

    public var nineStar: NineStar {
        let index = LunarUtil.getJiaZiIndex(ganZhi: ganZhi) + 1
        let yuan = ((_year + 2696) / 60) % 3
        var offset = (62 + yuan * 3 - index) % 9
        if 0 == offset {
            offset = 9
        }
        return NineStar(index: offset - 1)
    }

    override public var description: String {
        "\(_year)"
    }

    public var fullString: String {
        "\(year)年"
    }
}
