// 紫微斗数星耀定位模块（接口）
export module ZhouYi.ZiWei.Star;

import std;
import ZhouYi.GanZhi;
import ZhouYi.ZiWei.Constants;
import ZhouYi.ZhMapper;
import ZhouYi.tyme;

export namespace ZhouYi::ZiWei {
    using namespace std;
    using namespace ZhouYi::GanZhi;

    /**
     * @brief 星耀数据结构
     */
    struct StarData {
        string name;            // 星耀名称
        LiangDu liang_du;       // 亮度
        int gong_index;         // 所在宫位索引（以寅宫为0）
        optional<SiHua> si_hua; // 四化（可能没有）
        
        string to_string() const;
    };

    /**
     * @brief 安命主星（按命宫地支或年支）
     * 
     * 命主星映射表：
     * - 子→贪狼, 丑→巨门, 寅→禄存, 卯→文曲, 辰→廉贞, 巳→武曲
     * - 午→破军, 未→武曲, 申→廉贞, 酉→文曲, 戌→禄存, 亥→巨门
     * 
     * @param ming_gong_zhi 命宫地支（通用派）或年支（中州派）
     * @return 命主星名称
     */
    string get_ming_zhu_xing(DiZhi ming_gong_zhi);

    /**
     * @brief 安身主星（按年支）
     * 
     * 身主星映射表：
     * - 子/午→火星, 丑/未→天相, 寅/申→天梁
     * - 卯/酉→天同, 辰/戌→文昌, 巳/亥→天机
     * 
     * @param year_zhi 年支
     * @return 身主星名称
     */
    string get_shen_zhu_xing(DiZhi year_zhi);

    /**
     * @brief 起紫微星诀算法
     */
    int get_zi_wei_index(int lunar_day, WuXingJu wu_xing_ju);

    /**
     * @brief 获取天府星索引
     * 
     * 紫微与天府的位置关系规则：
     * - 寅/申：紫府同宫
     * - 子/辰：互换（紫微子则天府辰，紫微辰则天府子）
     * - 丑/卯：互换（紫微丑则天府卯，紫微卯则天府丑）
     * - 巳/亥：对宫
     * - 午/戌：互换（紫微午则天府戌，紫微戌则天府午）
     * - 未/酉：互换（紫微未则天府酉，紫微酉则天府未）
     * 
     * 索引对应（以寅宫为0）：
     * 寅0 卯1 辰2 巳3 午4 未5 申6 酉7 戌8 亥9 子10 丑11
     */
    constexpr int get_tian_fu_index(int zi_wei_index) {
        // 紫微地支索引转换为地支序号（子=0的系统）
        // 寅0→寅2, 卯1→卯3, 辰2→辰4, 巳3→巳5, 午4→午6, 未5→未7
        // 申6→申8, 酉7→酉9, 戌8→戌10, 亥9→亥11, 子10→子0, 丑11→丑1
        
        // 先将宫位索引转为地支（寅=0的系统转为子=0的系统）
        // 寅宫索引0 对应 地支寅(2), 卯宫索引1 对应 地支卯(3), ...
        int zi_wei_zhi = (zi_wei_index + 2) % 12;  // 转换为子=0的地支索引
        
        int tian_fu_zhi;
        switch (zi_wei_zhi) {
            case 2:  // 寅
            case 8:  // 申
                tian_fu_zhi = zi_wei_zhi;  // 同宫
                break;
            case 0:  // 子
                tian_fu_zhi = 4;  // 辰
                break;
            case 4:  // 辰
                tian_fu_zhi = 0;  // 子
                break;
            case 1:  // 丑
                tian_fu_zhi = 3;  // 卯
                break;
            case 3:  // 卯
                tian_fu_zhi = 1;  // 丑
                break;
            case 5:  // 巳
                tian_fu_zhi = 11; // 亥
                break;
            case 11: // 亥
                tian_fu_zhi = 5;  // 巳
                break;
            case 6:  // 午
                tian_fu_zhi = 10; // 戌
                break;
            case 10: // 戌
                tian_fu_zhi = 6;  // 午
                break;
            case 7:  // 未
                tian_fu_zhi = 9;  // 酉
                break;
            case 9:  // 酉
                tian_fu_zhi = 7;  // 未
                break;
            default:
                tian_fu_zhi = zi_wei_zhi;
        }
        
        // 转换回宫位索引（寅=0的系统）
        return (tian_fu_zhi + 10) % 12;  // (x - 2 + 12) % 12 = (x + 10) % 12
    }

    /**
     * @brief 安紫微星系（北斗星系）
     */
    map<ZhuXing, int> arrange_zi_wei_group(int zi_wei_index);

    /**
     * @brief 安天府星系（南斗星系）
     */
    map<ZhuXing, int> arrange_tian_fu_group(int tian_fu_index);

    /**
     * @brief 获取主星亮度表（按宫位地支排序，从寅开始）
     */
    array<LiangDu, 12> get_zhu_xing_liang_du_table(ZhuXing star);

    /**
     * @brief 安左辅右弼（按农历月份）
     */
    constexpr pair<int, int> get_zuo_you_index(int lunar_month);

    /**
     * @brief 安文昌文曲（按时辰）
     */
    constexpr pair<int, int> get_chang_qu_index(DiZhi hour_zhi);

    /**
     * @brief 安天魁天钺（按年干）
     */
    pair<int, int> get_kui_yue_index(TianGan year_gan);

    /**
     * @brief 安禄存（按年干）
     */
    constexpr int get_lu_cun_index(TianGan year_gan);

    /**
     * @brief 安擎羊陀罗（禄前擎羊，禄后陀罗）
     */
    pair<int, int> get_yang_tuo_index(int lu_cun_index);

