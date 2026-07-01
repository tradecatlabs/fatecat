// 紫微斗数三方四正系统模块（实现）
module ZhouYi.ZiWei.SanFang;

import ZhouYi.ZiWei.Constants;
import fmt;
import std;
import ZhouYi.ZhMapper;

namespace ZhouYi::ZiWei {
    using namespace std;

    // ============= 辅助函数 =============

    string SanFangSiZheng::to_string() const {
        return fmt::format("本宫:第{}宫, 对宫:第{}宫, 财帛:第{}宫, 官禄:第{}宫",
            ben_gong_index, dui_gong_index, cai_bo_index, guan_lu_index);
    }

    string JiaGongInfo::to_string() const {
        return fmt::format("第{}宫 被 第{}宫和第{}宫 夹持",
            target_gong, left_gong, right_gong);
    }

    string KongGongInfo::to_string() const {
        string result = fmt::format("第{}宫空宫，借第{}宫星耀：", gong_index, dui_gong_index);
        for (const auto& star : jie_xing) {
            result += star + " ";
        }
        return result;
    }

    // ============= 主函数实现 =============

    SanFangSiZheng get_san_fang_si_zheng(int gong_index) {
        gong_index = fix_index(gong_index);
        
        return SanFangSiZheng{
            .ben_gong_index = gong_index,
            .dui_gong_index = fix_index(gong_index + 6),  // 对宫
            .cai_bo_index = fix_index(gong_index + 8),    // 财帛位（三合宫）
            .guan_lu_index = fix_index(gong_index + 4)    // 官禄位（三合宫）
        };
    }

    JiaGongInfo get_jia_gong_info(int gong_index) {
        gong_index = fix_index(gong_index);
        
        return JiaGongInfo{
            .target_gong = gong_index,
            .left_gong = fix_index(gong_index - 1),   // 前一宫
            .right_gong = fix_index(gong_index + 1)   // 后一宫
        };
    }

    bool is_kong_gong(const vector<string>& zhu_xing_list) {
        // 检查是否有14正曜
        static const set<string> zheng_yao = {
            "紫微", "天机", "太阳", "武曲", "天同", "廉贞",
            "天府", "太阴", "贪狼", "巨门", "天相", "天梁", "七杀", "破军"
        };
        
        for (const auto& star : zhu_xing_list) {
            if (zheng_yao.find(star) != zheng_yao.end()) {
                return false;  // 有主星，不是空宫
            }
        }
        
        return true;  // 无主星，是空宫
    }

    KongGongInfo get_jie_xing_info(int gong_index, const vector<string>& dui_gong_zhu_xing) {
        gong_index = fix_index(gong_index);
        int dui_gong = fix_index(gong_index + 6);
        
        KongGongInfo info{
            .gong_index = gong_index,
            .dui_gong_index = dui_gong,
            .jie_xing = {}
        };
        
        // 从对宫借主星
        static const set<string> zheng_yao = {
            "紫微", "天机", "太阳", "武曲", "天同", "廉贞",
            "天府", "太阴", "贪狼", "巨门", "天相", "天梁", "七杀", "破军"
        };
        
        for (const auto& star : dui_gong_zhu_xing) {
            if (zheng_yao.find(star) != zheng_yao.end()) {
                info.jie_xing.push_back(star);
            }
        }
        
        return info;
    }

    // ============= SanFangAnalyzer 实现 =============

    SanFangAnalyzer::SanFangAnalyzer(const array<vector<string>, 12>& stars_in_gong)
        : stars_in_gong_(stars_in_gong) {}

    vector<string> SanFangAnalyzer::get_san_fang_stars(int gong_index) const {
        auto san_fang = get_san_fang_si_zheng(gong_index);
        vector<string> result;
        
        for (int idx : san_fang.get_all_indices()) {
            const auto& stars = stars_in_gong_[idx];
            result.insert(result.end(), stars.begin(), stars.end());
        }
        
        return result;
    }

    bool SanFangAnalyzer::san_fang_has_star(int gong_index, const string& star_name) const {
        auto san_fang_stars = get_san_fang_stars(gong_index);
        return find(san_fang_stars.begin(), san_fang_stars.end(), star_name) != san_fang_stars.end();
    }

