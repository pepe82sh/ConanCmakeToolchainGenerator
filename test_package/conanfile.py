import os

from conans import ConanFile, CMake, tools
from conans.util.env_reader import get_env


class HelloTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "CmakeToolchain"

    def build(self):
        # run externally
        self.run("cmake ../..")
        self.run("cmake --build .")

        # run in conan
        cmake = CMake(self)
        # Current dir is "test_package/build/<build_id>" and CMakeLists.txt is
        # in "test_package"
        cmake.configure()
        cmake.build()

    def imports(self):
        pass
        #self.copy("*.dll", dst="bin", src="bin")
        #self.copy("*.dylib*", dst="bin", src="lib")
        #self.copy('*.so*', dst='bin', src='lib')

    def test(self):
        pass
        #if not tools.cross_building(self.settings):
        #    os.chdir("bin")
        #    self.run(".%sexample" % os.sep)
