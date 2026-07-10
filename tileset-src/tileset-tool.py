#!/usr/bin/env python3
"""Round-trip reskin toolkit for Jarvis's Junction.

The tileset is a plain 32x32 grid PNG (1024x1024). This tool makes reskinning a
clean loop: EXPORT the current art to an editable template (+ a labelled guide
overlay), paint over the cells, then PACK it back into the game — or just upload
the edited PNG in-game via Options -> Tilesets -> Load custom tileset.

Usage (from repo root):
  python3 tileset-src/tileset-tool.py export        # -> tileset-src/template/
  python3 tileset-src/tileset-tool.py pack FILE      # install FILE as the tileset
  python3 tileset-src/tileset-tool.py regen          # rebuild the procedural sheet
  python3 tileset-src/tileset-tool.py atlas          # rebuild the labelled atlas
  python3 tileset-src/tileset-tool.py extract [FILE] [OUT] [--all]
                                                     # full sheet + a folder of per-tile PNGs
  python3 tileset-src/tileset-tool.py import SOURCE [--onto BASE] [--out FILE] [--pack]
                                                     # rebuild a sheet from a card or per-tile PNGs
"""
import sys, os, re, shutil, json, subprocess
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

def extract(path=None, outdir=None, dump_all=False):
    """Slice a tileset into the full sheet plus one PNG per named tile (animations
    numbered __f00, __f01, …).  Names come from the lexy-layout tile map, so this works
    on any lexy tileset — tileset-lexy.png, reference-lexy.png, or an edited sheet you
    downloaded from the game."""
    src = path or SHEET
    if not os.path.exists(src):
        sys.exit(f"no such file: {src}")
    im = Image.open(src).convert("RGBA")
    base = os.path.splitext(os.path.basename(src))[0]
    out = outdir or os.path.join(HERE, "extract", base)
    tiles_dir = os.path.join(out, "tiles")
    os.makedirs(tiles_dir, exist_ok=True)

    # The full "card": a copy of the whole sheet.
    im.save(os.path.join(out, f"{base}.png"))

    cols, rows = im.width // T, im.height // T
    if (im.width, im.height) != SIZE:
        print(f"note: {im.size} isn't the {SIZE} lexy grid; naming may be partial, "
              "out-of-bounds cells skipped.")
    crop = lambda c, r: im.crop((c*T, r*T, c*T+T, r*T+T))
    blank = lambda cell: cell.getbbox() is None  # fully transparent

    manifest, written, skipped = [], 0, 0
    for name, cells in CELLS.items():
        multi = len(cells) > 1
        for i, (col, row) in enumerate(cells):
            if col >= cols or row >= rows:
                continue
            cell = crop(col, row)
            if blank(cell):
                skipped += 1
                continue
            fname = f"{name}__f{i:02d}.png" if multi else f"{name}.png"
            cell.save(os.path.join(tiles_dir, fname))
            manifest.append({"file": f"tiles/{fname}", "tile": name,
                             "frame": i, "col": col, "row": row})
            written += 1

    if dump_all:
        cells_dir = os.path.join(out, "cells")
        os.makedirs(cells_dir, exist_ok=True)
        extra = 0
        for row in range(rows):
            for col in range(cols):
                cell = crop(col, row)
                if blank(cell):
                    continue
                cell.save(os.path.join(cells_dir, f"c{col:02d}_r{row:02d}.png"))
                extra += 1

    json.dump(manifest, open(os.path.join(out, "manifest.json"), "w"), indent=1)
    with open(os.path.join(out, "index.md"), "w") as f:
        f.write(f"# Extracted tiles — {base}\n\n")
        f.write(f"Source `{os.path.relpath(src, ROOT)}` ({im.width}×{im.height}, "
                f"{cols}×{rows} grid) — {written} tile files.\n\n")
        f.write("| file | tile | frame | col,row |\n|---|---|---|---|\n")
        for m in sorted(manifest, key=lambda m: (m["tile"], m["frame"])):
            f.write(f"| `{m['file']}` | `{m['tile']}` | {m['frame']} | {m['col']},{m['row']} |\n")

    rel = os.path.relpath(out, ROOT)
    print(f"Extracted {base} -> {rel}/")
    print(f"  {base}.png     the full card (whole sheet)")
    print(f"  tiles/         {written} individual tile PNGs (animations are __f00, __f01, …)")
    if skipped:
        print(f"                 {skipped} empty/transparent cells skipped")
    if dump_all:
        print(f"  cells/         {extra} non-empty grid cells, by coordinate (c<col>_r<row>.png)")
    print(f"  index.md + manifest.json   file -> tile / frame / col,row")
    if not dump_all:
        print("  (add --all to also dump every non-empty grid cell by coordinate)")

