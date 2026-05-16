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



# class CustomBuildHook(BuildHookInterface):
#     def initialize(self, version, build_data):
#         # 1. Define the external source and where to save it locally
#         download_url = "https://example.com/assets/pretrained_model.bin"
#         local_dir = ".build_assets"
#         local_file = os.path.join(local_dir, "pretrained_model.bin")
        
#         # 2. Download the file using httpx
#         if not os.path.exists(local_file):
#             print(f"--- [BUILD] Downloading external asset from {download_url} ---")
#             os.makedirs(local_dir, exist_ok=True)
            
#             # Using a context manager ensures the connection is cleanly closed
#             with httpx.stream("GET", download_url, follow_redirects=True) as response:
#                 response.raise_for_status() # Ensure the download didn't fail (e.g. 404)
                
#                 with open(local_file, "wb") as f:
#                     for chunk in response.iter_bytes(chunk_size=8192):
#                         f.write(chunk)
#             print("--- [BUILD] Download complete! ---")
#         else:
#             print("--- [BUILD] Asset already exists locally, skipping download. ---")
#         # 3. Inject the downloaded file into the final wheel
#         # This copies .build_assets/pretrained_model.bin into my_fictional_package/model.bin
#         target_name = "my_fictional_package/model.bin"
        
#         build_data["force_include"][local_file] = target_name
        
#         # If your downloaded file makes the package platform-specific, you can set these:
#         # build_data["pure_python"] = False
#         # build_data["infer_tag"] = True