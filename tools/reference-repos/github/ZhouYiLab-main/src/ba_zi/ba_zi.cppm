// C++23 Module - 八字排盘系统
export module ZhouYi.BaZi;

// 导入第三方库模块
import fmt;
import nlohmann.json;

// 导入自定义通用模块
import ZhouYi.BaZiBase;      // 八字基础数据结构（Pillar, BaZi）
import ZhouYi.GanZhi;        // 干支系统（包含十神）
import ZhouYi.WuXingUtils;   // 五行工具
import ZhouYi.tyme;          // 时间模块

// 导入标准库模块（最后）
import std;

/**
 * @brief 八字命理命名空间
 * 
 * 提供完整的八字排盘功能，包括：
 * - 大运（10年一个大运）
 * - 流年（每年运势）
 * - 流月（每月运势）
 * - 流时（每时运势）
 */
export namespace ZhouYi::BaZi {

// 使用通用命名空间
using namespace ZhouYi::BaZiBase;
using namespace ZhouYi::GanZhi;
using namespace ZhouYi::WuXingUtils;
namespace Mapper = ZhouYi::GanZhi::Mapper;

// ==================== 大运类 ====================

/**
 * @brief 大运信息
 * 
 * 每个大运10年，从某个年龄开始
 */
struct DaYun {
    Pillar pillar;              // 大运干支
    int start_age;              // 起运年龄
    int end_age;                // 结束年龄（start_age + 9）
    int start_year;             // 起始公历年份
    int end_year;               // 结束公历年份
    ShiShen gan_shi_shen;       // 天干十神
    ShiShen zhi_shi_shen;       // 地支十神（地支藏干主气）
    
    DaYun(const Pillar& p, int age, int year_start, TianGan day_gan)
        : pillar(p), start_age(age), end_age(age + 9), 
          start_year(year_start), end_year(year_start + 9) {
        gan_shi_shen = get_shi_shen(day_gan, p.gan);
        // 地支藏干取主气计算十神
        auto cang_gan = get_cang_gan(p.zhi);
        zhi_shi_shen = get_shi_shen(day_gan, cang_gan[0]);
    }
    
    /**
     * @brief 判断某个年龄是否在此大运范围内
     */
    bool contains_age(int age) const {
        return age >= start_age && age <= end_age;
    }
    
    /**
     * @brief 转换为字符串
     */
    std::string to_string() const {
        return std::format("{}({}-{}岁 {}-{}年)", 
                          pillar.to_string(), start_age, end_age,
                          start_year, end_year);
    }
    
    /**
     * @brief JSON 序列化
     */
    friend void to_json(nlohmann::json& j, const DaYun& dy) {
        j = {
            {"pillar", dy.pillar},
            {"start_age", dy.start_age},
            {"end_age", dy.end_age},
            {"start_year", dy.start_year},
            {"end_year", dy.end_year},
            {"gan_shi_shen", std::string(shi_shen_to_zh(dy.gan_shi_shen))},
            {"zhi_shi_shen", std::string(shi_shen_to_zh(dy.zhi_shi_shen))}
        };
    }
};

/**
 * @brief 大运系统
 * 
 * 管理一个人一生的大运，使用 tyme 库计算起运年龄
 */
class DaYunSystem {
private:
    std::vector<DaYun> da_yun_list_;    // 大运列表
    int qi_yun_age_;                    // 起运年龄
    bool shun_pai_;                     // 顺排（true）或逆排（false）
    tyme::ChildLimit child_limit_;      // 童限对象
    int birth_year_;                    // 出生年份（用于计算年龄）
    
public:
    /**
     * @brief 构造函数
     * 
     * @param bazi 八字
     * @param is_male 是否为男性
     * @param birth_year 出生年份
     * @param birth_month 出生月份
     * @param birth_day 出生日
     * @param birth_hour 出生时辰
     * @param birth_minute 出生分钟（默认0）
     * @param birth_second 出生秒（默认0）
     */
    DaYunSystem(const BaZiBase::BaZi& bazi, bool is_male, 
                int birth_year, int birth_month, int birth_day, int birth_hour = 12,
                int birth_minute = 0, int birth_second = 0) 
        : child_limit_(create_child_limit(birth_year, birth_month, birth_day, 
                                          birth_hour, birth_minute, birth_second, is_male)),
          birth_year_(birth_year) {
        // 判断年柱天干阴阳（阳年为阳，阴年为阴）
        bool yang_year = (get_yin_yang(bazi.year.gan) == YinYang::Yang);
        
        // 阳男阴女顺排，阴男阳女逆排
        shun_pai_ = (is_male == yang_year);
        
        // 计算实际起运年龄（周岁）= 起运年份 - 出生年份
        int qi_yun_year = child_limit_.get_end_time().get_year();
        qi_yun_age_ = qi_yun_year - birth_year;
        
        // 生成大运列表（一般排10个大运，100年）
        generate_da_yun_list(bazi, 10, birth_year);
    }
    
