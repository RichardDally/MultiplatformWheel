import platform
from pathlib import Path

# Get the directory where this current Python file is located
PACKAGE_DIR = Path(__file__).parent

def get_lib_path():
    current_os = platform.system().lower()
    
    if current_os == "windows":
        return PACKAGE_DIR / "lib_native.dll"
    if current_os == "linux":
        return PACKAGE_DIR / "lib_native.so"
    if current_os == "darwin":
        return PACKAGE_DIR / "lib_native.dylib"
    raise OSError("Unsupported operating system")

# Example usage (e.g., with ctypes)
# import ctypes
# lib = ctypes.CDLL(str(get_lib_path()))