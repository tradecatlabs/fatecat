// 紫微斗数星曜文档 - 通用定义
// 包含星曜类型、五行、阴阳等基础类型定义
export module ZhouYi.ZiWei.StarDoc.Common;

import std;
import ZhouYi.ZhMapper;

// ============= 枚举类型定义 =============

export namespace ZhouYi::ZiWei {
    using namespace std;

    // 星曜五行属性
    enum class XingYaoWuXing {
        Jin,         // 金
        Mu,          // 木
        Shui,        // 水
        Huo,         // 火
        Tu           // 土
    };

    // 星曜阴阳属性
    enum class XingYaoYinYang {
        Yang,        // 阳
        Yin          // 阴
    };

    // 星曜大类
    enum class StarType {
        ZhuXing,     // 十四主星
        FuXing,      // 十四辅星（六吉六煽二助）
        ZaYao,       // 三十七杂曜
        ShenSha,     // 四十八神煽
        COUNT
    };

    // 辅星分类
    enum class FuXingCategory {
        LiuJi,       // 六吉星
        LiuSha,      // 六煽星
        ErZhu,       // 二助星
        COUNT
    };

    // 杂曜分类
    enum class ZaYaoCategory {
        JiaoJi,      // 交际类
        GuAo,        // 孤傲类
        CaiYi,       // 才艺类
        JinGui,      // 矜贵类
        JingShen,    // 精神类
        XingYun,     // 幸运类
        JianKang,    // 健康类
        FengShang,   // 封赏类
        SiXiang,     // 思想类
        COUNT
    };

} // namespace ZhouYi::ZiWei

// ============= ZhMapper 特化（必须在结构体定义之前） =============

export namespace ZhouYi::Mapper {
    using namespace ZhouYi::ZiWei;
    
    template<>
    struct ZhMap<XingYaoWuXing> {
        static constexpr auto get_map() {
            using namespace std::literals;
            return std::array{
                "金"sv, "木"sv, "水"sv, "火"sv, "土"sv
            };
        }
    };
    
    template<>
    struct ZhMap<XingYaoYinYang> {
        static constexpr auto get_map() {
            using namespace std::literals;
            return std::array{
                "阳"sv, "阴"sv
            };
        }
    };
    
    template<>
    struct ZhMap<StarType> {
        static constexpr auto get_map() {
            using namespace std::literals;
            return std::array{
                "十四主星"sv, "十四辅星"sv, "三十七杂曜"sv, "四十八神煽"sv
            };
        }
    };
    
    template<>
    struct ZhMap<FuXingCategory> {
        static constexpr auto get_map() {
            using namespace std::literals;
            return std::array{
                "六吉星"sv, "六煽星"sv, "二助星"sv
            };
        }
    };
    
    template<>
    struct ZhMap<ZaYaoCategory> {
        static constexpr auto get_map() {
            using namespace std::literals;
            return std::array{
                "交际类"sv, "孤傲类"sv, "才艺类"sv, "矜贵类"sv,
                "精神类"sv, "幸运类"sv, "健康类"sv, "封赏类"sv, "思想类"sv
            };
        }
    };
    
} // namespace ZhouYi::Mapper

// ============= 结构体定义（在 ZhMapper 特化之后） =============

export namespace ZhouYi::ZiWei {
    using namespace std;

    /**
     * @brief 星曜详细文档信息（通用结构）
     */
    struct StarDocument {
        string name;                         // 星曜名称
        StarType star_type;                  // 星曜大类
        optional<XingYaoWuXing> wu_xing;     // 五行
        optional<XingYaoYinYang> yin_yang;   // 阴阳
        string hua_qi;                       // 化气
        string zhi_wu;                       // 职务
        string bie_hao;                      // 别号
        string description;                  // 详细描述
        string key_trait;                    // 核心特质
        
        // 辅星专属字段
        optional<FuXingCategory> fu_xing_category;  // 辅星分类
        
        // 杂曜专属字段
        optional<ZaYaoCategory> za_yao_category;    // 杂曜分类
        
        string to_string() const {
            ostringstream oss;
            
            oss << "【" << name << "】\n";
            oss << "━━━━━━━━━━━━━━━━━━━━━━━━━━\n";
            
            // 基本属性
            oss << "星曜类型: " << Mapper::to_zh(star_type) << "\n";
            if (wu_xing.has_value()) {
                oss << "五行: " << Mapper::to_zh(wu_xing.value()) << "\n";
            }
            if (yin_yang.has_value()) {
                oss << "阴阳: " << Mapper::to_zh(yin_yang.value()) << "\n";
            }
            
            if (!hua_qi.empty()) {
                oss << "化气: " << hua_qi << "\n";
            }
            if (!zhi_wu.empty()) {
                oss << "职务: " << zhi_wu << "\n";
            }
            if (!bie_hao.empty()) {
                oss << "别号: " << bie_hao << "\n";
            }
            
            // 分类信息
            if (fu_xing_category.has_value()) {
                oss << "辅星分类: " << Mapper::to_zh(fu_xing_category.value()) << "\n";
            }
            if (za_yao_category.has_value()) {
                oss << "杂曜分类: " << Mapper::to_zh(za_yao_category.value()) << "\n";
            }
            
            oss << "━━━━━━━━━━━━━━━━━━━━━━━━━━\n";
            
            // 关键特质
            if (!key_trait.empty()) {
                oss << "核心特质: " << key_trait << "\n";
            }
            
            // 详细描述
            if (!description.empty()) {
                oss << "\n" << description << "\n";
            }
            
            return oss.str();
        }
    };

    /**
     * @brief 分类信息（通用结构）
     */
    struct CategoryInfo {
        string name;                    // 分类名称
        string description;             // 分类说明
        vector<string> stars;           // 包含的星曜
    };

} // namespace ZhouYi::ZiWei