    /**
     * @brief 获取大运列表
     */
    const std::vector<DaYun>& get_da_yun_list() const {
        return da_yun_list_;
    }
    
    /**
     * @brief 获取起运年龄
     */
    int get_qi_yun_age() const {
        return qi_yun_age_;
    }
    
    /**
     * @brief 根据年龄获取当前大运
     */
    std::optional<DaYun> get_da_yun_by_age(int age) const {
        for (const auto& dy : da_yun_list_) {
            if (dy.contains_age(age)) {
                return dy;
            }
        }
        return std::nullopt;
    }
    
    /**
     * @brief 是否顺排
     */
    bool is_shun_pai() const {
        return shun_pai_;
    }
    
    /**
     * @brief 获取童限对象（用于访问 tyme 库的详细信息）
     */
    const tyme::ChildLimit& get_child_limit() const {
        return child_limit_;
    }
    
    /**
     * @brief 获取童限详细信息
     * 
     * @return 包含起运年龄详细信息的结构体
     */
    struct ChildLimitDetail {
        int start_age;          // 起运年龄（虚岁）
        int year_count;         // 年数
        int month_count;        // 月数
        int day_count;          // 日数
        int hour_count;         // 小时数
        int minute_count;       // 分钟数
        tyme::SolarTime start_time;   // 出生时刻
        tyme::SolarTime end_time;     // 起运时刻
    };
    
    ChildLimitDetail get_child_limit_detail() const {
        return ChildLimitDetail{
            child_limit_.get_start_age(),
            child_limit_.get_year_count(),
            child_limit_.get_month_count(),
            child_limit_.get_day_count(),
            child_limit_.get_hour_count(),
            child_limit_.get_minute_count(),
            child_limit_.get_start_time(),
            child_limit_.get_end_time()
        };
    }
    
    /**
     * @brief 从 tyme 库获取指定索引的大运
     * 
     * @param index 大运索引（0开始）
     * @return tyme::DecadeFortune 对象
     */
    tyme::DecadeFortune get_tyme_decade_fortune(int index) const {
        return tyme::DecadeFortune::from_child_limit(child_limit_, index);
    }
    
    /**
     * @brief 获取所有大运的 tyme 对象列表
     * 
     * @param count 大运数量（默认10个）
     * @return 大运列表
     */
    std::vector<tyme::DecadeFortune> get_all_tyme_decade_fortunes(int count = 10) const {
        std::vector<tyme::DecadeFortune> fortunes;
        fortunes.reserve(count);
        for (int i = 0; i < count; ++i) {
            fortunes.push_back(tyme::DecadeFortune::from_child_limit(child_limit_, i));
        }
        return fortunes;
    }
    
private:
    /**
     * @brief 创建童限对象
     * 
     * 使用 tyme 库计算童限信息（包含起运年龄）
     */
    static tyme::ChildLimit create_child_limit(int year, int month, int day, 
                                               int hour, int minute, int second, 
                                               bool is_male) {
        // 创建公历时间对象
        auto solar_time = tyme::SolarTime::from_ymd_hms(year, month, day, hour, minute, second);
        
        // 创建性别对象
        tyme::Gender gender = is_male ? tyme::Gender::MAN : tyme::Gender::WOMAN;
        
        // 使用 tyme 库计算童限（包含起运年龄）
        return tyme::ChildLimit::from_solar_time(solar_time, gender);
    }
    
