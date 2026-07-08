# Jarvis's Junction — project context

A butler-themed browser tile-puzzle game. **Fork of
[Lexy's Labyrinth](https://github.com/eevee/lexys-labyrinth)** (eevee, MIT engine +
CC-BY-SA original assets), reskinned so the player is *Jarvis*, butler to the
Master of the House, and every level is another duty on today's list. It's a
from-scratch, Chip's Challenge-*compatible* engine — no commercial assets.

- **Stack:** vanilla JS (ES modules), HTML5 Canvas, **no build step**. Static site.
- **Repo:** `BrewerIndustries/jarvis-junction` (public, for GitHub Pages).
- **Play:** https://jarvis-junction.dabrewer.dev/ (prod) · `/dev/` (dev).

## Environments (GitHub Pages, one site, two paths)

| Env  | Branch | Path    | URL                                      |
| ---- | ------ | ------- | ---------------------------------------- |
| DEV  | `dev`  | `/dev/` | https://jarvis-junction.dabrewer.dev/dev/ |
| PROD | `main` | `/`     | https://jarvis-junction.dabrewer.dev/     |

`.github/workflows/pages.yml` (on `dev`) checks out both branches → `/` and
`/dev/`. **Push to `dev`** rebuilds both; **pushing `main` does NOT auto-deploy** —
re-run the Action. See `deploy/README.md`.

## Workflow ⚠️

- **Work on `dev`.** Promote to `main` **only via a PR the owner approves** — never
  fast-forward or reset-push.
- Update `README.md` after meaningful changes.

## Where things live (engine inherited from upstream, `js/`)

- `game.js` — deterministic simulation core (the tick engine).
- `tiletypes.js` — every tile & creature behavior.
- `format-dat.js` / `format-c2g.js` / `format-tws.js` — CC1 DAT/CCL, CC2 C2M/C2G, replay parsers.
- `renderer-canvas.js`, `tileset.js` — Canvas rendering.
- `main.js` — UI/app shell; **`BUILTIN_PACKS`** (~line 2732) is the level-pack catalog.
- `editor/` — in-browser level editor. `headless/bulktest.mjs` — Node test harness.

## Reskin surface (butler theme)

- `index.html` — splash `<h1>`, tagline, `#splash-premise`, "Today's duties"
  heading, trademark disclaimer (⚠️ keep it).
- `js/main.js` `BUILTIN_PACKS` — pack titles/descriptions. Lead pack =
  "Jarvis's Orientation".
- **Next content milestone:** author an original butler-campaign level pack whose
  level names are household chores (the current packs are eevee's / community CC
  packs, kept with honest attribution).

## Licensing ⚠️ (see README)

MIT engine (© eevee) — keep `LICENSE`. Original art/sound/music CC-BY-SA 4.0.
Never bundle the commercial `chips.dat`, original sprites/audio, or use the
"Chip's Challenge" trademark beyond identification. Unaffiliated fan project.
