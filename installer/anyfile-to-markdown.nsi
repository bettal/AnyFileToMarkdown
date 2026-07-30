!include "MUI2.nsh"

Name "AnyFile to Markdown"
OutFile "AnyFileToMarkdown-Setup.exe"
Unicode True
InstallDir "$PROGRAMFILES\AnyFileToMarkdown"
RequestExecutionLevel admin

!define MUI_ABORTWARNING
!define MUI_ICON "..\icon.ico"

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "Russian"

Section "Install"
  SetOutPath "$INSTDIR"
  File /r "..\dist\AnyFileToMarkdown\*.*"
  CreateShortCut "$DESKTOP\AnyFile to Markdown.lnk" "$INSTDIR\AnyFileToMarkdown.exe"
  CreateDirectory "$SMPROGRAMS\AnyFile to Markdown"
  CreateShortCut "$SMPROGRAMS\AnyFile to Markdown\AnyFile to Markdown.lnk" "$INSTDIR\AnyFileToMarkdown.exe"
  CreateShortCut "$SMPROGRAMS\AnyFile to Markdown\Uninstall.lnk" "$INSTDIR\uninstall.exe"
  WriteUninstaller "$INSTDIR\uninstall.exe"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\AnyFileToMarkdown" "DisplayName" "AnyFile to Markdown"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\AnyFileToMarkdown" "UninstallString" '"$INSTDIR\uninstall.exe"'
SectionEnd

Section "Uninstall"
  Delete "$DESKTOP\AnyFile to Markdown.lnk"
  RMDir /r "$SMPROGRAMS\AnyFile to Markdown"
  RMDir /r "$INSTDIR"
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\AnyFileToMarkdown"
SectionEnd
