"""Compile the GUI and CLI with Nuitka, then create an Inno Setup installer."""
import os
from pathlib import Path
import shutil
import subprocess
import sys

from maya_umbrella_launcher.__version__ import __version__

ROOT = Path(__file__).resolve().parent.parent


def find_iscc():
    candidates = [os.environ.get("ISCC"), shutil.which("ISCC.exe")]
    for base in (os.environ.get("LOCALAPPDATA"), os.environ.get("ProgramFiles"),
                 os.environ.get("ProgramFiles(x86)")):
        if base:
            for version in ("7", "6"):
                candidates.extend([str(Path(base) / f"Inno Setup {version}" / "ISCC.exe"),
                                   str(Path(base) / "Programs" / f"Inno Setup {version}" / "ISCC.exe")])
    candidates.append(str(ROOT / ".tools" / "inno" / "ISCC.exe"))
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return candidate
    raise SystemExit("Inno Setup is required. Install it from https://jrsoftware.org/isdl.php "
                     "or set ISCC to the full path of ISCC.exe, then rerun uv run build.")


def main():
    if sys.platform != "win32" or sys.maxsize <= 2**32:
        raise SystemExit("Build requires 64-bit Windows and Python 3.10.")
    iscc = find_iscc()
    output = ROOT / "build"
    resource = ROOT / "maya_umbrella_launcher" / "resource"
    common = [sys.executable, "-m", "nuitka", "--mode=standalone",
              "--enable-plugin=pyside6", "--include-module=PySide6.QtSvg", "--assume-yes-for-downloads",
              f"--output-dir={output}", "--include-package=maya_umbrella_launcher",
              "--nofollow-import-to=maya_umbrella_launcher.build",
              "--include-package-data=dayu_widgets", "--include-package-data=certifi",
              f"--include-data-dir={resource}=maya_umbrella_launcher/resource",
              f"--windows-icon-from-ico={resource / 'app_umbrella.ico'}",
              f"--product-version={__version__}", f"--file-version={__version__}",
              "--product-name=Maya Umbrella Launcher"]
    for module, name, console in (("launcher_view", "maya_umbrella_launcher.exe", "disable"),
                                  ("launcher_cmd", "launcher_cmd.exe", "force")):
        subprocess.run(common + [f"--output-filename={name}",
                       f"--windows-console-mode={console}",
                       str(ROOT / "maya_umbrella_launcher" / f"{module}.py")],
                       cwd=ROOT, check=True)
    subprocess.run([iscc, f"/DAppVersion={__version__}", str(ROOT / "installer.iss")],
                   cwd=ROOT, check=True)
    print(f"Installer: {ROOT / 'dist' / ('MayaUmbrellaLauncher-' + __version__ + '-Setup.exe')}")


if __name__ == "__main__":
    main()
