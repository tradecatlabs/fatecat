// C++23 Module - 六爻排盘控制器接口
// 提供对外的六爻算法调用接口
export module ZhouYi.LiuYaoController;

// 导入第三方库模块
import nlohmann.json;

// 导入自定义模块
import ZhouYi.BaZiBase;  // 八字基础数据结构
import ZhouYi.GanZhi;    // 干支系统
import ZhouYi.LiuYao;    // 六爻内部实现

// 导入标准库模块
import std;

/**
 * @brief 六爻排盘控制器命名空间
 * 
 * 提供对外的六爻算法接口，封装内部实现细节
 */
export namespace ZhouYi::LiuYaoController {

// 重新导出必要的类型
using ZhouYi::BaZiBase::BaZi;
using ZhouYi::BaZiBase::Pillar;
using ZhouYi::LiuYao::YaoDetails;
using ZhouYi::LiuYao::HexagramInfo;

/**
 * @brief 六爻排盘结果
 * 
 * 封装排盘的所有结果信息
 */
struct LiuYaoPaiPanResult {
    std::vector<YaoDetails> yao_list;      // 六爻详细信息列表（从下到上，1-6爻）
    nlohmann::json json_data;               // 完整的 JSON 数据（英文 key）
    nlohmann::json ai_read_json_data;      // AI 可读的 JSON 数据（中文 key）
    
    // JSON 序列化支持
    friend void to_json(nlohmann::json& j, const LiuYaoPaiPanResult& r) {
        j = r.json_data;  // 直接使用内部的 JSON 数据
    }
};

/**
 * @brief 六爻排盘主接口
 * 
 * @param main_hexagram_code 主卦代码（6位二进制字符串，如 "010101"）
 *                           - '0' 表示阴爻（-- --）
 *                           - '1' 表示阳爻（———）
 *                           - 从下到上排列（第1位是初爻，第6位是上爻）
 * @param bazi 八字信息（用于计算旺衰、神煞等）
 * @param changing_line_indices 动爻位置列表（1-6，空列表表示无动爻）
 * @param generate_ai_json 是否生成 AI 可读的 JSON 数据（中文 key，默认 false）
 * 
 * @return LiuYaoPaiPanResult 排盘结果
 * 
 * @example
 * // 创建八字
 * auto bazi = ZhouYi::BaZiBase::BaZi::from_solar(2024, 10, 13, 14, 30);
 * 
 * // 排盘：主卦为 010101（从下到上），第3爻和第5爻动
 * auto result = calculate_liu_yao("010101", bazi, {3, 5}, true);
 * 
 * // 获取结果
 * for (const auto& yao : result.yao_list) {
 *     std::cout << "第" << yao.position << "爻: " 
 *               << yao.mainPillar.to_string() << std::endl;
 * }
 * 
 * // 导出 JSON（英文 key）
 * std::cout << result.json_data.dump(2) << std::endl;
 * 
 * // 导出 AI 可读 JSON（中文 key）
 * std::cout << result.ai_read_json_data.dump(2) << std::endl;
 */
LiuYaoPaiPanResult calculate_liu_yao(
    const std::string& main_hexagram_code,
    const BaZi& bazi,
    const std::vector<int>& changing_line_indices = {},
    bool generate_ai_json = false
);

/**
 * @brief 从爻辞生成主卦代码
 * 
 * @param yao_ci 爻辞数组（6个元素，从下到上）
 *               - 6：老阴（动）
 *               - 7：少阳
 *               - 8：少阴
 *               - 9：老阳（动）
 * @param out_changing_lines [输出] 动爻位置列表
 * @return 主卦代码（6位二进制字符串）
 * 
 * @example
 * std::vector<int> yao_ci = {7, 8, 6, 9, 7, 8};  // 从下到上
 * std::vector<int> changing_lines;
 * auto code = yao_ci_to_hexagram_code(yao_ci, changing_lines);
 * // code = "101010", changing_lines = {3, 4}
 * 
 * // 然后使用生成的代码进行排盘，可启用 AI JSON
 * auto result = calculate_liu_yao(code, bazi, changing_lines, true);
 */
std::string yao_ci_to_hexagram_code(
    const std::vector<int>& yao_ci,
    std::vector<int>& out_changing_lines
);

/**
 * @brief 从数字卦生成主卦代码（梅花易数、金钱卦等）
 * 
 * @param numbers 6个数字（从下到上）
 * @param odd_is_yang true 表示奇数为阳爻，false 表示偶数为阳爻（默认 true）
 * @return 主卦代码（6位二进制字符串）
 * 
 * @example
 * // 金钱卦：3个正面=阳爻(1)，3个反面=阴爻(0)
 * std::vector<int> numbers = {3, 2, 3, 1, 2, 3};  // 从下到上
 * auto code = numbers_to_hexagram_code(numbers, true);
 * 
 * // 然后使用生成的代码进行排盘，可启用 AI JSON
 * auto result = calculate_liu_yao(code, bazi, {}, true);
 */
std::string numbers_to_hexagram_code(
    const std::vector<int>& numbers,
    bool odd_is_yang = true
);

/**
 * @brief 获取卦象信息（不进行完整排盘）
 * 
 * @param hexagram_code 卦象代码（6位二进制字符串）
 * @return 卦象基本信息
 */
HexagramInfo get_hexagram_info(const std::string& hexagram_code);

/**
 * @brief 批量排盘（用于批量处理）
 * 
 * @param requests 批量请求列表，每个请求包含 {卦象代码, 八字, 动爻列表}
 * @param generate_ai_json 是否生成 AI 可读的 JSON 数据（中文 key，默认 false）
 * @return 批量结果列表
 */
std::vector<LiuYaoPaiPanResult> batch_calculate_liu_yao(
    const std::vector<std::tuple<std::string, BaZi, std::vector<int>>>& requests,
    bool generate_ai_json = false
);

} // namespace ZhouYi::LiuYaoController