    /**
     * @brief 生成大运列表
     */
    void generate_da_yun_list(const BaZiBase::BaZi& bazi, int count, int birth_year) {
        da_yun_list_.clear();
        
        // 从月柱开始推算
        TianGan current_gan = bazi.month.gan;
        DiZhi current_zhi = bazi.month.zhi;
        
        // 从童限获取实际起运年份
        // 起运时刻就是第一个大运的起始时间
        int qi_yun_year = child_limit_.get_end_time().get_year();
        
        // 计算实际起运年龄（周岁）
        // 起运年龄 = 起运年份 - 出生年份
        int current_age = qi_yun_year - birth_year;
        int current_year = qi_yun_year;
        
        for (int i = 0; i < count; ++i) {
            // 前进或后退一柱
            if (shun_pai_) {
                // 顺排：干支都加1
                current_gan = static_cast<TianGan>((static_cast<int>(current_gan) + 1) % 10);
                current_zhi = static_cast<DiZhi>((static_cast<int>(current_zhi) + 1) % 12);
            } else {
                // 逆排：干支都减1
                current_gan = static_cast<TianGan>((static_cast<int>(current_gan) + 9) % 10);
                current_zhi = static_cast<DiZhi>((static_cast<int>(current_zhi) + 11) % 12);
            }
            
            Pillar da_yun_pillar(current_gan, current_zhi);
            da_yun_list_.emplace_back(da_yun_pillar, current_age, current_year, bazi.day.gan);
            
            current_age += 10;
            current_year += 10;
        }
    }
};

// ==================== 流年类 ====================

/**
 * @brief 流年信息
 */
struct LiuNian {
    int year;                   // 公历年份
    Pillar pillar;              // 流年干支
    int age;                    // 虚岁年龄
    ShiShen gan_shi_shen;       // 天干十神
    ShiShen zhi_shi_shen;       // 地支十神
    
    LiuNian(int y, const Pillar& p, int a, TianGan day_gan)
        : year(y), pillar(p), age(a) {
        gan_shi_shen = get_shi_shen(day_gan, p.gan);
        auto cang_gan = get_cang_gan(p.zhi);
        zhi_shi_shen = get_shi_shen(day_gan, cang_gan[0]);
    }
    
    /**
     * @brief 转换为字符串
     */
    std::string to_string() const {
        return std::format("{}年 {} ({}岁)", year, pillar.to_string(), age);
    }
    
    /**
     * @brief JSON 序列化
     */
    friend void to_json(nlohmann::json& j, const LiuNian& ln) {
        j = {
            {"year", ln.year},
            {"pillar", ln.pillar},
            {"age", ln.age},
            {"gan_shi_shen", std::string(shi_shen_to_zh(ln.gan_shi_shen))},
            {"zhi_shi_shen", std::string(shi_shen_to_zh(ln.zhi_shi_shen))}
        };
    }
};

/**
 * @brief 创建流年
 * 
 * @param year 公历年份
 * @param birth_year 出生年份
 * @param day_gan 日干
 * @return LiuNian 流年对象
 */
inline LiuNian create_liu_nian(int year, int birth_year, TianGan day_gan) {
    // 从年份获取干支
    // 使用年中的日期（7月1日）以确保获取正确的农历年干支
    // 因为1月1日可能还在上一个农历年
    auto solar_day = tyme::SolarDay::from_ymd(year, 7, 1);
    auto lunar_day = solar_day.get_lunar_day();
    auto lunar_year = lunar_day.get_lunar_month().get_lunar_year();
    auto year_cycle = lunar_year.get_sixty_cycle();
    
    // 转换为 Pillar
    std::string gan_name = year_cycle.get_heaven_stem().get_name();
    std::string zhi_name = year_cycle.get_earth_branch().get_name();
    Pillar year_pillar(gan_name, zhi_name);
    
    // 计算虚岁
    int age = year - birth_year + 1;
    
    return LiuNian(year, year_pillar, age, day_gan);
}

// ==================== 流月类 ====================

/**
 * @brief 流月信息（节气月）
 */
struct LiuYue {
    int lunar_month_index;      // 农历月序号（1-12，对应寅月到丑月）
    Pillar pillar;              // 流月干支
    ShiShen gan_shi_shen;       // 天干十神
    ShiShen zhi_shi_shen;       // 地支十神
    std::string start_date;     // 起始日期（公历）
    std::string end_date;       // 结束日期（公历）
    
