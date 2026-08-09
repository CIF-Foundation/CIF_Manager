; CIF Core Windows installer
;
; Installs files from resource\ to C:\Users\Public\Documents\,
; preserving the directory structure under resource\.
;
; build_nsis.bat stages resource\ and overlays files listed in
; Installers/cif_core_windows.build.json (protos and Python orchestration
; from src/) before invoking makensis with /DRESOURCE_DIR=...

!ifndef RESOURCE_DIR
  !define RESOURCE_DIR "resource"
!endif

!include "MUI2.nsh"

!define MUI_ICON "cif_icon.ico"
!define MUI_UNICON "cif_icon.ico"

!define PRODUCT_NAME "CIF Core"
!define PRODUCT_VERSION "2.2.3.0"
!define PRODUCT_PUBLISHER "Dome Automation"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\CIF-CORE"
!define INSTALL_DIR "C:\Users\Public\Documents"
!define UNINSTALL_DIR "$PROGRAMFILES64\CIF-Core"
!define UNINSTALLER_NAME "cif-core-Uninstall.exe"
!define MANAGER_UI_EXE "$INSTDIR\CIF\manager\CIF Manager UI.exe"
!define STARTMENU_DIR "$SMPROGRAMS\${PRODUCT_NAME}"

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "cif-core-${PRODUCT_VERSION}.exe"
InstallDir "${INSTALL_DIR}"
RequestExecutionLevel admin
ShowInstDetails show
ShowUnInstDetails show

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_INSTFILES
!define MUI_FINISHPAGE_TEXT "Setup has successfully installed ${PRODUCT_NAME}.$\r$\n$\r$\nCIF files were installed to C:\Users\Public\Documents\CIF$\r$\n$\r$\nLaunch CIF Manager UI from the Start Menu under ${PRODUCT_NAME}."
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "English"

Section "Install"
  SetOutPath "${INSTALL_DIR}"
  File /r "${RESOURCE_DIR}\*"

  SetShellVarContext all
  CreateDirectory "${STARTMENU_DIR}"
  IfFileExists "${MANAGER_UI_EXE}" 0 +2
    CreateShortCut "${STARTMENU_DIR}\CIF Manager UI.lnk" "${MANAGER_UI_EXE}" "" "${MANAGER_UI_EXE}" 0

  SetOutPath "${UNINSTALL_DIR}"
  WriteUninstaller "${UNINSTALL_DIR}\${UNINSTALLER_NAME}"

  WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "DisplayName" "${PRODUCT_NAME}"
  WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "UninstallString" "$\"${UNINSTALL_DIR}\${UNINSTALLER_NAME}$\""
  WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
  WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "InstallLocation" "${INSTALL_DIR}"
  WriteRegDWORD HKLM "${PRODUCT_UNINST_KEY}" "NoModify" 1
  WriteRegDWORD HKLM "${PRODUCT_UNINST_KEY}" "NoRepair" 1
SectionEnd

Section "Uninstall"
  SetShellVarContext all
  Delete "${STARTMENU_DIR}\CIF Manager UI.lnk"
  RMDir "${STARTMENU_DIR}"

  RMDir /r "${INSTALL_DIR}\CIF"
  Delete "${UNINSTALL_DIR}\${UNINSTALLER_NAME}"
  RMDir "${UNINSTALL_DIR}"
  DeleteRegKey HKLM "${PRODUCT_UNINST_KEY}"
SectionEnd
