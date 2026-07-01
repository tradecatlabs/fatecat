# 指定系统名称为 Windows
set(CMAKE_SYSTEM_NAME Windows)

# 如果你需要针对不同的架构，请调整如下行
# 例如，对于 x64 架构：
set(CMAKE_GENERATOR_PLATFORM "x64" CACHE STRING "Visual Studio generator platform")

# 设置 Visual Studio 的版本号 (可选)
# 如果不指定，则使用最新安装的版本
# set(CMAKE_GENERATOR "Visual Studio 17 2022")

# 如果需要指定特定的工具集（如 v142 对应 VS2019），可以添加以下行
# set(CMAKE_VS_WINDOWS_TARGET_PLATFORM_VERSION "10.0" CACHE STRING "Windows SDK version")
# set(CMAKE_GENERATOR_TOOLSET "v142" CACHE STRING "Visual Studio toolset")

# 设置编译器和链接器标志
# 注意：对于多配置生成器（如 Visual Studio），使用 *_FLAGS_INIT 可以避免覆盖用户提供的标志
set(CMAKE_C_FLAGS_INIT "/W4 /MP" CACHE STRING "C Compiler flags")
set(CMAKE_CXX_FLAGS_INIT "/W4 /MP /EHsc" CACHE STRING "C++ Compiler flags")

# 设置调试、最小化尺寸发布、发布、带调试信息的发布模式下的编译标志
set(CMAKE_C_FLAGS_DEBUG_INIT "/MDd /Zi /Ob0 /Od /RTC1" CACHE STRING "Debug C Compiler flags")
set(CMAKE_C_FLAGS_MINSIZEREL_INIT "/MD /O1 /Ob1 /D NDEBUG" CACHE STRING "MinSizeRel C Compiler flags")
set(CMAKE_C_FLAGS_RELEASE_INIT "/MD /O2 /Ob2 /D NDEBUG" CACHE STRING "Release C Compiler flags")
set(CMAKE_C_FLAGS_RELWITHDEBINFO_INIT "/MD /Zi /O2 /Ob1" CACHE STRING "RelWithDebInfo C Compiler flags")

set(CMAKE_CXX_FLAGS_DEBUG_INIT "/MDd /Zi /Ob0 /Od /RTC1" CACHE STRING "Debug C++ Compiler flags")
set(CMAKE_CXX_FLAGS_MINSIZEREL_INIT "/MD /O1 /Ob1 /D NDEBUG" CACHE STRING "MinSizeRel C++ Compiler flags")
set(CMAKE_CXX_FLAGS_RELEASE_INIT "/MD /O2 /Ob2 /D NDEBUG" CACHE STRING "Release C++ Compiler flags")
set(CMAKE_CXX_FLAGS_RELWITHDEBINFO_INIT "/MD /Zi /O2 /Ob1" CACHE STRING "RelWithDebInfo C++ Compiler flags")

# 设置链接器标志
set(CMAKE_EXE_LINKER_FLAGS_INIT "/INCREMENTAL:NO" CACHE STRING "Executable linker flags")
set(CMAKE_SHARED_LINKER_FLAGS_INIT "/INCREMENTAL:NO" CACHE STRING "Shared library linker flags")
set(CMAKE_MODULE_LINKER_FLAGS_INIT "/INCREMENTAL:NO" CACHE STRING "Module linker flags")

# 设置查找库和包含文件的方式
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)

# 设置环境变量或路径（如果需要）
# set(ENV{VCTargetsPath} "C:/Program Files (x86)/Microsoft Visual Studio/2019/Community/Common7/IDE/VC/VCTargets")

# 如果有特定的库路径或包含路径，可以在这里添加
# set(CMAKE_LIBRARY_PATH "C:/path/to/lib")
# set(CMAKE_INCLUDE_PATH "C:/path/to/include")

# 如果你有一个预定义的sysroot，可以设置CMAKE_SYSROOT
# set(CMAKE_SYSROOT "C:/path/to/sysroot")

# 额外的 MSVC 特定设置
function(setting)
    # 文件过大编译参数
    add_compile_options(/bigobj)
    add_compile_options(/await:strict)
    # win32的宏必须设置定义
    add_compile_definitions(_WIN32_WINNT=0x0601)
    # 禁用某些警告（根据项目需求调整）
    add_compile_options(/wd4251)  # 示例：禁用4251警告
    # 设置运行时库（这里设置了多线程DLL版本）
    #[[foreach(flag_var
            CMAKE_CXX_FLAGS CMAKE_CXX_FLAGS_DEBUG CMAKE_CXX_FLAGS_RELEASE
            CMAKE_CXX_FLAGS_MINSIZEREL CMAKE_CXX_FLAGS_RELWITHDEBINFO
            CMAKE_C_FLAGS CMAKE_C_FLAGS_DEBUG CMAKE_C_FLAGS_RELEASE
            CMAKE_C_FLAGS_MINSIZEREL CMAKE_C_FLAGS_RELWITHDEBINFO)
        if(${flag_var} MATCHES "/MD")
            string(REGEX REPLACE "/MD" "/MT" ${flag_var} "${${flag_var}}")
        endif()
    endforeach()]]

    # 设置PDB输出目录（可选）
    set(CMAKE_PDB_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/pdb")
endfunction()