    LiuYue(int index, const Pillar& p, TianGan day_gan, 
           const std::string& start, const std::string& end)
        : lunar_month_index(index), pillar(p), 
          start_date(start), end_date(end) {
        gan_shi_shen = get_shi_shen(day_gan, p.gan);
        auto cang_gan = get_cang_gan(p.zhi);
        zhi_shi_shen = get_shi_shen(day_gan, cang_gan[0]);
    }
    
    /**
     * @brief 转换为字符串
     */
    std::string to_string() const {
        return std::format("{}月 {} ({})", 
                          lunar_month_index, pillar.to_string(), 
                          start_date);
    }
    
    /**
     * @brief JSON 序列化
     */
    friend void to_json(nlohmann::json& j, const LiuYue& ly) {
        j = {
            {"lunar_month_index", ly.lunar_month_index},
            {"pillar", ly.pillar},
            {"start_date", ly.start_date},
            {"gan_shi_shen", std::string(shi_shen_to_zh(ly.gan_shi_shen))},
            {"zhi_shi_shen", std::string(shi_shen_to_zh(ly.zhi_shi_shen))}
        };
    }
};

/**
 * @brief 获取某年的所有节气月（流月）
 * 
 * @param year 公历年份
 * @param day_gan 日干
 * @return std::vector<LiuYue> 12个节气月列表
 * 
 * 节气月从立春开始，按照十二地支顺序：
 * 正月（寅月）：立春开始
 * 二月（卯月）：惊蛰开始
 * 三月（辰月）：清明开始
 * 四月（巳月）：立夏开始
 * 五月（午月）：芒种开始
 * 六月（未月）：小暑开始
 * 七月（申月）：立秋开始
 * 八月（酉月）：白露开始
 * 九月（戌月）：寒露开始
 * 十月（亥月）：立冬开始
 * 十一月（子月）：大雪开始
 * 十二月（丑月）：小寒开始
 */
inline std::vector<LiuYue> get_liu_yue_of_year(int year, TianGan day_gan) {
    std::vector<LiuYue> result;
    result.reserve(12);
    
    // 节气索引（tyme库中的24节气索引，0=冬至）
    // 寅月从立春开始（索引3），每个月相差2（节+气）
    const int jie_qi_indices[] = {
        3,   // 寅月（正月）：立春（索引3）
        5,   // 卯月（二月）：惊蛰（索引5）
        7,   // 辰月（三月）：清明（索引7）
        9,   // 巳月（四月）：立夏（索引9）
        11,  // 午月（五月）：芒种（索引11）
        13,  // 未月（六月）：小暑（索引13）
        15,  // 申月（七月）：立秋（索引15）
        17,  // 酉月（八月）：白露（索引17）
        19,  // 戌月（九月）：寒露（索引19）
        21,  // 亥月（十月）：立冬（索引21）
        23,  // 子月（十一月）：大雪（索引23）
        1    // 丑月（十二月）：小寒（索引1，需要用下一年）
    };
    
    for (int i = 0; i < 12; ++i) {
        int term_index = jie_qi_indices[i];
        int term_year = year;
        
        // 丑月的小寒在下一年1月
        if (i == 11) {
            term_year = year + 1;
        }
        
        // 获取节气
        auto solar_term = tyme::SolarTerm::from_index(term_year, term_index);
        auto term_time = solar_term.get_julian_day().get_solar_time();
        
        // 使用节气后的某一天获取该月的八字月柱
        auto month_time = term_time.next(10); // 节气后10天
        auto lunar_hour = month_time.get_lunar_hour();
        auto eight_char = lunar_hour.get_eight_char();
        auto month_cycle = eight_char.get_month();
        
        // 获取节气月的干支
        std::string gan_name = month_cycle.get_heaven_stem().get_name();
        std::string zhi_name = month_cycle.get_earth_branch().get_name();
        Pillar month_pillar(gan_name, zhi_name);
        
        // 格式化起始日期（只显示起始，不显示结束）
        std::string start_date = std::format("{}月{}日起", 
                                            term_time.get_month(), 
                                            term_time.get_day());
        
        result.emplace_back(i + 1, month_pillar, day_gan, start_date, "");
    }
    
    return result;
}

// ==================== 流日类 ====================

/**
 * @brief 流日信息
 */
struct LiuRi {
    int year;                   // 公历年份
    int month;                  // 公历月份
    int day;                    // 公历日
    Pillar pillar;              // 流日干支
    ShiShen gan_shi_shen;       // 天干十神
    ShiShen zhi_shi_shen;       // 地支十神
    
