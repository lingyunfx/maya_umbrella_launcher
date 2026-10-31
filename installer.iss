#ifndef AppVersion
  #error AppVersion must be supplied by uv run build
#endif

[Setup]
AppId={{71D69393-3EC1-46D4-8343-1535C0CA7421}
AppName=Maya Umbrella Launcher
AppVersion={#AppVersion}
DefaultDirName={localappdata}\Programs\Maya Umbrella Launcher
DefaultGroupName=Maya Umbrella Launcher
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
OutputDir=dist
OutputBaseFilename=MayaUmbrellaLauncher-{#AppVersion}-Setup
SetupIconFile=maya_umbrella_launcher\resource\app_umbrella.ico
UninstallDisplayIcon={app}\maya_umbrella_launcher.exe
LicenseFile=LICENSE
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
CloseApplications=yes

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; Flags: unchecked

[Files]
Source: "build\launcher_view.dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "build\launcher_cmd.dist\*"; DestDir: "{app}\cli"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Maya Umbrella Launcher"; Filename: "{app}\maya_umbrella_launcher.exe"
Name: "{autodesktop}\Maya Umbrella Launcher"; Filename: "{app}\maya_umbrella_launcher.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\maya_umbrella_launcher.exe"; Description: "Launch Maya Umbrella Launcher"; Flags: nowait postinstall skipifsilent
