# Jarvis's Junction — v1 Design Definition

_Status: agreed scope, pre-art. Source of truth for what v1 is (and isn't)._

## North star

A **butler-themed** take on the classic tile puzzler, built on the open-source
Lexy's Labyrinth engine. You are **Jarvis**, butler to the Master of the House;
every level is a **duty**. What makes it feel modern is **not** re-adding QoL the
engine already has (rewind, turn-based, editor, replays, touch) — it's:

1. **Feel** — it plays like a 2020s game in the hand.
2. **Diegesis** — the whole shell reads as a butler's service, so it's
   *Jarvis's Junction*, not a Chip's Challenge clone with a new logo.

The theme is the modernization strategy, not decoration.

## Ruleset decision

**Fair-modern default = Lynx-fair, deterministic rules. No unfair MS-era bugs.**
"Speedrun tech" (boosting, etc.) may return later as an opt-in advanced mode, but
levels are designed for fair rules. Not player-selectable in v1.

## In scope for v1

### Pillar 1 — Game feel / juice
- Input buffering + a few frames of move leniency (responsive fast play).
- Juice pass: squash/stretch on Jarvis, screen-shake on bombs, pickup particles,
  a "duty complete" flourish at the exit.
- First-class game-speed slider (casual ↔ brisk).
- Mobile haptics (Vibration API) on collect/complete/fail.
- _Sound reflavor is asset-dependent — wire the hooks now, swap bespoke audio in
  during the later asset pass (household sounds: bell, lock clunk, teacup)._

### Pillar 2 — Look / diegetic UI  (CSS/UI only; tileset art deferred)
- Reframe the app shell as **the butler's ledger / the day's agenda**: HUD chrome,
  menu framing, "the Master's notes."
- Manor atmosphere via CSS: vignette, warm lamplight tint, optional parallax
  backdrop behind the grid.
- Theme the existing light/dark toggle as **day shift / night shift**.

### Pillar 4 — Campaign & hub
- A **manor-map hub** where rooms unlock (Kitchen, Library, Gardens, …); each room
  is a themed cluster of duties, escalating to a **"Dinner Party" boss level**.
- Short **story beats** between levels — dry butler wit from the Master's notes.
- An **original level pack** whose levels are **named as chores** ("Fetch the
  Morning Paper", "Polish the Silver"). Levels use the **existing tiles/behaviors**
  and existing art — the chore identity is in the *name and framing*, not new tiles.

### Pillar 5 — Meta / progression
- **Medals / par times** per duty: bronze/silver/gold ("done / done well / done
  impeccably").
- **"Employee of the Month"** achievement wall.
- **Daily Duty** — one deterministic seeded level per day (shareable result;
  sharing is local/URL, no server).
- Cosmetic unlocks (outfits / a cat companion) — carrot only, no balance risk.

### Pillar 7 — Accessibility
- Colorblind-safe key/lock palette (CC's one genuinely unfair spot).
- Remappable keys; honor `prefers-reduced-motion`; per-level text descriptions.

## Explicitly OUT of scope for v1

- **New gameplay mechanics or new tile types** (Pillar 3). v1 changes **zero tile
  behaviors**. Levels are authored from the existing tile vocabulary.
- **Redrawn / original tileset art** (the Pillar 2 🔴 item). v1 ships on eevee's
  original **CC-BY-SA** `tileset-lexy` art. A bespoke butler tileset is a later
  milestone.
- **Servers / accounts** (Pillar 6): global leaderboards, cloud save. These need a
  backend (Cloudflare Worker + D1 flavor), not plain GitHub Pages — phase 2.

## Art direction — DECIDED (2026-07-08)

**Cozy cottage / lived-in** — soft, homey, warm: wood, rugs, plants, warm clutter.
Friendlier than a grand manor; pairs with the brass UI. Approach: **procedural
start** (I generate the geometric terrain tiles), **character/monster art in a
later dedicated pass** (Aseprite / artist / AI — the sprites are real pixel art).

Started: cozy wood-plank **floor**, honey-**brick wall**, soft **water** — see
`tileset-src/make-cottage-tiles.py` (Pillow, composited into `tileset-lexy.png`).
Next terrain: gravel, dirt, fire, ice, then the decorative custom-colour tiles;
then the character/monster pass.

- Still open: bespoke SFX/music sourcing (wall-bump is now a synthesized grunt;
  `sfx/make-grunt.py`).

## Rough build order

1. Ship the standard package + dev/prod sites (in progress) so every change is
   visible on the dev URL.
2. Pillar 2 diegetic UI shell + Pillar 1 juice/feel (pure code, no assets) — the
   fastest way to make it *feel* like ours.
3. Pillar 7 accessibility (cheap, do alongside the UI pass).
4. Pillar 5 progression scaffolding (medals, Daily Duty, achievements).
5. Pillar 4 campaign: hub map + author the first chore-named level pack.
6. Later: asset pass (tileset + audio), then Pillar 6 servers.

## v1 success criteria

- Feels responsive and juicy on desktop **and** phone.
- Reads unmistakably as "a butler's duties" from the first screen, with no new
  tiles and no new art.
- A short authored campaign (one manor "wing") is playable end-to-end with medals
  and a hub.