def _cells_for_filename(stem):
    """Map an individual-tile filename (no extension) back to grid cell(s), matching the
    names `extract` writes: `<tile>` (all its cells), `<tile>__fNN` (frame NN), `c<col>_r<row>`."""
    m = re.fullmatch(r"c(\d+)_r(\d+)", stem)
    if m:
        return [(int(m.group(1)), int(m.group(2)))]
    if "__f" in stem:
        tile, fr = stem.rsplit("__f", 1)
        if tile in CELLS and fr.isdigit() and int(fr) < len(CELLS[tile]):
            return [tuple(CELLS[tile][int(fr)])]
        return None
    if stem in CELLS:
        return [tuple(c) for c in CELLS[stem]]  # a bare tile name fills every cell it owns
    return None

def do_import(source, onto=None, out=None, do_pack=False):
    """Rebuild a full sheet from a full-card PNG, or from a folder of individual tiles
    (as produced by `extract`).  Folder tiles are pasted back onto a base sheet by name,
    so you only need to supply the tiles you changed."""
    if not os.path.exists(source):
        sys.exit(f"no such file/folder: {source}")
    out = out or os.path.join(HERE, "import-out.png")

    if os.path.isfile(source):
        sheet = Image.open(source).convert("RGBA")
        if sheet.size != SIZE:
            sys.exit(f"a full-card import must be {SIZE}; got {sheet.size}. "
                     "For a folder of individual tiles, pass the folder instead.")
        summary = "imported full sheet"
    else:
        # Choose the base the tiles paste onto: current art (keep untouched tiles), a named
        # sheet, or a blank transparent sheet.
        if onto in (None, "current", "sheet"):
            base = SHEET
        elif onto in ("blank", "none", "transparent"):
            base = None
        else:
            base = onto
        if base:
            if not os.path.exists(base):
                sys.exit(f"no base sheet: {base}")
            sheet = Image.open(base).convert("RGBA")
            if sheet.size != SIZE:
                sheet = sheet.resize(SIZE, Image.NEAREST)
        else:
            sheet = Image.new("RGBA", SIZE, (0, 0, 0, 0))

        # Prefer tiles/ + cells/ subfolders (an extract dir); else the folder itself.
        dirs = [d for d in (os.path.join(source, "tiles"), os.path.join(source, "cells"))
                if os.path.isdir(d)] or [source]
        files = sorted(os.path.join(d, fn) for d in dirs for fn in os.listdir(d)
                       if fn.lower().endswith(".png"))
        placed, resized, skipped = 0, 0, []
        for path in files:
            coords = _cells_for_filename(os.path.basename(path)[:-4])
            if coords is None:
                skipped.append(os.path.basename(path))
                continue
            tile = Image.open(path).convert("RGBA")
            if tile.size != (T, T):
                tile = tile.resize((T, T), Image.NEAREST)
                resized += 1
            for (col, row) in coords:
                sheet.paste(tile, (col*T, row*T))  # replace the whole cell (incl. alpha)
                placed += 1
        if placed == 0:
            sys.exit("no placeable tiles found — expected names like player__f00.png, "
                     "key_red.png, or c16_r00.png.")
        summary = f"placed {placed} tiles"
        if resized: summary += f" ({resized} resized to 32x32)"
        if skipped:
            print(f"skipped {len(skipped)} unrecognised file(s): {', '.join(skipped[:6])}"
                  + (" …" if len(skipped) > 6 else ""))

    sheet.save(out)
    print(f"{summary} -> {os.path.relpath(out, ROOT)}")
    if do_pack:
        pack(out)
    else:
        print("Preview it in-game: Options -> Tilesets -> Load custom tileset.")
        print(f"Or install it as the default:  python3 tileset-src/tileset-tool.py pack {os.path.relpath(out, ROOT)}")

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    if cmd == "export": export()
    elif cmd == "pack":
        if len(sys.argv) < 3: sys.exit("usage: tileset-tool.py pack FILE.png")
        pack(sys.argv[2])
    elif cmd == "regen": run("make-tileset.py"); run("make-atlas-template.py"); print("Rebuilt sheet + atlas.")
    elif cmd == "atlas": run("make-atlas-template.py"); print("Rebuilt atlas.")
    elif cmd == "extract":
        args = sys.argv[2:]
        dump_all = "--all" in args
        args = [a for a in args if a != "--all"]
        extract(args[0] if len(args) > 0 else None,
                args[1] if len(args) > 1 else None, dump_all)
    elif cmd == "import":
        args = sys.argv[2:]
        do_pack = "--pack" in args
        args = [a for a in args if a != "--pack"]
        onto = out = None
        positional = []
        i = 0
        while i < len(args):
            if args[i] == "--onto" and i + 1 < len(args): onto = args[i + 1]; i += 2
            elif args[i] == "--out" and i + 1 < len(args): out = args[i + 1]; i += 2
            else: positional.append(args[i]); i += 1
        if not positional:
            sys.exit("usage: tileset-tool.py import SOURCE [--onto BASE] [--out FILE] [--pack]")
        do_import(positional[0], onto, out, do_pack)
    else: print(__doc__)

if __name__ == "__main__":
    main()
