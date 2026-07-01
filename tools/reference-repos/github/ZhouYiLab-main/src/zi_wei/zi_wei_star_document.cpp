// 紫微斗数星曜详细文档模块 - 主入口实现
// 统一入口函数实现
module ZhouYi.ZiWei.StarDocument;

import ZhouYi.ZiWei.StarDoc.Common;
import ZhouYi.ZiWei.StarDoc.ZhuXing;
import ZhouYi.ZiWei.StarDoc.FuXing;
import ZhouYi.ZiWei.StarDoc.ZaYao;
import ZhouYi.ZiWei.StarDoc.ShenSha;
import std;

namespace ZhouYi::ZiWei {
    using namespace std;
    using namespace ZhouYi::ZiWei::StarDoc;

    // ============= 统一入口API实现 =============

    optional<StarDocument> get_star_document(const string& star_name) {
        // 先查主星
        auto zhu_xing_doc = get_zhu_xing_document(star_name);
        if (zhu_xing_doc.has_value()) {
            return zhu_xing_doc;
        }
        
        // 再查辅星
        auto fu_xing_doc = get_fu_xing_document(star_name);
        if (fu_xing_doc.has_value()) {
            return fu_xing_doc;
        }
        
        // 再查杂曜
        auto za_yao_doc = get_za_yao_document(star_name);
        if (za_yao_doc.has_value()) {
            return za_yao_doc;
        }
        
        return nullopt;
    }

    optional<StarType> get_star_type(const string& star_name) {
        auto doc = get_star_document(star_name);
        if (doc.has_value()) {
            return doc->star_type;
        }
        return nullopt;
    }

    vector<string> get_stars_by_type(StarType type) {
        switch (type) {
            case StarType::ZhuXing:
                return get_all_zhu_xing_names();
            case StarType::FuXing:
                return get_all_fu_xing_names();
            case StarType::ZaYao:
                return get_all_za_yao_names();
            case StarType::ShenSha:
                return get_all_shen_sha_names();
            default:
                return {};
        }
    }

} // namespace ZhouYi::ZiWei
