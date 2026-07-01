// 大六壬控制器实现文件
module ZhouYi.DaLiuRen.Controller;

import std;
import fmt;

namespace ZhouYi::DaLiuRen::Controller {

// 交互式排盘
void DaLiuRenController::interactive_pai_pan() {
    int year, month, day, hour;
    bool is_lunar;
    
    fmt::print("\n\n");
    fmt::print("       大六壬自动排盘系统           \n");
    fmt::print("\n\n");
    
    get_date_input(year, month, day, hour, is_lunar);
    
    DaLiuRenResult result = is_lunar ? 
        DaLiuRenEngine::pai_pan_lunar(year, month, day, hour) :
        DaLiuRenEngine::pai_pan(year, month, day, hour);
    
    display_result_detailed(result);
}

// 从公历日期排盘
DaLiuRenResult DaLiuRenController::pai_pan_solar(int year, int month, int day, int hour) {
    return DaLiuRenEngine::pai_pan(year, month, day, hour);
}

// 从农历日期排盘
DaLiuRenResult DaLiuRenController::pai_pan_lunar(int year, int month, int day, int hour) {
    return DaLiuRenEngine::pai_pan_lunar(year, month, day, hour);
}

// 显示排盘结果（简洁版）
void DaLiuRenController::display_result(const DaLiuRenResult& result) {
    fmt::print("\n{}\n", result.to_string());
}

// 显示排盘结果（详细版）
void DaLiuRenController::display_result_detailed(const DaLiuRenResult& result) {
    fmt::print("\n\n");
    fmt::print("         大六壬排盘结果             \n");
    fmt::print("\n\n");
    
    // 显示八字
    fmt::print("【八字信息】\n");
    fmt::print("  年柱: {}\n", result.ba_zi.year.to_string());
    fmt::print("  月柱: {}\n", result.ba_zi.month.to_string());
    fmt::print("  日柱: {}\n", result.ba_zi.day.to_string());
    fmt::print("  时柱: {}\n", result.ba_zi.hour.to_string());
    if (!result.ba_zi.xun_kong_1.empty()) {
        fmt::print("  旬空: {}{}\n", result.ba_zi.xun_kong_1, result.ba_zi.xun_kong_2);
    }
    fmt::print("\n");
    
    // 显示基本信息
    fmt::print("【基本信息】\n");
    fmt::print("  月将: {}\n", Mapper::to_zh(result.yue_jiang));
    fmt::print("  贵人: {}\n", Mapper::to_zh(result.gui_ren));
    fmt::print("  昼夜: {}\n", result.is_day ? "白天（阳贵）" : "夜晚（阴贵）");
    fmt::print("\n");
    
    // 显示天地盘
    display_tian_di_pan(result.tian_di_pan, result.ba_zi.day.gan, result.ba_zi.day.zhi);
    
    // 显示四课
    display_si_ke(result.si_ke);
    
    // 显示三传
    auto day_gan = result.ba_zi.day.gan;
    auto day_zhi = result.ba_zi.day.zhi;
    display_san_chuan(result.san_chuan, day_gan, day_zhi);
    
    // 显示神煞
    fmt::print("\n{}", result.shen_sha.to_string());
    
    // 显示卦体
    if (!result.gua_ti.empty()) {
        fmt::print("\n【卦体格局】\n");
        for (const auto& gt : result.gua_ti) {
            fmt::print("  {}\n", gt);
        }
    }
}


// 显示天地盘
void DaLiuRenController::display_tian_di_pan(const TianDiPan& tian_di_pan, TianGan day_gan, DiZhi day_zhi) {
    fmt::print("【天地盘】\n");
    
    const auto& di_pan = tian_di_pan.get_di_pan();
    const auto& tian_pan = tian_di_pan.get_tian_pan();
    const auto& shen_jiang = tian_di_pan.get_shen_jiang();
    
    // 十二神将名称（按正确顺序）
    static const std::array<std::string, 12> shen_jiang_names = {
        "贵人", "螣蛇", "朱雀", "六合", "勾陈", "青龙",
        "天空", "白虎", "太常", "玄武", "太阴", "天后"
    };
    
    fmt::print("  \n");
    fmt::print("   位置   天盘    遁干    神将  \n");
    fmt::print("          地盘                  \n");
    fmt::print("  \n");
    
    for (int i = 0; i < 12; ++i) {
        DiZhi di = di_pan[i];
        DiZhi tian = tian_pan[i];
        
        // 找到地盘的神将
        std::string di_shen_jiang_name = "";
        for (int j = 0; j < 12; ++j) {
            if (shen_jiang[j] == di) {
                di_shen_jiang_name = shen_jiang_names[j];
                break;
            }
        }
        
        // 找到天盘的神将（天盘地支在地盘上的位置）
        std::string tian_shen_jiang_name = "";
        for (int j = 0; j < 12; ++j) {
            if (shen_jiang[j] == tian) {
                tian_shen_jiang_name = shen_jiang_names[j];
                break;
            }
        }
        
        // 地盘和天盘只显示地支
        std::string di_str = std::string(Mapper::to_zh(di));
        std::string tian_str = std::string(Mapper::to_zh(tian));
        
        // 获取天盘地支的遁干
        auto tian_dun_gan_opt = get_dun_gan(tian, day_gan, day_zhi);
        std::string tian_dun_gan_str = "  ";
        if (tian_dun_gan_opt.has_value()) {
            tian_dun_gan_str = std::string(Mapper::to_zh(tian_dun_gan_opt.value()));
        }
        
        // 获取地盘地支的遁干
        auto di_dun_gan_opt = get_dun_gan(di, day_gan, day_zhi);
        std::string di_dun_gan_str = "  ";
        if (di_dun_gan_opt.has_value()) {
            di_dun_gan_str = std::string(Mapper::to_zh(di_dun_gan_opt.value()));
        }
        
        // 第一行：显示地盘位置、天盘、天盘遁干、天盘神将
        // 中文字符显示宽度为2，需要手动对齐
        fmt::print("    {}     {}      {}     {}  \n",
            di_str, tian_str, tian_dun_gan_str, tian_shen_jiang_name);
        // 第二行：显示地盘、地盘遁干、地盘神将
        fmt::print("           {}      {}     {}  \n", 
            di_str, di_dun_gan_str, di_shen_jiang_name);
        
        // 每个位置结束后加一条分隔线
        if (i < 11) {
            if ((i + 1) % 4 == 0) {
                // 每4个位置加双分隔线（更明显）
                fmt::print("  \n");
                fmt::print("  \n");
            } else {
                // 每个位置加单分隔线
                fmt::print("  \n");
            }
        }
    }
    
    fmt::print("  \n\n");
}

// 显示四课（增强版，包含阴阳属性）
void DaLiuRenController::display_si_ke(const SiKe& si_ke) {
    fmt::print("【四课】\n");
    fmt::print("  第一课（干上神）: {} ({})\n", 
               si_ke.first.to_string(),
               si_ke.first.is_yang() ? "阳" : "阴");
    fmt::print("  第二课（神上神）: {} ({})\n", 
               si_ke.second.to_string(),
               si_ke.second.is_yang() ? "阳" : "阴");
    fmt::print("  第三课（支上神）: {} ({})\n", 
               si_ke.third.to_string(),
               si_ke.third.is_yang() ? "阳" : "阴");
    fmt::print("  第四课（神上神）: {} ({})\n", 
               si_ke.fourth.to_string(),
               si_ke.fourth.is_yang() ? "阳" : "阴");
    fmt::print("  干阳神: {}\n", Mapper::to_zh(si_ke.gan_yang_shen));
    fmt::print("  支阳神: {}\n", Mapper::to_zh(si_ke.zhi_yang_shen));
    fmt::print("\n");
}

// 显示三传（完整版，包含六亲、天干、神将）
void DaLiuRenController::display_san_chuan(const SanChuan& san_chuan, TianGan day_gan, DiZhi day_zhi) {
    fmt::print("【三传】\n");
    
    // 获取三传地支
    DiZhi chu = san_chuan.get_chu_chuan();
    DiZhi zhong = san_chuan.get_zhong_chuan(); 
    DiZhi mo = san_chuan.get_mo_chuan();
    
    // 获取遁干和六亲
    auto dun_gan = san_chuan.get_dun_gan(day_gan, day_zhi);
    auto liu_qin = san_chuan.get_liu_qin(day_gan);
    
    // 构建三传显示字符串
    std::array<std::string, 3> chuan_str;
    std::array<DiZhi, 3> chuan = {chu, zhong, mo};
    
    for (int i = 0; i < 3; ++i) {
        std::string str = std::string(liu_qin[i]) + " ";  // 六亲
        
        if (dun_gan[i].has_value()) {
            str += std::string(Mapper::to_zh(dun_gan[i].value()));  // 遁干
        } else {
            str += "空";  // 空亡
        }
        
        str += std::string(Mapper::to_zh(chuan[i]));  // 地支
        
        chuan_str[i] = str;
    }
    
    fmt::print("  初传: {}\n", chuan_str[0]);
    fmt::print("  中传: {}\n", chuan_str[1]);
    fmt::print("  末传: {}\n", chuan_str[2]);
    
    const auto& ke_shi = san_chuan.get_ke_shi();
    if (!ke_shi.empty()) {
        fmt::print("  课式: {}\n", fmt::join(ke_shi, ", "));
    }
    fmt::print("\n");
}

// 获取用户输入的日期
void DaLiuRenController::get_date_input(int& year, int& month, int& day, int& hour, bool& is_lunar) {
    std::string calendar_type;
    
    fmt::print("请选择历法（1=公历, 2=农历）[默认1]: ");
    std::string input;
    std::getline(std::cin, input);
    
    if (input.empty() || input == "1") {
        is_lunar = false;
        fmt::print("使用公历\n");
    } else {
        is_lunar = true;
        fmt::print("使用农历\n");
    }
    
    fmt::print("请输入年份: ");
    std::cin >> year;
    
    fmt::print("请输入月份: ");
    std::cin >> month;
    
    fmt::print("请输入日期: ");
    std::cin >> day;
    
    fmt::print("请输入时辰（0-23）: ");
    std::cin >> hour;
    
    // 清除输入缓冲区
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    
    fmt::print("\n输入的日期: {} 年 {} 月 {} 日 {} 时 ({})\n",
        year, month, day, hour, is_lunar ? "农历" : "公历");
}

// 格式化显示天地盘（圆形布局）
std::string DaLiuRenController::format_pan_circular(const TianDiPan& tdp) {
    // TODO: 实现圆形布局显示
    // 这是一个更高级的可视化功能，可以后续添加
    return "圆形布局显示功能待实现";
}

} // namespace ZhouYi::DaLiuRen::Controller