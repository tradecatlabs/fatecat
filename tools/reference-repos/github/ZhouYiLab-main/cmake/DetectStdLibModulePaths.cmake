#[[
  Detect platform-specific C++ standard library module paths and
  apply required global compile/link options for the selected toolchain.

  Outputs:
    STDLIB_MODULE_DIRS
    STDLIB_INCLUDE_DIRS
]]
function(detect_stdlib_module_paths)
    if(UNIX)
        # Linux/Unix/macOS: Auto-detect libc++ standard library module paths
        if(APPLE)
            set(HOMEBREW_LLVM_PREFIX_ARM64 "/opt/homebrew/opt/llvm")
            set(HOMEBREW_LLVM_PREFIX_X64 "/usr/local/opt/llvm")
            if(CMAKE_HOST_SYSTEM_PROCESSOR STREQUAL "arm64")
                set(HOMEBREW_LLVM_PREFIX ${HOMEBREW_LLVM_PREFIX_ARM64})
            else()
                set(HOMEBREW_LLVM_PREFIX ${HOMEBREW_LLVM_PREFIX_X64})
            endif()
            message(STATUS "macOS detection: arch=${CMAKE_HOST_SYSTEM_PROCESSOR}, Homebrew LLVM path=${HOMEBREW_LLVM_PREFIX}")
        endif()

        find_path(STDLIB_MODULE_DIRS
            NAMES std.cppm
            PATHS
                /usr/lib/llvm-22/share/libc++/v1
                /usr/lib/llvm-21/share/libc++/v1
                /usr/lib/llvm-20/share/libc++/v1
                /usr/lib/llvm-19/share/libc++/v1
                /usr/local/lib/llvm-22/share/libc++/v1
                /usr/local/lib/llvm-21/share/libc++/v1
                /usr/local/lib/llvm-20/share/libc++/v1
                /usr/local/lib/llvm-19/share/libc++/v1
                /opt/llvm/share/libc++/v1
                /opt/homebrew/opt/llvm/share/libc++/v1
                /usr/local/opt/llvm/share/libc++/v1
            DOC "Path to standard library modules (libc++)"
        )

        find_path(STDLIB_INCLUDE_DIRS
            NAMES __config
            PATHS
                /usr/lib/llvm-22/include/c++/v1
                /usr/lib/llvm-21/include/c++/v1
                /usr/lib/llvm-20/include/c++/v1
                /usr/lib/llvm-19/include/c++/v1
                /usr/local/lib/llvm-22/include/c++/v1
                /usr/local/lib/llvm-21/include/c++/v1
                /usr/local/lib/llvm-20/include/c++/v1
                /usr/local/lib/llvm-19/include/c++/v1
                /opt/llvm/include/c++/v1
                /usr/include/c++/v1
                /opt/homebrew/opt/llvm/include/c++/v1
                /usr/local/opt/llvm/include/c++/v1
            DOC "Path to libc++ headers"
        )

        if(STDLIB_MODULE_DIRS AND STDLIB_INCLUDE_DIRS)
            message(STATUS "Auto-detected libc++ paths:")
            message(STATUS "  Module directory: ${STDLIB_MODULE_DIRS}")
            message(STATUS "  Header directory: ${STDLIB_INCLUDE_DIRS}")

            if(APPLE)
                execute_process(
                    COMMAND xcrun --show-sdk-path
                    OUTPUT_VARIABLE MACOS_SDK_PATH
                    OUTPUT_STRIP_TRAILING_WHITESPACE
                )
                message(STATUS "macOS SDK path: ${MACOS_SDK_PATH}")

                get_filename_component(LLVM_LIB_PATH "${STDLIB_MODULE_DIRS}/../../../lib/c++" ABSOLUTE)
                message(STATUS "LLVM libc++ library path: ${LLVM_LIB_PATH}")

                add_compile_options(
                    -nostdinc++
                    -isystem ${STDLIB_INCLUDE_DIRS}
                    -isysroot ${MACOS_SDK_PATH}
                )
                add_link_options(
                    -stdlib=libc++
                    -L${LLVM_LIB_PATH}
                    -Wl,-rpath,${LLVM_LIB_PATH}
                    -lc++
                    -lc++abi
                )
            else()
                add_compile_options(
                    -nostdinc++
                    -isystem ${STDLIB_INCLUDE_DIRS}
                )
                add_link_options(-stdlib=libc++ -lc++ -lc++abi)
            endif()
        else()
            message(WARNING "Unable to auto-detect libc++ paths. Please set manually:")
            message(WARNING "  cmake -DSTDLIB_MODULE_DIRS=<path> -DSTDLIB_INCLUDE_DIRS=<path> ..")
        endif()

    elseif(WIN32)
        if(DEFINED ENV{VCToolsInstallDir})
            set(STDLIB_MODULE_DIRS "$ENV{VCToolsInstallDir}/modules" CACHE PATH "Path to standard library modules")
            if(EXISTS "${STDLIB_MODULE_DIRS}/std.ixx")
                message(STATUS "Detected MSVC module directory from VCToolsInstallDir environment variable: ${STDLIB_MODULE_DIRS}")
            else()
                message(WARNING "Found VCToolsInstallDir but std.ixx does not exist at: ${STDLIB_MODULE_DIRS}")
                unset(STDLIB_MODULE_DIRS CACHE)
            endif()
        endif()

        if(NOT STDLIB_MODULE_DIRS)
            get_filename_component(COMPILER_DIR "${CMAKE_CXX_COMPILER}" DIRECTORY)
            get_filename_component(COMPILER_HOST_DIR "${COMPILER_DIR}" DIRECTORY)
            get_filename_component(COMPILER_BIN_DIR "${COMPILER_HOST_DIR}" DIRECTORY)
            get_filename_component(MSVC_VERSION_DIR "${COMPILER_BIN_DIR}" DIRECTORY)
            set(DETECTED_MODULE_PATH "${MSVC_VERSION_DIR}/modules")

            if(EXISTS "${DETECTED_MODULE_PATH}/std.ixx")
                set(STDLIB_MODULE_DIRS "${DETECTED_MODULE_PATH}" CACHE PATH "Path to standard library modules")
                message(STATUS "Auto-detected MSVC module directory from compiler path: ${STDLIB_MODULE_DIRS}")
            else()
                message(STATUS "Unable to detect from compiler path, searching common installation locations...")
                find_path(STDLIB_MODULE_DIRS
                    NAMES std.ixx
                    PATHS
                        "C:/Program Files/Microsoft Visual Studio/2022/Community/VC/Tools/MSVC"
                        "C:/Program Files/Microsoft Visual Studio/2022/Professional/VC/Tools/MSVC"
                        "C:/Program Files/Microsoft Visual Studio/2022/Enterprise/VC/Tools/MSVC"
                        "F:/program/visul_studio/idea/VC/Tools/MSVC"
                    PATH_SUFFIXES
                        "14.44.35207/modules"
                        "14.43.34601/modules"
                        "14.42.34433/modules"
                    DOC "Path to MSVC standard library modules"
                )

                if(STDLIB_MODULE_DIRS)
                    message(STATUS "Found MSVC module directory at common location: ${STDLIB_MODULE_DIRS}")
                else()
                    message(WARNING "Unable to auto-detect MSVC module path. Please set manually:")
                    message(WARNING "  cmake -DSTDLIB_MODULE_DIRS=<path> ..")
                endif()
            endif()
        endif()
    endif()

    set(STDLIB_MODULE_DIRS "${STDLIB_MODULE_DIRS}" PARENT_SCOPE)
    set(STDLIB_INCLUDE_DIRS "${STDLIB_INCLUDE_DIRS}" PARENT_SCOPE)
