// 六爻排盘控制器实现文件
// 实现对外的六爻算法接口

// 导入模块接口
module ZhouYi.LiuYaoController;

// 导入内部实现
import ZhouYi.LiuYao;

// 导入标准库
import std;

namespace ZhouYi::LiuYaoController {

// 使用内部命名空间
using namespace ZhouYi::LiuYao;

/**
 * @brief 六爻排盘主接口实现
 */
LiuYaoPaiPanResult calculate_liu_yao(
    const std::string& main_hexagram_code,
    const BaZi& bazi,
    const std::vector<int>& changing_line_indices,
    bool generate_ai_json
) {
    // 验证卦象代码
    if (main_hexagram_code.length() != 6) {
        throw std::invalid_argument("卦象代码必须是6位二进制字符串");
    }
    
    for (char c : main_hexagram_code) {
        if (c != '0' && c != '1') {
            throw std::invalid_argument("卦象代码只能包含 '0' 和 '1'");
        }
    }
    
    // 验证动爻位置
    for (int pos : changing_line_indices) {
        if (pos < 1 || pos > 6) {
            throw std::invalid_argument("动爻位置必须在 1-6 之间");
        }
    }
    
    // 调用内部排盘函数
    auto [yao_list, json_data] = sixYaoDivination(main_hexagram_code, bazi, changing_line_indices);
    
    // 生成 AI 可读的 JSON（如果需要）
    nlohmann::json ai_read_json_data;
    if (generate_ai_json) {
        ai_read_json_data = aiSetSixYaoDivination(yao_list, json_data);
    }
    
    // 返回结果
    return LiuYaoPaiPanResult{
        .yao_list = std::move(yao_list),
        .json_data = std::move(json_data),
        .ai_read_json_data = std::move(ai_read_json_data)
    };
}

/**
 * @brief 从爻辞生成主卦代码实现
 */
std::string yao_ci_to_hexagram_code(
    const std::vector<int>& yao_ci,
    std::vector<int>& out_changing_lines
) {
    if (yao_ci.size() != 6) {
        throw std::invalid_argument("爻辞必须包含6个数字");
    }
    
    std::string code;
    code.reserve(6);
    out_changing_lines.clear();
    
    for (std::size_t i = 0; i < 6; ++i) {
        int value = yao_ci[i];
        int position = static_cast<int>(i) + 1;  // 爻位（1-6）
        
        switch (value) {
            case 6:  // 老阴（动）
                code += '0';
                out_changing_lines.push_back(position);
                break;
            case 7:  // 少阳
                code += '1';
                break;
            case 8:  // 少阴
                code += '0';
                break;
            case 9:  // 老阳（动）
                code += '1';
                out_changing_lines.push_back(position);
                break;
            default:
                throw std::invalid_argument(
                    "爻辞值必须是 6（老阴）、7（少阳）、8（少阴）或 9（老阳）"
                );
        }
    }
    
    return code;
}

/**
 * @brief 从数字卦生成主卦代码实现
 */
std::string numbers_to_hexagram_code(
    const std::vector<int>& numbers,
    bool odd_is_yang
) {
    if (numbers.size() != 6) {
        throw std::invalid_argument("数字列表必须包含6个元素");
    }
    
    std::string code;
    code.reserve(6);
    
    for (int num : numbers) {
        bool is_yang = odd_is_yang ? (num % 2 == 1) : (num % 2 == 0);
        code += is_yang ? '1' : '0';
    }
    
    return code;
}

/**
 * @brief 获取卦象信息实现
 */
HexagramInfo get_hexagram_info(const std::string& hexagram_code) {
    if (hexagram_code.length() != 6) {
        throw std::invalid_argument("卦象代码必须是6位二进制字符串");
    }
    
    for (char c : hexagram_code) {
        if (c != '0' && c != '1') {
            throw std::invalid_argument("卦象代码只能包含 '0' 和 '1'");
        }
    }
    
    // 从内部映射表获取卦象信息
    const auto& hexagram_map = get_hexagram_map();
    auto it = hexagram_map.find(hexagram_code);
    
    if (it != hexagram_map.end()) {
        return it->second;
    } else {
        throw std::runtime_error("未找到卦象代码: " + hexagram_code);
    }
}

/**
 * @brief 批量排盘实现
 */
std::vector<LiuYaoPaiPanResult> batch_calculate_liu_yao(
    const std::vector<std::tuple<std::string, BaZi, std::vector<int>>>& requests,
    bool generate_ai_json
) {
    std::vector<LiuYaoPaiPanResult> results;
    results.reserve(requests.size());
    
    for (const auto& [code, bazi, changing_lines] : requests) {
        try {
            results.push_back(calculate_liu_yao(code, bazi, changing_lines, generate_ai_json));
        } catch (const std::exception& e) {
            // 失败时添加空结果，并在 JSON 中记录错误
            LiuYaoPaiPanResult error_result;
            error_result.json_data["error"] = e.what();
            error_result.json_data["hexagram_code"] = code;
            results.push_back(std::move(error_result));
        }
    }
    
    return results;
}

} // namespace ZhouYi::LiuYaoController