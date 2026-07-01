// 紫微斗数星曜文档 - 十四辅星
export module ZhouYi.ZiWei.StarDoc.FuXing;

import std;
import ZhouYi.ZiWei.StarDoc.Common;
import ZhouYi.ZhMapper;

export namespace ZhouYi::ZiWei::StarDoc {
    using namespace std;
    using namespace ZhouYi::ZiWei;  // 导入类型定义

    // ============= 辅星分类说明 =============
    
    /**
     * @brief 获取辅星分类说明
     */
    string get_fu_xing_category_description(FuXingCategory category);

    /**
     * @brief 获取指定辅星分类的所有星曜
     */
    vector<string> get_fu_xing_by_category(FuXingCategory category);

    /**
     * @brief 获取所有辅星分类信息
     */
    vector<CategoryInfo> get_all_fu_xing_categories();

    /**
     * @brief 获取辅星文档
     */
    optional<StarDocument> get_fu_xing_document(const string& star_name);

    /**
     * @brief 获取辅星所属分类
     */
    optional<FuXingCategory> get_fu_xing_category(const string& star_name);

    /**
     * @brief 获取所有辅星名称
     */
    vector<string> get_all_fu_xing_names();

} // namespace ZhouYi::ZiWei::StarDoc