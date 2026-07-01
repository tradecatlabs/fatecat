# 指定系统名称为 Linux (或者根据需要更改)
set(CMAKE_SYSTEM_NAME Linux)

# 如果你正在为不同于主机的操作系统构建，请设置CMAKE_SYSTEM_PROCESSOR
# set(CMAKE_SYSTEM_PROCESSOR arm) # 示例：如果目标是ARM架构

# 设置GCC编译器及其选项
#set(CMAKE_C_COMPILER "/usr/bin/gcc-14")
#set(CMAKE_CXX_COMPILER "/usr/bin/g++-14")

# 设置编译标志（可以根据需要调整）
set(CMAKE_C_FLAGS "-Wall -std=gnu99" CACHE STRING "C Compiler flags")
set(CMAKE_CXX_FLAGS "-Wall -std=c++20" CACHE STRING "C++ Compiler flags")

# 设置调试、最小化尺寸发布、发布、带调试信息的发布模式下的编译标志
set(CMAKE_C_FLAGS_DEBUG "-g" CACHE STRING "Debug C Compiler flags")
set(CMAKE_C_FLAGS_MINSIZEREL "-Os -DNDEBUG" CACHE STRING "MinSizeRel C Compiler flags")
set(CMAKE_C_FLAGS_RELEASE "-O3 -DNDEBUG" CACHE STRING "Release C Compiler flags")
set(CMAKE_C_FLAGS_RELWITHDEBINFO "-O2 -g" CACHE STRING "RelWithDebInfo C Compiler flags")

set(CMAKE_CXX_FLAGS_DEBUG "-g" CACHE STRING "Debug C++ Compiler flags")
set(CMAKE_CXX_FLAGS_MINSIZEREL "-Os -DNDEBUG" CACHE STRING "MinSizeRel C++ Compiler flags")
set(CMAKE_CXX_FLAGS_RELEASE "-O3 -DNDEBUG" CACHE STRING "Release C++ Compiler flags")
set(CMAKE_CXX_FLAGS_RELWITHDEBINFO "-O2 -g" CACHE STRING "RelWithDebInfo C++ Compiler flags")

# 设置链接器和其他工具链组件
set(CMAKE_AR      "/usr/bin/ar" CACHE FILEPATH "Archiver")
set(CMAKE_RANLIB  "/usr/bin/ranlib" CACHE FILEPATH "Ranlib")
set(CMAKE_NM      "/usr/bin/nm" CACHE FILEPATH "NM")
set(CMAKE_OBJDUMP "/usr/bin/objdump" CACHE FILEPATH "Objdump")
#set(CMAKE_LINKER  "/usr/bin/ld" CACHE FILEPATH "Linker")

#并行链接
set(CMAKE_CXX_LINKER "ld.gold")
set(CMAKE_C_LINKER "ld.gold")

# 设置查找库和包含文件的方式
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)

function(setting)
endfunction()