// 紫微斗数运限系统模块（接口）
export module ZhouYi.ZiWei.Horoscope;

import std;
import ZhouYi.GanZhi;
import ZhouYi.ZiWei.Constants;
import ZhouYi.ZiWei.Star;
import ZhouYi.ZhMapper;

export namespace ZhouYi::ZiWei {
    using namespace std;

    /**
     * @brief 运限作用域
     */
    enum class Scope {
        Origin,   // 本命盘（地盘）
        Decadal,  // 大限盘（天盘）
        Yearly,   // 流年盘（人盘）
        Monthly,  // 流月盘
        Daily,    // 流日盘
        Hourly    // 流时盘
    };

    /**
     * @brief 大限数据结构（10年一大限）
     */
    struct DaXianData {
        int start_age;           // 起始年龄
        int end_age;             // 结束年龄
        int gong_index;          // 所在宫位索引
        TianGan tian_gan;        // 大限天干
        DiZhi di_zhi;            // 大限地支
        array<string, 4> si_hua; // 大限四化星（禄权科忌）
        
        string to_string() const;
    };

    /**
     * @brief 小限数据结构（虚岁对应的宫位）
     */
    struct XiaoXianData {
        int age;            // 虚岁
        int gong_index;     // 所在宫位索引
        
        string to_string() const;
    };

    /**
     * @brief 流年数据结构
     */
    struct LiuNianData {
        int year;                // 公历年份
        TianGan tian_gan;        // 流年天干
        DiZhi di_zhi;            // 流年地支
        int gong_index;          // 所在宫位索引（流年地支对应）
        array<string, 4> si_hua; // 流年四化星（禄权科忌）
        
        string to_string() const;
    };

    /**
     * @brief 流月数据结构
     */
    struct LiuYueData {
        int month;               // 农历月份
        TianGan tian_gan;        // 流月天干
        DiZhi di_zhi;            // 流月地支
        int gong_index;          // 所在宫位索引
        array<string, 4> si_hua; // 流月四化星
        
        string to_string() const;
    };

    /**
     * @brief 流日数据结构
     */
    struct LiuRiData {
        int day;                 // 农历日
        TianGan tian_gan;        // 流日天干
        DiZhi di_zhi;            // 流日地支
        int gong_index;          // 所在宫位索引
        array<string, 4> si_hua; // 流日四化星
        
        string to_string() const;
    };

    /**
     * @brief 流时数据结构
     */
    struct LiuShiData {
        DiZhi shi_chen;          // 时辰地支
        TianGan tian_gan;        // 流时天干
        DiZhi di_zhi;            // 流时地支
        int gong_index;          // 所在宫位索引
        array<string, 4> si_hua; // 流时四化星
        
        string to_string() const;
    };

    /**
     * @brief 运限星耀系统
     * 大限、流年、流月、流日、流时的魁钺昌曲禄羊陀马鸾喜
     */
    struct HoroscopeStarData {
        int gong_index;          // 宫位索引
        vector<string> stars;    // 流耀星名称列表
    };

    /**
     * @brief 安大限诀
     * 
     * 口诀：
     * 大限由命宫起，阳男阴女顺行，
     * 阴男阳女逆行，每十年过一宫限。
     * 
     * @param ming_index 命宫索引
     * @param wu_xing_ju 五行局
     * @param is_male 是否为男性
     * @param year_zhi 年支
     * @return 12个大限数据
     */
    array<DaXianData, 12> arrange_da_xian(
        int ming_index,
        WuXingJu wu_xing_ju,
        bool is_male,
        DiZhi year_zhi
    );

    /**
     * @brief 获取指定虚岁的小限宫位
     * 
     * 口诀：
     * 小限从寅宫起1岁，阳男阴女顺行，
     * 阴男阳女逆行，每岁一宫。
     * 
     * @param age 虚岁
     * @param is_male 是否为男性
     * @param year_zhi 年支
     * @return 小限数据
     */
    XiaoXianData get_xiao_xian(int age, bool is_male, DiZhi year_zhi);

    /**
     * @brief 获取流年宫位
     * 
     * 算法：流年以地支定宫，如甲子年在子宫
     * 
     * @param year_gan 流年天干
     * @param year_zhi 流年地支
     * @param ming_index 命宫索引
     * @return 流年数据
     */
    LiuNianData get_liu_nian(
        int year,
        TianGan year_gan,
        DiZhi year_zhi,
        int ming_index
    );

    /**
     * @brief 获取流月宫位
     * 
     * 算法：
     * 1. 从流年地支起命宫，逆数到生月所在宫位
     * 2. 再从该宫位起正月，顺数到流月
     * 
     * @param lunar_month 农历月份
     * @param birth_month 出生月份
     * @param year_zhi 流年地支
     * @param ming_index 命宫索引
     * @return 流月数据
     */
    LiuYueData get_liu_yue(
        int lunar_month,
        int birth_month,
        TianGan month_gan,
        DiZhi month_zhi,
        DiZhi year_zhi,
        int ming_index
    );

    /**
     * @brief 获取流日宫位
     * 
     * 算法：从流月宫位起初一，顺数到流日
     * 
     * @param lunar_day 农历日
     * @param day_gan 流日天干
     * @param day_zhi 流日地支
     * @param liu_yue_index 流月宫位索引
     * @return 流日数据
     */
    LiuRiData get_liu_ri(
        int lunar_day,
        TianGan day_gan,
        DiZhi day_zhi,
        int liu_yue_index
    );

    /**
     * @brief 获取流时宫位
     * 
     * 算法：从流日宫位起子时，顺数到流时
     * 
     * @param hour_zhi 时辰地支
     * @param hour_gan 流时天干
     * @param liu_ri_index 流日宫位索引
     * @return 流时数据
     */
    LiuShiData get_liu_shi(
        DiZhi hour_zhi,
        TianGan hour_gan,
        int liu_ri_index
    );

    /**
     * @brief 获取运限流耀星（魁钺昌曲禄羊陀马鸾喜）
     * 
     * @param gan 天干
     * @param zhi 地支
     * @param scope 作用域
     * @return 流耀星数据（12个宫位）
     */
    array<HoroscopeStarData, 12> get_horoscope_stars(
        TianGan gan,
        DiZhi zhi,
        Scope scope
    );

    /**
     * @brief 综合运限结果
     */
    struct HoroscopeResult {
        DaXianData da_xian;              // 大限
        XiaoXianData xiao_xian;          // 小限
        LiuNianData liu_nian;            // 流年
        LiuYueData liu_yue;              // 流月
        LiuRiData liu_ri;                // 流日
        LiuShiData liu_shi;              // 流时
        
        // 各运限的流耀星
        array<HoroscopeStarData, 12> da_xian_stars;  // 大限星（运魁、运钺...）
        array<HoroscopeStarData, 12> liu_nian_stars; // 流年星（流魁、流钺...）
        array<HoroscopeStarData, 12> liu_yue_stars;  // 流月星（月魁、月钺...）
        array<HoroscopeStarData, 12> liu_ri_stars;   // 流日星（日魁、日钺...）
        array<HoroscopeStarData, 12> liu_shi_stars;  // 流时星（时魁、时钺...）
        
        string to_string() const;
    };

} // namespace ZhouYi::ZiWei

