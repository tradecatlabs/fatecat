// 紫微斗数星曜详细文档模块 - 主入口
// 聚合并重导出所有星曜文档子模块
export module ZhouYi.ZiWei.StarDocument;

// 导出子模块
export import ZhouYi.ZiWei.StarDoc.Common;
export import ZhouYi.ZiWei.StarDoc.ZhuXing;
export import ZhouYi.ZiWei.StarDoc.FuXing;
export import ZhouYi.ZiWei.StarDoc.ZaYao;
export import ZhouYi.ZiWei.StarDoc.ShenSha;

import std;

export namespace ZhouYi::ZiWei {
    using namespace std;
    using namespace ZhouYi::ZiWei::StarDoc;

    // ============= 统一入口API =============
    
    /**
     * @brief 获取星曜文档信息（统一入口）
     * @param star_name 星曜名称
     * @return 星曜详细文档，如果未找到返回空optional
     */
    optional<StarDocument> get_star_document(const string& star_name);

    /**
     * @brief 获取星曜所属大类
     */
    optional<StarType> get_star_type(const string& star_name);

    /**
     * @brief 获取指定大类的所有星曜
     */
    vector<string> get_stars_by_type(StarType type);

} // namespace ZhouYi::ZiWei
