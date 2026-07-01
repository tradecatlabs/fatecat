// 八字系统示例
import ZhouYi.BaZiController;
import ZhouYi.GanZhi;
import ZhouYi.ZhMapper;
import fmt;
import std;

using namespace ZhouYi::BaZiController;
using namespace ZhouYi::GanZhi;
using namespace ZhouYi::Mapper;
using namespace std;

int main() {
    // AI 提示词输出
    fmt::print(R"(
- Role: 传统文化与命理学专家
- Background: 用户对八字算命感兴趣，可能是出于对传统文化的好奇，或者希望通过八字算命来了解自身运势、性格特点等。
- Profile: 你是一位精通传统文化与命理学的专家，对八字算命有着深入的研究和丰富的实践经验，熟悉八字的排盘、分析以及与人生吉凶祸福的关联。
- Skills: 你具备深厚的易学知识，能够准确推算八字，分析五行生克，解读命理信息，并结合现代人的生活实际，提供具有参考价值的建议。
- Goals: 为用户提供准确的八字排盘，分析八字中的五行属性、天干地支组合，解读其代表的性格特点、运势走向，并给出合理的建议。
- Constrains: 你的分析应基于传统文化的理论基础，避免迷信和夸大其词，尊重科学精神，不涉及封建迷信的内容，仅作为文化研究和参考。
- OutputFormat: 结合八字排盘结果、五行分析、性格解读、运势走向以及建议，以清晰、逻辑性强的文字形式呈现。
)");

    fmt::print("\n");
    fmt::print("\n");
    fmt::print("                    八字排盘系统                            \n");
    fmt::print("\n");
    fmt::print("\n");

    try {
        // 农历日期参数
        int lunar_year = 2005, lunar_month = 11, lunar_day = 2, lunar_hour = 8, lunar_minute =30 ;
        //int lunar_year = 2000, lunar_month = 6, lunar_day = 15, lunar_hour = 16, lunar_minute =30 ;
        //int lunar_year = 2005, lunar_month = 10, lunar_day = 23, lunar_hour = 19, lunar_minute =30 ;
        //int lunar_year = 2001, lunar_month = 5, lunar_day = 25, lunar_hour = 4, lunar_minute =30 ;
        bool is_male = false;

        auto result = pai_pan_lunar(lunar_year, lunar_month, lunar_day, lunar_hour, lunar_minute, is_male);

        // 从排盘结果中获取信息生成标题
        fmt::print("【八字排盘示例】农历{}年{}月{}日{}时{}分（{}）\n", 
                   lunar_year, lunar_month, lunar_day, result.birth_hour, result.birth_minute, result.is_male ? "男" : "女");
        fmt::print("\n");
        display_result(result);
        
        fmt::print("\n【八字详细信息】\n");
        fmt::print("\n");
        const auto& ba_zi = result.ba_zi;
        
        // 显示四柱
        fmt::print("年柱：{}\n", ba_zi.year.to_string());
        fmt::print("月柱：{}\n", ba_zi.month.to_string());
        fmt::print("日柱：{}\n", ba_zi.day.to_string());
        fmt::print("时柱：{}\n", ba_zi.hour.to_string());
        fmt::print("\n");

        // 显示十神关系
        fmt::print("【十神关系】\n");
        fmt::print("\n");
        fmt::print("年干对日干：{}\n", 
            shi_shen_to_zh(get_shi_shen(ba_zi.day.gan, ba_zi.year.gan)));
        fmt::print("月干对日干：{}\n", 
            shi_shen_to_zh(get_shi_shen(ba_zi.day.gan, ba_zi.month.gan)));
        fmt::print("时干对日干：{}\n", 
            shi_shen_to_zh(get_shi_shen(ba_zi.day.gan, ba_zi.hour.gan)));
        fmt::print("\n");

        // 显示大运信息
        fmt::print("【大运信息】\n");
        fmt::print("\n");
        display_da_yun(result, 10);  // 显示前5个大运
        fmt::print("\n");

        // 示例5：查看流年信息
        fmt::print("流年信息（2020-2030）\n");
        fmt::print("\n");
        display_liu_nian(result, 2020, 30);
        fmt::print("\n");

        fmt::print("2025年流月信息\n");
        fmt::print("\n");
        display_liu_yue(result, 2025);
        fmt::print("\n");

        fmt::print("2026年流月信息\n");
        fmt::print("\n");
        display_liu_yue(result, 2026);
        fmt::print("\n");

        fmt::print("2027年流月信息\n");
        fmt::print("\n");
        display_liu_yue(result, 2027);
        fmt::print("\n");

        // 示例7：查看流日信息
        fmt::print("2025年1月流日信息（前15天）\n");
        fmt::print("\n");
        display_liu_ri(result, 2026, 2, 60);
        fmt::print("\n");

    } catch (const std::exception& e) {
        fmt::print(" 错误：{}\n", e.what());
        return 1;
    }

    return 0;
}