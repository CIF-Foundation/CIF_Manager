@echo off
setlocal

set "NSIS=%ProgramFiles(x86)%\NSIS\makensis.exe"
if not exist "%NSIS%" (
  echo Error: NSIS not found at "%NSIS%"
  exit /b 1
)

pushd "%~dp0"

set "NSI_FILE=cif-lvcore.nsi"
set "PRODUCT_VERSION="
for /f "tokens=3 delims= " %%V in ('findstr /C:"define PRODUCT_VERSION" "%NSI_FILE%"') do set "PRODUCT_VERSION=%%~V"
if not defined PRODUCT_VERSION (
  echo Error: Could not read PRODUCT_VERSION from %NSI_FILE%
  popd
  exit /b 1
)
set "OUT_FILE=cif-lvcore-%PRODUCT_VERSION%.exe"

set "STAGING=%~dp0staging"
set "STAGING_RESOURCE=%STAGING%\resource"
set "RESOURCE=%~dp0resource"
set "REPO_ROOT=%~dp0..\.."
set "BUILD_CONFIG=%~dp0..\cif_lvcore_windows.build.json"
set "APPLY_CONFIG=%~dp0..\apply_ipk_build_config.py"

if not exist "%BUILD_CONFIG%" (
  echo Error: Build config not found at "%BUILD_CONFIG%"
  popd
  exit /b 1
)

if not exist "%APPLY_CONFIG%" (
  echo Error: apply_ipk_build_config.py not found at "%APPLY_CONFIG%"
  popd
  exit /b 1
)

if exist "%STAGING%" rmdir /s /q "%STAGING%"

echo Staging installer resources...
xcopy "%RESOURCE%\*" "%STAGING_RESOURCE%\" /E /I /Q /Y >nul
if errorlevel 1 (
  echo Error: Failed to stage installer resources.
  popd
  exit /b 1
)

echo Applying source file copies from cif_lvcore_windows.build.json...
python "%APPLY_CONFIG%" "%BUILD_CONFIG%" "%REPO_ROOT%" "%STAGING_RESOURCE%"
if errorlevel 1 (
  echo Error: Failed to apply Windows build config.
  popd
  exit /b 1
)

"%NSIS%" /DRESOURCE_DIR="%STAGING_RESOURCE%" "%NSI_FILE%"
if errorlevel 1 (
  popd
  exit /b 1
)

if not exist "%OUT_FILE%" (
  echo Error: Expected installer not found: %OUT_FILE%
  popd
  exit /b 1
)

echo Successfully created %OUT_FILE%
popd
endlocal
