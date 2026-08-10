import os
import sys

if getattr(sys, "frozen", False):
    torch_lib = os.path.join(sys._MEIPASS, "torch", "lib")
    os.add_dll_directory(torch_lib)