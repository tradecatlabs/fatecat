cmake_minimum_required(VERSION 3.6.0)
project(sxwnl-cpp)
set(CMAKE_VERBOSE_MAKEFILE on)
# 编译参数

if (WIN32)
  set(CMAKE_CXX_STANDARD 11)
  add_compile_options("$<$<C_COMPILER_ID:MSVC>:/utf-8>")
  add_compile_options("$<$<CXX_COMPILER_ID:MSVC>:/utf-8>")
  add_compile_options(-DWIN32)
else()
#  set(CMAKE_BUILD_TYPE "Release")
  set(ENV{CXXFLAGS} "$ENV{CXXFLAGS} -std=c++11 -w -s -fexceptions")
  set(CMAKE_CXX_FLAGS $ENV{CXXFLAGS})
  message("CMAKE_CXX_FLAGS:" ${CMAKE_CXX_FLAGS})
endif()


include_directories(
	${PROJECT_SOURCE_DIR}/eph
	${PROJECT_SOURCE_DIR}/lunar
	${PROJECT_SOURCE_DIR}/mylib
)
file(GLOB SRCS
	"${PROJECT_SOURCE_DIR}/eph/*"
	"${PROJECT_SOURCE_DIR}/lunar/*"
	"${PROJECT_SOURCE_DIR}/mylib/*"
)

# 测试
# add_executable(test0 test/test.cpp ${SRCS})

add_executable(test1 test/test1.cpp ${SRCS})