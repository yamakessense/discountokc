#!/usr/bin/env python3
"""Optimise photos dropped into assets/photos/pages/<page>/.

Run by .github/workflows/optimize-photos.yml on every push that touches that
folder. Can also be run locally after `pip install pillow`.

For each JPEG or PNG it finds, it writes `<name>.webp` capped at 1200px wide
plus `<name>@800.webp` and `<name>@400.webp`, then deletes the original so the
folder stays tidy and the repository does not carry both copies. WebP files
already at or under 1200px are left alone except for filling in any missing
derivative.

It never upscales: a source narrower than a derivative width is skipped, which
is why a small photo simply gets fewer files rather than a blurry big one.

The filename is deliberately preserved, because build.py turns it into the
photo's alt text. `red rubber mulch supersack.jpg` becomes
`red rubber mulch supersack.webp` and reads as "Red rubber mulch supersack".
"""
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES_DIR = os.path.join(HERE, "assets", "photos", "pages")

MAIN_WIDTH = 1200
DERIVATIVES = (800, 400)
QUALITY = 82
SOURCES = (".jpg", ".jpeg", ".png", ".webp")


def save(img, path, width):
    if img.width > width:
        h = round(img.height * width / img.width)
        img = img.resize((width, h), Image.LANCZOS)
    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGB")
    img.save(path, "WEBP", quality=QUALITY, method=6)
    return img.width


def main():
    if not os.path.isdir(PAGES_DIR):
        print("no assets/photos/pages/ yet — nothing to do")
        return 0

    changed = False
    for page in sorted(os.listdir(PAGES_DIR)):
        d = os.path.join(PAGES_DIR, page)
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            stem, ext = os.path.splitext(f)
            if ext.lower() not in SOURCES or "@" in stem or f.startswith("."):
                continue

            src = os.path.join(d, f)
            main_path = os.path.join(d, stem + ".webp")
            needed = [w for w in DERIVATIVES
                      if not os.path.exists(os.path.join(d, f"{stem}@{w}.webp"))]

            with Image.open(src) as img:
                img.load()
                # An oversized or non-WebP source always gets rewritten.
                if ext.lower() != ".webp" or img.width > MAIN_WIDTH:
                    w = save(img.copy(), main_path, MAIN_WIDTH)
                    print(f"  {page}/{stem}.webp  {w}px")
                    changed = True
                else:
                    w = img.width

                for width in needed:
                    if w <= width:
                        continue
                    save(img.copy(), os.path.join(d, f"{stem}@{width}.webp"), width)
                    print(f"  {page}/{stem}@{width}.webp")
                    changed = True

            if ext.lower() != ".webp" and os.path.exists(main_path):
                os.remove(src)
                print(f"  removed original {page}/{f}")
                changed = True

    print("changed" if changed else "everything already optimised")
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a") as fh:
            fh.write(f"changed={'true' if changed else 'false'}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
