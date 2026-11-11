; Inno Setup 7 supports deep dependency paths without user registry changes.
#if VER < EncodeVer(7, 0, 0)
  #error Inno Setup 7 or newer is required for long-path installation support.
#endif
#ifndef AppVersion
  #define AppVersion "0.2.5"
#endif
#ifndef DistDir
  #define DistDir "..\dist\SynthBO"
#endif

[Setup]
SetupArchitecture=x64
AppId={{B04C2468-D93F-4641-8D6F-CB7A78600EB1}
AppName=SynthBO
AppVersion={#AppVersion}
AppPublisher=SynthBO contributors
AppPublisherURL=https://github.com/wei-rui499/SynthBO
AppSupportURL=https://github.com/wei-rui499/SynthBO/issues
AppComments=Independent desktop interface for local chemical experiment planning
DefaultDirName={localappdata}\Programs\SynthBO
DefaultGroupName=SynthBO
UsePreviousGroup=no
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0.17763
OutputDir=..\installers
OutputBaseFilename=SynthBO-{#AppVersion}-windows-x64-setup-unsigned
Compression=lzma2/fast
SolidCompression=yes
LZMAUseSeparateProcess=yes
WizardStyle=modern
UninstallDisplayIcon={app}\SynthBO.exe
CloseApplications=yes
RestartApplications=no

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "chinesesimp"; MessagesFile: "localizations\ChineseSimplified.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "{#DistDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[InstallDelete]
; Remove only known previous application entry points when updating this AppId.
; User projects and all other files are outside this list.
Type: files; Name: "{app}\NanoBO.exe"
Type: files; Name: "{autodesktop}\NanoBO.lnk"
Type: files; Name: "{autoprograms}\NanoBO\NanoBO.lnk"
Type: files; Name: "{autoprograms}\NanoBO\NanoBO Tutorials.lnk"
Type: files; Name: "{autoprograms}\NanoBO\Uninstall NanoBO.lnk"
Type: dirifempty; Name: "{autoprograms}\NanoBO"

[Icons]
Name: "{group}\SynthBO"; Filename: "{app}\SynthBO.exe"; WorkingDir: "{localappdata}"
Name: "{group}\SynthBO Tutorials"; Filename: "{app}\_internal\docs\html\index.html"
Name: "{autodesktop}\SynthBO"; Filename: "{app}\SynthBO.exe"; WorkingDir: "{localappdata}"; Tasks: desktopicon
Name: "{group}\Uninstall SynthBO"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\SynthBO.exe"; Description: "{cm:LaunchProgram,SynthBO}"; Flags: nowait postinstall skipifsilent

; Project files are user-owned. The uninstaller removes only the installed app.
