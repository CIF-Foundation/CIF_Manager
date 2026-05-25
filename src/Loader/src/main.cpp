// cif_plugin_loader_cli: small host that loads a LabVIEW-built shared library, sets up the process so
// dependent libraries resolve next to the plugin, then calls a single exported entry point.
// Args: (1) path to the library (.dll / .so), (2) loader name passed through as a UTF-8 C string.
// Export name and optional "hold process" behavior come from CMake (plugin_loader_paths.h).

#include "plugin_loader_paths.h"

#include <cstdint>
#include <cstdio>
#include <string>
#include <string_view>
#include <vector>

#ifdef _WIN32

#include <windows.h>
#include <shellapi.h>

#else

#include <cerrno>
#include <cstdlib>
#include <cstring>
#include <filesystem>
#include <thread>
#include <unistd.h>

#include <dlfcn.h>

#endif

namespace {

#ifdef _WIN32
using PluginLoaderFn = void(__cdecl*)(uint32_t pid, char* loader_name);
#else
using PluginLoaderFn = void (*)(uint32_t pid, char* loader_name);
#endif

void PrintUsage() {
  std::fprintf(stderr, "Usage: cif_plugin_loader_cli <path-to-library> <loader-name>\n");
  std::fprintf(stderr, "  Loads the library and calls %s(PID, <loader-name>).\n", kPluginLoaderEntryPoint);
}

#ifdef _WIN32

// Normalizes a directory string for SetCurrentDirectory / display (trailing slashes optional on Windows).
std::wstring StripTrailingSeparators(std::wstring_view dir) {
  std::wstring out(dir);
  while (!out.empty() && (out.back() == L'/' || out.back() == L'\\')) {
    out.pop_back();
  }
  return out;
}

// Turns a possibly relative DLL path into a full path and the containing folder (for LoadLibrary + cwd).
bool ResolveDllPaths(const std::wstring& input_path, std::wstring* full_dll_path, std::wstring* dll_dir) {
  const DWORD needed = GetFullPathNameW(input_path.c_str(), 0, nullptr, nullptr);
  if (needed == 0) {
    return false;
  }
  std::vector<wchar_t> buf(static_cast<size_t>(needed));
  wchar_t* file_part = nullptr;
  const DWORD n = GetFullPathNameW(input_path.c_str(), needed, buf.data(), &file_part);
  if (n == 0 || n >= needed) {
    return false;
  }
  *full_dll_path = std::wstring(buf.data(), n);
  if (file_part && file_part > buf.data()) {
    *dll_dir = StripTrailingSeparators(std::wstring(buf.data(), static_cast<size_t>(file_part - buf.data())));
  } else {
    *dll_dir = L".";
  }
  return true;
}

// Loader name arrives as UTF-16 from the command line; the DLL entry expects UTF-8.
std::string WideToUtf8(std::wstring_view w) {
  if (w.empty()) {
    return {};
  }
  int n = WideCharToMultiByte(CP_UTF8, 0, w.data(), static_cast<int>(w.size()), nullptr, 0, nullptr, nullptr);
  if (n <= 0) {
    return {};
  }
  std::string out(static_cast<size_t>(n), '\0');
  WideCharToMultiByte(CP_UTF8, 0, w.data(), static_cast<int>(w.size()), out.data(), n, nullptr, nullptr);
  return out;
}

#else

// Absolute path + plugin directory (parent of the .so). Uses the current working directory for relative paths.
bool ResolveDllPaths(const std::string& input_path, std::string* full_dll_path, std::string* dll_dir,
                     std::string* err_msg) {
  std::error_code ec;
  const std::filesystem::path abs = std::filesystem::absolute(input_path, ec);
  if (ec) {
    if (err_msg) {
      *err_msg = ec.message();
    }
    return false;
  }
  *full_dll_path = abs.string();
  const std::filesystem::path parent = abs.parent_path();
  *dll_dir = parent.empty() ? std::string(".") : parent.string();
  return true;
}

// Prepend the plugin directory so dlopen can resolve companion .so files next to the main library.
void PrependLdLibraryPath(const std::string& dir) {
  const char* const old = std::getenv("LD_LIBRARY_PATH");
  std::string combined = dir;
  if (old && old[0] != '\0') {
    combined.push_back(':');
    combined.append(old);
  }
  (void)setenv("LD_LIBRARY_PATH", combined.c_str(), 1);
}

// Copies the previous LD_LIBRARY_PATH before mutation; call restore() to put the environment back.
struct LdLibraryPathScope {
  bool had_original = false;
  std::string original;

