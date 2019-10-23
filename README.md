[![Build Status](https://travis-ci.com/pepe82sh/ConanCmakeToolchainGenerator.svg?branch=master)](https://travis-ci.com/pepe82sh/ConanCmakeToolchainGenerator)


# ConanCmakeToolchainGenerator

This conan generator creates the files `conan_toolchain.cmake`
and `conanbuildinfo.cmake` inside your build folder. These files 
can than be imported in your `CMakeLists.txt`. `conan_toolchain.cmake`
has to be included prior to the `project` macro, while `conanbuildinfo.cmake`
has to be included after the `project` macro.
This way you'll be able to access all environment
variables and cmake definitions that will be set when the project
is build inside conan.

## Usage
In a fully automated example, you'd want to call conan install
from within your cmake file, if conan itself has not invoked
cmake.

```
cmake_minimum_required(VERSION 3.13)
if( NOT CONAN_EXPORTED )
	execute_process(
		COMMAND conan install "${CMAKE_CURRENT_LIST_DIR}"
		RESULT_VARIABLE CONAN_INSTALL_FAILED
	)
	if(CONAN_INSTALL_FAILED)
		message(FATAL_ERROR "conan install failed")
	endif()
endif()
include( ${CMAKE_BINARY_DIR}/conan_toolchain.cmake )

project(test)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)

add_library(test test.cpp)
```
