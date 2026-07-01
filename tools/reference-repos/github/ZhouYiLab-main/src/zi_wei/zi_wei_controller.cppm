// 紫微斗数控制器接口模块
export module ZhouYi.ZiWei.Controller;

import std;
import ZhouYi.GanZhi;
import ZhouYi.ZiWei;
import ZhouYi.ZiWei.Constants;
import ZhouYi.ZiWei.SiHua;
import ZhouYi.ZiWei.SanFang;
import ZhouYi.ZiWei.GeJu;
import ZhouYi.ZiWei.StarDocument;

export namespace ZhouYi::ZiWei {
    using namespace std;
    using namespace ZhouYi::GanZhi;

    // ============= 基础排盘功能 =============
    
    /**
     * @brief 阳历排盘并输出
     */
    void pai_pan_and_print_solar(int year, int month, int day, int hour, bool is_male);

    /**
     * @brief 农历排盘并输出
     */
    void pai_pan_and_print_lunar(int year, int month, int day, int hour, 
                                  bool is_male, bool is_leap_month = false);

    /**
     * @brief 显示宫位详情
     */
    void display_palace_detail(const ZiWeiResult& result, GongWei gong_wei);

    /**
     * @brief 显示命宫三方四正
     */
    void display_ming_gong_san_fang_si_zheng(const ZiWeiResult& result);

    // ============= 四化分析功能 =============
    
    /**
     * @brief 显示宫干四化分析
     */
    void display_gong_gan_si_hua(const ZiWeiResult& result);
    
    /**
     * @brief 显示自化分析
     */
    void display_zi_hua_analysis(const ZiWeiResult& result);
    
    /**
     * @brief 显示飞化分析
     */
    void display_fei_hua_analysis(const ZiWeiResult& result, int from_gong, SiHua si_hua_type);
    
    // ============= 格局分析功能 =============
    
    /**
     * @brief 显示命盘格局分析
     */
    void display_ge_ju_analysis(const ZiWeiResult& result);
    
    /**
     * @brief 显示吉格列表
     */
    void display_ji_ge(const ZiWeiResult& result);
    
    /**
     * @brief 显示凶格列表
     */
    void display_xiong_ge(const ZiWeiResult& result);
    
    /**
     * @brief 显示双星组合分析
     */
    void display_shuang_xing_zu_he(const ZiWeiResult& result);
    
    // ============= 三方四正分析功能 =============
    
    /**
     * @brief 显示指定宫位的三方四正
     */
    void display_san_fang_si_zheng(const ZiWeiResult& result, GongWei gong_wei);
    
    /**
     * @brief 显示空宫借星分析
     */
    void display_kong_gong_jie_xing(const ZiWeiResult& result);
    
    // ============= 星耀特性查询功能 =============
    
    /**
     * @brief 显示星耀详细信息
     */
    void display_star_info(const string& star_name);
    
    /**
     * @brief 显示所有桃花星
     */
    void display_tao_hua_xing();
    
    /**
     * @brief 显示所有财星
     */
    void display_cai_xing();
    
    // ============= 运限分析功能 =============
    
    /**
     * @brief 显示大限分析
     */
    void display_da_xian_analysis(const ZiWeiResult& result);
    
    /**
     * @brief 显示小限分析
     */
    void display_xiao_xian_analysis(const ZiWeiResult& result, int current_age);
    
    /**
     * @brief 显示流年分析
     */
    void display_liu_nian_analysis(const ZiWeiResult& result, int target_year, int current_age);
    
    /**
     * @brief 显示流月分析
     */
    void display_liu_yue_analysis(const ZiWeiResult& result, int target_year, int target_month, int current_age);
    
    /**
     * @brief 显示流日分析
     */
    void display_liu_ri_analysis(const ZiWeiResult& result, int target_year, int target_month, int target_day, int current_age);
    
    /**
     * @brief 显示流时分析
     */
    void display_liu_shi_analysis(const ZiWeiResult& result, int target_year, int target_month, int target_day, DiZhi target_hour, int current_age);
    
    /**
     * @brief 显示完整运限分析（大限+流年+流月+流日+流时）
     */
    void display_yun_xian_full_analysis(const ZiWeiResult& result, int target_year, int target_month, int target_day, DiZhi target_hour, int current_age);
    
    // ============= 综合分析功能 =============
    
    /**
     * @brief 显示完整命盘分析（包含所有分析）
     */
    void display_full_analysis(const ZiWeiResult& result);
    
    /**
     * @brief 导出为JSON格式（完整版，包含格局、四化等）
     */
    string export_to_json_full(const ZiWeiResult& result);
    
    /**
     * @brief 导出为JSON格式（基础版）
     */
    string export_to_json(const ZiWeiResult& result);

} // namespace ZhouYi::ZiWei

