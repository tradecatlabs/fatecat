// 奇门遁甲排盘系统 - 核心模块
// 实现奇门遁甲的完整排盘算法

export module ZhouYi.QiMen;

import ZhouYi.GanZhi;
import ZhouYi.tyme;
import ZhouYi.BaZiBase;
import nlohmann.json;
import fmt;
import std;

/**
 * @brief 奇门遁甲命名空间
 * 
 * 提供奇门遁甲排盘的完整功能
 */
export namespace ZhouYi::QiMen {

using namespace ZhouYi::GanZhi;
using namespace tyme;

// ==================== 枚举定义 ====================

/**
 * @brief 九宫位置枚举
 * 
 * 按照后天八卦九宫排列：
 * 4 9 2
 * 3 5 7
 * 8 1 6
 */
enum class Palace : std::uint8_t {
    Center = 5,  // 中宫
    North = 1,   // 坎一宫（北）
    NorthEast = 8,  // 艮八宫（东北）
    East = 3,    // 震三宫（东）
    SouthEast = 4,  // 巽四宫（东南）
    South = 9,   // 离九宫（南）
    SouthWest = 2,  // 坤二宫（西南）
    West = 7,    // 兑七宫（西）
    NorthWest = 6   // 乾六宫（西北）
};

/**
 * @brief 八门枚举
 * 
 * 八门按照后天八卦方位排列
 */
enum class Gate : std::uint8_t {
    Du = 0,      // 杜门（巽四宫）
    Jing = 1,    // 景门（离九宫）
    Si = 2,      // 死门（坤二宫）
    Shang = 3,   // 伤门（震三宫）
    Jing_Center = 4,  // 中宫
    Jing_Gate = 5,    // 惊门（兑七宫）
    Sheng = 6,   // 生门（艮八宫）
    Xiu = 7,     // 休门（坎一宫）
    Kai = 8      // 开门（乾六宫）
};

/**
 * @brief 九星枚举
 * 
 * 奇门九星
 */
enum class Star : std::uint8_t {
    TianFu = 0,      // 天辅
    TianYing = 1,    // 天英
    TianRui = 2,     // 天芮
    TianChong = 3,   // 天冲
    TianQin = 4,     // 天禽
    TianZhu = 5,     // 天柱
    TianRen = 6,     // 天任
    TianPeng = 7,    // 天蓬
    TianXin = 8      // 天心
};

/**
 * @brief 八神枚举
 * 
 * 奇门八神
 */
enum class Spirit : std::uint8_t {
    ZhiFu = 0,       // 直符
    TengShe = 1,     // 腾蛇
    TaiYin = 2,      // 太阴
    LiuHe = 3,       // 六合
    BaiHu = 4,       // 白虎
    XuanWu = 5,      // 玄武
    JiuDi = 6,       // 九地
    JiuTian = 7      // 九天
};

/**
 * @brief 阴阳遁枚举
 */
enum class Dun : std::uint8_t {
    Yang = 0,        // 阳遁
    Yin = 1          // 阴遁
};

/**
 * @brief 三元枚举
 * 
 * 上中下三元
 */
enum class Yuan : std::uint8_t {
    Shang = 0,       // 上元
    Zhong = 1,       // 中元
    Xia = 2          // 下元
};

/**
 * @brief 二十四节气枚举
 */
enum class SolarTerm : std::uint8_t {
    DongZhi = 0,     // 冬至
    XiaoHan = 1,     // 小寒
    DaHan = 2,       // 大寒
    LiChun = 3,      // 立春
    YuShui = 4,      // 雨水
    JingZhe = 5,     // 惊蛰
    ChunFen = 6,     // 春分
    QingMing = 7,    // 清明
    GuYu = 8,        // 谷雨
    LiXia = 9,       // 立夏
    XiaoMan = 10,    // 小满
    MangZhong = 11,  // 芒种
    XiaZhi = 12,     // 夏至
    XiaoShu = 13,    // 小暑
    DaShu = 14,      // 大暑
    LiQiu = 15,      // 立秋
    ChuShu = 16,     // 处暑
    BaiLu = 17,      // 白露
    QiuFen = 18,     // 秋分
    HanLu = 19,      // 寒露
    ShuangJiang = 20, // 霜降
    LiDong = 21,     // 立冬
    XiaoXue = 22,    // 小雪
    DaXue = 23       // 大雪
};

/**
 * @brief 六甲旬首枚举
 * 
 * 六十甲子分为六旬
 */
enum class JiaXun : std::uint8_t {
    JiaZi = 0,       // 甲子旬
    JiaXu = 1,       // 甲戌旬
    JiaShen = 2,     // 甲申旬
    JiaWu = 3,       // 甲午旬
    JiaChen = 4,     // 甲辰旬
    JiaYin = 5       // 甲寅旬
};

// ==================== 核心数据结构 ====================

/**
 * @brief 奇门盘单个宫位的信息
 */
struct PalaceInfo {
    Palace palace;           // 宫位
    Star star;              // 九星
    Gate gate;              // 八门
    Spirit spirit;          // 八神
    std::uint8_t tian_gan;  // 天盘天干（0-9 对应 甲-癸）
    std::uint8_t di_gan;    // 地盘天干（0-9 对应 甲-癸）
    std::uint8_t ren_gan;   // 人盘天干（0-9 对应 甲-癸）
};

/**
 * @brief 奇门盘完整信息
 */
struct QiMenPan {
    Dun dun;                 // 阴阳遁
    Yuan yuan;               // 三元
    std::uint8_t ju;         // 局数（1-9）
    SolarTerm solar_term;    // 节气
    std::array<PalaceInfo, 9> palaces;  // 九宫信息
    
