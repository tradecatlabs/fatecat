// 紫微斗数系统示例
import ZhouYi.ZiWei.Controller;
import ZhouYi.ZiWei.Constants;
import ZhouYi.GanZhi;
import fmt;
import std;

using namespace ZhouYi::ZiWei;
using namespace ZhouYi::GanZhi;
using namespace std;

int main() {
    fmt::print("\n");
    fmt::print("\n");
    fmt::print("                  紫微斗数系统示例演示                      \n");
    fmt::print("\n");
    fmt::print("\n");

    try {
        // 示例1：公历排盘并显示
        fmt::print("【示例1】公历排盘：1990年5月20日14时（男）\n");
        fmt::print("\n");
        pai_pan_and_print_solar(1990, 5, 20, 14, true);
        fmt::print("\n");

        // 示例2：农历排盘并显示
        fmt::print("【示例2】农历排盘：农历1990年四月二十六日未时（女）\n");
        fmt::print("\n");
        pai_pan_and_print_lunar(1990, 4, 26, 13, false);
        fmt::print("\n");

        // 示例3：查看特定宫位详情（需要先获取结果）
        fmt::print("【示例3】查看命宫详细信息\n");
        fmt::print("\n");
        // 注意：由于 pai_pan_solar 没有导出，我们使用 pai_pan_and_print_solar 的变体
        // 这里演示使用控制器显示功能
        fmt::print("（使用 pai_pan_and_print_solar 已包含详细信息）\n\n");

        // 示例4：四化系统分析
        fmt::print("【示例4】四化系统分析示例\n");
        fmt::print("\n");
        fmt::print("（四化分析已包含在 pai_pan_and_print_solar 输出中）\n\n");

        // 示例5：格局分析
        fmt::print("【示例5】格局分析示例\n");
        fmt::print("\n");
        fmt::print("（格局分析已包含在 pai_pan_and_print_solar 输出中）\n\n");

        // 示例6：运限分析
        fmt::print("【示例6】运限分析示例\n");
        fmt::print("\n");
        fmt::print("（大限、流年等分析已包含在 pai_pan_and_print_solar 输出中）\n\n");

        fmt::print("提示：pai_pan_and_print_solar() 函数已经包含了完整的排盘结果，\n");
        fmt::print("包括十二宫、星耀、四化、格局、大限、流年等所有信息。\n\n");

    } catch (const exception& e) {
        fmt::print(" 错误：{}\n", e.what());
        return 1;
    }

    fmt::print(" 紫微斗数系统示例演示完成！\n\n");
    return 0;
}
