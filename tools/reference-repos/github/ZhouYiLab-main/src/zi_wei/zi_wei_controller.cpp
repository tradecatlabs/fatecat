// 紫微斗数控制器实现
module ZhouYi.ZiWei.Controller;

import ZhouYi.GanZhi;
import ZhouYi.ZiWei;
import ZhouYi.ZiWei.SiHua;
import ZhouYi.ZiWei.SanFang;
import ZhouYi.ZiWei.GeJu;
import ZhouYi.ZiWei.StarDocument;
import ZhouYi.ZiWei.Horoscope;
import ZhouYi.ZhMapper;
import ZhouYi.tyme;
import fmt;
import nlohmann.json;
import std;

using json = nlohmann::json;

namespace ZhouYi::ZiWei {
    using namespace std;
    using namespace ZhouYi::GanZhi;
    using namespace ZhouYi::Mapper;

    void pai_pan_and_print_solar(int year, int month, int day, int hour, bool is_male) {
        try {
            auto result = pai_pan_solar(year, month, day, hour, is_male);
            fmt::print("{}\n", result.to_string());
        } catch (const exception& e) {
            fmt::print("[错误] 排盘错误: {}\n", e.what());
        }
    }

    void pai_pan_and_print_lunar(int year, int month, int day, int hour, 
                                  bool is_male, bool is_leap_month) {
        try {
            auto result = pai_pan_lunar(year, month, day, hour, is_male, is_leap_month);
            fmt::print("{}\n", result.to_string());
        } catch (const exception& e) {
            fmt::print("[错误] 排盘错误: {}\n", e.what());
        }
    }

    void display_palace_detail(const ZiWeiResult& result, GongWei gong_wei) {
        try {
            const auto& palace = result.get_palace(gong_wei);
            fmt::print("\n{}\n", palace.to_string());
        } catch (const exception& e) {
            fmt::print("[错误] 获取宫位错误: {}\n", e.what());
        }
    }

    void display_ming_gong_san_fang_si_zheng(const ZiWeiResult& result) {
        fmt::print("\n\n");
        fmt::print("       命宫三方四正\n");
        fmt::print("\n\n");
        
        // 命宫
        fmt::print("【命宫】\n");
        display_palace_detail(result, GongWei::MingGong);
        
        // 财帛宫（三方）
        fmt::print("\n【财帛宫（三方）】\n");
        display_palace_detail(result, GongWei::CaiBoGong);
        
        // 官禄宫（三方）
        fmt::print("\n【官禄宫（三方）】\n");
        display_palace_detail(result, GongWei::GuanLuGong);
        
        // 迁移宫（对宫，四正）
        fmt::print("\n【迁移宫（对宫）】\n");
        display_palace_detail(result, GongWei::QianYiGong);
    }

    string export_to_json(const ZiWeiResult& result) {
        json j;
        
        // 基本信息
        j["solar_date"] = result.solar_day.to_string();
        j["lunar_date"] = result.lunar_day.to_string();
        j["lunar_hour"] = result.lunar_hour.to_string();
        j["gender"] = result.is_male ? "男" : "女";
        
        // 四柱
        j["si_zhu"]["year"] = result.year_pillar.to_string();
        j["si_zhu"]["month"] = result.month_pillar.to_string();
        j["si_zhu"]["day"] = result.day_pillar.to_string();
        j["si_zhu"]["hour"] = result.hour_pillar.to_string();
        
        // 命盘核心数据
        j["wu_xing_ju"] = string(to_zh(result.wu_xing_ju));
        j["ming_gong_index"] = result.ming_gong_index;
        j["shen_gong_index"] = result.shen_gong_index;
        
        // 十二宫
        j["palaces"] = json::array();
        for (const auto& palace : result.palaces) {
            json p;
            p["name"] = string(to_zh(palace.gong_data.gong_wei));
            p["gan_zhi"] = fmt::format("{}{}",
                string(GanZhi::Mapper::to_zh(palace.gong_data.tian_gan)),
                string(GanZhi::Mapper::to_zh(palace.gong_data.di_zhi)));
            p["is_ming_palace"] = palace.gong_data.is_ming_palace;
            p["is_body_palace"] = palace.gong_data.is_body_palace;
            
            // 主星
            p["zhu_xing"] = json::array();
            for (const auto& star : palace.zhu_xing) {
                json s;
                s["name"] = star.name;
                s["liang_du"] = string(to_zh(star.liang_du));
                if (star.si_hua.has_value()) {
                    s["si_hua"] = string(to_zh(*star.si_hua));
                }
                p["zhu_xing"].push_back(s);
            }
            
            // 辅星
            p["fu_xing"] = json::array();
            for (const auto& star : palace.fu_xing) {
                p["fu_xing"].push_back(star.name);
            }
            
            // 煞星
            p["sha_xing"] = json::array();
            for (const auto& star : palace.sha_xing) {
                p["sha_xing"].push_back(star.name);
            }
            
            j["palaces"].push_back(p);
        }
        
        return j.dump(2);
    }

