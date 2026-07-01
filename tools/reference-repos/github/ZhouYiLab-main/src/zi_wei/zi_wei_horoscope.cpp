// 紫微斗数运限系统模块（实现）
module ZhouYi.ZiWei.Horoscope;

import ZhouYi.GanZhi;
import ZhouYi.ZiWei.Constants;
import ZhouYi.ZiWei.Star;
import fmt;
import std;
import ZhouYi.ZhMapper;

namespace ZhouYi::ZiWei {
    using namespace std;
    using namespace ZhouYi::GanZhi;
    using namespace ZhouYi::Mapper;

    // ============= 数据结构 to_string 实现 =============

    string DaXianData::to_string() const {
        return fmt::format("大限 {}~{} 岁 [{}-{}宫] 四化: {}",
            start_age, end_age,
            string(GanZhi::Mapper::to_zh(tian_gan)),
            string(GanZhi::Mapper::to_zh(di_zhi)),
            fmt::join(si_hua, " "));
    }

    string XiaoXianData::to_string() const {
        return fmt::format("小限 {} 岁 [第{}宫]", age, gong_index);
    }

    string LiuNianData::to_string() const {
        return fmt::format("流年 {} 年 [{}-{}宫] 四化: {}",
            year,
            string(GanZhi::Mapper::to_zh(tian_gan)),
            string(GanZhi::Mapper::to_zh(di_zhi)),
            fmt::join(si_hua, " "));
    }

    string LiuYueData::to_string() const {
        return fmt::format("流月 {} 月 [{}-{}宫] 四化: {}",
            month,
            string(GanZhi::Mapper::to_zh(tian_gan)),
            string(GanZhi::Mapper::to_zh(di_zhi)),
            fmt::join(si_hua, " "));
    }

    string LiuRiData::to_string() const {
        return fmt::format("流日 {} 日 [{}-{}宫] 四化: {}",
            day,
            string(GanZhi::Mapper::to_zh(tian_gan)),
            string(GanZhi::Mapper::to_zh(di_zhi)),
            fmt::join(si_hua, " "));
    }

    string LiuShiData::to_string() const {
        return fmt::format("流时 {}时 [{}-{}宫] 四化: {}",
            string(GanZhi::Mapper::to_zh(shi_chen)),
            string(GanZhi::Mapper::to_zh(tian_gan)),
            string(GanZhi::Mapper::to_zh(di_zhi)),
            fmt::join(si_hua, " "));
    }

    string HoroscopeResult::to_string() const {
        return fmt::format("{}\n{}\n{}\n{}\n{}\n{}",
            da_xian.to_string(),
            xiao_xian.to_string(),
            liu_nian.to_string(),
            liu_yue.to_string(),
            liu_ri.to_string(),
            liu_shi.to_string());
    }

    // ============= 大限算法 =============

    /**
     * @brief 安大限诀
     * 
     * 口诀：
     * 大限由命宫起，阳男阴女顺行，
     * 阴男阳女逆行，每十年过一宫限。
     */
    array<DaXianData, 12> arrange_da_xian(
        int ming_index,
        WuXingJu wu_xing_ju,
        bool is_male,
        DiZhi year_zhi
    ) {
        array<DaXianData, 12> result{};
        
        // 起运年龄（五行局数）
        int qi_yun_age = static_cast<int>(wu_xing_ju);
        
        // 判断顺逆：阳男阴女顺行，阴男阳女逆行
        int zhi_idx = static_cast<int>(year_zhi);
        bool yang_zhi = (zhi_idx % 2 == 0);
        bool shun_xing = (is_male == yang_zhi);
        
        for (int i = 0; i < 12; ++i) {
            int idx = shun_xing ? fix_index(ming_index + i) : fix_index(ming_index - i);
            int start_age = qi_yun_age + 10 * i;
            int end_age = start_age + 9;
            
            // 计算大限天干（从甲开始，根据流转方向递增或递减）
            int gan_offset = shun_xing ? i : -i;
            int gan_idx = (gan_offset + 10) % 10;
            TianGan start_gan = static_cast<TianGan>(gan_idx);
            
            result[idx] = DaXianData{
                .start_age = start_age,
                .end_age = end_age,
                .gong_index = idx,
                .tian_gan = start_gan,
                .di_zhi = static_cast<DiZhi>(idx),
                .si_hua = {}  // 需要根据大限天干获取四化
            };
            
            // 获取大限四化
            auto si_hua_map = get_si_hua_table(start_gan);
            int si_hua_idx = 0;
            for (const auto& [star, si_hua_type] : si_hua_map) {
                if (si_hua_idx < 4) {
                    result[idx].si_hua[si_hua_idx++] = string(to_zh(star));
                }
            }
        }
        
        return result;
    }

