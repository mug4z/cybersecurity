cmake_minimum_required(VERSION 3.22)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(pcapplusplus_include "$ENV{VCPKG_INC}/pcapplusplus")
project(test)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_EXTENSIONS ON)
add_compile_options(-Wall -Wextra -Werror)

find_package(PcapPlusPlus REQUIRED)
add_executable("${PROJECT_NAME}" writepcap.cpp)

# target_link_libraries(${PROJECT_NAME} PRIVATE PCAP::PCAP PcapPlusPlus::Pcap++ PcapPlusPlus::Common++ PcapPlusPlus::Packet++)
target_include_directories(${PROJECT_NAME} PRIVATE ${pcapplusplus_include})
target_link_libraries("${PROJECT_NAME}" PRIVATE 
    "$ENV{VCPKG_LIB}/libPcap++.a"
    "$ENV{VCPKG_LIB}/libPacket++.a"
    "$ENV{VCPKG_LIB}/libCommon++.a"
    "$ENV{VCPKG_LIB}/libpcap.a"   # Also link the system libpcap library that PcapPlusPlus sits on top of
 )
