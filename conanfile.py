import os
from conans.client.generators.cmake_paths import CMakePathsGenerator
from conans.client.build.cmake_flags import CMakeDefinitionsBuilder, get_generator
from conans import ConanFile
from conans.util.env_reader import get_env
from conans.model.conan_file import get_env_context_manager


def _cmake_escape_backslash(inp: str):
    return inp.replace("\\", "\\\\")


class CmakeToolchain(CMakePathsGenerator):

    def _get_cmake_environment_setters(self):
        old_env = dict(os.environ)
        with get_env_context_manager(self.conanfile):
            ret = []
            for name, value in self.conanfile.env.items():
                if isinstance(value, list):
                    value = str(get_env(name)).replace(old_env[name], "$ENV{{{name}}}".format(name=name))
                value = _cmake_escape_backslash(value)
                ret.append("set(ENV{{{name}}} \"{value}\")".format(name=name, value=value))
            return ret

    def _get_cmake_definitions(self):
        with get_env_context_manager(self.conanfile):
            ret = []
            build_type = self.conanfile.settings.get_safe("build_type")
            generator = get_generator(self.conanfile.settings)
            def_builder = CMakeDefinitionsBuilder(self.conanfile, generator=generator, forced_build_type=build_type)
            definitions = def_builder.get_definitions()
            del definitions["CONAN_EXPORTED"]
            for name, value in definitions.items():
                ret.append("set({name} {value})".format(name=name, value=value))
            return ret

    @property
    def filename(self):
        return "conan_toolchain.cmake"

    @property
    def content(self):
        lines=["if(NOT CONAN_EXPORTED)"]
        lines.extend(self._get_cmake_environment_setters())
        lines.extend(self._get_cmake_definitions())
        lines.append("endif()")
        return super().content + os.linesep.join(lines) + "\n"


class CmakeToolchainGeneratorPackage(ConanFile):
    name = 'cmake_toolchain_generator'
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
