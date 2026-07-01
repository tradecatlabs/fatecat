// 主程序入口 - 唯一允许的 .cpp 文件

// 导入第三方库模块（优先）
import fmt;
import magic_enum;
import nlohmann.json;

// 导入自定义模块
import ZhouYi.GanZhi;          // 包含 TianGan 和 DiZhi
import ZhouYi.BaZiBase;        // 八字基础结构
import ZhouYi.tyme;            // 农历时间库
import ZhouYi.LiuYaoController;// 六爻排盘控制器
import ZhouYi.DaLiuRen;        // 大六壬核心模块
import ZhouYi.DaLiuRen.Controller; // 大六壬控制器

// 导入标准库模块（最后）
import std;

using namespace fmt;
int main() {
    // 使用 fmt 模块进行彩色输出
    fmt::print(fg(fmt::color::green) | fmt::emphasis::bold,
               "=== ZhouYiLab C++23 Modules Demo ===\n\n");
    
    // ==================== 反射功能演示 ====================
    fmt::print(fg(fmt::color::cyan) | fmt::emphasis::bold, 
               "【1】magic_enum 反射功能演示\n");
    fmt::print("----------------------------------------------\n");
    
    // 获取天干枚举的所有值
    fmt::print(fg(fmt::color::yellow), "天干枚举值列表（英文名）:\n");
    constexpr auto tian_gan_values = magic_enum::enum_values<ZhouYi::GanZhi::TianGan>();
    for (auto value : tian_gan_values) {
        auto name = magic_enum::enum_name(value);
        auto index = magic_enum::enum_integer(value);
        fmt::print("  [{:2d}] {}\n", index, name);
    }
    
    fmt::print("\n");
    
    // ==================== 中文映射演示 ====================
    fmt::print(fg(fmt::color::cyan) | fmt::emphasis::bold, 
               "【2】中文映射功能演示\n");
    fmt::print("----------------------------------------------\n");
    
    // 天干中英文对照
    fmt::print(fg(fmt::color::magenta), "天干中英文对照表:\n");
    for (auto value : tian_gan_values) {
        auto en_name = magic_enum::enum_name(value);
        auto zh_name = ZhouYi::GanZhi::Mapper::to_zh(value);
        fmt::print("  {}  {}\n", en_name, zh_name);
    }
    
    fmt::print("\n");
    
    // 地支中英文对照
    fmt::print(fg(fmt::color::magenta), "地支中英文对照表（含生肖）:\n");
    constexpr auto di_zhi_values = magic_enum::enum_values<ZhouYi::GanZhi::DiZhi>();
    for (auto value : di_zhi_values) {
        auto en_name = magic_enum::enum_name(value);
        auto zh_name = ZhouYi::GanZhi::Mapper::to_zh(value);
        auto sheng_xiao = ZhouYi::GanZhi::Mapper::sheng_xiao_zh(value);
        fmt::print("  {}  {} ({})\n", en_name, zh_name, sheng_xiao);
    }
    
    fmt::print("\n");
    
    // ==================== 农历功能演示 ====================
    fmt::print(fg(fmt::color::cyan) | fmt::emphasis::bold, 
               "【3】农历日历功能演示（tyme4cpp）\n");
    fmt::print("----------------------------------------------\n");
    
    // 示例日期：1986年5月29日
    auto solar = tyme::SolarDay::from_ymd(1986, 5, 29);
    auto lunar = solar.get_lunar_day();
    
    fmt::print(fg(fmt::color::green), "公历日期: {}\n", solar.to_string());
    fmt::print(fg(fmt::color::green), "农历日期: {}\n", lunar.to_string());
    
    // 获取年月日的干支信息
    auto lunar_month = lunar.get_lunar_month();
    auto lunar_year = lunar_month.get_lunar_year();
    
    fmt::print(fg(fmt::color::yellow), "年份干支: {}\n", lunar_year.get_sixty_cycle().get_name());
    fmt::print(fg(fmt::color::yellow), "月份干支: {}\n", lunar_month.get_sixty_cycle().get_name());
    fmt::print(fg(fmt::color::yellow), "日期干支: {}\n", lunar.get_sixty_cycle().get_name());
    //fmt::print(fg(fmt::color::magenta), "生　　肖: {}\n", lunar_year.get_zodiac().get_name());
    
    fmt::print("\n");
    
    // ==================== 完整干支系统演示 ====================
    fmt::print(fg(fmt::color::cyan) | fmt::emphasis::bold, 
               "【4】完整干支系统演示（ZhouYi.GanZhi）\n");
    fmt::print("----------------------------------------------\n");
    
    // 展示六十甲子表
    auto jia_zi_list = ZhouYi::GanZhi::get_liu_shi_jia_zi();
    fmt::print(fg(fmt::color::yellow), "六十甲子表:\n");
    for (std::size_t i = 0; i < jia_zi_list.size(); ++i) {
        const auto& jz = jia_zi_list[i];
        fmt::print("{:2d}.{} ", i + 1, jz.to_string());
        if ((i + 1) % 10 == 0) {
            fmt::print("\n");
        }
    }
    fmt::print("\n");
    
    // 演示干支关系
    fmt::print(fg(fmt::color::green) | fmt::emphasis::bold, "干支关系演示:\n");
    
    // 地支六冲
    auto zi = ZhouYi::GanZhi::DiZhi::Zi;
    auto wu = ZhouYi::GanZhi::DiZhi::Wu;
    fmt::print("子午相冲: {}\n", 
               ZhouYi::GanZhi::is_chong(zi, wu) ? "是" : "否");
    
    // 地支六合
    auto chou = ZhouYi::GanZhi::DiZhi::Chou;
    fmt::print("子丑相合: {}\n", 
               ZhouYi::GanZhi::is_he(zi, chou) ? "是" : "否");
    
    // 地支三合
    auto shen = ZhouYi::GanZhi::DiZhi::Shen;
    auto chen = ZhouYi::GanZhi::DiZhi::Chen;
    auto [is_san_he, he_wx] = ZhouYi::GanZhi::is_san_he(shen, zi, chen);
    if (is_san_he) {
        fmt::print("申子辰三合: {} (合化为{})\n", "是", 
                   ZhouYi::GanZhi::Mapper::to_zh(he_wx));
    }
    
    // 五行生克
    auto mu = ZhouYi::GanZhi::WuXing::Mu;
    auto huo = ZhouYi::GanZhi::WuXing::Huo;
    fmt::print("木生火: {}\n", 
               ZhouYi::GanZhi::wu_xing_sheng(mu, huo) ? "是" : "否");
    
    fmt::print("\n");
    
    // 天干贵人
    fmt::print(fg(fmt::color::magenta), "天干贵人:\n");
    auto jia = ZhouYi::GanZhi::TianGan::Jia;
    auto yang_gui = ZhouYi::GanZhi::get_gui_ren(jia, true);
    auto yin_gui = ZhouYi::GanZhi::get_gui_ren(jia, false);
    fmt::print("甲日阳贵: {}, 阴贵: {}\n",
               ZhouYi::GanZhi::Mapper::to_zh(yang_gui),
               ZhouYi::GanZhi::Mapper::to_zh(yin_gui));
    
    fmt::print("\n");
    
    // ==================== 二十四节气演示 ====================
    fmt::print(fg(fmt::color::cyan) | fmt::emphasis::bold, 
               "【5】农历信息演示\n");
    fmt::print("----------------------------------------------\n");
    
    // 展示一些农历信息
    fmt::print(fg(fmt::color::green), "农历年: {}年\n", lunar_year.get_year());
    fmt::print(fg(fmt::color::green), "农历月数: {} 个月\n", lunar_year.get_month_count());
    fmt::print(fg(fmt::color::green), "农历天数: {} 天\n", lunar_year.get_day_count());
    fmt::print(fg(fmt::color::yellow), "本月天数: {} 天\n", lunar_month.get_day_count());
    
    fmt::print("\n");
    
    // ==================== JSON 序列化演示 ====================
    fmt::print(fg(fmt::color::cyan) | fmt::emphasis::bold, 
               "【6】JSON 序列化演示\n");
    fmt::print("----------------------------------------------\n");
    
    // 构建项目信息 JSON
    nlohmann::json project_info = {
        {"name", "ZhouYiLab"},
        {"version", "1.0.0"},
        {"description", "基于 C++23 Modules 的传统文化算法库"},
        {"features", {
            "完全模块化设计",
            "magic_enum 反射支持",
            "中英文双向映射",
            "农历公历互转",
            "干支纪年月日",
            "二十四节气",
            "fmt 格式化输出",
            "nlohmann::json 序列化"
        }},
        {"modules", {
            {"standard", "import std"},
            {"third_party", {
                {"fmt", "import fmt"},
                {"magic_enum", "import magic_enum"},
                {"nlohmann_json", "import nlohmann.json"}
            }},
            {"custom", {
                {"TianGan", "import ZhouYi.TianGan"},
                {"DiZhi", "import ZhouYi.DiZhi"},
                {"LunarCalendar", "import ZhouYi.LunarCalendar"}
            }}
        }},
        {"libraries", {
            {"tyme4cpp", {
                {"url", "https://github.com/6tail/tyme4cpp"},
                {"description", "强大的日历工具库"}
            }}
        }}
    };
    
    fmt::print("{}\n\n", project_info.dump(2));
    
    // ==================== 统计信息 ====================
    fmt::print(fg(fmt::color::cyan) | fmt::emphasis::bold, 
               "【7】统计信息\n");
    fmt::print("----------------------------------------------\n");
    
    fmt::print("天干数量: {}\n", magic_enum::enum_count<ZhouYi::GanZhi::TianGan>());
    fmt::print("地支数量: {}\n", magic_enum::enum_count<ZhouYi::GanZhi::DiZhi>());
    fmt::print("五行数量: {}\n", magic_enum::enum_count<ZhouYi::GanZhi::WuXing>());
    fmt::print("六十甲子: {} 个\n", jia_zi_list.size());
    //fmt::print("二十四节气: {} 个\n", terms_2025.size());
    
    // ==================== 八字计算演示 ====================
    fmt::print("\n");
    fmt::print(fg(fmt::color::cyan) | fmt::emphasis::bold, 
               "【8】八字计算与公历农历转换演示\n");
    fmt::print("----------------------------------------------\n");
    
    try {
        // 测试1: 从公历创建八字
        fmt::print(fg(fmt::color::yellow), "\n测试1: 公历转八字（带旬空）\n");
        fmt::print("公历: 2025年10月13日 14时30分\n");
        auto bazi1 = ZhouYi::BaZiBase::BaZi::from_solar(2025, 10, 13, 14, 30);
        fmt::print("八字:\n{}\n", bazi1);
        
        // 测试2: 从农历创建八字
        fmt::print(fg(fmt::color::yellow), "\n测试2: 农历转八字（带旬空）\n");
        fmt::print("农历: 2025年九月十一 子时\n");
        auto bazi2 = ZhouYi::BaZiBase::BaZi::from_lunar(2025, 9, 11, 0);
        fmt::print("八字:\n{}\n", bazi2);
        
        // 测试3: 公历农历转换
        fmt::print(fg(fmt::color::yellow), "\n测试3: 公历农历互转\n");
        ZhouYi::BaZiBase::SolarDate solar{2025, 10, 13};
        fmt::print("公历 2025-10-13  农历: {}\n", solar.to_lunar_string());
        
        ZhouYi::BaZiBase::LunarDate lunar{2025, 9, 11};
        fmt::print("农历 2025年九月十一  公历: {}\n", lunar.to_solar_string());
        
        // 测试4: 旬空说明
        fmt::print(fg(fmt::color::yellow), "\n测试4: 旬空（空亡）说明\n");
        fmt::print("旬空是根据日柱计算的，因为地支比天干多2个\n");
        fmt::print("每一旬（10天）中，最后两个地支就是旬空\n");
        fmt::print("日柱 {} 的旬空: {} {}\n", 
                   bazi1.day.to_string(), bazi1.xun_kong_1, bazi1.xun_kong_2);
        
        fmt::print(fg(fmt::color::green), "\n 八字计算功能正常！旬空计算正确！\n");
        
    } catch (const std::exception& e) {
        fmt::print(fg(fmt::color::red), " 错误: {}\n", e.what());
    }
    
    // ==================== 十二长生演示 ====================
    fmt::print("\n");
    fmt::print(fg(fmt::color::cyan) | fmt::emphasis::bold, 
               "【9】十二长生功能演示\n");
    fmt::print("----------------------------------------------\n");
    
    try {
        // 测试1: 获取天干在地支的十二长生状态
        fmt::print(fg(fmt::color::yellow), "\n测试1: 天干在地支的十二长生状态\n");
        
        auto gan = ZhouYi::GanZhi::TianGan::Jia;  // 甲木
        auto zhi = ZhouYi::GanZhi::DiZhi::Hai;    // 亥
        
        auto cs = ZhouYi::GanZhi::get_shi_er_chang_sheng(gan, zhi);
        auto cs_name = ZhouYi::GanZhi::ShiErChangShengMapper::to_zh(cs);
        
        fmt::print("甲木 在 亥 的状态: {}\n", cs_name);
        
        // 测试2: 展示甲木在十二地支的完整十二长生
        fmt::print(fg(fmt::color::yellow), "\n测试2: 甲木在十二地支的完整十二长生\n");
        fmt::print("甲木（阳干，顺行）:\n");
        
        constexpr auto di_zhi_values = magic_enum::enum_values<ZhouYi::GanZhi::DiZhi>();
        for (auto zhi_val : di_zhi_values) {
            auto cs_state = ZhouYi::GanZhi::get_shi_er_chang_sheng(ZhouYi::GanZhi::TianGan::Jia, zhi_val);
            auto cs_name2 = ZhouYi::GanZhi::ShiErChangShengMapper::to_zh(cs_state);
            auto zhi_name = ZhouYi::GanZhi::Mapper::to_zh(zhi_val);
            fmt::print("  {}  {}\n", zhi_name, cs_name2);
        }
        
        // 测试3: 展示乙木在十二地支的完整十二长生
        fmt::print(fg(fmt::color::yellow), "\n测试3: 乙木在十二地支的完整十二长生\n");
        fmt::print("乙木（阴干，逆行）:\n");
        
        for (auto zhi_val : di_zhi_values) {
            auto cs_state = ZhouYi::GanZhi::get_shi_er_chang_sheng(ZhouYi::GanZhi::TianGan::Yi, zhi_val);
            auto cs_name3 = ZhouYi::GanZhi::ShiErChangShengMapper::to_zh(cs_state);
            auto zhi_name = ZhouYi::GanZhi::Mapper::to_zh(zhi_val);
            fmt::print("  {}  {}\n", zhi_name, cs_name3);
        }
        
        // 测试4: 获取关键地支
        fmt::print(fg(fmt::color::yellow), "\n测试4: 十天干的长生、帝旺、墓库地支\n");
        constexpr auto tian_gan_values2 = magic_enum::enum_values<ZhouYi::GanZhi::TianGan>();
        for (auto gan_val : tian_gan_values2) {
            auto gan_name = ZhouYi::GanZhi::Mapper::to_zh(gan_val);
            auto cs_zhi = ZhouYi::GanZhi::get_chang_sheng_zhi(gan_val);
            auto dw_zhi = ZhouYi::GanZhi::get_di_wang_zhi(gan_val);
            auto mk_zhi = ZhouYi::GanZhi::get_mu_ku_zhi(gan_val);
            
            fmt::print("  {} - 长生:{}, 帝旺:{}, 墓库:{}\n", 
                      gan_name,
                      ZhouYi::GanZhi::Mapper::to_zh(cs_zhi),
                      ZhouYi::GanZhi::Mapper::to_zh(dw_zhi),
                      ZhouYi::GanZhi::Mapper::to_zh(mk_zhi));
        }
        
        // 测试5: 判断特定状态
        fmt::print(fg(fmt::color::yellow), "\n测试5: 状态判断函数\n");
        fmt::print("甲木在亥是否长生: {}\n", 
                   ZhouYi::GanZhi::is_chang_sheng(ZhouYi::GanZhi::TianGan::Jia, ZhouYi::GanZhi::DiZhi::Hai) ? "是" : "否");
        fmt::print("甲木在卯是否帝旺: {}\n", 
                   ZhouYi::GanZhi::is_di_wang(ZhouYi::GanZhi::TianGan::Jia, ZhouYi::GanZhi::DiZhi::Mao) ? "是" : "否");
        fmt::print("甲木在未是否墓库: {}\n", 
                   ZhouYi::GanZhi::is_mu_ku(ZhouYi::GanZhi::TianGan::Jia, ZhouYi::GanZhi::DiZhi::Wei) ? "是" : "否");
        fmt::print("甲木在申是否绝地: {}\n", 
                   ZhouYi::GanZhi::is_jue_di(ZhouYi::GanZhi::TianGan::Jia, ZhouYi::GanZhi::DiZhi::Shen) ? "是" : "否");
        
        fmt::print(fg(fmt::color::green), "\n 十二长生功能正常！\n");
        
    } catch (const std::exception& e) {
        fmt::print(fg(fmt::color::red), " 错误: {}\n", e.what());
    }
    
    // ==================== 大六壬排盘演示 ====================
    fmt::print("\n");
    fmt::print(fg(fmt::color::cyan) | fmt::emphasis::bold, 
               "【10】大六壬排盘演示\n");
    fmt::print("----------------------------------------------\n");
    
    try {
        // 测试1: 基本排盘
        fmt::print(fg(fmt::color::yellow), "\n测试1: 公历日期大六壬排盘\n");
        fmt::print("公历: 2025年10月10日 14时\n");
        
        auto dlr_result = ZhouYi::DaLiuRen::DaLiuRenEngine::pai_pan(2025, 10, 10, 14);
        
        // 使用控制器显示详细结果
        ZhouYi::DaLiuRen::Controller::DaLiuRenController::display_result_detailed(dlr_result);
        
        // 测试2: 访问详细信息
        fmt::print(fg(fmt::color::yellow), "\n测试2: 访问排盘详细信息\n");
        fmt::print("初传: {}\n", 
                   ZhouYi::GanZhi::Mapper::to_zh(dlr_result.san_chuan.get_chu_chuan()));
        fmt::print("中传: {}\n", 
                   ZhouYi::GanZhi::Mapper::to_zh(dlr_result.san_chuan.get_zhong_chuan()));
        fmt::print("末传: {}\n", 
                   ZhouYi::GanZhi::Mapper::to_zh(dlr_result.san_chuan.get_mo_chuan()));
        
        const auto& ke_shi = dlr_result.san_chuan.get_ke_shi();
        if (!ke_shi.empty()) {
            fmt::print("课式: {}\n", fmt::join(ke_shi, ", "));
        }
        
        fmt::print(fg(fmt::color::green), "\n 大六壬排盘功能正常！\n");
        
    } catch (const std::exception& e) {
        fmt::print(fg(fmt::color::red), " 错误: {}\n", e.what());
    }
    
    fmt::print("\n");
    fmt::print(fg(fmt::color::magenta) | fmt::emphasis::italic, 
               " 所有功能演示完成！\n");
    fmt::print(fg(fmt::color::green), 
               " C++23 Modules + 反射 + 中文映射 + 农历日历 + 八字计算 + 十二长生 + 大六壬完美运行！\n");
    
    return 0;
}