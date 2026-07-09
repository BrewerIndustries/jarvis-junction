# Jarvis's Junction

A modern, browser-based tile puzzle game — a friendly reimagining of the classic
early-'90s grid puzzler. **Jarvis's Junction is a fork of
[Lexy's Labyrinth](https://github.com/eevee/lexys-labyrinth) by eevee**, which is
itself an open-source, from-scratch reimplementation (it ships completely original
artwork, sound, and music — none of the original commercial game's assets).

It's static JS with **no build system**: serve the directory and open it in a browser.

## Status

- ✅ Forked from Lexy's Labyrinth upstream (2026-07-06), engine runs unmodified.
- ✅ Rebranded to *Jarvis's Junction* + butler-theme splash/pack copy (`index.html`,
  `js/main.js` `BUILTIN_PACKS`).
- ✅ Removed `tileset-tworld.png` (the vendored Tile World tileset — unused by the app
  and belongs to its owners).
- ✅ **Live**: GitHub Pages at https://jarvis-junction.dabrewer.dev/ (prod) and
  `/dev/` (dev); registered in the Launcher + Dashboard; idea-log card at *Building*.
- ✅ v1 scope agreed — see [`DESIGN.md`](DESIGN.md).
- ✅ **Diegetic butler theme**: warm brass/manor palette + serif type, "Master's
  note" splash, rebranded packs ("inspired by Chip's Challenge"), in-game pack-name
  override, butler UI labels (begin duty / duty roster / gratuity), and butler
  death/win messages. Front page uses the **butler sprite** (`butler.png`) as the logo
  (top splash + bottom bar); the "mode" (compat) button is text-only; the Lexy's
  Labyrinth credit moved to Options → About and the Chip's Challenge trademark notice
  to the foot of the splash.
- ✅ **Game-feel juice** (`js/juice.js`): pickup particles, socket/bomb/death
  screen-shake, "duty complete" confetti, mobile haptics — all off the sfx event
  hook, honoring `prefers-reduced-motion`; plus a game-speed slider, effects
  toggle, last-pressed-wins key override, and input buffering.
- ✅ **In-app tile editor** (Options → Tilesets → *Edit tiles in-app*): a Piskel-style
  pixel editor — pencil/eraser/fill/line/rect, palette + custom color, undo, copy/paste,
  onion skin, a searchable per-cell navigator, and a whole-tileset board (click any cell
  to edit). **Compare** ghost-overlays a reference set (the original Lexy art, or any PNG
  you load) on the canvas for tracing, with a ghost-opacity slider and hold-`\` peek.
  Edits save live to an *"Edited in-app"* tileset that persists across reloads and is a
  first-class row in the Tilesets table (so hitting Save no longer drops it back to Lexy).
  An **"Editing:" source picker** in the editor lets you choose which tileset to paint
  (so you continue your edits instead of always restarting from the base), and an
  **"Active skin" dropdown** in Options → Tilesets switches the live in-game tileset
  instantly for every format at once.
- ⏳ Next (per DESIGN.md): accessibility (colorblind palette, remappable keys),
  progression (medals/Daily Duty), the manor-hub campaign. Original tileset art +
  servers are later.

## Run locally

```bash
python3 -m http.server 8010
# open http://localhost:8010
```

(Browsers block module loading from `file:///`, so you need a real HTTP server.)

## Architecture (inherited from upstream)

All engine code is under `js/`, plain ES modules, ~21.5k lines:

| File | Role |
| ---- | ---- |
| `game.js` | Deterministic simulation core (the tick engine) |
| `tiletypes.js` | Every tile & creature behavior |
| `format-dat.js` | CC1 `.dat`/`.ccl` (MS & Lynx) parser |
| `format-c2g.js` / `format-tws.js` | CC2 `.c2m`/`.c2g` and replay parsers |
| `renderer-canvas.js`, `tileset.js` | HTML5 Canvas rendering |
| `main.js` | UI / app shell |
| `editor/` | Full in-browser level editor |
| `headless/bulktest.mjs` | Node test harness — `node js/headless/bulktest.mjs` |

## Licensing & attribution ⚠️

This project inherits upstream's licensing. **Keep `LICENSE` intact** — the MIT license
requires retaining eevee's copyright notice.

- **Engine code (`js/`)** — MIT, © 2020 Evelyn "Eevee" Woods. Ours to modify freely.
- **Original art / sound / music** (`tileset-lexy*.png`, `tileset-src/`, `music/`, `sfx/`,
  `icons/`) — **CC-BY-SA 4.0**. Usable with attribution + share-alike. Per-track music
  credits are in `js/soundtrack.js`.
- **Bundled level packs** (`levels/lexys-labyrinth.zip`, `levels/lexys-lessons.zip`) —
  eevee's own; the `CCLP*`/`CC2LP1` packs are **community creations, freely distributable
  but not OSI-open-source** and unrelated to the commercial games.

### IP landmines (do NOT introduce)

- ❌ The original `chips.dat` commercial level set — copyrighted, never bundle it.
- ❌ Original commercial sprites / sounds / music.
- ❌ The **"Chip's Challenge"** name is a registered trademark of Bridgestone Multimedia
  Group LLC. This is an **unaffiliated fan project**, used for identification only. Keep
  the disclaimer that ships in `index.html`.

The safe path (already the case here): permissive engine + original CC-BY-SA assets +
community/own levels + our own name.

## Upstream

Original project: https://github.com/eevee/lexys-labyrinth · play it at
https://c.eev.ee/lexys-labyrinth/ · docs on the
[wiki](https://github.com/eevee/lexys-labyrinth/wiki).
