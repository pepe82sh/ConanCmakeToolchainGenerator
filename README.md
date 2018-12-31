# ConanCmakeToolchainGenerator

This conan generator creates the file `conan_toolchain.cmake`
inside your build folder. This file can than be imported in your
`CMakeLists.txt`. This way you'll be able to access all environment
variables and cmake definitions that will be set when the project
is build inside conan. `CMAKE_MODULE_PATH` and `CMAKE_PREFIX_PATH`
are also set like in the `cmake_paths` generator.

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

add_library(test test.cpp)
```