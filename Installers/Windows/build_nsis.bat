@echo off
setlocal

set "NSIS=%ProgramFiles(x86)%\NSIS\makensis.exe"
if not exist "%NSIS%" (
  echo Error: NSIS not found at "%NSIS%"
  exit /b 1
)

pushd "%~dp0"

set "STAGING=%~dp0staging"
set "RESOURCE=%~dp0resource"
set "SRC_PROTOS=%~dp0..\..\src\protos"

if not exist "%SRC_PROTOS%" (
  echo Error: Canonical proto directory not found at "%SRC_PROTOS%"
  popd
  exit /b 1
)

if exist "%STAGING%" rmdir /s /q "%STAGING%"

echo Staging installer resources...
xcopy "%RESOURCE%\*" "%STAGING%\resource\" /E /I /Q /Y >nul
if errorlevel 1 (
  echo Error: Failed to stage installer resources.
  popd
  exit /b 1
)

echo Copying protos from src\protos...
xcopy "%SRC_PROTOS%\*" "%STAGING%\resource\CIF\protos\" /I /Y /Q >nul
if errorlevel 1 (
  echo Error: Failed to copy protos from src\protos.
  popd
  exit /b 1
)

"%NSIS%" /DRESOURCE_DIR="%STAGING%\resource" "cif-lvcore.nsi"
if errorlevel 1 (
  popd
  exit /b 1
)

echo Successfully created cif-lvcore-2.2.2.0.exe
popd
endlocal
