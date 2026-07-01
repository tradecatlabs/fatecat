// 紫微斗数格局判断系统模块（实现）
module ZhouYi.ZiWei.GeJu;

import ZhouYi.GanZhi;
import ZhouYi.ZiWei.Constants;
import ZhouYi.ZiWei.SanFang;
import fmt;
import std;
import ZhouYi.ZhMapper;

namespace ZhouYi::ZiWei {
    using namespace std;

    // ============= 辅助函数 =============

    string GeJuInfo::to_string() const {
        string ji_xiong = is_ji ? "[吉格]" : "[凶格]";
        return fmt::format("{} {} (分数:{}) - {}", ji_xiong, name, score, description);
    }

    string ShuangXingInfo::to_string() const {
        return fmt::format("{}+{} 在第{}宫 - {} ({})",
            xing1_name, xing2_name, gong_index, xing_zhi, description);
    }

    // ============= GeJuAnalyzer 实现 =============

    GeJuAnalyzer::GeJuAnalyzer(
        const array<vector<string>, 12>& stars_in_gong,
        const array<DiZhi, 12>& gong_di_zhi,
        int ming_gong_index
    ) : stars_in_gong_(stars_in_gong),
        gong_di_zhi_(gong_di_zhi),
        ming_gong_index_(ming_gong_index),
        san_fang_analyzer_(stars_in_gong) {}

    vector<GeJuInfo> GeJuAnalyzer::analyze_all() const {
        vector<GeJuInfo> all_geju;
        
        auto ji_ge = analyze_ji_ge();
        auto xiong_ge = analyze_xiong_ge();
        
        all_geju.insert(all_geju.end(), ji_ge.begin(), ji_ge.end());
        all_geju.insert(all_geju.end(), xiong_ge.begin(), xiong_ge.end());
        
        return all_geju;
    }

    vector<GeJuInfo> GeJuAnalyzer::analyze_ji_ge() const {
        vector<GeJuInfo> ji_ge_list;
        
        // 检查各种吉格
        if (auto geju = check_zi_fu_tong_gong(); geju.has_value()) {
            ji_ge_list.push_back(geju.value());
        }
        
        if (auto geju = check_zi_fu_chao_yuan(); geju.has_value()) {
            ji_ge_list.push_back(geju.value());
        }
        
        if (auto geju = check_tian_fu_chao_yuan(); geju.has_value()) {
            ji_ge_list.push_back(geju.value());
        }
        
        if (auto geju = check_jun_chen_qing_hui(); geju.has_value()) {
            ji_ge_list.push_back(geju.value());
        }
        
        if (auto geju = check_fu_xiang_chao_yuan(); geju.has_value()) {
            ji_ge_list.push_back(geju.value());
        }
        
        if (auto geju = check_ji_yue_tong_liang(); geju.has_value()) {
            ji_ge_list.push_back(geju.value());
        }
        
        if (auto geju = check_ji_liang_jia_hui(); geju.has_value()) {
            ji_ge_list.push_back(geju.value());
        }
        
        if (auto geju = check_ri_yue_bing_ming(); geju.has_value()) {
            ji_ge_list.push_back(geju.value());
        }
        
        if (auto geju = check_ri_zhao_lei_men(); geju.has_value()) {
            ji_ge_list.push_back(geju.value());
        }
        
        if (auto geju = check_yue_lang_tian_men(); geju.has_value()) {
            ji_ge_list.push_back(geju.value());
        }
        
        if (auto geju = check_ming_zhu_chu_hai(); geju.has_value()) {
            ji_ge_list.push_back(geju.value());
        }
        
        if (auto geju = check_ri_yue_bo_zhao(); geju.has_value()) {
            ji_ge_list.push_back(geju.value());
        }
        
        if (auto geju = check_yang_liang_chang_lu(); geju.has_value()) {
            ji_ge_list.push_back(geju.value());
        }
        
        if (auto geju = check_tan_wu_tong_xing(); geju.has_value()) {
            ji_ge_list.push_back(geju.value());
        }
        
        if (auto geju = check_tan_ling_jia_hui(); geju.has_value()) {
            ji_ge_list.push_back(geju.value());
        }
        
        if (auto geju = check_huo_tan(); geju.has_value()) {
            ji_ge_list.push_back(geju.value());
        }
        
        if (auto geju = check_ling_tan(); geju.has_value()) {
            ji_ge_list.push_back(geju.value());
        }
        
        if (auto geju = check_san_qi_jia_hui(); geju.has_value()) {
            ji_ge_list.push_back(geju.value());
        }
        
        if (auto geju = check_shuang_lu_jia_ming(); geju.has_value()) {
            ji_ge_list.push_back(geju.value());
        }
        
        if (auto geju = check_shuang_lu_jia_cai(); geju.has_value()) {
            ji_ge_list.push_back(geju.value());
        }
        
        if (auto geju = check_ke_quan_lu_jia(); geju.has_value()) {
            ji_ge_list.push_back(geju.value());
        }
        
        if (auto geju = check_zuo_you_jia(); geju.has_value()) {
            ji_ge_list.push_back(geju.value());
        }
        
        if (auto geju = check_chang_qu_jia_ming(); geju.has_value()) {
            ji_ge_list.push_back(geju.value());
        }
        
        if (auto geju = check_kui_yue_jia_ming(); geju.has_value()) {
            ji_ge_list.push_back(geju.value());
        }
        
        if (auto geju = check_lu_ma_jiao_chi(); geju.has_value()) {
            ji_ge_list.push_back(geju.value());
        }
        
        if (auto geju = check_quan_lu_xun_feng(); geju.has_value()) {
            ji_ge_list.push_back(geju.value());
        }
        
        return ji_ge_list;
    }