    // ============= 辅助函数：准备数据 =============
    
    namespace {
        // 准备宫干地支数据
        array<pair<TianGan, DiZhi>, 12> prepare_gong_gan_zhi(const ZiWeiResult& result) {
            array<pair<TianGan, DiZhi>, 12> gong_gan_zhi;
            for (int i = 0; i < 12; ++i) {
                gong_gan_zhi[i] = {
                    result.palaces[i].gong_data.tian_gan,
                    result.palaces[i].gong_data.di_zhi
                };
            }
            return gong_gan_zhi;
        }
        
        // 准备星耀列表
        array<vector<string>, 12> prepare_stars_in_gong(const ZiWeiResult& result) {
            array<vector<string>, 12> stars_in_gong;
            for (int i = 0; i < 12; ++i) {
                for (const auto& star : result.palaces[i].zhu_xing) {
                    stars_in_gong[i].push_back(star.name);
                }
                for (const auto& star : result.palaces[i].fu_xing) {
                    stars_in_gong[i].push_back(star.name);
                }
                for (const auto& star : result.palaces[i].sha_xing) {
                    stars_in_gong[i].push_back(star.name);
                }
            }
            return stars_in_gong;
        }
        
        // 准备地支列表
        array<DiZhi, 12> prepare_gong_di_zhi(const ZiWeiResult& result) {
            array<DiZhi, 12> gong_di_zhi;
            for (int i = 0; i < 12; ++i) {
                gong_di_zhi[i] = result.palaces[i].gong_data.di_zhi;
            }
            return gong_di_zhi;
        }
    }

    // ============= 四化分析功能实现 =============
    
    void display_gong_gan_si_hua(const ZiWeiResult& result) {
        fmt::print("\n\n");
        fmt::print("       宫干四化分析\n");
        fmt::print("\n\n");
        
        auto gong_gan_zhi = prepare_gong_gan_zhi(result);
        auto stars_in_gong = prepare_stars_in_gong(result);
        
        SiHuaSystem si_hua_system(gong_gan_zhi, stars_in_gong);
        
        for (const auto& gong_si_hua : si_hua_system.get_all_gong_gan_si_hua()) {
            fmt::print("{}\n", gong_si_hua.to_string());
        }
    }
    
    void display_zi_hua_analysis(const ZiWeiResult& result) {
        fmt::print("\n\n");
        fmt::print("       自化分析\n");
        fmt::print("\n\n");
        
        auto gong_gan_zhi = prepare_gong_gan_zhi(result);
        auto stars_in_gong = prepare_stars_in_gong(result);
        
        SiHuaSystem si_hua_system(gong_gan_zhi, stars_in_gong);
        auto zi_hua_list = si_hua_system.get_all_zi_hua();
        
        if (zi_hua_list.empty()) {
            fmt::print("无自化现象\n");
        } else {
            for (const auto& zi_hua : zi_hua_list) {
                fmt::print("{}\n", zi_hua.to_string());
            }
        }
    }
    