    LiuRi(int y, int m, int d, const Pillar& p, TianGan day_gan)
        : year(y), month(m), day(d), pillar(p) {
        gan_shi_shen = get_shi_shen(day_gan, p.gan);
        auto cang_gan = get_cang_gan(p.zhi);
        zhi_shi_shen = get_shi_shen(day_gan, cang_gan[0]);
    }
    
    /**
     * @brief 转换为字符串
     */
    std::string to_string() const {
        return std::format("{}年{}月{}日 {}", year, month, day, pillar.to_string());
    }
    
    /**
     * @brief JSON 序列化
     */
    friend void to_json(nlohmann::json& j, const LiuRi& lr) {
        j = {
            {"year", lr.year},
            {"month", lr.month},
            {"day", lr.day},
            {"pillar", lr.pillar},
            {"gan_shi_shen", std::string(shi_shen_to_zh(lr.gan_shi_shen))},
            {"zhi_shi_shen", std::string(shi_shen_to_zh(lr.zhi_shi_shen))}
        };
    }
};

/**
 * @brief 创建流日
 * 
 * @param year 公历年份
 * @param month 公历月份
 * @param day 公历日
 * @param day_gan 日干
 * @return LiuRi 流日对象
 */
inline LiuRi create_liu_ri(int year, int month, int day, TianGan day_gan) {
    // 从年月日获取干支
    auto bazi = BaZiBase::BaZi::from_solar(year, month, day, 12);
    
    return LiuRi(year, month, day, bazi.day, day_gan);
}

// ==================== 流时类 ====================

/**
 * @brief 流时信息
 */
struct LiuShi {
    int hour;                   // 时辰（0-23）
    Pillar pillar;              // 流时干支
    ShiShen gan_shi_shen;       // 天干十神
    ShiShen zhi_shi_shen;       // 地支十神
    
    LiuShi(int h, const Pillar& p, TianGan day_gan)
        : hour(h), pillar(p) {
        gan_shi_shen = get_shi_shen(day_gan, p.gan);
        auto cang_gan = get_cang_gan(p.zhi);
        zhi_shi_shen = get_shi_shen(day_gan, cang_gan[0]);
    }
    
    /**
     * @brief 转换为字符串
     */
    std::string to_string() const {
        return std::format("{}时 {}", hour, pillar.to_string());
    }
    
    /**
     * @brief JSON 序列化
     */
    friend void to_json(nlohmann::json& j, const LiuShi& ls) {
        j = {
            {"hour", ls.hour},
            {"pillar", ls.pillar},
            {"gan_shi_shen", std::string(shi_shen_to_zh(ls.gan_shi_shen))},
            {"zhi_shi_shen", std::string(shi_shen_to_zh(ls.zhi_shi_shen))}
        };
    }
};

/**
 * @brief 创建流时
 * 
 * @param year 公历年份
 * @param month 公历月份
 * @param day 公历日
 * @param hour 时辰
 * @param day_gan 日干
 * @return LiuShi 流时对象
 */
inline LiuShi create_liu_shi(int year, int month, int day, int hour, TianGan day_gan) {
    // 从年月日时获取干支
    auto bazi = BaZiBase::BaZi::from_solar(year, month, day, hour);
    
    return LiuShi(hour, bazi.hour, day_gan);
}

// ==================== 完整八字排盘结果 ====================

/**
 * @brief 完整八字排盘结果
 * 
 * 包含八字、大运、流年等所有信息
 */
struct BaZiResult {
    BaZiBase::BaZi ba_zi;           // 四柱八字
    bool is_male;                   // 性别
    int birth_year;                 // 出生年份（公历）
    int birth_month;                // 出生月份（公历）
    int birth_day;                  // 出生日（公历）
    int birth_hour;                 // 出生时辰
    int birth_minute;               // 出生分钟
    int birth_second;               // 出生秒
    // 农历日期信息
    int lunar_year;                 // 农历年份
    int lunar_month;                // 农历月份
    int lunar_day;                  // 农历日
    DaYunSystem da_yun_system;      // 大运系统
    