    vector<GeJuInfo> GeJuAnalyzer::analyze_xiong_ge() const {
        vector<GeJuInfo> xiong_ge_list;
        
        if (auto geju = check_ling_chang_tuo_wu(); geju.has_value()) {
            xiong_ge_list.push_back(geju.value());
        }
        
        if (auto geju = check_ji_ji_tong_gong(); geju.has_value()) {
            xiong_ge_list.push_back(geju.value());
        }
        
        if (auto geju = check_ju_ri_tong_gong(); geju.has_value()) {
            xiong_ge_list.push_back(geju.value());
        }
        
        if (auto geju = check_ming_xiang_liang_jia(); geju.has_value()) {
            xiong_ge_list.push_back(geju.value());
        }
        
        if (auto geju = check_ma_tou_dai_jian(); geju.has_value()) {
            xiong_ge_list.push_back(geju.value());
        }
        
        if (auto geju = check_liang_ji_jia_ming(); geju.has_value()) {
            xiong_ge_list.push_back(geju.value());
        }
        
        if (auto geju = check_sha_xing_jia_ming(); geju.has_value()) {
            xiong_ge_list.push_back(geju.value());
        }
        
        if (auto geju = check_kong_jie_jia_ming(); geju.has_value()) {
            xiong_ge_list.push_back(geju.value());
        }
        
        if (auto geju = check_yang_tuo_jia_ji(); geju.has_value()) {
            xiong_ge_list.push_back(geju.value());
        }
        
        if (auto geju = check_si_sha_chong_ming(); geju.has_value()) {
            xiong_ge_list.push_back(geju.value());
        }
        
        if (auto geju = check_ming_gong_wu_zhu_xing(); geju.has_value()) {
            xiong_ge_list.push_back(geju.value());
        }
        
        return xiong_ge_list;
    }

    vector<ShuangXingInfo> GeJuAnalyzer::analyze_shuang_xing() const {
        vector<ShuangXingInfo> shuang_xing_list;
        
        for (int i = 0; i < 12; ++i) {
            auto zhu_xing = get_zhu_xing_in_gong(i);
            
            if (zhu_xing.size() == 2) {
                string xing1 = zhu_xing[0];
                string xing2 = zhu_xing[1];
                
                ShuangXingInfo info{
                    .type = ShuangXingType::Unknown,
                    .xing1_name = xing1,
                    .xing2_name = xing2,
                    .gong_index = i,
                    .xing_zhi = "",
                    .description = ""
                };
                
                // 判断组合类型
                if ((xing1 == "紫微" && xing2 == "天府") || (xing1 == "天府" && xing2 == "紫微")) {
                    info.type = ShuangXingType::ZiWei_TianFu;
                    info.xing_zhi = "帝王格";
                    info.description = "紫微天府同宫，尊贵之格，主富贵双全";
                } else if ((xing1 == "紫微" && xing2 == "贪狼") || (xing1 == "贪狼" && xing2 == "紫微")) {
                    info.type = ShuangXingType::ZiWei_TanLang;
                    info.xing_zhi = "桃花犯主";
                    info.description = "紫微贪狼，桃花犯主，利于交际";
                } else if ((xing1 == "紫微" && xing2 == "七杀") || (xing1 == "七杀" && xing2 == "紫微")) {
                    info.type = ShuangXingType::ZiWei_QiSha;
                    info.xing_zhi = "雄宿乾元";
                    info.description = "紫微七杀，威权显赫，主将相之材";
                } else if ((xing1 == "武曲" && xing2 == "贪狼") || (xing1 == "贪狼" && xing2 == "武曲")) {
                    info.type = ShuangXingType::WuQu_TanLang;
                    info.xing_zhi = "财星会桃花";
                    info.description = "武曲贪狼，先贫后富，晚年发达";
                } else if ((xing1 == "太阳" && xing2 == "太阴") || (xing1 == "太阴" && xing2 == "太阳")) {
                    info.type = ShuangXingType::TaiYang_TaiYin;
                    info.xing_zhi = "日月同辉";
                    info.description = "太阳太阴，阴阳调和，富贵之格";
                }
                // 可以继续添加更多组合...
                
                shuang_xing_list.push_back(info);
            }
        }
        
        return shuang_xing_list;
    }

    int GeJuAnalyzer::get_total_score() const {
        int total = 0;
        
        for (const auto& geju : analyze_all()) {
            total += geju.score;
        }
        
        return total;
    }

    // ============= 格局判断具体实现 =============