    void display_fei_hua_analysis(const ZiWeiResult& result, int from_gong, SiHua si_hua_type) {
        fmt::print("\n\n");
        fmt::print("       第{}宫 {} 飞化链分析\n", from_gong, string(to_zh(si_hua_type)));
        fmt::print("\n\n");
        
        auto gong_gan_zhi = prepare_gong_gan_zhi(result);
        auto stars_in_gong = prepare_stars_in_gong(result);
        
        SiHuaSystem si_hua_system(gong_gan_zhi, stars_in_gong);
        auto chains = si_hua_system.get_fei_hua_chains(from_gong, si_hua_type, 4);
        
        if (chains.empty()) {
            fmt::print("无飞化链\n");
        } else {
            for (const auto& chain : chains) {
                fmt::print("{}\n", chain.to_string());
            }
        }
    }

    // ============= 格局分析功能实现 =============
    
    void display_ge_ju_analysis(const ZiWeiResult& result) {
        fmt::print("\n\n");
        fmt::print("       格局分析\n");
        fmt::print("\n\n");
        
        auto stars_in_gong = prepare_stars_in_gong(result);
        auto gong_di_zhi = prepare_gong_di_zhi(result);
        
        GeJuAnalyzer analyzer(stars_in_gong, gong_di_zhi, result.ming_gong_index);
        
        auto ji_ge = analyzer.analyze_ji_ge();
        auto xiong_ge = analyzer.analyze_xiong_ge();
        int total_score = analyzer.get_total_score();
        
        fmt::print("【命盘总分】：{}\n\n", total_score);
        
        if (!ji_ge.empty()) {
            fmt::print("【吉格】（共{}个）\n", ji_ge.size());
            for (const auto& geju : ji_ge) {
                fmt::print("  {}\n", geju.to_string());
            }
            fmt::print("\n");
        }
        
        if (!xiong_ge.empty()) {
            fmt::print("【凶格】（共{}个）\n", xiong_ge.size());
            for (const auto& geju : xiong_ge) {
                fmt::print("  {}\n", geju.to_string());
            }
        }
    }
    
    void display_ji_ge(const ZiWeiResult& result) {
        auto stars_in_gong = prepare_stars_in_gong(result);
        auto gong_di_zhi = prepare_gong_di_zhi(result);
        
        GeJuAnalyzer analyzer(stars_in_gong, gong_di_zhi, result.ming_gong_index);
        auto ji_ge = analyzer.analyze_ji_ge();
        
        fmt::print("\n【吉格列表】（共{}个）\n", ji_ge.size());
        for (const auto& geju : ji_ge) {
            fmt::print("{}\n", geju.to_string());
        }
    }
    
    void display_xiong_ge(const ZiWeiResult& result) {
        auto stars_in_gong = prepare_stars_in_gong(result);
        auto gong_di_zhi = prepare_gong_di_zhi(result);
        
        GeJuAnalyzer analyzer(stars_in_gong, gong_di_zhi, result.ming_gong_index);
        auto xiong_ge = analyzer.analyze_xiong_ge();
        
        fmt::print("\n【凶格列表】（共{}个）\n", xiong_ge.size());
        for (const auto& geju : xiong_ge) {
            fmt::print("{}\n", geju.to_string());
        }
    }
    
    void display_shuang_xing_zu_he(const ZiWeiResult& result) {
        auto stars_in_gong = prepare_stars_in_gong(result);
        auto gong_di_zhi = prepare_gong_di_zhi(result);
        
        GeJuAnalyzer analyzer(stars_in_gong, gong_di_zhi, result.ming_gong_index);
        auto shuang_xing = analyzer.analyze_shuang_xing();
        
        fmt::print("\n【双星组合】（共{}组）\n", shuang_xing.size());
        for (const auto& zu_he : shuang_xing) {
            fmt::print("{}\n", zu_he.to_string());
        }
    }

    // ============= 三方四正分析功能实现 =============
    
