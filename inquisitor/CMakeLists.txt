cmake_minimum_required(VERSION 3.22)
project(test)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_EXTENSIONS ON)
set(CMAKE_PREFIX_PATH "/home/tfrily/.brew")


find_package(PcapPlusPlus REQUIRED)

add_executable("${PROJECT_NAME}" main.cpp)