    /**
     * @brief 安火星铃星（按年支和时辰）
     */
    pair<int, int> get_huo_ling_index(DiZhi year_zhi, DiZhi hour_zhi);

    /**
     * @brief 安地空地劫（按时辰）
     */
    pair<int, int> get_kong_jie_index(DiZhi hour_zhi);

    /**
     * @brief 四化表（年干四化）
     */
    map<ZhuXing, SiHua> get_si_hua_table(TianGan year_gan);

    // ============= 杂耀星定位算法 =============

    /**
     * @brief 安红鸾天喜（按年支）
     */
    pair<int, int> get_hong_luan_tian_xi_index(DiZhi year_zhi);

    /**
     * @brief 安三台八座（按农历日和月份）
     */
    pair<int, int> get_san_tai_ba_zuo_index(int lunar_month, int lunar_day, DiZhi hour_zhi);

    /**
     * @brief 安恩光天贵（按农历日和时辰）
     */
    pair<int, int> get_en_guang_tian_gui_index(int lunar_month, int lunar_day, DiZhi hour_zhi);

    /**
     * @brief 安龙池凤阁（按年支）
     */
    pair<int, int> get_long_chi_feng_ge_index(DiZhi year_zhi);

    /**
     * @brief 安天才天寿（按年支、命宫和身宫索引）
     */
    pair<int, int> get_tian_cai_tian_shou_index(DiZhi year_zhi, int ming_index, int shen_index);

    /**
     * @brief 安台辅封诰（按时辰）
     */
    pair<int, int> get_tai_fu_feng_gao_index(DiZhi hour_zhi);

    /**
     * @brief 安天官天福（按年干）
     */
    pair<int, int> get_tian_guan_tian_fu_index(TianGan year_gan);

    /**
     * @brief 安天厨（按年干）
     */
    int get_tian_chu_index(TianGan year_gan);

    /**
     * @brief 安华盖（按年支）
     */
    int get_hua_gai_index(DiZhi year_zhi);

    /**
     * @brief 安咸池（按年支）
     */
    int get_xian_chi_index(DiZhi year_zhi);

    /**
     * @brief 安孤辰寡宿（按年支）
     */
    pair<int, int> get_gu_chen_gua_su_index(DiZhi year_zhi);

    /**
     * @brief 安蜚廉（按年支）
     */
    int get_fei_lian_index(DiZhi year_zhi);

    /**
     * @brief 安破碎（按年支）
     */
    int get_po_sui_index(DiZhi year_zhi);

    /**
     * @brief 安天刑（按月份）
     */
    int get_tian_xing_index(int lunar_month);

    /**
     * @brief 安天姚（按月份）
     */
    int get_tian_yao_index(int lunar_month);

    /**
     * @brief 安解神（按月份）
     */
    int get_jie_shen_index(int lunar_month);

    /**
     * @brief 安天巫（按月份）
     */
    int get_tian_wu_index(int lunar_month);

    /**
     * @brief 安天月（按月份）
     */
    int get_tian_yue_index(int lunar_month);

    /**
     * @brief 安阴煞（按月份）
     */
    int get_yin_sha_index(int lunar_month);

    /**
     * @brief 安天德月德（按年支）
     */
    pair<int, int> get_tian_de_yue_de_index(DiZhi year_zhi);

    /**
     * @brief 安天空（按年支）
     */
    int get_tian_kong_index(DiZhi year_zhi);

    /**
     * @brief 安旬空（按年干支）
     * 返回两个空亡地支的宫位索引
     */
    pair<int, int> get_xun_kong_index(TianGan year_gan, DiZhi year_zhi);

    /**
     * @brief 安截路空亡（按年干）
     */
    pair<int, int> get_jie_lu_kong_wang_index(TianGan year_gan);

    /**
     * @brief 安天哭天虚（按年支）
     */
    pair<int, int> get_tian_ku_tian_xu_index(DiZhi year_zhi);

    /**
     * @brief 安天使天伤（按命宫索引和性别）
     */
    pair<int, int> get_tian_shi_tian_shang_index(int ming_index, bool is_male, DiZhi year_zhi);

    /**
     * @brief 安年解（按年支）
     */
    int get_nian_jie_index(DiZhi year_zhi);

    /**
     * @brief 安天马（按年支）
     */
    int get_tian_ma_index(DiZhi year_zhi);

    /**
     * @brief 安大耗和龙德（按年支，生年杂耀）
     * 
     * 口诀：
     * 大耗在年支之对宫，前一位或后一位安星。
     * 阳地支顺行前一位，阴地支逆行后一位。
     * 龙德在大耗对宫。
     */
    pair<int, int> get_da_hao_long_de_index(DiZhi year_zhi);

    // ============= 长生12神和博士12神 =============

    /**
     * @brief 获取长生12神开始的宫位索引
     */
    int get_chang_sheng_12_start_index(WuXingJu wu_xing_ju);

    /**
     * @brief 安长生12神
     */
    array<ChangSheng12, 12> arrange_chang_sheng_12(
        WuXingJu wu_xing_ju, 
        bool is_male, 
        DiZhi year_zhi
    );

    /**
     * @brief 安博士12神
     */
    array<BoShi12, 12> arrange_bo_shi_12(
        TianGan year_gan,
        DiZhi year_zhi,
        bool is_male
    );

    // ============= 流年诸星 =============

    /**
     * @brief 获取将前12神开始的宫位索引
     */
    int get_jiang_qian_12_start_index(DiZhi year_zhi);

    /**
     * @brief 安岁前12神
     */
    array<SuiQian12, 12> arrange_sui_qian_12(DiZhi year_zhi);

    /**
     * @brief 安将前12神
     */
    array<JiangQian12, 12> arrange_jiang_qian_12(DiZhi year_zhi);

} // namespace ZhouYi::ZiWei
