#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Freeze script for Windows and Mac OSX.
"""
import glob
import os
import shutil
import sys
from cx_Freeze import setup, Executable


# Clean up
if os.path.exists("build"):
    shutil.rmtree(os.path.join(os.getcwd(), "build"))
if os.path.exists("dist"):
    shutil.rmtree(os.path.join(os.getcwd(), "dist"))

# Detect system
windows = sys.platform == 'win32'
osx = sys.platform == 'darwin'

app_script = "Time2Pull.py"
app_name = "Time2Pull"
app_exe = "Time2Pull.exe" if windows else app_name
app_icon = "time2pull/forms/icons/Time2Pull.ico" if windows else None


# Get App version
def read_version():
    """
    Reads the version without self importing
    """
    with open("time2pull/__init__.py") as f:
        lines = f.read().splitlines()
        for l in lines:
            if "__version__" in l:
                version = l.split("=")[1].strip().replace('"', "").replace("'", "")
                version = version.replace('-beta', '')
                version = version.replace('-alpha', '')
                return version
__version__ = read_version()


if len(sys.argv) == 1:
    sys.argv.append("build")

options = {"includes": ["PyQt5.QtNetwork"]}

print("### Freezing application\n"
      "#####################################################################\n")
setup(name=app_name,
      version=__version__,
      options={"build_exe": options, "bdist_mac": {'iconfile': app_icon}},
      executables=[
          Executable(
              app_script, targetName=app_exe,
              icon=app_icon if windows else None,
              base="Win32GUI" if windows else None
          )
      ]
)

if windows:
    print("\n### Creating windows installer using Inno Setup\n"
          "#####################################################################\n")
    try:
        build_dir = glob.glob("build/*")[0]
        # configure setup.iss with the correct version and build directory.
        with open("setup.iss.in", "r") as src, open("setup.iss", "w") as dst:
            lines = src.readlines()
            data = []
            for l in lines:
                l = l.replace("@VERSION@", __version__)
                l = l.replace("@BUILD_DIR@", build_dir)
                data.append(l)
            dst.writelines(data)
        # copy
        import PyQt5
        shutil.copy(os.path.join(os.path.dirname(PyQt5.__file__), "libEGL.dll"), build_dir)
        os.environ["PATH"] += ';C:\Program Files (x86)\Inno Setup 5'
        os.system("iscc %s" % os.path.join(os.getcwd(), "setup.iss"))
    except Exception as e:
        print(e)

