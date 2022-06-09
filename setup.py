import sys
from cx_Freeze import setup , Executable

setup(name="object detector",
      version="0.1",
      description="this software does object detection in realtime",
      executables=[Executable("main.py")]
      )