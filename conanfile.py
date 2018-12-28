import os
import platform
# from conans.client.generators.cmake import DepsCppCmake
from conans.client.generators.cmake_paths import CMakePathsGenerator
# from conans.model import Generator
from conans import ConanFile


def _cmake_escape(inp: str):
    """

    :type inp: str
    """
    return inp.replace("\\", "\\\\")


class CmakeToolchain(CMakePathsGenerator):
    append_with_spaces = ["CPPFLAGS", "CFLAGS", "CXXFLAGS", "LIBS", "LDFLAGS", "CL"]

    def _get_cmake_environment_setters(self):
        ret = []
        for name, value in self.conanfile.env.items():
            if isinstance(value, list):
                if name in self.append_with_spaces:
                    # Variables joined with spaces look like: CPPFLAGS="one two three"
                    value = _cmake_escape(" ".join(value))
                    ret.append("set(ENV{{{name}}} \"{value} $ENV{{{name}}}\")".format(name=name, value=value))
                else:
                    if platform.system() == "Windows":
                        value = os.pathsep.join(value)
                    else:
                        value = os.pathsep.join(['"%s"' % val for val in value])
                    value = _cmake_escape(value)
                    ret.append("set(ENV{{{name}}} \"{value};$ENV{{{name}}}\")".format(name=name, value=value))
            else:
                value = _cmake_escape(value)
                ret.append("set(ENV{{{name}}} \"{value}\")".format(name=name, value=value))
        return ret

    def _get_cmake_toolchain_setter(self):
        ret = []
        if "CONAN_CMAKE_TOOLCHAIN_FILE" in self.conanfile.env:
            toolchain = _cmake_escape(self.conanfile.env["CONAN_CMAKE_TOOLCHAIN_FILE"])
            ret.append("set(CMAKE_TOOLCHAIN_FILE \"{toolchain}\")"
                       .format(toolchain=toolchain))
        return ret

    # noinspection PyPropertyDefinition
    @property
    def filename(self):
        pass

    @property
    def content(self):
        toolchain_setter = self._get_cmake_toolchain_setter()
        env_setters = self._get_cmake_environment_setters()

        return {super().filename: super().content,
                "conan_toolchain.cmake": os.linesep.join(env_setters + toolchain_setter)}


class CmakeToolchainGeneratorPackage(ConanFile):
    name = 'CmakeToolchainGenerator'
    version = '0.1'
    description = "A generator for conan that can be used to build conan packages " \
                  "by invoking cmake instead of conan build"
    url = 'https://github.com/pepe82sh/ConanCmakeToolchainGenerator'
    license = 'MIT'

    def build(self):
        pass

    def package_info(self):
        self.cpp_info.includedirs = []
        self.cpp_info.libdirs = []
        self.cpp_info.bindirs = []
