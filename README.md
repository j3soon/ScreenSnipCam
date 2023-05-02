# Screen Snip Cam

Screenshot capture with a virtual camera window, works on Windows, Linux, and MacOS.

## Prerequisites

### Windows

1. Install Python3:
   ```sh
   winget install python3
   ```

### Linux

1. Install Python3:
   ```sh
   sudo apt update && sudo apt install -y python3
   ```

Make sure you have a Desktop (i.e., Display Manager).

### MacOS

1. Install [Homebrew](https://brew.sh/):
   ```sh
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
2. Install Python3:
   ```sh
   brew install python3
   ```
3. Update Tkinter:
   ```sh
   brew install tcl-tk
   brew install python-tk
   ```

## Launch From Source

```sh
git clone https://github.com/j3soon/ScreenSnipCam.git
cd ScreenSnipCam
# (Optional) Create a virtual environment
pip install -r requirements.txt
python screensnipcam/screensnipcam.py
# Or specify the screenshot directory
python screensnipcam/screensnipcam.py --path=.
```

## FAQ

1. If the screen snip file only shows the MacOS desktop wallpaper without any window, please [allow Screen Recording](https://support.apple.com/guide/mac-help/control-access-to-screen-recording-on-mac-mchld6aa7d23) for ScreenSnipCam or the Terminal.

2. If you encountered the following error message on MacOS:

   ```
   DEPRECATION WARNING: The system version of Tk is deprecated and may be removed in a future release. Please don't rely on it. Set TK_SILENCE_DEPRECATION=1 to suppress this warning.
   ```

   Run `brew install tcl-tk` to fix it by upgrading tkinter.

3. If you saw a black window on MacOS, run `brew install python-tk` to fix it by upgrading python tkinter.

## Related Works

- [GifCam](https://blog.bahraniapps.com/gifcam/): Record screen to gif with a virtual camera window, Windows only. This is also the inspiration of this project.
