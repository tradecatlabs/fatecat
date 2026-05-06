import Foundation

@objcMembers
public class LiuYue: NSObject {
    private var _index: Int
    private var _liuNian: LiuNian

    public var index: Int {
        get {
            _index
        }
    }

    public var liuNian: LiuNian {
        get {
            _liuNian
        }
    }

    public init(liuNian: LiuNian, index: Int) {
        _liuNian = liuNian
        _index = index
    }

    public var monthInChinese: String {
        get {
            LunarUtil.MONTH[_index + 1]
        }
    }

    public var ganZhi: String {
        get {
            var offset = 0
            let yearGan = _liuNian.ganZhi.prefix(1)
            switch (yearGan)
            {
            case "甲":
                offset = 2
                break
            case "己":
                offset = 2
                break
            case "乙":
                offset = 4
                break
            case "庚":
                offset = 4
                break
            case "丙":
                offset = 6
                break
            case "辛":
                offset = 6
                break
            case "丁":
                offset = 8
                break
            case "壬":
                offset = 8
                break
            default:
                break
            }
            let gan = LunarUtil.GAN[(_index + offset) % 10 + 1]
            let zhi = LunarUtil.ZHI[(_index + LunarUtil.BASE_MONTH_ZHI_INDEX) % 12 + 1]
            return gan + zhi
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
