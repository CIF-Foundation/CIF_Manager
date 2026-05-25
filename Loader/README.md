# Plugin loader CLI

Small console host that loads a LabVIEW-built shared library (`.dll` on Windows, `.so` on Linux), sets up dependency search paths, resolves the configured C export, and calls it with the current process ID and a caller-supplied loader name.

---

## What to place on the build machine

Copy the **entire project directory** (or at least these paths relative to the project root):

| Path | Purpose |
|------|---------|
| `CMakeLists.txt` | CMake project, options, `configure_file` |
| `cmake/plugin_loader_paths.h.in` | Template for generated `plugin_loader_paths.h` |
| `src/main.cpp` | Source for `cif_plugin_loader_cli` |

You do **not** need to copy the LabVIEW-built library onto the compiler host unless you want to run tests there; the build only compiles the loader. At **runtime**, you pass the path to the LabVIEW output library on the command line.

CMake writes **`plugin_loader_paths.h`** into the build directory during configuration. Do not hand-edit that file; it is regenerated every time you run CMake.

---

## What to change before building

The `-DNAME=value` fragments below are **CMake cache variables**, not Windows or Linux system environment variables. You append them to the **`cmake -S . -B build`** configure command; CMake stores them in **`build/CMakeCache.txt`** (until you reconfigure with different `-D` flags or edit the cache). They affect how the project is configured and built, not the whole machine.

1. **`PLUGIN_LOADER_ENTRY_POINT` (important)**  
   Must match the **exported C function name** in your LabVIEW shared library (default in repo: `PluginLoader_Loader`).  
   Set when you first configure CMake, for example (same idea on Windows and Linux—add to your `cmake -S . -B build ...` line):

   `-DPLUGIN_LOADER_ENTRY_POINT=YourExportName`

2. **`PLUGIN_LOADER_HOLD_PROCESS`**  
   Default is `ON`: after calling the export, the process stays alive and does not unload the library (typical for background servers). Use `-DPLUGIN_LOADER_HOLD_PROCESS=OFF` if you want a one-shot call and normal exit.

3. **`PLUGIN_LOADER_DLL_DIR` and `PLUGIN_LOADER_DLL_FILE`**  
   These only populate unused string constants in the generated header for this version of `main.cpp`. You can leave the defaults or align them with your layout for documentation; they do **not** affect the loader’s runtime path (the first command-line argument is the library path).

4. **Optional: edit defaults in `CMakeLists.txt`**  
   You may change the default `CACHE` values for `PLUGIN_LOADER_ENTRY_POINT` (and others) so repeated configures match your LabVIEW export without passing `-D` every time.

---

## Windows build

**Prerequisites:** CMake 3.20+, and a C++17 toolchain (for example Visual Studio 2022 with “Desktop development with C++”).

From the project root (example paths use `C:\Users\Public\Documents\CIF\manager`; adjust to your copy):

```powershell
cd D:\dev\temp\Launcher
cmake -S . -B build -G "Visual Studio 17 2022" -A x64
cmake --build build --config Release
```

With optional overrides on the **first** `cmake -S . -B build` line, for example:

```powershell
cmake -S . -B build -G "Visual Studio 17 2022" -A x64 `
  -DPLUGIN_LOADER_ENTRY_POINT=PluginLoader_Loader
```

**Where the executable is created**

- Visual Studio multi-config generator:  
  **`build\Release\cif_plugin_loader_cli.exe`** (or `build\Debug\cif_plugin_loader_cli.exe` if you build Debug).

Single-config generators (for example Ninja) put the binary under the build tree with a single configuration, for example:

```powershell
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build build
```

Typical output: **`build\cif_plugin_loader_cli.exe`**.

---

## Linux build

**Prerequisites:** CMake 3.20+, a C++17 compiler (GCC or Clang), and development headers for dynamic loading (on Debian/Ubuntu, `build-essential` and `cmake` are usually enough; `libdl` is part of `libc` and is linked via CMake’s `CMAKE_DL_LIBS`).

From the project root:

```bash
cd /path/to/Launcher
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
```

With an export name override on the first configure:

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release \
  -DPLUGIN_LOADER_ENTRY_POINT=PluginLoader_Loader
cmake --build build
```

**Where the executable is created**

- Default (Unix Makefiles or Ninja, single-config):  
  **`build/cif_plugin_loader_cli`**

Re-running **`cmake --build build`** after editing `src/main.cpp` or `CMakeLists.txt` is enough; run **`cmake -S . -B build ...`** again if you change cache variables or the template `cmake/plugin_loader_paths.h.in`.

---

## Run (both platforms)

```text
cif_plugin_loader_cli <path-to-library> <loader-name>
```

Example (Linux):

```bash
./build/cif_plugin_loader_cli /opt/mybuild/libPluginLoader.so "my-instance"
```

Example (Windows, Release):

```powershell
& "C:\Users\Public\Documents\CIF\manager\build\Release\cif_plugin_loader_cli.exe" "C:\Users\Public\Documents\CIF\manager\LV_PluginLoader.dll" "my-instance"
```

The loader name is passed to your export as a UTF-8 C string; on Windows, command-line parsing uses wide characters internally, then converts to UTF-8.
