// 中文映射辅助模块 - 用于枚举与中文的互相映射
// 基于 magic_enum 实现

// 导出模块
export module ZhouYi.ZhMapper;

// 先导入第三方库模块
import magic_enum;

// 导入标准库（最后）
import std;

/**
 * @brief 中文映射辅助命名空间
 * 
 * 提供枚举与中文字符串的双向映射功能
 */
export namespace ZhouYi::Mapper {

/**
 * @brief 中文映射表
 * @tparam E 枚举类型
 * 
 * 使用方法：
 * 1. 特化此模板为你的枚举类型
 * 2. 实现 get_map() 函数返回 std::array<std::string_view, N>
 */
template<typename E>
struct ZhMap {
    static_assert(std::is_enum_v<E>, "E must be an enum type");
    // 默认实现：没有中文映射，返回枚举名称
    static constexpr auto get_map() -> std::array<std::string_view, magic_enum::enum_count<E>()> {
        return {};
    }
};

/**
 * @brief 获取枚举的中文名称
 * @tparam E 枚举类型
 * @param value 枚举值
 * @return 中文名称，如果没有映射则返回英文名称
 */
template<typename E>
constexpr auto to_zh(E value) -> std::string_view {
    constexpr auto zh_map = ZhMap<E>::get_map();
    
    // 如果有中文映射表
    if constexpr (zh_map.size() > 0) {
        auto index = magic_enum::enum_index(value);
        if (index.has_value() && index.value() < zh_map.size()) {
            auto zh_name = zh_map[index.value()];
            if (!zh_name.empty()) {
                return zh_name;
            }
        }
    }
    
    // 回退到英文名称
    return magic_enum::enum_name(value);
}

/**
 * @brief 从中文名称获取枚举值
 * @tparam E 枚举类型
 * @param zh_name 中文名称
 * @return 枚举值的 optional
 */
template<typename E>
constexpr auto from_zh(std::string_view zh_name) -> std::optional<E> {
    constexpr auto zh_map = ZhMap<E>::get_map();
    constexpr auto values = magic_enum::enum_values<E>();
    
    // 在中文映射表中查找
    if constexpr (zh_map.size() > 0) {
        for (std::size_t i = 0; i < zh_map.size(); ++i) {
            if (zh_map[i] == zh_name) {
                return values[i];
            }
        }
    }
    
    // 回退到英文名称查找
    return magic_enum::enum_cast<E>(zh_name);
}

/**
 * @brief 获取所有枚举值的中文名称列表
 * @tparam E 枚举类型
 * @return 中文名称列表
 */
template<typename E>
constexpr auto get_all_zh_names() -> std::array<std::string_view, magic_enum::enum_count<E>()> {
    constexpr auto values = magic_enum::enum_values<E>();
    std::array<std::string_view, values.size()> result{};
    
    for (std::size_t i = 0; i < values.size(); ++i) {
        result[i] = to_zh(values[i]);
    }
    
    return result;
}

/**
 * @brief 获取枚举的所有信息（英文名、中文名、值）
 * @tparam E 枚举类型
 */
template<typename E>
struct EnumInfo {
    E value;
    std::string_view en_name;
    std::string_view zh_name;
    std::underlying_type_t<E> underlying_value;
};

/**
 * @brief 获取所有枚举的详细信息
 * @tparam E 枚举类型
 * @return 枚举信息列表
 */
template<typename E>
constexpr auto get_all_info() -> std::array<EnumInfo<E>, magic_enum::enum_count<E>()> {
    constexpr auto values = magic_enum::enum_values<E>();
    std::array<EnumInfo<E>, values.size()> result{};
    
    for (std::size_t i = 0; i < values.size(); ++i) {
        result[i] = EnumInfo<E>{
            .value = values[i],
            .en_name = magic_enum::enum_name(values[i]),
            .zh_name = to_zh(values[i]),
            .underlying_value = magic_enum::enum_integer(values[i])
        };
    }
    
    return result;
}

/**
 * @brief 枚举迭代器辅助
 * @tparam E 枚举类型
 * 
 * 使用方法：
 * for (auto value : ZhouYi::Mapper::enum_range<MyEnum>()) {
 *     // 处理每个枚举值
 * }
 */
template<typename E>
constexpr auto enum_range() {
    return magic_enum::enum_values<E>();
}

/**
 * @brief 检查字符串是否为有效的枚举值（英文或中文）
 * @tparam E 枚举类型
 * @param name 名称字符串
 * @return true 如果有效
 */
template<typename E>
constexpr bool is_valid_name(std::string_view name) {
    // 检查英文名
    if (magic_enum::enum_cast<E>(name).has_value()) {
        return true;
    }
    
    // 检查中文名
    if (from_zh<E>(name).has_value()) {
        return true;
    }
    
    return false;
}

} // namespace ZhouYi::Mapper