    optional<GeJuInfo> GeJuAnalyzer::check_zi_fu_tong_gong() const {
        // 检查命宫是否紫微天府同宫
        if (gong_has_all_stars(ming_gong_index_, {"紫微", "天府"})) {
            return GeJuInfo{
                .type = GeJuType::ZiFuTongGong,
                .name = "紫府同宫",
                .description = "紫微天府在命宫同坐，尊贵之格，主富贵双全，一生顺遂",
                .is_ji = true,
                .score = 80,
                .key_stars = {"紫微", "天府"},
                .key_gongs = {ming_gong_index_}
            };
        }
        
        return nullopt;
    }

    optional<GeJuInfo> GeJuAnalyzer::check_zi_fu_chao_yuan() const {
        // 紫微在命或财官，天府在三方四正
        if (gong_has_star(ming_gong_index_, "紫微") && 
            san_fang_analyzer_.san_fang_has_star(ming_gong_index_, "天府")) {
            return GeJuInfo{
                .type = GeJuType::ZiFuChaoYuan,
                .name = "紫府朝垣",
                .description = "紫微天府相朝，主贵显荣华",
                .is_ji = true,
                .score = 70,
                .key_stars = {"紫微", "天府"},
                .key_gongs = {ming_gong_index_}
            };
        }
        
        return nullopt;
    }

    optional<GeJuInfo> GeJuAnalyzer::check_tian_fu_chao_yuan() const {
        if (gong_has_star(ming_gong_index_, "天府") && 
            san_fang_analyzer_.san_fang_has_any_star(ming_gong_index_, {"禄存", "化禄"})) {
            return GeJuInfo{
                .type = GeJuType::TianFuChaoYuan,
                .name = "天府朝垣",
                .description = "天府守命逢禄，富贵之格",
                .is_ji = true,
                .score = 65,
                .key_stars = {"天府"},
                .key_gongs = {ming_gong_index_}
            };
        }
        
        return nullopt;
    }

    optional<GeJuInfo> GeJuAnalyzer::check_jun_chen_qing_hui() const {
        // 紫微、天相、天府等组合
        if (gong_has_star(ming_gong_index_, "紫微") && 
            san_fang_analyzer_.san_fang_has_all_stars(ming_gong_index_, {"天相", "天府"})) {
            return GeJuInfo{
                .type = GeJuType::JunChenQingHui,
                .name = "君臣庆会",
                .description = "紫微为君，天相天府为臣，君臣庆会，主富贵双全",
                .is_ji = true,
                .score = 75,
                .key_stars = {"紫微", "天相", "天府"},
                .key_gongs = {ming_gong_index_}
            };
        }
        
        return nullopt;
    }

    optional<GeJuInfo> GeJuAnalyzer::check_fu_xiang_chao_yuan() const {
        if (gong_has_all_stars(ming_gong_index_, {"天府", "天相"})) {
            return GeJuInfo{
                .type = GeJuType::FuXiangChaoYuan,
                .name = "府相朝垣",
                .description = "天府天相守命，财官双美",
                .is_ji = true,
                .score = 70,
                .key_stars = {"天府", "天相"},
                .key_gongs = {ming_gong_index_}
            };
        }
        
        return nullopt;
    }

    optional<GeJuInfo> GeJuAnalyzer::check_ji_yue_tong_liang() const {
        // 天机、天同、天梁、太阴会于寅申巳亥宫
        vector<string> ji_yue_stars = {"天机", "太阴", "天同", "天梁"};
        
        if (san_fang_analyzer_.san_fang_has_all_stars(ming_gong_index_, ji_yue_stars)) {
            return GeJuInfo{
                .type = GeJuType::JiYueTongLiang,
                .name = "机月同梁格",
                .description = "天机太阴天同天梁会合，清贵之格，适宜公职、学术",
                .is_ji = true,
                .score = 60,
                .key_stars = ji_yue_stars,
                .key_gongs = {ming_gong_index_}
            };
        }
        
        return nullopt;
    }

    optional<GeJuInfo> GeJuAnalyzer::check_ri_yue_bing_ming() const {
        // 太阳太阴在卯酉宫
        if (gong_has_all_stars(ming_gong_index_, {"太阳", "太阴"})) {
            DiZhi di_zhi = get_gong_di_zhi(ming_gong_index_);
            // 检查是否在卯宫或酉宫
            if (di_zhi == DiZhi::Mao || di_zhi == DiZhi::You) {
                return GeJuInfo{
                    .type = GeJuType::RiYueBingMing,
                    .name = "日月并明",
                    .description = "太阳太阴在卯酉宫，日月同辉，富贵之格",
                    .is_ji = true,
                    .score = 80,
                    .key_stars = {"太阳", "太阴"},
                    .key_gongs = {ming_gong_index_}
                };
            }
        }
        
        return nullopt;
    }

    optional<GeJuInfo> GeJuAnalyzer::check_yue_lang_tian_men() const {
        // 太阴在亥宫
        if (gong_has_star(ming_gong_index_, "太阴")) {
            DiZhi di_zhi = get_gong_di_zhi(ming_gong_index_);
            // 检查是否在亥宫
            if (di_zhi == DiZhi::Hai) {
                return GeJuInfo{
                    .type = GeJuType::YueLangTianMen,
                    .name = "月朗天门",
                    .description = "太阴居亥宫旺地，月朗天门，清贵之格",
                    .is_ji = true,
                    .score = 70,
                    .key_stars = {"太阴"},
                    .key_gongs = {ming_gong_index_}
                };
            }
        }
        
        return nullopt;
    }

