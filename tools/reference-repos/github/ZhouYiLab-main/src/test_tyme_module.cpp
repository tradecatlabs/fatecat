// 测试 tyme 模块

// 导入 tyme 模块
import ZhouYi.tyme;
import ZhouYi.tyme.util;

// 导入 fmt
import fmt;

// 导入标准库（最后）
import std;

int main() {
    // 测试 tyme 模块是否能正常使用
    fmt::print(fg(fmt::color::green), "=== 测试 Tyme 模块 ===\n\n");
    
    // 创建一个公历日期
    auto solar = tyme::SolarDay::from_ymd(2025, 1, 1);
    fmt::print("公历日期: {}\n", solar.to_string());
    
    // 转换为农历
    auto lunar = solar.get_lunar_day();
    fmt::print("农历日期: {}\n", lunar.to_string());
    
    fmt::print("\n");
    fmt::print(fg(fmt::color::cyan), " Tyme 模块测试成功！\n");
    
    return 0;
}