    // ============= 小限算法 =============

    /**
     * @brief 获取小限宫位
     * 
     * 口诀：
     * 小限从寅宫起1岁，阳男阴女顺行，
     * 阴男阳女逆行，每岁一宫。
     * 
     * 童限特殊规则（1-6岁）：
     * 一命二财三疾厄，四岁夫妻五福德，
     * 六岁事业为童限，专就宫垣视吉凶。
     */
    XiaoXianData get_xiao_xian(int age, bool is_male, DiZhi year_zhi) {
        // 童限特殊处理（1-6岁）
        if (age >= 1 && age <= 6) {
            // 命宫、财帛、疾厄、夫妻、福德、官禄
            constexpr array<int, 6> tong_xian_gong = {0, 1, 8, 3, 10, 6};
            return XiaoXianData{
                .age = age,
                .gong_index = tong_xian_gong[age - 1]
            };
        }
        
        // 正常小限计算
        int zhi_idx = static_cast<int>(year_zhi);
        bool yang_zhi = (zhi_idx % 2 == 0);
        bool shun_xing = (is_male == yang_zhi);
        
        // 从寅宫（索引0）起1岁
        int xiao_xian_index = shun_xing 
            ? fix_index(0 + (age - 1)) 
            : fix_index(0 - (age - 1));
        
        return XiaoXianData{
            .age = age,
            .gong_index = xiao_xian_index
        };
    }

    // ============= 流年算法 =============

    /**
     * @brief 获取流年宫位
     * 
     * 算法：流年以地支定宫，如甲子年在子宫
     */
    LiuNianData get_liu_nian(
        int year,
        TianGan year_gan,
        DiZhi year_zhi,
        int ming_index
    ) {
        // 流年地支对应宫位索引（寅0卯1辰2...）
        int zhi_idx = static_cast<int>(year_zhi);
        // 转换为从寅宫开始的索引
        int liu_nian_index = (zhi_idx + 10) % 12;  // 子=10, 丑=11, 寅=0...
        
        // 获取流年四化
        auto si_hua_map = get_si_hua_table(year_gan);
        array<string, 4> si_hua = {};
        int si_hua_idx = 0;
        for (const auto& [star, si_hua_type] : si_hua_map) {
            if (si_hua_idx < 4) {
                si_hua[si_hua_idx++] = string(to_zh(star));
            }
        }
        
        return LiuNianData{
            .year = year,
            .tian_gan = year_gan,
            .di_zhi = year_zhi,
            .gong_index = liu_nian_index,
            .si_hua = si_hua
        };
    }

    // ============= 流月算法 =============

    /**
     * @brief 获取流月宫位
     * 
     * 算法：
     * 1. 从流年地支起命宫，逆数到生月所在宫位
     * 2. 再从该宫位起正月，顺数到流月
     */
    LiuYueData get_liu_yue(
        int lunar_month,
        int birth_month,
        TianGan month_gan,
        DiZhi month_zhi,
        DiZhi year_zhi,
        int ming_index
    ) {
        int year_zhi_idx = static_cast<int>(year_zhi);
        int liu_nian_index = (year_zhi_idx + 10) % 12;
        
        // 从流年宫位逆数到生月
        int birth_month_index = fix_index(liu_nian_index - (birth_month - 1));
        
        // 从生月宫位顺数到当前月
        int liu_yue_index = fix_index(birth_month_index + (lunar_month - 1));
        
        // 获取流月四化
        auto si_hua_map = get_si_hua_table(month_gan);
        array<string, 4> si_hua = {};
        int si_hua_idx = 0;
        for (const auto& [star, si_hua_type] : si_hua_map) {
            if (si_hua_idx < 4) {
                si_hua[si_hua_idx++] = string(to_zh(star));
            }
        }
        
        return LiuYueData{
            .month = lunar_month,
            .tian_gan = month_gan,
            .di_zhi = month_zhi,
            .gong_index = liu_yue_index,
            .si_hua = si_hua
        };
    }

    // ============= 流日算法 =============