    optional<GeJuInfo> GeJuAnalyzer::check_ming_zhu_chu_hai() const {
        // 太阴在酉宫
        if (gong_has_star(ming_gong_index_, "太阴")) {
            DiZhi di_zhi = get_gong_di_zhi(ming_gong_index_);
            // 检查是否在酉宫
            if (di_zhi == DiZhi::You) {
                return GeJuInfo{
                    .type = GeJuType::MingZhuChuHai,
                    .name = "明珠出海",
                    .description = "太阴居酉宫得地，明珠出海，清秀之格",
                    .is_ji = true,
                    .score = 65,
                    .key_stars = {"太阴"},
                    .key_gongs = {ming_gong_index_}
                };
            }
        }
        
        return nullopt;
    }

    optional<GeJuInfo> GeJuAnalyzer::check_yang_liang_chang_lu() const {
        if (gong_has_all_stars(ming_gong_index_, {"太阳", "天梁"}) &&
            san_fang_analyzer_.san_fang_has_all_stars(ming_gong_index_, {"文昌", "禄存"})) {
            return GeJuInfo{
                .type = GeJuType::YangLiangChangLu,
                .name = "阳梁昌禄格",
                .description = "太阳天梁会昌禄，清贵之格，主功名显赫",
                .is_ji = true,
                .score = 70,
                .key_stars = {"太阳", "天梁", "文昌", "禄存"},
                .key_gongs = {ming_gong_index_}
            };
        }
        
        return nullopt;
    }

    optional<GeJuInfo> GeJuAnalyzer::check_tan_wu_tong_xing() const {
        // 贪狼武曲在丑未宫
        if (gong_has_all_stars(ming_gong_index_, {"贪狼", "武曲"})) {
            return GeJuInfo{
                .type = GeJuType::TanWuTongXing,
                .name = "贪武同行",
                .description = "贪狼武曲同宫于丑未，横发之格",
                .is_ji = true,
                .score = 65,
                .key_stars = {"贪狼", "武曲"},
                .key_gongs = {ming_gong_index_}
            };
        }
        
        return nullopt;
    }

    optional<GeJuInfo> GeJuAnalyzer::check_huo_tan() const {
        if (gong_has_all_stars(ming_gong_index_, {"贪狼", "火星"})) {
            return GeJuInfo{
                .type = GeJuType::HuoTanGeJu,
                .name = "火贪格",
                .description = "火星贪狼，突发之财，主横发",
                .is_ji = true,
                .score = 60,
                .key_stars = {"贪狼", "火星"},
                .key_gongs = {ming_gong_index_}
            };
        }
        
        return nullopt;
    }

    optional<GeJuInfo> GeJuAnalyzer::check_ling_tan() const {
        if (gong_has_all_stars(ming_gong_index_, {"贪狼", "铃星"})) {
            return GeJuInfo{
                .type = GeJuType::LingTanGeJu,
                .name = "铃贪格",
                .description = "铃星贪狼，暗发之财",
                .is_ji = true,
                .score = 55,
                .key_stars = {"贪狼", "铃星"},
                .key_gongs = {ming_gong_index_}
            };
        }
        
        return nullopt;
    }

    optional<GeJuInfo> GeJuAnalyzer::check_ji_liang_jia_hui() const {
        // 天机天梁在三方四正会合
        if ((gong_has_star(ming_gong_index_, "天机") && san_fang_analyzer_.san_fang_has_star(ming_gong_index_, "天梁")) ||
            (gong_has_star(ming_gong_index_, "天梁") && san_fang_analyzer_.san_fang_has_star(ming_gong_index_, "天机"))) {
            return GeJuInfo{
                .type = GeJuType::JiLiangJiaHui,
                .name = "机梁夹会",
                .description = "天机天梁会合，清贵之格，宜学术研究",
                .is_ji = true,
                .score = 60,
                .key_stars = {"天机", "天梁"},
                .key_gongs = {ming_gong_index_}
            };
        }
        
        return nullopt;
    }

    optional<GeJuInfo> GeJuAnalyzer::check_ri_zhao_lei_men() const {
        // 太阳在卯宫
        if (gong_has_star(ming_gong_index_, "太阳")) {
            DiZhi di_zhi = get_gong_di_zhi(ming_gong_index_);
            if (di_zhi == DiZhi::Mao) {
                return GeJuInfo{
                    .type = GeJuType::RiZhaoLeiMen,
                    .name = "日照雷门",
                    .description = "太阳居卯宫旺地，日照雷门，富贵之格",
                    .is_ji = true,
                    .score = 70,
                    .key_stars = {"太阳"},
                    .key_gongs = {ming_gong_index_}
                };
            }
        }
        
        return nullopt;
    }

