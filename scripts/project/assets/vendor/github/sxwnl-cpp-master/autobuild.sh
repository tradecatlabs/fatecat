#!/bin/bash

build_dir=build

if [ ! -d "$build_dir" ]; then
    mkdir -p $build_dir
fi
cd build && cmake .. && make -j4
