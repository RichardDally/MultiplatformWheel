# Multiplatform Wheel Example

This repository demonstrates how to build OS-specific Python Wheels (for Windows, Linux, and macOS) using `uv`, `hatchling`, and a custom build hook. 

This approach allows you to bundle platform-specific files (like compiled `.dll`, `.so`, or `.dylib` dynamic libraries) dynamically into the final `.whl` package depending on the OS the build is running on.

## Step-by-Step: How it Works

When you run a build command such as `uv build` (or `pip wheel .`), the following sequence of events takes place:

### 1. Build System Initialization (`pyproject.toml`)
The build frontend (`uv`) reads the `pyproject.toml` file and provisions an isolated build environment. It discovers that the project uses the `hatchling.build` backend:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

It also reads the `[tool.hatch.build.targets.wheel.hooks.custom]` section, which tells Hatchling: *"Before building the wheel, please run the custom Python hook located in `hatch_build.py`"*.

### 2. Executing the Build Hook (`hatch_build.py`)
Hatchling loads `hatch_build.py` and instantiates the custom class (which inherits from `BuildHookInterface`). It then calls the `initialize(self, version, build_data)` method.

Inside this method, three critical things happen:

* **OS Detection**: `platform.system()` detects the current operating system (e.g., Windows, Linux, Darwin).
* **Asset Mapping**: We use the `build_data["force_include"]` dictionary to map local files to paths *inside* the wheel. 
  ```python
  # This copies binaries/lib.dll into the wheel at multiplatform_wheel/lib_native.dll
  build_data["force_include"]["binaries/lib.dll"] = "multiplatform_wheel/lib_native.dll"
  ```
* **Platform Tagging**: To ensure that the final `.whl` file correctly identifies itself as a platform-specific binary (e.g., `win_amd64`, `manylinux`, `macosx` instead of `any`), we update the `build_data` metadata:
  ```python
  build_data["pure_python"] = False
  build_data["infer_tag"] = True
  ```

### 3. Wheel Assembly
Hatchling then proceeds to assemble the `.whl` ZIP archive. 
Because `infer_tag = True` was set, it inspects the current system environment (Python ABI, OS, Architecture) and renames the wheel appropriately (for instance: `dist/multiplatform_wheel-0.1.0-cp311-cp311-win_amd64.whl`). 

Finally, `uv` outputs the finalized wheel file to the `dist/` directory.

---

## References & Documentation

* **Hatchling Build Hook Plugins**: Learn more about the `BuildHookInterface` and the `build_data` dictionary.
  [https://hatch.pypa.io/latest/plugins/build-hook/](https://hatch.pypa.io/latest/plugins/build-hook/)
* **Hatchling Custom Hooks**: How to configure `pyproject.toml` to use a local `hatch_build.py`.
  [https://hatch.pypa.io/latest/config/build/#custom](https://hatch.pypa.io/latest/config/build/#custom)
