import argparse
import platform
import sys
import tkinter as tk
from datetime import datetime
from pathlib import Path

import utils.windows
from PIL import ImageGrab, ImageOps


class ScreenSnipCam:
    def __init__(self, path):
        self.frame1_size = (-1, -1)
        self.frame1_thickness = 1
        # Ref: https://stackoverflow.com/a/69325836
        if platform.system() == "Windows" and sys.getwindowsversion().build >= 22000:
            # Windows 11 has round window edges
            self.frame1_thickness = 4
        self.transparent_color = "gray"
        self.dirpath = Path(path)

    def on_resize(self, event):
        if event.widget != self.frame1:
            # Only listen to frame1 resize events
            return
        # Shrink the snip region to avoid capturing the black border of frame1
        w = event.width - 2 * self.frame1_thickness
        h = event.height - 2 * self.frame1_thickness
        if self.frame1_size == (w, h):
            # Only listen to size changes
            return
        self.frame1_size = (w, h)
        self.root.title(f"ScreenSnipCam: {w}x{h}")

    def save_screenshot(self):
        x = self.frame1.winfo_rootx() + 1 * self.frame1_thickness
        y = self.frame1.winfo_rooty() + 1 * self.frame1_thickness
        w = self.frame1.winfo_width() - 2 * self.frame1_thickness
        h = self.frame1.winfo_height() - 2 * self.frame1_thickness
        assert (w, h) == self.frame1_size
        cropping = self.check1_var.get()

        print(f"snipping at location ({x}, {y}) with size {w}x{h}, cropping: {cropping}")
        img = ImageGrab.grab(bbox=(x, y, x+w, y+h), all_screens=True)
        # The conversion is required since the grab output format may vary.
        img = img.convert('RGB')
        assert (w, h) == img.size
        if cropping:
            bbox = ImageOps.invert(img).getbbox()
            img = img.crop(bbox)

        filename = self.txt1.get("1.0", tk.END).strip()
        if filename == "":
            ts = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
            filename = f"{ts}_{w}x{h}"
        self.dirpath.mkdir(parents=True, exist_ok=True)
        filepath = self.dirpath / (filename + ".png")
        idx = 0
        while filepath.exists():
            filepath = self.dirpath / (filename + "_" + str(idx) + ".png")
            idx += 1
        print(f"saving to file: {filepath}")
        img.save(filepath)
        self.txt1.delete("1.0", tk.END)

    def layout(self):
        # Main window
        self.root = tk.Tk()
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.wm_attributes("-topmost", True)
        self.root.bind('<Configure>', self.on_resize)
        self.root.geometry('500x500')

        # Two frames splitting the window into two columns
        # Snip region
        self.frame1 = tk.Frame(
            self.root,
            background=self.transparent_color,
            highlightbackground="black",
            highlightthickness=self.frame1_thickness
        )
        # Controls
        self.frame1.grid(row=0, column=0, sticky=tk.NSEW)
        self.frame2 = tk.Frame(self.root)
        self.frame2.grid(row=0, column=1, sticky=tk.NSEW)
        # Textbox specifying the filename
        self.txt1 = tk.Text(self.frame2, width=10, height=1)
        self.txt1.pack(padx=8, pady=8)
        # Button for taking a screenshot
        self.btn1 = tk.Button(self.frame2, text="Snip", command=self.save_screenshot)
        self.btn1.pack(padx=8, pady=8)
        # Checkbox for determining whether to crop the screenshot
        self.check1_var = tk.IntVar()
        self.check1 = tk.Checkbutton(self.frame2, text="Crop", variable=self.check1_var)
        self.check1.pack(padx=8, pady=8)

        # Platform-dependent initialization
        # Ref: https://stackoverflow.com/a/22106858
        if platform.system() == "Linux":
            # Since transparent colors are not supported on Linux, we use alpha instead.
            self.root.wait_visibility(self.root)
            self.root.wm_attributes("-alpha", 0.5)
        elif platform.system() == "Windows":
            self.root.wm_attributes("-transparentcolor", self.transparent_color)
        elif platform.system() == "Darwin":
            self.root.wm_attributes("-transparent", True)
            self.root.config(bg='systemTransparent')
            self.frame1.config(bg='systemTransparent')

    def main(self):
        # Platform-specific initialization
        if platform.system() == "Windows":
            utils.windows.set_dpi_awareness()
        # Initialize window layout
        self.layout()
        # Start the main event (or message) loop
        self.root.mainloop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path",
        default=Path.home() / "Desktop/Screenshots",
        help="directory path to save the screenshot to"
    )
    args = parser.parse_args()
    cam = ScreenSnipCam(args.path)
    cam.main()
