@echo off
rem Windows launcher for the cif_lvcore_ipk build.
rem
rem Requires WSL because the IPK is assembled with Linux tar and bash scripts.
rem Converts the repo path to a WSL path, then runs build_cif_lvcore_ipk.sh.
rem Output is written to Installers\output\cif-lvcore.<version>.ipk
setlocal

set "INSTALLERS_DIR=%~dp0"
set "REPO_DIR=%INSTALLERS_DIR%.."

where wsl >nul 2>&1
if errorlevel 1 (
  echo Error: WSL is required to build the cif_lvcore_ipk package.
  exit /b 1
)

rem Translate the Windows repo path to a path WSL can use, e.g. /mnt/d/dev/CIF_Manager
for /f "usebackq delims=" %%I in (`wsl wslpath -a "%REPO_DIR%"`) do set "WSL_REPO=%%I"

echo Building cif_lvcore_ipk via WSL...
wsl bash -lc "cd '%WSL_REPO%/Installers' && chmod +x build_cif_lvcore_ipk.sh build_ipk.sh apply_ipk_build_config.py normalize_ipk_line_endings.py && ./build_cif_lvcore_ipk.sh"
if errorlevel 1 (
  echo Error: IPK build failed.
  exit /b 1
)

echo IPK build completed. Output is in Installers\output\
endlocal
