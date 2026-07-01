// 紫微斗数宫位计算模块
export module ZhouYi.ZiWei.Palace;

import std;
import ZhouYi.GanZhi;
import ZhouYi.ZiWei.Constants;
import ZhouYi.ZhMapper;
import ZhouYi.tyme;
import fmt;

export namespace ZhouYi::ZiWei {
    using namespace std;
    using namespace ZhouYi::GanZhi;
    using namespace ZhouYi::Mapper;

    /**
     * @brief 定五行局法（以命宫天干地支而定）
     * 
     * 纳音五行计算取数巧记口诀：
     * - 甲乙丙丁一到五，子丑午未一来数，
     * - 寅卯申酉二上走，辰巳戌亥三为足。
     * - 干支相加多减五，五行木金水火土。
     * 
     * @param gan 命宫天干
     * @param zhi 命宫地支
     * @return 五行局
     */
    constexpr WuXingJu get_wu_xing_ju(TianGan gan, DiZhi zhi) {
        // 天干取数：甲乙=1, 丙丁=2, 戊己=3, 庚辛=4, 壬癸=5
        int gan_num = static_cast<int>(gan) / 2 + 1;
        
        // 地支取数：子午丑未=1, 寅申卯酉=2, 辰戌巳亥=3
        int zhi_idx = static_cast<int>(zhi);
        int zhi_num;
        if (zhi_idx == 0 || zhi_idx == 6 || zhi_idx == 1 || zhi_idx == 7) {
            zhi_num = 1; // 子午丑未
        } else if (zhi_idx == 2 || zhi_idx == 8 || zhi_idx == 3 || zhi_idx == 9) {
            zhi_num = 2; // 寅申卯酉
        } else {
            zhi_num = 3; // 辰戌巳亥
        }
        
        // 干支相加，超过5者减去5
        int sum = gan_num + zhi_num;
        while (sum > 5) {
            sum -= 5;
        }
        
        // 1木3局 2金4局 3水2局 4火6局 5土5局
        const WuXingJu ju_table[] = {
            WuXingJu::MuSanJu,    // 1
            WuXingJu::JinSiJu,    // 2
            WuXingJu::ShuiErJu,   // 3
            WuXingJu::HuoLiuJu,   // 4
            WuXingJu::TuWuJu      // 5
        };
        
        return ju_table[sum - 1];
    }

    /**
     * @brief 获取命宫和身宫数据
     * 
     * 安命身宫诀：
     * - 寅起正月，顺数至生月，逆数生时为命宫。
     * - 寅起正月，顺数至生月，顺数生时为身宫。
     * 
     * @param lunar_month 农历月份（1-12）
     * @param hour_zhi 时辰地支
     * @return pair<命宫索引, 身宫索引>（以寅宫为0）
     */
    constexpr pair<int, int> get_ming_shen_index(int lunar_month, DiZhi hour_zhi) {
        // 寅宫为起始点（索引0）
        // 从寅开始顺数到生月
        int month_index = lunar_month - 1;
        
        // 时辰地支索引
        int hour_index = static_cast<int>(hour_zhi);
        
        // 命宫：从生月逆数到时辰
        // 由于寅为地支第3位（0-based为2），所以需要调整
        // 从寅（宫位0）开始，顺数lunar_month-1得到月宫位
        // 再从月宫位逆数hour_index得到命宫
        int ming_index = fix_index(month_index - hour_index);
        
        // 身宫：从生月顺数到时辰
        int shen_index = fix_index(month_index + hour_index);
        
        return {ming_index, shen_index};
    }

    /**
     * @brief 获取命宫天干
     * 
     * 使用五虎遁从年干算起
     * 
     * @param year_gan 年干
     * @param ming_index 命宫索引（以寅宫为0）
     * @return 命宫天干
     */
    constexpr TianGan get_ming_gan(TianGan year_gan, int ming_index) {
        // 五虎遁：从年干定寅月天干
        // 甲己丙寅头，乙庚戊寅头，丙辛庚寅头，丁壬壬寅头，戊癸甲寅头
        const TianGan yin_gan_table[] = {
            TianGan::Bing,  // 甲年
            TianGan::Wu,    // 乙年
            TianGan::Geng,  // 丙年
            TianGan::Ren,   // 丁年
            TianGan::Jia,   // 戊年
            TianGan::Bing,  // 己年
            TianGan::Wu,    // 庚年
            TianGan::Geng,  // 辛年
            TianGan::Ren,   // 壬年
            TianGan::Jia    // 癸年
        };
        
        TianGan yin_gan = yin_gan_table[static_cast<int>(year_gan)];
        
        // 从寅宫天干顺数到命宫
        int ming_gan_idx = (static_cast<int>(yin_gan) + ming_index) % 10;
        return static_cast<TianGan>(ming_gan_idx);
    }

