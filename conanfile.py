#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class pugixmlConan(ConanFile):
    name = "pugixml"
    version = "1.8.1"
    description = "Light-weight, simple and fast XML parser for C++ with XPath support"
    url = "https://github.com/bincrafters/conan-pugixml"
    homepage = "https://github.com/zeux/pugixml"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "MIT"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False], "header_only": [True, False]}
    default_options = "shared=False", "fPIC=True", "header_only=False"
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def configure(self):
        if self.options.header_only:
            if self.settings.os != 'Windows':
                self.options.remove("fPIC")
            self.options.remove("shared")
            self.settings.clear()

    def source(self):
        source_url = self.homepage
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)

    def configure_cmake(self):
        cmake = CMake(self)
        # pugixml use lib64 on linux/x86_64
        cmake.definitions["CMAKE_INSTALL_LIBDIR"] = "lib"
        cmake.definitions["BUILD_TESTS"] = False
        if self.settings.os == 'Windows' and self.settings.compiler == 'Visual Studio':
            cmake.definitions['CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS'] = self.options.shared
        cmake.configure(build_folder=self.build_subfolder)
        return cmake

    def build(self):
        if not self.options.header_only:
            cmake = self.configure_cmake()
            cmake.build()

    def package(self):
        readme_contents = tools.load(os.path.join(self.source_subfolder, "README.md"))
        license_contents = readme_contents[readme_contents.find("This library is"):]
        tools.save("LICENSE", license_contents)
        self.copy(pattern="LICENSE", dst="licenses", src=self.build_folder)
        if self.options.header_only:
            source_dir = os.path.join(self.source_subfolder, "src")
            self.copy(pattern="*", dst="include", src=source_dir)
        else:
            cmake = self.configure_cmake()
            cmake.install()

    def package_info(self):
        if self.options.header_only:
            self.info.header_only()
            self.cpp_info.defines = ["PUGIXML_HEADER_ONLY"]
        else:
            self.cpp_info.libs = tools.collect_libs(self)
