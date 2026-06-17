cmake_minimum_required(VERSION 3.22)
project(test)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_EXTENSIONS ON)
set(BREW_PATH "/home/tfrily/.brew")
set(CMAKE_PREFIX_PATH ${BREW_PATH})

add_executable("${PROJECT_NAME}" writepcap.cpp)

target_link_libraries("${PROJECT_NAME}" PRIVATE 
    "${BREW_PATH}/lib/libPcap++.a"
    "${BREW_PATH}/lib/libPacket++.a"
    "${BREW_PATH}/lib/libCommon++.a"
    "${BREW_PATH}/lib/libpcap.a"   # Also link the system libpcap library that PcapPlusPlus sits on top of
)
