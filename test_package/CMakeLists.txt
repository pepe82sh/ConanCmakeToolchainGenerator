cmake_minimum_required(VERSION 3.12)
project(PackageTest CXX)

add_executable(example example.cpp)
#target_link_libraries(example ${CONAN_LIBS})

# CTest is a testing tool that can be used to test your project.
# enable_testing()
# add_test(NAME example
#          WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
#          COMMAND example)
