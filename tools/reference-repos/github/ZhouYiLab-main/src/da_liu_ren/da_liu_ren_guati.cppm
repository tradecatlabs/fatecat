/**
 * @file da_liu_ren_guati.cppm
 * @brief 大六壬卦体判定模块
 * 
 * 参考 dalurenpython-master/shipan/guati.py 实现
 */

export module ZhouYi.DaLiuRen.GuaTi;

import ZhouYi.GanZhi;
import ZhouYi.BaZiBase;
import ZhouYi.DaLiuRen;
import std;

export namespace ZhouYi::DaLiuRen::GuaTi {

using namespace ZhouYi::GanZhi;
using namespace ZhouYi::BaZiBase;
using namespace ZhouYi::DaLiuRen;

/**
 * @brief 卦体判定引擎
 */
class GuaTiEngine {
public:
    /**
     * @brief 判定所有卦体
     * 
     * @param result 大六壬排盘结果
     * @return 卦体名称列表
     */
    static std::vector<std::string> judge_all(
        const BaZi& ba_zi,
        DiZhi yue_jiang,
        const TianDiPan& tian_di_pan,
        const SiKe& si_ke,
        const SanChuan& san_chuan
    );

private:
    // ==================== 基础卦体 ====================
    
    /**
     * @brief 伏吟卦：支上神与支相同
     */
    static bool is_fu_yin(const SiKe& si_ke);
    
    /**
     * @brief 返吟卦：支上神与支相冲
     */
    static bool is_fan_yin(const SiKe& si_ke);
    
    // ==================== 吉卦 ====================
    
    /**
     * @brief 龙德卦：初传为月将，太岁支在三传中
     */
    static bool is_long_de(
        const BaZi& ba_zi,
        DiZhi yue_jiang,
        const SanChuan& san_chuan
    );
    
    /**
     * @brief 三奇卦：旬奇在三传中
     */
    static bool is_san_qi(
        const BaZi& ba_zi,
        const SanChuan& san_chuan
    );
    
    /**
     * @brief 六仪卦：旬首在三传中
     */
    static bool is_liu_yi(
        const BaZi& ba_zi,
        const SanChuan& san_chuan
    );
    
    /**
     * @brief 铸印卦：巳上见戌，且巳、戌、卯俱在三传中
     */
    static bool is_zhu_yin(
        const TianDiPan& tian_di_pan,
        const SanChuan& san_chuan
    );
    
    /**
     * @brief 斫轮卦：初传为卯，干上神为卯且干为庚辛，或卯临申酉
     */
    static bool is_zhuo_lun(
        const TianDiPan& tian_di_pan,
        const SiKe& si_ke,
        const SanChuan& san_chuan
    );
    
    /**
     * @brief 轩盖卦（高盖卦）：子、卯、天马（午）俱在三传中
     */
    static bool is_xuan_gai(
        const BaZi& ba_zi,
        const SanChuan& san_chuan
    );
    
    /**
     * @brief 官爵卦：戌在三传，太常在三传，驿马在三传
     */
    static bool is_guan_jue(
        const BaZi& ba_zi,
        const SanChuan& san_chuan
    );
    
    // ==================== 凶卦 ====================
    
    /**
     * @brief 九丑卦：特定干支日，支上神为丑
     */
    static bool is_jiu_chou(const SiKe& si_ke);
    
    /**
     * @brief 罗网卦：辰戌丑未四墓全在四课三传中
     */
    static bool is_luo_wang(
        const SiKe& si_ke,
        const SanChuan& san_chuan
    );
    
    // ==================== 其他卦体 ====================
    
    /**
     * @brief 连珠卦：三传地支连续
     */
    static bool is_lian_zhu(const SanChuan& san_chuan);
    
    /**
     * @brief 连茹卦：三传地支连续递减
     */
    static bool is_lian_ru(const SanChuan& san_chuan);
    
    // ==================== 辅助函数 ====================
    
    /**
     * @brief 计算旬奇
     */
    static DiZhi calc_xun_qi(TianGan day_gan, DiZhi day_zhi);
    
    /**
     * @brief 计算天马（月内天马）
     */
    static DiZhi calc_tian_ma(DiZhi month_zhi);
    
    /**
     * @brief 计算驿马
     */
    static DiZhi calc_yi_ma(DiZhi zhi);
};

} // namespace ZhouYi::DaLiuRen::GuaTi

