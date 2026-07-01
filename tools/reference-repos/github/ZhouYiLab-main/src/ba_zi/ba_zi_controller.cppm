// C++23 Module - 八字控制器接口
// 提供对外的八字算法调用接口
export module ZhouYi.BaZiController;

// 导入第三方库模块
import fmt;
import nlohmann.json;

// 导入自定义模块
import ZhouYi.BaZiBase;  // 八字基础数据结构
import ZhouYi.GanZhi;    // 干支系统
import ZhouYi.BaZi;      // 八字内部实现

// 导入标准库模块
import std;

/**
 * @brief 八字控制器命名空间
 * 
 * 提供对外的八字算法接口，封装内部实现细节
 */
export namespace ZhouYi::BaZiController {

// 重新导出必要的类型
using ZhouYi::BaZiBase::BaZi;
using ZhouYi::BaZiBase::Pillar;
using ZhouYi::BaZi::BaZiResult;
using ZhouYi::BaZi::DaYun;
using ZhouYi::BaZi::LiuNian;
using ZhouYi::BaZi::LiuYue;
using ZhouYi::BaZi::LiuRi;
using ZhouYi::BaZi::LiuShi;
using ZhouYi::GanZhi::ShiShen;
using ZhouYi::GanZhi::shi_shen_to_zh;

/**
 * @brief 八字排盘主接口
 * 
 * @param year 公历年
 * @param month 公历月（1-12）
 * @param day 公历日（1-31）
 * @param hour 公历时（0-23）
 * @param minute 公历分（0-59，默认0）
 * @param is_male 是否为男性
 * @return BaZiResult 完整的八字排盘结果
 * 
 * @example
 * // 排一个男性的八字，1990年1月1日12时出生
 * auto result = pai_pan_solar(1990, 1, 1, 12, 0, true);
 * 
 * // 获取八字
 * const auto& bazi = result.ba_zi;
 * std::println("年柱: {}", bazi.year.to_string());
 * 
 * // 获取大运
 * for (const auto& dy : result.da_yun_system.get_da_yun_list()) {
 *     std::println("{}", dy.to_string());
 * }
 * 
 * // 获取流年
 * auto liu_nian_2024 = result.get_liu_nian(2024);
 * std::println("2024年流年: {}", liu_nian_2024.to_string());
 */
BaZiResult pai_pan_solar(int year, int month, int day, int hour, 
                         int minute = 0, bool is_male = true);

/**
 * @brief 从农历排盘
 * 
 * @param year 农历年
 * @param month 农历月（1-12，负数表示闰月）
 * @param day 农历日（1-30）
 * @param hour 时辰（0-23）
 * @param minute 分钟（0-59，默认0）
 * @param is_male 是否为男性
 * @return BaZiResult 完整的八字排盘结果
 */
BaZiResult pai_pan_lunar(int year, int month, int day, int hour,
                         int minute = 0, bool is_male = true);

/**
 * @brief 显示八字排盘结果（控制台输出）
 * 
 * @param result 排盘结果
 */
void display_result(const BaZiResult& result);

/**
 * @brief 显示大运信息
 * 
 * @param result 排盘结果
 * @param max_count 显示的大运数量（默认10个）
 */
void display_da_yun(const BaZiResult& result, int max_count = 10);

/**
 * @brief 显示流年信息
 * 
 * @param result 排盘结果
 * @param start_year 开始年份
 * @param count 显示的年数（默认10年）
 */
void display_liu_nian(const BaZiResult& result, int start_year, int count = 10);

/**
 * @brief 显示流月信息
 * 
 * @param result 排盘结果
 * @param year 年份
 */
void display_liu_yue(const BaZiResult& result, int year);

/**
 * @brief 显示流日信息
 * 
 * @param result 排盘结果
 * @param year 年份
 * @param month 月份
 * @param day_count 显示的天数（默认30天）
 */
void display_liu_ri(const BaZiResult& result, int year, int month, int day_count = 30);

/**
 * @brief 显示童限详细信息
 * 
 * @param result 排盘结果
 * 
 * 显示起运的精确信息：起运年龄、年月日时分
 */
void display_child_limit_detail(const BaZiResult& result);

/**
 * @brief 显示 tyme 库大运详细信息
 * 
 * @param result 排盘结果
 * @param index 大运索引（0开始）
 * 
 * 显示单个大运的完整信息，包括起止年份、干支等
 */
void display_tyme_decade_fortune(const BaZiResult& result, int index);

/**
 * @brief 批量排盘
 * 
 * @param requests 批量请求列表，每个请求包含 {年, 月, 日, 时, 性别}
 * @return 批量结果列表
 */
std::vector<BaZiResult> batch_pai_pan(
    const std::vector<std::tuple<int, int, int, int, bool>>& requests);

} // namespace ZhouYi::BaZiController