    optional<GeJuInfo> GeJuAnalyzer::check_ri_yue_bo_zhao() const {
        // 太阳太阴在三方夹照命宫
        auto san_fang = get_san_fang_si_zheng(ming_gong_index_);
        bool has_tai_yang = false;
        bool has_tai_yin = false;
        
        for (int gong : san_fang.get_all_indices()) {
            if (gong != ming_gong_index_) {  // 不包括本宫
                if (gong_has_star(gong, "太阳")) has_tai_yang = true;
                if (gong_has_star(gong, "太阴")) has_tai_yin = true;
            }
        }
        
        if (has_tai_yang && has_tai_yin) {
            return GeJuInfo{
                .type = GeJuType::RiYueBoZhao,
                .name = "日月夹照",
                .description = "日月在三方夹照命宫，阴阳和合，富贵之格",
                .is_ji = true,
                .score = 65,
                .key_stars = {"太阳", "太阴"},
                .key_gongs = {ming_gong_index_}
            };
        }
        
        return nullopt;
    }

    optional<GeJuInfo> GeJuAnalyzer::check_tan_ling_jia_hui() const {
        // 贪狼铃星在三方会合
        if ((gong_has_star(ming_gong_index_, "贪狼") && san_fang_analyzer_.san_fang_has_star(ming_gong_index_, "铃星")) ||
            (gong_has_star(ming_gong_index_, "铃星") && san_fang_analyzer_.san_fang_has_star(ming_gong_index_, "贪狼"))) {
            return GeJuInfo{
                .type = GeJuType::TanLingJiaHui,
                .name = "贪铃夹会",
                .description = "贪狼铃星会合，横发之财",
                .is_ji = true,
                .score = 55,
                .key_stars = {"贪狼", "铃星"},
                .key_gongs = {ming_gong_index_}
            };
        }
        
        return nullopt;
    }

    optional<GeJuInfo> GeJuAnalyzer::check_san_qi_jia_hui() const {
        // 化禄、化权、化科会于三方四正
        if (san_fang_analyzer_.san_fang_has_all_stars(ming_gong_index_, {"化禄", "化权", "化科"})) {
            return GeJuInfo{
                .type = GeJuType::SanQiJiaHui,
                .name = "三奇嘉会",
                .description = "化禄化权化科会于三方四正，极贵之格",
                .is_ji = true,
                .score = 80,
                .key_stars = {"化禄", "化权", "化科"},
                .key_gongs = {ming_gong_index_}
            };
        }
        
        return nullopt;
    }

    optional<GeJuInfo> GeJuAnalyzer::check_shuang_lu_jia_ming() const {
        auto jia_gong = get_jia_gong_info(ming_gong_index_);
        
        bool left_has_lu = gong_has_any_star(jia_gong.left_gong, {"禄存", "化禄"});
        bool right_has_lu = gong_has_any_star(jia_gong.right_gong, {"禄存", "化禄"});
        
        if (left_has_lu && right_has_lu) {
            return GeJuInfo{
                .type = GeJuType::ShuangLuJiaMing,
                .name = "双禄夹命",
                .description = "禄存化禄夹命，财禄丰厚",
                .is_ji = true,
                .score = 70,
                .key_stars = {"禄存", "化禄"},
                .key_gongs = {ming_gong_index_, jia_gong.left_gong, jia_gong.right_gong}
            };
        }
        
        return nullopt;
    }

    optional<GeJuInfo> GeJuAnalyzer::check_shuang_lu_jia_cai() const {
        // 找到财帛宫
        auto san_fang = get_san_fang_si_zheng(ming_gong_index_);
        int cai_bo_gong = san_fang.cai_bo_index;
        
        auto jia_gong = get_jia_gong_info(cai_bo_gong);
        
        bool left_has_lu = gong_has_any_star(jia_gong.left_gong, {"禄存", "化禄"});
        bool right_has_lu = gong_has_any_star(jia_gong.right_gong, {"禄存", "化禄"});
        
        if (left_has_lu && right_has_lu) {
            return GeJuInfo{
                .type = GeJuType::ShuangLuJiaCai,
                .name = "双禄夹财",
                .description = "禄存化禄夹财帛宫，财源广进",
                .is_ji = true,
                .score = 68,
                .key_stars = {"禄存", "化禄"},
                .key_gongs = {cai_bo_gong, jia_gong.left_gong, jia_gong.right_gong}
            };
        }
        
        return nullopt;
    }

    optional<GeJuInfo> GeJuAnalyzer::check_ke_quan_lu_jia() const {
        auto jia_gong = get_jia_gong_info(ming_gong_index_);
        
        // 检查左右宫是否有化科、化权、化禄中的任意两个
        vector<string> si_hua_list = {"化科", "化权", "化禄"};
        int count = 0;
        
        for (const auto& si_hua : si_hua_list) {
            if (gong_has_star(jia_gong.left_gong, si_hua) || gong_has_star(jia_gong.right_gong, si_hua)) {
                count++;
            }
        }
        
        if (count >= 2) {
            return GeJuInfo{
                .type = GeJuType::KeQuanLuJia,
                .name = "科权禄夹",
                .description = "化科化权化禄夹命，权贵之格",
                .is_ji = true,
                .score = 75,
                .key_stars = {"化科", "化权", "化禄"},
                .key_gongs = {ming_gong_index_, jia_gong.left_gong, jia_gong.right_gong}
            };
        }
        
        return nullopt;
    }

