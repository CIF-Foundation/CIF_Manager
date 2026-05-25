cmake_minimum_required(VERSION 3.20)
project(PluginLoaderCli LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(PLUGIN_LOADER_DLL_DIR
    "D:/dev/builds/Temp/pluginloader"
    CACHE PATH "Folder containing PluginLoader.dll and its LabVIEW RTE dependencies")

set(PLUGIN_LOADER_DLL_FILE
    "PluginLoader.dll"
    CACHE STRING "LabVIEW shared library file name")

set(PLUGIN_LOADER_ENTRY_POINT
    "PluginLoader_Loader"
    CACHE STRING "Exported C function name from the LabVIEW DLL")

# gRPC (and similar) servers often return from the exported VI while worker threads keep running.
# If the host process exits or FreeLibrary runs, the DLL unloads and the server stops / misbehaves.
option(PLUGIN_LOADER_HOLD_PROCESS
       "After calling the DLL entry, keep the process alive and do not FreeLibrary (use for background servers)"
       ON)

file(TO_CMAKE_PATH "${PLUGIN_LOADER_DLL_DIR}" _dir_cmake)
string(REPLACE "\\" "/" _dir_esc "${_dir_cmake}")
if(NOT _dir_esc MATCHES "/$")
  string(APPEND _dir_esc "/")
endif()
set(PLUGIN_LOADER_DLL_DIR_ESC "${_dir_esc}")

file(TO_CMAKE_PATH "${PLUGIN_LOADER_DLL_FILE}" _dll_cmake)
cmake_path(GET _dll_cmake FILENAME PLUGIN_LOADER_DLL_FILE_ESC)

configure_file(
  "${CMAKE_CURRENT_SOURCE_DIR}/cmake/plugin_loader_paths.h.in"
  "${CMAKE_CURRENT_BINARY_DIR}/plugin_loader_paths.h"
  @ONLY)

add_executable(cif_plugin_loader_cli src/main.cpp)
target_include_directories(cif_plugin_loader_cli PRIVATE "${CMAKE_CURRENT_BINARY_DIR}")
if(WIN32)
  target_link_libraries(cif_plugin_loader_cli PRIVATE shell32)
else()
  target_link_libraries(cif_plugin_loader_cli PRIVATE ${CMAKE_DL_LIBS})
endif()

if(PLUGIN_LOADER_HOLD_PROCESS)
  target_compile_definitions(cif_plugin_loader_cli PRIVATE PLUGIN_LOADER_HOLD_PROCESS=1)
else()
  target_compile_definitions(cif_plugin_loader_cli PRIVATE PLUGIN_LOADER_HOLD_PROCESS=0)
endif()

if(MSVC)
  target_compile_options(cif_plugin_loader_cli PRIVATE /W4 /permissive-)
endif()
