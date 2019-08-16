import os
from conans.client.generators.cmake import CMakeGenerator
from conans.client.build.cmake_flags import CMakeDefinitionsBuilder, get_generator
from conans import ConanFile
from conans.util.env_reader import get_env
from conans.model.conan_file import get_env_context_manager

conan_toolchain_content = """
if(NOT CONAN_EXPORTED)
{environment}
{definitions}
endif()
"""


def _cmake_escape_backslash(inp: str):
    """
    Escapes backslashes for cmake. Basically it replaces any \ with \\
    :param inp: Input string
    :return: Input string with backslashes escaped for cmake
    """
    return inp.replace("\\", "\\\\")


class CmakeToolchain(CMakeGenerator):
    """
    conan generator for cmake toolchains. Extends conans cmake generator and creates an additional file containing
    the toolchain and environment. That file must be included prior to the project macro in the CMake file.
    """

    def _get_cmake_environment_setters(self):
        """
        Detect all environment changes made by conan and convert them to cmake commands
        :return: string to print into a cmake file
        """
        old_env = dict(os.environ)
        with get_env_context_manager(self.conanfile):
            ret = []
            for name, value in self.conanfile.env.items():
                if isinstance(value, list):
                    value = str(get_env(name)).replace(old_env[name], "$ENV{{{name}}}".format(name=name))
                value = _cmake_escape_backslash(value)
                ret.append("set(ENV{{{name}}} \"{value}\")".format(name=name, value=value))
            return os.linesep.join(ret)

    def _get_cmake_definitions(self):
        """
        Detect all definitions conan sends to cmake by command line and convert them to cmake commands. Removes the
        CONAN_EXPORTED definition, so that users may check if conan has been invoked or not.
        :return: string to print into a cmake file
        """
        with get_env_context_manager(self.conanfile):
            ret = []
            build_type = self.conanfile.settings.get_safe("build_type")
            generator = get_generator(self.conanfile.settings)
            def_builder = CMakeDefinitionsBuilder(self.conanfile, generator=generator, forced_build_type=build_type)
            definitions = def_builder.get_definitions()
            del definitions["CONAN_EXPORTED"]
            for name, value in definitions.items():
                value = _cmake_escape_backslash(value)
                ret.append("set({name} {value})".format(name=name, value=value))
            return os.linesep.join(ret)

    @property
    def filename(self):
        pass

    @property
    def content(self):
        """ Content of the output file. """
        # environment and definitions will only be set if cmake has not been invoked by conan
        content = conan_toolchain_content.format(environment=self._get_cmake_environment_setters(),
                                                 definitions=self._get_cmake_definitions())
        return {super().filename: super().content,
                "conan_toolchain.cmake": content}


class CmakeToolchainGeneratorPackage(ConanFile):
    name = 'cmake_toolchain_generator'
    version = '0.2'
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
