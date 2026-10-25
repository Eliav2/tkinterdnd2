import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tkinterdnd2",
    version="0.7.0",
    author="petasis\\pmgagne\\eliav2\\squiblydoo",
    description="TkinterDnD2 is a python wrapper for George Petasis'' tkDnD Tk extension version 2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Eliav2/tkinterdnd2",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={
        # Include tkdnd extension files.
        "tkinterdnd2": [
            "tkdnd/linux-x64/*.*", "tkdnd/linux-x64-tcl9/*.*",
            "tkdnd/linux-arm64/*.*", "tkdnd/linux-arm64-tcl9/*.*",
            "tkdnd/osx-x64/*.*", "tkdnd/osx-arm64/*.*", "tkdnd/osx-arm64-tcl9/*.*",
            "tkdnd/win-x64/*.*", "tkdnd/win-x64-tcl9/*.*",
            "tkdnd/win-x86/*.*", "tkdnd/win-x86-tcl9/*.*",
            "tkdnd/win-arm64/*.*",
            # PyInstaller hook, found through the pyinstaller40 entry point below.
            "__pyinstaller/hook-tkinterdnd2.py",
        ],
    },
    entry_points={
        "pyinstaller40": [
            "hook-dirs = tkinterdnd2.__pyinstaller:get_hook_dirs",
        ],
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)