    /**
     * @brief 获取命宫地支
     * 
     * @param ming_index 命宫索引（以寅宫为0）
     * @return 命宫地支
     */
    constexpr DiZhi get_ming_zhi(int ming_index) {
        // 寅=0, 卯=1, ... 丑=11
        // 地支从寅开始：寅卯辰巳午未申酉戌亥子丑
        const DiZhi zhi_table[] = {
            DiZhi::Yin, DiZhi::Mao, DiZhi::Chen, DiZhi::Si,
            DiZhi::Wu, DiZhi::Wei, DiZhi::Shen, DiZhi::You,
            DiZhi::Xu, DiZhi::Hai, DiZhi::Zi, DiZhi::Chou
        };
        return zhi_table[ming_index];
    }

    /**
     * @brief 宫位数据结构
     */
    struct GongWeiData {
        GongWei gong_wei;           // 宫位类型
        TianGan tian_gan;           // 天干
        DiZhi di_zhi;               // 地支
        bool is_body_palace;        // 是否为身宫
        bool is_ming_palace;        // 是否为命宫
        WuXingJu wu_xing_ju;        // 五行局（仅命宫有效）
        
        // 宫位索引（以寅宫为0）
        int index;
        
        string to_string() const {
            return fmt::format("{} ({}{})", 
                string(to_zh(gong_wei)),
                string(GanZhi::Mapper::to_zh(tian_gan)),
                string(GanZhi::Mapper::to_zh(di_zhi))
            );
        }
    };

    /**
     * @brief 排布十二宫
     * 
     * @param year_gan 年干
     * @param lunar_month 农历月份
     * @param hour_zhi 时辰地支
     * @return 从寅宫开始的十二宫数据
     */
    inline vector<GongWeiData> arrange_twelve_palaces(
        TianGan year_gan, 
        int lunar_month, 
        DiZhi hour_zhi
    ) {
        vector<GongWeiData> palaces(12);
        
        // 获取命宫和身宫索引
        auto [ming_index, shen_index] = get_ming_shen_index(lunar_month, hour_zhi);
        
        // 获取寅宫天干（五虎遁）
        // 甲己丙寅头，乙庚戊寅头，丙辛庚寅头，丁壬壬寅头，戊癸甲寅头
        const TianGan yin_gan_table[] = {
            TianGan::Bing,  // 甲年
            TianGan::Wu,    // 乙年
            TianGan::Geng,  // 丙年
            TianGan::Ren,   // 丁年
            TianGan::Jia,   // 戊年
            TianGan::Bing,  // 己年
            TianGan::Wu,    // 庚年
            TianGan::Geng,  // 辛年
            TianGan::Ren,   // 壬年
            TianGan::Jia    // 癸年
        };
        TianGan yin_gan = yin_gan_table[static_cast<int>(year_gan)];
        
        // 获取命宫天干地支
        TianGan ming_gan = get_ming_gan(year_gan, ming_index);
        DiZhi ming_zhi = get_ming_zhi(ming_index);
        
        // 计算五行局
        WuXingJu wu_xing_ju = get_wu_xing_ju(ming_gan, ming_zhi);
        
        // 填充十二宫数据
        // 宫位名称从命宫开始逆时针排列（紫微斗数标准顺序）
        // 命宫 → 父母 → 福德 → 田宅 → 官禄 → 奴仆 → 迁移 → 疾厄 → 财帛 → 子女 → 夫妻 → 兄弟
        const GongWei gong_wei_order[] = {
            GongWei::MingGong, GongWei::FuMuGong, GongWei::FuDeGong,
            GongWei::TianZhaiGong, GongWei::GuanLuGong, GongWei::NuPuGong,
            GongWei::QianYiGong, GongWei::JiBingGong, GongWei::CaiBoGong,
            GongWei::ZiNvGong, GongWei::FuQiGong, GongWei::XiongDiGong
        };
        
        for (int i = 0; i < 12; ++i) {
            // 宫位在星盘中的实际索引
            int palace_index = i;
            
            // 该宫位相对于命宫的偏移
            int offset_from_ming = fix_index(i - ming_index);
            
            // 该宫位的天干（从寅宫天干顺数）
            // 每个宫位的天干 = 寅宫天干 + 宫位索引
            TianGan palace_gan = static_cast<TianGan>(
                (static_cast<int>(yin_gan) + i) % 10
            );
            
            // 该宫位的地支（从寅宫开始）
            DiZhi palace_zhi = get_ming_zhi(i);
            
            // 该宫位的宫名
            GongWei gong_wei = gong_wei_order[offset_from_ming];
            
            palaces[i] = GongWeiData{
                .gong_wei = gong_wei,
                .tian_gan = palace_gan,
                .di_zhi = palace_zhi,
                .is_body_palace = (i == shen_index),
                .is_ming_palace = (i == ming_index),
                .wu_xing_ju = (i == ming_index) ? wu_xing_ju : WuXingJu::ShuiErJu,
                .index = i
            };
        }
        
        return palaces;
    }

} // namespace ZhouYi::ZiWei

