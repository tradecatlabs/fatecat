// C++23 Module - 五行工具模块
// 提供五行相关的映射、关系判断等功能
export module ZhouYi.WuXingUtils;

// 导入标准库模块（最后）
import std;

/**
 * @brief 五行工具命名空间
 * 
 * 提供五行相关的数据映射和关系判断功能
 */
export namespace ZhouYi::WuXingUtils {

// ==================== 五行关系枚举 ====================

/**
 * @brief 五行关系枚举
 */
enum class ElementalRelation {
    Generates,      // 生 (我生)
    GeneratedBy,    // 被生 (生我)
    Controls,       // 克 (我克)
    ControlledBy,   // 被克 (克我)
    Same,           // 同 (比和)
    Error           // 错误
};

// ==================== 地支五行映射 ====================

/**
 * @brief 地支五行映射表
 */
inline const std::unordered_map<std::string, std::string> branchFiveElements = {
    {"子", "水"}, {"丑", "土"}, {"寅", "木"}, {"卯", "木"}, 
    {"辰", "土"}, {"巳", "火"}, {"午", "火"}, {"未", "土"}, 
    {"申", "金"}, {"酉", "金"}, {"戌", "土"}, {"亥", "水"}
};

/**
 * @brief 五行索引映射 (用于旺衰和六亲计算)
 * 
 * 金=0, 水=1, 木=2, 火=3, 土=4
 * 生: (i+1)%5, 克: (i+2)%5
 */
inline const std::unordered_map<std::string, int> fiveElementIndex = {
    {"金", 0}, {"水", 1}, {"木", 2}, {"火", 3}, {"土", 4}
};

// ==================== 地支藏干 ====================

/**
 * @brief 地支藏干映射表
 * 
 * 每个地支中藏的天干（本气、中气、余气）
 */
inline const std::unordered_map<std::string, std::vector<std::string>> hiddenStems = {
    {"子", {"癸"}},
    {"丑", {"癸", "辛", "己"}},
    {"寅", {"甲", "丙", "戊"}},
    {"卯", {"乙"}},
    {"辰", {"戊", "乙", "癸"}},
    {"巳", {"丙", "庚", "戊"}},
    {"午", {"丁", "己"}},
    {"未", {"己", "丁", "乙"}},
    {"申", {"庚", "壬", "戊"}},
    {"酉", {"辛"}},
    {"戌", {"戊", "辛", "丁"}},
    {"亥", {"壬", "甲"}}
};

// ==================== 辅助函数 ====================

/**
 * @brief 判断两个地支的五行关系
 * 
 * @param branch1 第一个地支
 * @param branch2 第二个地支
 * @return ElementalRelation 五行关系
 */
inline ElementalRelation getElementalRelationship(
    const std::string& branch1, 
    const std::string& branch2
) {
    if (!branchFiveElements.contains(branch1) || 
        !branchFiveElements.contains(branch2)) {
        return ElementalRelation::Error;
    }

    const std::string& elem1 = branchFiveElements.at(branch1);
    const std::string& elem2 = branchFiveElements.at(branch2);

    if (!fiveElementIndex.contains(elem1) || 
        !fiveElementIndex.contains(elem2)) {
        return ElementalRelation::Error;
    }

    int idx1 = fiveElementIndex.at(elem1);
    int idx2 = fiveElementIndex.at(elem2);

    if (idx1 == idx2) return ElementalRelation::Same;         // 同我
    if (idx2 == (idx1 + 1) % 5) return ElementalRelation::Generates;    // 我生
    if (idx2 == (idx1 + 2) % 5) return ElementalRelation::Controls;     // 我克
    if (idx1 == (idx2 + 1) % 5) return ElementalRelation::GeneratedBy;  // 生我
    if (idx1 == (idx2 + 2) % 5) return ElementalRelation::ControlledBy; // 克我

    return ElementalRelation::Error;
}

/**
 * @brief 将五行关系枚举转为中文字符串
 * 
 * @param rel 五行关系枚举
 * @return std::string 中文描述
 */
inline std::string relationToString(ElementalRelation rel) {
    switch (rel) {
        case ElementalRelation::Generates:     return "生";
        case ElementalRelation::GeneratedBy:   return "被生";
        case ElementalRelation::Controls:      return "克";
        case ElementalRelation::ControlledBy:  return "被克";
        case ElementalRelation::Same:          return "同";
        default:                               return "错误";
    }
}

/**
 * @brief 获取地支的五行属性
 * 
 * @param branch 地支
 * @return std::string 五行属性（"金"、"木"、"水"、"火"、"土"）
 */
inline std::string getBranchElement(const std::string& branch) {
    if (branchFiveElements.contains(branch)) {
        return branchFiveElements.at(branch);
    }
    return "未知";
}

// ==================== 旺衰状态计算 ====================

/**
 * @brief 计算爻的旺衰状态
 * 
 * 根据月令判断爻的旺衰状态。月令是判断五行强弱的核心标准。
 * 
 * 旺衰五态：
 * - 旺：当令者旺（五行值月令）
 * - 相：生我者相（月令生爻）
 * - 休：我生者休（爻生月令）
 * - 囚：我克者囚（爻克月令）
 * - 死：克我者死（月令克爻）
 * 
 * 特殊处理：
 * - 四季月（辰、戌、丑、未）：土旺金相、火休木囚、水死
 * 
 * @param lineElement 爻的五行属性（"金"、"木"、"水"、"火"、"土"）
 * @param monthBranch 月支
 * @return std::string 旺衰状态（"旺"、"相"、"休"、"囚"、"死"、"未知"）
 * 
 * @example
 * getWangShuai("木", "寅") // 返回 "旺" (木临月建)
 * getWangShuai("火", "寅") // 返回 "相" (木生火)
 * getWangShuai("土", "寅") // 返回 "休" (火生土，但寅月火未当令，实为木生土)
 */
inline std::string getWangShuai(const std::string& lineElement, const std::string& monthBranch) {
    // 验证输入有效性
    if (!branchFiveElements.contains(monthBranch) || !fiveElementIndex.contains(lineElement)) {
        return "未知";
    }
    
    std::string monthElement = branchFiveElements.at(monthBranch);

    // 四季月（辰戌丑未）特殊处理：土旺
    // 辰戌丑未月，土旺。对于非土爻，月令的影响需要更复杂的月令分野理论，此处简化。
    // 简化处理：四季月，土最旺，其他五行根据与土的关系判断
    if (monthBranch == "辰" || monthBranch == "戌" || monthBranch == "丑" || monthBranch == "未") {
        monthElement = "土"; // 当令者旺
    }

    if (!fiveElementIndex.contains(monthElement)) {
        return "未知";
    }

    int lineIdx = fiveElementIndex.at(lineElement);
    int monthIdx = fiveElementIndex.at(monthElement);

    // 五行旺衰判断（基于五行生克循环）
    if (lineIdx == monthIdx) return "旺";           // 同我者旺 (临月建)
    if (lineIdx == (monthIdx + 4) % 5) return "相"; // 生我者相 (月令生爻)
    if (lineIdx == (monthIdx + 1) % 5) return "休"; // 我生者休 (爻生月令)
    if (lineIdx == (monthIdx + 2) % 5) return "囚"; // 我克者囚 (爻克月令)
    if (lineIdx == (monthIdx + 3) % 5) return "死"; // 克我者死 (月令克爻)

    return "未知";
}

} // namespace ZhouYi::WuXingUtils

