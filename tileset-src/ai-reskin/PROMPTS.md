# AI reskin kit — turn Lexy (the fox) into Jarvis (the butler)

Everything here is for feeding an image model (ChatGPT / GPT‑image) **one pose block at
a time** — the reliable way to do it. Each block = attach two images (the fox pose strip
+ the butler reference) and paste the prompt. Assemble the finished frames back onto the
sheet afterward, then clean up in the in‑app editor.

## The character (paste this description whenever asked)

> **Jarvis** — a butler. Dark side‑parted hair, pale skin, black/charcoal **tailcoat**,
> **white shirt‑front**, **crimson bow‑tie**. Small, chunky, friendly pixel‑art body.

Reference image: **`jarvis-reference.png`** (front view; it's the only view that exists
yet — the model must infer back/side views from it plus the fox's poses).

## The blocks

Each fox strip is the original **Lexy** protagonist. Cells are **32×32**, shown at 8×
(walk) / 7× (the rest) so you can see them. Left‑to‑right = animation order. On the
`swim` / `push` / `special` sheets, the **grey left column is a label, not a sprite** —
tell the model to ignore it.

| # | Attach (Image A) | Frames | What it is |
|---|---|---|---|
| 1 | `pose-walk-south.png` | 8 | walk cycle, facing the camera |
| 2 | `pose-walk-north.png` | 8 | walk cycle, facing away |
| 3 | `pose-walk-east.png`  | 8 | walk cycle, facing right |
| 4 | `pose-walk-west.png`  | 8 | walk cycle, facing left |
| 5 | `pose-swim.png`   | 4 dirs × 2 | swimming — head above a **blue water splash** |
| 6 | `pose-push.png`   | 4 dirs × 3 | pushing/straining against a block |
| 7 | `pose-special.png`| skate ×4, burned ×4, exit ×1 | ice‑skating spin; grey **defeated** pose w/ motion lines; happy **win** pose with a heart |

Do them in that order. Verify block 1 looks like Jarvis before spending prompts on the rest.

## The prompt (one per block)

Attach **Image A** (the pose strip for this block) and **Image B** (`jarvis-reference.png`),
then paste — filling in the two blanks from the table:

> You are an expert pixel‑art sprite artist for a 32×32 tile game.
>
> **Image A** is a reference strip of my game's protagonist — a small orange‑and‑cream
> **fox** — drawn as **[N] separate 32×32 frames**, left to right, showing **[DESCRIBE:
> e.g. "the 8‑frame walk cycle facing south/the camera"]**. Read each cell as one frame:
> note the exact facing, the leg/arm position, the body bob, and any effect around the
> character (e.g. the blue water splash when swimming). *(If the strip has a grey left
> column, that's just a text label — ignore it, don't reproduce it.)*
>
> **Image B** is my replacement character, **Jarvis the butler**: dark side‑parted hair,
> pale skin, black tailcoat, white shirt‑front, crimson bow‑tie. Study his design and colours.
>
> **Task:** Redraw the strip **frame‑for‑frame with Jarvis instead of the fox.** In each
> cell Jarvis must be doing the **exact same thing** the fox is — same facing, same
> animation phase (which foot/arm is forward, the bob), same size and position inside the
> 32×32 cell so it stays grid‑aligned. **Keep any effects** around him (the water splash,
> motion lines, the win‑pose heart) — just swap the creature.
>
> **Hard rules:** true pixel art at 32‑px cells — **hard edges, no anti‑aliasing or blur**,
> a small flat palette, 1‑px dark outline, and **Jarvis identical across every frame**.
> Output must be a single horizontal strip of **[N] equal 32×32 cells** (so **[N×32]×32**
> logical pixels), **transparent background**, nothing shifted off the grid. Change only
> the character.

For the multi‑direction sheets (5–7), add:

> This sheet has several rows — one per direction/state (labelled on the left). Produce the
> **same rows in the same order**, each redrawn with Jarvis, keeping every effect.

## After you get frames back

1. It'll likely come back larger and a bit soft — **downscale to 32 px per cell** (nearest‑
   neighbour) in any editor.
2. Open **Options → Tilesets → Duplicate "Lexy (original)"**, name it e.g. *"Jarvis (AI)"*,
   then **Edit** it. Drop each frame into its cell (the cell numbers/legend match the layout).
3. Turn on **Compare → "Lexy (original)"** as the ghost and use the **👻 ghost brush** to
   trace/patch anything the model got slightly wrong. The grid + palette tools do the last 10%.

## Notes

- **`player2` (Cerise)** is a second, pinker character at rows 4–7 of the sheet (same pose
  set). Not included here — ask and I'll generate her strips too.
- The **monsters** are *different creatures* (bug, glider, ball, tank…), not the protagonist
  — leave them as Lexy, or reskin separately later.
- **Licensing:** these poses are eevee's **CC‑BY‑SA 4.0** Lexy's Labyrinth art. Anything a
  model derives from them stays a CC‑BY‑SA derivative — keep the attribution and share‑alike.

*Generated from `reference-lexy.png` (fox poses) + `tileset-lexy.png` (butler), lexy layout
player block = cols 16–31, rows 0–3.*
