// C++23 Module - 八字基础数据结构
// 提供干支柱、八字等通用数据结构（基于枚举，类型安全）
export module ZhouYi.BaZiBase;

// 导入第三方库模块
import nlohmann.json;
import fmt;

// 导入干支系统模块
import ZhouYi.GanZhi;

// 导入农历时间库模块
import ZhouYi.tyme;

// 导入标准库模块（最后）
import std;

/**
 * @brief 八字基础命名空间
 * 
 * 提供玄学算法中通用的基础数据结构
 * 所有结构体基于枚举类型，提供编译期类型安全
 */
export namespace ZhouYi::BaZiBase {

// 使用干支系统的类型
using ZhouYi::GanZhi::TianGan;
using ZhouYi::GanZhi::DiZhi;
// Mapper 是命名空间，使用 using namespace 或直接用全限定名
namespace Mapper = ZhouYi::GanZhi::Mapper;

/**
 * @brief 干支柱结构体（基于枚举，类型安全）
 * 
 * 表示一个天干地支的组合（如"甲子"）
 * 使用枚举类型，提供编译期类型检查，避免字符串错误
 */
struct Pillar {
    TianGan gan;   // 天干枚举
    DiZhi zhi;     // 地支枚举

    // ==================== 构造函数 ====================
    
    /**
     * @brief 默认构造函数（甲子）
     */
    constexpr Pillar() : gan(TianGan::Jia), zhi(DiZhi::Zi) {}
    
    /**
     * @brief 枚举构造函数（推荐使用）
     */
    constexpr Pillar(TianGan g, DiZhi z) : gan(g), zhi(z) {}

    /**
     * @brief 从字符串构造（辅助构造函数）
     * 
     * 用于从字符串创建干支柱，主要用于解析外部数据
     * 
     * @param stem_str 天干字符串（如 "甲"）
     * @param branch_str 地支字符串（如 "子"）
     * @throws std::invalid_argument 如果字符串无法映射到枚举
     * 
     * @example
     * Pillar p1("甲", "子");  // 创建甲子
     * Pillar p2("乙", "丑");  // 创建乙丑
     */
    Pillar(const std::string& stem_str, const std::string& branch_str) 
        : gan(string_to_tian_gan(stem_str)), zhi(string_to_di_zhi(branch_str)) {}

    /**
     * @brief 从字符串视图构造
     */
    Pillar(std::string_view stem_str, std::string_view branch_str)
        : gan(string_to_tian_gan(stem_str)), zhi(string_to_di_zhi(branch_str)) {}

    // ==================== 比较运算符 ====================
    
    auto operator<=>(const Pillar& other) const = default;
    bool operator==(const Pillar& other) const = default;

    // ==================== 转换函数 ====================
    
    /**
     * @brief 转换为完整字符串
     * @return 如 "甲子"
     */
    std::string to_string() const {
        return std::string(Mapper::to_zh(gan)) + std::string(Mapper::to_zh(zhi));
    }

    /**
     * @brief 获取天干字符串
     * @return 如 "甲"
     */
    std::string stem() const {
        return std::string(Mapper::to_zh(gan));
    }

    /**
     * @brief 获取地支字符串
     * @return 如 "子"
     */
    std::string branch() const {
        return std::string(Mapper::to_zh(zhi));
    }

    // ==================== 输出运算符 ====================
    
    /**
     * @brief 重载 << 操作符
     */
    friend std::ostream& operator<<(std::ostream& os, const Pillar& obj) {
        return os << Mapper::to_zh(obj.gan) << Mapper::to_zh(obj.zhi);
    }

    // ==================== JSON 序列化 ====================
    
    /**
     * @brief JSON 序列化支持
     */
    friend void to_json(nlohmann::json& j, const Pillar& p) {
        j = {
            {"stem", p.stem()},
            {"branch", p.branch()}
        };
    }

    /**
     * @brief JSON 反序列化支持
     */
    friend void from_json(const nlohmann::json& j, Pillar& p) {
        std::string stem_str = j["stem"];
        std::string branch_str = j["branch"];
        p = Pillar(stem_str, branch_str);
    }

private:
    // ==================== 辅助函数（私有） ====================
    
    /**
     * @brief 字符串转天干枚举
     */
    static TianGan string_to_tian_gan(std::string_view str) {
        static const std::unordered_map<std::string_view, TianGan> map = {
            {"甲", TianGan::Jia}, {"乙", TianGan::Yi}, 
            {"丙", TianGan::Bing}, {"丁", TianGan::Ding},
            {"戊", TianGan::Wu}, {"己", TianGan::Ji},
            {"庚", TianGan::Geng}, {"辛", TianGan::Xin},
            {"壬", TianGan::Ren}, {"癸", TianGan::Gui}
        };
        
        if (auto it = map.find(str); it != map.end()) {
            return it->second;
        }
        throw std::invalid_argument(std::string("无效的天干: ") + std::string(str));
    }

