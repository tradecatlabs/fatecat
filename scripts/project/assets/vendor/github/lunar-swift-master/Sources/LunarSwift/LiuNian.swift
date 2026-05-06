import Foundation

@objcMembers
public class LiuNian: NSObject {
    private var _year: Int
    private var _age: Int
    private var _index: Int
    private var _daYun: DaYun
    private var _lunar: Lunar

    public var year: Int {
        get {
            _year
        }
    }
    public var age: Int {
        get {
            _age
        }
    }

    public var index: Int {
        get {
            _index
        }
    }

    public var daYun: DaYun {
        get {
            _daYun
        }
    }

    public var lunar: Lunar {
        get {
            _lunar
        }
    }

    public init(daYun: DaYun, index: Int) {
        _daYun = daYun
        _lunar = _daYun.lunar
        _index = index
        _year = _daYun.startYear + index
        _age = _daYun.startAge + index
    }

    public var ganZhi: String {
        get {
            var offset = LunarUtil.getJiaZiIndex(ganZhi: _lunar.jieQiTable["立春"]!.lunar.yearInGanZhiExact) + _index
            if _daYun.index > 0 {
                offset += _daYun.startAge - 1
            }
            offset %= LunarUtil.JIA_ZI.count
            return LunarUtil.JIA_ZI[offset]
        }
    }

    public var xun: String {
        get {
            LunarUtil.getXun(ganZhi: ganZhi)
        }
    }

    public var xunKong: String {
        get {
            LunarUtil.getXunKong(ganZhi: ganZhi)
        }
    }

    public func getLiuYue() -> [LiuYue] {
        var l = [LiuYue]()
        for i in (0..<12) {
            l.append(LiuYue(liuNian: self, index: i))
        }
        return l
    }

}
