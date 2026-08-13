#!/usr/bin/env python3
"""Prepare photos for the site. Run this locally, never on CI.

The site build (build.py) stays dependency-free on purpose: it reads WebP
dimensions with a hand-rolled header parser and needs no image library. This
script is the other half of that bargain — it is where the actual resizing
happens, on a person's machine, and it commits the results.

    pip install pillow

    # bring a new photo in, at any size, from anywhere
    python3 tools/prep_photos.py add ~/Downloads/IMG_1234.jpg storefront-yukon

    # regenerate the responsive derivatives for everything already committed
    python3 tools/prep_photos.py derive

What it writes, into assets/photos/:

    <name>.webp        the main image, capped at 1200px wide
    <name>@800.webp    for tablets and small laptops
    <name>@400.webp    for phones

build.py picks these up automatically — photo_tag() looks for the @800 and
@400 files on disk and emits a srcset when they exist, so a phone stops
downloading a 1200px photo to display it 356px wide.

It never upscales. A 188px-wide source stays 188px and simply gets no larger
derivatives, because inventing pixels makes a photo look worse, not better.
"""
import os
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is needed for this script only:  pip install pillow\n"
             "The site build itself has no such dependency.")

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHOTO_DIR = os.path.join(HERE, "assets", "photos")

MAIN_WIDTH = 1200
DERIVATIVES = (800, 400)
QUALITY = 82


def _save(img, path, width):
    """Write one WebP at the given width, preserving aspect ratio."""
    if img.width > width:
        h = round(img.height * width / img.width)
        img = img.resize((width, h), Image.LANCZOS)
    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGB")
    img.save(path, "WEBP", quality=QUALITY, method=6)
    return img.width, img.height, os.path.getsize(path)


def process(src, name):
    """One source image -> a main WebP plus whatever derivatives make sense."""
    with Image.open(src) as img:
        img.load()
        sw, sh = img.size

        main = os.path.join(PHOTO_DIR, name + ".webp")
        w, h, size = _save(img.copy(), main, MAIN_WIDTH)
        print(f"  {name}.webp".ljust(34) + f"{w}x{h}  {size // 1024} KB")

        for d in DERIVATIVES:
            if w <= d:
                # Source is already at or below this width. A derivative would
                # be an upscale of an image the browser can just use directly.
                print(f"  {name}@{d}.webp".ljust(34) + f"skipped — source is only {w}px wide")
                continue
            p = os.path.join(PHOTO_DIR, f"{name}@{d}.webp")
            dw, dh, dsize = _save(img.copy(), p, d)
            print(f"  {name}@{d}.webp".ljust(34) + f"{dw}x{dh}  {dsize // 1024} KB")

        if sw < MAIN_WIDTH:
            print(f"  note: source was only {sw}x{sh}. It will look soft on a "
                  f"high-DPI phone. A larger original would render sharper.")


def cmd_add(args):
    if len(args) != 2:
        sys.exit("usage: prep_photos.py add <source-image> <name>")
    src, name = args
    if not os.path.exists(src):
        sys.exit(f"no such file: {src}")
    print(f"{os.path.basename(src)} -> assets/photos/")
    process(src, name)
    print(f"\nNow add it to PHOTOS in build.py as (\"{name}.jpg\", \"alt text here\").")


def cmd_derive(_args):
    """Rebuild @800/@400 for every main photo already committed."""
    mains = sorted(f for f in os.listdir(PHOTO_DIR)
                   if f.endswith(".webp") and "@" not in f)
    print(f"{len(mains)} photos in assets/photos/\n")
    made = skipped = 0
    for f in mains:
        name = f[:-5]
        path = os.path.join(PHOTO_DIR, f)
        with Image.open(path) as img:
            img.load()
            for d in DERIVATIVES:
                if img.width <= d:
                    skipped += 1
                    continue
                out = os.path.join(PHOTO_DIR, f"{name}@{d}.webp")
                _save(img.copy(), out, d)
                made += 1
    print(f"wrote {made} derivatives, skipped {skipped} "
          f"(source already at or below that width)")


COMMANDS = {"add": cmd_add, "derive": cmd_derive}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        sys.exit(__doc__)
    COMMANDS[sys.argv[1]](sys.argv[2:])