    void display_san_fang_si_zheng(const ZiWeiResult& result, GongWei gong_wei) {
        int gong_index = result.get_palace(gong_wei).gong_data.index;
        auto san_fang = get_san_fang_si_zheng(gong_index);
        
        fmt::print("\n\n");
        fmt::print("       {} 三方四正\n", string(to_zh(gong_wei)));
        fmt::print("\n\n");
        
        fmt::print("{}\n\n", san_fang.to_string());
        
        for (int idx : san_fang.get_all_indices()) {
            const auto& palace = result.palaces[idx];
            fmt::print("{}\n\n", palace.to_string());
        }
    }
    
    void display_kong_gong_jie_xing(const ZiWeiResult& result) {
        auto stars_in_gong = prepare_stars_in_gong(result);
        
        SanFangAnalyzer analyzer(stars_in_gong);
        auto kong_gong_list = analyzer.get_all_kong_gong();
        
        fmt::print("\n【空宫借星】（共{}个）\n", kong_gong_list.size());
        if (kong_gong_list.empty()) {
            fmt::print("无空宫\n");
        } else {
            for (const auto& kong_gong : kong_gong_list) {
                fmt::print("{}\n", kong_gong.to_string());
            }
        }
    }

    // ============= 星耀特性查询功能实现 =============
    
    void display_star_info(const string& star_name) {
        auto doc = get_star_document(star_name);
        if (doc.has_value()) {
            fmt::print("\n{}\n", doc->to_string());
        } else {
            fmt::print("\n未找到星曜「{}」的详细信息\n", star_name);
        }
    }
    
    void display_tao_hua_xing() {
        // 交际类杂耀包含桃花星
        auto tao_hua_list = StarDoc::get_za_yao_by_category(ZaYaoCategory::JiaoJi);
        fmt::print("\n【桃花星列表】：{}\n", fmt::join(tao_hua_list, "、"));
    }
    
    void display_cai_xing() {
        // 财星主要是禄存、天马（二助星）
        auto cai_xing_list = StarDoc::get_fu_xing_by_category(FuXingCategory::ErZhu);
        fmt::print("\n【财星列表】：{}\n", fmt::join(cai_xing_list, "、"));
    }

    // ============= 运限分析功能实现 =============
    
    void display_da_xian_analysis(const ZiWeiResult& result) {
        fmt::print("\n\n");
        fmt::print("       大限分析\n");
        fmt::print("\n\n");
        
        for (int i = 0; i < 12; ++i) {
            const auto& da_xian = result.da_xian_data[i];
            fmt::print("第{}限：{}岁-{}岁 - 大限宫位：第{}宫 {}\n",
                i + 1,
                da_xian.start_age,
                da_xian.end_age,
                da_xian.gong_index,
                string(to_zh(result.palaces[da_xian.gong_index].gong_data.gong_wei)));
        }
    }
    
    void display_xiao_xian_analysis(const ZiWeiResult& result, int current_age) {
        fmt::print("\n\n");
        fmt::print("       小限分析（{}岁）\n", current_age);
        fmt::print("\n\n");
        
        auto xiao_xian_data = get_xiao_xian(current_age, result.is_male, result.year_pillar.zhi);
        
        fmt::print("小限宫位：第{}宫 {}\n",
            xiao_xian_data.gong_index,
            string(to_zh(result.palaces[xiao_xian_data.gong_index].gong_data.gong_wei)));
        
        fmt::print("\n{}\n", result.palaces[xiao_xian_data.gong_index].to_string());
    }
    