    bool SanFangAnalyzer::san_fang_has_all_stars(int gong_index, const vector<string>& star_names) const {
        auto san_fang_stars = get_san_fang_stars(gong_index);
        
        for (const auto& star : star_names) {
            if (find(san_fang_stars.begin(), san_fang_stars.end(), star) == san_fang_stars.end()) {
                return false;
            }
        }
        
        return true;
    }

    bool SanFangAnalyzer::san_fang_has_any_star(int gong_index, const vector<string>& star_names) const {
        auto san_fang_stars = get_san_fang_stars(gong_index);
        
        for (const auto& star : star_names) {
            if (find(san_fang_stars.begin(), san_fang_stars.end(), star) != san_fang_stars.end()) {
                return true;
            }
        }
        
        return false;
    }

    vector<string> SanFangAnalyzer::get_jia_gong_stars(int gong_index) const {
        auto jia_gong = get_jia_gong_info(gong_index);
        vector<string> result;
        
        // 左边宫的星
        const auto& left_stars = stars_in_gong_[jia_gong.left_gong];
        result.insert(result.end(), left_stars.begin(), left_stars.end());
        
        // 右边宫的星
        const auto& right_stars = stars_in_gong_[jia_gong.right_gong];
        result.insert(result.end(), right_stars.begin(), right_stars.end());
        
        return result;
    }

    bool SanFangAnalyzer::is_ji_xing_jia(int gong_index) const {
        auto jia_gong = get_jia_gong_info(gong_index);
        const auto& left_stars = stars_in_gong_[jia_gong.left_gong];
        const auto& right_stars = stars_in_gong_[jia_gong.right_gong];
        
        // 吉星列表
        static const set<string> ji_xing = {
            "左辅", "右弼", "文昌", "文曲", "天魁", "天钺", "禄存"
        };
        
        bool left_is_ji = false;
        bool right_is_ji = false;
        
        for (const auto& star : left_stars) {
            if (ji_xing.find(star) != ji_xing.end()) {
                left_is_ji = true;
                break;
            }
        }
        
        for (const auto& star : right_stars) {
            if (ji_xing.find(star) != ji_xing.end()) {
                right_is_ji = true;
                break;
            }
        }
        
        return left_is_ji && right_is_ji;  // 左右都有吉星才算夹
    }

    bool SanFangAnalyzer::is_sha_xing_jia(int gong_index) const {
        auto jia_gong = get_jia_gong_info(gong_index);
        const auto& left_stars = stars_in_gong_[jia_gong.left_gong];
        const auto& right_stars = stars_in_gong_[jia_gong.right_gong];
        
        // 煞星列表
        static const set<string> sha_xing = {
            "擎羊", "陀罗", "火星", "铃星", "地空", "地劫"
        };
        
        bool left_is_sha = false;
        bool right_is_sha = false;
        
        for (const auto& star : left_stars) {
            if (sha_xing.find(star) != sha_xing.end()) {
                left_is_sha = true;
                break;
            }
        }
        
        for (const auto& star : right_stars) {
            if (sha_xing.find(star) != sha_xing.end()) {
                right_is_sha = true;
                break;
            }
        }
        
        return left_is_sha && right_is_sha;  // 左右都有煞星才算夹
    }

    vector<KongGongInfo> SanFangAnalyzer::get_all_kong_gong() const {
        vector<KongGongInfo> result;
        
        for (int i = 0; i < 12; ++i) {
            if (is_kong_gong(stars_in_gong_[i])) {
                int dui_gong = fix_index(i + 6);
                auto kong_info = get_jie_xing_info(i, stars_in_gong_[dui_gong]);
                result.push_back(kong_info);
            }
        }
        
        return result;
    }

    bool SanFangAnalyzer::is_zhu_xing(const string& star_name) const {
        static const set<string> zheng_yao = {
            "紫微", "天机", "太阳", "武曲", "天同", "廉贞",
            "天府", "太阴", "贪狼", "巨门", "天相", "天梁", "七杀", "破军"
        };
        
        return zheng_yao.find(star_name) != zheng_yao.end();
    }

} // namespace ZhouYi::ZiWei

