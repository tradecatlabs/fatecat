cmake_minimum_required(VERSION 3.28)

project(ZhouYiLab 
    VERSION 1.0.0
    DESCRIPTION "周易实验室 - 传统文化算法库"
    LANGUAGES CXX
)

# ==============================================================================
# C++ 标准配置
# ==============================================================================
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_CXX_SCAN_FOR_MODULES ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Module build strategy:
#   AUTO   - use SHARED when prebuilt dir is provided and valid, otherwise LOCAL
#   LOCAL  - build std/json modules in this project
#   SHARED - consume prebuilt modules from ZHOUYILAB_PREBUILT_MODULES_DIR
set(ZHOUYILAB_MODULE_MODE "AUTO" CACHE STRING "AUTO|LOCAL|SHARED")
set_property(CACHE ZHOUYILAB_MODULE_MODE PROPERTY STRINGS AUTO LOCAL SHARED)
set(ZHOUYILAB_PREBUILT_MODULES_DIR "" CACHE PATH
    "Path to prebuilt module directory (std/nlohmann)")
set(ZHOUYILAB_SHARED_REQUIRED_MODULE_SPECS
    "std=std.*,std-*.pcm;std.compat=std.compat.*,std.compat-*.pcm;nlohmann.json=nlohmann.json.*,nlohmann_json.*,json.*"
    CACHE STRING "SHARED mode required modules: name=glob1,glob2;name2=glob1,glob2")

# ==============================================================================
# 平台特定编译标志（MSVC）
# ==============================================================================
if(MSVC)
    # 添加 /utf-8 标志确保所有源文件和模块使用相同的编码设置
    # 这对于 C++ 模块的 BMI 兼容性至关重要
    add_compile_options(/utf-8)
    message(STATUS "MSVC: 启用 UTF-8 编码支持 (/utf-8)")
endif()

# ==============================================================================
# 自动检测平台特定的标准库模块路径
# ==============================================================================
#[[
  Load helper functions from 3rdparty/cmake:
    1) detect_stdlib_module_paths
    2) configure_cxx_modules
]]
include(${CMAKE_CURRENT_SOURCE_DIR}/cmake/DetectStdLibModulePaths.cmake)
detect_stdlib_module_paths()
resolve_module_mode()


# ==============================================================================
# 第三方库配置
# ==============================================================================

# 临时禁用模块扫描，避免 CMake 尝试扫描第三方库的编译器特性测试
set(CMAKE_CXX_SCAN_FOR_MODULES_BACKUP ${CMAKE_CXX_SCAN_FOR_MODULES})
set(CMAKE_CXX_SCAN_FOR_MODULES OFF)

# 配置第三方库的 C++ modules 支持
# 启用 fmt 的 module 模式（稳定支持）
set(FMT_MODULE ON CACHE BOOL "Build fmt as a C++ module" FORCE)
if(ZHOUYILAB_EFFECTIVE_MODULE_MODE STREQUAL "SHARED")
    # Shared mode: skip building nlohmann_json module (reuse external pcm).
    set(NLOHMANN_JSON_BUILD_MODULES OFF CACHE BOOL "" FORCE)
else()
    # 启用 nlohmann_json 的 module 支持
    set(NLOHMANN_JSON_BUILD_MODULES ON CACHE BOOL "Build nlohmann_json C++ module" FORCE)
endif()

# 修复msvc的警告
if(MSVC)
    # 启用异常处理机制
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /EHsc")
endif()

if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    # 禁用保留模块标识符警告（libc++ 标准库需要）fix warning: 'std' is a reserved name for a module [-Wreserved-module-identifier]
    add_compile_options(-Wno-reserved-module-identifier)

    # 禁用模块包含警告（第三方库 ASIO 引起）
    # fix warning: '#include <***>' attaches the declarations to the named module 'asio', which is not usually intended;
    # consider moving that directive before the module declaration [-Winclude-angled-in-module-purview]
    add_compile_options(-Wno-include-angled-in-module-purview)
endif()

# 添加第三方库
add_subdirectory(3rdparty/fmt)
if(ZHOUYILAB_EFFECTIVE_MODULE_MODE STREQUAL "SHARED")
    # Shared mode: nlohmann_json module comes from -fprebuilt-module-path.
    # Still add_subdirectory for headers, but create stub for module target.
    add_subdirectory(3rdparty/nlohmann_json)
    file(WRITE "${CMAKE_CURRENT_BINARY_DIR}/_stub.cpp" "")
    add_library(nlohmann_json_modules STATIC "${CMAKE_CURRENT_BINARY_DIR}/_stub.cpp")
    target_link_libraries(nlohmann_json_modules PUBLIC nlohmann_json::nlohmann_json)
else()
    add_subdirectory(3rdparty/nlohmann_json)
endif()
add_subdirectory(3rdparty/asio)

# 恢复模块扫描
set(CMAKE_CXX_SCAN_FOR_MODULES ${CMAKE_CXX_SCAN_FOR_MODULES_BACKUP})

# 包含头文件目录
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/3rdparty/nlohmann_json/include)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/3rdparty/magic_enum/include)


