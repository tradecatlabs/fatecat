linux-clang

-DCMAKE_TOOLCHAIN_FILE=/mnt/f/runtime/vcpkg-ubuntu24/scripts/buildsystems/vcpkg.cmake
-DVCPKG_TARGET_TRIPLET=x64-linux-libcxx
-DVCPKG_CHAINLOAD_TOOLCHAIN_FILE=/mnt/h/study/cpp/folly_vcpkg/cmake/clang.toolchain.cmake


linux-gcc
-DCMAKE_TOOLCHAIN_FILE=/mnt/f/runtime/vcpkg-ubuntu24/scripts/buildsystems/vcpkg.cmake
-DVCPKG_TARGET_TRIPLET=x64-linux
-DVCPKG_CHAINLOAD_TOOLCHAIN_FILE=/mnt/h/study/cpp/folly_vcpkg/cmake/gcc.toolchain.cmake

windows

-DCMAKE_TOOLCHAIN_FILE=F:/runtime/vcpkg-ubuntu24/scripts/buildsystems/vcpkg.cmake
-DVCPKG_CHAINLOAD_TOOLCHAIN_FILE=H:/study/cpp/folly_vcpkg/cmake/clang.toolchain.cmake