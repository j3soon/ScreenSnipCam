import ctypes
import platform


def set_dpi_awareness():
    if platform.system() != "Windows":
        raise Exception("This function is only for Windows")
    release = platform.release()
    # Ref: https://github.com/python/cpython/blob/984387f39a3385ed5699bd7e21797c348e543b19/Lib/platform.py#L333
    # Ref: https://stackoverflow.com/a/44422362
    if release in ['2000', 'XP', 'XPMedia', 'XP64']:
        raise Exception(f"Windows {release} is not supported")
    elif release in ['Vista', '7', '8']:
        # Ref: https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setprocessdpiaware
        success = ctypes.windll.user32.SetProcessDPIAware()
        if success == 0:
            raise Exception("Windows SetProcessDPIAware failed")
    elif release in ['8.1', '10', '11', 'post11']:
        # Ref: https://learn.microsoft.com/en-us/windows/win32/api/shellscalingapi/nf-shellscalingapi-setprocessdpiawareness
        # Ref: https://learn.microsoft.com/en-us/windows/win32/api/shellscalingapi/ne-shellscalingapi-process_dpi_awareness
        PROCESS_SYSTEM_DPI_AWARE = 1
        PROCESS_PER_MONITOR_DPI_AWARE = 2
        S_OK = 0
        success = ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_SYSTEM_DPI_AWARE)
        if success != S_OK:
            raise Exception("Windows SetProcessDpiAwareness failed")
    else:
        raise Exception(f"Unknown Windows release: {release}, " +
            "please open an issue at: https://github.com/j3soon/overlay-toolbox/issues")
