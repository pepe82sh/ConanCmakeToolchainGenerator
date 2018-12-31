cmake_minimum_required(VERSION 3.12)
include(${CMAKE_BINARY_DIR}/conan_toolchain.cmake)
project(PackageTest CXX)

# Check cmake values
if(NOT CONAN_COMPILER)
    message(FATAL_ERROR "CONAN_COMPILER was expected but not set.")
endif()


add_library(example example.cpp)
#target_link_libraries(example ${CONAN_LIBS})

# CTest is a testing tool that can be used to test your project.
# enable_testing()
# add_test(NAME example
#          WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
#          COMMAND example)
