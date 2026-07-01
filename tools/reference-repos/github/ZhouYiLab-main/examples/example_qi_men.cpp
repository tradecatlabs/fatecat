// 奇门遁甲排盘示例程序
// 支持农历和公历日期的排盘算法

import ZhouYi.QiMen;
import ZhouYi.QiMen.Pan;
import ZhouYi.QiMen.Controller;
import fmt;
import std;

/**
 * @brief 主程序 - 演示奇门排盘
 */
int main() {
    using namespace ZhouYi::QiMen;
    
    fmt::println("");
    fmt::println("      奇门遁甲排盘示例程序              ");
    fmt::println("   支持农历和公历日期的排盘算法        ");
    fmt::println("\n");
    
    // 示例1：公历排盘 - 2011年6月18日 3时56分
    fmt::println("【示例1】公历排盘");
    fmt::println("日期：2011年6月18日 3时56分\n");
    
    auto result1 = QiMenController::pai_pan_solar(2011, 6, 18, 3, 56);
    if (result1) {
        const auto& pan = result1.value();
        fmt::println(" 排盘成功");
        fmt::println("  阴阳遁：{}", pan.dun == Dun::Yang ? "阳遁" : "阴遁");
        fmt::println("  局数：第{}局\n", pan.ju);
        
        // 显示完整的九宫排盘
        auto full_pan = QiMenController::get_pan_description(pan);
        fmt::println("{}", full_pan);
    } else {
        fmt::println(" 排盘失败：{}\n", result1.error());
    }
    
    // 示例2：公历排盘 - 2002年11月19日 0时
    fmt::println("\n【示例2】公历排盘");
    fmt::println("日期：2002年11月19日 0时\n");
    
    auto result2 = QiMenController::pai_pan_solar(2002, 11, 19, 0, 0);
    if (result2) {
        const auto& pan = result2.value();
        fmt::println(" 排盘成功");
        fmt::println("  阴阳遁：{}", pan.dun == Dun::Yang ? "阳遁" : "阴遁");
        fmt::println("  局数：第{}局\n", pan.ju);
        
        // 显示完整的九宫排盘
        auto full_pan = QiMenController::get_pan_description(pan);
        fmt::println("{}", full_pan);
    } else {
        fmt::println(" 排盘失败：{}\n", result2.error());
    }
    
    // 示例3：公历排盘 - 2023年6月21日 12时
    fmt::println("\n【示例3】公历排盘");
    fmt::println("日期：2023年6月21日 12时\n");
    
    auto result3 = QiMenController::pai_pan_solar(2023, 6, 21, 12, 0);
    if (result3) {
        const auto& pan = result3.value();
        fmt::println(" 排盘成功");
        fmt::println("  阴阳遁：{}", pan.dun == Dun::Yang ? "阳遁" : "阴遁");
        fmt::println("  局数：第{}局\n", pan.ju);
        auto summary = QiMenAnalyzer::get_summary(pan);
        fmt::println("{}", summary);
    } else {
        fmt::println(" 排盘失败：{}\n", result3.error());
    }
    
    // 示例4：农历排盘 - 农历五月初五 14时
    fmt::println("\n【示例4】农历排盘");
    fmt::println("日期：农历2023年5月5日 14时\n");
    
    auto result4 = QiMenController::pai_pan_lunar(2023, 5, 5, 14, 30);
    if (result4) {
        const auto& pan = result4.value();
        fmt::println(" 排盘成功");
        fmt::println("  阴阳遁：{}", pan.dun == Dun::Yang ? "阳遁" : "阴遁");
        fmt::println("  局数：第{}局\n", pan.ju);
        auto summary = QiMenAnalyzer::get_summary(pan);
        fmt::println("{}", summary);
    } else {
        fmt::println(" 排盘失败：{}\n", result4.error());
    }
    
    // 示例5：分析吉凶
    fmt::println("\n【示例5】分析宫位吉凶");
    if (result1) {
        const auto& pan = result1.value();
        auto analysis = QiMenAnalyzer::analyze_auspiciousness(pan, Palace::South);
        if (analysis) {
            fmt::println("南宫（离九宫）分析：\n{}", analysis.value());
        }
    }
    
    // 示例6：JSON 输出（有序）
    fmt::println("\n【示例6】JSON 格式输出（保持字段顺序）");
    if (result1) {
        const auto& pan = result1.value();
        auto json_str = QiMenController::get_pan_json_ordered(pan);
        fmt::println("{}", json_str);
    }
    
    fmt::println("\n");
    fmt::println("         示例程序执行完成               ");
    fmt::println("");
    
    return 0;
}
