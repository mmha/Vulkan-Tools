from conans import ConanFile, CMake, tools
import os

class VulkanToolsConan(ConanFile):
    name = "vulkan-tools"
    settings = "os", "arch"
    version = "1.1.97"
    requires = "vulkan-headers/[>=1.1.97]@mmha/testing", "vulkan-loader/[>=1.1.97]@mmha/testing"
    exports_sources = "*", "!.git"
    no_copy_source = True
    generators = "cmake"
    options = {
        "cube": [False, True],
        "vulkaninfo": [False, True]
    }
    default_options = {
        "cube": True,
        "vulkaninfo": True
    }

    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_CUBE"] = self.options.cube
        cmake.definitions["BUILD_VULKANINFO"] = self.options.vulkaninfo
        cmake.definitions["BUILD_ICD"] = False
        cmake.definitions["VULKAN_LOADER_INSTALL_DIR"] = self.deps_cpp_info["vulkan-loader"].rootpath
        cmake.definitions["VULKAN_HEADERS_INSTALL_DIR"] = self.deps_cpp_info["vulkan-headers"].rootpath
        cmake.configure()
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.env_info.path.append(os.path.join(self.package_folder, "bin"))
