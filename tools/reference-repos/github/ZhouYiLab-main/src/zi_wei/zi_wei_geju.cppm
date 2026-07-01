// 紫微斗数格局判断系统模块（接口）
export module ZhouYi.ZiWei.GeJu;

import std;
import ZhouYi.GanZhi;
import ZhouYi.ZiWei.Constants;
import ZhouYi.ZiWei.SanFang;
import ZhouYi.ZhMapper;

export namespace ZhouYi::ZiWei {
    using namespace std;
    using namespace ZhouYi::GanZhi;

    /**
     * @brief 格局类型枚举
     */
    enum class GeJuType {
        // ========= 富贵格局 =========
        ZiFuTongGong,          // 紫府同宫
        ZiFuChaoYuan,          // 紫府朝垣
        TianFuChaoYuan,        // 天府朝垣
        JunChenQingHui,        // 君臣庆会
        FuXiangChaoYuan,       // 府相朝垣
        
        // 机月同梁格
        JiYueTongLiang,        // 机月同梁格
        JiLiangJiaHui,         // 机梁夹会
        
        // 日月格局
        RiYueBingMing,         // 日月并明（卯酉宫）
        RiZhaoLeiMen,          // 日照雷门（卯宫）
        YueLangTianMen,        // 月朗天门（亥宫）
        MingZhuChuHai,         // 明珠出海（酉宫太阴）
        RiYueBoZhao,           // 日月夹照
        
        // 阳梁格局
        YangLiangChangLu,      // 阳梁昌禄格
        
        // 贪狼格局
        TanWuTongXing,         // 贪武同行（丑未宫）
        TanLingJiaHui,         // 贪铃夹会
        HuoTanGeJu,            // 火贪格局
        LingTanGeJu,           // 铃贪格局
        
        // ========= 权贵格局 =========
        SanQiJiaHui,           // 三奇嘉会（禄权科）
        ShuangLuJiaMing,       // 双禄夹命
        ShuangLuJiaCai,        // 双禄夹财
        KeQuanLuJia,           // 科权禄夹
        ZuoYouJiaMing,         // 左右夹命/财
        ChangQuJiaMing,        // 昌曲夹命
        KuiYueJiaMing,         // 魁钺夹命
        
        // ========= 凶格 =========
        LingChangTuoWu,        // 铃昌陀武（铃星文昌陀罗武曲同宫）
        JiJiTongGong,          // 巨机同宫（辰戌宫）
        JuRiTongGong,          // 巨日同宫（最忌）
        MingXiangLiangJia,     // 命无正曜（空宫）
        MaTouDaiJian,          // 马头带箭（午宫擎羊守命）
        LiangJiJiaMing,        // 羊陀夹命
        HuoLingJiaMing,        // 火铃夹命
        KongJieJiaMing,        // 空劫夹命
        YangTuoJiaJi,          // 羊陀夹忌
        SiShaChongMing,        // 四煞冲命
        
        // ========= 其他重要格局 =========
        LuMaJiaoChiGeJu,       // 禄马交驰
        QuanLuXunFeng,         // 权禄巡逢
        MinggongWuZhuXing,     // 命宫无主星
    };

    /**
     * @brief 格局信息
     */
    struct GeJuInfo {
        GeJuType type;              // 格局类型
        string name;                // 格局名称
        string description;         // 格局说明
        bool is_ji;                 // 是否吉格（true=吉，false=凶）
        int score;                  // 格局分数（-100~+100）
        vector<string> key_stars;   // 关键星耀
        vector<int> key_gongs;      // 关键宫位
        
        string to_string() const;
    };

    /**
     * @brief 双星组合类型
     */
    enum class ShuangXingType {
        // 紫微系组合
        ZiWei_TianFu,      // 紫微天府
        ZiWei_TanLang,     // 紫微贪狼
        ZiWei_TianXiang,   // 紫微天相
        ZiWei_QiSha,       // 紫微七杀
        ZiWei_PoJun,       // 紫微破军
        
        // 天府系组合
        TianFu_WuQu,       // 天府武曲
        TianFu_LianZhen,   // 天府廉贞
        
        // 武曲系组合
        WuQu_TianFu,       // 武曲天府
        WuQu_TanLang,      // 武曲贪狼
        WuQu_TianXiang,    // 武曲天相
        WuQu_QiSha,        // 武曲七杀
        WuQu_PoJun,        // 武曲破军
        
        // 太阳系组合
        TaiYang_TaiYin,    // 太阳太阴
        TaiYang_TianLiang,  // 太阳天梁
        TaiYang_JuMen,      // 太阳巨门
        
        // 其他重要组合
        TianTong_TaiYin,    // 天同太阴
        TianTong_TianLiang, // 天同天梁
        TianTong_JuMen,     // 天同巨门
        TianJi_TaiYin,      // 天机太阴
        TianJi_TianLiang,   // 天机天梁
        TianJi_JuMen,       // 天机巨门
        
        Unknown             // 其他组合
    };

