import Foundation

@objcMembers
public class XiaoYun: NSObject {
    private var _year: Int
    private var _age: Int
    private var _index: Int
    private var _forward: Bool = false
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

    public var forward: Bool {
        get {
            _forward
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

    public init(daYun: DaYun, index: Int, forward: Bool) {
        _daYun = daYun
        _lunar = _daYun.lunar
        _index = index
        _year = _daYun.startYear + index
        _age = _daYun.startAge + index
        _forward = forward
    }

    public var ganZhi: String {
        get {
            var offset = LunarUtil.getJiaZiIndex(ganZhi: _lunar.timeInGanZhi)
            var add = _index + 1
            if _daYun.index > 0 {
                add += _daYun.startAge - 1
            }
            offset += _forward ? add : -add
            let size = LunarUtil.JIA_ZI.count
            while offset < 0
            {
                offset += size
            }
            offset %= size
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

}