    // 直符和直使
    Star zhi_fu_star;        // 直符星
    Gate zhi_shi_gate;       // 直使门
    Palace zhi_fu_palace;    // 直符所在宫
    
    // 日期信息
    int solar_year = 0;      // 阳历年
    int solar_month = 0;     // 阳历月
    int solar_day = 0;       // 阳历日
    int hour = 0;            // 时辰
    int lunar_year = 0;      // 农历年
    int lunar_month = 0;     // 农历月
    int lunar_day = 0;       // 农历日
    bool is_leap_month = false;  // 是否闰月
    
    // 八字信息
    std::optional<BaZiBase::BaZi> ba_zi;  // 八字（年月日时四柱）
};

// ==================== 工具函数 ====================

/**
 * @brief 获取宫位的中文名称
 */
constexpr std::string_view palace_name(Palace p) noexcept {
    switch (p) {
        case Palace::Center: return "中";
        case Palace::North: return "北";
        case Palace::NorthEast: return "东北";
        case Palace::East: return "东";
        case Palace::SouthEast: return "东南";
        case Palace::South: return "南";
        case Palace::SouthWest: return "西南";
        case Palace::West: return "西";
        case Palace::NorthWest: return "西北";
        default: return "未知";
    }
}

/**
 * @brief 获取八门的中文名称
 */
constexpr std::string_view gate_name(Gate g) noexcept {
    switch (g) {
        case Gate::Du: return "杜";
        case Gate::Jing: return "景";
        case Gate::Si: return "死";
        case Gate::Shang: return "伤";
        case Gate::Jing_Gate: return "惊";
        case Gate::Sheng: return "生";
        case Gate::Xiu: return "休";
        case Gate::Kai: return "开";
        default: return "未知";
    }
}

/**
 * @brief 获取九星的中文名称
 */
constexpr std::string_view star_name(Star s) noexcept {
    switch (s) {
        case Star::TianFu: return "天辅";
        case Star::TianYing: return "天英";
        case Star::TianRui: return "天芮";
        case Star::TianChong: return "天冲";
        case Star::TianQin: return "天禽";
        case Star::TianZhu: return "天柱";
        case Star::TianRen: return "天任";
        case Star::TianPeng: return "天蓬";
        case Star::TianXin: return "天心";
        default: return "未知";
    }
}

/**
 * @brief 获取八神的中文名称
 */
constexpr std::string_view spirit_name(Spirit sp) noexcept {
    switch (sp) {
        case Spirit::ZhiFu: return "直符";
        case Spirit::TengShe: return "腾蛇";
        case Spirit::TaiYin: return "太阴";
        case Spirit::LiuHe: return "六合";
        case Spirit::BaiHu: return "白虎";
        case Spirit::XuanWu: return "玄武";
        case Spirit::JiuDi: return "九地";
        case Spirit::JiuTian: return "九天";
        default: return "未知";
    }
}

/**
 * @brief 获取节气的中文名称
 */
constexpr std::string_view solar_term_name(SolarTerm st) noexcept {
    switch (st) {
        case SolarTerm::DongZhi: return "冬至";
        case SolarTerm::XiaoHan: return "小寒";
        case SolarTerm::DaHan: return "大寒";
        case SolarTerm::LiChun: return "立春";
        case SolarTerm::YuShui: return "雨水";
        case SolarTerm::JingZhe: return "惊蛰";
        case SolarTerm::ChunFen: return "春分";
        case SolarTerm::QingMing: return "清明";
        case SolarTerm::GuYu: return "谷雨";
        case SolarTerm::LiXia: return "立夏";
        case SolarTerm::XiaoMan: return "小满";
        case SolarTerm::MangZhong: return "芒种";
        case SolarTerm::XiaZhi: return "夏至";
        case SolarTerm::XiaoShu: return "小暑";
        case SolarTerm::DaShu: return "大暑";
        case SolarTerm::LiQiu: return "立秋";
        case SolarTerm::ChuShu: return "处暑";
        case SolarTerm::BaiLu: return "白露";
        case SolarTerm::QiuFen: return "秋分";
        case SolarTerm::HanLu: return "寒露";
        case SolarTerm::ShuangJiang: return "霜降";
        case SolarTerm::LiDong: return "立冬";
        case SolarTerm::XiaoXue: return "小雪";
        case SolarTerm::DaXue: return "大雪";
        default: return "未知";
    }
}

// 天干地支名称映射已在 GanZhi 模块中定义，使用 Mapper::to_zh() 获取

// ==================== 定局算法 ====================

/**
 * @brief 根据节气确定阴阳遁
 * 
 * 冬至后用阳遁，夏至后用阴遁
 */
constexpr Dun get_dun_from_solar_term(SolarTerm st) noexcept {
    // 冬至到（不含）夏至为阳遁；夏至到（不含）冬至为阴遁
    switch (st) {
        // 阳遁
        case SolarTerm::DongZhi:
        case SolarTerm::XiaoHan:
        case SolarTerm::DaHan:
        case SolarTerm::LiChun:
        case SolarTerm::YuShui:
        case SolarTerm::JingZhe:
        case SolarTerm::ChunFen:
        case SolarTerm::QingMing:
        case SolarTerm::GuYu:
        case SolarTerm::LiXia:
        case SolarTerm::XiaoMan:
        case SolarTerm::MangZhong:
            return Dun::Yang;
        // 阴遁
        case SolarTerm::XiaZhi:
        case SolarTerm::XiaoShu:
        case SolarTerm::DaShu:
        case SolarTerm::LiQiu:
        case SolarTerm::ChuShu:
        case SolarTerm::BaiLu:
        case SolarTerm::QiuFen:
        case SolarTerm::HanLu:
        case SolarTerm::ShuangJiang:
        case SolarTerm::LiDong:
        case SolarTerm::XiaoXue:
        case SolarTerm::DaXue:
            return Dun::Yin;
        default:
            return Dun::Yang;
    }
}

/**
 * @brief 根据节气和三元确定局数
 * 
 * 按照阳遁歌和阴遁歌确定
 */
constexpr std::uint8_t get_ju_from_solar_term_and_yuan(SolarTerm st, Yuan yuan) noexcept {
    // 阳遁歌：
    // 冬至惊蛰一七四，小寒二八五同推；
    // 大寒春分三九六，芒种六三九是真；
    // 谷雨小满五二八，立春八五二相随；
    // 清明立夏四一七，九六三从雨水期。
    // 阴遁歌：
    // 夏至白露九三六，小暑八二五重逢；
    // 大暑秋分七一四，立秋二五八流通；
    // 霜降小雪五八二，大雪四七一相同；
    // 处暑排来一四七，立冬寒露六九三。
    
    Dun dun = get_dun_from_solar_term(st);
    
    if (dun == Dun::Yang) {
        switch (st) {
            // 冬至惊蛰一七四
            case SolarTerm::DongZhi:
            case SolarTerm::JingZhe:
                return yuan == Yuan::Shang ? 1 : (yuan == Yuan::Zhong ? 7 : 4);
            // 小寒二八五
            case SolarTerm::XiaoHan:
                return yuan == Yuan::Shang ? 2 : (yuan == Yuan::Zhong ? 8 : 5);
            // 大寒春分三九六
            case SolarTerm::DaHan:
            case SolarTerm::ChunFen:
                return yuan == Yuan::Shang ? 3 : (yuan == Yuan::Zhong ? 9 : 6);
            // 芒种六三九
            case SolarTerm::MangZhong:
                return yuan == Yuan::Shang ? 6 : (yuan == Yuan::Zhong ? 3 : 9);
            // 谷雨小满五二八
            case SolarTerm::GuYu:
            case SolarTerm::XiaoMan:
                return yuan == Yuan::Shang ? 5 : (yuan == Yuan::Zhong ? 2 : 8);
            // 立春八五二
            case SolarTerm::LiChun:
                return yuan == Yuan::Shang ? 8 : (yuan == Yuan::Zhong ? 5 : 2);
            // 清明立夏四一七
            case SolarTerm::QingMing:
            case SolarTerm::LiXia:
                return yuan == Yuan::Shang ? 4 : (yuan == Yuan::Zhong ? 1 : 7);
            // 九六三从雨水期（雨水）
            case SolarTerm::YuShui:
                return yuan == Yuan::Shang ? 9 : (yuan == Yuan::Zhong ? 6 : 3);
            default:
                return 1;
        }
    } else {  // 阴遁
        switch (st) {
            // 夏至白露九三六
            case SolarTerm::XiaZhi:
            case SolarTerm::BaiLu:
                return yuan == Yuan::Shang ? 9 : (yuan == Yuan::Zhong ? 3 : 6);
            // 小暑八二五
            case SolarTerm::XiaoShu:
                return yuan == Yuan::Shang ? 8 : (yuan == Yuan::Zhong ? 2 : 5);
            // 大暑秋分七一四
            case SolarTerm::DaShu:
            case SolarTerm::QiuFen:
                return yuan == Yuan::Shang ? 7 : (yuan == Yuan::Zhong ? 1 : 4);
            // 立秋二五八
            case SolarTerm::LiQiu:
                return yuan == Yuan::Shang ? 2 : (yuan == Yuan::Zhong ? 5 : 8);
            // 霜降小雪五八二
            case SolarTerm::ShuangJiang:
            case SolarTerm::XiaoXue:
                return yuan == Yuan::Shang ? 5 : (yuan == Yuan::Zhong ? 8 : 2);
            // 大雪四七一
            case SolarTerm::DaXue:
                return yuan == Yuan::Shang ? 4 : (yuan == Yuan::Zhong ? 7 : 1);
            // 处暑排来一四七
            case SolarTerm::ChuShu:
                return yuan == Yuan::Shang ? 1 : (yuan == Yuan::Zhong ? 4 : 7);
            // 立冬寒露六九三
            case SolarTerm::LiDong:
            case SolarTerm::HanLu:
                return yuan == Yuan::Shang ? 6 : (yuan == Yuan::Zhong ? 9 : 3);
            default:
                return 1;
        }
    }
  }

/**
 * @brief 根据地支确定三元
 * 
 * 根据符头日期确定上中下三元
 */
constexpr Yuan get_yuan_from_di_zhi(std::uint8_t di_zhi) noexcept {
    // 子午卯酉（四仲）-> 上元
    // 寅申巳亥（四孟）-> 中元
    // 辰戌丑未（四季）-> 下元
    switch (di_zhi) {
        case 0:  // 子
        case 6:  // 午
        case 3:  // 卯
        case 9:  // 酉
            return Yuan::Shang;
        case 2:  // 寅
        case 8:  // 申
        case 5:  // 巳
        case 11: // 亥
            return Yuan::Zhong;
        case 4:  // 辰
        case 10: // 戌
        case 1:  // 丑
        case 7:  // 未
            return Yuan::Xia;
        default:
            return Yuan::Shang;
    }
}

// ==================== 排盘算法 ====================

/**
 * @brief 洛书九宫顺序（顺时针，不含中宫）
 * 
 * 用于转盘时的宫位转动
 * 顺序：1(坎) -> 8(艮) -> 3(震) -> 4(巽) -> 9(离) -> 2(坤) -> 7(兑) -> 6(乾)
 */
constexpr std::array<std::uint8_t, 8> get_luo_shu_order() noexcept {
    return {1, 8, 3, 4, 9, 2, 7, 6};
}

/**
 * @brief 洛书九宫逆序（逆时针，不含中宫）
 * 
 * 用于阴遁转盘
 * 顺序：1(坎) -> 6(乾) -> 7(兑) -> 2(坤) -> 9(离) -> 4(巽) -> 3(震) -> 8(艮)
 */
constexpr std::array<std::uint8_t, 8> get_luo_shu_reverse_order() noexcept {
    return {1, 6, 7, 2, 9, 4, 3, 8};
}

/**
 * @brief 旬首与六仪的映射关系
 * 
 * 甲子旬→戊，甲戌旬→己，甲申旬→庚，甲午旬→辛，甲辰旬→壬，甲寅旬→癸
 */
constexpr std::uint8_t get_liu_yi_from_jia_xun(JiaXun xun) noexcept {
    switch (xun) {
        case JiaXun::JiaZi:   return 4;  // 戊
        case JiaXun::JiaXu:   return 5;  // 己
        case JiaXun::JiaShen: return 6;  // 庚
        case JiaXun::JiaWu:   return 7;  // 辛
        case JiaXun::JiaChen: return 8;  // 壬
        case JiaXun::JiaYin:  return 9;  // 癸
        default: return 4;
    }
}

/**
 * @brief 根据宫位数字获取宫位枚举
 */
constexpr Palace get_palace_from_number(std::uint8_t num) noexcept {
    switch (num) {
        case 1: return Palace::North;
        case 2: return Palace::SouthWest;
        case 3: return Palace::East;
        case 4: return Palace::SouthEast;
        case 5: return Palace::Center;
        case 6: return Palace::NorthWest;
        case 7: return Palace::West;
        case 8: return Palace::NorthEast;
        case 9: return Palace::South;
        default: return Palace::Center;
    }
}

/**
 * @brief 根据宫位枚举获取宫位数字
 */
constexpr std::uint8_t get_number_from_palace(Palace p) noexcept {
    return static_cast<std::uint8_t>(p);
}

/**
 * @brief 获取九宫对应的九星（固定排列）
 */
constexpr Star get_star_at_palace(Palace p) noexcept {
    switch (p) {
        case Palace::SouthEast: return Star::TianFu;      // 巽四宫
        case Palace::South: return Star::TianYing;        // 离九宫
        case Palace::SouthWest: return Star::TianRui;     // 坤二宫
        case Palace::East: return Star::TianChong;        // 震三宫
        case Palace::Center: return Star::TianQin;        // 中五宫
        case Palace::West: return Star::TianZhu;          // 兑七宫
        case Palace::NorthEast: return Star::TianRen;     // 艮八宫
        case Palace::North: return Star::TianPeng;        // 坎一宫
        case Palace::NorthWest: return Star::TianXin;     // 乾六宫
        default: return Star::TianFu;
    }
}

/**
 * @brief 获取九宫对应的八门（固定排列）
 */
constexpr Gate get_gate_at_palace(Palace p) noexcept {
    switch (p) {
        case Palace::SouthEast: return Gate::Du;          // 巽四宫
        case Palace::South: return Gate::Jing;            // 离九宫
        case Palace::SouthWest: return Gate::Si;          // 坤二宫
        case Palace::East: return Gate::Shang;            // 震三宫
        case Palace::Center: return Gate::Jing_Center;    // 中五宫
        case Palace::West: return Gate::Jing_Gate;        // 兑七宫
        case Palace::NorthEast: return Gate::Sheng;       // 艮八宫
        case Palace::North: return Gate::Xiu;             // 坎一宫
        case Palace::NorthWest: return Gate::Kai;         // 乾六宫
        default: return Gate::Du;
    }
}

/**
 * @brief 获取宫位序列（用于顺飞和逆飞）
 */
constexpr std::array<Palace, 9> get_palace_sequence(bool reverse = false) noexcept {
    if (!reverse) {
        // 顺飞：9 1 2 3 4 5 6 7 8
        return {
            Palace::South, Palace::North, Palace::SouthWest,
            Palace::East, Palace::Center, Palace::West,
            Palace::NorthEast, Palace::NorthWest, Palace::NorthWest
        };
    } else {
        // 逆飞：9 7 8 3 5 1 4 2 6
        return {
            Palace::South, Palace::West, Palace::NorthEast,
            Palace::East, Palace::Center, Palace::North,
            Palace::SouthEast, Palace::SouthWest, Palace::NorthWest
        };
    }
}

/**
 * @brief 天干序列（地盘排列）
 * 
 * 戊己庚辛壬癸丁丙乙
 */
constexpr std::array<std::uint8_t, 9> get_tian_gan_sequence() noexcept {
    return {4, 5, 6, 7, 8, 9, 3, 2, 1};  // 戊己庚辛壬癸丁丙乙
}

// ==================== JSON 序列化 ====================

/**
 * @brief 奇门盘 JSON 序列化
 */
inline void to_json(nlohmann::json& j, const QiMenPan& pan) {
    using namespace ZhouYi::GanZhi;
    
    // 按照顺序添加字段（JSON 会保持插入顺序）
    
    // 1. 日期信息（阳历和农历）
    nlohmann::json solar_date = nlohmann::json::object();
    solar_date["year"] = pan.solar_year;
    solar_date["month"] = pan.solar_month;
    solar_date["day"] = pan.solar_day;
    solar_date["hour"] = pan.hour;
    j["solar_date"] = solar_date;
    
    nlohmann::json lunar_date = nlohmann::json::object();
    lunar_date["year"] = pan.lunar_year;
    lunar_date["month"] = pan.lunar_month;
    lunar_date["day"] = pan.lunar_day;
    lunar_date["is_leap_month"] = pan.is_leap_month;
    j["lunar_date"] = lunar_date;
    
    // 2. 八字信息
    if (pan.ba_zi.has_value()) {
        j["ba_zi"] = pan.ba_zi.value();
    }
    
    // 3. 阴阳遁信息
    j["dun"] = pan.dun == Dun::Yang ? "yang" : "yin";
    j["dun_zh"] = pan.dun == Dun::Yang ? "阳遁" : "阴遁";
    
    // 4. 三元信息
    std::string yuan_str;
    std::string yuan_zh;
    switch (pan.yuan) {
        case Yuan::Shang: yuan_str = "shang"; yuan_zh = "上元"; break;
        case Yuan::Zhong: yuan_str = "zhong"; yuan_zh = "中元"; break;
        case Yuan::Xia: yuan_str = "xia"; yuan_zh = "下元"; break;
    }
    j["yuan"] = yuan_str;
    j["yuan_zh"] = yuan_zh;
    
    // 5. 局数和节气
    j["ju"] = pan.ju;
    j["solar_term"] = std::string(solar_term_name(pan.solar_term));
    
    // 6. 直符直使信息
    j["zhi_fu_star"] = std::string(star_name(pan.zhi_fu_star));
    j["zhi_shi_gate"] = std::string(gate_name(pan.zhi_shi_gate));
    j["zhi_fu_palace"] = std::string(palace_name(pan.zhi_fu_palace));
    
    // 7. 九宫信息（最后）
    nlohmann::json palaces_json = nlohmann::json::array();
    for (std::size_t i = 0; i < pan.palaces.size(); ++i) {
        const auto& p = pan.palaces[i];
        // 使用有序 JSON 对象，palace_num 在最前面
        nlohmann::json palace_json = nlohmann::json::object();
        
        palace_json["palace_num"] = get_number_from_palace(p.palace);
        palace_json["palace_name"] = std::string(palace_name(p.palace));
        palace_json["star"] = std::string(star_name(p.star));
        palace_json["gate"] = std::string(gate_name(p.gate));
        palace_json["spirit"] = std::string(spirit_name(p.spirit));
        palace_json["di_gan"] = std::string(Mapper::to_zh(static_cast<TianGan>(p.di_gan)));
        palace_json["tian_gan"] = std::string(Mapper::to_zh(static_cast<TianGan>(p.tian_gan)));
        
        palaces_json.push_back(palace_json);
    }
    j["palaces"] = palaces_json;
}

}  // namespace ZhouYi::QiMen