# ==============================================================================
# 源文件收集
# ==============================================================================
#
# 源码目录结构：
#   src/               - 主程序入口（main.cpp）和测试文件
#   src/common/        - 通用基础模块（天干、地支、干支、中文映射等）
#   src/liu_yao/       - 六爻相关模块
#   src/da_liu_ren/    - 大六壬相关模块
#   src/ba_zi/         - 八字相关模块
#   src/zi_wei/        - 紫微斗数相关模块
#   src/common/tyme/   - 农历时间库模块
#

# 收集所有 C++ 源文件
file(GLOB_RECURSE CPP_SOURCES "src/*.cpp")

# 收集模块接口文件
file(GLOB_RECURSE MODULE_INTERFACE_FILES 
    "src/*.cppm"    # C++23 module 接口文件
    "src/*.ixx"     # MSVC module 接口文件
)

# 排除测试文件（它有自己的 main 函数）
list(REMOVE_ITEM CPP_SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/src/test_tyme_module.cpp")

# 排除主程序入口文件
list(REMOVE_ITEM CPP_SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/src/main.cpp")

# ==============================================================================
# 核心库目标
# ==============================================================================

# 创建静态库，包含所有核心模块和实现（除了 main.cpp）
add_library(ZhouYiLabCore STATIC 
    ${CPP_SOURCES} 
    ${MODULE_INTERFACE_FILES}
)

# 定义 MAGIC_ENUM_USE_STD_MODULE 以使用 import std
target_compile_definitions(ZhouYiLabCore PUBLIC
    MAGIC_ENUM_USE_STD_MODULE
)

#[[
  Configure C++ modules for ZhouYiLabCore:
    - project modules
    - magic_enum module
    - std modules (when detected)
    - shared prebuilt mode (when ZHOUYILAB_EFFECTIVE_MODULE_MODE=SHARED)
]]
configure_cxx_modules(
    TARGET ZhouYiLabCore
    MODULE_INTERFACE_FILES ${MODULE_INTERFACE_FILES}
    EXTRA_MODULE_FILES ${CMAKE_CURRENT_SOURCE_DIR}/3rdparty/magic_enum/module/magic_enum.cppm
    EFFECTIVE_MODE ${ZHOUYILAB_EFFECTIVE_MODULE_MODE}
    PREBUILT_MODULES_DIR ${ZHOUYILAB_PREBUILT_MODULES_DIR}
)

# 链接第三方库到核心库
target_link_libraries(ZhouYiLabCore PUBLIC
    fmt::fmt
    nlohmann_json_modules
    asio::asio
)

# Windows 平台需要链接网络库
if(WIN32)
    target_link_libraries(ZhouYiLabCore PUBLIC ws2_32 mswsock)
endif()

# 模块生成模式（CMake 4.0+ 特性）
# SEPARATE: 模块接口单元的编译与其他翻译单元分离
set_property(TARGET ZhouYiLabCore PROPERTY
    CXX_MODULE_GENERATION_MODE "SEPARATE"
)

# ==============================================================================
# 主可执行文件目标
# ==============================================================================

# 创建可执行文件，只包含 main.cpp
add_executable(ZhouYiLab src/main.cpp)

# 链接核心库
target_link_libraries(ZhouYiLab PRIVATE ZhouYiLabCore)

# 设置模块生成模式
set_property(TARGET ZhouYiLab PROPERTY
    CXX_MODULE_GENERATION_MODE "SEPARATE"
)

# ==============================================================================
# 构建信息汇总
# ==============================================================================

message(STATUS "==========================================")
message(STATUS "项目: ${PROJECT_NAME} v${PROJECT_VERSION}")
message(STATUS "C++ 标准: C++${CMAKE_CXX_STANDARD}")
message(STATUS "编译器: ${CMAKE_CXX_COMPILER_ID} ${CMAKE_CXX_COMPILER_VERSION}")
message(STATUS "构建类型: ${CMAKE_BUILD_TYPE}")
message(STATUS "模块模式: ${ZHOUYILAB_EFFECTIVE_MODULE_MODE} (configured: ${ZHOUYILAB_MODULE_MODE})")
if(ZHOUYILAB_EFFECTIVE_MODULE_MODE STREQUAL "SHARED")
    message(STATUS "预编译模块目录: ${ZHOUYILAB_PREBUILT_MODULES_DIR}")
endif()
if(UNIX)
    if(STDLIB_MODULE_DIRS)
        message(STATUS "libc++ 模块: ${STDLIB_MODULE_DIRS}")
    endif()
elseif(WIN32)
    if(STDLIB_MODULE_DIRS)
        message(STATUS "MSVC 模块: ${STDLIB_MODULE_DIRS}")
    endif()
endif()
message(STATUS "==========================================")

# ==============================================================================
# 测试配置 (已禁用)
# ==============================================================================
# 测试功能已被移除以避免 CI 环境中的模块系统冲突
# Tests have been removed to avoid module system conflicts in CI environment

# ==============================================================================
# 示例程序配置
# ==============================================================================

if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/examples/CMakeLists.txt")
    add_subdirectory(examples)
    message(STATUS "示例程序已启用 (位于 examples/ 目录)")
endif()