    void display_liu_nian_analysis(const ZiWeiResult& result, int target_year, int current_age) {
        fmt::print("\n\n");
        fmt::print("       {}年流年分析（{}岁）\n", target_year, current_age);
        fmt::print("\n\n");
        
        // 使用tyme库获取流年天干地支
        auto solar_day = tyme::SolarDay::from_ymd(target_year, 1, 1);
        auto sixty_cycle_day = solar_day.get_sixty_cycle_day();
        auto year_cycle = sixty_cycle_day.get_year();
        
        auto year_gan = year_cycle.get_heaven_stem();
        auto year_zhi = year_cycle.get_earth_branch();
        
        // 转换为我们的TianGan和DiZhi类型
        TianGan tian_gan = static_cast<TianGan>(year_gan.get_index());
        DiZhi di_zhi = static_cast<DiZhi>(year_zhi.get_index());
        
        // 调用horoscope模块获取流年数据
        auto liu_nian_data = get_liu_nian(target_year, tian_gan, di_zhi, result.ming_gong_index);
        
        fmt::print("流年干支：{}{} ({}年)\n", 
            string(GanZhi::Mapper::to_zh(liu_nian_data.tian_gan)),
            string(GanZhi::Mapper::to_zh(liu_nian_data.di_zhi)),
            target_year);
        fmt::print("流年宫位：第{}宫 {}\n",
            liu_nian_data.gong_index,
            string(to_zh(result.palaces[liu_nian_data.gong_index].gong_data.gong_wei)));
        
        // 显示流年四化
        fmt::print("\n流年四化：\n");
        for (int i = 0; i < 4; ++i) {
            if (!liu_nian_data.si_hua[i].empty()) {
                fmt::print("  {} - {}\n", 
                    string(to_zh(static_cast<SiHua>(i))),
                    liu_nian_data.si_hua[i]);
            }
        }
        
        fmt::print("\n流年宫位详情：\n");
        fmt::print("{}\n", result.palaces[liu_nian_data.gong_index].to_string());
    }
    
    void display_liu_yue_analysis(const ZiWeiResult& result, int target_year, int target_month, int current_age) {
        fmt::print("\n\n");
        fmt::print("       {}年{}月流月分析（{}岁）\n", target_year, target_month, current_age);
        fmt::print("\n\n");
        
        // 使用tyme库获取流月天干地支
        auto solar_day = tyme::SolarDay::from_ymd(target_year, target_month, 15); // 使用月中作为参考日
        auto lunar_day = solar_day.get_lunar_day();
        int lunar_month = lunar_day.get_lunar_month().get_month();
        int birth_month = result.month_pillar.zhi == DiZhi::Zi ? 11 : static_cast<int>(result.month_pillar.zhi) - 1;
        
        auto sixty_cycle_day = solar_day.get_sixty_cycle_day();
        auto month_cycle = sixty_cycle_day.get_month();
        auto year_cycle = sixty_cycle_day.get_year();
        
        TianGan month_gan = static_cast<TianGan>(month_cycle.get_heaven_stem().get_index());
        DiZhi month_zhi = static_cast<DiZhi>(month_cycle.get_earth_branch().get_index());
        DiZhi year_zhi = static_cast<DiZhi>(year_cycle.get_earth_branch().get_index());
        
        // 调用horoscope模块获取流月数据
        auto liu_yue_data = get_liu_yue(lunar_month, birth_month, month_gan, month_zhi, year_zhi, result.ming_gong_index);
        
        fmt::print("流月干支：{}{} (农历{}月)\n", 
            string(GanZhi::Mapper::to_zh(liu_yue_data.tian_gan)),
            string(GanZhi::Mapper::to_zh(liu_yue_data.di_zhi)),
            liu_yue_data.month);
        fmt::print("流月宫位：第{}宫 {}\n",
            liu_yue_data.gong_index,
            string(to_zh(result.palaces[liu_yue_data.gong_index].gong_data.gong_wei)));
        
        // 显示流月四化
        fmt::print("\n流月四化：\n");
        for (int i = 0; i < 4; ++i) {
            if (!liu_yue_data.si_hua[i].empty()) {
                fmt::print("  {} - {}\n", 
                    string(to_zh(static_cast<SiHua>(i))),
                    liu_yue_data.si_hua[i]);
            }
        }
        
        fmt::print("\n流月宫位详情：\n");
        fmt::print("{}\n", result.palaces[liu_yue_data.gong_index].to_string());
    }
    