    /**
     * @brief 获取流日宫位
     * 
     * 算法：从流月宫位起初一，顺数到流日
     */
    LiuRiData get_liu_ri(
        int lunar_day,
        TianGan day_gan,
        DiZhi day_zhi,
        int liu_yue_index
    ) {
        // 从流月宫位起初一，顺数到流日
        int liu_ri_index = fix_index(liu_yue_index + (lunar_day - 1));
        
        // 获取流日四化
        auto si_hua_map = get_si_hua_table(day_gan);
        array<string, 4> si_hua = {};
        int si_hua_idx = 0;
        for (const auto& [star, si_hua_type] : si_hua_map) {
            if (si_hua_idx < 4) {
                si_hua[si_hua_idx++] = string(to_zh(star));
            }
        }
        
        return LiuRiData{
            .day = lunar_day,
            .tian_gan = day_gan,
            .di_zhi = day_zhi,
            .gong_index = liu_ri_index,
            .si_hua = si_hua
        };
    }

    // ============= 流时算法 =============

    /**
     * @brief 获取流时宫位
     * 
     * 算法：从流日宫位起子时，顺数到流时
     */
    LiuShiData get_liu_shi(
        DiZhi hour_zhi,
        TianGan hour_gan,
        int liu_ri_index
    ) {
        // 从流日宫位起子时，顺数到流时
        int hour_idx = static_cast<int>(hour_zhi);
        int liu_shi_index = fix_index(liu_ri_index + hour_idx);
        
        // 获取流时四化
        auto si_hua_map = get_si_hua_table(hour_gan);
        array<string, 4> si_hua = {};
        int si_hua_idx = 0;
        for (const auto& [star, si_hua_type] : si_hua_map) {
            if (si_hua_idx < 4) {
                si_hua[si_hua_idx++] = string(to_zh(star));
            }
        }
        
        return LiuShiData{
            .shi_chen = hour_zhi,
            .tian_gan = hour_gan,
            .di_zhi = hour_zhi,
            .gong_index = liu_shi_index,
            .si_hua = si_hua
        };
    }

    // ============= 运限流耀星算法 =============

    /**
     * @brief 获取运限流耀星（魁钺昌曲禄羊陀马鸾喜）
     * 
     * 根据不同作用域返回对应的流耀星名称
     */
    array<HoroscopeStarData, 12> get_horoscope_stars(
        TianGan gan,
        DiZhi zhi,
        Scope scope
    ) {
        array<HoroscopeStarData, 12> result{};
        
        // 初始化每个宫位的星耀列表
        for (int i = 0; i < 12; ++i) {
            result[i].gong_index = i;
            result[i].stars = {};
        }
        
        // 获取各种星耀的位置
        auto [kui_idx, yue_idx] = get_kui_yue_index(gan);
        auto [chang_idx, qu_idx] = get_chang_qu_index(zhi);
        int lu_idx = get_lu_cun_index(gan);
        auto [yang_idx, tuo_idx] = get_yang_tuo_index(lu_idx);
        auto [hong_luan_idx, tian_xi_idx] = get_hong_luan_tian_xi_index(zhi);
        
        // 天马索引（按地支）
        int ma_idx = 0;
        if (zhi == DiZhi::Yin || zhi == DiZhi::Wu || zhi == DiZhi::Xu) {
            ma_idx = 6; // 申
        } else if (zhi == DiZhi::Shen || zhi == DiZhi::Zi || zhi == DiZhi::Chen) {
            ma_idx = 0; // 寅
        } else if (zhi == DiZhi::Si || zhi == DiZhi::You || zhi == DiZhi::Chou) {
            ma_idx = 9; // 亥
        } else { // 亥卯未
            ma_idx = 3; // 巳
        }
        
        // 根据作用域确定星耀前缀
        string prefix;
        switch (scope) {
            case Scope::Origin:
                prefix = "";
                break;
            case Scope::Decadal:
                prefix = "运";
                break;
            case Scope::Yearly:
                prefix = "流";
                // 流年还有年解
                result[get_nian_jie_index(zhi)].stars.push_back("年解");
                break;
            case Scope::Monthly:
                prefix = "月";
                break;
            case Scope::Daily:
                prefix = "日";
                break;
            case Scope::Hourly:
                prefix = "时";
                break;
        }
        
        // 添加流耀星
        result[kui_idx].stars.push_back(prefix + "魁");
        result[yue_idx].stars.push_back(prefix + "钺");
        result[chang_idx].stars.push_back(prefix + "昌");
        result[qu_idx].stars.push_back(prefix + "曲");
        result[lu_idx].stars.push_back(prefix + "禄");
        result[yang_idx].stars.push_back(prefix + "羊");
        result[tuo_idx].stars.push_back(prefix + "陀");
        result[ma_idx].stars.push_back(prefix + "马");
        result[hong_luan_idx].stars.push_back(prefix + "鸾");
        result[tian_xi_idx].stars.push_back(prefix + "喜");
        
        return result;
    }

} // namespace ZhouYi::ZiWei

