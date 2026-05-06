import Foundation

@objcMembers
public class NineStar: NSObject {
    public static var NUMBER: [String] = ["一", "二", "三", "四", "五", "六", "七", "八", "九"]
    public static var COLOR: [String] = ["白", "黑", "碧", "绿", "黄", "白", "赤", "白", "紫"]
    public static var WU_XING: [String] = ["水", "土", "木", "木", "土", "金", "金", "土", "火"]

    public static var POSITION: [String] = ["坎", "坤", "震", "巽", "中", "乾", "兑", "艮", "离"]

    public static var NAME_BEI_DOU: [String] = ["天枢", "天璇", "天玑", "天权", "玉衡", "开阳", "摇光", "洞明", "隐元"]

    public static var NAME_XUAN_KONG: [String] = ["贪狼", "巨门", "禄存", "文曲", "廉贞", "武曲", "破军", "左辅", "右弼"]

    public static var NAME_QI_MEN: [String] = ["天蓬", "天芮", "天冲", "天辅", "天禽", "天心", "天柱", "天任", "天英"]

    public static var BA_MEN_QI_MEN: [String] = ["休", "死", "伤", "杜", "", "开", "惊", "生", "景"]

    public static var NAME_TAI_YI: [String] = ["太乙", "摄提", "轩辕", "招摇", "天符", "青龙", "咸池", "太阴", "天乙"]

    public static var TYPE_TAI_YI: [String] = ["吉神", "凶神", "安神", "安神", "凶神", "吉神", "凶神", "吉神", "吉神"]

    public static var SONG_TAI_YI: [String] = ["门中太乙明，星官号贪狼，赌彩财喜旺，婚姻大吉昌，出入无阻挡，参谒见贤良，此行三五里，黑衣别阴阳。", "门前见摄提，百事必忧疑，相生犹自可，相克祸必临，死门并相会，老妇哭悲啼，求谋并吉事，尽皆不相宜，只可藏隐遁，若动伤身疾。", "出入会轩辕，凡事必缠牵，相生全不美，相克更忧煎，远行多不利，博彩尽输钱，九天玄女法，句句不虚言。", "招摇号木星，当之事莫行，相克行人阻，阴人口舌迎，梦寐多惊惧，屋响斧自鸣，阴阳消息理，万法弗违情。", "五鬼为天符，当门阴女谋，相克无好事，行路阻中途，走失难寻觅，道逢有尼姑，此星当门值，万事有灾除。", "神光跃青龙，财气喜重重，投入有酒食，赌彩最兴隆，更逢相生旺，休言克破凶，见贵安营寨，万事总吉同。", "吾将为咸池，当之尽不宜，出入多不利，相克有灾情，赌彩全输尽，求财空手回，仙人真妙语，愚人莫与知，动用虚惊退，反复逆风吹。", "坐临太阴星，百祸不相侵，求谋悉成就，知交有觅寻，回风归来路，恐有殃伏起，密语中记取，慎乎莫轻行。", "迎来天乙星，相逢百事兴，运用和合庆，茶酒喜相迎，求谋并嫁娶，好合有天成，祸福如神验，吉凶甚分明。"]

    public static var LUCK_XUAN_KONG: [String] = ["吉", "凶", "凶", "吉", "凶", "吉", "凶", "吉", "吉"]

    public static var LUCK_QI_MEN: [String] = ["大凶", "大凶", "小吉", "大吉", "大吉", "大吉", "小凶", "小吉", "小凶"]

    public static var YIN_YANG_QI_MEN: [String] = ["阳", "阴", "阳", "阳", "阳", "阴", "阴", "阳", "阴"]

    private var _index: Int

    public var index: Int {
        _index
    }

    public init(index: Int) {
        _index = index
    }

    public class func fromIndex(index: Int) -> NineStar {
        return NineStar(index: index)
    }

    public var number: String {
        NineStar.NUMBER[_index]
    }

    public var color: String {
        NineStar.COLOR[_index]
    }

    public var wuXing: String {
        NineStar.WU_XING[_index]
    }

    public var position: String {
        NineStar.POSITION[_index]
    }

    public var positionDesc: String {
        LunarUtil.POSITION_DESC[position]!
    }

    public var nameInXuanKong: String {
        NineStar.NAME_XUAN_KONG[_index]
    }

    public var nameInBeiDou: String {
        NineStar.NAME_BEI_DOU[_index]
    }

    public var nameInQiMen: String {
        NineStar.NAME_QI_MEN[_index]
    }

    public var nameInTaiYi: String {
        NineStar.NAME_TAI_YI[_index]
    }

    public var luckInQiMen: String {
        NineStar.LUCK_QI_MEN[_index]
    }

    public var luckInXuanKong: String {
        NineStar.LUCK_XUAN_KONG[_index]
    }

    public var yinYangInQiMen: String {
        NineStar.YIN_YANG_QI_MEN[_index]
    }

    public var typeInTaiYi: String {
        NineStar.TYPE_TAI_YI[_index]
    }

    public var baMenInQiMen: String {
        NineStar.BA_MEN_QI_MEN[_index]
    }

    public var songInTaiYi: String {
        NineStar.SONG_TAI_YI[_index]
    }

    override public var description: String {
        "\(number)\(color)\(wuXing)\(nameInBeiDou)"
    }

    public var fullString: String {
        var s = "\(number)\(color)\(wuXing) \(position)(\(positionDesc)) \(nameInBeiDou) 玄空[\(nameInXuanKong) \(luckInXuanKong)] 奇门[\(nameInQiMen) \(luckInQiMen)"
        if !baMenInQiMen.isEmpty {
            s += " \(baMenInQiMen)门] "
        }
        s += " \(yinYangInQiMen) 太乙[\(nameInTaiYi) \(typeInTaiYi)]"
        return s
    }
}