  LdLibraryPathScope() {
    if (const char* const p = std::getenv("LD_LIBRARY_PATH")) {
      had_original = true;
      original.assign(p);
    }
  }

  void prepend_plugin_dir(const std::string& dir) { PrependLdLibraryPath(dir); }

  void restore() const {
    if (had_original) {
      (void)setenv("LD_LIBRARY_PATH", original.c_str(), 1);
    } else {
      (void)unsetenv("LD_LIBRARY_PATH");
    }
  }
};

#endif

}  // namespace

int main(int argc, char** argv) {
#ifdef _WIN32
  (void)argc;
  (void)argv;

  // Wide argv preserves non-ASCII paths and names without relying on the ACP.
  int wargc = 0;
  LPWSTR* wargv = CommandLineToArgvW(GetCommandLineW(), &wargc);
  if (!wargv) {
    return 1;
  }

  if (wargc < 3) {
    PrintUsage();
    LocalFree(wargv);
    return 1;
  }

  const std::wstring dll_path_arg = wargv[1];
  const std::wstring name_wide = wargv[2];
  LocalFree(wargv);

  std::wstring dll_path;
  std::wstring plugin_cwd;
  if (!ResolveDllPaths(dll_path_arg, &dll_path, &plugin_cwd)) {
    std::fprintf(stderr, "GetFullPathNameW(\"%ls\") failed: %lu\n", dll_path_arg.c_str(), GetLastError());
    return 1;
  }

  const std::string name_utf8 = WideToUtf8(name_wide);
  if (name_utf8.empty() && !name_wide.empty()) {
    std::fprintf(stderr, "Could not convert loader name to UTF-8.\n");
    return 1;
  }

  std::wstring prev_cwd(MAX_PATH + 1, L'\0');
  const DWORD prev_len = GetCurrentDirectoryW(static_cast<DWORD>(prev_cwd.size()), prev_cwd.data());
  if (prev_len == 0 || prev_len >= prev_cwd.size()) {
    std::fprintf(stderr, "GetCurrentDirectoryW failed: %lu\n", GetLastError());
    return 1;
  }
  prev_cwd.resize(prev_len);

  if (!SetDllDirectoryW(plugin_cwd.c_str())) {
    std::fprintf(stderr, "SetDllDirectoryW failed: %lu\n", GetLastError());
    return 1;
  }

  if (!SetCurrentDirectoryW(plugin_cwd.c_str())) {
    std::fprintf(stderr, "SetCurrentDirectoryW(\"%ls\") failed: %lu\n", plugin_cwd.c_str(), GetLastError());
    SetDllDirectoryW(nullptr);
    return 1;
  }

  const HMODULE mod = LoadLibraryW(dll_path.c_str());
  if (!mod) {
    std::fprintf(stderr, "LoadLibraryW(\"%ls\") failed: %lu\n", dll_path.c_str(), GetLastError());
    SetCurrentDirectoryW(prev_cwd.c_str());
    SetDllDirectoryW(nullptr);
    return 1;
  }

  auto* const entry = reinterpret_cast<PluginLoaderFn>(GetProcAddress(mod, kPluginLoaderEntryPoint));
  if (!entry) {
    std::fprintf(stderr, "GetProcAddress(\"%s\") failed: %lu\n", kPluginLoaderEntryPoint, GetLastError());
    FreeLibrary(mod);
    SetCurrentDirectoryW(prev_cwd.c_str());
    SetDllDirectoryW(nullptr);
    return 1;
  }

  std::vector<char> name_buf(name_utf8.begin(), name_utf8.end());
  name_buf.push_back('\0');

  const uint32_t pid = static_cast<uint32_t>(GetCurrentProcessId());

  entry(pid, name_buf.data());

#if PLUGIN_LOADER_HOLD_PROCESS
  std::fprintf(stderr,
               "Keeping process alive so the library stays loaded (background work).\n"
               "Exit this process when you want to unload (close window or End Task).\n");
  Sleep(INFINITE);
#else
  FreeLibrary(mod);
  SetCurrentDirectoryW(prev_cwd.c_str());
  SetDllDirectoryW(nullptr);
  return 0;
#endif

#else

  if (argc < 3) {
    PrintUsage();
    return 1;
  }

  const std::string dll_path_arg = argv[1];
  const std::string name_utf8 = argv[2];

  std::string dll_path;
  std::string plugin_cwd;
  std::string resolve_err;
  if (!ResolveDllPaths(dll_path_arg, &dll_path, &plugin_cwd, &resolve_err)) {
    std::fprintf(stderr, "Could not resolve path \"%s\": %s\n", dll_path_arg.c_str(), resolve_err.c_str());
    return 1;
  }

  constexpr std::size_t kPathMax = 4096;
  std::vector<char> prev_cwd(kPathMax);
  if (getcwd(prev_cwd.data(), prev_cwd.size()) == nullptr) {
    std::fprintf(stderr, "getcwd failed: %s\n", std::strerror(errno));
    return 1;
  }

  LdLibraryPathScope ld_scope;
  ld_scope.prepend_plugin_dir(plugin_cwd);

  if (chdir(plugin_cwd.c_str()) != 0) {
    std::fprintf(stderr, "chdir(\"%s\") failed: %s\n", plugin_cwd.c_str(), std::strerror(errno));
    ld_scope.restore();
    return 1;
  }

  (void)dlerror();
  void* const mod = dlopen(dll_path.c_str(), RTLD_NOW | RTLD_LOCAL);
  if (!mod) {
    const char* err = dlerror();
    std::fprintf(stderr, "dlopen(\"%s\") failed: %s\n", dll_path.c_str(), err ? err : "unknown error");
    chdir(prev_cwd.data());
    ld_scope.restore();
    return 1;
  }

  (void)dlerror();
  void* const sym = dlsym(mod, kPluginLoaderEntryPoint);
  const char* const dlsym_err = dlerror();
  if (dlsym_err != nullptr) {
    std::fprintf(stderr, "dlsym(\"%s\") failed: %s\n", kPluginLoaderEntryPoint, dlsym_err);
    dlclose(mod);
    chdir(prev_cwd.data());
    ld_scope.restore();
    return 1;
  }
  if (sym == nullptr) {
    std::fprintf(stderr, "dlsym(\"%s\") returned nullptr.\n", kPluginLoaderEntryPoint);
    dlclose(mod);
    chdir(prev_cwd.data());
    ld_scope.restore();
    return 1;
  }

  auto* const entry = reinterpret_cast<PluginLoaderFn>(sym);

  std::vector<char> name_buf(name_utf8.begin(), name_utf8.end());
  name_buf.push_back('\0');

  const uint32_t pid = static_cast<uint32_t>(getpid());

  entry(pid, name_buf.data());

#if PLUGIN_LOADER_HOLD_PROCESS
  std::fprintf(stderr,
               "Keeping process alive so the library stays loaded (background work).\n"
               "Send SIGTERM to this PID (%u) to stop when finished.\n",
               static_cast<unsigned>(pid));
  for (;;) {
    std::this_thread::sleep_for(std::chrono::hours(24));
  }
#else
  dlclose(mod);
  chdir(prev_cwd.data());
  ld_scope.restore();
  return 0;
#endif

#endif
}
