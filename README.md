# Jarvis's Junction

A modern, browser-based tile puzzle game — a friendly reimagining of the classic
early-'90s grid puzzler. **Jarvis's Junction is a fork of
[Lexy's Labyrinth](https://github.com/eevee/lexys-labyrinth) by eevee**, which is
itself an open-source, from-scratch reimplementation (it ships completely original
artwork, sound, and music — none of the original commercial game's assets).

It's static JS with **no build system**: serve the directory and open it in a browser.

## Status

- ✅ Forked from Lexy's Labyrinth upstream (2026-07-06), engine runs unmodified.
- ✅ Rebranded visible title to *Jarvis's Junction* (`index.html`).
- ✅ Removed `tileset-tworld.png` (the vendored Tile World tileset — unused by the app
  and belongs to its owners).
- ⏳ Deeper reskin (own icon/sprites/name inside the engine + editor) — not yet done.
- ⏳ Deploy wiring (`.jarvis.json`, Launcher/Dashboard registry, subdomain) — not yet done.

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