    optional<GeJuInfo> GeJuAnalyzer::check_zuo_you_jia() const{
        auto jia_gong = get_jia_gong_info(ming_gong_index_);
        
        bool left_has_zuo = gong_has_star(jia_gong.left_gong, "左辅");
        bool right_has_you = gong_has_star(jia_gong.right_gong, "右弼");
        
        if (left_has_zuo && right_has_you) {
            return GeJuInfo{
                .type = GeJuType::ZuoYouJiaMing,
                .name = "左右夹命",
                .description = "左辅右弼夹命，贵人扶持",
                .is_ji = true,
                .score = 65,
                .key_stars = {"左辅", "右弼"},
                .key_gongs = {ming_gong_index_, jia_gong.left_gong, jia_gong.right_gong}
            };
        }
        
        return nullopt;
    }

    optional<GeJuInfo> GeJuAnalyzer::check_chang_qu_jia_ming() const {
        auto jia_gong = get_jia_gong_info(ming_gong_index_);
        
        bool left_has_chang = gong_has_star(jia_gong.left_gong, "文昌");
        bool right_has_qu = gong_has_star(jia_gong.right_gong, "文曲");
        bool left_has_qu = gong_has_star(jia_gong.left_gong, "文曲");
        bool right_has_chang = gong_has_star(jia_gong.right_gong, "文昌");
        
        if ((left_has_chang && right_has_qu) || (left_has_qu && right_has_chang)) {
            return GeJuInfo{
                .type = GeJuType::ChangQuJiaMing,
                .name = "昌曲夹命",
                .description = "文昌文曲夹命，主文名科甲",
                .is_ji = true,
                .score = 70,
                .key_stars = {"文昌", "文曲"},
                .key_gongs = {ming_gong_index_, jia_gong.left_gong, jia_gong.right_gong}
            };
        }
        
        return nullopt;
    }

    optional<GeJuInfo> GeJuAnalyzer::check_kui_yue_jia_ming() const {
        auto jia_gong = get_jia_gong_info(ming_gong_index_);
        
        bool left_has_kui = gong_has_star(jia_gong.left_gong, "天魁");
        bool right_has_yue = gong_has_star(jia_gong.right_gong, "天钺");
        bool left_has_yue = gong_has_star(jia_gong.left_gong, "天钺");
        bool right_has_kui = gong_has_star(jia_gong.right_gong, "天魁");
        
        if ((left_has_kui && right_has_yue) || (left_has_yue && right_has_kui)) {
            return GeJuInfo{
                .type = GeJuType::KuiYueJiaMing,
                .name = "魁钺夹命",
                .description = "天魁天钺夹命，贵人提携，主显贵",
                .is_ji = true,
                .score = 72,
                .key_stars = {"天魁", "天钺"},
                .key_gongs = {ming_gong_index_, jia_gong.left_gong, jia_gong.right_gong}
            };
        }
        
        return nullopt;
    }

    optional<GeJuInfo> GeJuAnalyzer::check_lu_ma_jiao_chi() const {
        // 禄存天马同宫或会合
        if (gong_has_all_stars(ming_gong_index_, {"禄存", "天马"}) ||
            (gong_has_star(ming_gong_index_, "禄存") && san_fang_analyzer_.san_fang_has_star(ming_gong_index_, "天马")) ||
            (gong_has_star(ming_gong_index_, "天马") && san_fang_analyzer_.san_fang_has_star(ming_gong_index_, "禄存"))) {
            return GeJuInfo{
                .type = GeJuType::LuMaJiaoChiGeJu,
                .name = "禄马交驰",
                .description = "禄存天马交会，主富贵双全，利经商远行",
                .is_ji = true,
                .score = 68,
                .key_stars = {"禄存", "天马"},
                .key_gongs = {ming_gong_index_}
            };
        }
        
        return nullopt;
    }

    optional<GeJuInfo> GeJuAnalyzer::check_quan_lu_xun_feng() const {
        // 化权化禄在命宫或三方四正
        if (san_fang_analyzer_.san_fang_has_all_stars(ming_gong_index_, {"化权", "化禄"})) {
            return GeJuInfo{
                .type = GeJuType::QuanLuXunFeng,
                .name = "权禄巡逢",
                .description = "化权化禄巡逢，主权贵富足",
                .is_ji = true,
                .score = 70,
                .key_stars = {"化权", "化禄"},
                .key_gongs = {ming_gong_index_}
            };
        }
        
        return nullopt;
    }

    // ============= 凶格判断 =============

    optional<GeJuInfo> GeJuAnalyzer::check_ling_chang_tuo_wu() const {
        if (gong_has_all_stars(ming_gong_index_, {"铃星", "文昌", "陀罗", "武曲"})) {
            return GeJuInfo{
                .type = GeJuType::LingChangTuoWu,
                .name = "铃昌陀武",
                .description = "铃星文昌陀罗武曲同宫，大凶之格，易遭刑克",
                .is_ji = false,
                .score = -70,
                .key_stars = {"铃星", "文昌", "陀罗", "武曲"},
                .key_gongs = {ming_gong_index_}
            };
        }
        
        return nullopt;
    }

