# Reskinning Jarvis's Junction — tileset workflow

The whole look of the game is one image: **`tileset-lexy.png`**, a **1024×1024**
sheet laid out as a **32×32 grid of 32px tiles**. The engine reads each tile by
its grid position, so **pixel = `col × 32, row × 32`**. Reskinning is just
repainting cells on that grid.

There are three ways in, from "no code" to "regenerate everything".

## How the sheet is laid out

Two zones on the grid:

- **Left block (cols 0–15)** — terrain and items: floors, walls, water/fire/ice,
  keys, doors, boots, buttons, blocks. Mostly one cell each; a few animate across a
  row (e.g. `water` = 4 frames).
- **Right block (cols 16–31)** — the animated actors: `player`, `player2`, and every
  monster.

For actors the grid is **rows = facing direction, columns = animation frames**:

- **Rows go North, East, South, West** (top → bottom).
- Columns are the frames for each state. The **player** (cols 16–31, rows 0–3) reads
  left-to-right: col 16 = standing · cols 16–23 = the 8-frame **walk cycle** ·
  24–25 = **swimming** · 26–28 = **pushing** · 29 = **skating** (ice/force floor) ·
  30 = **burned** · 31 = **exited**.
- Monsters follow the same rule — each creature's block is *directions × walk frames*.

So the cell at **(18, 3)** is *player · walking west · frame 3*. The **View legend**
button (Options → Tilesets) spells this out for every cell, and the **numbered guide**
stamps matching numbers onto the sheet. `atlas-template.png` is the printed version of
the same map.

(Top-left, rows 0–1 cols 0–15, is a bitmap font + digit tiles used for floor letters
and score numbers — not something you'd normally repaint.)

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
| `tile-index.json` | tile → primary `[col, row, cellCount]` |
| `tile-descriptions.json` | tile → plain-English "what it does" (used by the in-app legend) |
| `make-tileset.py` | the procedural generator (one function per tile) |
| `make-atlas-template.py` | rebuilds the atlas + index from the current sheet |
| `tileset-tool.py` | `export` / `pack FILE` / `regen` / `atlas` / `extract` |

- `python3 tileset-src/tileset-tool.py regen` — rebuild the whole sheet from the
  procedural generators (after you tweak a generator in `make-tileset.py`).
- `python3 tileset-src/tileset-tool.py atlas` — rebuild just the labelled atlas.

## Extracting a tileset into individual tiles

```bash
python3 tileset-src/tileset-tool.py extract [FILE] [OUTDIR] [--all]
```

Slices a tileset into **the full sheet** plus a **folder of one PNG per named tile** —
handy for editing a single sprite, feeding tiles to an image model one at a time, or
building references. Works on any lexy-layout sheet: the default `tileset-lexy.png`, the
bundled `reference-lexy.png`, or an edited sheet you downloaded from the game
(Options → Tilesets → ⤓ Download tileset).

Output lands in `tileset-src/extract/<name>/` (git-ignored):
- `<name>.png` — the whole sheet (the "card").
- `tiles/` — `floor.png`, `key_red.png`, … ; animated/multi-cell tiles are numbered
  `player__f00.png`, `player__f01.png`, … in layout order.
- `index.md` + `manifest.json` — map each file back to its tile name / frame / `col,row`.
- add `--all` to also dump **every** non-empty grid cell by coordinate into `cells/`.

## Importing — a full card or individual tiles

```bash
python3 tileset-src/tileset-tool.py import SOURCE [--onto BASE] [--out FILE] [--pack]
```

The inverse of `extract` — rebuilds a full sheet from either:
- **a full-card PNG** (a 1024×1024 sheet), or
- **a folder of individual tiles** named the way `extract` writes them
  (`key_red.png`, `player__f03.png`, `c16_r00.png`). Only the tiles you supply are placed,
  so you can drop in just the sprites you changed.

Options:
- `--onto BASE` — what the tiles paste onto: `current` (the live `tileset-lexy.png`, so
  untouched tiles keep their art — the default), `blank` (transparent), or a path to any sheet.
- `--out FILE` — where to write the result (default `tileset-src/import-out.png`).
- `--pack` — install the result as the game tileset immediately (same as running `pack`).
- Tiles that aren't 32×32 (e.g. AI output at 2×) are auto-resized down with nearest-neighbour.

Round-trip: `extract` → edit / regenerate individual tiles → `import` → preview in-game
(Options → Tilesets → Load custom tileset) or `--pack` to ship. Verified lossless: importing
an unedited extract reproduces every named cell exactly.

Requires Pillow: `pip3 install Pillow`.
