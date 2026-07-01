// 紫微斗数星曜文档 - 三十七杂耀（接口）
export module ZhouYi.ZiWei.StarDoc.ZaYao;

import ZhouYi.ZiWei.StarDoc.Common;
import std;

export namespace ZhouYi::ZiWei::StarDoc {
    using namespace std;
    using namespace ZhouYi::ZiWei;  // 导入类型定义

    // ============= 杂耀分类相关函数 =============

    /// 获取杂耀分类的描述
    /// @param category 杂耀分类
    /// @return 分类描述
    string get_za_yao_category_description(ZaYaoCategory category);

    /// 获取某分类下的所有杂耀名称
    /// @param category 杂耀分类
    /// @return 该分类下的杂耀名称列表
    vector<string> get_za_yao_by_category(ZaYaoCategory category);

    /// 获取所有杂耀分类信息
    /// @return 所有杂耀分类的详细信息
    vector<CategoryInfo> get_all_za_yao_categories();

    // ============= 杂耀文档查询函数 =============

    /// 获取杂耀的详细文档
    /// @param star_name 杂耀名称
    /// @return 杂耀文档，如果未找到则返回 nullopt
    optional<StarDocument> get_za_yao_document(const string& star_name);

    /// 获取杂耀的分类
    /// @param star_name 杂耀名称
    /// @return 杂耀分类，如果未找到则返回 nullopt
    optional<ZaYaoCategory> get_za_yao_category(const string& star_name);

    /// 获取所有杂耀名称
    /// @return 所有杂耀名称列表
    vector<string> get_all_za_yao_names();

} // namespace ZhouYi::ZiWei::StarDoc