    optional<GeJuInfo> GeJuAnalyzer::check_ji_ji_tong_gong() const {
        if (gong_has_all_stars(ming_gong_index_, {"巨门", "天机"})) {
            DiZhi di_zhi = get_gong_di_zhi(ming_gong_index_);
            // 检查是否在辰宫或戌宫
            if (di_zhi == DiZhi::Chen || di_zhi == DiZhi::Xu) {
                return GeJuInfo{
                    .type = GeJuType::JiJiTongGong,
                    .name = "巨机同宫",
                    .description = "巨门天机同宫于辰戌，口舌是非多，劳碌奔波",
                    .is_ji = false,
                    .score = -50,
                    .key_stars = {"巨门", "天机"},
                    .key_gongs = {ming_gong_index_}
                };
            }
        }
        
        return nullopt;
    }

    optional<GeJuInfo> GeJuAnalyzer::check_ma_tou_dai_jian() const {
        // 擎羊在午宫守命
        if (gong_has_star(ming_gong_index_, "擎羊")) {
            DiZhi di_zhi = get_gong_di_zhi(ming_gong_index_);
            // 检查是否在午宫
            if (di_zhi == DiZhi::Wu) {
                return GeJuInfo{
                    .type = GeJuType::MaTouDaiJian,
                    .name = "马头带箭",
                    .description = "擎羊居午宫守命，马头带箭，刑克严重，易有血光之灾",
                    .is_ji = false,
                    .score = -65,
                    .key_stars = {"擎羊"},
                    .key_gongs = {ming_gong_index_}
                };
            }
        }
        
        return nullopt;
    }

    optional<GeJuInfo> GeJuAnalyzer::check_sha_xing_jia_ming() const {
        if (san_fang_analyzer_.is_sha_xing_jia(ming_gong_index_)) {
            return GeJuInfo{
                .type = GeJuType::HuoLingJiaMing,
                .name = "煞星夹命",
                .description = "煞星夹命，困顿辛劳",
                .is_ji = false,
                .score = -55,
                .key_stars = {"擎羊", "陀罗", "火星", "铃星"},
                .key_gongs = {ming_gong_index_}
            };
        }
        
        return nullopt;
    }

    optional<GeJuInfo> GeJuAnalyzer::check_kong_jie_jia_ming() const {
        auto jia_gong = get_jia_gong_info(ming_gong_index_);
        
        bool left_has_kong = gong_has_star(jia_gong.left_gong, "地空");
        bool right_has_jie = gong_has_star(jia_gong.right_gong, "地劫");
        bool left_has_jie = gong_has_star(jia_gong.left_gong, "地劫");
        bool right_has_kong = gong_has_star(jia_gong.right_gong, "地空");
        
        if ((left_has_kong && right_has_jie) || (left_has_jie && right_has_kong)) {
            return GeJuInfo{
                .type = GeJuType::KongJieJiaMing,
                .name = "空劫夹命",
                .description = "地空地劫夹命，财运不聚，理想高远",
                .is_ji = false,
                .score = -50,
                .key_stars = {"地空", "地劫"},
                .key_gongs = {ming_gong_index_, jia_gong.left_gong, jia_gong.right_gong}
            };
        }
        
        return nullopt;
    }

    optional<GeJuInfo> GeJuAnalyzer::check_ju_ri_tong_gong() const {
        // 巨门太阳同宫
        if (gong_has_all_stars(ming_gong_index_, {"巨门", "太阳"})) {
            return GeJuInfo{
                .type = GeJuType::JuRiTongGong,
                .name = "巨日同宫",
                .description = "巨门太阳同宫，口舌是非多，宜外交公职",
                .is_ji = false,
                .score = -40,
                .key_stars = {"巨门", "太阳"},
                .key_gongs = {ming_gong_index_}
            };
        }
        
        return nullopt;
    }

    optional<GeJuInfo> GeJuAnalyzer::check_ming_xiang_liang_jia() const {
        // 命宫无正曜（空宫）
        auto zhu_xing = get_zhu_xing_in_gong(ming_gong_index_);
        
        if (zhu_xing.empty()) {
            return GeJuInfo{
                .type = GeJuType::MingXiangLiangJia,
                .name = "命无正曜",
                .description = "命宫空宫无主星，需借对宫之星，命运多变",
                .is_ji = false,
                .score = -30,
                .key_stars = {},
                .key_gongs = {ming_gong_index_}
            };
        }
        
        return nullopt;
    }

    optional<GeJuInfo> GeJuAnalyzer::check_liang_ji_jia_ming() const {
        auto jia_gong = get_jia_gong_info(ming_gong_index_);
        
        bool left_has_yang = gong_has_star(jia_gong.left_gong, "擎羊");
        bool right_has_tuo = gong_has_star(jia_gong.right_gong, "陀罗");
        bool left_has_tuo = gong_has_star(jia_gong.left_gong, "陀罗");
        bool right_has_yang = gong_has_star(jia_gong.right_gong, "擎羊");
        
        if ((left_has_yang && right_has_tuo) || (left_has_tuo && right_has_yang)) {
            return GeJuInfo{
                .type = GeJuType::LiangJiJiaMing,
                .name = "羊陀夹命",
                .description = "擎羊陀罗夹命，进退失据，劳碌辛苦",
                .is_ji = false,
                .score = -60,
                .key_stars = {"擎羊", "陀罗"},
                .key_gongs = {ming_gong_index_, jia_gong.left_gong, jia_gong.right_gong}
            };
        }
        
        return nullopt;
    }