endfunction()

#[[
  Resolve and validate module build mode.

  Inputs:
    ZHOUYILAB_MODULE_MODE: AUTO | LOCAL | SHARED
    ZHOUYILAB_PREBUILT_MODULES_DIR: optional path for SHARED mode
    ZHOUYILAB_SHARED_REQUIRED_MODULE_SPECS:
      Semicolon-separated specs: name=glob1,glob2,...
      Example:
        std=std.*,std-*.pcm;std.compat=std.compat.*,std.compat-*.pcm;nlohmann.json=nlohmann.json.*,nlohmann_json.*,json.*

  Outputs:
    ZHOUYILAB_EFFECTIVE_MODULE_MODE: LOCAL | SHARED
]]
function(resolve_module_mode)
    if(NOT DEFINED ZHOUYILAB_MODULE_MODE)
        message(FATAL_ERROR "ZHOUYILAB_MODULE_MODE must be defined before resolve_module_mode()")
    endif()

    string(TOUPPER "${ZHOUYILAB_MODULE_MODE}" _mode)
    if(NOT _mode STREQUAL "AUTO" AND NOT _mode STREQUAL "LOCAL" AND NOT _mode STREQUAL "SHARED")
        message(FATAL_ERROR "Invalid ZHOUYILAB_MODULE_MODE='${ZHOUYILAB_MODULE_MODE}'. Expected: AUTO|LOCAL|SHARED")
    endif()

    if(_mode STREQUAL "AUTO")
        if(ZHOUYILAB_PREBUILT_MODULES_DIR AND EXISTS "${ZHOUYILAB_PREBUILT_MODULES_DIR}")
            set(_effective_mode "SHARED")
        else()
            set(_effective_mode "LOCAL")
        endif()
    else()
        set(_effective_mode "${_mode}")
    endif()

    if(_effective_mode STREQUAL "SHARED")
        if(NOT ZHOUYILAB_PREBUILT_MODULES_DIR)
            message(FATAL_ERROR "SHARED mode requires ZHOUYILAB_PREBUILT_MODULES_DIR")
        endif()
        if(NOT IS_DIRECTORY "${ZHOUYILAB_PREBUILT_MODULES_DIR}")
            message(FATAL_ERROR "ZHOUYILAB_PREBUILT_MODULES_DIR is not a directory: ${ZHOUYILAB_PREBUILT_MODULES_DIR}")
        endif()
        if(NOT ZHOUYILAB_SHARED_REQUIRED_MODULE_SPECS)
            message(FATAL_ERROR
                "SHARED mode requires ZHOUYILAB_SHARED_REQUIRED_MODULE_SPECS "
                "(format: name=glob1,glob2,...)")
        endif()

        foreach(_spec IN LISTS ZHOUYILAB_SHARED_REQUIRED_MODULE_SPECS)
            string(FIND "${_spec}" "=" _eq_pos)
            if(_eq_pos LESS 1)
                message(FATAL_ERROR
                    "Invalid module spec '${_spec}'. Expected format: name=glob1,glob2,...")
            endif()

            string(SUBSTRING "${_spec}" 0 ${_eq_pos} _module_name)
            math(EXPR _val_start "${_eq_pos} + 1")
            string(SUBSTRING "${_spec}" ${_val_start} -1 _glob_csv)
            string(REPLACE "," ";" _globs "${_glob_csv}")

            if(NOT _globs)
                message(FATAL_ERROR
                    "Invalid module spec '${_spec}'. At least one glob is required.")
            endif()

            set(_found FALSE)
            foreach(_g IN LISTS _globs)
                file(GLOB _hits "${ZHOUYILAB_PREBUILT_MODULES_DIR}/${_g}")
                if(_hits)
                    set(_found TRUE)
                    break()
                endif()
            endforeach()

            if(NOT _found)
                message(FATAL_ERROR
                    "SHARED mode validation failed: missing '${_module_name}' artifacts in "
                    "'${ZHOUYILAB_PREBUILT_MODULES_DIR}'. Expected one of patterns: ${_globs}")
            endif()
        endforeach()
    endif()

    set(ZHOUYILAB_EFFECTIVE_MODULE_MODE "${_effective_mode}" PARENT_SCOPE)
