"""PyInstaller hook file for tkinterdnd2.

PyInstaller finds this hook automatically when tkinterdnd2 is installed, so a
plain `pyinstaller myproject.py` is enough. To use a copy of this file instead,
put it in a folder and pass that folder to PyInstaller:

    pyinstaller myproject/myproject.py --additional-hooks-dir=.
"""

import os
import platform
import tkinter
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs, logger


# tkinterdnd2 ships the tkdnd library for every OS and CPU, one folder each:
#   tkinterdnd2/tkdnd/win-x64/        (for Tcl/Tk 8)
#   tkinterdnd2/tkdnd/win-x64-tcl9/   (for Tcl/Tk 9, not every platform has one)
# A built app only runs on the OS, CPU and Tcl/Tk of the Python doing the build,
# so this hook bundles only the folder the built app will load.
PLATFORM_FOLDERS = {
    ('Linux', 'aarch64'): 'linux-arm64',
    ('Linux', 'x86_64'): 'linux-x64',
    ('Windows', 'ARM64'): 'win-arm64',
    ('Windows', 'AMD64'): 'win-x64',
    ('Windows', 'x86'): 'win-x86',
}

# macOS apps can be built for both Intel and Apple Silicon at once
# (--target-arch universal2), so always bundle both macOS folders.
MACOS_FOLDERS = ['osx-arm64', 'osx-x64']

# Each platform folder also contains the Tcl scripts for the other OSes; skip those.
UNUSED_SCRIPTS = {
    'Windows': {'tkdnd_unix.tcl', 'tkdnd_macosx.tcl'},
    'Linux': {'tkdnd_windows.tcl', 'tkdnd_macosx.tcl'},
    'Darwin': {'tkdnd_windows.tcl', 'tkdnd_unix.tcl'},
}

system = platform.system()
# Same CPU detection as TkinterDnD._require(): on Windows, PROCESSOR_ARCHITECTURE gives
# the architecture of the running Python (e.g. AMD64 for x64 Python on an ARM64 PC).
if system == 'Windows':
    machine = os.environ.get('PROCESSOR_ARCHITECTURE', platform.machine())
else:
    machine = platform.machine()

if system == 'Darwin':
    platform_folders = MACOS_FOLDERS
elif (system, machine) in PLATFORM_FOLDERS:
    platform_folders = [PLATFORM_FOLDERS[(system, machine)]]
else:
    # Warn instead of failing the build: this hook runs for every PyInstaller build
    # that uses tkinterdnd2, and the app may work without drag and drop.
    logger.warning('tkinterdnd2: no TkDND binaries for platform "%s %s"; none will be bundled.', system, machine)
    platform_folders = []

all_files = collect_data_files('tkinterdnd2') + collect_dynamic_libs('tkinterdnd2')
available_folders = {os.path.basename(dest) for src, dest in all_files}
uses_tcl9 = int(str(tkinter.TclVersion).split('.')[0]) >= 9


def folder_to_bundle(platform_folder):
    # Like TkinterDnD._require(), use the Tcl 9 folder when building with Tcl 9,
    # falling back to the Tcl 8 folder if there is no Tcl 9 build for this platform.
    if uses_tcl9 and platform_folder + '-tcl9' in available_folders:
        return platform_folder + '-tcl9'
    return platform_folder


folders_to_bundle = {folder_to_bundle(f) for f in platform_folders}


def is_needed(source_path, dest_dir):
    folder = os.path.basename(dest_dir)
    filename = os.path.basename(source_path)
    return folder in folders_to_bundle and filename not in UNUSED_SCRIPTS[system]


datas = {(src, dest) for src, dest in all_files if is_needed(src, dest)}