    optional<GeJuInfo> GeJuAnalyzer::check_yang_tuo_jia_ji() const {
        // 化忌被擎羊陀罗夹
        auto jia_gong = get_jia_gong_info(ming_gong_index_);
        
        bool ming_has_ji = gong_has_star(ming_gong_index_, "化忌");
        bool left_has_yang_or_tuo = gong_has_any_star(jia_gong.left_gong, {"擎羊", "陀罗"});
        bool right_has_yang_or_tuo = gong_has_any_star(jia_gong.right_gong, {"擎羊", "陀罗"});
        
        if (ming_has_ji && left_has_yang_or_tuo && right_has_yang_or_tuo) {
            return GeJuInfo{
                .type = GeJuType::YangTuoJiaJi,
                .name = "羊陀夹忌",
                .description = "化忌被羊陀夹持，凶上加凶，灾祸频生",
                .is_ji = false,
                .score = -70,
                .key_stars = {"擎羊", "陀罗", "化忌"},
                .key_gongs = {ming_gong_index_, jia_gong.left_gong, jia_gong.right_gong}
            };
        }
        
        return nullopt;
    }

    optional<GeJuInfo> GeJuAnalyzer::check_si_sha_chong_ming() const {
        // 四煞（擎羊陀罗火星铃星）在三方四正冲照命宫
        int sha_count = 0;
        vector<string> si_sha = {"擎羊", "陀罗", "火星", "铃星"};
        
        for (const auto& sha : si_sha) {
            if (san_fang_analyzer_.san_fang_has_star(ming_gong_index_, sha)) {
                sha_count++;
            }
        }
        
        if (sha_count >= 3) {
            return GeJuInfo{
                .type = GeJuType::SiShaChongMing,
                .name = "四煞冲命",
                .description = "四煞聚会冲命，劳碌奔波，多灾多难",
                .is_ji = false,
                .score = -65,
                .key_stars = si_sha,
                .key_gongs = {ming_gong_index_}
            };
        }
        
        return nullopt;
    }

    optional<GeJuInfo> GeJuAnalyzer::check_ming_gong_wu_zhu_xing() const {
        // 与check_ming_xiang_liang_jia类似，但更侧重于无主星的情况
        auto zhu_xing = get_zhu_xing_in_gong(ming_gong_index_);
        
        if (zhu_xing.empty()) {
            return GeJuInfo{
                .type = GeJuType::MinggongWuZhuXing,
                .name = "命宫无主星",
                .description = "命宫无正曜主星，格局较弱，需借对宫",
                .is_ji = false,
                .score = -25,
                .key_stars = {},
                .key_gongs = {ming_gong_index_}
            };
        }
        
        return nullopt;
    }

    // ============= 辅助函数 =============

    /**
     * @brief 获取宫位的地支
     */
    DiZhi GeJuAnalyzer::get_gong_di_zhi(int gong_index) const {
        return gong_di_zhi_[fix_index(gong_index)];
    }

    bool GeJuAnalyzer::gong_has_star(int gong_index, const string& star_name) const {
        const auto& stars = stars_in_gong_[fix_index(gong_index)];
        return find(stars.begin(), stars.end(), star_name) != stars.end();
    }

    bool GeJuAnalyzer::gong_has_all_stars(int gong_index, const vector<string>& stars) const {
        const auto& gong_stars = stars_in_gong_[fix_index(gong_index)];
        
        for (const auto& star : stars) {
            if (find(gong_stars.begin(), gong_stars.end(), star) == gong_stars.end()) {
                return false;
            }
        }
        
        return true;
    }

    bool GeJuAnalyzer::gong_has_any_star(int gong_index, const vector<string>& stars) const {
        const auto& gong_stars = stars_in_gong_[fix_index(gong_index)];
        
        for (const auto& star : stars) {
            if (find(gong_stars.begin(), gong_stars.end(), star) != gong_stars.end()) {
                return true;
            }
        }
        
        return false;
    }

    vector<string> GeJuAnalyzer::get_zhu_xing_in_gong(int gong_index) const {
        vector<string> zhu_xing;
        static const set<string> zheng_yao = {
            "紫微", "天机", "太阳", "武曲", "天同", "廉贞",
            "天府", "太阴", "贪狼", "巨门", "天相", "天梁", "七杀", "破军"
        };
        
        const auto& stars = stars_in_gong_[fix_index(gong_index)];
        for (const auto& star : stars) {
            if (zheng_yao.find(star) != zheng_yao.end()) {
                zhu_xing.push_back(star);
            }
        }
        
        return zhu_xing;
    }

} // namespace ZhouYi::ZiWei

