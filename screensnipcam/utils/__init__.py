import platform
from . import windows

def initialize():
    if platform.system() == "Windows":
        windows.set_dpi_awareness()