    void display_liu_ri_analysis(const ZiWeiResult& result, int target_year, int target_month, int target_day, int current_age) {
        fmt::print("\n\n");
        fmt::print("       {}年{}月{}日流日分析（{}岁）\n", target_year, target_month, target_day, current_age);
        fmt::print("\n\n");
        
        // 使用tyme库获取流日天干地支
        auto solar_day = tyme::SolarDay::from_ymd(target_year, target_month, target_day);
        auto lunar_day = solar_day.get_lunar_day();
        int lunar_day_num = lunar_day.get_day();
        
        auto sixty_cycle_day = solar_day.get_sixty_cycle_day();
        auto day_cycle = sixty_cycle_day.get_sixty_cycle();
        
        TianGan day_gan = static_cast<TianGan>(day_cycle.get_heaven_stem().get_index());
        DiZhi day_zhi = static_cast<DiZhi>(day_cycle.get_earth_branch().get_index());
        
        // 先获取流月宫位索引（简化实现，假设从结果中获取）
        auto solar_day_month = tyme::SolarDay::from_ymd(target_year, target_month, 15);
        auto lunar_day_month = solar_day_month.get_lunar_day();
        int lunar_month = lunar_day_month.get_lunar_month().get_month();
        int birth_month = result.month_pillar.zhi == DiZhi::Zi ? 11 : static_cast<int>(result.month_pillar.zhi) - 1;
        
        auto sixty_cycle_day_month = solar_day_month.get_sixty_cycle_day();
        auto month_cycle = sixty_cycle_day_month.get_month();
        auto year_cycle = sixty_cycle_day_month.get_year();
        
        TianGan month_gan = static_cast<TianGan>(month_cycle.get_heaven_stem().get_index());
        DiZhi month_zhi = static_cast<DiZhi>(month_cycle.get_earth_branch().get_index());
        DiZhi year_zhi = static_cast<DiZhi>(year_cycle.get_earth_branch().get_index());
        
        auto liu_yue_data = get_liu_yue(lunar_month, birth_month, month_gan, month_zhi, year_zhi, result.ming_gong_index);
        
        // 调用horoscope模块获取流日数据
        auto liu_ri_data = get_liu_ri(lunar_day_num, day_gan, day_zhi, liu_yue_data.gong_index);
        
        fmt::print("流日干支：{}{} (农历{}日)\n", 
            string(GanZhi::Mapper::to_zh(liu_ri_data.tian_gan)),
            string(GanZhi::Mapper::to_zh(liu_ri_data.di_zhi)),
            liu_ri_data.day);
        fmt::print("流日宫位：第{}宫 {}\n",
            liu_ri_data.gong_index,
            string(to_zh(result.palaces[liu_ri_data.gong_index].gong_data.gong_wei)));
        
        // 显示流日四化
        fmt::print("\n流日四化：\n");
        for (int i = 0; i < 4; ++i) {
            if (!liu_ri_data.si_hua[i].empty()) {
                fmt::print("  {} - {}\n", 
                    string(to_zh(static_cast<SiHua>(i))),
                    liu_ri_data.si_hua[i]);
            }
        }
        
        fmt::print("\n流日宫位详情：\n");
        fmt::print("{}\n", result.palaces[liu_ri_data.gong_index].to_string());
    }
    
