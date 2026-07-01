// 大六壬系统示例
import ZhouYi.DaLiuRen.Controller;
import ZhouYi.GanZhi;
import fmt;
import std;

using namespace ZhouYi::DaLiuRen::Controller;
using namespace ZhouYi::GanZhi;
using namespace std;

int main() {
    fmt::print("\n");
    fmt::print("\n");
    fmt::print("                  大六壬系统示例演示                        \n");
    fmt::print("\n");
    fmt::print("\n");

    try {
        // 示例1：阳历起课
        fmt::print("【示例1】阳历起课\n");
        fmt::print("\n");
        fmt::print("起课时间：2025年11月3日 16时\n\n");
        auto result1 = DaLiuRenController::pai_pan_solar(2025, 11, 3, 16);
        DaLiuRenController::display_result(result1);
        fmt::print("\n");

        /*
        // 示例2：农历起课
        fmt::print("【示例2】农历起课\n");
        fmt::print("\n");
        fmt::print("起课时间：农历2025年五月二十日 午时\n\n");
        auto result2 = DaLiuRenController::pai_pan_lunar(2025, 5, 20, 11);
        DaLiuRenController::display_result(result2);
        fmt::print("\n");

        // 示例3：查看详细排盘信息
        fmt::print("【示例3】查看详细排盘信息\n");
        fmt::print("\n");
        auto result3 = DaLiuRenController::pai_pan_solar(2025, 6, 15, 14);
        DaLiuRenController::display_result_detailed(result3);
        fmt::print("\n");
        */

        // 示例4：查看四课和三传
        fmt::print("【示例4】查看四课和三传\n");
        fmt::print("\n");
        auto result4 = DaLiuRenController::pai_pan_solar(2025, 11, 3, 16);
        DaLiuRenController::display_si_ke(result4.si_ke);
        fmt::print("\n");
        DaLiuRenController::display_san_chuan(result4.san_chuan, result4.ba_zi.day.gan, result4.ba_zi.day.zhi);
        fmt::print("\n");
        DaLiuRenController::display_result_detailed(result4);
    } catch (const std::exception& e) {
        fmt::print(" 错误：{}\n", e.what());
        return 1;
    }

    fmt::print(" 大六壬系统示例演示完成！\n\n");
    return 0;
}