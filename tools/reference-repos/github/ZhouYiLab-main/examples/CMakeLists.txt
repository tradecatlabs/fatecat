# ==============================================================================
# ZhouYiLab 示例程序配置
# ==============================================================================

# 如果单独编译examples，需要设置项目名
if(NOT PROJECT_NAME)
    project(ZhouYiLab_Examples
        VERSION 1.0.0
        LANGUAGES CXX
    )
    
    # 设置C++23标准
    set(CMAKE_CXX_STANDARD 23)
    set(CMAKE_CXX_STANDARD_REQUIRED ON)
    set(CMAKE_CXX_EXTENSIONS OFF)
    
    # 添加父目录以访问主项目的模块
    add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/.. ${CMAKE_CURRENT_BINARY_DIR}/ZhouYiLab)
endif()

# 确保支持C++模块
if(NOT CMAKE_CXX_STANDARD EQUAL 23)
    message(FATAL_ERROR "Examples require C++23 support")
endif()

# ==============================================================================
# 示例程序配置选项
# ==============================================================================

# 默认不构建示例程序，加快编译速度
option(BUILD_EXAMPLES "Build example programs" OFF)

# 示例程序列表及描述
set(EXAMPLES
    example_asio        # "Asio 异步网络示例"
    example_ba_zi       # "八字排盘示例"
    example_da_liu_ren  # "大六壬起课示例"
    example_liu_yao     # "六爻起卦示例"
    example_zi_wei      # "紫微斗数排盘示例"
    example_stacktrace  # "std::stacktrace 功能测试"
    example_qi_men      # "奇门遁甲排盘示例"
)

# ==============================================================================
# 辅助函数：创建示例可执行文件
# ==============================================================================

function(add_zhouyi_example name)
    # 如果 BUILD_EXAMPLES 为 OFF，则使用 EXCLUDE_FROM_ALL
    # 这样默认构建时不会编译示例，但可以手动构建指定示例
    if(NOT BUILD_EXAMPLES)
        add_executable(${name} EXCLUDE_FROM_ALL ${name}.cpp)
    else()
        add_executable(${name} ${name}.cpp)
    endif()
    
    # 设置模块依赖
    target_compile_features(${name} PRIVATE cxx_std_23)
    
    # 链接核心库（包含所有模块）
    target_link_libraries(${name} PRIVATE ZhouYiLabCore)
    
    # 设置输出目录
    set_target_properties(${name} PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/examples
    )
    
    # 设置模块生成模式
    set_property(TARGET ${name} PROPERTY
        CXX_MODULE_GENERATION_MODE "SEPARATE"
    )
endfunction()

# ==============================================================================
# 创建所有示例程序
# ==============================================================================

foreach(EXAMPLE ${EXAMPLES})
    add_zhouyi_example(${EXAMPLE})
endforeach()

# 创建一个目标来一次性构建所有示例
add_custom_target(all_examples
    DEPENDS ${EXAMPLES}
    COMMENT "构建所有示例程序"
)

# ==============================================================================
# 提示信息
# ==============================================================================

message(STATUS "==========================================")
message(STATUS "示例程序配置:")
if(BUILD_EXAMPLES)
    message(STATUS "  BUILD_EXAMPLES: ON (示例会自动构建)")
else()
    message(STATUS "  BUILD_EXAMPLES: OFF (示例默认不构建)")
    message(STATUS "")
    message(STATUS "  如需构建所有示例，运行:")
    message(STATUS "    cmake --build . --target all_examples")
    message(STATUS "")
    message(STATUS "  如需构建单个示例，运行:")
    message(STATUS "    cmake --build . --target example_ba_zi")
    message(STATUS "")
    message(STATUS "  或启用自动构建:")
    message(STATUS "    cmake -DBUILD_EXAMPLES=ON ..")
endif()
message(STATUS "")
message(STATUS "  可用示例:")
message(STATUS "    - example_asio         : Asio 异步网络示例")
message(STATUS "    - example_ba_zi        : 八字排盘示例")
message(STATUS "    - example_da_liu_ren   : 大六壬起课示例")
message(STATUS "    - example_liu_yao      : 六爻起卦示例")
message(STATUS "    - example_zi_wei       : 紫微斗数排盘示例")
message(STATUS "    - example_stacktrace   : std::stacktrace 功能测试")
message(STATUS "    - example_qi_men       : 奇门遁甲排盘示例")
message(STATUS "==========================================")