endfunction()

#[[
  Configure C++ module file sets for a target.

  Args:
    TARGET <target_name>
    MODULE_INTERFACE_FILES <list...>
    EXTRA_MODULE_FILES <list...>
    EFFECTIVE_MODE <LOCAL|SHARED>
    PREBUILT_MODULES_DIR <path>   # required when EFFECTIVE_MODE=SHARED
]]
function(configure_cxx_modules)
    set(options)
    set(oneValueArgs TARGET EFFECTIVE_MODE PREBUILT_MODULES_DIR)
    set(multiValueArgs MODULE_INTERFACE_FILES EXTRA_MODULE_FILES)
    cmake_parse_arguments(CFG "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

    if(NOT CFG_TARGET)
        message(FATAL_ERROR "configure_cxx_modules requires TARGET")
    endif()

    if(NOT CFG_EFFECTIVE_MODE)
        message(FATAL_ERROR "configure_cxx_modules requires EFFECTIVE_MODE")
    endif()

    if(CFG_EFFECTIVE_MODE STREQUAL "SHARED")
        if(NOT CFG_PREBUILT_MODULES_DIR)
            message(FATAL_ERROR "SHARED mode requires PREBUILT_MODULES_DIR")
        endif()
        message(STATUS "Using shared prebuilt modules from ${CFG_PREBUILT_MODULES_DIR}")
        if(STDLIB_INCLUDE_DIRS)
            target_include_directories(${CFG_TARGET} SYSTEM PUBLIC
                ${STDLIB_INCLUDE_DIRS}
            )
        endif()

        target_sources(${CFG_TARGET} PUBLIC
            FILE_SET cxx_modules TYPE CXX_MODULES
            BASE_DIRS ${CMAKE_CURRENT_SOURCE_DIR}
            FILES
                ${CFG_MODULE_INTERFACE_FILES}
                ${CFG_EXTRA_MODULE_FILES}
        )
        if(MSVC)
            target_compile_options(${CFG_TARGET} PUBLIC
                "/ifcSearchDir${CFG_PREBUILT_MODULES_DIR}"
            )
        elseif(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
            target_compile_options(${CFG_TARGET} PUBLIC
                "-fprebuilt-module-path=${CFG_PREBUILT_MODULES_DIR}"
            )
        else()
            message(FATAL_ERROR "SHARED module mode currently supports MSVC and Clang only")
        endif()

    elseif(CFG_EFFECTIVE_MODE STREQUAL "LOCAL" AND UNIX AND STDLIB_MODULE_DIRS AND STDLIB_INCLUDE_DIRS)
        target_include_directories(${CFG_TARGET} SYSTEM PUBLIC
            ${STDLIB_INCLUDE_DIRS}
        )
        target_sources(${CFG_TARGET} PUBLIC
            FILE_SET cxx_modules TYPE CXX_MODULES
            BASE_DIRS ${CMAKE_CURRENT_SOURCE_DIR} ${STDLIB_MODULE_DIRS}
            FILES
                ${CFG_MODULE_INTERFACE_FILES}
                ${CFG_EXTRA_MODULE_FILES}
                ${STDLIB_MODULE_DIRS}/std.cppm
                ${STDLIB_MODULE_DIRS}/std.compat.cppm
        )

    elseif(CFG_EFFECTIVE_MODE STREQUAL "LOCAL" AND WIN32 AND STDLIB_MODULE_DIRS)
        target_sources(${CFG_TARGET} PUBLIC
            FILE_SET cxx_modules TYPE CXX_MODULES
            BASE_DIRS ${CMAKE_CURRENT_SOURCE_DIR} ${STDLIB_MODULE_DIRS}
            FILES
                ${CFG_MODULE_INTERFACE_FILES}
                ${CFG_EXTRA_MODULE_FILES}
                ${STDLIB_MODULE_DIRS}/std.ixx
                ${STDLIB_MODULE_DIRS}/std.compat.ixx
        )

    elseif(CFG_EFFECTIVE_MODE STREQUAL "LOCAL")
        message(WARNING "Standard library module path not detected, using project modules only")
        target_sources(${CFG_TARGET} PUBLIC
            FILE_SET cxx_modules TYPE CXX_MODULES
            BASE_DIRS ${CMAKE_CURRENT_SOURCE_DIR}
            FILES
                ${CFG_MODULE_INTERFACE_FILES}
                ${CFG_EXTRA_MODULE_FILES}
        )
    else()
        message(FATAL_ERROR "Unknown EFFECTIVE_MODE='${CFG_EFFECTIVE_MODE}' in configure_cxx_modules")
    endif()
endfunction()
