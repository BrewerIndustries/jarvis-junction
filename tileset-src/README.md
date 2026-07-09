# Reskinning Jarvis's Junction — tileset workflow

The whole look of the game is one image: **`tileset-lexy.png`**, a **1024×1024**
sheet laid out as a **32×32 grid of 32px tiles**. The engine reads each tile by
its grid position, so **pixel = `col × 32, row × 32`**. Reskinning is just
repainting cells on that grid.

There are three ways in, from "no code" to "regenerate everything".

## The loop, in one command each

```bash
# 1. EXPORT the current art to an editable template (+ a labelled guide + the atlas)
python3 tileset-src/tileset-tool.py export

# 2. …paint over tileset-src/template/tileset.png…  (see "Editing" below)

# 3a. PACK it back in as the game's default tileset
python3 tileset-src/tileset-tool.py pack tileset-src/template/tileset.png
#     OR 3b. upload the edited PNG live in-game (no rebuild — see below)
```

`export` writes into `tileset-src/template/`:
- **`tileset.png`** — a clean copy of the current sheet. **This is what you paint.**
- **`guide.png`** — a transparent overlay with the cell grid + each tile's name.
  Open it as a **top layer** in your editor for reference, then **hide/remove it
  before you export or pack** (it must not end up baked into the art).

## Editing

Open `template/tileset.png` in any pixel editor (Aseprite, Piskel, Photoshop,
GIMP). Add `guide.png` as a top layer so you can see which cell is which. Paint
your 32×32 sprite into each cell, keeping it on the grid. Then flatten/hide the
guide and save at the full **1024×1024** size.

- **Terrain tiles** (floor, wall, water…) are **opaque** — fill the whole 32×32.
- **Items, blocks, characters, monsters, VFX** are drawn **over** terrain, so
  give them a **transparent background** (only the object is painted).
- Animated tiles use several cells in a row (e.g. `water` = 4 frames); paint each.
- Directional actors (player, monsters) use a block of cells; the current art
  just repeats one sprite — paint each facing if you want real turning.

## Uploading live in-game (fastest, no rebuild)

The game reads any square 32×32-grid PNG as this ("Jarvis") layout. So you can
preview an edit instantly. **Options → Tilesets** has the whole loop built in:

- **⤓ Download tileset** — the sheet to paint.
- **⤓ Download numbered guide** — a transparent overlay that numbers every cell;
  lay it on top while you paint.
- **View legend** — a page listing every numbered cell with its thumbnail, exactly
  what it is (e.g. `player — moving · west · #3`, `ice corner SE`), and what the
  tile does. Searchable. The numbers match the guide.
- **Load custom tileset →** pick your edited `tileset.png` to apply it live.

It's applied immediately and remembered in your browser. Great for iterating.
To make it everyone's default, `pack` it and redeploy (below).

## Shipping it as the default

```bash
python3 tileset-src/tileset-tool.py pack tileset-src/template/tileset.png
git add tileset-lexy.png && git commit -m "reskin: <what changed>"
git push origin dev            # updates the dev site
# then promote dev -> main via an approved PR for the public URL
```

## Reference & regeneration

| file | what it is |
| ---- | ---------- |
| `atlas-template.png` | printed map: every tile named at its slot, with col/row rulers |
| `tile-index.md` | text key: tile → `col,row` → cell count, grouped by category |
| `tile-cells.json` | machine-readable: tile → every cell it occupies |
| `make-tileset.py` | the procedural generator (one function per tile) |
| `make-atlas-template.py` | rebuilds the atlas + index from the current sheet |
| `tileset-tool.py` | `export` / `pack FILE` / `regen` / `atlas` |

- `python3 tileset-src/tileset-tool.py regen` — rebuild the whole sheet from the
  procedural generators (after you tweak a generator in `make-tileset.py`).
- `python3 tileset-src/tileset-tool.py atlas` — rebuild just the labelled atlas.

Requires Pillow: `pip3 install Pillow`.
