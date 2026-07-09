#!/usr/bin/env python3
"""Round-trip reskin toolkit for Jarvis's Junction.

The tileset is a plain 32x32 grid PNG (1024x1024). This tool makes reskinning a
clean loop: EXPORT the current art to an editable template (+ a labelled guide
overlay), paint over the cells, then PACK it back into the game — or just upload
the edited PNG in-game via Options -> Tilesets -> Load custom tileset.

Usage (from repo root):
  python3 tileset-src/tileset-tool.py export      # -> tileset-src/template/
  python3 tileset-src/tileset-tool.py pack FILE    # install FILE as the tileset
  python3 tileset-src/tileset-tool.py regen        # rebuild the procedural sheet
  python3 tileset-src/tileset-tool.py atlas        # rebuild the labelled atlas
"""
import sys, os, shutil, json, subprocess
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SHEET = os.path.join(ROOT, "tileset-lexy.png")
TPL_DIR = os.path.join(HERE, "template")
CELLS = json.load(open(os.path.join(HERE, "tile-cells.json")))
T = 32
SIZE = (1024, 1024)

def load_font(sz):
    for p in ("/System/Library/Fonts/Menlo.ttc", "/System/Library/Fonts/Monaco.ttf",
              "/System/Library/Fonts/Supplemental/Arial.ttf"):
        if os.path.exists(p):
            try:
                from PIL import ImageFont; return ImageFont.truetype(p, sz)
            except Exception: pass
    from PIL import ImageFont; return ImageFont.load_default()

def run(script):
    subprocess.run([sys.executable, os.path.join(HERE, script)], check=True, cwd=ROOT)

def make_guide(out):
    """Transparent 1024x1024 overlay: cell grid + each tile named at its slot.
    Drop this in as a TOP layer while editing template/tileset.png, then hide it
    before you export/pack."""
    im = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    d = ImageDraw.Draw(im, "RGBA")
    for i in range(33):
        heavy = (i % 4 == 0)
        c = (30, 24, 20, 140) if heavy else (30, 24, 20, 55)
        w = 2 if heavy else 1
        d.line([(i*T, 0), (i*T, 1024)], fill=c, width=w)
        d.line([(0, i*T), (1024, i*T)], fill=c, width=w)
    f = load_font(8)
    for name, cells in CELLS.items():
        for (col, row) in cells:
            x0, y0 = col*T, row*T
            d.rectangle([x0, y0, x0+T-1, y0+7], fill=(20, 16, 12, 150))
            d.text((x0+1, y0), name[:8], fill=(255, 240, 210, 255), font=f)
    im.save(out)

def export():
    os.makedirs(TPL_DIR, exist_ok=True)
    shutil.copy(SHEET, os.path.join(TPL_DIR, "tileset.png"))
    make_guide(os.path.join(TPL_DIR, "guide.png"))
    run("make-atlas-template.py")
    print("Exported to tileset-src/template/:")
    print("  tileset.png  <- paint over this (clean 32x32 grid, 1024x1024)")
    print("  guide.png    <- reference overlay: open as a TOP layer, hide before export")
    print("Also refreshed tileset-src/atlas-template.png (printed name/coordinate map).")
    print("\nWhen done:  python3 tileset-src/tileset-tool.py pack tileset-src/template/tileset.png")
    print("Or upload the edited PNG in-game: Options -> Tilesets -> Load custom tileset.")

def pack(path):
    if not os.path.exists(path):
        sys.exit(f"no such file: {path}")
    im = Image.open(path).convert("RGBA")
    if im.size != SIZE:
        sys.exit(f"expected a {SIZE[0]}x{SIZE[1]} sheet (32x32 grid of 32px tiles); got {im.size}. "
                 "Flatten/hide the guide layer and export at full size.")
    im.save(SHEET)
    run("make-atlas-template.py")
    print(f"Installed {os.path.basename(path)} as tileset-lexy.png and refreshed the atlas.")
    print("Reload the game (or redeploy) to see it. To ship to prod, commit + promote via PR.")

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    if cmd == "export": export()
    elif cmd == "pack":
        if len(sys.argv) < 3: sys.exit("usage: tileset-tool.py pack FILE.png")
        pack(sys.argv[2])
    elif cmd == "regen": run("make-tileset.py"); run("make-atlas-template.py"); print("Rebuilt sheet + atlas.")
    elif cmd == "atlas": run("make-atlas-template.py"); print("Rebuilt atlas.")
    else: print(__doc__)

if __name__ == "__main__":
    main()