    /**
     * @brief 双星组合信息
     */
    struct ShuangXingInfo {
        ShuangXingType type;        // 组合类型
        string xing1_name;          // 第一颗星
        string xing2_name;          // 第二颗星
        int gong_index;             // 所在宫位
        string xing_zhi;            // 组合性质（如：财官双美）
        string description;         // 组合说明
        
        string to_string() const;
    };

    /**
     * @brief 格局判断引擎
     */
    class GeJuAnalyzer {
    public:
        /**
         * @brief 构造函数
         * @param stars_in_gong 每个宫位的星耀列表
         * @param gong_di_zhi 每个宫位的地支（从寅宫开始）
         * @param ming_gong_index 命宫索引
         */
        GeJuAnalyzer(
            const array<vector<string>, 12>& stars_in_gong,
            const array<DiZhi, 12>& gong_di_zhi,
            int ming_gong_index
        );
         
        /**
         * @brief 分析所有格局
         */
        vector<GeJuInfo> analyze_all() const;
        
        /**
         * @brief 分析吉格
         */
        vector<GeJuInfo> analyze_ji_ge() const;
        
        /**
         * @brief 分析凶格
         */
        vector<GeJuInfo> analyze_xiong_ge() const;
        
        /**
         * @brief 分析双星组合
         */
        vector<ShuangXingInfo> analyze_shuang_xing() const;
        
        /**
         * @brief 获取命盘总评分
         */
        int get_total_score() const;
        
    private:
        array<vector<string>, 12> stars_in_gong_;
        array<DiZhi, 12> gong_di_zhi_;        // 每个宫位的地支
        int ming_gong_index_;
        SanFangAnalyzer san_fang_analyzer_;
        
        // 富贵格局判断
        optional<GeJuInfo> check_zi_fu_tong_gong() const;
        optional<GeJuInfo> check_zi_fu_chao_yuan() const;
        optional<GeJuInfo> check_tian_fu_chao_yuan() const;
        optional<GeJuInfo> check_jun_chen_qing_hui() const;
        optional<GeJuInfo> check_fu_xiang_chao_yuan() const;
        optional<GeJuInfo> check_ji_yue_tong_liang() const;
        optional<GeJuInfo> check_ji_liang_jia_hui() const;
        optional<GeJuInfo> check_ri_yue_bing_ming() const;
        optional<GeJuInfo> check_ri_zhao_lei_men() const;
        optional<GeJuInfo> check_yue_lang_tian_men() const;
        optional<GeJuInfo> check_ming_zhu_chu_hai() const;
        optional<GeJuInfo> check_ri_yue_bo_zhao() const;
        optional<GeJuInfo> check_yang_liang_chang_lu() const;
        optional<GeJuInfo> check_tan_wu_tong_xing() const;
        optional<GeJuInfo> check_tan_ling_jia_hui() const;
        optional<GeJuInfo> check_huo_tan() const;
        optional<GeJuInfo> check_ling_tan() const;
        
        // 权贵格局判断
        optional<GeJuInfo> check_san_qi_jia_hui() const;
        optional<GeJuInfo> check_shuang_lu_jia_ming() const;
        optional<GeJuInfo> check_shuang_lu_jia_cai() const;
        optional<GeJuInfo> check_ke_quan_lu_jia() const;
        optional<GeJuInfo> check_zuo_you_jia() const;
        optional<GeJuInfo> check_chang_qu_jia_ming() const;
        optional<GeJuInfo> check_kui_yue_jia_ming() const;
        
        // 凶格判断
        optional<GeJuInfo> check_ling_chang_tuo_wu() const;
        optional<GeJuInfo> check_ji_ji_tong_gong() const;
        optional<GeJuInfo> check_ju_ri_tong_gong() const;
        optional<GeJuInfo> check_ming_xiang_liang_jia() const;
        optional<GeJuInfo> check_ma_tou_dai_jian() const;
        optional<GeJuInfo> check_liang_ji_jia_ming() const;
        optional<GeJuInfo> check_sha_xing_jia_ming() const;
        optional<GeJuInfo> check_kong_jie_jia_ming() const;
        optional<GeJuInfo> check_yang_tuo_jia_ji() const;
        optional<GeJuInfo> check_si_sha_chong_ming() const;
        
        // 其他重要格局
        optional<GeJuInfo> check_lu_ma_jiao_chi() const;
        optional<GeJuInfo> check_quan_lu_xun_feng() const;
        optional<GeJuInfo> check_ming_gong_wu_zhu_xing() const;
        
        // 辅助函数
        DiZhi get_gong_di_zhi(int gong_index) const;
        bool gong_has_star(int gong_index, const string& star_name) const;
        bool gong_has_all_stars(int gong_index, const vector<string>& stars) const;
        bool gong_has_any_star(int gong_index, const vector<string>& stars) const;
        vector<string> get_zhu_xing_in_gong(int gong_index) const;
    };

} // namespace ZhouYi::ZiWei

