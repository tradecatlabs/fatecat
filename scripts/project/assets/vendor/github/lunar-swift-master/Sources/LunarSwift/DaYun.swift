import Foundation

@objcMembers
public class DaYun: NSObject {
    private var _startYear: Int
    private var _endYear: Int
    private var _startAge: Int
    private var _endAge: Int
    private var _index: Int
    private var _yun: Yun
    private var _lunar: Lunar

    public var startYear: Int {
        get {
            _startYear
        }
    }

    public var endYear: Int {
        get {
            _endYear
        }
    }

    public var startAge: Int {
        get {
            _startAge
        }
    }

    public var endAge: Int {
        get {
            _endAge
        }
    }

    public var index: Int {
        get {
            _index
        }
    }

    public var yun: Yun {
        get {
            _yun
        }
    }

    public var lunar: Lunar {
        get {
            _lunar
        }
    }

    public init(yun: Yun, index: Int) {
        _yun = yun
        _lunar = yun.lunar
        _index = index
        let birthYear = _lunar.solar.year
        let year = _yun.startSolar.year
        if index < 1 {
            _startYear = birthYear
            _startAge = 1
            _endYear = year - 1
            _endAge = year - birthYear
        } else {
            let add = (index - 1) * 10
            _startYear = year + add
            _startAge = _startYear - birthYear + 1
            _endYear = _startYear + 9
            _endAge = _startAge + 9
        }
    }

    public var ganZhi: String {
        get {
            if _index < 1 {
                return ""
            }
            var offset = LunarUtil.getJiaZiIndex(ganZhi: _lunar.monthInGanZhiExact)
            offset += _yun.forward ? _index : -_index
            let size = LunarUtil.JIA_ZI.count
            if offset >= size {
                offset -= size
            }
            if offset < 0 {
                offset += size
            }
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

    public func getLiuNian(n: Int = 10) -> [LiuNian] {
        var l = [LiuNian]()
        var size = n
        if _index < 1 {
            size = _endYear - _startYear + 1
        }
        for i in (0..<size) {
            l.append(LiuNian(daYun: self, index: i))
        }
        return l
    }

    public func getXiaoYun(n: Int = 10) -> [XiaoYun] {
        var l = [XiaoYun]()
        var size = n
        if _index < 1 {
            size = _endYear - _startYear + 1
        }
        for i in (0..<size) {
            l.append(XiaoYun(daYun: self, index: i, forward: _yun.forward))
        }
        return l
    }

}
