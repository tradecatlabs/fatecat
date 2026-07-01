// 紫微斗数三方四正系统模块（接口）
export module ZhouYi.ZiWei.SanFang;

import std;
import ZhouYi.ZiWei.Constants;
import ZhouYi.ZhMapper;

export namespace ZhouYi::ZiWei {
    using namespace std;

    /**
     * @brief 三方四正宫位结构
     * 
     * 三方四正包括：
     * - 本宫：目标宫位本身
     * - 对宫：与本宫相对（相差6宫）
     * - 财帛位：本宫+8（三合宫之一）
     * - 官禄位：本宫+4（三合宫之一）
     */
    struct SanFangSiZheng {
        int ben_gong_index;      // 本宫索引
        int dui_gong_index;      // 对宫索引（+6）
        int cai_bo_index;        // 财帛位（+8）
        int guan_lu_index;       // 官禄位（+4）
        
        /**
         * @brief 获取所有宫位索引
         */
        array<int, 4> get_all_indices() const {
            return {ben_gong_index, dui_gong_index, cai_bo_index, guan_lu_index};
        }
        
        /**
         * @brief 判断某宫是否在三方四正中
         */
        bool contains(int gong_index) const {
            return gong_index == ben_gong_index ||
                   gong_index == dui_gong_index ||
                   gong_index == cai_bo_index ||
                   gong_index == guan_lu_index;
        }
        
        string to_string() const;
    };

    /**
     * @brief 夹宫信息
     * 左右两宫夹持某宫
     */
    struct JiaGongInfo {
        int target_gong;         // 目标宫位
        int left_gong;           // 左边宫位（前一宫）
        int right_gong;          // 右边宫位（后一宫）
        
        string to_string() const;
    };

    /**
     * @brief 空宫信息
     * 无主星的宫位
     */
    struct KongGongInfo {
        int gong_index;          // 空宫索引
        int dui_gong_index;      // 对宫索引（借星来源）
        vector<string> jie_xing; // 借来的星耀
        
        bool is_kong() const {
            return !jie_xing.empty();
        }
        
        string to_string() const;
    };

    /**
     * @brief 获取三方四正
     * 
     * @param gong_index 目标宫位索引
     * @return 三方四正结构
     */
    SanFangSiZheng get_san_fang_si_zheng(int gong_index);

    /**
     * @brief 获取夹宫信息
     * 
     * @param gong_index 目标宫位索引
     * @return 夹宫信息
     */
    JiaGongInfo get_jia_gong_info(int gong_index);

    /**
     * @brief 判断某宫是否空宫（无主星）
     * 
     * @param zhu_xing_list 宫位的主星列表
     * @return 是否空宫
     */
    bool is_kong_gong(const vector<string>& zhu_xing_list);

    /**
     * @brief 获取借星（从对宫借主星）
     * 
     * @param gong_index 空宫索引
     * @param dui_gong_zhu_xing 对宫的主星列表
     * @return 空宫信息（包含借来的星）
     */
    KongGongInfo get_jie_xing_info(int gong_index, const vector<string>& dui_gong_zhu_xing);

    /**
     * @brief 三方四正分析器
     */
    class SanFangAnalyzer {
    public:
        /**
         * @brief 构造函数
         * @param stars_in_gong 每个宫位的所有星耀
         */
        SanFangAnalyzer(const array<vector<string>, 12>& stars_in_gong);
        
        /**
         * @brief 获取三方四正的所有星耀
         */
        vector<string> get_san_fang_stars(int gong_index) const;
        
        /**
         * @brief 判断三方四正是否有某星
         */
        bool san_fang_has_star(int gong_index, const string& star_name) const;
        
        /**
         * @brief 判断三方四正是否有某些星（全部满足）
         */
        bool san_fang_has_all_stars(int gong_index, const vector<string>& star_names) const;
        
        /**
         * @brief 判断三方四正是否有某些星（满足其一）
         */
        bool san_fang_has_any_star(int gong_index, const vector<string>& star_names) const;
        
        /**
         * @brief 获取夹某宫的星耀
         */
        vector<string> get_jia_gong_stars(int gong_index) const;
        
        /**
         * @brief 判断是否被吉星夹（左辅右弼、文昌文曲、天魁天钺）
         */
        bool is_ji_xing_jia(int gong_index) const;
        
        /**
         * @brief 判断是否被煞星夹（擎羊陀罗、火星铃星）
         */
        bool is_sha_xing_jia(int gong_index) const;
        
        /**
         * @brief 获取所有空宫
         */
        vector<KongGongInfo> get_all_kong_gong() const;
        
    private:
        array<vector<string>, 12> stars_in_gong_;
        
        /**
         * @brief 判断是否为主星
         */
        bool is_zhu_xing(const string& star_name) const;
    };

} // namespace ZhouYi::ZiWei