    void display_liu_shi_analysis(const ZiWeiResult& result, int target_year, int target_month, int target_day, DiZhi target_hour, int current_age) {
        fmt::print("\n\n");
        fmt::print("       {}年{}月{}日 {} 流时分析（{}岁）\n", 
            target_year, target_month, target_day, 
            string(to_zh(target_hour)), 
            current_age);
        fmt::print("\n\n");
        
        // 使用tyme库获取流时天干
        auto solar_day = tyme::SolarDay::from_ymd(target_year, target_month, target_day);
        auto sixty_cycle_day = solar_day.get_sixty_cycle_day();
        auto day_cycle = sixty_cycle_day.get_sixty_cycle();
        
        // 根据日干和时辰地支计算时干（五鼠遁日起时法）
        int day_gan_index = day_cycle.get_heaven_stem().get_index();
        int hour_zhi_index = static_cast<int>(target_hour);
        int hour_gan_index = (day_gan_index % 5 * 2 + hour_zhi_index) % 10;
        
        TianGan hour_gan = static_cast<TianGan>(hour_gan_index);
        
        // 获取流日宫位索引（需要先计算流日）
        auto lunar_day = solar_day.get_lunar_day();
        int lunar_day_num = lunar_day.get_day();
        TianGan day_gan = static_cast<TianGan>(day_cycle.get_heaven_stem().get_index());
        DiZhi day_zhi = static_cast<DiZhi>(day_cycle.get_earth_branch().get_index());
        
        // 获取流月数据
        auto solar_day_month = tyme::SolarDay::from_ymd(target_year, target_month, 15);
        auto lunar_day_month = solar_day_month.get_lunar_day();
        int lunar_month = lunar_day_month.get_lunar_month().get_month();
        int birth_month = result.month_pillar.zhi == DiZhi::Zi ? 11 : static_cast<int>(result.month_pillar.zhi) - 1;
        
        auto sixty_cycle_day_month = solar_day_month.get_sixty_cycle_day();
        auto month_cycle = sixty_cycle_day_month.get_month();
        auto year_cycle = sixty_cycle_day_month.get_year();
        
        TianGan month_gan = static_cast<TianGan>(month_cycle.get_heaven_stem().get_index());
        DiZhi month_zhi = static_cast<DiZhi>(month_cycle.get_earth_branch().get_index());
        DiZhi year_zhi = static_cast<DiZhi>(year_cycle.get_earth_branch().get_index());
        
        auto liu_yue_data = get_liu_yue(lunar_month, birth_month, month_gan, month_zhi, year_zhi, result.ming_gong_index);
        auto liu_ri_data = get_liu_ri(lunar_day_num, day_gan, day_zhi, liu_yue_data.gong_index);
        
        // 调用horoscope模块获取流时数据
        auto liu_shi_data = get_liu_shi(target_hour, hour_gan, liu_ri_data.gong_index);
        
        fmt::print("流时干支：{}{}\n", 
            string(GanZhi::Mapper::to_zh(liu_shi_data.tian_gan)),
            string(GanZhi::Mapper::to_zh(liu_shi_data.di_zhi)));
        fmt::print("流时宫位：第{}宫 {}\n",
            liu_shi_data.gong_index,
            string(to_zh(result.palaces[liu_shi_data.gong_index].gong_data.gong_wei)));
        
        // 显示流时四化
        fmt::print("\n流时四化：\n");
        for (int i = 0; i < 4; ++i) {
            if (!liu_shi_data.si_hua[i].empty()) {
                fmt::print("  {} - {}\n", 
                    string(to_zh(static_cast<SiHua>(i))),
                    liu_shi_data.si_hua[i]);
            }
        }
        
        fmt::print("\n流时宫位详情：\n");
        fmt::print("{}\n", result.palaces[liu_shi_data.gong_index].to_string());
    }
    
    void display_yun_xian_full_analysis(const ZiWeiResult& result, int target_year, int target_month, int target_day, DiZhi target_hour, int current_age) {
        fmt::print("\n");
        fmt::print("\n");
        fmt::print("              完整运限分析报告                              \n");
        fmt::print("       {}年{}月{}日 {} （{}岁）            \n",
            target_year, target_month, target_day,
            string(GanZhi::Mapper::to_zh(target_hour)),
            current_age);
        fmt::print("\n");
        
        // 大限
        display_da_xian_analysis(result);
        
        // 小限
        display_xiao_xian_analysis(result, current_age);
        
        // 流年
        display_liu_nian_analysis(result, target_year, current_age);
        
        // 流月
        display_liu_yue_analysis(result, target_year, target_month, current_age);
        
        // 流日
        display_liu_ri_analysis(result, target_year, target_month, target_day, current_age);
        
        // 流时
        display_liu_shi_analysis(result, target_year, target_month, target_day, target_hour, current_age);
        
        fmt::print("\n");
        fmt::print("\n");
        fmt::print("       运限分析完成\n");
        fmt::print("\n");
    }