    /**
     * @brief 字符串转地支枚举
     */
    static DiZhi string_to_di_zhi(std::string_view str) {
        static const std::unordered_map<std::string_view, DiZhi> map = {
            {"子", DiZhi::Zi}, {"丑", DiZhi::Chou},
            {"寅", DiZhi::Yin}, {"卯", DiZhi::Mao},
            {"辰", DiZhi::Chen}, {"巳", DiZhi::Si},
            {"午", DiZhi::Wu}, {"未", DiZhi::Wei},
            {"申", DiZhi::Shen}, {"酉", DiZhi::You},
            {"戌", DiZhi::Xu}, {"亥", DiZhi::Hai}
        };
        
        if (auto it = map.find(str); it != map.end()) {
            return it->second;
        }
        throw std::invalid_argument(std::string("无效的地支: ") + std::string(str));
    }
};

/**
 * @brief 四柱八字结构体
 * 
 * 表示一个完整的四柱八字信息（年月日时）
 */
struct BaZi {
    Pillar year;            // 年柱
    Pillar month;           // 月柱
    Pillar day;             // 日柱
    Pillar hour;            // 时柱
    std::string xun_kong_1; // 旬空地支1
    std::string xun_kong_2; // 旬空地支2

    // 默认构造函数
    BaZi() = default;

    // 完整构造函数
    BaZi(const Pillar& y, const Pillar& m, const Pillar& d, const Pillar& h,
         const std::string& xk1 = "", const std::string& xk2 = "")
        : year(y), month(m), day(d), hour(h), xun_kong_1(xk1), xun_kong_2(xk2) {}

    // 比较运算符（注意：由于 std::string 在模块环境下的 <=> 问题，只提供 ==）
    bool operator==(const BaZi& other) const = default;

    /**
     * @brief 重载 << 操作符，用于输出 BaZi
     */
    friend std::ostream& operator<<(std::ostream& os, const BaZi& bazi) {
        os << "年柱: " << bazi.year << "\n"
           << "月柱: " << bazi.month << "\n"
           << "日柱: " << bazi.day << "\n"
           << "时柱: " << bazi.hour << "\n"
           << "旬空: " << bazi.xun_kong_1 << bazi.xun_kong_2;
        return os;
    }

    /**
     * @brief JSON 序列化支持
     */
    friend void to_json(nlohmann::json& j, const BaZi& b) {
        j = {
            {"year", b.year},
            {"month", b.month},
            {"day", b.day},
            {"hour", b.hour},
            {"xun_kong_1", b.xun_kong_1},
            {"xun_kong_2", b.xun_kong_2}
        };
    }

    /**
     * @brief JSON 反序列化支持
     */
    friend void from_json(const nlohmann::json& j, BaZi& b) {
        b.year = j["year"];
        b.month = j["month"];
        b.day = j["day"];
        b.hour = j["hour"];
        std::string xk1 = j["xun_kong_1"];
        std::string xk2 = j["xun_kong_2"];
        b.xun_kong_1 = xk1;
        b.xun_kong_2 = xk2;
    }

    /**
     * @brief 从公历日期时间创建八字
     * 
     * @param year 公历年（如 2024）
     * @param month 公历月（1-12）
     * @param day 公历日（1-31）
     * @param hour 公历时（0-23）
     * @param minute 公历分（0-59，默认0）
     * @param second 公历秒（0-59，默认0）
     * @return 八字对象（包含旬空信息）
     * 
     * @example
     * auto bazi = BaZi::from_solar(2024, 1, 15, 12);  // 2024年1月15日12时
     */
    static BaZi from_solar(int year, int month, int day, int hour, int minute = 0, int second = 0) {
        // 创建公历时间
        auto solar_time = tyme::SolarTime::from_ymd_hms(year, month, day, hour, minute, second);
        
        // 获取农历时间
        auto lunar_hour = solar_time.get_lunar_hour();
        
        // 获取八字
        auto eight_char = lunar_hour.get_eight_char();
        
        // 获取各柱
        auto year_cycle = eight_char.get_year();
        auto month_cycle = eight_char.get_month();
        auto day_cycle = eight_char.get_day();
        auto hour_cycle = eight_char.get_hour();
        
        // 转换为 Pillar
        Pillar year_pillar = convert_sixty_cycle_to_pillar(year_cycle);
        Pillar month_pillar = convert_sixty_cycle_to_pillar(month_cycle);
        Pillar day_pillar = convert_sixty_cycle_to_pillar(day_cycle);
        Pillar hour_pillar = convert_sixty_cycle_to_pillar(hour_cycle);
        
        // 计算旬空（基于日柱）
        auto xun_kong_branches = day_cycle.get_extra_earth_branches();
        std::string xk1 = xun_kong_branches.size() > 0 ? xun_kong_branches[0].get_name() : "";
        std::string xk2 = xun_kong_branches.size() > 1 ? xun_kong_branches[1].get_name() : "";
        
        return BaZi(year_pillar, month_pillar, day_pillar, hour_pillar, xk1, xk2);
    }

