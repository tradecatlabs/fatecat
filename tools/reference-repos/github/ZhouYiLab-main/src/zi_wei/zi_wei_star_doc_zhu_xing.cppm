// 紫微斗数星曜文档 - 十四主星（接口）
// 包含紫微、天机、太阳、武曲、天同、廉贞、天府、太阴、贪狼、巨门、天相、天梁、七杀、破军
export module ZhouYi.ZiWei.StarDoc.ZhuXing;

import ZhouYi.ZiWei.StarDoc.Common;
import ZhouYi.ZhMapper;
import std;

export namespace ZhouYi::ZiWei::StarDoc {
    using namespace std;
    using namespace ZhouYi::ZiWei;

    // ============= 主星分类 =============
    
    /**
     * @brief 主星分类（按星系）
     */
    enum class ZhuXingCategory {
        ZiWeiXing,       // 紫微星系（紫微、天机、太阳、武曲、天同、廉贞）
        TianFuXing,      // 天府星系（天府、太阴、贪狼、巨门、天相、天梁、七杀、破军）
        COUNT
    };

    // ============= 双星组合结构 =============
    
    /**
     * @brief 双星组合文档
     */
    struct DualStarDocument {
        string name;                     // 组合名称（如"紫微天府"）
        string star1;                    // 主星1
        string star2;                    // 主星2
        double probability;              // 命宫出现概率
        string ge_ju;                    // 格局名称（如有）
        string description;              // 组合特性描述
        string key_trait;                // 核心特质
        
        string to_string() const;
    };

    // ============= 主星分类相关函数 =============

    /// 获取主星分类的描述
    string get_zhu_xing_category_description(ZhuXingCategory category);

    /// 获取某分类下的所有主星名称
    vector<string> get_zhu_xing_by_category(ZhuXingCategory category);

    /// 获取所有主星分类信息
    vector<CategoryInfo> get_all_zhu_xing_categories();

    // ============= 主星文档查询函数 =============

    /// 获取主星的详细文档
    optional<StarDocument> get_zhu_xing_document(const string& star_name);

    /// 获取主星的分类
    optional<ZhuXingCategory> get_zhu_xing_category(const string& star_name);

    /// 获取所有主星名称
    vector<string> get_all_zhu_xing_names();

    // ============= 双星组合查询函数 =============

    /// 获取双星组合的详细文档
    optional<DualStarDocument> get_dual_star_document(const string& star1, const string& star2);

    /// 获取某主星的所有双星组合
    vector<DualStarDocument> get_dual_star_combinations(const string& star_name);

    /// 获取所有双星组合
    vector<DualStarDocument> get_all_dual_star_combinations();

} // namespace ZhouYi::ZiWei::StarDoc

// ============= ZhMapper 特化 =============

export namespace ZhouYi::Mapper {
    using namespace ZhouYi::ZiWei::StarDoc;
    
    template<>
    struct ZhMap<ZhuXingCategory> {
        static constexpr auto get_map() {
            using namespace std::literals;
            return std::array{
                "紫微星系"sv, "天府星系"sv
            };
        }
    };
    
} // namespace ZhouYi::Mapper