    // ============= 综合分析功能实现 =============
    
    void display_full_analysis(const ZiWeiResult& result) {
        fmt::print("\n");
        fmt::print("\n");
        fmt::print("              紫微斗数完整命盘分析报告                      \n");
        fmt::print("\n");
        
        // 基本信息
        fmt::print("\n【基本信息】\n");
        fmt::print("{}\n", result.to_string());
        
        // 格局分析
        display_ge_ju_analysis(result);
        
        // 四化分析
        display_gong_gan_si_hua(result);
        
        // 自化分析
        display_zi_hua_analysis(result);
        
        // 空宫分析
        display_kong_gong_jie_xing(result);
        
        // 大限分析
        display_da_xian_analysis(result);
    }
    
    string export_to_json_full(const ZiWeiResult& result) {
        json j = json::parse(export_to_json(result));
        
        auto stars_in_gong = prepare_stars_in_gong(result);
        auto gong_di_zhi = prepare_gong_di_zhi(result);
        auto gong_gan_zhi = prepare_gong_gan_zhi(result);
        
        // 添加格局信息
        GeJuAnalyzer ge_ju_analyzer(stars_in_gong, gong_di_zhi, result.ming_gong_index);
        auto ji_ge = ge_ju_analyzer.analyze_ji_ge();
        auto xiong_ge = ge_ju_analyzer.analyze_xiong_ge();
        
        j["ge_ju"]["ji_ge"] = json::array();
        for (const auto& geju : ji_ge) {
            json g;
            g["name"] = geju.name;
            g["description"] = geju.description;
            g["score"] = geju.score;
            j["ge_ju"]["ji_ge"].push_back(g);
        }
        
        j["ge_ju"]["xiong_ge"] = json::array();
        for (const auto& geju : xiong_ge) {
            json g;
            g["name"] = geju.name;
            g["description"] = geju.description;
            g["score"] = geju.score;
            j["ge_ju"]["xiong_ge"].push_back(g);
        }
        
        j["ge_ju"]["total_score"] = ge_ju_analyzer.get_total_score();
        
        // 添加四化信息
        SiHuaSystem si_hua_system(gong_gan_zhi, stars_in_gong);
        j["si_hua"]["gong_gan_si_hua"] = json::array();
        for (const auto& gong_si_hua : si_hua_system.get_all_gong_gan_si_hua()) {
            json sh;
            sh["gong_index"] = gong_si_hua.gong_index;
            sh["gong_gan"] = string(to_zh(gong_si_hua.gong_gan));
            sh["si_hua_list"] = json::array();
            for (const auto& si_hua_info : gong_si_hua.si_hua_list) {
                if (!si_hua_info.star_name.empty()) {
                    json info;
                    info["star"] = si_hua_info.star_name;
                    info["type"] = string(to_zh(si_hua_info.type));
                    info["to_gong"] = si_hua_info.gong_index;
                    sh["si_hua_list"].push_back(info);
                }
            }
            j["si_hua"]["gong_gan_si_hua"].push_back(sh);
        }
        
        auto zi_hua_list = si_hua_system.get_all_zi_hua();
        j["si_hua"]["zi_hua"] = json::array();
        for (const auto& zi_hua : zi_hua_list) {
            json zh;
            zh["gong_index"] = zi_hua.gong_index;
            zh["types"] = json::array();
            for (const auto& type : zi_hua.zi_hua_types) {
                zh["types"].push_back(string(to_zh(type)));
            }
            j["si_hua"]["zi_hua"].push_back(zh);
        }
        
        // 添加大限信息
        j["da_xian"] = json::array();
        for (const auto& dx : result.da_xian_data) {
            json dxj;
            dxj["start_age"] = dx.start_age;
            dxj["end_age"] = dx.end_age;
            dxj["gong_index"] = dx.gong_index;
            j["da_xian"].push_back(dxj);
        }
        
        return j.dump(2);
    }

} // namespace ZhouYi::ZiWei

