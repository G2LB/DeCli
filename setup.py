#!/usr/bin/env python3
"""
setup.py — DeCli declaratie generator

Gebruik:
    py setup.py fonts      Download Tinos Nerd Font naar fonts/
"""
import os
import sys
import zipfile
import urllib.request

TINOS_URL = "https://github.com/ryanoasis/nerd-fonts/releases/download/v3.3.0/Tinos.zip"
FONTS_DIR = "fonts"
TARGETS = [
    "TinosNerdFont-Regular.ttf",
    "TinosNerdFont-Bold.ttf",
    "TinosNerdFont-Italic.ttf",
    "TinosNerdFont-BoldItalic.ttf",
]


def download_fonts():
    """Download en pak Tinos Nerd Font uit in fonts/."""
    os.makedirs(FONTS_DIR, exist_ok=True)
    zip_path = os.path.join(FONTS_DIR, "Tinos.zip")
    print("  Download Tinos Nerd Font van GitHub...")
    urllib.request.urlretrieve(TINOS_URL, zip_path)
    print("  Uitpakken...")
    with zipfile.ZipFile(zip_path) as zf:
        names = [n for n in zf.namelist() if any(n.endswith(t) for t in TARGETS)]
        for name in names:
            dst = os.path.join(FONTS_DIR, os.path.basename(name))
            if not os.path.exists(dst):
                with zf.open(name) as src, open(dst, "wb") as fh:
                    fh.write(src.read())
                print(f"    {os.path.basename(name)}")
            else:
                print(f"    {os.path.basename(name)} (bestaat al)")
    os.remove(zip_path)
    print("  Klaar! fonts/ bevat Tinos Nerd Font.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "fonts":
        download_fonts()
    else:
        print(__doc__)
