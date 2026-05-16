import platform
from hatchling.builders.hooks.plugin.interface import BuildHookInterface

class CustomBuildHook(BuildHookInterface):
    def initialize(self, version, build_data):
        # 1. Detect the current OS
        current_os = platform.system().lower()
        
        # 2. Map the OS to the correct binary file
        if current_os == "windows":
            source_file = "binaries/lib.dll"
            target_name = "lib_native.dll"
        elif current_os == "linux":
            source_file = "binaries/lib.so"
            target_name = "lib_native.so"
        elif current_os == "darwin":  # macOS
            source_file = "binaries/lib.dylib"
            target_name = "lib_native.dylib"
        else:
            raise RuntimeError(f"Unsupported OS: {current_os}")

        # 3. Dynamically inject the file into the wheel
        # 'force_include' mapping format: { "source/path": "path/inside/the/wheel" }
        build_data["force_include"][source_file] = f"multiplatform_wheel/{target_name}"
        build_data["pure_python"] = False
        build_data["infer_tag"] = True
        
        print(f"--- [BUILD] Including {source_file} as {target_name} ---")