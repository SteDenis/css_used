from cx_Freeze import setup, Executable
import os.path
import sys

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
print(PYTHON_INSTALL_DIR)
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')
options = {
    'build_exe': {
        'include_files':[
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
        ],
    },}

base = None
if sys.platform == "win32":
    base = "Win32GUI"


target = Executable(
    script = "app.py",
    copyright= "SteDenis",
    base = base)

setup( name = "SteDenis",
       version = "0.1" ,
       description = "" ,
       options = options,
       executables = [target])