    BaZiResult(const BaZiBase::BaZi& bz, bool male, int by, int bm, int bd, int bh, 
               int bmin = 0, int bsec = 0, int ly = 0, int lm = 0, int ld = 0)
        : ba_zi(bz), is_male(male), birth_year(by), birth_month(bm), 
          birth_day(bd), birth_hour(bh), birth_minute(bmin), birth_second(bsec),
          lunar_year(ly), lunar_month(lm), lunar_day(ld),
          da_yun_system(bz, male, by, bm, bd, bh, bmin, bsec) {}
    
    /**
     * @brief 获取指定年份的流年
     */
    LiuNian get_liu_nian(int year) const {
        return create_liu_nian(year, birth_year, ba_zi.day.gan);
    }
    
    /**
     * @brief 获取指定年份的所有流月（节气月）
     */
    std::vector<LiuYue> get_liu_yue_list(int year) const {
        return get_liu_yue_of_year(year, ba_zi.day.gan);
    }
    
    /**
     * @brief 获取指定日期的流日
     */
    LiuRi get_liu_ri(int year, int month, int day) const {
        return create_liu_ri(year, month, day, ba_zi.day.gan);
    }
    
    /**
     * @brief 获取指定时辰的流时
     */
    LiuShi get_liu_shi(int year, int month, int day, int hour) const {
        return create_liu_shi(year, month, day, hour, ba_zi.day.gan);
    }
    
    /**
     * @brief 获取当前年龄的大运
     */
    std::optional<DaYun> get_current_da_yun(int age) const {
        return da_yun_system.get_da_yun_by_age(age);
    }
    
    /**
     * @brief 获取童限详细信息
     * 
     * 返回完整的起运信息，包括精确的年月日时分
     */
    DaYunSystem::ChildLimitDetail get_child_limit_detail() const {
        return da_yun_system.get_child_limit_detail();
    }
    
    /**
     * @brief 获取 tyme 库的大运对象
     * 
     * @param index 大运索引（0开始）
     * @return tyme::DecadeFortune 对象，可访问更多信息
     */
    tyme::DecadeFortune get_tyme_decade_fortune(int index) const {
        return da_yun_system.get_tyme_decade_fortune(index);
    }
    
    /**
     * @brief 获取所有 tyme 库的大运对象
     * 
     * @param count 大运数量（默认10个）
     * @return 大运列表
     */
    std::vector<tyme::DecadeFortune> get_all_tyme_decade_fortunes(int count = 10) const {
        return da_yun_system.get_all_tyme_decade_fortunes(count);
    }
    
    /**
     * @brief 获取 tyme 库的小运对象
     * 
     * @param index 小运索引（0开始）
     * @return tyme::Fortune 对象
     */
    tyme::Fortune get_tyme_fortune(int index) const {
        return tyme::Fortune::from_child_limit(da_yun_system.get_child_limit(), index);
    }
    
    /**
     * @brief 获取四柱十神
     */
    std::array<ShiShen, 4> get_si_zhu_shi_shen() const {
        TianGan day_gan = ba_zi.day.gan;
        return {
            get_shi_shen(day_gan, ba_zi.year.gan),
            get_shi_shen(day_gan, ba_zi.month.gan),
            get_shi_shen(day_gan, ba_zi.day.gan),  // 日干比肩
            get_shi_shen(day_gan, ba_zi.hour.gan)
        };
    }
    
    /**
     * @brief 转换为 JSON
     */
    nlohmann::json to_json() const {
        nlohmann::json j;
        j["ba_zi"] = ba_zi;
        j["is_male"] = is_male;
        j["birth_date"] = {
            {"year", birth_year},
            {"month", birth_month},
            {"day", birth_day},
            {"hour", birth_hour}
        };
        
        // 大运
        j["da_yun"] = {
            {"qi_yun_age", da_yun_system.get_qi_yun_age()},
            {"shun_pai", da_yun_system.is_shun_pai()},
            {"list", da_yun_system.get_da_yun_list()}
        };
        
        // 十神
        auto shi_shen_arr = get_si_zhu_shi_shen();
        j["shi_shen"] = {
            {"year", std::string(shi_shen_to_zh(shi_shen_arr[0]))},
            {"month", std::string(shi_shen_to_zh(shi_shen_arr[1]))},
            {"day", std::string(shi_shen_to_zh(shi_shen_arr[2]))},
            {"hour", std::string(shi_shen_to_zh(shi_shen_arr[3]))}
        };
        
        return j;
    }
};

} // namespace ZhouYi::BaZi

