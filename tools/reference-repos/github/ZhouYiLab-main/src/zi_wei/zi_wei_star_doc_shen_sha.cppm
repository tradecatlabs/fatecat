// 紫微斗数星曜文档 - 四十八神煞（接口）
// 包含长生12神、博士12神、将前12神、岁前12神
export module ZhouYi.ZiWei.StarDoc.ShenSha;

import ZhouYi.ZiWei.StarDoc.Common;
import ZhouYi.ZhMapper;
import std;

export namespace ZhouYi::ZiWei::StarDoc {
    using namespace std;
    using namespace ZhouYi::ZiWei;

    // ============= 神煞分类 =============
    
    /**
     * @brief 神煞分类（四十八神煞）
     * 神煞是修饰型星曜，更偏向于一种气质
     */
    enum class ShenShaCategory {
        ChangSheng,      // 长生12神（固定，长期）
        BoShi,           // 博士12神（固定，长期）
        JiangQian,       // 将前12神（流动，随流年变化）
        SuiQian,         // 岁前12神（流动，随流年变化）
        COUNT
    };

    // ============= 神煞文档结构 =============
    
    /**
     * @brief 神煞详细文档信息
     */
    struct ShenShaDocument {
        string name;                         // 神煞名称
        ShenShaCategory category;            // 所属分类
        optional<XingYaoWuXing> wu_xing;     // 五行（博士12神有五行属性）
        string description;                  // 详细描述
        string key_effect;                   // 核心效果
        bool is_fixed;                       // 是否固定（true=出生后固定，false=随流年变化）
        
        string to_string() const;
    };

    // ============= 分类相关函数 =============

    /// 获取神煞分类的描述
    string get_shen_sha_category_description(ShenShaCategory category);

    /// 获取某分类下的所有神煞名称
    vector<string> get_shen_sha_by_category(ShenShaCategory category);

    /// 获取所有神煞分类信息
    vector<CategoryInfo> get_all_shen_sha_categories();

    // ============= 神煞文档查询函数 =============

    /// 获取神煞的详细文档
    optional<ShenShaDocument> get_shen_sha_document(const string& star_name);

    /// 获取神煞的分类
    optional<ShenShaCategory> get_shen_sha_category(const string& star_name);

    /// 获取所有神煞名称
    vector<string> get_all_shen_sha_names();

    /// 判断是否为固定神煞（长生12神、博士12神）
    bool is_fixed_shen_sha(const string& star_name);

    /// 判断是否为流动神煞（将前12神、岁前12神）
    bool is_dynamic_shen_sha(const string& star_name);

} // namespace ZhouYi::ZiWei::StarDoc

// ============= ZhMapper 特化 =============

export namespace ZhouYi::Mapper {
    using namespace ZhouYi::ZiWei::StarDoc;
    
    template<>
    struct ZhMap<ShenShaCategory> {
        static constexpr auto get_map() {
            using namespace std::literals;
            return std::array{
                "长生十二神"sv, "博士十二神"sv, "将前十二神"sv, "岁前十二神"sv
            };
        }
    };
    
} // namespace ZhouYi::Mapper