    /**
     * @brief 从农历日期时间创建八字
     * 
     * @param year 农历年
     * @param month 农历月（1-12，负数表示闰月）
     * @param day 农历日（1-30）
     * @param hour 时辰（0-23）
     * @param minute 分钟（0-59，默认0）
     * @param second 秒（0-59，默认0）
     * @return 八字对象（包含旬空信息）
     * 
     * @example
     * auto bazi = BaZi::from_lunar(2024, 1, 1, 0);  // 农历2024年正月初一子时
     */
    static BaZi from_lunar(int year, int month, int day, int hour, int minute = 0, int second = 0) {
        // 创建农历时间
        auto lunar_hour = tyme::LunarHour::from_ymd_hms(year, month, day, hour, minute, second);
        
        // 获取八字
        auto eight_char = lunar_hour.get_eight_char();
        
        // 获取各柱
        auto year_cycle = eight_char.get_year();
        auto month_cycle = eight_char.get_month();
        auto day_cycle = eight_char.get_day();
        auto hour_cycle = eight_char.get_hour();
        
        // 转换为 Pillar
        Pillar year_pillar = convert_sixty_cycle_to_pillar(year_cycle);
        Pillar month_pillar = convert_sixty_cycle_to_pillar(month_cycle);
        Pillar day_pillar = convert_sixty_cycle_to_pillar(day_cycle);
        Pillar hour_pillar = convert_sixty_cycle_to_pillar(hour_cycle);
        
        // 计算旬空（基于日柱）
        auto xun_kong_branches = day_cycle.get_extra_earth_branches();
        std::string xk1 = xun_kong_branches.size() > 0 ? xun_kong_branches[0].get_name() : "";
        std::string xk2 = xun_kong_branches.size() > 1 ? xun_kong_branches[1].get_name() : "";
        
        return BaZi(year_pillar, month_pillar, day_pillar, hour_pillar, xk1, xk2);
    }

private:
    /**
     * @brief 将 tyme::SixtyCycle 转换为 Pillar
     * 
     * @param cycle 六十甲子对象
     * @return Pillar 干支柱对象
     */
    static Pillar convert_sixty_cycle_to_pillar(const tyme::SixtyCycle& cycle) {
        // 获取天干地支的名称
        std::string gan_name = cycle.get_heaven_stem().get_name();
        std::string zhi_name = cycle.get_earth_branch().get_name();
        
        // 通过字符串构造 Pillar（会使用 Pillar 的字符串构造函数）
        return Pillar(gan_name, zhi_name);
    }
};

/**
 * @brief 公历日期结构体
 * 
 * 简单封装公历日期，方便使用
 */
struct SolarDate {
    int year;   // 公历年
    int month;  // 公历月（1-12）
    int day;    // 公历日（1-31）
    
    /**
     * @brief 转换为农历日期
     */
    std::string to_lunar_string() const {
        auto solar_day = tyme::SolarDay::from_ymd(year, month, day);
        auto lunar_day = solar_day.get_lunar_day();
        return lunar_day.to_string();
    }
    
    /**
     * @brief 获取八字（按中午12点计算）
     */
    BaZi to_bazi() const {
        return BaZi::from_solar(year, month, day, 12);
    }
};

/**
 * @brief 农历日期结构体
 * 
 * 简单封装农历日期，方便使用
 */
struct LunarDate {
    int year;   // 农历年
    int month;  // 农历月（正数：正常月份，负数：闰月）
    int day;    // 农历日（1-30）
    
    /**
     * @brief 转换为公历日期字符串
     */
    std::string to_solar_string() const {
        auto lunar_day = tyme::LunarDay::from_ymd(year, month, day);
        auto solar_day = lunar_day.get_solar_day();
        return solar_day.to_string();
    }
    
    /**
     * @brief 获取八字（按子时初计算）
     */
    BaZi to_bazi() const {
        return BaZi::from_lunar(year, month, day, 0);
    }
};

} // namespace ZhouYi::BaZiBase

// ==================== fmt 格式化支持（模块外） ====================

// 为 Pillar 提供 fmt 格式化支持
template <>
struct fmt::formatter<ZhouYi::BaZiBase::Pillar> : fmt::formatter<std::string> {
    auto format(const ZhouYi::BaZiBase::Pillar& p, fmt::format_context& ctx) const {
        return fmt::formatter<std::string>::format(p.to_string(), ctx);
    }
};

// 为 BaZi 提供 fmt 格式化支持
template <>
struct fmt::formatter<ZhouYi::BaZiBase::BaZi> : fmt::formatter<std::string> {
    auto format(const ZhouYi::BaZiBase::BaZi& b, fmt::format_context& ctx) const {
        std::string result = fmt::format(
            "年柱: {}\n月柱: {}\n日柱: {}\n时柱: {}\n旬空: {}{}",
            b.year.to_string(),
            b.month.to_string(),
            b.day.to_string(),
            b.hour.to_string(),
            b.xun_kong_1,
            b.xun_kong_2
        );
        return fmt::formatter<std::string>::format(result, ctx);
    }
};
